class RiskEstimator:
    def __init__(self, ml_prediction, ml_confidence, prev_risk_score, speed_kmph, zone):
        self.ml_prediction = ml_prediction
        self.ml_confidence = ml_confidence
        self.prev_risk_score = prev_risk_score
        self.speed_kmph = speed_kmph
        self.zone = zone
        
        self.ALPHA_MIN = 0.1
        self.ALPHA_MAX = 0.6
    
    def risk_score(self):
        speed_mps = self.speed_kmph / 3.6
        speed_factor = min(speed_mps / 30.0, 1.0)
        alpha = self.ALPHA_MIN + (self.ALPHA_MAX - self.ALPHA_MIN) * speed_factor

        current_obs = self.ml_prediction * self.ml_confidence
        new_risk = ((1 - alpha) * self.prev_risk_score) + (current_obs * alpha)

        if speed_mps < 0.5:
            new_risk *= 0.7
        if self.zone == "critical_zone":
            new_risk = max(new_risk, 0.3)

        return max(0.0, min(1.0, float(new_risk)))

#rsk = RiskScore(1, 0.65,0.0,50,"warning_zone")
#print(rsk.risk_score())