import os
from win10toast import ToastNotifier
from dotenv import load_dotenv
from datetime import datetime,timezone
import requests
import json
import uuid
import functions

n=ToastNotifier()
load_dotenv()
todoist_token=os.getenv("TODOIST_TOKEN")
def show_notification(task):
	"""Shows a notification for a given task."""
	content=task["content"]
	description=task["description"]
	if description=="":
		description =" "
	if content=="":
		content =" "

	n.show_toast(content,description)
	complete_task(task)

def create_todoist_task(content,description=None,project=None,section=None,parent_task=None,labels=None,priority=None,due_datetime=None):
	"""Creates a task in todoist.

	:param content:The name of the task.
	:type content:string
	:param description:The task description.
	:type description:string
	:param project:The id of the project to put the task in.
	:type project:integer
	:param section:The id of the section to put the task in.
	:type section:integer
	:param parent_task:The id of this task's parent task.
	:type parent_task:integer
	:param label:A list of label ids to apply to the task.
	:type label:list
	:param priority:The priority of the task.
	:type priority:integer
	:param due_datetime:The datetime that the task is due, in rfc3339 format.
	:type due_datetime:string
	"""


	return requests.post(
		"https://api.todoist.com/rest/v1/tasks",
		data=json.dumps({
			"content":content,
			"description":description,
			"project_id":project,
			"section_id":section,
			"parent_id":parent_task,
			"label_ids":labels,
			"priority":priority,
			"due_datetime":due_datetime
		}),
		headers={
			"Content-Type":"application/json",
			"X-Request-Id":str(uuid.uuid4()),
			"Authorization":f"Bearer {todoist_token}"
		}
	).json()


def get_tasks_from_todoist():
	"""Get all your tasks from todoist, filtering by label."""
	return requests.get(
		"https://api.todoist.com/rest/v1/tasks",
		params={
			"label_id":2158391266
			# filter:"@label & tomorrow"
		},
		headers={
			"Authorization": f"Bearer {todoist_token}"
		}
	).json()

def get_labels_from_todoist():
	"""Get all your todoist labels and return them as json."""
	return requests.get(
		"https://api.todoist.com/rest/v1/labels",
		headers={
			"Authorization": f"Bearer {todoist_token}"
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
			due=functions.get_date_object(due)
			if due.day==today.day:
				# tasks.append(due)
				if output is not None:
					if item not in output:
						output.append(item)
				else:
					tasks.append(item)
	if list is None:
		return tasks

def update_jobs(scheduler,tasks):
	"""Add tasks to the scheduler, making sure there are no duplicates."""
	current_jobs=scheduler.get_jobs()

	for task in tasks:
		job_in=False
		for job in current_jobs:
			# Iterate through the jobs and see if the job for this task is there
			if job.args[0] == task:
				job_in=True
		if not job_in:
			#if it is not there, add it.
			scheduler.add_job(show_notification,'date',run_date=task["due"]["datetime"],args=[task])


def complete_task(task):
	"""Completes a todoist task"""
	requests.post(
		f"https://api.todoist.com/rest/v1/tasks/{task['id']}/close",
		headers={
			"Authorization":f"Bearer {todoist_token}"
		}
	)

def sync(scheduler,tasks):
	"""Sync tasks and jobs."""
	get_tasks_today(tasks)
	update_jobs(scheduler,tasks)
	scheduler.print_jobs()
