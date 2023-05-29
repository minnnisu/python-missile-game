import tkinter as tk
import sys
from missileGame import GameStage
from user import User

class App(tk.Tk):
    def __init__(self, frame_class, swidth, sheight):
        tk.Tk.__init__(self)
        self.geometry(str(swidth) + "x" + str(sheight))
        self._frame = None
        self.switch_frame(frame_class)
        self.mainloop()
        
    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)

        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        
    def quit(self):
       self.destroy()
       
class Alert(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Please enter your nickname").pack()
        tk.Button(self, text="OK",
                  command=lambda: master.quit()).pack() # Play Games
    

class MainPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Missile Game").pack()
        tk.Button(self, text="play game",
                  command=lambda: master.switch_frame(LoginPage)).pack() # Play Game
        tk.Button(self, text="Show rank",
                  command=lambda: master.switch_frame(RankPage)).pack() # Rank

class LoginPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Missile Game").pack()
        
        # input user info
        tk.Label(self, text="User name").pack()
        self.usernameInput = tk.Text(self, width=20, height=1)
        self.usernameInput.pack()
        tk.Button(self, text="Login",
                  command=lambda: self.checkUserNameVaild(master)).pack()
        
        tk.Button(self, text="Play without login",
                  command=lambda: self.playGame(master, None)).pack() # play without login
        
    def getUsername(self):
        return self.usernameInput.get("1.0","end-1c")
    
    def checkUserNameVaild(self, master):
        if self.getUsername() == "":
            App(Alert, 200, 100)
            return
        
        username = self.getUsername()
        self.playGame(master, username)
        
    def playGame(self, master, username = None):       
        user = User(username) # 유저 생성
        gameStage = GameStage(user) 
        master.quit()
        gameStage.playGame()
    
class RankPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Missile Game").pack(side="top", fill="x", pady=10)
        
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

if __name__ == "__main__":
    app = App(MainPage, 600, 500)