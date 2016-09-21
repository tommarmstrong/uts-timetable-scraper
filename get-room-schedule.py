import json

subjects = []

with open('./data/classes.json') as file:
    subjects = json.load(file)

room_classes = {}

for s in subjects:
    if s["classes"]:
        for c in s["classes"]:
            location = c["location"].strip()
            locations = [location]
            # Remove date ranges from locations
            if "(" in location:
                parts = location.split(" ")
                locations = []
                for p in parts:
                    if "/" not in p:
                        locations.append(p)

            num_initial_locations = len(locations)

            # Split locations with pluses
            for i in range(0, num_initial_locations):
                if "+" in locations[i]:
                    l = locations[i]
                    split = l.split("+")
                    location_parts = split[0].split(".")
                    level = location_parts[0] + "." + location_parts[1]

                    # Replace element with just first location
                    locations[i] = split[0]

                    # For each split part thereon, create a new location
                    for j in range(1, len(split)):
                        locations.append(level + "." + split[j])

            for l in locations:
                if l not in room_classes:
                    room_classes[l] = {
                        "classes": []
                    }
                room_classes[l]["classes"].append(c)

with open("./data/room_classes.json", "w+") as file:
    file.write(json.dumps(room_classes))
