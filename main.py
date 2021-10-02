from dotenv import load_dotenv
from datetime import date,datetime,timezone
from win10toast import ToastNotifier
from dateutil import parser
import os
import requests




load_dotenv()
todoist_token=os.getenv("TODOIST_TOKEN")
n=ToastNotifier()


# scheduler=Scheduler()
# scheduler.start()

def get_date_object(date_string):
	# return iso8601.parse_date(date_string)
	return parser.parse(date_string).astimezone()
	


def showNotification(task):
	content=task["content"]
	description=task["description"]
	if description=="":
		description =" "
	if content=="":
		content =" "

	n.show_toast(content,description)
	# notification.notify(
	# 	title=content,
	# 	message=description,
	# 	app_icon=None,
	# 	timeout=5
	# )

def getTasksFromTodoist():
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

def getLabelsFromTodoist():
	return requests.get(
		"https://api.todoist.com/rest/v1/labels",
		headers={
			"Authorization": "Bearer %s" % todoist_token
		}
	).json()

def getTasksToday(list=None):
	today=datetime.now(timezone.utc).astimezone().replace(microsecond=0)

	response=getTasksFromTodoist()
	if list is None:
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
				if list is not None:
					if item not in list:	
						list.append(item)
				else:
					tasks.append(item)
	if list is None:	
		return tasks


	

# exec_date=date()
# show_notification(getTasksFromTodoist())
# print(getLabelsFromTodoist())
# tasks=getTasksToday()
tasks=[]

getTasksToday(tasks)

for task in tasks:
	showNotification(task)

# print(tasks)
# print()
# print(len(tasks))
