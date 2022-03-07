import json
import requests
import todoist
import functions

with open("config.json", "rt", encoding="utf-8") as config_file:
    config = json.load(config_file)


CANVAS_TOKEN = config["canvas_token"]


def get_current_courses():
    """Get the current courses in canvas."""
    return requests.get(
        "https://rsd.instructure.com/api/v1/dashboard/dashboard_cards",
        headers={"Authorization": f"Bearer {CANVAS_TOKEN}"},
    ).json()


def get_current_user():
    return requests.get(
        "https://rsd.instructure.com/api/v1/users/self",
        headers={"Authorization": f"Bearer {CANVAS_TOKEN}"},
    ).json()


def get_todo():
    # documentation at https://canvas.instructure.com/doc/api/users.html#method.users.todo_items
    return requests.get(
        "https://rsd.instructure.com/api/v1/users/self/todo",
        headers={"Authorization": f"Bearer {CANVAS_TOKEN}"},
        params={"include": "ungraded_quizzes"},
    ).json()


def create_assignments():
    # Get assignments from todo list
    todos = get_todo()
    for todo in todos:
        # if not functions.is_value_in_list(
        # todo["course_id"], "course_id", config["course_locations"]
        # ):
        # continue
        course_locations = config["course_locations"]

        assignment = todo["assignment"]
        location = functions.is_value_in_list(
            todo["course_id"], "course_id", config["course_locations"]
        )

        # todoist.create_todoist_task(todo["assignment"]["name"])
        print(location, assignment["name"])
        base_task = todoist.create_todoist_task(
            assignment["name"],
            project=course_locations[location]["todoist_project_id"],
            section=course_locations[location]["todoist_section_id"],
            # due_datetime=assignment["due_at"],
        )

        todoist.create_todoist_task(
            assignment["name"] + " due",
        )


def get_current_assignments(course):
    """Get the current assignments for a course."""
    today = functions.get_today()
    assignments = requests.get(
        f"https://rsd.instructure.com/api/v1/courses/{course['id']}/assignments",
        headers={"Authorization": f"Bearer {CANVAS_TOKEN}"},
        params={"include": ["submission"], "bucket": "future"},
    ).json()
    print(f"Testing course with name:{course['originalName']} and id:{course['id']}...")
    i = functions.is_value_in_list(
        course["id"], "course_id", config["course_locations"]
    )

    if i is False:
        print("Bad course, returning...")
        return
    locations = config["course_locations"][i]
    tasks = todoist.get_tasks_in_project(locations["todoist_project_id"])
    for assignment in assignments:
        print()
        print(f"testing assignment {assignment['name']}...")
        if functions.is_value_in_list(assignment["name"], "content", tasks):
            print(f"Todoist task {assignment['name']} already exists, skipping...")
            continue
        # 		if "submission" in assignment:
        # 			#print(assignment["submission"])
        # 			if assignment["submission"]["workflow_state"]=="unsubmitted":
        # 				pass
        # 			print(f"Submission user id is {assignment['submission']['user_id']}")
        # 			if assignment["submission"]["user_id"]==config["canvas_user_id"]:
        # 				print("Correct user in submission object")
        # 			else:
        # 				print("Incorrect user in submission object")
        # 			print(f"Canvas assignment {assignment['name']} has been completed, skipping...")
        # 			continue
        assignment_due = functions.get_date_object(assignment["due_at"])
        if functions.is_one_datetime_before_another(today, assignment_due):
            # If the due date is in the future
            print(f"Creating todoist task {assignment['name']}")
            parent_task = todoist.create_todoist_task(
                assignment["name"],
                project=locations["todoist_project_id"],
                section=locations["todoist_section_id"],
            )
            todoist.create_todoist_task(
                assignment["name"] + " due",
                project=locations["todoist_project_id"],
                section=locations["todoist_section_id"],
                parent_task=parent_task["id"],
                labels=locations["todoist_label_ids"],
                due_datetime=assignment["due_at"],
            )
            url = f"https://rsd.instructure.com/courses/{course['id']}/assignments/{assignment['id']}"
            todoist.create_comment(parent_task["id"], url)

        else:
            print(f"Assignment too early({assignment['due_at']}), skipping...")


# course=get_current_courses()[0]["id"]
# print(todoist.create_todoist_task("This is a test",priority=3))
# print(get_current_assignments(course))

# courses = get_current_courses()
# for course in courses:
# get_current_assignments(course)
create_assignments()

# user=get_current_user()
# print(user)


# print(f"Current user id equals user in config.json: {user['id']==config['canvas_user_id']}")
