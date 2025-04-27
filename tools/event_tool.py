# tools/event_tool.py

import json
import os

def get_events():
    try:
        file_path = os.path.join("data", "session_details.json")
        with open(file_path, "r", encoding="utf-8") as f:
            events = json.load(f)

        # Optional: Format/shorten results if needed
        formatted_events = [
            {
                "name": event.get("name"),
                "date": event.get("date"),
                "time": event.get("time"),
                "location": event.get("location"),
                "description": event.get("description")
            }
            for event in events
        ]

        return formatted_events

    except Exception as e:
        print(f"[Event Tool] Error loading session data: {e}")
        return []


# test_event_tool.py (optional test)

from tools.event_tool import get_events

events = get_events()

for event in events:
    print(f"{event['name']} on {event['date']} at {event['time']} ({event['location']})")
    print(f"Description: {event['description']}\n")
