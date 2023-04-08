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

def crowling_AFY_CM(db):
    #data frame
    data=pd.DataFrame(data=[],columns=['id','이름','주최','주관','지원기간','공모분야','자격요건','시상내역','지원','출처','상세정보','비고','url'])

    #url
    url='https://allforyoung.com/posts/contest'

    #open
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    driver.get(url)
    driver.set_window_size(900,900) #반응형 웹 방지
    time.sleep(2)
    
    #waiter
    wait=WebDriverWait(driver, 10)
    
    lastPage=driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/section[3]/div[2]/div/ul/li[7]').text
    item=1
    repeat=0
    page=1
    #data search
    while True:
        form=[]
        xpath='//*[@id="__next"]/div/div/section[3]/div[1]/div[%d]/div[2]/p[2]'%(item)
        try:
            element=driver.find_element(By.XPATH,xpath)
        except:
            print("finish")
            break
        time.sleep(2)
        driver.execute_script("arguments[0].click()",element)
        time.sleep(2)

        driver.switch_to.window(window_name=driver.window_handles[-1]) #탭이동
        name=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div/div/section[1]/div/div[1]/div[1]/h4'))).text
        tmpS=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div/div/section[1]/div/div[2]/div[2]/div[1]/div[1]/span[2]'))).text
        tmp=tmpS.split('/')
        form.append(tmp[0])
        if len(tmp)>1:
            form.append(tmp[1])
        else:
            form.append(tmp[0])
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div/div/section[1]/div/div[2]/div[2]/div[1]/div[2]/span[2]'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div/div/section[1]/div/div[2]/div[2]/div[1]/div[3]/span[2]'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div/div/section[1]/div/div[2]/div[2]/div[1]/div[4]/span[2]'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div/div/section[1]/div/div[2]/div[2]/div[1]/div[5]/span[2]'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div/div/section[2]/section/div[2]'))).text)
        address=driver.current_url
        case=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div/div/section[1]/div/div[2]/div[2]/div[2]/button[1]'))).text
        element=driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/section[1]/div/div[2]/div[2]/div[2]/button[1]')
        time.sleep(2)
        driver.execute_script("arguments[0].click()",element)
        time.sleep(2)
        if case=='지원하기':
            driver.switch_to.window(window_name=driver.window_handles[-1]) #탭이동
            form.append(driver.current_url)
            # #탭을 닫고 이전 탭으로 이동
            # driver.close()
            # driver.switch_to.window(driver.window_handles[-1])
        else:
            form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="modal-root"]/div/div/div/div[2]/p'))).text)

        parse=(urlparse(address).path).split('/')[2] #게시물번호
        id='AFY'+parse
        info={'id': [id],'이름': [name],'주최': [form[0]],'주관': [form[1]],'지원기간': [form[2]],'공모분야': [form[3]],'자격요건': [form[4]],'시상내역': [form[5]],'지원': [form[7]],'출처': ['요즘것들'],'상세정보': [form[6]],'비고': ['공모전'],'url': [address]}
        #print(info)
        data=pd.concat([data,pd.DataFrame(info)],axis=0,ignore_index=True)
        #print(form)

        
        #기본탭 제외 전부 닫기
        tap=driver.window_handles
        for i in range(len(tap)-1,0,-1):
            driver.switch_to.window(driver.window_handles[i])
            driver.close()    
        driver.switch_to.window(driver.window_handles[0])

        item+=1

        if item>24:
            item=1
            if page==lastPage:
                break
            element=driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/section[3]/div[2]/div/button[2]')
            time.sleep(2)
            driver.execute_script("arguments[0].click()",element)
            time.sleep(2)
            page=page+1
        
        repeat+=1
        print(repeat,name,'AFY_CM')
        

    print(data)
    # 손질
    data=data.drop_duplicates(['이름'],keep='first') #중복값 제거
    data=data.fillna('') #결측값 대체
    #data.to_csv('공모전(요즘것들).csv', encoding='utf-8-sig')
    data.to_sql(name='cm_AFY',con=db.db_connection,if_exists='replace',index=False) #db에 저장

    driver.quit()
    print("exit")

