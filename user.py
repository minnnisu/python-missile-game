import share

class User:
    def __init__(self, pygame):
        self.userState = "live"
        self.heart = pygame.image.load(share.IMAGES_DIR + 'heart.png')
        self.heartCount = 3
        self.fireCount = 0

    def increaseFireCount(self):
        self.fireCount += 1

    def decreaseHeart(self):
        self.heartCount -= 1

    def isDie(self):
        print(self.heartCount)
        return self.heartCount < 1

    def showHeart(self, monitor, x, y, distance=30):
        for i in range(self.heartCount):  # 남은 하트의 개수를 보여준다
            monitor.paintEntity(self.heart, x + (distance * i), y)
            
    def dieUser(self, monitor, pygame):
        button_image = pygame.image.load(
            share.IMAGES_DIR + "retry-button.png") # return Surface
        button_rect = button_image.get_rect()
        button_rect.center = (400, 300)  # 버튼의 위치 (x, y)

        running = True

        while running:
            (pygame.time.Clock()).tick(100)  # 게임 진행을 늦춘다(10~100 정도가 적당).
            monitor.fillBackground()  # 배경 색칠
            monitor.writeText('Game Over', 100, monitor.sheight - 100)
            monitor.paintEntity(button_image, 400, 300)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 버튼을 눌렀을 때
                    if event.button == 1:  # 마우스 왼쪽 버튼을 클릭했을 때
                        mouse_pos = pygame.mouse.get_pos()  # 마우스 위치 가져오기
                        if button_rect.collidepoint(mouse_pos):  # 버튼 위에서 클릭한 경우
                            print("Button Clicked!")
            pygame.display.update()
