# lesson 2 ex8
import json

import requests
import time

url_longtime_job = "https://playground.learnqa.ru/ajax/api/longtime_job"

response = requests.get(url_longtime_job)
response_json = json.loads(response.text)
token = response_json['token']
seconds = response_json['seconds']
print("1)", response, response.text)

response = requests.get(url_longtime_job, params={"token": token})
print("2)", response, response.text)
status = json.loads(response.text)["status"]
assert status == "Job is NOT ready"

print(f"3) waiting {seconds} seconds...")
time.sleep(seconds)

response = requests.get(url_longtime_job, params={"token": token})
response_json = json.loads(response.text)
status = response_json["status"]
print("4)", response, response.text)
assert "result" in response_json
assert status == "Job is ready"

