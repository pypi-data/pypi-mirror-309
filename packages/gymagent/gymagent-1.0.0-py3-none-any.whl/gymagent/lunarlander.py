class LunarlanderV2Agent:
    def decide(self, observation):
        x, y, v_x, v_y, angle, v_angle, contact_left, contact_right = observation

        if contact_left or contact_right: # legs have contact
            f_y = -10. * v_y - 1.
            f_angle = 0.
        else:
            f_y = 5.5 * np.abs(x) - 10. * y - 10. * v_y - 1.
            f_angle = -np.clip(5. * x + 10. * v_x, -4, 4) + 10. * angle + 20. * v_angle

        if np.abs(f_angle) <= 1 and f_y <= 0:
            action = 0 # do nothing
        elif np.abs(f_angle) < f_y:
            action = 2 # main engine
        elif f_angle < 0.:
            action = 1 # left engine
        else:
            action = 3 # right engine
        return action


class LunarLanderContinuousV2Agent:
    def decide(self, observation):
        x, y, v_x, v_y, angle, v_angle, contact_left, contact_right = observation

        if contact_left or contact_right: # legs have contact
            f_y = -10. * v_y - 1.
            f_angle = 0.
        else:
            f_y = 5.5 * np.abs(x) - 10. * y - 10. * v_y - 1.
            f_angle = -np.clip(5. * x + 10. * v_x, -4, 4) + 10. * angle + 20. * v_angle

        action = np.array([f_y, f_angle])
        return action
