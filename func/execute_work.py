import os
import threading
import time
import webbrowser

import pyautogui
import pyperclip
from pynput import keyboard

# 自定义环境
import environment.custom_constant.custom_constant as custom_constant

# 自定义lib
from lib import stop_with_main_thread

from pynput.keyboard import Key


def execute_work(config_name, click_object, event=None):
    print('配置名称: ', config_name, end=', ')
    print('click_object 对象: ', click_object)
    for config_dic in click_object[1][1]:
        action_type = config_dic[custom_constant.action_mode]
        if action_type == custom_constant.open_webbroswer_action:
            # 打开网址
            webbrowser.open(config_dic[custom_constant.input_content])
            # 等待5s, 防止机器运行缓慢导致非理想结果
            time.sleep(5)
        elif action_type == custom_constant.open_file_action:
            os.stat(config_dic[custom_constant.input_content])
            # 等待5s, 防止机器运行缓慢导致非理想结果
            time.sleep(5)
        elif action_type == custom_constant.click_action or action_type == custom_constant.input_action:
            # 点击/输入
            action_x = str_to_int(config_dic[custom_constant.action_x])
            action_y = str_to_int(config_dic[custom_constant.action_y])
            if action_x != '' and action_y != '':
                click_work(config_dic, action_x, action_y)
            if action_type == custom_constant.input_action:
                pyperclip.copy(config_dic[custom_constant.input_content])
                pyautogui.hotkey('ctrl', 'v')
    # 为了剪切板安全
    pyperclip.copy('autoClick')
    if event is not None:
        event.set()


def click_work(config_dic, x, y):
    click_type = config_dic[custom_constant.click_type]
    if click_type == custom_constant.click_type_once:  # 普通(单次点击)模式
        print('单次点击')
        pyautogui.click(x, y)
    elif click_type == custom_constant.click_type_continuous:  # 连点模式
        print('连点模式')

        def click():
            while True:
                pyautogui.click(x, y)

        click_thread = threading.Thread(target=click)

        def quit_click_keypress_inside(key):
            quit_click_keypress(key, click_thread)

        listener = keyboard.Listener(
            on_press=quit_click_keypress_inside, on_release=quit_click_keyrelease
        )
        listener.start()
        click_thread.start()
        click_thread.join()


def quit_click_keypress(key, click_thread):  # 当设定的按钮按下, 退出连点模式
    if key == Key.esc:
        stop_with_main_thread.stop_thread(click_thread)


def quit_click_keyrelease(key):  # 暂时不需要
    pass


def str_to_int(string):
    if string != '':
        return int(string)
