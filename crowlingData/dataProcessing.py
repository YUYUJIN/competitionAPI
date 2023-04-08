import pandas as pd
from sqlalchemy import create_engine
import pymysql

def dataProcessing(db):
    #dataframe
    data=pd.DataFrame(data=[],columns=['id','title','manage','taget','men','period','local','field','inquiry','page','awarding','benefit','source','detail','note','url'])

    """
    1 이름/주최/기업형태/참여대상/시상규모/접수기간/홈페이지/활동혜택/공모분야/출처/상세정보/비고/url
    2 이름/주최/주관/후원/접수기간/참가대상/응모분야/시상규모/1등시상금/특전/문의(전화)/이메일/홈페이지/출처/상세정보/비고/url
    3 이름/주최/주관/지원기간/공모분야/자격요건/시상내역/지원/출처/상세정보/비고/url
    4 이름/주최/기업형태/참여대상/접수기간/활동기간/모집인원/활동지역/우대역량/홈페이지/활동혜택/관심분야/활동분야/출처/상세정보/비고/url
    5 이름/주최/주관/지원기간/활동분야/활동기간/모집인원/지원/출처/상세정보/비고/url
    6 이름/주최/주관/후원/접수기간/참가대상/응모분야/특전/문의(전화)/이메일/홈페이지/출처/상세정보/비고/url
    7 이름/기업명/기업형태/접수기간/모집직무/채용인원/채용형태/홈페이지/근무지역/출처/상세정보/비고/url
    8 이름/기업명/기업형태/접수기간/모집직무/채용인원/채용형태/홈페이지/근무지역/출처/상세정보/비고/url

    이름 12345678
    /주관(주최/주관/후원/기업명/기업형태) 12345678
    /대상(참여대상/참가대상/자격요건/우대역량/모집직무) 12345678
    /인원(모집인원/채용인원/채용형태) 4578
    /기간(접수기간/활동기간/지원기간) 12345678
    /지역(활동지역/근무지역) 478
    /분야(공모분야/응모분야/모집직무/관심분야/활동분야) 1234567
    /문의(전화/이메일) 26
    /페이지(지원,홈페이지) 1234568
    /시상(시상내역/시상규모/1등시상금) 123
    /혜택(활동혜택/특전) 1246
    /출처 12345678
    /상세정보 12345678
    /비고 12345678
    /url 12345678
    """

    #column index
    cmId=0

    #1 이름/주최/기업형태/참여대상/시상규모/접수기간/홈페이지/활동혜택/공모분야/출처/상세정보/비고/url
    tmp=pd.DataFrame(data=[],columns=['id','title','manage','taget','men','period','local','field','inquiry','page','awarding','benefit','source','detail','note','url'])
    #values=pd.read_csv(r'C:\Users\wlsyo\test\testdata\공모전(링커리어).csv',index_col=0)
    values=pd.read_sql_table('cm_LK',db.conn,index_col=0)
    values=values.drop_duplicates(['이름'],keep='first') #중복값 제거
    values=values.fillna('') #결측값 대체
    tmp['id']=values['id']
    tmp['title']=values['이름']
    tmp['manage']=values['주최']+'/'+values['기업형태']
    tmp['taget']=values['참여대상']
    tmp['men']='00명'
    tmp['period']=values['접수기간']
    tmp['local']='제한없음'
    tmp['field']=values['공모분야']
    tmp['inquiry']='None'
    tmp['page']=values['홈페이지']
    tmp['awarding']=values['시상규모']
    tmp['benefit']=values['활동혜택']
    tmp['source']=values['출처']
    tmp['detail']=values['상세정보']
    tmp['note']=values['비고']
    tmp['url']=values['url']
    data=pd.concat([data,tmp],axis=0,ignore_index=True)

    #2 이름/주최/주관/후원/접수기간/참가대상/응모분야/시상규모/1등시상금/특전/문의(전화)/이메일/홈페이지/출처/상세정보/비고/url
    tmp=pd.DataFrame(data=[],columns=['id','title','manage','taget','men','period','local','field','inquiry','page','awarding','benefit','source','detail','note','url'])
    #values=pd.read_csv(r'C:\Users\wlsyo\test\testdata\공모전(스펙토리).csv',index_col=0)
    values=pd.read_sql_table('cm_SPT',db.conn,index_col=0)
    values=values.drop_duplicates(['이름'],keep='first') #중복값 제거
    values=values.fillna('') #결측값 대체
    tmp['id']=values['id']
    tmp['title']=values['이름']
    tmp['manage']=values['주최']+'/'+values['주관']+'/'+values['후원']
    tmp['taget']=values['참가대상']
    tmp['men']='제한없음'
    tmp['period']=values['접수기간']
    tmp['local']='제한없음'
    tmp['field']=values['응모분야']
    tmp['inquiry']=values['문의(전화)']+'/'+values['이메일']
    tmp['page']=values['홈페이지']
    tmp['awarding']=values['시상규모']+'/'+values['1등시상금']
    tmp['benefit']=values['특전']
    tmp['source']=values['출처']
    tmp['detail']=values['상세정보']
    tmp['note']=values['비고']
    tmp['url']=values['url']
    data=pd.concat([data,tmp],axis=0,ignore_index=True)

    #3 이름/주최/주관/지원기간/공모분야/자격요건/시상내역/지원/출처/상세정보/비고/url
    tmp=pd.DataFrame(data=[],columns=['id','title','manage','taget','men','period','local','field','inquiry','page','awarding','benefit','source','detail','note','url'])
    #values=pd.read_csv(r'C:\Users\wlsyo\test\testdata\공모전(요즘것들).csv',index_col=0)
    values=pd.read_sql_table('cm_AFY',db.conn,index_col=0)
    values=values.drop_duplicates(['이름'],keep='first') #중복값 제거
    values=values.fillna('') #결측값 대체
    tmp['id']=values['id']
    tmp['title']=values['이름']
    tmp['manage']=values['주최']+'/'+values['주관']
    tmp['taget']=values['자격요건']
    tmp['men']='00명'
    tmp['period']=values['지원기간']
    tmp['local']='제한없음'
    tmp['field']=values['공모분야']
    tmp['inquiry']='None'
    tmp['page']=values['지원']
    tmp['awarding']=values['시상내역']
    tmp['benefit']='None'
    tmp['source']=values['출처']
    tmp['detail']=values['상세정보']
    tmp['note']=values['비고']
    tmp['url']=values['url']
    data=pd.concat([data,tmp],axis=0,ignore_index=True)

    #4 이름/주최/기업형태/참여대상/접수기간/활동기간/모집인원/활동지역/우대역량/홈페이지/활동혜택/관심분야/활동분야/출처/상세정보/비고/url
    tmp=pd.DataFrame(data=[],columns=['id','title','manage','taget','men','period','local','field','inquiry','page','awarding','benefit','source','detail','note','url'])
    #values=pd.read_csv(r'C:\Users\wlsyo\test\testdata\대외활동(링커리어).csv',index_col=0)
    values=pd.read_sql_table('oa_LK',db.conn,index_col=0)
    values=values.drop_duplicates(['이름'],keep='first') #중복값 제거
    values=values.fillna('') #결측값 대체
    tmp['id']=values['id']
    tmp['title']=values['이름']
    tmp['manage']=values['주최']+'/'+values['기업형태']
    tmp['taget']=values['참여대상']+values['우대역량']
    tmp['men']=values['모집인원']
    tmp['period']=values['접수기간']+'/'+values['활동기간']
    tmp['local']=values['활동지역']
    tmp['field']=values['관심분야']+'/'+values['활동분야']
    tmp['inquiry']='None'
    tmp['page']=values['홈페이지']
    tmp['awarding']='None'
    tmp['benefit']=values['활동혜택']
    tmp['source']=values['출처']
    tmp['detail']=values['상세정보']
    tmp['note']=values['비고']
    tmp['url']=values['url']
    data=pd.concat([data,tmp],axis=0,ignore_index=True)

    #5 이름/주최/주관/지원기간/활동분야/활동기간/모집인원/지원/출처/상세정보/비고/url
    tmp=pd.DataFrame(data=[],columns=['id','title','manage','taget','men','period','local','field','inquiry','page','awarding','benefit','source','detail','note','url'])
    #values=pd.read_csv(r'C:\Users\wlsyo\test\testdata\대외활동(요즘것들).csv',index_col=0)
    values=pd.read_sql_table('oa_AFY',db.conn,index_col=0)
    values=values.drop_duplicates(['이름'],keep='first') #중복값 제거
    values=values.fillna('') #결측값 대체
    tmp['id']=values['id']
    tmp['title']=values['이름']
    tmp['manage']=values['주최']+'/'+values['주관']
    tmp['taget']='제한없음'
    tmp['men']=values['모집인원']
    tmp['period']=values['지원기간']+'/'+values['활동기간']
    tmp['local']='제한없음'
    tmp['field']=values['활동분야']
    tmp['inquiry']='None'
    tmp['page']=values['지원']
    tmp['awarding']='None'
    tmp['benefit']='None'
    tmp['source']=values['출처']
    tmp['detail']=values['상세정보']
    tmp['note']=values['비고']
    tmp['url']=values['url']
    data=pd.concat([data,tmp],axis=0,ignore_index=True)

    #6 이름/주최/주관/후원/접수기간/참가대상/응모분야/특전/문의(전화)/이메일/홈페이지/출처/상세정보/비고/url
    tmp=pd.DataFrame(data=[],columns=['id','title','manage','taget','men','period','local','field','inquiry','page','awarding','benefit','source','detail','note','url'])
    #values=pd.read_csv(r'C:\Users\wlsyo\test\testdata\대외활동(스펙토리).csv',index_col=0)
    values=pd.read_sql_table('oa_SPT',db.conn,index_col=0)
    values=values.drop_duplicates(['이름'],keep='first') #중복값 제거
    values=values.fillna('') #결측값 대체
    tmp['id']=values['id']
    tmp['title']=values['이름']
    tmp['manage']=values['주최']+'/'+values['주관']+'/'+values['후원']
    tmp['taget']=values['참가대상']
    tmp['men']='00명'
    tmp['period']=values['접수기간']
    tmp['local']='제한없음'
    tmp['field']=values['응모분야']
    tmp['inquiry']=values['문의(전화)']+'/'+values['이메일']
    tmp['page']=values['홈페이지']
    tmp['awarding']='None'
    tmp['benefit']=values['특전']
    tmp['source']=values['출처']
    tmp['detail']=values['상세정보']
    tmp['note']=values['비고']
    tmp['url']=values['url']
    data=pd.concat([data,tmp],axis=0,ignore_index=True)

    #7 이름/기업명/기업형태/접수기간/모집직무/채용인원/채용형태/홈페이지/근무지역/출처/상세정보/비고/url
    tmp=pd.DataFrame(data=[],columns=['id','title','manage','taget','men','period','local','field','inquiry','page','awarding','benefit','source','detail','note','url'])
    #values=pd.read_csv(r'C:\Users\wlsyo\test\testdata\인턴(링커리어).csv',index_col=0)
    values=pd.read_sql_table('in_LK',db.conn,index_col=0)
    values=values.drop_duplicates(['이름'],keep='first') #중복값 제거
    values=values.fillna('') #결측값 대체
    tmp['id']=values['id']
    tmp['title']=values['이름']
    tmp['manage']=values['기업명']+'/'+values['기업형태']
    tmp['taget']=values['모집직무']
    tmp['men']=values['채용인원']+'/'+values['채용형태']
    tmp['period']=values['접수기간']
    tmp['local']=values['근무지역']
    tmp['field']=values['모집직무']
    tmp['inquiry']='None'
    tmp['page']=values['홈페이지']
    tmp['awarding']='None'
    tmp['benefit']='None'
    tmp['source']=values['출처']
    tmp['detail']=values['상세정보']
    tmp['note']=values['비고']
    tmp['url']=values['url']
    data=pd.concat([data,tmp],axis=0,ignore_index=True)

    #8 이름/기업명/기업형태/접수기간/모집직무/채용인원/채용형태/홈페이지/근무지역/출처/상세정보/비고/url
    tmp=pd.DataFrame(data=[],columns=['id','title','manage','taget','men','period','local','field','inquiry','page','awarding','benefit','source','detail','note','url'])
    #values=pd.read_csv(r'C:\Users\wlsyo\test\testdata\채용(링커리어).csv',index_col=0)
    values=pd.read_sql_table('em_LK',db.conn,index_col=0)
    values=values.drop_duplicates(['이름'],keep='first') #중복값 제거
    values=values.fillna('') #결측값 대체
    tmp['id']=values['id']
    tmp['title']=values['이름']
    tmp['manage']=values['기업명']+'/'+values['기업형태']
    tmp['taget']=values['모집직무']
    tmp['men']=values['채용인원']+'/'+values['채용형태']
    tmp['period']=values['접수기간']
    tmp['local']=values['근무지역']
    tmp['field']=values['모집직무']
    tmp['inquiry']='None'
    tmp['page']=values['홈페이지']
    tmp['awarding']='None'
    tmp['benefit']='None'
    tmp['source']=values['출처']
    tmp['detail']=values['상세정보']
    tmp['note']=values['비고']
    tmp['url']=values['url']
    data=pd.concat([data,tmp],axis=0,ignore_index=True)

    # 손질
    data=data.drop_duplicates(['title'],keep='first') #중복값 제거
    data=data.fillna('') #결측값 대체

    #data.to_csv('test.csv', encoding='utf-8-sig') #저장
    #db에 저장
    data.to_sql(name='cmlist',con=db.db_connection,if_exists='replace',index=False)
    print('done')

