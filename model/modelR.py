import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine
import pymysql

class modelR:
    def __init__(self,DB):
        # #mysql con
        # db='mysql+pymysql://root:wls159@localhost:3306/cmdata'
        # self.db_connection=create_engine(db)
        # self.conn=self.db_connection.connect()
        
        # data=pd.read_csv(r'C:\Users\wlsyo\test\test.csv',index_col=0)
        self.data=pd.read_sql_table('cmlist',DB.conn)
        self.data=self.data.fillna('') #결측값 대체

        self.values=pd.DataFrame(data=[],columns=['id','data'])
        self.values['id']=self.data['id']
        self.values['data']=self.data['local']+' '+self.data['field']+' '+self.data['awarding']+' '+self.data['benefit']+' '+self.data['detail']
        #print(values['data'].isnull().sum())

    def findRecommend(self,userTable):
        data=pd.DataFrame(data=[],columns=['id','data']) #dataFrame

        #add userdata
        userData=pd.DataFrame(data=[],columns=['id','data'])
        userData['id']=userTable['id']
        userData['data']=userTable['local']+' '+userTable['field']+' '+userTable['awarding']+' '+userTable['benefit']+' '+userTable['detail']
        data=pd.concat([self.values,userData],axis=0,ignore_index=True) 
        data=data.drop_duplicates(['id'],keep='first') #중복값 제거
        data=data.fillna('') #결측값 대체

        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(data['data'])
        #print(tfidf_matrix.shape)

        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        #print(cosine_sim.shape)

        #타이틀의 인덱스를 가지는 딕셔너리
        ftitleToIndex=dict(zip(data['id'],data.index))
        
        #userData의 id를 가지는 리스트
        userid=userData['id']
        candidate=pd.DataFrame(data=[],columns=['id','score'])
        
        for i in range(userData.shape[0]):
            idx=ftitleToIndex[userid[i]]  #인덱스 반환

            # 해당 데이터와 다른 데이터 사이의 유사도
            sim_scores = list(enumerate(cosine_sim[idx]))
            
            # 유사도에 따른 정렬
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            # 가장 유사한 10개의 데이터
            sim_scores = sim_scores[1:11]
            
            # 가장 유사한 10개의 데이터의 인덱스
            data_indices = [idx[0] for idx in sim_scores]
            candidate=pd.concat([candidate,pd.DataFrame({'id':data['id'].iloc[data_indices],'score':'one'})],axis=0,ignore_index=False)
            # # 가장 유사한 10개의 데이터 반환
            # return data['id'].iloc[data_indices].values.tolist()
        scores=candidate.groupby('id').count()
        scores=scores.sort_values(by=['score'],ascending=False)
        return scores[0:10].index.tolist()

# checkTitle='넷제로 영상공모전 LET\'S ZERO NET ZERO'
# print(titleToIndex[checkTitle],checkTitle)
# print(findRecommend(checkTitle))