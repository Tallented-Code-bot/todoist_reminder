import json
import requests
import todoist
import functions

with open("config.json","r") as config_file:
	config=json.load(config_file)


CANVAS_TOKEN=config["canvas_token"]

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
	today=functions.get_today()
	response=requests.get(
		f"https://rsd.instructure.com/api/v1/courses/{course}/assignments",
		headers={
			"Authorization": f"Bearer {CANVAS_TOKEN}"
		}
	).json()

	response_due=functions.get_date_object(response["due_at"])
	if functions.is_one_datetime_before_another(today, response_due):
		# If the due date is in the future
		todoist.create_todoist_task(response["name"])
			
# course=get_current_courses()[0]["id"]
# print(todoist.create_todoist_task("This is a test",priority=3))
# print(get_current_assignments(course))