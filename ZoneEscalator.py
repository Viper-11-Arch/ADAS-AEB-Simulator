class  ZoneEscalator:
    def __init__(self, prev_zone, base_zone, risk_score):
        self.prev_zone = prev_zone
        self.base_zone = base_zone
        self.risk_score = risk_score
        self.zone_rank = {
            "critical_zone" : 2,
            "warning_zone" : 1,
            "safe_zone" : 0
        }
    
    def escalate_zone(self): 
        final_zone = max(self.prev_zone, self.base_zone, key = lambda z : self.zone_rank[z])
        if self.risk_score >= 0.85:
            final_zone = "critical_zone"
        elif self.risk_score >= 0.6 and final_zone == "safe_zone":
            final_zone = "warning_zone"
        if self.zone_rank[final_zone] < self.zone_rank[self.base_zone]:
            final_zone = self.base_zone
        return final_zone
    
#zone_escalator = ZoneEscalator("safe_zone","safe_zone", 0.85)
#print(zone_escalator.escalate_zone())