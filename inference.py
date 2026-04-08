import os
import requests
from client import TrafficClient
from grader import grade_episode

def main():
    task = os.getenv("TASK_NAME", "easy")
    client = TrafficClient(base_url="http://localhost:7860")
    try:
        obs = client.reset(difficulty=task)
    except:
        # Fallback for local testing if server is on 8000
        client = TrafficClient(base_url="http://localhost:8000")
        obs = client.reset(difficulty=task)

    done = False
    while not done:
        if obs["emergency_vehicle_present"]:
            action = "activate_emergency_mode"
        elif sum(obs["queues"].values()) > 12:
            action = "change_phase"
        else:
            action = "extend_green"
        result = client.step(action)
        obs = result["observation"]
        done = result["done"]
        info = result["info"]
    score = grade_episode(info, task)
    print(f"Final score for {task}: {score}")
    return score

if __name__ == "__main__":
    main()