import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

import requests
from bs4 import BeautifulSoup

URL = 'https://recruit.navercorp.com/naver/job/list/developer?searchSysComCd=&entTypeCd=&searchTxt='

options = webdriver.ChromeOptions()
options.add_argument('window-size=1920,1080')

driver = webdriver.Chrome('devstack-notice-crawling/chromedriver')
driver.implicitly_wait(5)
driver.get(url=URL)

noticeList, new_noticeList = [], []

response = requests.get(driver.current_url)


## 채용공고 리스트 데이터를 긁어오는데 실패
if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    notice_list = soup.select('.card_list')
    
    print(notice_list)
    # for notice in notice_list[3].children:
    #     print(notice)
else : 
    print(response.status_code)
    

driver.execute_script("loadJobList();")

print('----------noticeList--------------')
print(noticeList)

driver.close()