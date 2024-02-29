from pywinauto import Desktop, findwindows
from pywinauto.application import Application
from pywinauto.timings import wait_until
from pywinauto.keyboard import send_keys
import time
from pywinauto import Desktop



def printWindows():
    import re
    from pywinauto import Desktop

    # 获取桌面上所有窗口
    windows = Desktop(backend="uia").windows()

    # 假设你知道标题中包含的文字
    partial_title = "高性能"

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


# printWindows()

browser_window = Desktop(backend="uia").window(title="高性能：有哪些常见的 SQL 优化手段？ - Google Chrome for Testing")
browser_window.print_control_identifiers()
print_dialog = browser_window.child_window(title="打印", control_type="Pane", found_index=1)
# 寻找目标打印机的下拉框
# 定位到可能的目标打印机下拉列表的ComboBox控件
printer_combobox = print_dialog.child_window(control_type='ComboBox', found_index=0)
# 展开下拉列表
printer_combobox.click_input()
# 假设已经点击了下拉框，下拉框已展开
# 使用方向键（向下键）来选择需要的选项
# 假设“另存为PDF”选项是第一个选项，只需按一次向下键。如果不是第一个，相应地增加按键次数
send_keys('{DOWN}')
send_keys('{DOWN}')
# 等待一小段时间，确保按键操作被处理
time.sleep(1)
# 按回车键确认选择
send_keys('{ENTER}')