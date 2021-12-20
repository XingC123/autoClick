import threading
from tkinter import *

# 自定义环境
import environment.config.main_config
import gui.app_info
# 自定义gui方法
import gui.main_window
# 自定义lib方法
import lib.necessary_lib as necessary_lib
import lib.runNeedLib as runNeedLib
from lib import stop_with_main_thread

width_root_window = 600
height_root_window = 400


class MainStateWindow:
    def __init__(self):
        # 创建配置文件
        self.main_config = environment.config.main_config.MainConfig(runNeedLib.getCurRunPath(__file__))

        # 一些变量的声明
        self.click_object = None

        # 主窗口
        self.main_state_window = Tk()
        necessary_lib.fit_screen_zoom(self.main_state_window)
        self.main_state_window.title('自动化')
        self.main_state_window.geometry(necessary_lib.middle_screen(self.main_state_window,
                                                                    width_root_window, height_root_window))
        self.main_state_window.resizable(False, False)

        # 菜单栏
        self.menubar = Menu(self.main_state_window)
        self.info_menu()

        # 主frame
        self.main_frame = Frame(self.main_state_window, width=width_root_window, height=height_root_window - 50)
        self.main_frame.pack_propagate(False)
        self.main_frame.pack()

        # 功能区frame,属于主frame
        self.func_frame = Frame(self.main_frame)
        self.func_frame.pack(expand=YES)

        # 功能区frame(下级frame按序号从小到大,从左向右排列)
        # 下级1
        self.left_buttons_frame = Frame(self.func_frame)
        self.left_buttons_frame.pack(side=LEFT)

        def show_select_config():
            gui.main_window.MainApp(self.main_state_window, self.click_object, 'show')
        Button(self.left_buttons_frame, text='查看', command=show_select_config).pack(side=TOP, anchor=E)
        Button(self.left_buttons_frame, text='暂停').pack(side=TOP, anchor=E)

        def modify_select_config():
            gui.main_window.MainApp(self.main_state_window, self.click_object, 'modify')
        Button(self.left_buttons_frame, text='修改', command=modify_select_config).pack(side=TOP, anchor=E)
        Button(self.left_buttons_frame, text='保存所有修改').pack(side=TOP, anchor=E)
        # 下级2
        self.show_work_frame = Frame(self.func_frame, width=300, height=150, bd=1, relief=GROOVE)
        self.show_work_frame.pack_propagate(False)
        self.show_work_frame.pack(side=LEFT)
        # 下级3
        self.right_buttons_frame = Frame(self.func_frame)
        self.right_buttons_frame.pack(side=LEFT)

        def add_config():
            gui.main_window.MainApp(self.main_state_window, self.click_object, 'add')

        Button(self.right_buttons_frame, text='+', width=2, command=add_config).pack(side=TOP, anchor=W)

        def del_config():
            pass

        Button(self.right_buttons_frame, text='-', width=2, command=del_config).pack(side=TOP, anchor=W)

        # 功能区frame(一般指最下方按钮所在frame)
        self.work_frame = Frame(self.main_state_window, width=width_root_window, height=50)
        self.work_frame.pack_propagate(False)
        self.work_frame.pack()

        def do_all_works_now():
            pass

        Button(self.work_frame, text='立即执行全部任务', command=do_all_works_now).pack()

        # 窗口其他必要属性
        self.main_state_window.config(menu=self.menubar)
        self.main_state_window.protocol('WM_DELETE_WINDOW', lambda: self.close_window())
        self.main_state_window.mainloop()

    # 窗口组件的其他方法
    def info_menu(self):
        info_menu = Menu(self.menubar, tearoff=False)

        def app_info():
            gui.app_info.info_app_info_menu(self.main_state_window)

        info_menu.add_command(label='关于软件', command=app_info)

        self.menubar.add_cascade(label='关于', menu=info_menu)

    def close_window(self):
        # 自定义的关闭主窗口时执行的方法
        all_threads = threading.enumerate()
        for i in all_threads:
            stop_with_main_thread.stop_thread(i)
        self.main_state_window.destroy()

    # 一些变量的初始化方法
    def init_click_object(self):
        self.click_object = {}


if __name__ == '__main__':
    MainStateWindow()
