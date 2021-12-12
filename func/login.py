import time
import webbrowser

import pyautogui
import pyperclip

import gui.custom_messagebox as custom_messagebox
from lib import stop_with_main_thread

# 是否执行完所有函数
is_worked = False


def login(parent_window, click_object):
    def tip_window():
        def recv():
            global is_worked
            while True:
                if is_worked is True:
                    break
                else:
                    time.sleep(2)

        custom_messagebox.CustomMessagebox(parent_window, '正在执行任务', 300, 200, ['正在执行任务...'], True, recv, True)

    stop_with_main_thread.StopWithMainThread(tip_window).run()

    if click_object['web_path'][1] != '':
        print(click_object['web_path'][1])
        webbrowser.open(click_object['web_path'][1])
        time.sleep(5)
    # 点击账号输入框
    if click_object['account_x'][1] != '' and click_object['account_y'][1] != '':
        print('账号坐标:', click_object['account_x'][1], click_object['account_y'][1])
        pyautogui.click(str_to_int(click_object['account_x'][1]), str_to_int(click_object['account_y'][1]))
        print('账号:', click_object['account'][1])
        pyperclip.copy(click_object['account'][1])
        time.sleep(5)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(5)
    # 点击一下空白处
    if click_object['auto_click_blank_x'][1] != '' and click_object['auto_click_blank_y'][1] != '':
        pyautogui.click(str_to_int(click_object['auto_click_blank_x'][1]), str_to_int(click_object['auto_click_blank_y'][1]))
        time.sleep(5)
    # 点击密码框
    if click_object['password_x'][1] != '' and click_object['password_y'][1] != '':
        print('密码坐标:', click_object['password_x'][1], click_object['password_y'][1])
        pyautogui.click(str_to_int(click_object['password_x'][1]), str_to_int(click_object['password_y'][1]))
        print('密码:', click_object['password'][1])
        pyperclip.copy(click_object['password'][1])
        time.sleep(5)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(2)
    # 点击登录按钮
    if click_object['login_x'][1] != '' and click_object['login_y'][1] != '':
        print('登录坐标:', click_object['login_x'][1], click_object['login_y'][1])
        pyautogui.click(str_to_int(click_object['login_x'][1]), str_to_int(click_object['login_y'][1]))

    # 所有语句执行完毕
    global is_worked
    is_worked = True


def str_to_int(string):
    if string != '':
        return int(string)
