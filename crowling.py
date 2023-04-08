# from crowlingData.allforyoung import *
# from crowlingData.linkarrer import *
# from crowlingData.spectory import *
from crowlingData.dataProcessing import *
from settingDB import setDB

db=setDB()

#요즘것들 공모전
crowling_AFY_CM(db)

#요즘것들 대외활동
crowling_AFY_OA(db)

#링커리어 공모전
crowling_LK_CM(db)

#링커리어 대외활동
crowling_LK_OA(db)

#링커리어 인턴
crowling_LK_IN(db)

#링커리어 채용
crowling_LK_EM(db)

#스펙토리 공모전
crowling_SPT_CM(db)

#스펙토리 대외활동
crowling_SPT_OA(db)

#데이터 전처리
dataProcessing(db)

db.close()
