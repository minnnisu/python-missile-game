import share

class Heart:
    def __init__(self, pygame):
        self.heart = pygame.image.load(share.IMAGES_DIR + 'heart.png')
        self.heartCount = 3 # 남은 하트 수
        
    def getHeartCount(self):
        return self.heartCount
    
    def decreaseHeartCount(self):
        self.heartCount -= 1
        
    def showHeart(self, monitor, x, y, distance=30):
        for i in range(self.heartCount):  # 남은 하트의 개수를 보여준다
            monitor.paintEntity(self.heart, x + (distance * i), y)

class User:
    def __init__(self, _username = None):
        self.username = _username
        
    def init(self, heart):
        self.heart = heart
        self.fireCount = 0 
        
    def isDie(self):
        return self.heart.getHeartCount() < 1
        
    def increaseFireCount(self):
        self.fireCount += 1

    def getHeart(self):
        return self.heart

   

    
