class DecisionEngine:
    def __init__(self, ml_prediction,ml_confidence,zone):
        self.ml_prediction = ml_prediction 
        self.ml_confidence = ml_confidence
        self.zone = zone
        self.CONFIDENCE_THRESHOLD = 0.7
    def decision(self):
        if self.zone == "critical_zone":
            return "EMERGENCY_BRAKE"
        elif self.zone == "warning_zone":
            return "APPLY_BRAKES"
        elif self.zone == "safe_zone":
            if self.ml_confidence >= self.CONFIDENCE_THRESHOLD:
                return "ALERT_DRIVER"
            else:
                return "NORMAL_RIDE"
        else:
            return "NORMAL_RIDE"

#decision_engine = DecisionEngine(1,0.70,"safe_zone")
#print(decision_engine.decision())
