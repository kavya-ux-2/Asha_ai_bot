# tools/mentor_tool.py

import csv
import os

def get_mentors(limit=5):
    try:
        file_path = os.path.join("data", "job_listing_data.csv")
        mentors = []

        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                mentors.append({
                    "name": row.get("mentor_name"),
                    "expertise": row.get("expertise"),
                    "availability": row.get("availability"),
                    "email": row.get("email")
                })
                if len(mentors) >= limit:
                    break

        return mentors

    except Exception as e:
        print(f"[Mentor Tool] Error reading mentorship data: {e}")
        return []


# test_mentor_tool.py (optional test)

from tools.mentor_tool import get_mentors

mentors = get_mentors()

for mentor in mentors:
    print(f"{mentor['name']} ({mentor['expertise']}) - Available: {mentor['availability']}")
    print(f"Contact: {mentor['email']}\n")
