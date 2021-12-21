from tkinter import *
# 自定义lib
import lib.necessary_lib as necessary_lib

# 重要变量定义
width_root_window = 600
height_root_window = 530


class ConfigEditer:
    def __init__(self, parent_window, click_object, work_mode):
        # 形参转对象属性
        self.parent_window = parent_window
        self.click_object = click_object
        self.work_mode = work_mode
        # 传参的处理
        # 禁止操作父窗口
        self.parent_window.attributes('-disable', True)
        # 主窗口
        self.root_window = Toplevel()
        self.root_window.title('配置编辑')
        self.root_window.geometry(necessary_lib.middle_screen(self.root_window, width_root_window, height_root_window))
        necessary_lib.fit_screen_zoom(self.root_window)
        # 主frame
        self.root_frame = Frame(self.root_window)
        self.root_frame.pack()
        # 主功能frame
        self.func_frame = Frame(self.root_frame)
        self.func_frame.pack(expand=YES)
        # Label(text=self.click_object)
        # 下级frame: 1
        self.autoClick_frame = Frame(self.func_frame)
        self.autoClick_frame.grid(row=0)

        def check_state_autoclick_checkbutton():
            if self.autoClick_checkbutton_value.get():
                self.autoClick_entry['state'] = 'normal'
            else:
                self.autoClick_entry['state'] = 'disabled'
        self.autoClick_checkbutton_value = BooleanVar()
        self.autoClick_checkbutton_value.set(False)
        self.autoClick_checkbutton = Checkbutton(self.autoClick_frame, text='自动执行',
                                                 variable=self.autoClick_checkbutton_value,
                                                 onvalue=True, offvalue=False,
                                                 command=check_state_autoclick_checkbutton)
        self.autoClick_checkbutton.grid(row=0, column=0, padx=5)
        Label(self.autoClick_frame, text='延迟执行时间(单位: s)').grid(row=0, column=1, padx=5)
        self.autoClick_entry = Entry(self.autoClick_frame, width=3)
        self.autoClick_entry.grid(row=0, column=2, padx=5)
        # 下级frame: 2
        self.actions_frame = Frame(self.func_frame, width=50)
        self.actions_frame.grid(row=1, column=0)

        self.actions_frame.update()
        self.action_listbox = Listbox(self.actions_frame, width=self.actions_frame.winfo_width())
        self.action_listbox.pack()
        # 下级frame: 3
        self.right_button_frame = Frame(self.func_frame)
        self.right_button_frame.grid(row=1, column=1)

        Button(self.right_button_frame, text='+', width=2, command=self.add_action).grid(row=0)
        Button(self.right_button_frame, text='-', width=2, command=self.del_action).grid(row=1)

        # 控件加载完毕
        if self.work_mode == 'modify':
            pass
        elif self.work_mode == 'show':
            pass
        check_state_autoclick_checkbutton()

        # 主窗口属性
        self.root_window.protocol('WM_DELETE_WINDOW', lambda: self.close())
        self.root_window.mainloop()

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
            if action_type == 'click' or action_type == 'click_blank':
                input_content_text['state'] = 'disabled'
            else:
                input_content_text['state'] = 'normal'

        action_type_value = StringVar()
        action_type_value.set('click')
        click_checkbutton = Radiobutton(action_type_frame, text='模拟点击', variable=action_type_value, value='click',
                                        command=check_state)
        click_checkbutton.grid(row=0, column=0)
        input_checkbutton = Radiobutton(action_type_frame, text='模拟输入', variable=action_type_value, value='input',
                                        command=check_state)
        input_checkbutton.grid(row=0, column=1)
        click_blank_checkbutton = Radiobutton(action_type_frame, text='点击空白处',
                                              variable=action_type_value, value='click_blank',
                                              command=check_state)
        click_blank_checkbutton.grid(row=0, column=2)
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
        # 要键入的内容 #
        input_content_frame = Frame(frame)
        input_content_frame.grid(row=2)
        Label(input_content_frame, text='要键入的内容').grid(row=0)
        input_content_text = Text(input_content_frame, width=50, height=5)
        input_content_text.grid(row=1)
        # 拓展按钮
        extend_frame = Frame(window, width=window.winfo_width(), height=50)
        extend_frame.pack_propagate(False)
        extend_frame.pack(expand=YES)

        def save_config():
            # 数据包装
            action_type = action_type_value.get()

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
        window.mainloop()

    def del_action(self):
        pass

    def close(self):
        if self.work_mode == 'modify' or self.work_mode == 'add':
            pass
        self.parent_window.attributes('-disable', False)
        self.root_window.destroy()
