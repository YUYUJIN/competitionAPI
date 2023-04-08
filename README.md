# competitionAPI
> selenium을 이용한 크롤링을 진행하여 database 내에 공모전 정보를 수집  
> Flask, SQLAlchemy를 이용한 간이 API 구성  
> scikit-learn,pandas를 이용한 유사 공모전 추천 시스템  
  
<img src=https://img.shields.io/badge/python-3.8.0-green></img>
<img src=https://img.shields.io/badge/selenium-4.4.2-yellow></img>
<img src=https://img.shields.io/badge/Flask-2.2.2-blue></img>
<img src=https://img.shields.io/badge/SQLAlchemy-1.4.40-orange></img>
<img src=https://img.shields.io/badge/scikit--learn-1.1.2-lightgrey></img>
<img src=https://img.shields.io/badge/pandas-1.4.3-red></img>

## How to use
사전준비 및 필요 dependency 설치   
```
git clone https://github.com/YUYUJIN/competitionAPI.git
cd competitionAPI
pip install -r requirements.txt
```

workplace 내에 .env 파일을 만들어 Database의 정보생성
본 프로젝트에서는 AWS의 RDS를 사용하였고, 엔진으로는 MySQL로 구성하였다.  
<(rds)이미지>  

이후 크롤링 코드를 실행하여 크롤링한 정보를 Database에 저장한다.  
```
python crowling.py
```  

이후 app을 구동하여 간이 API를 사용한다.  
```
python app.py
```

## Crowling
해당 프로젝트에서 크롤링될 사이트로는 구글 검색에서 상위에 랭크된 공모전 사이트를 이용하였다.  
링커리어: https://linkareer.com  
스펙토리: http://spectory.net  
요즘것들: https://allforyoung.com 
   
아래 사이트에서 중복되거나 서로 상충할 수 있는 정보들로 데이터의 속성을 정의하였다.  
정의한 속성은 제목, 주관, 대상, 인원, 기간, 지역, 분야, 문의, 상세 페이지, 시상, 지원, 원본, 세부사항이다.  
  
<(db)이미지>
  
selenium으로 조작하고, xpath를 위주로 정보에 접근하였다. 몇몇 사이트는 동적으로 페이지가 랜딩되기 때문에 css 코드가 수정되는 경우가 많았고, class등의 항목은 누락되는 경우가 많아 xpath로 접근하였다. 추가로 xpath는 프로젝트 개발 시점에 맞게 css 코드 내 규칙을 찾아 작성되었으므로 추후 올바르지 않을 수 있다.

## TF-IDF && Cosine Similarity
Flask를 통해 간이 API를 사용한다. 유저가 선호하는 공모전 데이터를 DataBase에 저장한다.  
<(user)이미지>
  
크롤링을 통해 저장한 데이터를 유저가 선호하는 공모전 데이터와 유사도를 비교하여 상위 10개의 데이터를 찾는다.  
  
유저가 선호하는 공모전이 2개 이상인 경우에는 각 공모전과 유사한 10개의 공모전들을 찾고 중복 정도를 검사하여 중복도가 높은 최상위 10개의 데이터를 사용한다.  
  
이 때 유사도는 TF-IDF와 코사인 유사도 방식만을 사용하여 해당 정보의 유사도를 비교한다.  
  
참고자료: https://wikidocs.net/24603  

## API Document
<(API 명세서)이미지>  
최종 API와 결과는 위와 같다. 아래 상세 페이지 참조.  
  
API Document: https://documenter.getpostman.com/view/15695216/VUqptxfz  

## Reference
딥 러닝을 이용한 자연어 처리 입문: https://wikidocs.net/24603  