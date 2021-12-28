import threading
import time
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
        # 本地配置中, 需要启动程序自动执行的额配置名称的列表
        self.auto_execute = None
        # 按优先级排序的本地配置名称列表
        self.config_priority_list = None
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
            self.process_selected('show')

        Button(self.left_buttons_frame, text='查看', command=show_select_config).pack(side=TOP, anchor=E)
        # Button(self.left_buttons_frame, text='暂停').pack(side=TOP, anchor=E)

        def modify_select_config():
            event = threading.Event()
            curselection = ()

            def start_editer():
                nonlocal curselection
                curselection = self.process_selected('modify', True, event)

            def change_in_dic():
                event.wait()
                nonlocal curselection
                if len(curselection) > 0:
                    # 获取当前选中项信息
                    curselection = curselection[0]
                    curname = self.all_config_listbox.get(curselection)
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
                    self.all_config_listbox.activate(curselection)
                    self.all_config_listbox.select_set(curselection)

            editer_thread = threading.Thread(target=start_editer)
            change_thread = threading.Thread(target=change_in_dic)
            editer_thread.start()
            change_thread.start()

        Button(self.left_buttons_frame, text='修改', command=modify_select_config).pack(side=TOP, anchor=E)

        def save_all_config():
            # 删除本地配置文件中已被废弃的项目
            for i in self.deleted_elements_list:
                self.root_config.delete_section(i)
            # 配置优先级列表
            self.root_config.set_value(custom_constant.rootconfig, custom_constant.config_priority,
                                       self.config_priority_list)
            # 需要自动执行的配置名称的列表
            startwithboot_list = []
            for i in self.all_config_listbox.get(0, self.all_config_listbox.size() - 1):
                # 写入配置
                self.root_config.set_value(i, custom_constant.click_object, self.all_config_dic[i])
                # 检查是否需要自动执行

                if len(self.all_config_dic[i][0]) != 0 and self.all_config_dic[i][0][0]:
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

            def start_editer():
                gui.config_editer.ConfigEditer(self.main_state_window, self.click_object, 'add', None, event)

            def write_to_dic():
                # 写入保存所有配置名称的dic中
                event.wait()
                config_name = self.click_object[0]
                if config_name != '':
                    self.all_config_dic[config_name] = self.click_object[1]
                    self.all_config_listbox.insert(END, config_name)
                    self.config_priority_list.append(config_name)

            editer_thread = threading.Thread(target=start_editer)
            write_thread = threading.Thread(target=write_to_dic)
            editer_thread.start()
            write_thread.start()

        Button(self.right_buttons_frame, text='+', width=2, command=add_config).pack(side=TOP, anchor=W)

        def del_config():
            config_name = self.get_selected_name_listbox()
            curselection_index = self.get_selected_index_listbox()
            if self.all_config_listbox.size() != 0:
                self.deleted_elements_list.append(config_name)
                self.all_config_listbox.delete(curselection_index)
                del self.all_config_dic[config_name]
                del self.config_priority_list[curselection_index]
            else:
                gui.custom_messagebox.CustomMessagebox(self.main_state_window, '错误', 200, 100, ['未选择配置'])

        Button(self.right_buttons_frame, text='-', width=2, command=del_config).pack(side=TOP, anchor=W)

        def up_priority():
            self.adjust_config_priority('up')

        def down_priority():
            self.adjust_config_priority('down')

        Button(self.right_buttons_frame, text='↑', width=2, command=up_priority).pack(side=TOP, anchor=W)
        Button(self.right_buttons_frame, text='↓', width=2, command=down_priority).pack(side=TOP, anchor=W)

        # 功能区frame(一般指最下方按钮所在frame)
        self.work_frame = Frame(self.main_state_window, width=width_root_window, height=50)
        self.work_frame.pack_propagate(False)
        self.work_frame.pack()

        Button(self.work_frame, text='立即执行选中任务', command=self.execute_selected_work).grid(row=0, column=0)
        Button(self.work_frame, text='立即执行全部任务', command=self.execute_all_work).grid(row=0, column=1)

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
            # 获取需要自动执行的配置的名称
            config_name_list = self.root_config.get_value(custom_constant.rootconfig, custom_constant.startwithboot)
            if config_name_list != '':
                self.auto_execute = eval(config_name_list)
            # 获取配置显示和执行的优先级
            config_priority = self.root_config.get_value(custom_constant.rootconfig, custom_constant.config_priority)
            if config_priority != '':
                self.config_priority_list = eval(config_priority)
            # 按优先级顺序赋值
            for i in self.config_priority_list:
                self.all_config_listbox.insert(END, i)
                self.all_config_dic[i] = eval(self.root_config.get_value(i, custom_constant.click_object))
        else:
            self.auto_execute = []
            self.config_priority_list = []
        threading.Thread(target=self.auto_execute_work).start()

    def adjust_config_priority(self, change):
        # 配置优先级调整
        # 获取选中项
        curselection_index = self.get_selected_index_listbox()
        if curselection_index != -1:
            if change == 'up':
                # 提高配置执行优先级
                if curselection_index != 0:
                    last_index = curselection_index - 1
                    # 调整 self.config_priority_list
                    tmp = self.config_priority_list[curselection_index]
                    del self.config_priority_list[curselection_index]
                    self.config_priority_list.insert(last_index, tmp)
                    # 调整ui的listbox部分
                    tmp = self.all_config_listbox.get(curselection_index)
                    self.all_config_listbox.delete(curselection_index)
                    self.all_config_listbox.insert(last_index, tmp)
                    self.all_config_listbox.see(last_index)
                    self.all_config_listbox.activate(last_index)
                    self.all_config_listbox.select_set(last_index)
            else:
                # 降低优先级
                if curselection_index != self.all_config_listbox.size() - 1:
                    next_index = curselection_index + 1
                    # 调整 self.config_priority
                    tmp = self.config_priority_list[curselection_index]
                    del self.config_priority_list[curselection_index]
                    self.config_priority_list.insert(next_index, tmp)
                    # 调整ui的listbox部分
                    tmp = self.all_config_listbox.get(curselection_index)
                    self.all_config_listbox.delete(curselection_index)
                    self.all_config_listbox.insert(next_index, tmp)
                    self.all_config_listbox.see(next_index)
                    self.all_config_listbox.activate(next_index)
                    self.all_config_listbox.select_set(next_index)
        else:
            gui.custom_messagebox.CustomMessagebox(self.main_state_window, '配置错误', 200, 100, ['未选择配置'])

    # 数据处理
    def get_selected_index_listbox(self):
        # 获取 self.all_config_listbox 选中项的索引 (当前仅支持单选, 所以返回0号位)
        curselection = self.all_config_listbox.curselection()
        if len(curselection) != 0:
            return curselection[0]
        else:
            return -1

    def get_selected_name_listbox(self):
        # 返回 self.all_config_listbox 选中项的文本
        curselection = self.all_config_listbox.curselection()
        if len(curselection) != 0:
            return self.all_config_listbox.get(self.get_selected_index_listbox())
        else:
            return ''

    def process_selected(self, work_mode, send_index=False, event=None):
        # 处理所选项
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
            if send_index:
                event.set()
        return curselection

    def execute_selected_work(self):
        # 执行所选项
        config_name = self.get_selected_name_listbox()
        if config_name == '':
            gui.custom_messagebox.CustomMessagebox(self.main_state_window, '配置错误', 200, 100, ['未选择配置'])
        else:
            event = threading.Event()

            def execute():
                time.sleep(3)
                if event.is_set() is False:
                    self.init_click_object(config_name, self.all_config_dic[config_name])
                    func.execute_work.execute_work(config_name, self.click_object, event)
                else:
                    if str(tip_thread).find('stopped') == -1:
                        stop_with_main_thread.stop_thread(tip_thread)
                    return

            def check_finish():
                event.wait()

            def tip_window():
                gui.custom_messagebox.CustomMessagebox(self.main_state_window, '任务执行中', 400, 200, ['正在执行任务'],
                                                       False, check_finish, True, event)

            tip_thread = threading.Thread(target=tip_window)
            execute_thread = threading.Thread(target=execute)
            tip_thread.start()
            execute_thread.start()

    def execute_all_work(self):
        # 执行所有任务
        length_all_config_listbox = self.all_config_listbox.size()
        max_index_all_config_listbox = length_all_config_listbox - 1
        if length_all_config_listbox > 0:
            event = threading.Event()

            def execute():
                time.sleep(3)
                index = 0
                for i in self.all_config_listbox.get(0, max_index_all_config_listbox):
                    if event.is_set() is False:
                        self.init_click_object(i, self.all_config_dic[i])
                        func.execute_work.execute_work(i, self.click_object)
                        if index == max_index_all_config_listbox:
                            event.set()
                    else:
                        if str(tip_thread).find('stopped') == -1:
                            stop_with_main_thread.stop_thread(tip_thread)
                        return
                    index += 1
                    # 停止3s再进行下个任务
                    time.sleep(3)

            def check_finish():
                event.wait()

            def tip_window():
                gui.custom_messagebox.CustomMessagebox(self.main_state_window, '任务执行中', 400, 200, ['正在执行任务'],
                                                       False, check_finish, True, event)

            tip_thread = threading.Thread(target=tip_window)
            execute_thread = threading.Thread(target=execute)
            tip_thread.start()
            execute_thread.start()
        else:
            gui.custom_messagebox.CustomMessagebox(self.main_state_window, '配置错误', 200, 100, ['配置为空'])

    def auto_execute_work(self):
        if self.auto_execute is not None and len(self.auto_execute) != 0:
            event = threading.Event()

            def execute():
                index = 0
                max_index_startwithboot_list = len(self.auto_execute) - 1
                time.sleep(3)
                for i in self.auto_execute:
                    if event.is_set() is False:
                        self.init_click_object(i, self.all_config_dic[i])
                        if self.click_object[1][0][0]:
                            time.sleep(int(self.click_object[1][0][1]))
                        func.execute_work.execute_work(i, self.click_object)
                        if index == max_index_startwithboot_list:
                            event.set()
                    else:
                        if str(tip_thread).find('stopped') == -1:
                            stop_with_main_thread.stop_thread(tip_thread)
                        return
                    index += 1
                    time.sleep(3)

            def check_finish():
                event.wait()

            def tip_window():
                gui.custom_messagebox.CustomMessagebox(self.main_state_window, '任务执行中', 400, 200,
                                                       ['检查到需要自动执行的配置', '3s后自动执行任务'],
                                                       False, check_finish, True, event)

            tip_thread = threading.Thread(target=tip_window)
            execute_thread = threading.Thread(target=execute)
            tip_thread.start()
            execute_thread.start()


if __name__ == '__main__':
    MainStateWindow()
