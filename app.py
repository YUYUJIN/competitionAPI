from flask import Flask, jsonify, request
from sqlalchemy import create_engine
import pymysql
import pandas as pd
from model.modelR import modelR
from settingDB import setDB
import atexit

app=Flask("cm_api")
db=setDB()
model=modelR(db)

@app.route("/api/<userId>/CM", methods=['GET','POST','DELETE'])
def api(userId):
    userTable='user'+userId

    if request.method=='GET':
        try:
            #tagetId=db.db_connection.execute("select * from %s"%(userTable)).fetchall()
            userData=pd.read_sql_table(userTable,db.conn)
            rcmId=model.findRecommend(userData)
            where="id=\"%s\" or id=\"%s\" or id=\"%s\" or id=\"%s\" or id=\"%s\" or id=\"%s\" or id=\"%s\" or id=\"%s\" or id=\"%s\" or id=\"%s\""%(rcmId[0],rcmId[1],rcmId[2],rcmId[3],rcmId[4],rcmId[5],rcmId[6],rcmId[7],rcmId[8],rcmId[9])
            result=db.db_connection.execute("select id,title,period,field from cmlist where %s"%(where)).fetchall()
            response = {
                '0':{'id':result[0][0],
                    'title':result[0][1],
                    'period':result[0][2],
                    'field':result[0][3]},
                '1':{'id':result[1][0],
                    'title':result[1][1],
                    'period':result[1][2],
                    'field':result[1][3]},
                '2':{'id':result[2][0],
                    'title':result[2][1],
                    'period':result[2][2],
                    'field':result[2][3]},
                '3':{'id':result[3][0],
                    'title':result[3][1],
                    'period':result[3][2],
                    'field':result[3][3]},
                '4':{'id':result[4][0],
                    'title':result[4][1],
                    'period':result[4][2],
                    'field':result[4][3]},
                '5':{'id':result[5][0],
                    'title':result[5][1],
                    'period':result[5][2],
                    'field':result[5][3]},
                '6':{'id':result[6][0],
                    'title':result[6][1],
                    'period':result[6][2],
                    'field':result[6][3]},
                '7':{'id':result[7][0],
                    'title':result[7][1],
                    'period':result[7][2],
                    'field':result[7][3]},
                '8':{'id':result[8][0],
                    'title':result[8][1],
                    'period':result[8][2],
                    'field':result[8][3]},
                '9':{'id':result[9][0],
                    'title':result[9][1],
                    'period':result[9][2],
                    'field':result[9][3]},
                'message': 'success'
            }
        except:
            response={
                'message': 'failed'
            }
        
    if request.method=='POST':
        taget=request.get_json()
        tagetId=taget['id']

        try:
            db.db_connection.execute("insert into %s select * from cmlist where id=\"%s\""%(userTable,tagetId))
            response={
                'message': 'success'
            }        
        except:
            response={
                'message': 'failed'
            }

    if request.method=='DELETE':
        taget=request.json
        tagetId=taget['id']
        try:
            db.db_connection.execute("delete from %s where id=\"%s\""%(userTable,tagetId))
            response = {
                'massage': 'success'
            }
        except:
            response={
                'massage': 'failed'
            }
    
    return jsonify(response), 200

@app.route("/api/<userId>/CM/detail/<cmid>", methods=['GET'])
def detail(userId,cmid):
    userTable='user'+userId
    tagetId=cmid

    if request.method=='GET':
        try:
            tagetData=db.db_connection.execute("select * from %s where id=\"%s\""%(userTable,tagetId)).fetchall()
            print(tagetData)
            response = {
                'title': tagetData[0][1],
                'manage': tagetData[0][2],
                'taget': tagetData[0][3],
                'men': tagetData[0][4],
                'period': tagetData[0][5],
                'local': tagetData[0][6],
                'field': tagetData[0][7],
                'inquiry': tagetData[0][8],
                'page': tagetData[0][9],
                'awarding': tagetData[0][10],
                'benefit': tagetData[0][11],
                'source': tagetData[0][12],
                'detail': tagetData[0][15],
                'note': tagetData[0][13],
                'url': tagetData[0][14],
                'massage': 'success'
            }
        except:
            response={
                'massage': 'failed'
            }
    
    return jsonify(response), 200

#define closing/register closing db
@atexit.register
def close_running():
    db.close()

if __name__=='__main__':
    app.run('0.0.0.0',port=5000,debug=True)