import share

class Monitor:
    def __init__(self, _pygame):
        self.pygame = _pygame
        self.swidth, self.sheight = 500, 700  # 화면 크기
        
        self.monitor = self.pygame.display.set_mode((self.swidth, self.sheight))
        self.pygame.display.set_caption('우주괴물 무찌르기')
        
    def fillBackground(self):
        self.monitor.fill((share.BACKGROUND_COLOR['r'], share.BACKGROUND_COLOR['g'], share.BACKGROUND_COLOR['b']))  

    def paintEntity(self, entity, x, y):
        self.monitor.blit(entity, (x, y))
        
    def writeText(self, text, x, y):
        font = self.pygame.font.Font(share.FONT_DIR, 20)      # 한글 폰트
        entity = font.render(text, True, (share.FONT_COLOR['r'], share.FONT_COLOR['g'], share.FONT_COLOR['b']))
        self.monitor.blit(entity, (x, y))