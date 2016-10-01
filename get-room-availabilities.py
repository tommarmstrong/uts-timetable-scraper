import json
import datetime
import sys
from operator import itemgetter

room_classes = {}

with open("./data/room_classes.json") as file:
    room_classes = json.load(file)


def get_range_dates(date_string):
    year = datetime.date.today().strftime("%Y")

    parts = date_string.split("-")

    if len(parts) == 1:
        return [date_string]

    s0_parts = parts[0].split("/")
    d0 = datetime.date(int(year), int(s0_parts[1]), int(s0_parts[0]))

    s1_parts = parts[1].split("/")
    d1 = datetime.date(int(year), int(s1_parts[1]), int(s1_parts[0]))

    weeks = int((d1 - d0).days / 7)

    dates = []

    for i in range(0, weeks+1):
        d = d0 + datetime.timedelta(days=7*i)
        dates.append(d.strftime("{dt.day}/{dt.month}".format(dt = d)))

    return dates


def get_end_time(start, duration):
    t_parts = start.split(":")
    t = datetime.datetime(year=1, day=1, month=1, hour=int(t_parts[0]), minute=int(t_parts[1]))
    d_parts = duration.split(" ")
    end = t + datetime.timedelta(minutes=int(d_parts[0]))

    return end.strftime("%H:%M")

rooms = {}
availabilities = {}

for room in room_classes:
    # {
    #   days: {
    #       21-09: {
    #           classes: [],
    #           availabilities: []
    #       }
    #   }
    # }

    # {
    #     "weeks": "4/8-8/9, 22/9-20/10",
    #     "start": "18:00",
    #     "duration": "90 min",
    #     "subject_code": "21036",
    #     "day": "Thu",
    #     "activity": "01",
    #     "location": "CB04.03.321 ",
    #     "group": "Lec1"
    # }

    temp_r = {
        "days": {}
    }

    # Figure out when classes are on each day
    if room_classes[room]["classes"]:
        for c in room_classes[room]["classes"]:
            if c["duration"]:

                cl = {
                    "start": c["start"],
                    "end": get_end_time(c["start"], c["duration"]),
                    "subject_code": c["subject_code"]
                }

                date_ranges = c["weeks"].split(", ")
                dates = []

                for ra in date_ranges:
                    dates = get_range_dates(ra)

                for date in dates:
                    if date not in temp_r["days"]:
                        temp_r["days"][date] = {"classes": []}
                    temp_r["days"][date]["classes"].append(cl)

    rooms[room] = temp_r

    # Figure out gaps between classes

    for r in rooms:
        for day in rooms[r]["days"]:
            if "classes" in rooms[r]["days"][day]:
                sorted_classes = sorted(rooms[r]["days"][day]["classes"], key=itemgetter("start"))

                availability = [{
                    "start": "00:00",
                    "end": sorted_classes[0]["start"]
                }]

                for i in range(0, len(sorted_classes)):
                    start = sorted_classes[i]["end"]
                    if (i + 1) < len(sorted_classes):
                        end = sorted_classes[i + 1]["start"]
                    else:
                        end = "23:59"
                    if start != end:
                        availability.append({
                            "start": start,
                            "end": end
                        })

                if r not in availabilities:
                    availabilities[r] = {}

                availabilities[r][day] = availability

with open("./data/simplified_rooms.json", "w+") as file:
    file.write(json.dumps(rooms))

with open("./data/availabilities.json", "w+") as file:
    file.write(json.dumps(availabilities))