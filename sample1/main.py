# sample_code/main.py
"""
Sample Python application with dead code for testing
"""

import os
import sys
import json
import unused_module  # This import is never used

def used_function():
    """This function is used by main"""
    return "Hello from used function"

def unused_function():
    """This function is never called"""
    return "This will never be seen"

def another_unused_function(param1, param2):
    """Another unused function with parameters"""
    result = param1 + param2
    return result

class UsedClass:
    """A class that is actually used"""
    
    def __init__(self):
        self.value = 42
        
    def used_method(self):
        """This method is called"""
        return self.value * 2
        
    def unused_method(self):
        """This method is never called"""
        return "unused"

class UnusedClass:
    """A class that is never instantiated"""
    
    def __init__(self):
        self.data = []
        
    def method1(self):
        return len(self.data)
        
    def method2(self):
        self.data.append("item")

def helper_function():
    """Helper function used by main"""
    obj = UsedClass()
    return obj.used_method()

def main():
    """Main function"""
    print(used_function())
    print(helper_function())
    
    # This creates some usage
    result = helper_function()
    print(f"Result: {result}")

if __name__ == "__main__":
    main()


# sample_code/utils.py
"""
Utility functions - some used, some not
"""

def utility_function():
    """This utility is used"""
    return "utility result"

def unused_utility():
    """This utility is never used"""
    return "never called"

class UtilityClass:
    """A utility class"""
    
    def __init__(self):
        self.name = "utility"
        
    def get_name(self):
        return self.name


# sample_code/module_with_imports.py
"""
Module that imports and uses some functions
"""

from main import used_function, unused_function  # unused_function import is dead
from utils import utility_function
import json  # This import is used
import pickle  # This import is unused

def process_data():
    """Function that uses imports"""
    result = used_function()
    util_result = utility_function()
    
    data = {"result": result, "util": util_result}
    return json.dumps(data)

def another_function():
    """Another function"""
    return process_data()


# sample_code/completely_unused.py
"""
Entire module that's never imported or used
"""

def dead_function1():
    """Completely dead function"""
    return "dead1"

def dead_function2():
    """Another completely dead function"""
    return "dead2"

class DeadClass:
    """Completely dead class"""
    
    def __init__(self):
        self.value = 0
        
    def dead_method(self):
        return self.value
