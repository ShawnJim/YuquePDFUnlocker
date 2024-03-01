import os
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from pywinauto.application import Application
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import base64

from tools import fix_title

# 定义超时时间
timeout = 60

def init_webdriver(browser_path, driver_path):
    """
    初始化WebDriver。
    """
    chrome_options = Options()
    chrome_options.binary_location = browser_path
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def login_and_prepare(driver, url, password):
    """
    打开网页并准备进行操作。
    """
    driver.get(url)
    driver.maximize_window()
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "ant-input")))
    password_input = driver.find_element(By.XPATH,
                                         "//input[contains(@class, 'ant-input') and contains(@class, 'larkui-input') "
                                         "and contains(@class, 'index-module_input_wnaMD')]")
    password_input.send_keys(password)
    # 其他可能的准备操作
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(@class, 'BookCatalog-module_asideActionsCont_31lvb')]"))).click()
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(@class, 'BookCatalog-module_asideActionsCont_31lvb')]"))).click()


scroll_script = """
function scrollToBottom(scrollDuration) {
    var start = window.pageYOffset,
        end = document.body.scrollHeight,
        distance = end - start,
        scrollStep = distance / (scrollDuration / 15),
        scrollInterval = setInterval(function() {
        if (window.scrollY < end) {
            window.scrollBy(0, scrollStep);
        } else clearInterval(scrollInterval);
    }, 15);
}

scrollToBottom(20000);  // 滚动持续时间，单位为毫秒
"""

def save_pdf_by_cdp(driver, save_path, file_name):
    time.sleep(10)  # 等待页面加载完成（可根据需要调整时间）
    # 从页首移动到页尾
    driver.execute_script(scroll_script)
    time.sleep(20)
    # 使用CDP发送打印命令
    result = driver.execute_cdp_cmd("Page.printToPDF", {
        "landscape": False
    })
    pdf_data = base64.b64decode(result['data'])
    file_name = fix_title(file_name)
    with open(f'{save_path}\\{file_name}.pdf', 'wb') as f:
        f.write(pdf_data)

    time.sleep(5)  # 等待文件保存完成（可根据需要调整时间）

def save_pdf(driver, save_path, file_name):
    """
    使用打印对话框将当前页面保存为PDF。
    """
    # 确保目录存在
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    time.sleep(20)  # 等待页面加载完成（可根据需要调整时间）
    # 从页首移动到页尾
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # 执行Ctrl+P打开打印对话框
    driver.execute_script("window.print();")
    time.sleep(5)  # 等待打印对话框打开

    app = Application(backend="uia").connect(title_re="打印")
    print_dialog = app.window(title_re="打印")

    # 等待并点击保存按钮
    save_button = print_dialog.child_window(title="保存", control_type="Button")
    if not save_button.exists():
        raise Exception("无法找到保存按钮")
    save_button.click()

    # 处理另存为对话框
    time.sleep(2)  # 等待另存为对话框打开
    save_as_dialog = Application(backend="uia").connect(title="另存为")
    dialog = save_as_dialog.window(title="另存为")

    # 输入文件名并保存
    dialog.type_keys(f'{save_path}\\{file_name}', with_spaces=True)
    dialog.type_keys("{ENTER}")

def process_items(driver, save_path):
    """
    处理页面上的每个项目。
    """
    items = driver.find_elements(By.CLASS_NAME, "catalogTreeItem-module_CatalogItem_xkX7p")
    for item in items:
        try:
            title = item.find_element(By.CLASS_NAME, "catalogTreeItem-module_title_snpKw").text
            print(f"处理: {title}")
            # 保存pdf
            save_pdf(driver, save_path, f"{title}")
        except StaleElementReferenceException:
            print("元素状态发生变化，跳过。")
            continue


from selenium.common.exceptions import NoSuchElementException

def scroll_into_view(driver, element):
    """
    滚动浏览器窗口以确保元素在视口内。
    """
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(1)  # 短暂等待，确保页面滚动完成

