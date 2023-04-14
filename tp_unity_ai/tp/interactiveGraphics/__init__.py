import requests
from tp_unity_ai.tp.interactiveGraphics.agent import Agent

API_url = "http://localhost:7000"


def get_agents_from_server():
    url = API_url + "/agents"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve agents list. Server returned status code {response.status_code}")
        return None


def get_agent_with_name(agent_name):
    data = get_agents_from_server()

    for key in data:
        val = data[key]
        if val['name'] == agent_name:
            return Agent(val)

    print(f"Failed to retrieve agent with name: {agent_name}")
    return None


def get_agent_with_id(agent_id):
    data = get_agents_from_server()

    for key in data:
        val = data[key]
        if val['id'] == str(agent_id):
            return Agent(val)

    print(f"Failed to retrieve agent with id: {agent_id}")
    return None
