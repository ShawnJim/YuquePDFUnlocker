from pywinauto import Desktop, findwindows
from pywinauto.application import Application


def printWindows():
    # 获取桌面上所有窗口
    desktop = Desktop(backend="uia")

    # 查找与当前激活的selenium窗口句柄对应的pywinauto窗口
    browser_windows = findwindows.find_elements(class_name='Chrome_WidgetWin_1')

    # 筛选出正确的窗口
    for w_handle in browser_windows:
        window = desktop.window(handle=w_handle.handle)
        print(window.window_text())

# # 打印浏览器窗口的所有直接子窗口的标题
# for child in browser_window.children():
#     print(child.window_text())

# 如果找到“另存为”对话框，可以直接与它交互
# 例如:
# browser_window_title = "SpringBoot 常见面试题总结 - Google Chrome"
# browser_window = Desktop(backend="uia").window(title="打印")
# browser_window.print_control_identifiers()
# save_as_dialog = browser_window.child_window(title="将打印输出另存为", control_type="Window")
# save_as_dialog.print_control_identifiers()

# app = Desktop(backend="uia").window(title="打印")
# app.print_control_identifiers()


# printWindows()

from pywinauto import Application

app = Application(backend="uia").connect(title_re=".*Chrome.*", found_index=0)
print_dialog = app.window(title_re=".*打印.*")

# 假设预览区域是最深层的Pane控件
# 此处的定位可能需要根据实际Inspect工具观察的结果进行调整
preview_pane = print_dialog.Pane.child_window(control_type="Pane", found_index=0)
