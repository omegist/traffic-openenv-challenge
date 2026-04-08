from enum import Enum
from pydantic import BaseModel
from typing import Dict, Optional

class LightPhase(str, Enum):
    NS_GREEN = "NS_GREEN"
    EW_GREEN = "EW_GREEN"

class Action(BaseModel):
    action_type: str  # change_phase, extend_green, activate_emergency_mode

class Observation(BaseModel):
    queues: Dict[str, int]
    current_phase: LightPhase
    emergency_vehicle_present: bool
    emergency_direction: Optional[str]
    step_count: int