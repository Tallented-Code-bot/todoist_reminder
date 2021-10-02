from datetime import datetime,timezone
import os
from dotenv import load_dotenv
from win10toast import ToastNotifier
from dateutil import parser
import requests




load_dotenv()
todoist_token=os.getenv("TODOIST_TOKEN")
n=ToastNotifier()


# scheduler=Scheduler()
# scheduler.start()

def get_date_object(date_string):
	"""Parse a datetime string as a datetime object."""
	# return iso8601.parse_date(date_string)
	return parser.parse(date_string).astimezone()



def show_notification(task):
	"""Shows a notification for a given task."""
	content=task["content"]
	description=task["description"]
	if description=="":
		description =" "
	if content=="":
		content =" "

	n.show_toast(content,description)

def get_tasks_from_todoist():
	"""Get all your tasks from todoist, filtering by label."""
	return requests.get(
		"https://api.todoist.com/rest/v1/tasks",
		params={
			"label_id":2158391266
			# filter:"@label & tomorrow"
		},
		headers={
			"Authorization": "Bearer %s" % todoist_token
		}
	).json()

def get_labels_from_todoist():
	"""Get all your todoist labels and return them as json."""
	return requests.get(
		"https://api.todoist.com/rest/v1/labels",
		headers={
			"Authorization": "Bearer %s" % todoist_token
		}
	).json()


def get_tasks_today(output=None):
	"""
	Gets all your todoist tasks for today that have the reminder label.

	:param output: The list to append to.  This function will not make duplicate items.
	:type output: list

	:rtype:list
	:return: A list of all todoist tasks for today with the reminder label.
	"""
	today=datetime.now(timezone.utc).astimezone().replace(microsecond=0)

	response=get_tasks_from_todoist()
	if output is None:
		tasks=[]

	for item in response:
		# print(item)
		try:
			due=item['due']["datetime"]
		except KeyError:
			continue
		if due:
			due=get_date_object(due)
			if due.day==today.day:
				# tasks.append(due)
				if output is not None:
					if item not in output:
						output.append(item)
				else:
					tasks.append(item)
	if list is None:
		return tasks



# exec_date=date()
# show_notification(getTasksFromTodoist())
# print(getLabelsFromTodoist())
# tasks=getTasksToday()
tasks=[]

get_tasks_today(tasks)

for task in tasks:
	show_notification(task)

# print(tasks)
# print()
# print(len(tasks))
