import webbrowser
import pyautogui
import time


def open():
    # 先打开指定网页
    webbrowser.open("http://10.10.11.2/gportal/web/login")


def click():
    # 开始执行点击
    # 点击账号框
    pyautogui.click(1515, 538)
    time.sleep(5)
    # 点击输入框后浏览器会自动弹出已保存的密码
    pyautogui.click(1487, 703)
    time.sleep(2)
    # 点击登录按钮
    pyautogui.click(1413, 624)


if __name__ == '__main__':
    print('正在执行任务...')
    open()
    # 给电脑足够时间来打开网页
    time.sleep(15)
    click()
