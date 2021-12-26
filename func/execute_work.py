import os
import time
import webbrowser

import pyautogui
import pyperclip

import environment.custom_constant.custom_constant as custom_constant


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
                pyautogui.click(action_x, action_y)
            if action_type == custom_constant.input_action:
                pyperclip.copy(config_dic[custom_constant.input_content])
                pyautogui.hotkey('ctrl', 'v')
    # 为了剪切板安全
    pyperclip.copy('autoClick')
    if event is not None:
        event.set()


def str_to_int(string):
    if string != '':
        return int(string)
