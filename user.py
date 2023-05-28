import share

class User:
    def __init__(self, pygame):
        self.userName = None
        self.userState = "live"
        self.heart = pygame.image.load(share.IMAGES_DIR + 'heart.png')
        self.heartCount = 3 # 남은 하트 수
        self.fireCount = 0 # 파괴한 괴물 수

    def increaseFireCount(self):
        self.fireCount += 1

    def decreaseHeart(self):
        self.heartCount -= 1

    def isDie(self):
        return self.heartCount < 1

    def showHeart(self, monitor, x, y, distance=30):
        for i in range(self.heartCount):  # 남은 하트의 개수를 보여준다
            monitor.paintEntity(self.heart, x + (distance * i), y)
