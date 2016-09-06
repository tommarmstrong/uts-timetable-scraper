from bs4 import BeautifulSoup
import requests


def is_class_row(tag):
    try:
        return tag.attrs["bgcolor"] == "#eeeeee" and tag.attrs["valign"] == "top"
    except Exception:
        pass


def fetch_classes(subject_code):
    url = "https://mysubjects.uts.edu.au/aplus2016/aptimetable?fun=unit_select&flat_timetable=yes"
    data = {
        "student_set": "",
        "teaching_periods": "ALL",
        "campuses": "ALL",
        "filter": "",
        "filter_name": "",
        "faculty": "ALL",
        "unassigned": str(subject_code) + "31269_SPR_U_1_S",
        "assigned": str(subject_code) + "_SPR_U_1_S",
        "activity_types": "ALL",
        "day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "after_time": "08%3A00",
        "before_time": "23%3A00"
    }

    r = requests.post(url, data)

    soup = BeautifulSoup(r.text, "html.parser")
    class_rows = soup.find_all(is_class_row)

    if len(class_rows) == 0:
        print("No classes")

    else:
        classes = []
        for row in class_rows:
            fields = row.find_all("td")
            classes.append({
                "subject_code": subject_code,
                "group": fields[0].text,
                "activity": fields[1].text,
                "day": fields[2].text,
                "start": fields[3].text,
                "duration": fields[4].text,
                "location": fields[5].text,
                "weeks": fields[7].text
            })
        return classes

print(fetch_classes(31269))