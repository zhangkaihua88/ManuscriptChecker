from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from utils import init_config
from RSC import RSC_Checker


class LoadDriver():
    def __init__(self):
        self.config = init_config()
        self.loadDriver()

    def loadDriver(self):
        options = webdriver.ChromeOptions()
        # To ignore the check of the SSL Certificate
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')

        if self.config.getboolean("Default", "VPN"):
            host = self.config.get("Default", "host")
            port = self.config.get("Default", "port")
            proxy = f"--proxy-server=http://{host}:{port}"
            options.add_argument(proxy)
            proxies = {'https': f'http://{host}:{port}',
                       'http': f'http://{host}:{port}'}
        else:
            proxies = None

        # Full screen display
        options.add_argument("start-maximized")
        # start chrome without showing the browser

        # 隐藏运行
        # options.add_argument('headless')
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # END start chrome without showing the browser

        # # 不加载图片, 提升速度
        # options.add_argument('blink-settings=imagesEnabled=false')

        # options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Chrome(
            executable_path=ChromeDriverManager(proxies=proxies).install(),
            options=options,
        )
        self.driver.execute_cdp_cmd(
            'Page.addScriptToEvaluateOnNewDocument',
            {
                'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
            }
        )

if __name__ == "__main__":
    driver = LoadDriver().driver
    RSC_Checker(driver)
