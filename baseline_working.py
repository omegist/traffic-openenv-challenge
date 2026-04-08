import time
import requests
from grader import grade_episode

class DirectTrafficClient:
    """Direct client that doesn't need HTTP server"""
    def __init__(self):
        from server.traffic_environment import TrafficEnv
        self.env = TrafficEnv()

    def reset(self, difficulty="easy"):
        return self.env.reset(difficulty=difficulty)

    def step(self, action_type):
        from server.models import Action
        obs, reward, done, info = self.env.step(Action(action_type=action_type))
        return obs, reward, done, info

def run_baseline():
    client = DirectTrafficClient()
    tasks = ['easy', 'medium', 'hard']
    results = []

    print("="*60)
    print("TRAFFIC SIGNAL CONTROL - BASELINE TEST")
    print("="*60)

    for task in tasks:
        print(f"\n--- Testing {task.upper()} ---")
        obs = client.reset(difficulty=task)
        done = False
        step_count = 0
        actions_count = {'change_phase': 0, 'extend_green': 0, 'activate_emergency_mode': 0}

        while not done:
            # FIXED: Use dictionary access instead of attribute access
            if obs['emergency_vehicle_present']:
                action = "activate_emergency_mode"
            elif sum(obs['queues'].values()) > 12:
                action = "change_phase"
            else:
                action = "extend_green"

            obs, reward, done, info = client.step(action)
            actions_count[action] += 1
            step_count += 1

            if step_count % 25 == 0:
                total_queue = sum(obs['queues'].values())
                print(f"  Step {step_count}: queue={total_queue}, throughput={info['throughput']}")

        score = grade_episode(info, task)
        results.append((task, score, info))
        print(f"✅ {task}: Score={score:.3f}, Throughput={info['throughput']}, Emergencies={info['emergencies']}")
        print(f"   Actions: {actions_count}")

    print("\n" + "="*60)
    print("FINAL SCORES")
    print("="*60)
    avg_score = sum(s for _, s, _ in results) / len(results)
    for task, score, info in results:
        print(f"{task.upper()}: {score:.3f} (throughput: {info['throughput']})")
    print(f"\nAverage Score: {avg_score:.3f}")
    return avg_score

if __name__ == "__main__":
    run_baseline()
