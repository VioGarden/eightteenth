import json
import time
start_time = time.time()

f = open('search/fixtures/dataamq.json', 'r')
data = f.read()
f.close()

user = json.loads(data)

array = []

for i in range(len(user)):
    user[i]["show"] = user[i].pop("anime") # user[i]["show"] = user[i]["anime"] >>> del user[i]["anime"]
    user[i]["annid"] = user[i].pop("annid")
    user[i]["song"] = user[i].pop("title")
    user[i]["artist"] = user[i].pop("artist")
    user[i]["opedin"] = user[i].pop("type")
    user[i]["h720"] = user[i].pop("720")
    if user[i]["h720"] == "N/A":
        user[i]["h720"] = ""
    user[i]["h480"] = user[i].pop("480")
    if user[i]["h480"] == "N/A":
        user[i]["h480"] = ""
    user[i]["mp3"] = user[i].pop("mp3")
    if user[i]["mp3"] == "N/A":
        user[i]["mp3"] = ""


    temp_dict = {}
    temp_dict["model"] = "search.AotData"
    temp_dict["pk"] = i
    temp_dict["fields"] = user[i]
    array.append(temp_dict)

file = open('search/fixtures/amqfixture.json', 'a')
file.write(json.dumps(array))
file.close()

print("--- %s seconds ---" % (time.time() - start_time))