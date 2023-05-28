# Multi-frame tkinter application v2.3
import tkinter as tk
import pygame
from missileGame import playGame
from user import User
from monitor import Monitor
import sys

class SampleApp(tk.Tk):
    def __init__(self, frame_class, user=None):
        tk.Tk.__init__(self)
        self.geometry("600x500")
        self._frame = None
        self.switch_frame(frame_class, user)
        self.mainloop()
        
    def switch_frame(self, frame_class, user=None):
        """Destroys current frame and replaces it with a new one."""
        if str(frame_class) == "<class '__main__.GameOver'>":
            new_frame = frame_class(master=self, user=user)
        else:
            new_frame = frame_class(self)

        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        
    def quit(self):
       self.destroy()
    

class MainPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Missile Game").pack() # Game Title
        tk.Button(self, text="play game",
                  command=lambda: master.switch_frame(LoginPage)).pack() # Play Game
        tk.Button(self, text="Show rank",
                  command=lambda: master.switch_frame(RankPage)).pack() # Rank

class LoginPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Missile Game").pack() # Game Title
        
        # input user info
        tk.Label(self, text="User name").pack()
        self.userNameInput = tk.Text(self, width=20, height=1)
        self.userNameInput.pack()
        tk.Button(self, text="Login",
                  command=lambda: self.playGame(master, True)).pack()
        
        tk.Button(self, text="Play without login",
                  command=lambda: self.playGame(master)).pack() # play without login
        
    def getUsername(self):
        return self.userNameInput.get("1.0","end-1c")
        
    def playGame(self, master, isLogin=False):
        if isLogin:
            userName = self.getUsername()
            if userName != "":
                print(userName)
            # configure DB
            # play Game
        else:
            print("without login")
            # play Game
        
        pygame.init()
        monitor = Monitor(pygame)
        user = User(pygame)
        master.quit()
        
        playGame(monitor, pygame, user)
        SampleApp(GameOver,user)
    
class RankPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Missile Game").pack(side="top", fill="x", pady=10) # Game Title
        
        # 위젯 생성
        widget = tk.Listbox(self, width=50)
        for i in range(100):
            widget.insert("end", i)
        scrollbar = tk.Scrollbar(self)
        # 기능 상호 연결
        widget.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=widget.yview)
        # 배치
        widget.pack(side="left", fill="y")
        scrollbar.pack(side="right", fill="y")
                
        tk.Label(self, text="Rank").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to main page",
                  command=lambda: master.switch_frame(MainPage)).pack()
        
class GameOver(tk.Frame):
    def __init__(self, master, user):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Missile Game").pack(side="top", fill="x", pady=10) # Game Title
        tk.Label(self, text="score: " + str(user.fireCount)).pack(side="top", fill="x", pady=10)
        tk.Button(self, text="retry", command=lambda:self.retryGame(master, user)).pack()
        tk.Button(self, text="quit", command=lambda:self.quitGame(master)).pack()
        
    def retryGame(self, master, _user):
        pygame.init()
        monitor = Monitor(pygame)
        user = User(pygame)
        user.userName = _user.userName
        master.quit()
        
        playGame(monitor, pygame, user)
        
    def quitGame(self, master):
        sys.exit()

if __name__ == "__main__":
    app = SampleApp(MainPage)