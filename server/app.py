from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional, List
from enum import Enum
import random
import uvicorn

class LightPhase(str, Enum):
    NS_GREEN = 'NS_GREEN'
    EW_GREEN = 'EW_GREEN'

class Action(BaseModel):
    action_type: str

class TrafficEnv:
    def __init__(self):
        self.reset()
    def reset(self, difficulty='easy'):
        self.difficulty = difficulty
        self.rate = {'easy': 0.1, 'medium': 0.3, 'hard': 0.5}.get(difficulty, 0.1)
        self.queues = {'North': 0, 'South': 0, 'East': 0, 'West': 0}
        self.phase = LightPhase.NS_GREEN
        self.emergency_present = False
        self.emergency_dir = None
        self.step_count = 0
        self.throughput = 0
        self.emergencies_handled = 0
        return self._get_obs()
    def _get_obs(self):
        return {
            'queues': self.queues, 'current_phase': self.phase,
            'emergency_vehicle_present': self.emergency_present,
            'emergency_direction': self.emergency_dir, 'step_count': self.step_count
        }
    def step(self, action: Action):
        self.step_count += 1
        reward = 0.0
        if action.action_type == 'change_phase':
            self.phase = LightPhase.EW_GREEN if self.phase == LightPhase.NS_GREEN else LightPhase.NS_GREEN
        elif action.action_type == 'activate_emergency_mode' and self.emergency_present:
            self.emergencies_handled += 1
            self.emergency_present = False
            reward += 20.0

        green_dirs = ['North', 'South'] if self.phase == LightPhase.NS_GREEN else ['East', 'West']
        for d in green_dirs:
            if self.queues[d] > 0: self.queues[d] -= 1; self.throughput += 1
        for d in self.queues:
            if random.random() < self.rate: self.queues[d] += 1

        if not self.emergency_present and random.random() < 0.05:
            self.emergency_present = True
            self.emergency_dir = random.choice(list(self.queues.keys()))

        done = self.step_count >= 100
        info = {'throughput': self.throughput, 'emergencies': self.emergencies_handled}
        return self._get_obs(), reward, done, info

app = FastAPI()
env = TrafficEnv()

@app.get('/health')
def health(): return {'status': 'ok'}

@app.get('/observation_space')
def observation_space():
    return {'type': 'dict', 'properties': {'queues': {'type': 'dict'}, 'current_phase': {'type': 'string'}, 'emergency_vehicle_present': {'type': 'boolean'}, 'emergency_direction': {'type': ['string', 'null']}, 'step_count': {'type': 'integer'}}}

@app.get('/action_space')
def action_space():
    return {'type': 'dict', 'properties': {'action_type': {'type': 'string', 'enum': ['change_phase', 'extend_green', 'activate_emergency_mode']}}}

@app.post('/reset')
def reset(difficulty: str = 'easy'): return env.reset(difficulty)

@app.post('/step')
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {'observation': obs, 'reward': reward, 'done': done, 'info': info}

if __name__ == '__main__':
    uvicorn.run("server.app:app", host='0.0.0.0', port=7860)