def get_items(driver):
    """
    获取并返回页面上当前可见的元素列表。
    """
    try:
        virtual_tree = driver.find_element(By.CLASS_NAME, "lark-virtual-tree")
        return virtual_tree.find_elements(By.CLASS_NAME, "catalogTreeItem-module_CatalogItem_xkX7p")
    except NoSuchElementException:
        return []

def wait_for_page_load(driver, timeout=30):
    """
    等待页面加载完成。

    :param driver: WebDriver实例。
    :param timeout: 最长等待时间（秒）。
    """
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )


def scroll_tree_to_under(driver):
    try:
        # 定位到可滑动的div元素
        virtual_tree = driver.find_element(By.CLASS_NAME, "lark-virtual-tree")
        # 使用JavaScript向下滑动
        scroll_amount = 100  # 滑动的像素数，可以根据需要调整
        driver.execute_script("arguments[0].scrollTop += arguments[1];", virtual_tree, scroll_amount)
    except NoSuchElementException:
        print("滑动异常")


def process_items_until_done(driver, save_path):
    """
    循环处理页面上的元素，直到没有新数据。
    """
    file_index = 0
    # 获取文件夹下存在多少文件
    file_count = sum([len(files) for r, d, files in os.walk(save_path)])
    # 存储已获取的数据
    data_set = set()
    collision_counter = 0
    while True:
        items = get_items(driver)
        new_data_found = False
        try:
            for item in items:
                scroll_into_view(driver, item)
                title = item.find_element(By.CLASS_NAME, "catalogTreeItem-module_title_snpKw").text
                if title not in data_set:
                    collision_counter = 0
                    data_set.add(title)
                    new_data_found = True
                    if file_index >= file_count:
                        # 保存pdf
                        links = item.find_elements(By.TAG_NAME, "a")
                        if links:
                            print(f"处理: {title}")
                            links[0].click()
                            # 等待页面加载完成
                            wait_for_page_load(driver)
                            save_pdf_by_cdp(driver, save_path, f"{title}")
                            new_data_found = True
                        else:
                            print(f"{title}, 纯标题，无链接")
                    else:
                        print("文件已处理，跳过！")
                    file_index += 1
                else:
                    print(f"title: {title} 已维护碰撞 {collision_counter} 次")
                    collision_counter += 1
                    scroll_tree_to_under(driver)
                    continue  # 继续处理下一个元素
        except StaleElementReferenceException:
            continue  # 继续处理下一个元素

        if not new_data_found:
            break  # 如果没有发现新数据，说明已经到达底部

        if collision_counter > 5:
            print("以碰撞至少3次, 判断执行完成")
            # 获取最后一个元素
            items = get_items(driver)
            # 下载最后一个
            item = items[len(items) - 1].find_element()
            title = item.find_element(By.CLASS_NAME, "catalogTreeItem-module_title_snpKw").text
            links = item.find_elements(By.TAG_NAME, "a")
            if links:
                print(f"处理: {title}")
                links[0].click()
                # 等待页面加载完成
                wait_for_page_load(driver)
                save_pdf_by_cdp(driver, save_path, f"{title}")
            else:
                print(f"{title}, 纯标题，无链接")
            break
        time.sleep(1)  # 增加等待时间，确保数据加载

    print("处理完成，没有更多数据。")

if __name__ == "__main__":
    browser_path = input("Enter the browser path: ")
    driver_path = input("Enter the driver path: ")
    url = input("Enter the URL: ")
    password = input("Enter the password: ")
    save_path = input("Enter the save path: ")

    driver = init_webdriver(browser_path, driver_path)
    try:
        login_and_prepare(driver, url, password)
        # 适当的等待或导航逻辑来定位到需要导出的页面
        # process_items(driver, save_path)
        process_items_until_done(driver, save_path)
    finally:
        driver.quit()
