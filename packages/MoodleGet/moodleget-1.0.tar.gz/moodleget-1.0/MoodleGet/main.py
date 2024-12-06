from requests import post
from datetime import datetime, timedelta

class MoodleAPI:
    def __init__(self, url, token):
        self.url = url
        self.token = token
    
    def call(self, function:str, data:dict={}, params={}):
        """
        Send a post request to Moodle with given function, data and parameters\n
        Returns the response from Moodle in json format
        """
        
        if data == {}:
            data = {
                "wstoken": self.token,
                "wsfunction": function,
                "moodlewsrestformat": "json"
            }

        intial_response = post(self.url, params=params, data=data)
        if intial_response.status_code == 200:
            response = intial_response.json()
        else:
            raise Exception(f"Could not connect to the site, status code: f{response.status_code}")

        return response

    def get_courses(self) -> tuple:
        """
        Finds all users courses and returns all the info from courses and a list containing all the course id-s
        """
        courses_list = self.call("core_course_get_recent_courses")
        courses_dict = {}
        course_names_list = []
        course_id_list = []
        course_code_list = []
        for course in courses_list:
            code = course["shortname"]
            id = course["id"]
            name = course["fullname"]
            courses_dict[id] = [code, name]
            course_id_list.append(id)
            course_names_list.append(name)
            course_code_list.append(code)
        return (courses_dict, course_id_list)

    def get_calendar_events(self, course_ids:list) -> list:
        """
        Gets all calendar events from now until 3 weeks from now and returns the events and their info in a list
        """
        unix_time = int((datetime.now() - datetime(1970, 1, 1)).total_seconds())
        unix_3_weeks = int((datetime.now() + timedelta(weeks=3) - datetime(1970, 1, 1)).total_seconds())
        data = {
            "options[userevents]": 0,
            "options[siteevents]": 0,
            "options[timestart]": unix_time,
            "options[timeend]": unix_3_weeks,
            "options[ignorehidden]": 0
        }
        for idx, course_id in enumerate(course_ids):
            data[f"events[courseids][{idx}]"] = course_id
        moodle_response = self.call("core_calendar_get_calendar_events", data)
        events = moodle_response["events"]
        events_list = []
        for event in events:
            event_id = event["id"]
            name = event["name"]
            description = event["description"].strip()
            events_course_id = event["courseid"]
            exercise_type = event["modulename"]
            event_starttime = event["timestart"]
            events_list.append([event_id, name, events_course_id, exercise_type, event_starttime])
        return events_list