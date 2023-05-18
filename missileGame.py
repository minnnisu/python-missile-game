import random
import sys
import pygame
from share import IMAGES_DIR, FONT_DIR, BACKGROUND_COLOR, FONT_COLOR, paintEntity


class Ship:
    def __init__(self, swidth, sheight):
        self.ship = pygame.image.load(IMAGES_DIR + 'ship02.png')
        self.shipSize = self.ship.get_rect().size
        self.shipX = swidth / 2  # 우주선의 X좌표
        self.shipY = sheight * 0.8  # 우주선의 Y좌표
        self.dx, self.dy = 0, 0  # 키보드를 누를때 우주선의 이동량

    def moveX(self, x):
        self.dx += x

    def moveY(self, y):
        self.dy += y

    # 우주선이 화면 안에서만 움직이게 한다.
    def moveShip(self, swidth, sheight):
        if (0 < self.shipX + self.dx and self.shipX + self.dx <= swidth - self.shipSize[0]) \
                and (sheight/2 < self.shipY + self.dy and self.shipY + self.dy <= sheight - self.shipSize[1]):  # 화면의 중앙까지만
            self.shipX += self.dx
            self.shipY += self.dy
        paintEntity(monitor, self.ship, self.shipX, self.shipY)

    def stopShip(self):
        self.dx = 0
        self.dy = 0


class Monster:
    def __init__(self, swidth):
        self.monsterImage = ['monster01.png', 'monster02.png', 'monster03.png', 'monster04.png',
                             'monster05.png', 'monster06.png', 'monster07.png', 'monster08.png',
                             'monster09.png', 'monster10.png']
        self.monster = pygame.image.load(
            IMAGES_DIR + random.choice(self.monsterImage))
        self.monsterSize = self.monster.get_rect().size
        self.monsterX = 0
        self.monsterY = random.randrange(
            0, int(swidth * 0.3))  # 우주괴물은 위에서 3번째까지
        self.monsterSpeed = random.randrange(1, 5)

    def initMonster(self, swidth):
        # 우주괴물을 초기화(무작위 이미지로 다시 준비)
        self.monster = pygame.image.load(IMAGES_DIR +
                                         random.choice(self.monsterImage))
        self.monsterSize = self.monster.get_rect().size
        self.monsterX = 0
        self.monsterY = random.randrange(0, int(swidth * 0.3))
        self.monsterSpeed = random.randrange(1, 5)

    # 우주괴물이 자동으로 나타나 왼쪽에서 오른쪽으로 움직인다.
    def moveMonster(self, swidth, user):
        self.monsterX += self.monsterSpeed
        if self.monsterX > swidth:
            user.decreaseHeart()  # 우주괴물을 놓칠 때 마다 하트가 감소한다.
            self.monsterX = 0
            self.monsterY = random.randrange(0, int(swidth * 0.3))
            # 우주괴물 이미지를 무작위로 선택한다.
            self.monster = pygame.image.load(IMAGES_DIR +
                                             random.choice(self.monsterImage))
            self.monsterSize = self.monster.get_rect().size
            self.monsterSpeed = random.randrange(1, 5)

        paintEntity(monitor, self.monster, self.monsterX, self.monsterY)


class Missile:
    def __init__(self):
        self.missile = pygame.image.load(IMAGES_DIR + 'missile.png')
        self.missileX, self.missileY = None, None  # None은 미사일을 쏘지 않았다는 의미이다.

    def initMissile(self):
        self.missileX, self.missileY = None, None   # 총알이 사라진다.

    def shootMissile(self, ship):
        if self.missileX == None:
            self.missileX = ship.shipX + ship.shipSize[0]/2
            self.missileY = ship.shipY

    def showMissile(self, monster, user, swidth):
        # @기능 4-4 : 미사일을 화면에 표시한다.
        if self.missileX != None:                          # 총알을 쏘면 좌표를 위로 변경한다.
            self.missileY -= 10
            if self.missileY < 0:
                self.missileX, self.missileY = None, None   # 총알이 사라진다.

        if self.missileX != None:           # 미사일을 쏜 적이 있으면 미사일을 그려준다.
            paintEntity(monitor, self.missile, self.missileX, self.missileY)
            # @기능 5-2 : 우주괴물이 미사일에 맞았는지 체크한다.
            if (monster.monsterX < self.missileX and self.missileX < monster.monsterX + monster.monsterSize[0]) and \
                    (monster.monsterY < self.missileY and self.missileY < monster.monsterY + monster.monsterSize[1]):
                user.increaseFireCount()
                monster.initMonster(swidth)
                self.initMissile()


def writeScore(monitor, score, sheight):
    myfont = pygame.font.Font(FONT_DIR + 'NanumGothic.ttf', 20)      # 한글 폰트
    txt = myfont.render('파괴한 우주괴물 수 : ' + str(score), True,
                        (FONT_COLOR['r'], FONT_COLOR['g'], FONT_COLOR['b']))
    monitor.blit(txt, (10, sheight - 40))
    pygame.display.update()


def playGame(_monitor, pygame, swidth, sheight, user):
    global monitor
    monitor = _monitor

    r = BACKGROUND_COLOR['r']
    g = BACKGROUND_COLOR['g']
    b = BACKGROUND_COLOR['b']

    ship = Ship(swidth, sheight)
    monster = Monster(swidth)
    missile = Missile()

    # @기능 5-1 : 맞힌 우주괴물 숫자를 저장할 변수를 선언한다.

    # 무한 반복
    while True:
        if (user.isDie()):
            return

        (pygame.time.Clock()).tick(50)  # 게임 진행을 늦춘다(10~100 정도가 적당).
        monitor.fill((r, g, b))              # 화면 배경을 칠한다.
        user.showHeart(monitor, sheight)

        # 키보드나 마우스 이벤트가 들어오는지 체크한다.
        for e in pygame.event.get():
            if e.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

            # @기능 2-3 : 방향키에 따라 우주선이 움직이게 한다.
            # 방향키를 누르면 우주선이 이동한다(누르고 있으면 계속 이동).
            if e.type in [pygame.KEYDOWN]:
                if e.key == pygame.K_LEFT:
                    ship.moveX(-5)
                elif e.key == pygame.K_RIGHT:
                    ship.moveX(5)
                elif e.key == pygame.K_UP:
                    ship.moveY(-5)
                elif e.key == pygame.K_DOWN:
                    ship.moveY(5)
                # @기능 4-3 : 스페이스바를 누르면 미사일을 발사한다.
                elif e.key == pygame.K_SPACE:
                    missile.shootMissile(ship)

            # 방향키를 떼면 우주선이 멈춘다.
            if e.type in [pygame.KEYUP]:
                if e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT \
                   or e.key == pygame.K_UP or e.key == pygame.K_DOWN:
                    ship.stopShip()

        ship.moveShip(swidth, sheight)
        monster.moveMonster(swidth, user)
        missile.showMissile(monster, user, swidth)

        # @기능 5-3 : 점수를 화면에 쓰는 함수를 호출한다.
        writeScore(monitor, user.fireCount, sheight)

        # 화면을 업데이트한다.
        pygame.display.update()
