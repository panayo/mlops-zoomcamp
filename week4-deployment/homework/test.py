import requests

date = {"year" : 2021,
        "month": 4}

url = 'http://localhost:9696/predict'
rep = requests.post(url,json = date)

print(rep.json())