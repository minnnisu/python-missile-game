# Multi-frame tkinter application v2.3
import tkinter as tk
from tkinter import ttk

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(MainPage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class MainPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Missile Game").pack(side="top", fill="x", pady=10) # Game Title
        tk.Button(self, text="play game",
                  command=lambda: master.switch_frame(LoginPage)).pack() # Play Game
        tk.Button(self, text="Show rank",
                  command=lambda: master.switch_frame(RankPage)).pack() # Rank

class LoginPage(tk.Frame):
    def __init__(self, master):
        self.isLogin = False
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Missile Game").pack(side="top", fill="x", pady=10) # Game Title
        
        # input user info
        tk.Label(self, text="User name").pack(side="top", fill="x", pady=10)
        tk.Text(self, width=20, height=5).pack()
        tk.Button(self, text="Login",
                  command=lambda: master.switch_frame(MainPage)).pack()
        
        tk.Button(self, text="Play without login",
                  command=lambda: master.switch_frame(MainPage)).pack() # play without login
        
    def playGame(self):
        if self.isLogin:
            print()
            # configure DB
            # play Game
        else:
            print()
            # play Game
    
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
        
if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()