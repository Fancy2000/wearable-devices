import requests
import json
from clickhouse_driver import Client

client = Client(host='localhost')
client.execute("USE WEARABLE_DEVICES")

print("Enter UID")
UID = input()
print("Enter OAUTH_TOKEN")
OAUTH_TOKEN = input()
print("Enter APP_SECRET_KEY")
APP_SECRET_KEY = input()
print("Enter CLIENT_ID")
CLIENT_ID = input()
url = "https://www.googleapis.com/auth/fitness.blood_pressure.read"
headers = {'content-type': 'application/json',
           'Authorization': 'Bearer %s' % OAUTH_TOKEN}
blood_pressure = requests.get(url, headers=headers)
url = "https://www.googleapis.com/auth/fitness.heart_rate.read"
headers = {'content-type': 'application/json',
           'Authorization': 'Bearer %s' % OAUTH_TOKEN}
heart_rate = requests.get(url, headers=headers)
if heart_rate.status_code != 200 or blood_pressure.status_code != 200:
    raise Exception("Sorry, status code is not available to continue")
blood_pressure = json.loads(blood_pressure.content)
heart_rate = json.loads(heart_rate.content)
merged_dict = {key: value for (key, value) in (blood_pressure.items() + heart_rate.items())}
merged_dict = json.dumps(merged_dict)
print("If you want to put a comment about your health - enter 1, else 0")
is_comment = int(input())
if is_comment == 1:
    print("describe your state of health")
    health_comment = input()
    result = client.execute(f"INSERT INTO data (json) FORMAT JSONAsString {merged_dict}, {'comment: {health_comment}'}")
elif not is_comment:
    result = client.execute(f"INSERT INTO data (json) FORMAT JSONAsString {merged_dict}, {'comment: {''}'}")

