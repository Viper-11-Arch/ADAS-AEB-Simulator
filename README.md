# AI Assisted AEB Simulator

## What it does?
AI Assisted Automated Emergency Braking Simulator combining physics-based safety logic with ML risk estimation

## Architecture
- ZoneLogic - Physics based TTC(Time-To-Collision) calculation
- RiskEstimator - ML Risk Scoring with Exponential Smoothing
- ZoneEscalator - Zone persistance and Escalation
- DecisionEngine - Action decision based on zone and ML confidence
- AEBSimulation - Main orchestrator

## Tech Stack 
- Python
- Pandas
- Scikit-Learn
- Streamlit

## How to run?
- pip install -r requirements.txt
- streamlit run app_v1.py

## Screenshots

### Live Simulation
![Live Simulation](screenshots/Screenshot (640).png)

### Final State
![Final State](screenshots/Screenshot (641).png)

### Risk Analysis
![Risk Analysis](screenshots/Screenshot (642).png)
