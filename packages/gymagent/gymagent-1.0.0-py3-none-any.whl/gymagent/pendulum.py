class PendulumV0Agent:
    def decide(self, observation):
        x, y, angle_velocity = observation
        flip = (y < 0.)
        if flip:
            y *= -1. # now y >= 0
            angle_velocity *= -1.
        angle = np.arcsin(y)
        if x < 0.:
            angle = np.pi - angle
        if (angle < -0.3 * angle_velocity) or \
                (angle > 0.03 * (angle_velocity - 2.5) ** 2. + 1. and \
                angle < 0.15 * (angle_velocity + 3.) ** 2. + 2.):
            force = 2.
        else:
            force = -2.
        if flip:
            force *= -1.
        action = np.array([force,])
        return action
