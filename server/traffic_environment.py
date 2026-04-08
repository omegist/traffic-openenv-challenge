import random
from .models import LightPhase, Action, Observation

class TrafficEnv:
    def __init__(self):
        self.reset()

    def reset(self, difficulty: str = "easy"):
        self.difficulty = difficulty
        self.rate = {"easy": 0.1, "medium": 0.3, "hard": 0.5}.get(difficulty, 0.1)
        self.queues = {"North": 0, "South": 0, "East": 0, "West": 0}
        self.phase = LightPhase.NS_GREEN
        self.emergency_present = False
        self.emergency_dir = None
        self.step_count = 0
        self.throughput = 0
        self.emergencies_handled = 0
        return self._get_obs()

    def _get_obs(self):
        return {
            "queues": self.queues,
            "current_phase": self.phase.value,
            "emergency_vehicle_present": self.emergency_present,
            "emergency_direction": self.emergency_dir,
            "step_count": self.step_count,
        }

    def step(self, action: Action):
        reward = 0.0
        self.step_count += 1

        if action.action_type == "change_phase":
            self.phase = LightPhase.EW_GREEN if self.phase == LightPhase.NS_GREEN else LightPhase.NS_GREEN
            reward -= 1.0
        elif action.action_type == "extend_green":
            green_dirs = ["North", "South"] if self.phase == LightPhase.NS_GREEN else ["East", "West"]
            for d in green_dirs:
                removed = min(self.queues[d], 2)
                self.queues[d] -= removed
                self.throughput += removed
        elif action.action_type == "activate_emergency_mode":
            if self.emergency_present:
                reward += 15.0
                self.emergencies_handled += 1
                self.emergency_present = False
                self.emergency_dir = None
            else:
                reward -= 10.0

        green_dirs = ["North", "South"] if self.phase == LightPhase.NS_GREEN else ["East", "West"]
        for d in green_dirs:
            if self.queues[d] > 0:
                self.queues[d] -= 1
                self.throughput += 1

        for d in self.queues:
            if random.random() < self.rate:
                self.queues[d] += 1

        if not self.emergency_present and random.random() < 0.05:
            self.emergency_present = True
            self.emergency_dir = random.choice(list(self.queues.keys()))

        done = self.step_count >= 100
        info = {"throughput": self.throughput, "emergencies": self.emergencies_handled}
        return self._get_obs(), reward, done, info