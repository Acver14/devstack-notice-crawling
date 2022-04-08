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
import datetime
from connectDB import DevStackDB

db = DevStackDB()
skill_list = db.runQuery('SELECT * FROM Skill')[0]

URL = 'https://recruit.navercorp.com/naver/job/list/developer?searchSysComCd=&entTypeCd=&searchTxt='

options = webdriver.ChromeOptions()
options.add_argument('window-size=1920,1080')

driver = webdriver.Chrome('devstack-notice-crawling/chromedriver')
driver.implicitly_wait(10)
driver.get(url=URL)

companyNo = db.runQuery('SELECT companyNo FROM Company WHERE companyName=\'Naver\'')[0][0]['companyNo']

noticeList, new_noticeList = [], []

last_height = driver.execute_script("return document.documentElement.scrollHeight")
time.sleep(3)
print(last_height)
while True:
    # driver.execute_script("loadJobList")
    try:
        driver.find_element_by_id('moreDiv').click()
    except selenium.common.exceptions.ElementNotInteractableException:
        break
    time.sleep(3)
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    print(new_height)
    
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

notice_list = soup.find("div", class_="card_list").find_all('li')

notice_url_list = []
for notice in notice_list:
    date = notice.find('em', class_="crd_date").text
    if '마감' in date:
        continue
    if '~' in date:
        endDate = date.split('~')[1]
    else:
        endDate = date
    
    notice_url_list.append({
        'link' : 'https://recruit.navercorp.com' + notice.find('a')["href"],
        'title': notice.find('strong', class_="crd_tit").text,
        'endDate': endDate,
        'skill' : []
        })

for notice in notice_url_list:
    html = urlopen(notice['link'])
    soup = BeautifulSoup(html, 'html.parser')
    context = soup.select_one('#content > div > div.career_detail > div.dtl_context > div.context_area').text
    for skill in skill_list:
        if skill['skillName'].casefold() in context.casefold():
            notice['skill'].append(skill)

for notice in notice_url_list:
    if notice['skill']:
        notice['endDate'] = datetime.datetime.strptime(notice['endDate'], '%Y.%m.%d').isoformat()
        print(notice['title'], notice['endDate'], notice['link'])
        print(notice['skill'])
        print()
        data = (notice['title'], notice['link'], notice['endDate'], companyNo)
        query = 'INSERT INTO Notice (noticeTitle, noticeUrl, noticeEndDate, companyNo) VALUES(\'%s\', \'%s\', \'%s\', %d)' % data
        print(query)
        noticeNo = db.runQuery(query)[1]
        print(noticeNo)
        for skill in notice['skill']:
            data = (noticeNo, skill['skillNo'])
            query = 'INSERT INTO NoticeSkillStack (noticeNo, skillNo) VALUES(%d, %d)' % data
            db.runQuery(query)
db.connection.commit()
            

driver.close()
db.close()