import json

data = {"Host": '127.0.0.1',
        "Port": 8081}
with open("parametros.json", "w") as file:
    json.dump(data, file)
