
"""
Dead Code Detection using Neo4j
Analyzes Python codebases to identify potentially unused functions, classes, and variables
"""

import ast
import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass
from neo4j import GraphDatabase
import argparse
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class CodeElement:
    name: str
    type: str  # 'function', 'class', 'variable', 'import'
    file_path: str
    line_number: int
    is_used: bool = False
    used_by: Set[str] = None
    
    def __post_init__(self):
        if self.used_by is None:
            self.used_by = set()

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.definitions: List[CodeElement] = []
        self.usages: List[Tuple[str, int]] = [] 
        self.imports: List[CodeElement] = []
        self.current_class = None
        
    def visit_FunctionDef(self, node):
        func_name = node.name
        if self.current_class:
            func_name = f"{self.current_class}.{func_name}"
            
        self.definitions.append(CodeElement(
            name=func_name,
            type='function',
            file_path=self.file_path,
            line_number=node.lineno
        ))
        self.generic_visit(node)
        
    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)
        
    def visit_ClassDef(self, node):
        self.definitions.append(CodeElement(
            name=node.name,
            type='class',
            file_path=self.file_path,
            line_number=node.lineno
        ))
        
        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class
        
    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(CodeElement(
                name=alias.name,
                type='import',
                file_path=self.file_path,
                line_number=node.lineno
            ))
            
    def visit_ImportFrom(self, node):
        module = node.module or ''
        for alias in node.names:
            import_name = f"{module}.{alias.name}" if module else alias.name
            self.imports.append(CodeElement(
                name=import_name,
                type='import',
                file_path=self.file_path,
                line_number=node.lineno
            ))
            
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.usages.append((node.id, node.lineno))
        self.generic_visit(node)
        
    def visit_Attribute(self, node):
        if isinstance(node.ctx, ast.Load):
            # Handle method/attribute calls like obj.method()
            if isinstance(node.value, ast.Name):
                attr_name = f"{node.value.id}.{node.attr}"
                self.usages.append((attr_name, node.lineno))
        self.generic_visit(node)

