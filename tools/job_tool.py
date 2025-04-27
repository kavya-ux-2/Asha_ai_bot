# tools/job_tool.py

import requests

API_URL = "https://www.arbeitnow.com/api/job-board-api"

def search_jobs(query, limit=5):
    try:
        response = requests.get(API_URL)
        data = response.json()

        # Basic keyword filter
        matching_jobs = []
        for job in data.get("data", []):
            if query.lower() in job["title"].lower() or query.lower() in job["company_name"].lower():
                matching_jobs.append({
                    "title": job["title"],
                    "company": job["company_name"],
                    "location": job.get("location", "Remote/Not Specified"),
                    "url": job.get("url")
                })
            if len(matching_jobs) >= limit:
                break

        return matching_jobs

    except Exception as e:
        print(f"[Job Tool] Error fetching jobs: {e}")
        return []


# test_job_tool.py (optional test)

from tools.job_tool import search_jobs


query = "software"
results = search_jobs(query)

for job in results:
    print(f"{job['title']} at {job['company']} ({job['location']})\nLink: {job['url']}\n")