def crowling_AFY_OA(db):
    #data frame
    data=pd.DataFrame(data=[],columns=['id','이름','주최','주관','지원기간','활동분야','활동기간','모집인원','지원','출처','상세정보','비고','url'])

    #url
    url='https://allforyoung.com/posts/activity'

    #open
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    driver.get(url)
    driver.set_window_size(900,900) #반응형 웹 방지
    time.sleep(2)

    #waiter
    wait=WebDriverWait(driver, 10)

    lastPage=driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/section[3]/div[2]/div/ul/li[7]').text
    item=1
    repeat=0
    page=1
    #data search
    while True:
        form=[]
        xpath='//*[@id="__next"]/div/div/section[3]/div[1]/div[%d]/div[2]/p[2]'%(item)
        try:
            element=driver.find_element(By.XPATH,xpath)
        except:
            print("finish")
            break
        time.sleep(2)
        driver.execute_script("arguments[0].click()",element)
        time.sleep(2)

        driver.switch_to.window(window_name=driver.window_handles[-1]) #탭이동
        name=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div/div/section[1]/div/div[1]/div[1]/h4'))).text
        tmpS=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div/div/section[1]/div/div[2]/div[2]/div[1]/div[1]/span[2]'))).text
        tmp=tmpS.split('/')
        form.append(tmp[0])
        if len(tmp)>1:
            form.append(tmp[1])
        else:
            form.append(tmp[0])
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div/div/section[1]/div/div[2]/div[2]/div[1]/div[2]/span[2]'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div/div/section[1]/div/div[2]/div[2]/div[1]/div[3]/span[2]'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div/div/section[1]/div/div[2]/div[2]/div[1]/div[4]/span[2]'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div/div/section[1]/div/div[2]/div[2]/div[1]/div[5]/span[2]'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div/div/section[2]/section/div[2]/div/div/div/div'))).text)
        address=driver.current_url
        case=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div/div/section[1]/div/div[2]/div[2]/div[2]/button[1]'))).text
        element=driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/section[1]/div/div[2]/div[2]/div[2]/button[1]')
        time.sleep(2)
        driver.execute_script("arguments[0].click()",element)
        time.sleep(2)
        if case=='지원하기':
            driver.switch_to.window(window_name=driver.window_handles[-1]) #탭이동
            form.append(driver.current_url)
            # #탭을 닫고 이전 탭으로 이동
            # driver.close()
            # driver.switch_to.window(driver.window_handles[-1])
        else:
            form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="modal-root"]/div/div/div/div[2]/p'))).text)

        parse=(urlparse(address).path).split('/')[2] #게시물번호
        id='AFY'+parse
        info={'id': [id],'이름': [name],'주최': [form[0]],'주관': [form[1]],'지원기간': [form[2]],'활동분야': [form[3]],'활동기간': [form[4]],'모집인원': [form[5]],'지원': [form[7]],'출처': ['요즘것들'],'상세정보': [form[6]],'비고': ['대외활동'],'url': [address]}
        #print(info)
        data=pd.concat([data,pd.DataFrame(info)],axis=0,ignore_index=True)
        #print(form)

        
        #기본탭 제외 전부 닫기
        tap=driver.window_handles
        for i in range(len(tap)-1,0,-1):
            driver.switch_to.window(driver.window_handles[i])
            driver.close()    
        driver.switch_to.window(driver.window_handles[0])

        item+=1

        if item>24:
            item=1
            if page==lastPage:
                break
            element=driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/section[3]/div[2]/div/button[2]')
            time.sleep(2)
            driver.execute_script("arguments[0].click()",element)
            time.sleep(2)
            page=page+1
        
        repeat+=1
        print(repeat,name,'AFY_OA')
        

    print(data)
    # 손질
    data=data.drop_duplicates(['이름'],keep='first') #중복값 제거
    data=data.fillna('') #결측값 대체
    data.to_sql(name='oa_AFY',con=db.db_connection,if_exists='replace',index=False) #db에 저장

    driver.quit()
    print("exit")