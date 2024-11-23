import win32api,win32gui,win32con

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
x,y=rect[0],rect[1]
w,h=rect[2] - x,rect[3] - y

point = win32api.GetCursorPos()
print(point)