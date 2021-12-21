import threading
from tkinter import *

# 自定义环境
import environment.config.main_config
from environment.custom_constant import custom_constant
# 自定义gui方法
import gui.app_info
import gui.config_editer
# 自定义lib方法
import lib.necessary_lib as necessary_lib
import lib.runNeedLib as runNeedLib
from lib import stop_with_main_thread

width_root_window = 600
height_root_window = 400


class MainStateWindow:
    def __init__(self):
        # 创建配置文件
        self.root_config = environment.config.main_config.MainConfig(runNeedLib.getCurRunPath(__file__))

        # 一些变量的声明
        self.click_object = None
        self.all_config_dic = None
        self.auto_execute = None

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
            gui.config_editer.ConfigEditer(self.main_state_window, self.click_object, 'show')

        Button(self.left_buttons_frame, text='查看', command=show_select_config).pack(side=TOP, anchor=E)
        Button(self.left_buttons_frame, text='暂停').pack(side=TOP, anchor=E)

        def modify_select_config():
            gui.config_editer.ConfigEditer(self.main_state_window, self.click_object, 'modify')

        Button(self.left_buttons_frame, text='修改', command=modify_select_config).pack(side=TOP, anchor=E)
        Button(self.left_buttons_frame, text='保存所有修改').pack(side=TOP, anchor=E)
        # 下级2
        self.show_work_frame = Frame(self.func_frame, width=300, height=150)
        self.show_work_frame.pack_propagate(False)
        self.show_work_frame.pack(side=LEFT)
        self.show_work_frame.update()
        self.all_config_listbox = Listbox(self.show_work_frame,
                                          width=self.show_work_frame.winfo_screenwidth(),
                                          height=self.show_work_frame.winfo_height())
        self.all_config_listbox.pack()
        # 下级3
        self.right_buttons_frame = Frame(self.func_frame)
        self.right_buttons_frame.pack(side=LEFT)

        def add_config():
            gui.config_editer.ConfigEditer(self.main_state_window, self.click_object, 'add')

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

        # 控件初始化完成后的方法
        self.custom_init()
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

    # 窗口控件初始化后任务
    def custom_init(self):
        # 加载本地配置
        self.load_root_config('boot')
        # 检查是否有任务需要自动执行
        self.check_auto_execute()

    def check_auto_execute(self):
        # 检查是否有任务需要自动执行
        if self.auto_execute is not None and len(self.auto_execute) != 0:
            # self.auto_execute 已被赋值
            for i in self.auto_execute:
                if self.root_config.main_config.has_section(i):
                    # 从dic里的value值得到相关操作数给"数据执行"方法
                    pass

    def load_root_config(self, mode):
        # 加载本地配置
        self.all_config_dic = {}
        if mode != 'boot':
            self.root_config.read_config()
        config_sections = self.root_config.sections
        if len(config_sections) > 1:
            for i in config_sections:
                if i == custom_constant.rootconfig:
                    config_name_list = self.root_config.get_value(i, custom_constant.startwithboot)
                    if config_name_list != '':
                        self.auto_execute = eval(config_name_list)
                else:
                    self.all_config_listbox.insert(END, i)
                    # self.all_config_dic[i] = self.root_config.main_config.items(i)
                    self.all_config_dic[i] = self.root_config.get_config(i)
        else:
            pass
        print(self.all_config_dic)

    # 数据处理
    def execute_work(self, click_object):
        pass


if __name__ == '__main__':
    MainStateWindow()
