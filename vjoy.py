import keyboard as k
import win32api,win32gui,win32con

class vjoy:
    def __init__(self, o_pos):
        self.status = 0
        self.o_pos = o_pos
        self.w_pos = (self.o_pos[0], self.o_pos[1]-50)
        self.s_pos = (self.o_pos[0], self.o_pos[1]+50)
        self.a_pos = (self.o_pos[0]-50, self.o_pos[1])
        self.d_pos = (self.o_pos[0]+50, self.o_pos[1])
        self.hwnds = []
        self.titles = []
        self.hwnd = None
        self.stop_status = False

    def callback(self, hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if not title == "":
                self.hwnds.append(hwnd)
                self.titles.append(title)
#             print("{} 窗口标题:".format(len(self.hwnds)), title, " 窗口句柄:", hwnd)
        return True

    def get_hwnds(self):
        win32gui.EnumWindows(self.callback, None)
#         self.hwnd = self.hwnds[int(input("输入你需要的窗口编号："))-1]

    def down(self,x,y):
        if self.status == 0:
            self.long_position = win32api.MAKELONG(self.o_pos[0],self.o_pos[1])
            win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, self.long_position)
            self.long_position = win32api.MAKELONG(x, y)
            win32api.PostMessage(self.hwnd, win32con.WM_MOUSEMOVE, None, self.long_position)
            status = 1

    def up(self):
        self.status = 0
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, self.long_position)
    
    def get_rect(self):
        '''根据GetWindowRect拿到主窗口的左顶点的位置坐标(x,y)和窗口的宽高(w*h)'''
        rect = win32gui.GetWindowRect(self.hwnd)
        x,y=rect[0],rect[1]
        w,h=rect[2] - x,rect[3] - y
        self.long_position = win32api.MAKELONG(x, y)
    
    def stop(self):
        self.stop_status = True
    
    def vjoy(self):
        while True:
            if self.stop_status:
                break
            # 等待下一个事件。
            event = k.read_event()
            if event.event_type == k.KEY_DOWN:
                if k.is_pressed("w") and k.is_pressed("d"):
                    self.down(self.d_pos[0],self.w_pos[1])
                elif k.is_pressed("w") and k.is_pressed("a"):
                    self.down(self.a_pos[0],self.w_pos[1])
                elif k.is_pressed("s") and k.is_pressed("d"):
                    self.down(self.d_pos[0],self.s_pos[1])
                elif k.is_pressed("s") and k.is_pressed("a"):
                    self.down(self.a_pos[0],self.s_pos[1])
                else:
                    if k.is_pressed("w"):
                        self.down(self.w_pos[0],self.w_pos[1])
                    elif k.is_pressed("s"):
                        self.down(self.s_pos[0],self.s_pos[1])
                    elif k.is_pressed("a"):
                        self.down(self.a_pos[0],self.a_pos[1])
                    elif k.is_pressed("d"):
                        self.down(self.d_pos[0],self.d_pos[1])
                self.status = 0
            if event.event_type == k.KEY_UP:
                if (not k.is_pressed("w")) and (not k.is_pressed("a")) and (not k.is_pressed("s")) and (not k.is_pressed("d")):
                    self.up()

if __name__ == "__main__":
    vjoy = vjoy((0,0))
#     vjoy.get_hwnds()
    vjoy.vjoy()