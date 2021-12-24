import threading
from tkinter import *

# 自定义环境
import environment.config.main_config
from environment.custom_constant import custom_constant
import environment.config.click_config as click_config
# 自定义func方法
import func.execute_work
# 自定义gui方法
import gui.app_info
import gui.config_editer
import gui.custom_messagebox
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
        # 保存所有配置信息的dic字典
        self.all_config_dic = None
        self.auto_execute = None
        # 所有需要在本地配置中删除的项目的列表
        self.deleted_elements_list = []

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
            self.execute_selected('show')

        Button(self.left_buttons_frame, text='查看', command=show_select_config).pack(side=TOP, anchor=E)
        Button(self.left_buttons_frame, text='暂停').pack(side=TOP, anchor=E)

        def modify_select_config():
            event = threading.Event()
            # 获取当前选中项信息
            curselection = self.all_config_listbox.curselection()[0]
            curname = self.all_config_listbox.get(curselection)

            def start_editer():
                self.execute_selected('modify', True, event)

            def change_in_dic():
                event.wait()
                # 删除listbox中选中项数据
                self.all_config_listbox.delete(curselection)
                # 添加删除配置名称添加入全局删除列表中
                self.deleted_elements_list.append(curname)
                # 删除dic中原配置名, 并插入新数据
                del self.all_config_dic[curname]
                config_name = self.click_object[0]
                self.all_config_dic[config_name] = self.click_object[1]
                # 插入到原位置
                self.all_config_listbox.insert(curselection, config_name)

            editer_thread = threading.Thread(target=start_editer)
            change_thread = threading.Thread(target=change_in_dic)
            editer_thread.start()
            change_thread.start()

        Button(self.left_buttons_frame, text='修改', command=modify_select_config).pack(side=TOP, anchor=E)

        def save_all_config():
            # 删除本地配置文件中已被废弃的项目
            for i in self.deleted_elements_list:
                self.root_config.delete_section(i)
            # 需要自动执行的配置名称的列表
            startwithboot_list = []
            for i in self.all_config_listbox.get(0, self.all_config_listbox.size() - 1):
                # 写入配置
                self.root_config.set_value(i, custom_constant.click_object, self.all_config_dic[i])
                # 检查是否需要自动执行
                if self.all_config_dic[i][0][0]:
                    startwithboot_list.append(i)
            self.root_config.set_value(custom_constant.rootconfig, custom_constant.startwithboot, startwithboot_list)

        Button(self.left_buttons_frame, text='保存所有修改', command=save_all_config).pack(side=TOP, anchor=E)
        # 下级2
        self.show_work_frame = Frame(self.func_frame, width=300, height=150)
        self.show_work_frame.pack_propagate(False)
        self.show_work_frame.pack(side=LEFT)
        self.show_work_frame.update()
        self.all_config_listbox = Listbox(self.show_work_frame,
                                          width=self.show_work_frame.winfo_screenwidth(),
                                          height=self.show_work_frame.winfo_height(), selectmode=BROWSE)
        self.all_config_listbox.pack()
        # 下级3
        self.right_buttons_frame = Frame(self.func_frame)
        self.right_buttons_frame.pack(side=LEFT)

        def add_config():
            event = threading.Event()
            self.init_click_object('', [[], []])

            def start_eduter():
                gui.config_editer.ConfigEditer(self.main_state_window, self.click_object, 'add', None, event)

            def write_to_dic():
                # 写入保存所有配置名称的dic中
                event.wait()
                config_name = self.click_object[0]
                self.all_config_dic[config_name] = self.click_object[1]
                self.all_config_listbox.insert(END, config_name)

            editer_thread = threading.Thread(target=start_eduter)
            write_thread = threading.Thread(target=write_to_dic)
            editer_thread.start()
            write_thread.start()

        Button(self.right_buttons_frame, text='+', width=2, command=add_config).pack(side=TOP, anchor=W)

        def del_config():
            pass

        Button(self.right_buttons_frame, text='-', width=2, command=del_config).pack(side=TOP, anchor=W)

        # 功能区frame(一般指最下方按钮所在frame)
        self.work_frame = Frame(self.main_state_window, width=width_root_window, height=50)
        self.work_frame.pack_propagate(False)
        self.work_frame.pack()

        Button(self.work_frame, text='立即执行全部任务', command=self.execute_all_work).pack()

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
    def init_click_object(self, config_name, action_list):
        self.click_object = click_config.ClickConfig(config_name, action_list).generate_click_object()

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
                    self.all_config_dic[i] = eval(self.root_config.get_value(i, custom_constant.click_object))
        else:
            pass
        print('加载函数结果: ', end='')
        print(self.all_config_dic)

    # 数据处理
    def execute_selected(self, work_mode, send_index=False, event=None):
        curselection = self.all_config_listbox.curselection()
        count_selected = len(curselection)
        if count_selected == 1:
            config_name = self.all_config_listbox.get(curselection[0])
            self.init_click_object(config_name, self.all_config_dic[config_name])
            if send_index:
                gui.config_editer.ConfigEditer(self.main_state_window, self.click_object, work_mode,
                                               curselection[0], event)
            else:
                gui.config_editer.ConfigEditer(self.main_state_window, self.click_object, work_mode)
        elif count_selected == 0:
            gui.custom_messagebox.CustomMessagebox(self.main_state_window, '配置错误', 200, 100, ['未选择配置'])

    def execute_selected_work(self, click_object):
        pass

    def execute_all_work(self):
        # 执行所有任务
        for i in self.all_config_listbox.get(0, self.all_config_listbox.size() - 1):
            def execute():
                func.execute_work.execute_work(i, self.init_click_object(i, self.all_config_dic[i]))
            execute_thread = threading.Thread(target=execute)
            execute_thread.start()
            execute_thread.join()


if __name__ == '__main__':
    MainStateWindow()
