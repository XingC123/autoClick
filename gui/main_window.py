import webbrowser
from tkinter import *

import gui.app_info
# 自定义gui方法
import gui.custom_messagebox as custom_messagebox
import gui.get_xy_window
# 自定义lib方法
import lib.necessary_lib as necessary_lib
# 自定义环境
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
    def __init__(self, parent_window, click_object, work_mode):
        # 父窗口的操作
        self.parent_window = parent_window
        self.parent_window.attributes('-disable', True)
        # 工作模式
        self.work_mode = work_mode
        # 用来存放所有信息的自定义对象
        # 在init函数末尾赋初值
        self.click_object = None
        # 根配置文件
        self.root_config = None
        # 多选框状态
        self.check_dic = None
        # 创建主窗口
        self.main_window = Toplevel()
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

        # 界面渲染完成后的初始化方法

        # 窗口其他必要属性
        self.main_window.config(menu=self.menubar)
        self.main_window.protocol('WM_DELETE_WINDOW', lambda: self.close_window())
        self.main_window.mainloop()

    # 其他窗口部件方法域
    def set_main_window_menu(self):
        info_menu = Menu(self.menubar, tearoff=0)

        def app_info():
            gui.app_info.info_app_info_menu(self.main_window)
        info_menu.add_command(label='关于软件', command=app_info)

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
        if self.work_mode == 'modify' or self.work_mode == 'add':
            pass
        self.parent_window.attributes('-disable', False)
        self.main_window.destroy()

