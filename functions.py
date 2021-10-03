from datetime import datetime,timezone 
from dateutil import parser
def get_date_object(date_string):
	"""Parse a datetime string as a datetime object."""
	# return iso8601.parse_date(date_string)
	return parser.parse(date_string).astimezone()

def get_today():
	"""Return the current date and time in a datetime object with timezone."""
	return datetime.now(timezone.utc).astimezone().replace(microsecond=0)
