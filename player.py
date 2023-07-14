class Player:
    def __init__(self, id, path_picture, position_x, position_y, angle, is_connected, bullets=[], health=5, score=0):
        self.x = position_x
        self.y = position_y
        self.is_connected = is_connected
        self.id = id
        self.health = health
        self.height, self.width = 50, 50
        self.speed = 5
        self.acc = 0.05
        self.score = score
        self.angle = angle
        self.path = path_picture
        self.bullets = bullets