---
title: Traffic Signal Control (OpenEnv)
emoji: ✅
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8000
---

# ✅ Traffic Signal Control: AI-Driven Urban Mobility

### ⑥ [**Download & View Project Presentation (PPTX)**](https://drive.google.com/file/d/1Xe51I16zyZRNwBByJBlccIn8j6pjjm-y/view?usp=sharing)

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/omegist16/traffic-openenv-challenge)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Project Overview
An intelligent traffic management environment designed for high-density urban scenarios, specifically optimized for **Indian road conditions**. This project implements a sophisticated simulation where AI agents must balance throughput against unpredictable emergency vehicle arrivals.

### ➀ Unique Selling Points
- **Software-Only Architecture**: Lightweight Docker-based environment for instant deployment.
- **Emergency Priority System**: Real-time detection and handling of emergency vehicles with high reward weighting.
- **India Focus**: High arrival rates and asymmetrical flow patterns reflecting real-world urban chaos.
- **OpenEnv Compliant**: Standardized API for seamless LLM or RL agent integration.

---

## ⏐ Code Structure
| File/Folder | Purpose |
|:---|:---|
| `server/` | Core backend: FastAPI app, Pydantic models, and Traffic Environment logic. |
| `client.py` | Python wrapper for interacting with the environment API via HTTP. |
| `grader.py` | Official scoring engine (0.0 - 1.0) based on throughput and emergency handling. |
| `baseline_working.py` | Heuristic-based baseline demonstration showing compliant interaction. |
| `inference.py` | Production-ready script for running agents against the live server. |
| `Dockerfile` | Containerization for reliable Hugging Face Space hosting. |

---

## ✅ OpenEnv Compliance Note
This project fully implements the OpenEnv interface requirements. While the `openenv.Environment` base class is currently unavailable on PyPI, the environment exposes all mandatory endpoints (`/reset`, `/step`, `/observation_space`, `/action_space`) required for standardized evaluation.

---

## ⌛ Performance Benchmarks (Official Grader)
- **✃ Easy Mode**: `0.700` (Arrival Rate: 0.1)
- **✃ Medium Mode**: `0.500` (Arrival Rate: 0.3)
- **✃ Hard Mode**: `0.500` (Arrival Rate: 0.5)

---

## ⚙️ How to Use

### 1. Reset the Environment
```bash
curl -X POST "http://localhost:8000/reset?difficulty=medium"
```

### 2. Take an Action
```json
POST /step
{
  "action_type": "activate_emergency_mode"
}
```

### 3. Run the Baseline
```bash
python baseline_working.py
```

Developed for the OpenEnv Hackathon Challenge.