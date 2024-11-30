from vjoy import vjoy

import tkinter as tk
from tkinter import ttk,messagebox
import keyboard as k

import os
import json
import sys
import win32api
import threading
from pathlib import Path

real_path = Path(os.path.realpath(sys.argv[0])).parent

# 更改工作目录
def source_path(relative_path):
    if getattr(sys,'frozen',False):
        base_path=sys._MEIPASS
    else:
        base_path=os.path.abspath(".")
    return os.path.join(base_path, relative_path)
    
cd=source_path('')
os.chdir(cd)

class App(tk.Tk):
    def __init__(self, real_path):
        super().__init__()
#         self.geometry("500x300")
        self.title('Vjoy虚拟摇杆')
        self.iconbitmap("icon.ico")
        self.path = os.path.join(real_path,"config.json")
        while True:
            try:
                with open(self.path,"r") as f:
#                     print(json.load(f))
                    self.o_pos = tuple(json.load(f))
                    break
            except:
                messagebox.showerror('错误','无法打开配置文件，进入设置模式')
                self.config()
        self.vjoy = vjoy(self.o_pos)
        self.vjoy.get_hwnds()
        
        # 创建vjoy进程
        self.thread = threading.Thread(target=self.vjoy.vjoy, daemon=True)

        # 初始化数据
        self.titles = self.vjoy.titles
        self.hwnds = self.vjoy.hwnds
        self.paddings = {'padx': 5, 'pady': 5}

        # 设置变量
        self.option_var = tk.StringVar(self)

        # 创建控件
        self.create_widgets()

    def create_widgets(self):
        frame1 = ttk.Frame(self)
        frame1.pack()
        frame2 = ttk.Frame(self)
        frame2.pack()
        
        # 标签
        label = ttk.Label(frame1, text='选择你的窗口:')
#         label.grid(row=0,column=0)
        label.pack()

        # OptionMenu
        option_menu = ttk.OptionMenu(
        frame1,
        self.option_var,
        self.titles[0],
        *self.titles,
        )
#         option_menu.grid(row=1,column=0)
        option_menu.pack()
        
        # 确定
        self.button = ttk.Button(frame2, text="确定", command=self.callback)
        self.button.grid(row=0,column=0)
        
        # 暂停
        self.button3 = ttk.Button(frame2, text="暂停", command=self.stop)
        self.button3.grid(row=0,column=1)
        
        # 退出
        self.button2 = ttk.Button(frame2, text="退出", command=sys.exit)
        self.button2.grid(row=0,column=2)
        
        #设置
        self.setting = ttk.Button(self,text="设置", command=self.config)
        self.setting.pack()
        
        # 输出
        self.output_label = ttk.Label(self, text="虚拟摇杆已启动", foreground='red')
        
    def callback(self):
        self.vjoy.hwnd = self.hwnds[self.titles.index(self.option_var.get())]
        self.vjoy.get_rect()
        self.button.config(state="disable")
        # 输出标签
        self.output_label.pack(padx=self.paddings["padx"],pady=self.paddings["pady"])
        # 运行vjoy
        try:
           self.thread.start()
        except:
           print("Error: unable to start thread")
    
    def stop(self):
        self.vjoy.stop()
        self.thread = threading.Thread(target=self.vjoy.vjoy, daemon=True)
        self.button.config(state="able")
        self.output_label.pack_forget()
    
    def config(self):
        k.add_hotkey("ctrl+alt+s", self.get_pos)
        messagebox.showinfo('设置','鼠标移动到摇杆中心\n按下Ctrl+Alt+S确定\n（关闭此窗口后再按下键盘）')
        k.wait("ctrl+alt+s")
        with open(self.path, "w") as f:
            json.dump(self.point,f)
    
    def get_pos(self):
        self.point = tuple(win32api.GetCursorPos())
    
if __name__ == "__main__":
    app = App(real_path)
    app.mainloop()