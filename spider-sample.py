import os
import time

import pyautogui
import pyperclip
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from tools import fix_title


def save_file(path):
    if not os.path.exists(path):
        # 如果目录不存在，则创建目录
        os.mkdir(path)
    else:
        print('目录已存在')
    title = driver.title
    print('页面标题：', title)
    # 获取浏览器窗口的位置
    browser_window = driver.get_window_rect()

    # 将鼠标移动到浏览器窗口的中心，并单击
    browser_center_x = browser_window['x'] + browser_window['width'] // 2
    browser_center_y = browser_window['y'] + browser_window['height'] // 2
    pyautogui.click(browser_center_x, browser_center_y)
    # 等待一段时间确保浏览器窗口获得焦点
    time.sleep(1)
    # 使用 pyautogui 模拟按下 Ctrl + P
    pyautogui.hotkey('ctrl', 'p')
    time.sleep(1)
    # 输入打印文件的路径
    title = fix_title(title)
    pyperclip.copy(title)
    time.sleep(5)
    pyautogui.press('enter')  # 模拟按下回车键
    time.sleep(3)
    # 模拟粘贴操作
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(3)
    # 模拟按下 alt + d 进入文件名输入框
    pyautogui.hotkey('alt', 'd')
    time.sleep(3)
    # 模拟按下退格键
    pyautogui.press('backspace')
    time.sleep(3)
    # 输入打印文件的路径
    pyperclip.copy(path)
    time.sleep(1)
    # 模拟粘贴操作
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(3)
    # 模拟按下 enter 键确认打印
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.press('enter')
    time.sleep(2)

    pyautogui.press('enter')
    # 关闭浏览器
    time.sleep(20)


def handover_new_handles(original_window):
    # 获取所有窗口句柄
    all_windows = driver.window_handles
    # 找到新窗口句柄
    new_window = [window for window in all_windows if window != original_window][0]
    # 切换到新窗口
    driver.switch_to.window(new_window)

# 设置 Chrome 选项
chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--print-to-pdf-no-header')
chrome_options.add_argument('--print-to-pdf=D:/PycharmProjects/spider-yuque-doc/kafka.pdf')  # 指定输出 PDF 的文件名

# 初始化 WebDriver
# 创建 WebDriver 实例，传递 executable_path 参数
driver_path = input("Enter the driver path")
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)


url = input("Enter the url: ")
passwd = input("Enter the password: ")
# 打开网页
driver.get(url)
# 最大化窗口
driver.maximize_window()
# 等待页面加载
time.sleep(5)
# 在这里模拟输入密码等操作
password_input = driver.find_element(By.XPATH, "//input[contains(@class, 'ant-input') and contains(@class, 'larkui-input') and contains(@class, 'index-module_input_wnaMD')]")
password_input.send_keys(passwd)

# 等待页面完全加载
time.sleep(5)

# 等待页面加载完成
driver.implicitly_wait(10)

# 等待页面完全加载
time.sleep(1)

docs = driver.find_elements(By.XPATH, "//div[contains(@class, 'catalogTreeItem-module_CatalogItem_xkX7p')]")

# 获取当前窗口句柄
original_window = driver.current_window_handle
for index, doc in enumerate(docs):
    if index < len(docs) / 2:
        doc = docs[index].find_element(By.TAG_NAME, 'a')
        ActionChains(driver).key_down(Keys.CONTROL).click(doc).key_up(Keys.CONTROL).perform()
        # 切换到新窗口句柄
        handover_new_handles(original_window)
        save_file('D:/PycharmProjects/spider-yuque-doc/Kafka常见面试题知识点总结/')
        # 关闭新窗口
        driver.close()
        # 切换回原来的窗口
        driver.switch_to.window(original_window)

time.sleep(1)

# 关闭浏览器
driver.quit()
