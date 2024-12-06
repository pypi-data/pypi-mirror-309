from os import environ
from requests import post
from datetime import datetime, timedelta

class MoodleAPI:
    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.kursuste_info, self.kursuste_id_list = self.hangi_kursused()
        self.vaadeldavad_kursused = self.kursuste_id_list
        self.kalendri_info = self.hangi_kalendri_info([7550, 1755, 12774, 10892, 500, 8434])
        self.loetud_sundmused_list = []
    
    # Kutsub Moodle'i API-d kindla argumendiga vastavalt küsitavale infole
    def call(self, funktsioon:str, data:dict={}, params={}):
        if params == {}:
            argumendid = {
                "wstoken": self.token,
                "wsfunction": funktsioon,
                "moodlewsrestformat": "json"
            }
        else:
            argumendid = params

        vastus = post(self.url, params=argumendid, data=data)
        if vastus.status_code == 200:
            vastus2 = vastus.json()
        else:
            vastus2 = f"Kutse ebaõnnestus, status code f{vastus.status_code}"

        return vastus2

    # Leiab ja tagastab kõigi viimatiste Moodle'i kursuste info dictina
    def hangi_kursused(self) -> dict:
        kursuste_list = self.call("core_course_get_recent_courses")
        kursuste_dict = {}
        kursuste_nimed_list = []
        kursuste_id_list = []
        kursuste_kood_list = []
        for kursus in kursuste_list:
            kood = kursus["shortname"]
            id = kursus["id"]
            nimi = kursus["fullname"]
            kursuste_dict[id] = [kood, nimi]
            kursuste_id_list.append(id)
            kursuste_nimed_list.append(nimi)
            kursuste_kood_list.append(kood)
        return kursuste_dict, kursuste_id_list

    # Leiab ja prindib kõik Moodle'i kalendri sündmused
    def hangi_kalendri_info(self, kursuste_idd:list) -> list:
        unix_hetkeaeg = int((datetime.now() - datetime(1970, 1, 1)).total_seconds())
        unixaeg_3_ndl_parast = int((datetime.now() + timedelta(weeks=3) - datetime(1970, 1, 1)).total_seconds())
        data = {
            "options[userevents]": 0,
            "options[siteevents]": 0,
            "options[timestart]": unix_hetkeaeg,
            "options[timeend]": unixaeg_3_ndl_parast,
            "options[ignorehidden]": 0
        }
        for idx, kursuse_id in enumerate(kursuste_idd):
            data[f"events[courseids][{idx}]"] = kursuse_id
        moodle_vastus = self.call("core_calendar_get_calendar_events", data)
        sundmused = moodle_vastus["events"]
        sundmuste_list = []
        for sundmus in sundmused:
            sundmuse_id = sundmus["id"]
            pealkiri = sundmus["name"]
            kirjeldus = sundmus["description"].strip()
            sundmuse_kursuse_id = sundmus["courseid"]
            ulesande_tuup = sundmus["modulename"]
            ulesande_algusaeg = sundmus["timestart"]
            sundmuste_list.append([sundmuse_id, pealkiri, sundmuse_kursuse_id, ulesande_tuup, ulesande_algusaeg])
        return sundmuste_list

def main():
    # Andmed Moodlega ühendamiseks
    token_moodle = environ["MOODLE_TOKEN"]
    url = "https://moodle.ut.ee/webservice/rest/server.php"
    
    # Loon suhtluse API-dega
    moodle_api = MoodleAPI(url, token_moodle)

    


if __name__ == "__main__":
    main()