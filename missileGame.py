import random
import sys
import share 
import pygame
from monitor import Monitor
from db.userTable import UserTable
import sys
import tkinter as tk
from user import Heart

class App(tk.Tk):
    def __init__(self, frame_class, user=None):
        tk.Tk.__init__(self)
        self.geometry("600x500")
        self._frame = None
        self.switch_frame(frame_class, user)
        self.mainloop()
        
    def switch_frame(self, frame_class, user=None):
        """Destroys current frame and replaces it with a new one."""
        if str(frame_class) == "<class 'missileGame.GameOver'>":
            new_frame = frame_class(self, user)
        else:
            new_frame = frame_class(self)

        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        
    def quit(self):
       self.destroy()
       
class GameOver(tk.Frame):
    def __init__(self, master, _diedUser):
        self.diedUser = _diedUser
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Missile Game").pack(side="top", fill="x", pady=10) # Game Title
        tk.Label(self, text="score: " + str(self.diedUser.fireCount)).pack(side="top", fill="x", pady=10)
        tk.Button(self, text="retry", command=lambda:self.retryGame(master)).pack()
        tk.Button(self, text="quit", command=lambda:self.quitGame()).pack()
        
        if(self.diedUser.username):
            userTable = UserTable()
            userInfo = userTable.selectUser(self.diedUser.username, True)
            if userInfo == []: # Not exist user info
                userTable.insertUser(self.diedUser)
            elif self.diedUser.fireCount > int(userInfo[0]['score']):
                userTable.updateUser(self.diedUser)   
        
    def retryGame(self, master):
        gameStage = GameStage(self.diedUser)
        master.quit()
        gameStage.playGame()
        
    def quitGame(self):
        sys.exit()

class Ship:
    def __init__(self, swidth, sheight):
        self.ship = pygame.image.load(share.IMAGES_DIR + 'ship02.png')
        self.shipSize = self.ship.get_rect().size
        self.shipX = swidth / 2  # 우주선의 X좌표
        self.shipY = sheight * 0.8  # 우주선의 Y좌표
        self.dx, self.dy = 0, 0  # 키보드를 누를때 우주선의 이동량

    def moveX(self, x):
        self.dx += x

    def moveY(self, y):
        self.dy += y

    # 우주선이 화면 안에서만 움직이게 한다.
    def moveShip(self, monitor):
        if (0 < self.shipX + self.dx and self.shipX + self.dx <= monitor.swidth - self.shipSize[0]) \
                and (monitor.sheight/2 < self.shipY + self.dy and self.shipY + self.dy <= monitor.sheight - self.shipSize[1]):  # 화면의 중앙까지만
            self.shipX += self.dx
            self.shipY += self.dy
        monitor.paintEntity(self.ship, self.shipX, self.shipY)

    def stopShip(self):
        self.dx = 0
        self.dy = 0


class Monster:
    def __init__(self, swidth):
        self.monsterImage = ['monster01.png', 'monster02.png', 'monster03.png', 'monster04.png',
                             'monster05.png', 'monster06.png', 'monster07.png', 'monster08.png',
                             'monster09.png', 'monster10.png']
        self.monster = pygame.image.load(
            share.IMAGES_DIR + random.choice(self.monsterImage))
        self.monsterSize = self.monster.get_rect().size
        self.monsterX = 0
        self.monsterY = random.randrange(
            0, int(swidth * 0.3))  # 우주괴물은 위에서 3번째까지
        self.monsterSpeed = random.randrange(1, 5)

    def initMonster(self, swidth):
        # 우주괴물을 초기화(무작위 이미지로 다시 준비)
        self.monster = pygame.image.load(share.IMAGES_DIR +
                                         random.choice(self.monsterImage))
        self.monsterSize = self.monster.get_rect().size
        self.monsterX = 0
        self.monsterY = random.randrange(0, int(swidth * 0.3))
        self.monsterSpeed = random.randrange(1, 5)

    # 우주괴물이 자동으로 나타나 왼쪽에서 오른쪽으로 움직인다.
    def moveMonster(self, monitor, user):
        self.monsterX += self.monsterSpeed
        if self.monsterX > monitor.swidth:
            user.getHeart().decreaseHeartCount()  # 우주괴물을 놓칠 때 마다 하트가 감소한다.
            self.monsterX = 0
            self.monsterY = random.randrange(0, int(monitor.swidth * 0.3))
            # 우주괴물 이미지를 무작위로 선택한다.
            self.monster = pygame.image.load(share.IMAGES_DIR +
                                             random.choice(self.monsterImage))
            self.monsterSize = self.monster.get_rect().size
            self.monsterSpeed = random.randrange(1, 5)

        monitor.paintEntity(self.monster, self.monsterX, self.monsterY)
        
