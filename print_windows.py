from pywinauto import Desktop, findwindows
from pywinauto.application import Application
from pywinauto.timings import wait_until

from pywinauto import Desktop



def printWindows():
    import re
    from pywinauto import Desktop

    # 获取桌面上所有窗口
    windows = Desktop(backend="uia").windows()

    # 假设你知道标题中包含的文字
    partial_title = "介绍"

    # 通过遍历所有窗口，找到包含这部分标题的窗口
    for w in windows:
        if re.search(partial_title, w.window_text(), re.IGNORECASE):
            browser_window_title = w.window_text()
            break

    print(browser_window_title)  # 打印找到的窗口标题


def print_all():
    windows = Desktop(backend="uia").windows()
    for w in windows:
        print(w.window_text())


browser_window = Desktop(backend="uia").window(title="介绍 - Google Chrome for Testing")
browser_window.print_control_identifiers()
print_dialog = browser_window.child_window(title="打印", control_type="Pane", found_index=1)
print_button = print_dialog.child_window(title="打印", control_type="Button")
if not print_button.exists():
    # 如果找不到“打印”按钮，则尝试查找其他可能的控件
    print_button = print_dialog.child_window(title="打印", control_type="Button", found_index=1)
print_button.click()
