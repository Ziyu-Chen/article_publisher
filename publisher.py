import selenium
import clipboard
import time
import datetime
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

EXECUTABLE_PATH = '/Users/ziyu/Desktop/chromedriver.exe'


class Publisher:
    def __init__(self, urls, selectors):
        self.browser = None
        self.urls = urls
        self.selectors = selectors

    def init_browser(self):
        # Initialize the browser
        options = Options()
        options.add_argument('no-sandbox')
        options.add_argument("--user-data-dir=chrome-data")
        options.add_experimental_option('excludeSwitches',
                                        ['enable-automation'])
        options.add_experimental_option(
            'prefs', {'profile.managed_default_content_settings.images': 2})
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(executable_path=EXECUTABLE_PATH)
        self.browser.implicitly_wait(1)
        self.browser.maximize_window()

    def open(self, url):
        self.browser.get(url)

    def wait(self, wait_time):
        self.browser.implicitly_wait(wait_time)

    def load(self, wait_time=1):
        # Record the starting time
        start = datetime.datetime.now()
        max_height = self.browser.execute_script(
            "return document.body.scrollHeight")
        while True:
            # Scroll down bit by bit
            for i in range(int(max_height / 500)):
                self.browser.execute_script("window.scrollTo(0, %d);" %
                                            (i * 500))

            # Wait for the page to load
            time.sleep(wait_time)

            # Calculate the current scrollHeight
            current_height = self.browser.execute_script(
                "return document.body.scrollHeight")

            # Stop scrolling if the scrollHeight has not increased compared with the previous iteration
            if current_height > max_height:
                max_height = current_height
            else:
                break

        # Record the ending time, then calculate and print the total time
        end = datetime.datetime.now()
        delta = end - start
        print("Took {} to fully load the page".format(delta))

    def login(self):
        self.open(self.urls['login'])
        time.sleep(20)
        self.open(self.urls['editor'])

    def paste(self, selector):
        try:
            element = self.browser.find_element(by=selector[0],
                                                value=selector[1])
            element.send_keys(Keys.CONTROL, 'v')
            print('Text pasted')
        except Exception as e:
            print(e)

    def enter(self, selector):
        try:
            element = self.browser.find_element(by=selector[0],
                                                value=selector[1])
            element.send_keys(Keys.ENTER)
            print('ENTER pressed')
        except Exception as e:
            print(e)

    def press_enter_in_article(self):
        self.enter(self.selectors['article'])

    def add_empty_line_in_article(self):
        self.press_enter_in_article()
        self.press_enter_in_article()

    def set_text(self, text_type, text):
        clipboard.copy(text)
        self.paste(self.selectors[text_type])

    # def type(self, xpath, text):
    #     input_box = self.browser.find_element_by_xpath(xpath)
    #     input_box.send_keys(text)


class WeiboPublisher(Publisher):
    def __init__(self):
        urls = {
            'login': 'https://weibo.com/819961230/home',
            'editor': 'https://card.weibo.com/article/v3/editor#/draft/1398872'
        }
        selectors = {
            'title': [By.TAG_NAME, 'textarea'],
            'abstract': [By.TAG_NAME, 'input'],
            'article': [By.CLASS_NAME, 'WB_editor_iframe_new'],
            'bold': [By.CLASS_NAME, 'ficon-bold']
        }
        super(WeiboPublisher, self).__init__(urls, selectors)


def main():
    publisher = WeiboPublisher()
    publisher.init_browser()
    publisher.login()

    publisher.load()
    # a = publisher.browser.find_element_by_tag_name('textarea')
    # a.send_keys(Keys.CONTROL, 'v').perform()
    new_article_button = publisher.browser.find_element_by_class_name(
        'ficon_e_edit')
    if new_article_button:
        new_article_button.click()
    time.sleep(5)
    publisher.set_text('title', '昨晚，美股迎来了近月来最惨烈的挫败！')
    publisher.set_text('abstract', '昨晚，美股迎来了近月来最惨烈的挫败！')
    publisher.set_text('article', '昨晚，美股迎来了近月来最惨烈的挫败！')
    publisher.add_empty_line_in_article()
    publisher.set_text('article', '昨晚，美股迎来了近月来最惨烈的挫败！')
    time.sleep(10000)


if __name__ == '__main__':
    main()