class Neo4jDeadCodeDetector:
    
    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        self.code_elements: Dict[str, CodeElement] = {}
        
    def close(self):
        self.driver.close()
        
    def clear_database(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            logger.info("Cleared existing Neo4j data")
            
    def analyze_directory(self, directory_path: str) -> None:
        logger.info(f"Analyzing directory: {directory_path}")
        
        for root, dirs, files in os.walk(directory_path):
            dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', '.venv', 'venv', 'node_modules'}]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    self.analyze_file(file_path)
                    
    def analyze_file(self, file_path: str) -> None:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            tree = ast.parse(content, filename=file_path)
            analyzer = CodeAnalyzer(file_path)
            analyzer.visit(tree)
            
            for definition in analyzer.definitions:
                key = f"{definition.file_path}::{definition.name}"
                self.code_elements[key] = definition
                
            for import_elem in analyzer.imports:
                key = f"{import_elem.file_path}::{import_elem.name}"
                self.code_elements[key] = import_elem
                
            for usage_name, line_num in analyzer.usages:
                self.mark_as_used(usage_name, file_path, line_num)
                
            logger.info(f"Analyzed: {file_path}")
            
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            
    def mark_as_used(self, usage_name: str, file_path: str, line_num: int):
        current_file_key = f"{file_path}::{usage_name}"
        if current_file_key in self.code_elements:
            self.code_elements[current_file_key].is_used = True
            return
            
        for key, element in self.code_elements.items():
            if element.name == usage_name or element.name.endswith(f".{usage_name}"):
                element.is_used = True
                element.used_by.add(f"{file_path}:{line_num}")
                
    def create_graph_nodes(self):
        with self.driver.session() as session:
            for element in self.code_elements.values():
                session.run("""
                    CREATE (e:CodeElement {
                        name: $name,
                        type: $type,
                        file_path: $file_path,
                        line_number: $line_number,
                        is_used: $is_used,
                        id: $id
                    })
                """, 
                name=element.name,
                type=element.type,
                file_path=element.file_path,
                line_number=element.line_number,
                is_used=element.is_used,
                id=f"{element.file_path}::{element.name}"
                )
                
        logger.info("Created Neo4j nodes for code elements")
        
    def create_usage_relationships(self):
        with self.driver.session() as session:
            for element in self.code_elements.values():
                if element.used_by:
                    for usage_location in element.used_by:
                        file_path, line_num = usage_location.rsplit(':', 1)
                        
                        for key, potential_user in self.code_elements.items():
                            if (potential_user.file_path == file_path and 
                                potential_user.line_number < int(line_num)):
                                
                                session.run("""
                                    MATCH (user:CodeElement {id: $user_id})
                                    MATCH (used:CodeElement {id: $used_id})
                                    CREATE (user)-[:USES {line_number: $line_number}]->(used)
                                """,
                                user_id=f"{potential_user.file_path}::{potential_user.name}",
                                used_id=f"{element.file_path}::{element.name}",
                                line_number=int(line_num)
                                )
                                break
                                
        logger.info("Created usage relationships")
        
    def find_dead_code(self) -> List[CodeElement]:
        with self.driver.session() as session:
            result = session.run("""
                MATCH (e:CodeElement)
                WHERE e.is_used = false 
                AND e.type IN ['function', 'class']
                AND NOT e.name STARTS WITH '_'
                AND NOT e.name IN ['main', '__init__']
                RETURN e.name as name, e.type as type, e.file_path as file_path, 
                       e.line_number as line_number
                ORDER BY e.file_path, e.line_number
            """)
            
            dead_code = []
            for record in result:
                dead_code.append(CodeElement(
                    name=record['name'],
                    type=record['type'],
                    file_path=record['file_path'],
                    line_number=record['line_number'],
                    is_used=False
                ))
                
        return dead_code
        
    def get_usage_statistics(self) -> Dict[str, int]:
        with self.driver.session() as session:
            result = session.run("""
                MATCH (e:CodeElement)
                RETURN e.type as type, 
                       COUNT(e) as total,
                       SUM(CASE WHEN e.is_used THEN 1 ELSE 0 END) as used,
                       SUM(CASE WHEN e.is_used THEN 0 ELSE 1 END) as unused
            """)
            
            stats = {}
            for record in result:
                stats[record['type']] = {
                    'total': record['total'],
                    'used': record['used'],
                    'unused': record['unused']
                }
                
        return stats
        
    def run_analysis(self, directory_path: str):
        """Run complete dead code analysis"""
        logger.info("Starting dead code analysis...")
        
        self.clear_database()
        
        self.analyze_directory(directory_path)
        
        self.create_graph_nodes()
        self.create_usage_relationships()
        
        dead_code = self.find_dead_code()
        
        stats = self.get_usage_statistics()
        
        return dead_code, stats

def main():
    parser = argparse.ArgumentParser(description='Dead Code Detection using Neo4j')
    parser.add_argument('directory', help='Directory path to analyze')
    parser.add_argument('--neo4j-uri', default='bolt://localhost:7687', 
                       help='Neo4j URI (default: bolt://localhost:7687)')
    parser.add_argument('--neo4j-user', default='neo4j', 
                       help='Neo4j username (default: neo4j)')
    parser.add_argument('--neo4j-password', default='password', 
                       help='Neo4j password (default: password)')
    parser.add_argument('--output', help='Output file for results')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.directory):
        logger.error(f"Directory not found: {args.directory}")
        sys.exit(1)
        
    detector = Neo4jDeadCodeDetector(args.neo4j_uri, args.neo4j_user, args.neo4j_password)
    
    try:
        dead_code, stats = detector.run_analysis(args.directory)
        
        print("\n" + "="*60)
        print("DEAD CODE DETECTION RESULTS")
        print("="*60)
        
        print("\nSTATISTICS:")
        for code_type, data in stats.items():
            print(f"{code_type.upper()}:")
            print(f"  Total: {data['total']}")
            print(f"  Used: {data['used']}")
            print(f"  Unused: {data['unused']} ({data['unused']/data['total']*100:.1f}%)")
            
        print(f"\nPOTENTIALLY DEAD CODE ({len(dead_code)} items):")
        print("-" * 40)
        
        output_lines = []
        for element in dead_code:
            line = f"{element.type.upper()}: {element.name} ({element.file_path}:{element.line_number})"
            print(line)
            output_lines.append(line)
            
        if args.output:
            with open(args.output, 'w') as f:
                f.write("Dead Code Detection Results\n")
                f.write("=" * 30 + "\n\n")
                f.write("Statistics:\n")
                for code_type, data in stats.items():
                    f.write(f"{code_type}: {data['unused']}/{data['total']} unused\n")
                f.write("\nPotentially Dead Code:\n")
                for line in output_lines:
                    f.write(line + "\n")
            print(f"\nResults saved to: {args.output}")
            
        print("\n" + "="*60)
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        sys.exit(1)
    finally:
        detector.close()

if __name__ == "__main__":
    main()
