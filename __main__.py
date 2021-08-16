from gevent import monkey as curious_george
curious_george.patch_all(thread=False, select=False)

from selenium import webdriver

# from crawlers.DaumNewsCrawler import DaumCrawler
# from crawlers.NaverNewsCrawler import NaverCrawler
from crawlers.DaumNewsMultiCrawler import crawlLinks as daumCrawlLinks, crawlNews as daumCrawlNews
from crawlers.NaverNewsMultiCrawler import crawlLinks as naverCrawlLinks, crawlNews as naverCrawlNews

from utils.util import *

from tqdm import trange

import sys
sys.setrecursionlimit(5000)

if __name__ == "__main__":
    # ------------------------------
    keyword = "모병제"
    start_date = "20180601"
    end_date = "20210601"
    # ------------------------------


    # --- chrome driver setting ---
    driver_url = './chromedriver.exe'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--privileged')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # ------------------------------


    keyword = keyword.replace(' ', '+')

    # daumCrawlLinks(keyword, start_date, end_date, driver_url, chrome_options)
    # naverCrawlLinks(keyword, start_date, end_date, driver_url, chrome_options)

    # daumCrawlNews(keyword, start_date, end_date, driver_url, chrome_options)
    # naverCrawlNews(keyword, start_date, end_date, driver_url, chrome_options)

    merge_crawl_data_json(keyword, start_date, end_date)