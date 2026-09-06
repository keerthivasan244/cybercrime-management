import requests
import time
import os

BASE_URL = "http://localhost:8000/api"

docs = [
    {
        "case_id": "CASE-101",
        "source_type": "text",
        "filename": "surveillance_report.txt",
        "content": "On October 12, 2023, John Doe was seen at the Blue Warehouse in Miami. He was observed speaking with Jane Smith. Jane Smith later made a transfer of $10,000."
    },
    {
        "case_id": "CASE-101",
        "source_type": "text",
        "filename": "interrogation.txt",
        "content": "Subject Jane Smith denied knowing John. However, phone records indicate she called Johnathan Doe on October 10."
    },
    {
        "case_id": "CASE-102",
        "source_type": "text",
        "filename": "financial_records.txt",
        "content": "A sum of $10,000 was moved from Jane Smith's account to a shell company in the Cayman Islands. The Blue Warehouse is owned by the shell company."
    }
]

def seed():
    print("Uploading evidence...")
    for d in docs:
        files = {'file': (d["filename"], d["content"].encode('utf-8'))}
        data = {'case_id': d["case_id"], 'source_type': d["source_type"]}
        res = requests.post(f"{BASE_URL}/upload", files=files, data=data)
        print(f"Uploaded {d['filename']}: {res.json()}")
    
    print("Waiting 5 seconds for background extraction tasks to finish...")
    time.sleep(5)
    
    print("Running Entity Resolution...")
    res = requests.post(f"{BASE_URL}/resolve")
    print(res.json())
    
    print("Syncing to Neo4j Knowledge Graph...")
    res = requests.post(f"{BASE_URL}/sync_graph")
    print(res.json())
    
    print("Running Anomaly Detection...")
    res = requests.post(f"{BASE_URL}/anomalies/detect")
    print(res.json())

    print("Seed complete.")

if __name__ == "__main__":
    # Ensure backend is running before executing this
    seed()
