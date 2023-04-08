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

def crowling_SPT_OA(db):
    #data frame
    data=pd.DataFrame(data=[],columns=['id','이름','주최','주관','후원','접수기간','참가대상','응모분야','특전','문의(전화)','이메일','홈페이지','출처','상세정보','비고','url'])

    #url
    page=1
    url='http://spectory.net/activities?page=%d&searchDate=latest'%(page)

    #open
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    driver.get(url)
    driver.set_window_size(900,900) #반응형 웹 방지
    time.sleep(2)

    #waiter
    wait=WebDriverWait(driver, 10)

    row=1
    repeat=0
    #data search
    while True:
        form=[]
        xpath='//*[@id="contentWrap"]/div[2]/section/table/tbody/tr[%d]/td[1]/a'%(row)
        try:
            element=wait.until(EC.presence_of_element_located((By.XPATH,xpath)))
        except:
            print("finish")
            break
        time.sleep(2)
        driver.execute_script("arguments[0].click()",element)
        time.sleep(2)
        name=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/h2'))).text #이름
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[1]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[2]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[3]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[5]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[6]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[7]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[8]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[9]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[11]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[12]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[2]'))).text)
        address=driver.current_url
        parse=(((urlparse(address)).query).split('&')[0]).split('=')[1] #게시물번호
        id='SPT'+parse
        #print(form)
        info={'id': [id],'이름': [name],'주최': [form[0]],'주관': [form[1]],'후원': [form[2]],'접수기간': [form[3]],'참가대상': [form[4]],'응모분야': [form[5]],'특전': [form[6]],'문의(전화)':[form[7]],'이메일': form[8],'홈페이지': [form[9]],'출처': ['스펙토리'],'상세정보': [form[10]],'비고': ['대외활동'],'url': [address]}
        #print(info)
        data=pd.concat([data,pd.DataFrame(info)],axis=0,ignore_index=True)
        driver.back()
        row+=1
        
        if row>10:
            page+=1
            row=1
            url='http://spectory.net/activities?page=%d&searchDate=latest'%(page)
            driver.get(url)
            time.sleep(3)
        
        repeat+=1
        print(repeat,name,'SPT_OA')

    #url
    page=1
    url='http://spectory.net/activities?page=%d&searchDate=deadline'%(page)
    driver.get(url)
    time.sleep(3)
    row=1
    while True:
        form=[]
        xpath='//*[@id="contentWrap"]/div[2]/section/table/tbody/tr[%d]/td[1]/a'%(row)
        try:
            element=wait.until(EC.presence_of_element_located((By.XPATH,xpath)))
        except:
            print("finish")
            break
        time.sleep(2)
        driver.execute_script("arguments[0].click()",element)
        time.sleep(2)
        name=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/h2'))).text #이름
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[1]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[2]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[3]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[5]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[6]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[7]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[8]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[9]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[11]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[12]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[2]'))).text)
        address=driver.current_url
        parse=(((urlparse(address)).query).split('&')[0]).split('=')[1] #게시물번호
        id='SPT'+parse
        #print(form)
        info={'id': [id],'이름': [name],'주최': [form[0]],'주관': [form[1]],'후원': [form[2]],'접수기간': [form[3]],'참가대상': [form[4]],'응모분야': [form[5]],'특전': [form[6]],'문의(전화)':[form[7]],'이메일': form[8],'홈페이지': [form[9]],'출처': ['스펙토리'],'상세정보': [form[10]],'비고': ['대외활동'],'url': [address]}
        #print(info)
        data=pd.concat([data,pd.DataFrame(info)],axis=0,ignore_index=True)
        driver.back()
        row+=1

        if row>10:
            page+=1
            row=1
            url='http://spectory.net/activities?page=%d&searchDate=deadline'%(page)
            driver.get(url)
            time.sleep(3)
        
        repeat+=1
        print(repeat,name,'SPT_OA')
        

    print(data)
    # 손질
    data=data.drop_duplicates(['이름'],keep='first') #중복값 제거
    data=data.fillna('') #결측값 대체
    #data.to_csv('대외활동(스펙토리).csv', encoding='utf-8-sig')
    data.to_sql(name='oa_SPT',con=db.db_connection,if_exists='replace',index=False) #db에 저장

    driver.quit()
    print("exit")

