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
	assignments=requests.get(
		f"https://rsd.instructure.com/api/v1/courses/{course['id']}/assignments",
		headers={
			"Authorization": f"Bearer {CANVAS_TOKEN}"
		},
		params={
			"bucket":"future"
		}
	).json()
	print(f"Testing course with name:{course['originalName']} and id:{course['id']}...")	
	i=functions.is_value_in_list(course["id"],"course_id",config["course_locations"])

	if i is False:
		print("Bad course, returning...")
		return
	for assignment in assignments:
		print("testing assignment...")
		assignment_due=functions.get_date_object(assignment["due_at"])
		if functions.is_one_datetime_before_another(today, assignment_due):
			# If the due date is in the future
			locations=config["course_locations"][i]
			print(f"Creating todoist task {assignment['name']}")
			parent_task=todoist.create_todoist_task(
				assignment["name"],
				project=locations["todoist_project_id"],
				section=locations["todoist_section_id"]
			)
			todoist.create_todoist_task(
				assignment["name"]+" due",
				project=locations["todoist_project_id"],
				section=locations["todoist_section_id"],
				parent_task=parent_task["id"],
				labels=locations["todoist_label_ids"],
				due_datetime=assignment["due_at"]
			)

		else:
			print(f"Assignment too early({assignment['due_at']}), skipping...")


# course=get_current_courses()[0]["id"]
# print(todoist.create_todoist_task("This is a test",priority=3))
# print(get_current_assignments(course))
courses=get_current_courses()
for course in courses:
	get_current_assignments(course)
