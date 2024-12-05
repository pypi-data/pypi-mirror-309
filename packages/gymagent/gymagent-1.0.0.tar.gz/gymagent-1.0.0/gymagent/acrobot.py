class AcrobotV1Agent:
    def decide(self, observation):
        x0, y0, x1, y1, v0, v1 = observation
        if v1 < -0.3:
            action = 0
        elif v1 > 0.3:
            action = 2
        else:
            y = y1 + x0 * y1 + x1 * y0
            if y > 0.:
                action = 0
            else:
                action = 2
        return action
