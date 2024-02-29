import os
import pyautogui
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pywinauto.application import Application
from pywinauto import Desktop
from pywinauto.keyboard import send_keys
from pywinauto.timings import wait_until
import time
from tools import fix_title

from selenium.common.exceptions import StaleElementReferenceException

# 定义超时时间（例如30秒）
timeout = 60


def get_print_border():
    # 获取浏览器窗口的位置
    browser_window = driver.get_window_rect()
    # 将鼠标移动到浏览器窗口的中心，并单击
    browser_center_x = browser_window['x'] + browser_window['width'] // 2
    browser_center_y = browser_window['y'] + browser_window['height'] // 2
    pyautogui.click(browser_center_x, browser_center_y)
    # 使用 pyautogui 模拟按下 Ctrl + P
    pyautogui.hotkey('ctrl', 'p')
    time.sleep(30)


def save_file(path):
    if not os.path.exists(path):
        # 如果目录不存在，则创建目录
        os.mkdir(path)
    else:
        print('目录已存在')
    title = driver.title
    print('页面标题：', title)
    # 使用 Selenium 模拟按下 Ctrl + P 打开打印对话框
    get_print_border()
    # 等待打印对话框出现
    browser_window_title = driver.title + " - Google Chrome for Testing"
    wait_until(timeout, 1, lambda: Desktop(backend="uia").window(title=browser_window_title).exists())
    browser_window = Desktop(backend="uia").window(title=browser_window_title)
    browser_window = Desktop(backend="uia").window(title=browser_window_title)
    print_dialog = browser_window.child_window(title="打印", control_type="Pane", found_index=0)
    print_button = print_dialog.child_window(title="打印", control_type="Button")
    if not print_button.exists():
        # 如果找不到“打印”按钮，则尝试查找其他可能的控件
        print_button = print_dialog.child_window(title="打印", control_type="Button", found_index=1)
    print_button.click()
    # 等待页面加载完成，保证导出数据不异常
    time.sleep(5)

    # 连接到“另存为”对话框
    # 等待“另存为”对话框出现，最多等待60秒
    wait_until(timeout, 1, lambda: browser_window.child_window(title="将打印输出另存为", control_type="Window").exists())
    time.sleep(2)
    save_as_dialog = browser_window.child_window(title="将打印输出另存为", control_type="Window")
    # 设置文件夹视图
    # 发送 Alt + D 快捷键激活地址栏
    save_as_dialog.type_keys("%d")
    # 然后发送你想要输入的路径
    send_keys(f'{path}'+r'/{ENTER}')
    # 设置文件名并保存
    file_name = f"{fix_title(title)}.pdf"
    # 获取文件名编辑框
    file_name_edit = save_as_dialog.child_window(auto_id="1001", control_type="Edit")
    # 设置文件名
    file_name_edit.set_text(file_name)
    # 找到并点击保存按钮
    save_button = save_as_dialog.child_window(title="保存(S)", auto_id="1", control_type="Button")
    save_button.click()

    time.sleep(10)



def handover_new_handles(original_window):
    # 等待新窗口出现
    WebDriverWait(driver, timeout).until(EC.number_of_windows_to_be(2))
    # 获取所有窗口句柄
    all_windows = driver.window_handles
    # 找到新窗口句柄
    new_window = [window for window in all_windows if window != original_window][0]
    # 切换到新窗口
    driver.switch_to.window(new_window)


# 设置 Chrome 选项
chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--print-to-pdf-no-header')
# chrome_options.add_argument('--print-to-pdf=D:/PycharmProjects/spider-yuque-doc/kafka.pdf')  # 指定输出 PDF 的文件名
browser_path = input("Enter the browser path")
chrome_options.binary_location = browser_path

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
WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "ant-input")))

# 在这里模拟输入密码等操作
password_input = driver.find_element(By.XPATH, "//input[contains(@class, 'ant-input') and contains(@class, 'larkui-input') and contains(@class, 'index-module_input_wnaMD')]")
password_input.send_keys(passwd)

WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'BookCatalog-module_asideActionsCont_31lvb')]"))).click()
WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'BookCatalog-module_asideActionsCont_31lvb')]"))).click()

# 定位到 lark-virtual-tree 元素
virtual_tree = driver.find_element(By.CLASS_NAME, "lark-virtual-tree")

# 存储已获取的数据
data_set = set()

# 获取当前窗口句柄
original_window = driver.current_window_handle


# 定位到 lark-virtual-tree 元素并获取其子元素
def get_items():
    virtual_tree = driver.find_element(By.CLASS_NAME, "lark-virtual-tree")
    return virtual_tree.find_elements(By.CLASS_NAME, "catalogTreeItem-module_CatalogItem_xkX7p")


# 定义一个函数，确保元素在视口内
def scroll_into_view(element):
    driver.execute_script("arguments[0].scrollIntoView();", element)
    WebDriverWait(driver, timeout).until(EC.visibility_of(element))  # 等待元素可见


file_index = 0
save_path = input('保存地址')
# 获取文件夹下存在多少文件
file_count = sum([len(files) for r, d, files in os.walk(save_path)])
# 循环直到没有新数据
while True:
    # 重新获取当前可见的元素
    items = get_items()
    new_data_found = False

    for item in items:
        try:
            # 确保元素在视口内
            scroll_into_view(item)

            title = item.find_element(By.CLASS_NAME, "catalogTreeItem-module_title_snpKw").text
            links = item.find_elements(By.TAG_NAME, "a")
            if links:
                link = links[0].get_attribute("href")
                data = (title, link)

                if data not in data_set:
                    data_set.add(data)
                    new_data_found = True
                    print(f"标题: {title}, 链接: {link}")
                    if file_index >= file_count:
                        time.sleep(5)
                        ActionChains(driver).key_down(Keys.CONTROL).click(links[0]).key_up(Keys.CONTROL).perform()
                        # 切换到新窗口句柄
                        handover_new_handles(original_window)
                        save_file(save_path)
                        # 关闭新窗口
                        driver.close()
                        # 切换回原来的窗口
                        driver.switch_to.window(original_window)
                    else:
                        print("文件已处理，跳过！")
                    file_index += 1
            else:
                print(f"标题: {title} 没有链接")
        except StaleElementReferenceException:
            # 元素过期，重新获取 items
            items = get_items()
            continue  # 继续处理下一个元素

    if not new_data_found:
        break  # 如果没有发现新数据，说明已经到达底部

    time.sleep(1)  # 增加等待时间，确保数据加载

driver.quit()
