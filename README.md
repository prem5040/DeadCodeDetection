# DeadCodeDetection

A tool to detect dead code in your projects using Neo4j for graph-based analysis.

---

## 📋 Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Usage](#usage)
- [License](#license)

---

## 🌟 Features
- Detects unused functions, classes, and variables.
- Uses Neo4j for efficient graph-based code analysis.
- Outputs results in a structured text file.

---

## 🛠 Prerequisites
- Python 3.8+
- Docker and Docker Compose
- Git (optional, for cloning the repository)

---

## 🚀 Setup

1. Clone the Repository (Optional) <br>
git clone repository-url  <br>
cd DeadCodeDetection  <br>


2. Create a Virtual Environment  <br>
python3 -m venv venv

3. Activate the Virtual Environment  <br>
macOS/Linux:  <br>
source venv/bin/activate  <br>
Windows:  <br>
venv\Scripts\activate  <br>

4. Install Dependencies <br>
pip install -r requirements.txt  <br>

5. Start Neo4j with Docker Compose  <br>
docker-compose up -d  <br>

Wait for 30 seconds to ensure Neo4j is fully initialized.<br>
6. Verify Neo4j is Running  <br>
docker-compose ps <br>

You should see the Neo4j container listed as Up.

💻 Usage
1. Access Neo4j Browser <br>
Open your browser and navigate to: <br>
🔗 http://localhost:7474 <br>
Login Credentials: <br>
Username: neo4j <br>
Password: password <br>

2. Run Dead Code Detection <br>
Execute the following command to analyze your code: <br>
python3 deadcode.py ./sample_code --output sample_code_results.txt <br>
Note: Replace ./sample_code with the path to your project directory. <br>

3. View Results <br>
The results will be saved in the specified output file (sample_code_results.txt by default). <br>
