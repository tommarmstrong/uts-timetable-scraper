from bs4 import BeautifulSoup
import requests
import json
import sys


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
        "unassigned": str(subject_code) + "_SPR_U_1_S",
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


subjects = []

with open("./data/subjects.json") as file:
    subjects = json.load(file)

total = len(subjects)
count = 0

classes = []

for subject in subjects:
    count += 1
    print("{} of {} fetching data for: {} {}".format(count, total, subject["code"], subject["name"]))
    s = subject
    s["classes"] = fetch_classes(subject["code"])
    classes.append(s)


with open("./data/classes.json", "w+") as file:
    file.write(json.dumps(classes))