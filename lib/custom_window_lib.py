import threading

from lib import stop_with_main_thread


def close_window(window):
    # 自定义的关闭主窗口时执行的方法
    all_threads = threading.enumerate()
    for i in all_threads:
        stop_with_main_thread.stop_thread(i)
    window.destroy()
