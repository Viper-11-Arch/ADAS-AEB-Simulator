class ZoneLogic:
    def __init__(self, speed, distance):
        self.speed = speed
        self.distance = distance
        self.REACTION_TIME = 0.7
        self.SAFETY_MARGIN = 3.0 
        self.DECEL = 5.0

    def compute_zone(self):
        speed_mps = self.speed / 3.6
        effective_distance = self.distance - self.SAFETY_MARGIN

        if effective_distance <= 0:
            return 'critical_zone'
        
        reaction_distance = speed_mps *  self.REACTION_TIME
        braking_distance = (speed_mps ** 2) / (2 * self.DECEL)
        required_distance = braking_distance + reaction_distance

        ttc = effective_distance / speed_mps if speed_mps > 0 else float('inf')

        if ttc < 1.0 or effective_distance <= required_distance:
            return 'critical_zone'
        elif ttc < 2.5 or 1.5 * required_distance >= effective_distance:
            return 'warning_zone'
        else:
            return 'safe_zone'


#aeb = ZoneLogic(speed=100, obstacle_distance=120)
#print(aeb.compute_zone())