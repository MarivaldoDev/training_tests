from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager


def make_browser(*options):
    chrome_options = Options()

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    chrome_service = Service(ChromeDriverManager().install())
    browser = WebDriver(service=chrome_service, options=chrome_options)

    return browser
