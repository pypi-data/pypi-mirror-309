class PongNoFrameskipAgent:
    def decide(self, observation):
        racket = np.where((observation[34:193, :, 0] == 92).any(axis=1))[0].mean()
        ball = np.where((observation[34:193, :, 0] == 236).any(axis=1))[0].mean()
        return 2 + int(racket < ball)
