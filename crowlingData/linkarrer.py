import pandas as pd
import numpy as np
import time
from sqlalchemy import create_engine
from urllib.parse import urlparse, parse_qs

import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
# 알림창 끄기
options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 1
})
options.add_argument("headless") #창 숨기기

def crowling_LK_CM(db):
    #data frame
    data=pd.DataFrame(data=[],columns=['id','이름','주최','기업형태','참여대상','시상규모','접수기간','홈페이지','활동혜택','공모분야','출처','상세정보','비고','url'])

    #url
    page=1
    url='https://linkareer.com/list/contest?filterType=CATEGORY&orderBy_direction=DESC&orderBy_field=CREATED_AT&page=%d'%(page)

    #open
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    driver.get(url)
    driver.set_window_size(900,900) #반응형 웹 방지
    time.sleep(2)

    #waiter
    wait=WebDriverWait(driver, 10)

    # element=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div[1]/div[4]/div[2]/div/div[1]/p')))
    # resultString=element.text
    # num=int(re.sub(r'[^0-9]','',resultString))
    reqeat=0
    col=1
    row=1

    #data search
    while True:
        xpath='//*[@id="__next"]/div[1]/div[4]/div[2]/div/div[2]/div/div[%d]/div[%d]/div/div[2]/a/h5'%(row,col)
        try:
            element=driver.find_element(By.XPATH,xpath)
        except:
            print("finish")
            break
        time.sleep(2)
        driver.execute_script("arguments[0].click()",element)
        time.sleep(2)
        name=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div[1]/div[3]/div/div[1]/div[1]/div[1]/div/div[1]/div[2]/div[2]'))).text
        information=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div[1]/div[3]/div/div[1]/div[1]/div[1]/div/div[2]'))).text
        tmi=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div[1]/div[3]/div/div[1]/div[1]/div[3]/div[1]/div[1]/div[2]'))).text
        address=driver.current_url
        form=information.split('\n')
        parse=(urlparse(address).path).split('/')[2] #게시물번호
        id='LK'+parse
        #print(form)
        info={'id': [id],'이름': [name],'주최': [form[0]],'기업형태': [form[2]],'참여대상': [form[4]],'시상규모': [form[6]],'접수기간': [form[8]],'홈페이지': [form[10]],'활동혜택': [form[12]],'공모분야': [form[14]],'상세정보': [tmi],'출처': ['링커리어'],'비고': ['공모전'],'url': [address]}
        #print(info)
        data=pd.concat([data,pd.DataFrame(info)],axis=0,ignore_index=True)
        
        driver.back()
        col+=1
        if col>2:
            col=1
            row+=1

        if row>10:
            page+=1
            col=1
            row=1
            url='https://linkareer.com/list/contest?filterType=CATEGORY&orderBy_direction=DESC&orderBy_field=CREATED_AT&page=%d'%(page)
            driver.get(url)
            time.sleep(3)
        
        reqeat+=1
        print(reqeat,name,'LK_CM')

    print(data)
    # 손질
    data=data.drop_duplicates(['이름'],keep='first') #중복값 제거
    data=data.fillna('') #결측값 대체
    #data.to_csv('공모전(링커리어).csv', encoding='utf-8-sig')
    data.to_sql(name='cm_LK',con=db.db_connection,if_exists='replace',index=False) #db에 저장

    driver.quit()
    print("exit")

