import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

import time

stack_list = ['kubernetes', 'python', 'c++', 'shell']

URL = 'https://recruit.navercorp.com/naver/job/list/developer?searchSysComCd=&entTypeCd=&searchTxt='

options = webdriver.ChromeOptions()
options.add_argument('window-size=1920,1080')

driver = webdriver.Chrome('devstack-notice-crawling/chromedriver')
driver.implicitly_wait(10)
driver.get(url=URL)

noticeList, new_noticeList = [], []

# last_height = driver.execute_script("document.body.scrollHeight")
# time.sleep(5)
# print(last_height)
# while True:
#     driver.execute_script("loadJobList();")
#     new_height = driver.execute_script("document.body.scrollHeight")
#     time.sleep(5)
#     if new_height == last_height:
#         break
#     last_height = new_height
#     print(new_height)
    
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

notice_url_list = []

# notice_list = soup.select('#jobListDiv > ul > li')
notice_list = soup.find("div", class_="card_list").find_all('li')
for notice in notice_list:
    # print('https://recruit.navercorp.com' + notice.find('a')["href"])
    notice_url_list.append({
        'link' : 'https://recruit.navercorp.com' + notice.find('a')["href"],
        'title': notice.find('strong', class_="crd_tit").text,
        'date' : notice.find('em', class_="crd_date").text,
        'skill' : ''
        })
    
for notice in notice_url_list:
    html = urlopen(notice['link'])
    soup = BeautifulSoup(html, 'html.parser')
    context = soup.select_one('#content > div > div.career_detail > div.dtl_context > div.context_area').text
    for skill in stack_list:
        if skill.casefold() in context.casefold():
            notice['skill'] += ' ' + skill

for notice in notice_url_list:
    print(notice['title'], notice['date'], notice['link'])
    print(notice['skill'])
    print()

driver.close()