from dateutil import parser
def get_date_object(date_string):
	"""Parse a datetime string as a datetime object."""
	# return iso8601.parse_date(date_string)
	return parser.parse(date_string).astimezone()
