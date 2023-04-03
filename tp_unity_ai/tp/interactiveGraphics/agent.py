import json

import requests

API_url = "http://localhost:7000"


class Agent:
    def __init__(self, agent_json):
        self.name = agent_json.get('name')
        self.id = agent_json.get('id')

    def post_command(self, command, variables=None):
        # Define the URL of the server endpoint
        url = API_url + "/commands"

        # Define the JSON payload to send in the POST request
        payload = {
            "name": self.name,
            "id": self.id,
            "command": command
        }

        if variables:
            for key in variables:
                payload[key] = variables[key]

        # Convert the payload to a JSON string
        json_payload = json.dumps(payload)

        # Set the headers for the POST request
        headers = {
            "Content-Type": "application/json"
        }

        # Send the POST request with the JSON payload
        response = requests.post(url, headers=headers, data=json_payload)

        # Check the status code of the response
        if response.status_code == 200:
            print("Command sent successfully!")
        else:
            print(f"Failed to send command. Server returned status code {response.status_code}")

    def move(self):
        self.post_command("move")

    def stop(self):
        self.post_command("stop")

    def turn_left(self):
        self.post_command("turn_left")

    def turn_right(self):
        self.post_command("turn_right")

    def set_speed(self, speed):
        self.post_command("set_speed", variables={'speed': speed})



