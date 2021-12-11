import threading
import time
import webbrowser
from tkinter import *

import environment.config.main_config
import func.login
import gui.custom_messagebox as custom_messagebox
import gui.get_xy_window
import lib.necessary_lib as necessary_lib
import lib.stop_with_main_thread as stop_with_main_thread
from environment.custom_constant.custom_constant import *

# 常用变量
width_root_window = 600
height_root_window = 530


def replace_entry_value(element, value):
    element_type = str(type(element))
    if element_type.find('Entry') != -1:
        element.delete(0, 'end')
        element.insert(0, value)
    elif element_type.find('BooleanVar') != -1:
        if value == '':
            element.set(True)
        else:
            element.set(value)


def set_config_from_dic(dic):
    # 为 click_object 或者 root_config 赋值
    for i in dic:
        dic[i][1] = dic[i][0].get()


class MainApp:
    def __init__(self, main_app_execute_path):
        # 创建配置文件
        self.main_config = environment.config.main_config.MainConfig(main_app_execute_path)
        # 用来存放所有信息的自定义对象
        # 在init函数末尾赋初值
        self.click_object = None
        # 根配置文件
        self.root_config = None
        # 多选框状态
        self.check_dic = None
        # 创建主窗口
        self.main_window = Tk()
        necessary_lib.fit_screen_zoom(self.main_window)
        self.main_window.title('自动点击登录')
        self.main_window.geometry(necessary_lib.middle_screen(self.main_window, width_root_window, height_root_window))
        self.main_window.resizable(False, False)
        self.main_window.update_idletasks()
        self.menubar = Menu(self.main_window)
        # 子菜单项 #
        self.set_main_window_menu()

        # 内容主frame
        self.main_frame = Frame(self.main_window, width=width_root_window, height=height_root_window - 70)
        self.main_frame.pack_propagate(False)
        self.main_frame.pack()
        # 网址
        self.web_path_frame = Frame(self.main_frame)
        self.web_path_frame.pack(ipadx=10)
        Label(self.web_path_frame, text='请确保网址格式正确无误,否则将发生不可预料的后果', font=CustomFont().microsoft_yahei_10).pack()
        Label(self.web_path_frame, text='网址').pack(side=LEFT)
        self.web_path = Entry(self.web_path_frame, width=50)
        self.web_path.pack(side=LEFT)

        def open_web_path():
            path = self.web_path.get()
            if path != '':
                webbrowser.open(path)

        Button(self.web_path_frame, text='打开', command=open_web_path).pack(side=LEFT)
        # 密码以及账号的输入框坐标
        self.position_frame = Frame(self.main_frame, bd=1, relief='groove')
        self.position_frame.pack(ipady=10)
        # 账号
        position_account_frame = Frame(self.position_frame)
        position_account_frame.pack(side=LEFT, padx=10)
        Label(position_account_frame, text='账号框坐标').pack()
        position_account_left_frame = Frame(position_account_frame)
        position_account_left_frame.pack(side=LEFT)
        position_account_right_frame = Frame(position_account_frame)
        position_account_right_frame.pack(side=RIGHT)

        def get_xy_account():
            gui.get_xy_window.GetXY(self.main_window, self.positionX_account_entry, self.positionY_account_entry)

        Button(position_account_left_frame, text='采集', height=1, command=get_xy_account).pack()
        # X坐标 #
        positionX_account_frame = Frame(position_account_right_frame)
        positionX_account_frame.pack(side=TOP, pady=5)
        Label(positionX_account_frame, text='X').pack(side=LEFT)
        self.positionX_account_entry = Entry(positionX_account_frame)
        self.positionX_account_entry.pack(side=RIGHT)
        # Y坐标 #
        positionY_account_frame = Frame(position_account_right_frame)
        positionY_account_frame.pack(side=TOP, pady=5)
        Label(positionY_account_frame, text='Y').pack(side=LEFT)
        self.positionY_account_entry = Entry(positionY_account_frame)
        self.positionY_account_entry.pack(side=RIGHT)
        # 密码
        position_password_frame = Frame(self.position_frame)
        position_password_frame.pack(side=LEFT, padx=10)
        Label(position_password_frame, text='密码框坐标').pack()
        position_password_left_frame = Frame(position_password_frame)
        position_password_left_frame.pack(side=LEFT)
        position_password_right_frame = Frame(position_password_frame)
        position_password_right_frame.pack(side=RIGHT)

        def get_xy_password():
            gui.get_xy_window.GetXY(self.main_window, self.positionX_password_entry, self.positionY_password_entry)

        Button(position_password_right_frame, text='采集', height=1, command=get_xy_password).pack()
        # X坐标 #
        positionX_password_frame = Frame(position_password_left_frame)
        positionX_password_frame.pack(side=TOP, pady=5)
        Label(positionX_password_frame, text='X').pack(side=LEFT)
        self.positionX_password_entry = Entry(positionX_password_frame)
        self.positionX_password_entry.pack(side=RIGHT)
        # Y坐标 #
        positionY_password_frame = Frame(position_password_left_frame)
        positionY_password_frame.pack(side=TOP, pady=5)
        Label(positionY_password_frame, text='Y').pack(side=LEFT)
        self.positionY_password_entry = Entry(positionY_password_frame)
        self.positionY_password_entry.pack(side=RIGHT)

        # 账户密码录入
        self.account_password_frame = Frame(self.main_frame)
        self.account_password_frame.pack(ipady=10)
        # 账号frame #
        account_frame = Frame(self.account_password_frame)
        account_frame.pack(side=TOP, pady=5)
        Label(account_frame, text='账号').pack(side=LEFT)
        self.account_entry = Entry(account_frame)
        self.account_entry.pack(side=RIGHT)
        # 密码 #
        password_frame = Frame(self.account_password_frame)
        password_frame.pack(side=TOP, pady=5)
        Label(password_frame, text='密码').pack(side=LEFT)
        self.password_entry = Entry(password_frame)
        self.password_entry.pack(side=RIGHT)

        # 登录按钮的XY
        self.login_frame = Frame(self.main_frame)
        self.login_frame.pack(ipady=10)
        Label(self.login_frame, text='登录按钮').pack(side=LEFT)
        Label(self.login_frame, text='X').pack(side=LEFT)
        self.positionX_login_entry = Entry(self.login_frame, )
        self.positionX_login_entry.pack(side=LEFT)
        Label(self.login_frame, text='Y').pack(side=LEFT)
        self.positionY_login_entry = Entry(self.login_frame, )
        self.positionY_login_entry.pack(side=LEFT)

        def get_xy_login():
            gui.get_xy_window.GetXY(self.main_window, self.positionX_login_entry, self.positionY_login_entry)

        Button(self.login_frame, text='采集', command=get_xy_login).pack(side=LEFT)

        # 扩展选项
        self.extent_config_frame = Frame(self.main_frame, bd=1, relief='groove')
        self.extent_config_frame.pack()
        # 自动点击空白处 #
        self.auto_click_blank_frame = Frame(self.extent_config_frame)
        self.auto_click_blank_frame.pack(side=TOP)
        self.auto_click_blank_value = BooleanVar()
        # 默认状态 #
        self.auto_click_blank_value.set(True)

        def check_state_auto_click_blank():
            self.check_state(self.auto_click_blank_value,
                             [self.auto_click_blank_x_entry, self.auto_click_blank_y_entry])

        auto_click_blank = Checkbutton(self.auto_click_blank_frame, text='自动点击空白处',
                                       variable=self.auto_click_blank_value,
                                       onvalue=True, offvalue=False,
                                       command=check_state_auto_click_blank)
        auto_click_blank.pack(side=LEFT)
        Label(self.auto_click_blank_frame, text='X').pack(side=LEFT)
        self.auto_click_blank_x_entry = Entry(self.auto_click_blank_frame, width=10)
        self.auto_click_blank_x_entry.pack(side=LEFT)
        Label(self.auto_click_blank_frame, text='Y').pack(side=LEFT)
        self.auto_click_blank_y_entry = Entry(self.auto_click_blank_frame, width=10)
        self.auto_click_blank_y_entry.pack(side=LEFT)
        # 程序启动后定时执行 #
        auto_start_after_boot_frame = Frame(self.extent_config_frame)
        auto_start_after_boot_frame.pack(side=TOP)
        self.auto_start_after_boot_value = BooleanVar()

        def check_state_auto_start_after_boot():
            self.check_state(self.auto_start_after_boot_value, [self.auto_start_after_boot_entry])

        self.auto_start_after_boot = Checkbutton(auto_start_after_boot_frame, text='程序启动后定时执行(单位:s)',
                                                 variable=self.auto_start_after_boot_value,
                                                 onvalue=True, offvalue=False,
                                                 command=check_state_auto_start_after_boot)
        self.auto_start_after_boot.pack(side=LEFT)
        self.auto_start_after_boot_entry = Entry(auto_start_after_boot_frame, width=10)
        self.auto_start_after_boot_entry.pack(side=LEFT)

        # Label(auto_start_after_boot_frame, text='最多三位数').pack(side=LEFT)
        # def load_root_config():
        #     if self.load_root_config_boot() is False:
        #         self.auto_start_after_boot_value.set(False)
        #
        # stop_with_main_thread.StopWithMainThread(load_root_config).run()
        # 配置保存与加载
        self.config_frame = Frame(self.main_frame)
        self.config_frame.pack(ipady=10)

        Button(self.config_frame, text='加载配置', command=self.load_config).pack(side=LEFT)

        def save_config():
            if self.get_input():
                self.get_input_root()

                def save():
                    for i in self.root_config:
                        self.main_config.set_value(rootconfig, i, self.root_config[i][1])
                    for i in self.click_object:
                        self.main_config.set_value(userconfig, i, self.click_object[i][1])
                    custom_messagebox.CustomMessagebox(self.main_window, '保存配置', 300, 200, ['保存成功'])

                stop_with_main_thread.StopWithMainThread(save).run()

        Button(self.config_frame, text='保存配置', command=save_config).pack(side=LEFT)

        def clear_input_config():
            self.make_input_empty()

        Button(self.config_frame, text='清空已输入配置', command=clear_input_config).pack(side=LEFT)

        def clear_local_config():
            self.main_config.clear()

        Button(self.config_frame, text='清空本地配置', command=clear_local_config).pack(side=LEFT)

        # 功能按钮
        self.work_button_frame = Frame(self.main_window, width=width_root_window, height=50)
        self.work_button_frame.pack_propagate(False)
        self.work_button_frame.pack(side=BOTTOM)

        def work_start():
            # 新建线程来操作
            stop_with_main_thread.StopWithMainThread(self.login_work()).run()

        Button(self.work_button_frame, text='登录', command=work_start).pack(side=RIGHT, padx=10)

        # 界面渲染完成后的初始化方法
        self.init_checkbutton_state()
        self.init_root_config()
        self.init_click_object()
        self.check_state_all()

        def load_root_config():
            if self.load_root_config_boot() is False:
                self.auto_start_after_boot_value.set(False)

        stop_with_main_thread.StopWithMainThread(load_root_config).run()

        # 窗口其他必要属性
        self.main_window.config(menu=self.menubar)
        self.main_window.protocol('WM_DELETE_WINDOW', lambda: self.close_window())
        self.main_window.mainloop()

    # 其他窗口部件方法域
    def set_main_window_menu(self):
        info_menu = Menu(self.menubar, tearoff=0)

        def info_app_info_menu():
            width = 500
            height = 200
            msg_list = ['软件名: 自动点击登录', '作者: XingC', '邮箱: 123fengmo@gmail.com', '声明: 仅做学习交流之用,因其他用法造成的一切问题本人概不负责']
            custom_messagebox.CustomMessagebox(self.main_window, '关于软件', width, height, msg_list)

        info_menu.add_command(label='关于软件', command=info_app_info_menu)

        def help_info_menu():
            width = 500
            height = 200
            msg_list = ['输入框功能不限于所谓的名字',
                        '什么意思呢?就是你在框里输入什么都是可以的,只要给出相应坐标和内容,配置得当,就可以运行',
                        '软件已设置的搜索框种类可以理解为一次执行可以有最多多少个功能生效']
            custom_messagebox.CustomMessagebox(self.main_window, '帮助', width, height, msg_list)

        info_menu.add_command(label='帮助', command=help_info_menu)

        self.menubar.add_cascade(label='关于', menu=info_menu)

    def check_state(self, element_value, element, ):
        # 检查 element_value 的值,并控制相关组件的状态
        if element_value.get() is True:
            for i in element:
                i['state'] = 'normal'
        else:
            for i in element:
                i['state'] = 'disabled'

    def init_checkbutton_state(self):
        # 要检查的列表
        self.check_dic = {'auto_click_blank': [self.auto_click_blank_value,
                                               [self.auto_click_blank_x_entry, self.auto_click_blank_y_entry]],
                          'auto_start_after_boot': [self.auto_start_after_boot_value,
                                                    [self.auto_start_after_boot_entry]]
                          }

    def check_state_all(self):
        # self.init_checkbutton_state()
        for i in self.check_dic:
            self.check_state(self.check_dic[i][0], self.check_dic[i][1])

    def set_all_checkbutton_state(self, value):
        # self.init_checkbutton_state()
        for i in self.check_dic:
            self.check_dic[i][0].set(value)

    def close_window(self):
        # 自定义的关闭主窗口时执行的方法
        all_threads = threading.enumerate()
        for i in all_threads:
            stop_with_main_thread.stop_thread(i)
        self.main_window.destroy()

    # 执行的任务域
    def login_work(self):
        if self.get_input():
            func.login.login(self.main_window, self.click_object)

    def load_config(self, if_popup_window=True):
        # 配置文件重载
        self.main_config.read_config()
        if len(self.main_config.main_config.items(userconfig)) == 0:
            if if_popup_window:
                custom_messagebox.CustomMessagebox(self.main_window, '加载配置', 300, 200, ['配置为空'])
        else:
            def load():
                # 先将所有具有"通过复选框状态控制其他组件是否可用"特性的复选框对应值为 True
                self.set_all_checkbutton_state(True)
                # 根配置
                self.init_root_config()
                for i in self.root_config:
                    replace_entry_value(self.root_config[i][0], self.main_config.get_value(rootconfig, i))
                # self.click_object对象赋值
                self.init_click_object()
                for i in self.click_object:
                    replace_entry_value(self.click_object[i][0], self.main_config.get_value(userconfig, i))
                self.check_state_all()
                if if_popup_window:
                    custom_messagebox.CustomMessagebox(self.main_window, '加载配置', 300, 200, ['加载成功'])

            load()

    def init_click_object(self):
        # 为 self.click_object 对象赋初值
        self.click_object = {'web_path': [self.web_path, ''],
                             'account_x': [self.positionX_account_entry, ''],
                             'account_y': [self.positionY_account_entry, ''],
                             'password_x': [self.positionX_password_entry, ''],
                             'password_y': [self.positionY_password_entry, ''],
                             'account': [self.account_entry, ''],
                             'password': [self.password_entry, ''],
                             'login_x': [self.positionX_login_entry, ''],
                             'login_y': [self.positionY_login_entry, ''],
                             'auto_click_blank': [self.auto_click_blank_value, True],
                             'auto_click_blank_x': [self.auto_click_blank_x_entry, '10'],
                             'auto_click_blank_y': [self.auto_click_blank_y_entry, '400']
                             }

    def get_input(self):
        # 为click_object赋值(将数据读入亦或是初始化此对象)
        if self.click_object['web_path'][0].get() == '':
            custom_messagebox.CustomMessagebox(self.main_window, '错误', 300, 200, ['网址不能为空'])
            return False
        else:
            set_config_from_dic(self.click_object)
            return True

    def make_input_empty(self):
        def make_empty():
            self.init_click_object()
            self.init_root_config()
            # 将root_config置空
            for i in self.root_config:
                replace_entry_value(self.root_config[i][0], self.root_config[i][1])
            # 将click_object置空
            for i in self.click_object:
                replace_entry_value(self.click_object[i][0], self.click_object[i][1])

        stop_with_main_thread.StopWithMainThread(make_empty).run()

    def init_root_config(self):
        self.root_config = {'auto_start_after_boot_value': [self.auto_start_after_boot_value, False],
                            'auto_start_after_boot_delay': [self.auto_start_after_boot_entry, '']
                            }

    def get_input_root(self):
        set_config_from_dic(self.root_config)

    def load_root_config_boot(self):
        self.init_root_config()
        if self.main_config.get_value(rootconfig, 'auto_start_after_boot_value') == 'True':
            delay = self.main_config.get_value(rootconfig, 'auto_start_after_boot_delay')
            if delay.isdigit():
                def boot():
                    time.sleep(int(delay))
                    self.load_config(False)
                    self.login_work()

                # def boot():
                #     time.sleep(5)
                #     print('这是方法体内容')

                def boot_main():
                    custom_messagebox.CustomMessagebox(
                        self.main_window, '开机任务', 300, 200,
                        ['检测到开启自动操作的配置文件', '将在 ' + delay + ' 后自动执行'], False, boot, True)

                stop_with_main_thread.StopWithMainThread(boot_main).run()
                return True
        return False
