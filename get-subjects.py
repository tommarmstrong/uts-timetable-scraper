from bs4 import BeautifulSoup
import requests
import json

faculties = ("ads", "bus", "comm", "cii", "dab", "edu", "eng", "health", "health-gem", "it", "intl", "law", "sci", "tdi")


def get_faculty_subjects(short_name):
    uri = "http://www.handbook.uts.edu.au/{}/lists/numerical.html".format(short_name)

    r = requests.get(uri)

    soup = BeautifulSoup(r.text, "html.parser")

    content = soup.find(class_="ie-images")

    subjects = []

    anchors = content.find_all('a')

    for anchor in anchors:
        if anchor.text != "Alphabetical list of subjects":
            subject = {
                "code": anchor.text,
                "name": anchor.nextSibling[1:]
            }
            subjects.append(subject)

    return subjects

all_subjects = []

for faculty in faculties:
    all_subjects += get_faculty_subjects(faculty)

with open("./data/subjects.json", 'w') as file:
    file.write(json.dumps(all_subjects))