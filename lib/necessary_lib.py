import ctypes


def fit_screen_zoom(window):
    # 避免屏幕缩放导致的显示模糊
    # 告诉操作系统使用程序自身的dpi适配
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    # 获取屏幕的缩放因子
    ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
    # 设置程序缩放
    window.tk.call('tk', 'scaling', ScaleFactor / 75)


def real_screen_size(window):
    # ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
    # print(window.winfo_screenwidth(), window.winfo_screenheight())
    # return window.winfo_screenwidth() * ScaleFactor, window.winfo_screenheight() * ScaleFactor
    return window.winfo_screenwidth(), window.winfo_screenheight()


def middle_screen(window, width, height):
    # 将窗口显示在屏幕中心
    # 用法:window = tkinter.Tk()
    #     width = 300
    #     height = 200
    #     window.geometry(middle_screen(window, width, height))
    real_screen_width, real_screen_height = real_screen_size(window)
    positionX = 0 if real_screen_width == width else real_screen_width / 2 - width / 2
    positionY = 0 if real_screen_height == height else real_screen_height / 2 - height / 2
    # print('屏幕尺寸:', real_screen_width, real_screen_height)
    position_and_size = '%dx%d+%d+%d' % (width, height, positionX, positionY)
    return position_and_size
