import copy
import threading
from tkinter import *

# 自定义环境 environment
import environment.config.click_config as click_config
import environment.custom_constant.custom_constant as custom_constant
# 自定义gui
import gui.get_xy_window
# 自定义lib
import gui.custom_messagebox
import lib.necessary_lib as necessary_lib

# 重要变量定义
width_root_window = 600
height_root_window = 530


class ConfigEditer:
    def __init__(self, parent_window, click_object, work_mode, index=None, event=None):
        # 形参转对象属性
        self.parent_window = parent_window
        self.click_object = click_object
        self.work_mode = work_mode
        self.index = index
        self.event = event
        # 传参的处理
        # 禁止操作父窗口
        self.parent_window.attributes('-disable', True)
        # 保存所有动作的列表
        self.click_object_copy = copy.deepcopy(self.click_object)
        # 主窗口
        self.root_window = Toplevel()
        self.root_window.title('配置编辑')
        self.root_window.geometry(necessary_lib.middle_screen(self.root_window, width_root_window, height_root_window))
        self.root_window.resizable(False, False)
        necessary_lib.fit_screen_zoom(self.root_window)
        # 主frame
        self.root_frame = Frame(self.root_window)
        self.root_frame.pack()
        # 主功能frame
        self.func_frame = Frame(self.root_frame)
        self.func_frame.pack(expand=YES)
        # Label(text=self.click_object_copy)
        # 下级frame: 1
        self.config_name_frame = Frame(self.func_frame)
        self.config_name_frame.grid(row=0)
        Label(self.config_name_frame, text='配置名称').grid(row=0, column=0)
        self.config_name_entry = Entry(self.config_name_frame, width=20)
        self.config_name_entry.grid(row=0, column=1)
        # 下级frame: 2
        self.autoClick_frame = Frame(self.func_frame)
        self.autoClick_frame.grid(row=1)

        def check_state_autoclick_checkbutton():
            if self.autoClick_checkbutton_value.get():
                self.autoClick_interval_entry['state'] = 'normal'
            else:
                self.autoClick_interval_entry['state'] = 'disabled'

        self.autoClick_checkbutton_value = BooleanVar()
        self.autoClick_checkbutton_value.set(False)
        self.autoClick_checkbutton = Checkbutton(self.autoClick_frame, text='自动执行',
                                                 variable=self.autoClick_checkbutton_value,
                                                 onvalue=True, offvalue=False,
                                                 command=check_state_autoclick_checkbutton)
        self.autoClick_checkbutton.grid(row=0, column=0, padx=5)
        Label(self.autoClick_frame, text='延迟执行时间(单位: s)').grid(row=0, column=1, padx=5)
        self.autoClick_interval_entry = Entry(self.autoClick_frame, width=3)
        self.autoClick_interval_entry.grid(row=0, column=2, padx=5)
        # 下级frame: 3
        self.actions_frame = Frame(self.func_frame, width=50)
        self.actions_frame.grid(row=2, column=0)

        self.actions_frame.update()
        self.action_listbox = Listbox(self.actions_frame, width=self.actions_frame.winfo_width())
        self.action_listbox.pack()
        # 下级frame: 4
        self.right_button_frame = Frame(self.func_frame)
        self.right_button_frame.grid(row=2, column=1)

        if self.work_mode != 'show':
            # 不是"查看配置"才可以显示"添加"和"删除"按钮
            Button(self.right_button_frame, text='+', width=2, command=self.add_action).grid(row=0)
            Button(self.right_button_frame, text='-', width=2, command=self.del_action).grid(row=1)

            def up_priority():
                self.adjust_config_priority('up')

            def down_priority():
                self.adjust_config_priority('down')

            Button(self.right_button_frame, text='↑', width=2, command=up_priority).grid(row=2)
            Button(self.right_button_frame, text='↓', width=2, command=down_priority).grid(row=3)

        # 保存配置按钮
        def save_config():
            self.save_config()

        if self.work_mode != 'show':
            Button(self.func_frame, text='保存', command=save_config).grid(row=3)

        # 控件加载完毕
        self.init_elements_state(self.work_mode)
        check_state_autoclick_checkbutton()

        # 主窗口属性
        self.root_window.protocol('WM_DELETE_WINDOW', lambda: self.close())
        # self.root_window.mainloop()

    # 主窗口控件赋值

    # 主窗口控件其他方法
    def init_elements_state(self, work_mode):
        # 配置名称
        self.config_name_entry.insert(0, self.click_object_copy[0])
        if work_mode == 'show':
            self.config_name_entry['state'] = DISABLED
        if work_mode == 'show' or work_mode == 'modify':
            # 自动点击启用与否以及延迟间隔
            if len(self.click_object_copy[1][0]) != 0:
                self.autoClick_checkbutton_value.set(self.click_object_copy[1][0][0])
            if self.autoClick_checkbutton_value.get():
                self.autoClick_interval_entry.insert(0, self.click_object_copy[1][0][1])
            # 中间动作列表
            for i in self.click_object_copy[1][1]:
                self.action_listbox.insert(END, click_config.ClickConfig().print_click_object(i))

    def save_config(self):
        config_name = self.config_name_entry.get()
        tip_close_event = threading.Event()

        def tip_window_success():
            gui.custom_messagebox.CustomMessagebox(self.root_window, '成功', 250, 100, ['保存成功'], True, None, False,
                                                   tip_close_event)

        def close():
            tip_close_event.wait()
            self.close()

        if len(config_name) != 0 and (len(self.click_object_copy[1][0]) != 0 or len(self.click_object_copy[1][1]) != 0):
            # 在"配置名不为空"和"配置内容不为空"的情况下进行保存操作
            # 保存"自动执行"和"延迟执行时间"
            auto_click = self.autoClick_checkbutton_value.get()
            autoclick_interval = self.autoClick_interval_entry.get()
            length_autoclick_interval = len(autoclick_interval)
            length_auto_click_list = len(self.click_object_copy[1][0])
            # 是否所有选项都符合要求
            auto_click_finish = False
            if length_auto_click_list == 0:
                # 长度为0, 说明"work_mode = add"
                if auto_click:
                    if length_autoclick_interval == 0:
                        gui.custom_messagebox.CustomMessagebox(self.root_window, '配置错误', 250, 100, ['延迟时间不能为空'])
                    else:
                        self.click_object[1][0].append(auto_click)
                        self.click_object[1][0][0] = auto_click
                        self.click_object[1][0].append(autoclick_interval)
                        auto_click_finish = True
                else:
                    self.click_object[1][0].append(auto_click)
                    auto_click_finish = True
            else:
                # "自动执行功能"
                if self.click_object[1][0][0]:
                    if auto_click:
                        if length_autoclick_interval == 0:
                            gui.custom_messagebox.CustomMessagebox(self.root_window, '配置错误', 250, 100, ['延迟时间不能为空'])
                        else:
                            self.click_object[1][0][0] = auto_click
                            self.click_object[1][0][1] = autoclick_interval
                            auto_click_finish = True
                    else:
                        self.click_object[1][0][0] = False
                        auto_click_finish = True
                else:
                    if auto_click:
                        if length_autoclick_interval == 0:
                            gui.custom_messagebox.CustomMessagebox(self.root_window, '配置错误', 250, 100, ['延迟时间不能为空'])
                        else:
                            self.click_object[1][0][0] = auto_click
                            self.click_object[1][0].append(autoclick_interval)
                            auto_click_finish = True
                    else:
                        auto_click_finish = True
            if auto_click_finish:
                self.click_object[0] = config_name
                # 保存所有更改到 click_object
                # self.click_object = copy.deepcopy(self.click_object_copy)
                self.click_object[1][1] = []
                for i in self.click_object_copy[1][1]:
                    self.click_object[1][1].append(i)
                tip_thread = threading.Thread(target=tip_window_success)
                close_thread = threading.Thread(target=close)
                tip_thread.start()
                close_thread.start()
        else:
            gui.custom_messagebox.CustomMessagebox(self.root_window, '配置错误', 250, 100, ['配置名称或配置为空'])

    def del_action(self):
        index = self.action_listbox.curselection()
        if len(index) != 0:
            self.action_listbox.delete(index[0])
            del self.click_object_copy[1][1][index[0]]
        else:
            gui.custom_messagebox.CustomMessagebox(self.root_window, '错误', 200, 200, ['未选中操作项'])

    def adjust_config_priority(self, change):
        # 配置优先级调整
        # 获取选中项
        curselection_index = self.get_selected_index_listbox()
        if curselection_index != -1:
            if change == 'up':
                # 提高配置执行优先级
                if curselection_index != 0:
                    last_index = curselection_index - 1
                    # 调整 click_pbject_copy
                    action_list = self.click_object_copy[1][1]
                    tmp = action_list[curselection_index]
                    del action_list[curselection_index]
                    action_list.insert(last_index, tmp)
                    # 调整ui的listbox部分
                    tmp = self.action_listbox.get(curselection_index)
                    self.action_listbox.delete(curselection_index)
                    self.action_listbox.insert(last_index, tmp)
                    self.action_listbox.see(last_index)
                    self.action_listbox.activate(last_index)
                    self.action_listbox.select_set(last_index)
            else:
                # 降低优先级
                if curselection_index != self.action_listbox.size() - 1:
                    next_index = curselection_index + 1
                    # 调整 click_pbject_copy
                    action_list = self.click_object_copy[1][1]
                    tmp = action_list[curselection_index]
                    del action_list[curselection_index]
                    action_list.insert(next_index, tmp)
                    # 调整ui的listbox部分
                    tmp = self.action_listbox.get(curselection_index)
                    self.action_listbox.delete(curselection_index)
                    self.action_listbox.insert(next_index, tmp)
                    self.action_listbox.see(next_index)
                    self.action_listbox.activate(next_index)
                    self.action_listbox.select_set(next_index)
        else:
            gui.custom_messagebox.CustomMessagebox(self.root_window, '配置错误', 200, 100, ['未选择配置'])

    def close(self):
        if self.work_mode == 'modify' or self.work_mode == 'add':
            if self.event is not None:
                self.event.set()
        self.parent_window.attributes('-disable', False)
        self.root_window.destroy()

    # 数据处理
    def get_selected_index_listbox(self):
        # 获取 self.all_config_listbox 选中项的索引 (当前仅支持单选, 所以返回0号位)
        curselection = self.action_listbox.curselection()
        if len(curselection) != 0:
            return curselection[0]
        else:
            return -1

    def get_selected_name_listbox(self):
        # 返回 self.all_config_listbox 选中项的文本
        curselection = self.action_listbox.curselection()
        if len(curselection) != 0:
            return self.action_listbox.get(self.get_selected_index_listbox())
        else:
            return ''

    # 添加动作
    def add_action(self):
        self.root_window.attributes('-disable', True)
        window = Toplevel()
        window.title('动作类型')
        window.geometry(necessary_lib.middle_screen(window, 500, 400))
        necessary_lib.fit_screen_zoom(window)
        window.update()
        frame = Frame(window, width=window.winfo_width(), height=window.winfo_height() - 50)
        frame.pack_propagate(False)
        frame.pack()
        # 动作类型选择
        action_type_frame = Frame(frame)
        action_type_frame.grid(row=0)

        def check_state():
            action_type = action_type_value.get()
            if action_type == custom_constant.click_action:
                action_x_entry['state'] = NORMAL
                action_y_entry['state'] = NORMAL
                input_content_text['state'] = 'disabled'
            elif action_type == custom_constant.input_action:
                action_x_entry['state'] = NORMAL
                action_y_entry['state'] = NORMAL
                input_content_text['state'] = 'normal'
            elif action_type == custom_constant.open_webbroswer_action or \
                    action_type == custom_constant.open_file_action:
                action_x_entry['state'] = DISABLED
                action_y_entry['state'] = DISABLED
                input_content_text['state'] = 'normal'

        action_type_value = StringVar()
        action_type_value.set('click')
        click_checkbutton = Radiobutton(action_type_frame, text='模拟点击', variable=action_type_value,
                                        value=custom_constant.click_action, command=check_state)
        click_checkbutton.grid(row=0, column=0)
        input_checkbutton = Radiobutton(action_type_frame, text='模拟输入', variable=action_type_value,
                                        value=custom_constant.input_action, command=check_state)
        input_checkbutton.grid(row=0, column=1)
        # click_blank_checkbutton = Radiobutton(action_type_frame, text='点击空白处',
        #                                       variable=action_type_value, value='click_blank',
        #                                       command=check_state)
        # click_blank_checkbutton.grid(row=0, column=2)
        open_webbroswer = Radiobutton(action_type_frame, text='打开网址',
                                      variable=action_type_value, value=custom_constant.open_webbroswer_action,
                                      command=check_state)
        open_webbroswer.grid(row=0, column=2)
        open_file = Radiobutton(action_type_frame, text='打开程序',
                                variable=action_type_value, value=custom_constant.open_file_action,
                                command=check_state)
        open_file.grid(row=0, column=3)
        # 动作属性选择
        action_attribute_frame = Frame(frame)
        action_attribute_frame.grid(row=1)
        # 坐标 #
        Label(action_attribute_frame, text='坐标').grid(row=0, column=0, padx=5)
        Label(action_attribute_frame, text='X').grid(row=0, column=1, padx=5)
        action_x_entry = Entry(action_attribute_frame, width=5)
        action_x_entry.grid(row=0, column=2, padx=5)
        Label(action_attribute_frame, text='Y').grid(row=0, column=3, padx=5)
        action_y_entry = Entry(action_attribute_frame, width=5)
        action_y_entry.grid(row=0, column=4, padx=5)

        def get_xy():
            gui.get_xy_window.GetXY(window, action_x_entry, action_y_entry)

        Button(action_attribute_frame, text='采集', command=get_xy).grid(row=0, column=5, padx=5)
        click_type = StringVar()
        click_type.set('once')
        click_type_once_checkbox = Checkbutton(action_attribute_frame, text='单次点击',
                                               variable=click_type, onvalue=custom_constant.click_type_once)
        click_type_once_checkbox.grid(row=1, column=2, padx=5)
        click_type_continuous_checkbox = Checkbutton(action_attribute_frame, text='持续点击(ESC退出点击)',
                                                     variable=click_type, onvalue=custom_constant.click_type_continuous)
        click_type_continuous_checkbox.grid(row=1, column=4, padx=5)
        # 要键入的内容 #
        input_content_frame = Frame(frame)
        input_content_frame.grid(row=2)
        Label(input_content_frame, text='要键入的内容/要打开的网址(格式务必正确)/要打开的文件(完整路径)').grid(row=0)
        input_content_text = Text(input_content_frame, width=50, height=5)
        input_content_text.grid(row=1)
        # 拓展按钮
        extend_frame = Frame(window, width=window.winfo_width(), height=50)
        extend_frame.pack_propagate(False)
        extend_frame.pack(expand=YES)

        def save_config():
            # 数据包装
            action_type = action_type_value.get()
            curlength_action_list = len(self.click_object_copy[1][1])
            self.click_object_copy[1][1].append({custom_constant.action_mode: action_type,
                                                 custom_constant.action_x: action_x_entry.get(),
                                                 custom_constant.action_y: action_y_entry.get(),
                                                 custom_constant.click_type: click_type.get()
                                                 })
            if action_type == custom_constant.input_action or action_type == custom_constant.open_webbroswer_action or \
                    action_type == custom_constant.open_file_action:
                self.click_object_copy[1][1][curlength_action_list][custom_constant.input_content] = \
                    input_content_text.get(1.0, END)
            self.action_listbox.insert(END,
                                       click_config.ClickConfig('', []).print_click_object(
                                           self.click_object_copy[1][1][curlength_action_list]))
            # 关闭窗口
            close()

        Button(extend_frame, text='保存', command=save_config).grid(row=0, column=0)

        def clean_input():
            pass

        Button(extend_frame, text='清空已输入', command=clean_input).grid(row=0, column=1)

        # 控件加载完成后
        check_state()

        def close():
            self.root_window.attributes('-disable', False)
            window.destroy()

        window.protocol('WM_DELETE_WINDOW', lambda: close())
        # window.mainloop()
