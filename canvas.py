import os
import requests
from dotenv import load_dotenv
import todoist

load_dotenv()
CANVAS_TOKEN=os.getenv('CANVAS_TOKEN')

def get_current_courses():
	"""Get the current courses in canvas."""
	return requests.get(
		"https://rsd.instructure.com/api/v1/dashboard/dashboard_cards",
		headers={
			"Authorization":f"Bearer {CANVAS_TOKEN}"
		}
	).json()

def get_current_assignments(course):
	"""Get the current assignments for a course."""
	return requests.get(
		f"https://rsd.instructure.com/api/v1/courses/{course}/assignments",
		headers={
			"Authorization": f"Bearer {CANVAS_TOKEN}"
		}
	).json()

# course=get_current_courses()[0]["id"]
print(todoist.create_todoist_task("This is a test",priority=3))
# print(get_current_assignments(course))