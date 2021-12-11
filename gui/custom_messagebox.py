from tkinter import *
from tkinter.font import Font

import lib.necessary_lib as necessary_lib
import lib.stop_with_main_thread as stop_with_main_thread
import environment.custom_constant.custom_constant


class CustomMessagebox:
    Message_font = 10

    def __init__(self, parent_window, title, width, height, string_list, if_disable_parent=True, func=None,
                 auto_close=False):
        # 传入的自定义方法
        self.func = func
        self.custom_func_thread = stop_with_main_thread.StopWithMainThread(self.func, True)
        # 窗口是否执行过自定义的 close() 方法
        self.if_closed = False
        # 父窗口
        self.parent_window = parent_window
        self.if_disable_parent = if_disable_parent
        if self.if_disable_parent:
            self.parent_window.attributes('-disable', True)
        # 主窗口
        self.msg_window = Toplevel()
        geometry = necessary_lib.middle_screen(self.msg_window, width, height)
        # 窗口属性
        necessary_lib.fit_screen_zoom(self.msg_window)
        self.msg_window.title(title)
        self.msg_window.geometry(geometry)
        self.msg_window.resizable(False, False)
        # 字体
        # self.ft = Font(size=CustomMessagebox.Message_font)
        self.ft = environment.custom_constant.custom_constant.CustomFont().microsoft_yahei

        def main_content():
            # 列表内元素最后将处于不同行,请合理安排内容
            return '\n'.join(string_list)

        # 控件
        parent = Frame(self.msg_window)
        parent.pack(expand=1)
        # 如果没有这一句,winfo_width()将会得到一个错误的结果
        self.msg_window.update_idletasks()
        Message(parent, text=main_content(), width=self.msg_window.winfo_width(), font=self.ft).pack(fill=X)
        # 自定义关闭窗口方法
        self.msg_window.protocol('WM_DELETE_WINDOW', lambda: self.close())

        def custom_func():
            # 执行传入构造函数的方法
            if self.func is not None:
                self.custom_func_thread.run()
            if auto_close and self.if_closed is False:
                # 若窗口设置 auto_close = True ,正常情况下,线程执行成功会自动关闭,即无需执行停止线程操作,传参 False
                self.close(False)
        stop_with_main_thread.StopWithMainThread(custom_func).run()

        # 要在新线程中调用此类,避免报错，注释掉
        # self.msg_window.mainloop()

    def close(self, if_stop_thread=True):
        self.if_closed = True
        if self.func is not None and if_stop_thread:
            son_thread = self.custom_func_thread.thread
            if str(son_thread).find('stopped') == -1:
                # 子线程未被关闭
                stop_with_main_thread.stop_thread(self.custom_func_thread.thread)
        if self.if_disable_parent:
            self.parent_window.attributes('-disable', False)
        self.msg_window.destroy()
