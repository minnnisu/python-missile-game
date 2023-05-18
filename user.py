from share import IMAGES_DIR, paintEntity


class User:
    def __init__(self, pygame):
        self.heart = pygame.image.load(IMAGES_DIR + 'heart.png')
        self.heartCount = 3
        self.fireCount = 0

    def increaseFireCount(self):
        self.fireCount += 1

    def decreaseHeart(self):
        self.heartCount -= 1

    def isDie(self):
        return self.heartCount < 1

    def showHeart(self, monitor, sheight):
        for i in range(self.heartCount):  # 남은 하트의 개수를 보여준다
            paintEntity(monitor, self.heart, 220 + (30 * i), sheight - 38)
