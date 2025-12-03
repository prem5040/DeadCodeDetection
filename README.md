# DeadCodeDetection
To run the program:

Create virtual environment 
python -m venv venv 
Activate virtual environment (on mac) 
source venv/bin/activate

Install the requirements
pip install -r requirements.txt

Start Neo4j using Docker Compose 
docker-compose up -d

After 30s,  Check if it's running 
docker-compose ps

Then, Open browser and
http://localhost:7474
Login ID: neo4j
Password: password

Then run the command to get the results:
python3 deadcode.py ./sample_code --output sample_code_results.txt
<img width="468" height="331" alt="image" src="https://github.com/user-attachments/assets/5fb197e6-7376-4178-aca0-b362d920b123" />
