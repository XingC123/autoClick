from gui import custom_messagebox


def info_app_info_menu(window):
    width = 500
    height = 200
    msg_list = ['软件名: 自动点击登录', '版本: 2.5', '日期: 21.12.26', '作者: XingC',
                '邮箱: 123fengmo@gmail.com', '声明: 仅做学习交流之用,因其他用法造成的一切问题本人概不负责']
    custom_messagebox.CustomMessagebox(window, '关于软件', width, height, msg_list)
