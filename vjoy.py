import keyboard as k
import win32api,win32gui,win32con

status = 0
o_pos = (350, 630)			# 摇杆中心坐标
w_pos = (o_pos[0], o_pos[1]-50)
s_pos = (o_pos[0], o_pos[1]+50)
a_pos = (o_pos[0]-50, o_pos[1])
d_pos = (o_pos[0]+50, o_pos[1])
hwnds = []

def callback(hwnd, extra):
    global hwnds
    if win32gui.IsWindowVisible(hwnd):
        hwnds.append(hwnd)
        title = win32gui.GetWindowText(hwnd)
        print("{} 窗口标题:".format(len(hwnds)), title, " 窗口句柄:", hwnd)
    return True


win32gui.EnumWindows(callback, None)
hwnd = hwnds[int(input("输入你需要的窗口编号："))-1]
 
'''根据GetWindowRect拿到主窗口的左顶点的位置坐标(x,y)和窗口的宽高(w*h)'''
rect = win32gui.GetWindowRect(hwnd)
# print(rect,hwnd)
x,y=rect[0],rect[1]
w,h=rect[2] - x,rect[3] - y
long_position = win32api.MAKELONG(x, y)

def down(x,y):
    global status, long_position
    if status == 0:
        long_position = win32api.MAKELONG(o_pos[0],o_pos[1])
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
        long_position = win32api.MAKELONG(x, y)
        win32api.PostMessage(hwnd, win32con.WM_MOUSEMOVE, None, long_position)
        status = 1

def up():
    global status, long_position
    status = 0
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)

while True:
    # 等待下一个事件。
    event = k.read_event()
    if event.event_type == k.KEY_DOWN:
        if k.is_pressed("w") and k.is_pressed("d"):
            down(d_pos[0],w_pos[1])
        elif k.is_pressed("w") and k.is_pressed("a"):
            down(a_pos[0],w_pos[1])
        elif k.is_pressed("s") and k.is_pressed("d"):
            down(d_pos[0],s_pos[1])
        elif k.is_pressed("s") and k.is_pressed("a"):
            down(a_pos[0],s_pos[1])
        else:
            if k.is_pressed("w"):
                down(w_pos[0],w_pos[1])
            elif k.is_pressed("s"):
                down(s_pos[0],s_pos[1])
            elif k.is_pressed("a"):
                down(a_pos[0],a_pos[1])
            elif k.is_pressed("d"):
                down(d_pos[0],d_pos[1])
        status = 0
    elif event.event_type == k.KEY_UP:
        if (not k.is_pressed("w")) and (not k.is_pressed("a")) and (not k.is_pressed("s")) and (not k.is_pressed("d")):
            up()