class Missile:
    def __init__(self):
        self.missile = pygame.image.load(share.IMAGES_DIR + 'missile.png')
        self.missileX, self.missileY = None, None  # None은 미사일을 쏘지 않았다는 의미이다.

    def initMissile(self):
        self.missileX, self.missileY = None, None   # 총알이 사라진다.

    def shootMissile(self, ship):
        if self.missileX == None:
            self.missileX = ship.shipX + ship.shipSize[0]/2
            self.missileY = ship.shipY

    def showMissile(self, monitor, monster, user):
        # @기능 4-4 : 미사일을 화면에 표시한다.
        if self.missileX != None:                          # 총알을 쏘면 좌표를 위로 변경한다.
            self.missileY -= 10
            if self.missileY < 0:
                self.missileX, self.missileY = None, None   # 총알이 사라진다.

        if self.missileX != None:           # 미사일을 쏜 적이 있으면 미사일을 그려준다.
            monitor.paintEntity(self.missile, self.missileX, self.missileY)
            # @기능 5-2 : 우주괴물이 미사일에 맞았는지 체크한다.
            if (monster.monsterX < self.missileX and self.missileX < monster.monsterX + monster.monsterSize[0]) and \
                    (monster.monsterY < self.missileY and self.missileY < monster.monsterY + monster.monsterSize[1]):
                user.increaseFireCount()
                monster.initMonster(monitor.swidth)
                self.initMissile()

class GameStage:
    def __init__(self, _user):
        self.pygame = pygame
        self.pygame.init()
        
        self.user = _user
        self.monitor = Monitor(self.pygame)
        self.user.init(Heart(self.pygame))

    def playGame(self):
        ship = Ship(self.monitor.sheight, self.monitor.sheight)
        monster = Monster(self.monitor.sheight)
        missile = Missile()

        while True:
            if (self.user.isDie()):
                self.dieUser()

            (self.pygame.time.Clock()).tick(50)  # 게임 진행을 늦춘다(10~100 정도가 적당).
            self.monitor.fillBackground()
            self.user.getHeart().showHeart(self.monitor, 220, self.monitor.sheight - 38)

            # 키보드나 마우스 이벤트가 들어오는지 체크한다.
            for e in self.pygame.event.get():
                if e.type in [self.pygame.QUIT]:
                    self.pygame.quit()
                    sys.exit()

                if e.type in [self.pygame.KEYDOWN]:
                    # 방향키에 따라 우주선이 움직이게 한다.
                    if e.key == self.pygame.K_LEFT:
                        ship.moveX(-5)
                    elif e.key == self.pygame.K_RIGHT:
                        ship.moveX(5)
                    elif e.key == self.pygame.K_UP:
                        ship.moveY(-5)
                    elif e.key == self.pygame.K_DOWN:
                        ship.moveY(5)
                    
                    elif e.key == self.pygame.K_SPACE: # 스페이스바를 누르면 미사일을 발사한다.
                        missile.shootMissile(ship)

                # 방향키를 떼면 우주선이 멈춘다.
                if e.type in [self.pygame.KEYUP]:
                    if e.key == self.pygame.K_LEFT or e.key == self.pygame.K_RIGHT \
                    or e.key == self.pygame.K_UP or e.key == self.pygame.K_DOWN:
                        ship.stopShip()

            ship.moveShip(self.monitor)
            monster.moveMonster(self.monitor, self.user)
            missile.showMissile(self.monitor, monster, self.user)

            fireCountTxt = 'Fire Count: ' + str(self.user.fireCount)
            self.monitor.writeText(fireCountTxt, 10, self.monitor.sheight-40)
            
            if self.user.username:
                usernameTxt = 'Username: ' + self.user.username
                self.monitor.writeText(usernameTxt, 10, self.monitor.sheight-70)
           
            # 화면을 업데이트한다.
            self.pygame.display.update()
            
    def dieUser(self):
        App(GameOver, self.user)
