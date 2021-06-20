import os
from getgauge.python import before_suite, after_suite, step
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from uuid import uuid1
from getgauge.python import custom_screenshot_writer


class Driver:
    instance = None


@before_suite
def init():
    global driver
    options = Options()
    #  By default the chrom instance is launched in
    #  headless mode. Do not pass this option if
    #  you want to see the browser window
    options.add_argument("--headless")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dedv-shm-usage')
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")

    Driver.instance = webdriver.Chrome(
        executable_path=r'C:\Users\greta\Documents\chromedriver\chromedriver.exe')


@after_suite
def close():
    Driver.instance.close()


@step("Login at <url>")
def go_to_get_started_page():
    Driver.instance.find_element_by_xpath(
        "//input[@name='username']").send_keys("user@gmail.com")
    Driver.instance.find_element_by_xpath(
        "//input[@name='password']").send_keys("123")
    Driver.instance.find_element_by_xpath("//input[@value='Login']").click()


@step("Go to Buzzer homepage at <url>")
def go_to_gauge_homepage_at(url):
    Driver.instance.get(url)

# Return a screenshot file name


@custom_screenshot_writer
def take_screenshot():
    image = Driver.instance.get_screenshot_as_png()
    file_name = os.path.join(
        os.getenv("gauge_screenshots_dir"), "screenshot-{0}.png".format(uuid1().int))
    file = open(file_name, "wb")
    file.write(image)
    return os.path.basename(file_name)