def crowling_LK_OA(db):
    #data frame
    data=pd.DataFrame(data=[],columns=['id','이름','주최','기업형태','참여대상','접수기간','활동기간','모집인원','활동지역','우대역량','홈페이지','활동혜택','관심분야','활동분야','출처','상세정보','비고','url'])

    #url
    page=1
    url='https://linkareer.com/list/activity?filterType=CATEGORY&orderBy_direction=DESC&orderBy_field=CREATED_AT&page=%d'%(page)

    #open
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    driver.get(url)
    driver.set_window_size(900,900) #반응형 웹 방지
    time.sleep(2)

    #waiter
    wait=WebDriverWait(driver, 10)

    # element=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div[1]/div[4]/div[2]/div/div[1]/p')))
    # resultString=element.text
    # num=int(re.sub(r'[^0-9]','',resultString))
    # print(num)
    repeat=0
    col=1
    row=1
    #data search
    while True:
        xpath='//*[@id="__next"]/div[1]/div[4]/div[2]/div/div[2]/div/div[%d]/div[%d]/div/div[2]/a/h5'%(row,col)
        try:
            element=driver.find_element(By.XPATH,xpath)
        except:
            print("finish")
            break
        time.sleep(2)
        driver.execute_script("arguments[0].click()",element)
        time.sleep(2)
        name=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div[1]/div[3]/div/div[1]/div[1]/div[1]/div/div[1]/div[2]/div[2]'))).text
        information=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div[1]/div[3]/div/div[1]/div[1]/div[1]/div/div[2]'))).text
        tmi=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div[1]/div[3]/div/div[1]/div[1]/div[3]/div[1]'))).text
        address=driver.current_url
        form=information.split('\n')
        parse=(urlparse(address).path).split('/')[2] #게시물번호
        id='LK'+parse
        #print(form)
        info={'id': [id],'이름': [name],'주최': [form[0]],'기업형태': [form[2]],'참여대상': [form[4]],'접수기간': [form[6]],'활동기간': [form[8]],'모집인원': [form[10]],'활동지역': [form[12]],'우대역량': [form[14]],'홈페이지': [form[16]],'관심분야': form[18],'활동분야': form[20],'출처': ['링커리어'],'상세정보': [tmi],'비고': ['대외활동'],'url': [address]}
        #print(info)
        data=pd.concat([data,pd.DataFrame(info)],axis=0,ignore_index=True)
        
        driver.back()
        col+=1
        if col>2:
            col=1
            row+=1

        if row>10:
            page+=1
            col=1
            row=1
            url='https://linkareer.com/list/activity?filterType=CATEGORY&orderBy_direction=DESC&orderBy_field=CREATED_AT&page=%d'%(page)
            driver.get(url)
            time.sleep(3)
        
        repeat+=1
        print(repeat,name,'LK_OA')
        

    print(data)
    # 손질
    data=data.drop_duplicates(['이름'],keep='first') #중복값 제거
    data=data.fillna('') #결측값 대체
    #data.to_csv('대외활동(링커리어).csv', encoding='utf-8-sig')
    data.to_sql(name='oa_LK',con=db.db_connection,if_exists='replace',index=False) #db에 저장

    driver.quit()
    print("exit")

def crowling_LK_EM(db):
    #data frame
    data=pd.DataFrame(data=[],columns=['id','이름','기업명','기업형태','접수기간','모집직무','채용인원','채용형태','홈페이지','근무지역','출처','상세정보','비고','url'])

    #url
    page=1
    url='https://linkareer.com/list/recruit?orderBy_direction=DESC&orderBy_field=RECENT&page=%d'%(page)

    #open
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    driver.get(url)
    driver.set_window_size(900,900) #반응형 웹 방지
    time.sleep(2)

    #waiter
    wait=WebDriverWait(driver, 10)

    # element=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div[1]/div[4]/div[2]/div[1]/p')))
    # resultString=element.text
    # num=int(re.sub(r'[^0-9]','',resultString))
    # print(num)
    row=1
    repeat=0
    #data search
    while True:
        xpath='//*[@id="__next"]/div[1]/div[4]/div[2]/div[4]/div[%d]/div[1]/div[2]/div[1]/div[2]/a/p'%(row)
        try:
            element=driver.find_element(By.XPATH,xpath)
        except:
            print("finish")
            break
        time.sleep(2)
        driver.execute_script("arguments[0].click()",element)
        time.sleep(2)
        name=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div[1]/div[3]/div/div[1]/div[1]/div[1]/div/div[1]/div[2]/div[2]'))).text
        information=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div[1]/div[3]/div/div[1]/div[1]/div[1]/div/div[2]'))).text
        tmi=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div[1]/div[3]/div/div[1]/div[1]/div[3]/div[1]'))).text
        address=driver.current_url
        form=information.split('\n')
        parse=(urlparse(address).path).split('/')[2] #게시물번호
        id='LK'+parse
        #print(form)
        info={'id': [id],'이름': [name],'기업명': [form[0]],'기업형태': [form[2]],'접수기간': [form[4]],'모집직무': [form[6]],'채용인원': [form[8]],'채용형태': [form[10]],'홈페이지': [form[12]],'근무지역': [form[14]],'출처': ['링커리어'],'상세정보': [tmi],'비고': ['채용정보'],'url': [address]}
        #print(info)
        data=pd.concat([data,pd.DataFrame(info)],axis=0,ignore_index=True)
        
        driver.back()
        row+=1

        if row>20:
            page+=1
            row=1
            url='https://linkareer.com/list/recruit?orderBy_direction=DESC&orderBy_field=RECENT&page=%d'%(page)
            driver.get(url)
            time.sleep(3)
        
        repeat+=1
        print(repeat,name,'LK_EM')
        

    print(data)
    # 손질
    data=data.drop_duplicates(['이름'],keep='first') #중복값 제거
    data=data.fillna('') #결측값 대체
    #data.to_csv('채용(링커리어).csv', encoding='utf-8-sig')
    data.to_sql(name='em_LK',con=db.db_connection,if_exists='replace',index=False) #db에 저장

    driver.quit()
    print("exit")

