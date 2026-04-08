import requests

class TrafficClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def health_check(self):
        return requests.get(f"{self.base_url}/health").json()

    def reset(self, difficulty="easy"):
        return requests.post(f"{self.base_url}/reset", params={"difficulty": difficulty}).json()

    def step(self, action_type):
        resp = requests.post(f"{self.base_url}/step", json={"action_type": action_type})
        resp.raise_for_status()
        return resp.json()

    def get_metrics(self):
        return requests.get(f"{self.base_url}/metrics").json()

    def get_observation_space(self):
        return requests.get(f"{self.base_url}/observation_space").json()

    def get_action_space(self):
        return requests.get(f"{self.base_url}/action_space").json()