class Bullet:
    def __init__(self, angle, player_id, player_center):
        self.angle = angle
        self.x = player_center[0]
        self.y = player_center[1]
        self.owner = player_id