def crowling_LK_IN(db):
    #data frame
    data=pd.DataFrame(data=[],columns=['id','이름','기업명','기업형태','접수기간','모집직무','채용인원','채용형태','홈페이지','근무지역','출처','상세정보','비고','url'])

    #url
    page=1
    url='https://linkareer.com/list/intern?orderBy_direction=DESC&orderBy_field=RECENT&page=%d'%(page)

    #open
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    driver.get(url)
    driver.set_window_size(900,900) #반응형 웹 방지
    time.sleep(2)

    #waiter
    wait=WebDriverWait(driver, 10)

    # element=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div[1]/div[4]/div[2]/div[1]/p')))
    # resultString=element.text
    # num=int(re.sub(r'[^0-9]','',resultString))
    # print(num)
    row=1
    repeat=0
    #data search
    while True:
        xpath='//*[@id="__next"]/div[1]/div[4]/div[2]/div[4]/div[%d]/div[1]/div[2]/div[1]/div[2]/a/p'%(row)
        try:
            element=driver.find_element(By.XPATH,xpath)
        except:
            print("finish")
            break
        time.sleep(2)
        driver.execute_script("arguments[0].click()",element)
        time.sleep(2)
        name=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div[1]/div[3]/div/div[1]/div[1]/div[1]/div/div[1]/div[2]/div[2]'))).text
        information=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div[1]/div[3]/div/div[1]/div[1]/div[1]/div/div[2]'))).text
        tmi=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div[1]/div[3]/div/div[1]/div[1]/div[3]/div[1]'))).text
        address=driver.current_url
        form=information.split('\n')
        parse=(urlparse(address).path).split('/')[2] #게시물번호
        id='LK'+parse
        #print(form)
        info={'id': [id],'이름': [name],'기업명': [form[0]],'기업형태': [form[2]],'접수기간': [form[4]],'모집직무': [form[6]],'채용인원': [form[8]],'채용형태': [form[10]],'홈페이지': [form[12]],'근무지역': [form[14]],'출처': ['링커리어'],'상세정보': [tmi],'비고': ['인턴정보'],'url': [address]}
        #print(info)
        data=pd.concat([data,pd.DataFrame(info)],axis=0,ignore_index=True)
        
        driver.back()
        row+=1

        if row>20:
            page+=1
            row=1
            url='https://linkareer.com/list/intern?orderBy_direction=DESC&orderBy_field=RECENT&page=%d'%(page)
            driver.get(url)
            time.sleep(3)
        
        repeat+=1
        print(repeat,name,'LK_IN')
        

    print(data)
    # 손질
    data=data.drop_duplicates(['이름'],keep='first') #중복값 제거
    data=data.fillna('') #결측값 대체
    #data.to_csv('인턴(링커리어).csv', encoding='utf-8-sig')
    data.to_sql(name='in_LK',con=db.db_connection,if_exists='replace',index=False) #db에 저장

    driver.quit()
    print("exit")