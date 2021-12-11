from tkinter import *
from tkinter.font import Font

import lib.necessary_lib as necessary_lib


class GetXY:
    Message_font_size = 10

    def __init__(self, parent_window, parent_x, parent_y):
        self.parent_window = parent_window
        self.parent_window = parent_window
        self.parent_window.attributes('-disable', True)
        # 主窗口
        self.main_window = Toplevel()
        self.width = 300
        self.height = 200
        # self.width, self.height = necessary_lib.real_screen_size(self.main_window)
        geometry = necessary_lib.middle_screen(self.main_window, self.width, self.height)
        # 窗口属性
        necessary_lib.fit_screen_zoom(self.main_window)
        self.main_window.attributes('-alpha', 0.5)
        self.main_window.title('坐标采集')
        self.main_window.geometry(geometry)
        self.main_window.resizable(False, False)

        self.main_frame = Frame(self.main_window, width=self.width, height=self.height)
        self.main_frame.pack_propagate(False)
        self.main_frame.pack(expand=YES)

        Message(self.main_frame, text='将下方按钮放入文本框内后,点击', width=self.width).pack()

        def get_xy(event):
            parent_x.delete(0, 'end')
            parent_x.insert(0, event.x_root)
            parent_y.delete(0, 'end')
            parent_y.insert(0, event.y_root)

        get_button = Button(self.main_frame, text='点我', width=5, height=1, )
        get_button.pack()
        get_button.bind('<Button-1>', get_xy)

        self.main_window.protocol('WM_DELETE_WINDOW', lambda: self.close())
        self.main_window.mainloop()

    def close(self):
        self.parent_window.attributes('-disable', False)
        self.main_window.destroy()