def crowling_SPT_CM(db):
    #data frame
    data=pd.DataFrame(data=[],columns=['id','이름','주최','주관','후원','접수기간','참가대상','응모분야','시상규모','1등시상금','특전','문의(전화)','이메일','홈페이지','출처','상세정보','비고','url'])

    #url
    page=1
    url='http://spectory.net/contest?page=%d&searchDate=prev'%(page)

    #open
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    driver.get(url)
    driver.set_window_size(900,900) #반응형 웹 방지
    time.sleep(2)

    #waiter
    wait=WebDriverWait(driver, 10)
    row=1
    repeat=0
    #data search
    #접수예정
    while True:
        form=[]
        xpath='//*[@id="contentWrap"]/div[2]/section/table/tbody/tr[%d]/td[1]/a'%(row)
        try:
            element=wait.until(EC.presence_of_element_located((By.XPATH,xpath)))
        except:
            print("finish")
            break
        time.sleep(2)
        driver.execute_script("arguments[0].click()",element)
        time.sleep(2)
        name=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/h2'))).text #이름
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[1]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[2]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[3]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[5]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[6]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[7]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[8]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[9]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[10]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[11]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[13]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[14]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[2]'))).text)
        address=driver.current_url
        parse=(((urlparse(address)).query).split('&')[0]).split('=')[1] #게시물번호
        id='SPT'+parse
        #print(form)
        info={'id': [id],'이름': [name],'주최': [form[0]],'주관': [form[1]],'후원': [form[2]],'접수기간': [form[3]],'참가대상': [form[4]],'응모분야': [form[5]],'시상규모': [form[6]],'1등시상금': [form[7]],'특전': [form[8]],'문의(전화)': [form[9]],'이메일': [form[10]],'홈페이지': [form[11]],'출처': ['스펙토리'],'상세정보': [form[12]],'비고': ['공모전'],'url': [address]}
        #print(info)
        data=pd.concat([data,pd.DataFrame(info)],axis=0,ignore_index=True)
        driver.back()
        row+=1
        
        if row>10:
            page+=1
            row=1
            url='http://spectory.net/contest?page=%d&searchDate=prev'%(page)
            driver.get(url)
            time.sleep(3)
        
        repeat+=1
        print(repeat,name,'SPT_CM')

    #접수중
    #url
    page=1
    url='http://spectory.net/contest?page=%d&searchDate=latest'%(page)
    driver.get(url)
    time.sleep(3)
    row=1
    while True:
        form=[]
        xpath='//*[@id="contentWrap"]/div[2]/section/table/tbody/tr[%d]/td[1]/a'%(row)
        try:
            element=wait.until(EC.presence_of_element_located((By.XPATH,xpath)))
        except:
            print("finish")
            break
        time.sleep(2)
        driver.execute_script("arguments[0].click()",element)
        time.sleep(2)
        name=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/h2'))).text #이름
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[1]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[2]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[3]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[5]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[6]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[7]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[8]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[9]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[10]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[11]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[13]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[14]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[2]'))).text)
        address=driver.current_url
        parse=(((urlparse(address)).query).split('&')[0]).split('=')[1] #게시물번호
        id='SPT'+parse
        #print(form)
        info={'id': [id],'이름': [name],'주최': [form[0]],'주관': [form[1]],'후원': [form[2]],'접수기간': [form[3]],'참가대상': [form[4]],'응모분야': [form[5]],'시상규모': [form[6]],'1등시상금': [form[7]],'특전': [form[8]],'문의(전화)': [form[9]],'이메일': [form[10]],'홈페이지': [form[11]],'출처': ['스펙토리'],'상세정보': [form[12]],'비고': ['공모전'],'url': [address]}
        #print(info)
        data=pd.concat([data,pd.DataFrame(info)],axis=0,ignore_index=True)
        driver.back()
        row+=1

        if row>10:
            page+=1
            row=1
            url='http://spectory.net/contest?page=%d&searchDate=latest'%(page)
            driver.get(url)
            time.sleep(3)
        
        repeat+=1
        print(repeat,name,'SPT_CM')
        
    #마감임박
    #url
    page=1
    url='http://spectory.net/contest?page=%d&searchDate=deadline'%(page)
    driver.get(url)
    time.sleep(3)
    row=1
    while True:
        form=[]
        xpath='//*[@id="contentWrap"]/div[2]/section/table/tbody/tr[%d]/td[1]/a'%(row)
        try:
            element=wait.until(EC.presence_of_element_located((By.XPATH,xpath)))
        except:
            print("finish")
            break
        time.sleep(2)
        driver.execute_script("arguments[0].click()",element)
        time.sleep(2)
        name=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/h2'))).text #이름
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[1]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[2]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[3]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[5]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[6]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[7]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[8]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[9]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[10]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[11]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[13]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[1]/div[2]/table/tbody/tr[14]/td'))).text)
        form.append(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="divPrint"]/div[2]'))).text)
        address=driver.current_url
        parse=(((urlparse(address)).query).split('&')[0]).split('=')[1] #게시물번호
        id='SPT'+parse
        #print(form)
        info={'id': [id],'이름': [name],'주최': [form[0]],'주관': [form[1]],'후원': [form[2]],'접수기간': [form[3]],'참가대상': [form[4]],'응모분야': [form[5]],'시상규모': [form[6]],'1등시상금': [form[7]],'특전': [form[8]],'문의(전화)': [form[9]],'이메일': [form[10]],'홈페이지': [form[11]],'출처': ['스펙토리'],'상세정보': [form[12]],'비고': ['공모전'],'url': [address]}
        #print(info)
        data=pd.concat([data,pd.DataFrame(info)],axis=0,ignore_index=True)
        driver.back()
        row+=1

        if row>10:
            page+=1
            row=1
            url='http://spectory.net/contest?page=%d&searchDate=deadline'%(page)
            driver.get(url)
            time.sleep(3)
        
        repeat+=1
        print(repeat,name,'SPT_CM')

    print(data)
    # 손질
    data=data.drop_duplicates(['이름'],keep='first') #중복값 제거
    data=data.fillna('') #결측값 대체
    #data.to_csv('공모전(스펙토리).csv', encoding='utf-8-sig')
    data.to_sql(name='cm_SPT',con=db.db_connection,if_exists='replace',index=False) #db에 저장

    driver.quit()
    print("exit")