import requests
from typing import Dict, Any

class TrafficClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def reset(self, difficulty="easy") -> Dict[str, Any]:
        response = requests.post(f"{self.base_url}/reset", params={"difficulty": difficulty})
        return response.json()

    def step(self, action_type: str) -> Dict[str, Any]:
        response = requests.post(f"{self.base_url}/step", json={"action_type": action_type})
        return response.json()

    def get_observation_space(self) -> Dict[str, Any]:
        response = requests.get(f"{self.base_url}/observation_space")
        return response.json()

    def get_action_space(self) -> Dict[str, Any]:
        response = requests.get(f"{self.base_url}/action_space")
        return response.json()
