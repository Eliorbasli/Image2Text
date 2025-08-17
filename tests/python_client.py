import requests
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"
BASE_DIR = Path(__file__).resolve().parent


def submit_image(file_path: Path) -> str:
    with file_path.open("rb") as f:
        files = {
            "file": (file_path.name, f, "image/png")
        }
        resp = requests.post(f"{BASE_URL}/submit", files=files)
    resp.raise_for_status()
    return resp.json()["job_id"]


def get_status(job_id: str) -> dict:
    """Check the status of a job."""
    resp = requests.get(f"{BASE_URL}/status/{job_id}")
    resp.raise_for_status()
    status = resp.json()
    print(f"[+] Job {job_id} status -> {status}")
    return status


def get_result(job_id: str) -> str:
    resp = requests.get(f"{BASE_URL}/result/{job_id}")
    if resp.status_code == 202:
        return "(still processing)"
    resp.raise_for_status()
    return resp.text

import time

if __name__ == "__main__":
    
    print("\n#################### Submit file ####################")
    job_id = submit_image(BASE_DIR/"sample_images/sample2.png")
    # job_id2 = submit_image("sample_images/sample2.jpg")
    # job_id3 = submit_image("sample_images/sample3.jpg")
    # job_id4 = submit_image("sample_images/sample4.jpg")

    print(f"Job ID = {job_id}")
    
    while True:
        print("\n#################### Get Status ####################")
        status = get_status(job_id)
        if status["status"] in ("done", "failed"):
            print(f"Job {job_id} completed with status: {status['status']}")
            break
        time.sleep(2)

    if status["status"] == "done":
        print("\n#################### Get Result ####################")
        
        get_result(job_id)
        
        print(f"Result for job {job_id}: {get_result(job_id)}")
