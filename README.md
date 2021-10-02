# Todoist Reminder
This project implements reminders for [Todoist](https://todoist.com).
Todoist already has reminders, but they are a paid feature.

## Installation

``` bash
# Clone the repository
git clone https://github.com/Tallented-Code-bot/todoist_reminder

cd todoist-reminder

# Make a virtual environment
python -m venv env
# Activate it
source env/bin/activate
# Install all the required packages
pip install -r requirements.txt
```
Once you have installed the packages, make a .env file
in the root of the repository with these contents:

``` env
TODOIST_TOKEN=<your todoist token>
```

To get your todoist token, go to todoist.  Click on your 
icon and go to integrations, then scroll down and copy your API token.