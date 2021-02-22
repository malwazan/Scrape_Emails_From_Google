# import required modules
import scrapy
from scrapy.spiders import CrawlSpider, Request
from googlesearch import search
import re
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class EmailExtractor(CrawlSpider):
    name = 'email_extractor'
    # enable user agents rotations
    rotate_user_agent = True

    def __init__(self, *args, **kwargs):
        super(EmailExtractor, self).__init__(*args, **kwargs)
        self.email_list = []
        self.query = " 'market places business'.gmail.com "

    
    # sending requests
    def start_requests(self):
        for results in search(self.query, num=10, stop=None, pause=2):
            try:
                yield SeleniumRequest(
                    url=results,
                    callback=self.parse,
                    wait_until=EC.presence_of_element_located(
                        (By.TAG_NAME, "html")),
                    dont_filter=True
                )
            except:
                pass
    
    # extracting emails
    def parse(self, response):
        try:
            EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
            emails = re.finditer(EMAIL_REGEX, str(response.text))
            for email in emails:
                self.email_list.append(email.group())
        
            for email in set(self.email_list):
                yield{
                    "emails": email
                }
        
            self.email_list.clear()
        except:
            pass
