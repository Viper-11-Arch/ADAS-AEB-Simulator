import time
import joblib
import pandas as pd

from ZoneLogic import ZoneLogic
from RiskEstimator import RiskEstimator
from DecisionEngine import DecisionEngine
from ZoneEscalator import ZoneEscalator

model = joblib.load("risk_model.pkl")

class AEBSimulation:
    def __init__(self, speed_kmph, distance, speed_change, throttle_change):
        self.speed_kmph = speed_kmph
        self.distance = distance
        self.speed_change = speed_change
        self.throttle_change = throttle_change

        self.risk_score = 0.0
        self.prev_zone = "safe_zone"
        
        self.DELTA_TIME = 0.2
        self.MAX_TIME = 20.0
        self.ML_THRESHOLD = 0.3
        self.STOP_SPEED_KMPH = 1.0
        self.SAFE_CLEAR_DISTANCE = 10
        self.LOW_RISK_THRESHOLD = 0.3
        self.STABLE_TIME_REQUIRED = 0.1
        self.SAFE_APPROACHED_SPEED = 25.0
        self.DRIVER_DESIRED_SPEED = self.speed_kmph

    def run_simulation(self):
        time_log = 0.0
        logs = []
        stable_time = 0.0
        
        while self.distance > 0 and self.MAX_TIME > time_log:
            features = pd.DataFrame([[self.throttle_change, self.speed_change,self.distance]], 
                                    columns = ["throttle_change","speed_change","distance"])
            ml_confi = model.predict_proba(features)[0][1]
            ml_pred = int(ml_confi > self.ML_THRESHOLD)

            base_zone = ZoneLogic(self.speed_kmph, self.distance).compute_zone()
            final_zone = ZoneEscalator(self.prev_zone, base_zone, self.risk_score).escalate_zone()

            self.risk_score = RiskEstimator(ml_pred, ml_confi,self.risk_score,self.speed_kmph,final_zone).risk_score()

            if self.speed_kmph < self.STOP_SPEED_KMPH and self.distance < self.SAFE_CLEAR_DISTANCE:
                stable_time += self.DELTA_TIME
            else:
                stable_time = 0.0

            if stable_time >= self.STABLE_TIME_REQUIRED and self.risk_score < self.LOW_RISK_THRESHOLD:
                if final_zone == "critical_zone":
                    final_zone = "warning_zone"
                elif final_zone == "warning_zone":
                    final_zone = "safe_zone"
                
            if final_zone == "warning_zone":
                target_speed = self.SAFE_APPROACHED_SPEED
            elif final_zone == "safe_zone":
                target_speed = self.DRIVER_DESIRED_SPEED
            else:
                target_speed = 0.0
            
            
            if self.speed_kmph < self.SAFE_APPROACHED_SPEED and self.distance < self.SAFE_CLEAR_DISTANCE:
                self.risk_score *= 0.98

            self.prev_zone = final_zone
            
            action = DecisionEngine(ml_pred, ml_confi, final_zone).decision()

            current_speed_mps = self.speed_kmph / 3.6
            target_speed_mps = target_speed / 3.6

            decel = 0.0
            if current_speed_mps > target_speed_mps:
                if self.prev_zone == "critical_zone":
                    decel = 7.5
                else:
                    decel = 3.5

            current_speed_mps = max(target_speed_mps, current_speed_mps - decel * self.DELTA_TIME)
            self.speed_kmph = current_speed_mps * 3.6

            self.distance -= current_speed_mps * self.DELTA_TIME
            self.distance = max(0.0, self.distance)
            time_log += self.DELTA_TIME
            
            logs.append(
                {
                    "time":time_log,
                    "speed_kmph": self.speed_kmph,
                    "distance": self.distance,
                    "risk": self.risk_score,
                    "zone": final_zone,
                    "action": action
                }
            )           
            time.sleep(0.1)
        
        return pd.DataFrame(logs)


run_simulation = AEBSimulation(70.0,92.0,30, 32)
df = run_simulation.run_simulation()
print(df)
           
        

            





