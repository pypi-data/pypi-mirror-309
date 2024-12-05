class CartPoleV0Agent:
    def decide(self, observation):
        position, velocity, angle, angle_velocity = observation
        action = int(3. * angle + angle_velocity > 0.)
        return action
