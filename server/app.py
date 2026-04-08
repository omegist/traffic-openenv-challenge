from fastapi import FastAPI, HTTPException
from .models import Action
from .traffic_environment import TrafficEnv
import uvicorn

app = FastAPI(title="Traffic Signal Control")
env = TrafficEnv()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/observation_space")
def observation_space():
    return {
        "type": "dict",
        "properties": {
            "queues": {"type": "dict", "additionalProperties": {"type": "integer"}},
            "current_phase": {"type": "string", "enum": ["NS_GREEN", "EW_GREEN"]},
            "emergency_vehicle_present": {"type": "boolean"},
            "emergency_direction": {"type": ["string", "null"]},
            "step_count": {"type": "integer"},
        },
    }

@app.get("/action_space")
def action_space():
    return {
        "type": "dict",
        "properties": {
            "action_type": {
                "type": "string",
                "enum": ["change_phase", "extend_green", "activate_emergency_mode"],
            }
        },
    }

@app.post("/reset")
def reset(difficulty: str = "easy"):
    return env.reset(difficulty)

@app.post("/step")
def step(action: Action):
    try:
        obs, reward, done, info = env.step(action)
        return {"observation": obs, "reward": reward, "done": done, "info": info}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/metrics")
def metrics():
    return {"throughput": env.throughput, "emergencies": env.emergencies_handled}

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860, reload=False)

if __name__ == "__main__":
    main()