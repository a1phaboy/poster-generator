from operator import index
import random
from zhdate import ZhDate
from datetime import datetime
import json
import requests
import mysql.connector


class config:
    def __init__(self,width,height,backgroundColor,blocks,texts,images,lines):
        self.width = width
        self.height = height
        self.backgroundColor = backgroundColor
        self.blocks = blocks
        self.texts = texts
        self.images = images
        self.lines = lines

class blocks:
    def __init__(self,x,y,width,height,backgroundColor,borderRadius,zIndex):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.backgroundColor = backgroundColor
        self.borderRadius = borderRadius
        self.zIndex = zIndex

class texts:
    def __init__(self,x,y,text,fontSize,font,color,lineNum=10,baseLine="middle",textAlign="center",zindex=3):
        self.x = x
        self.y = y
        self.text = text
        self.fontSize = fontSize
        self.color = color
        self.lineHeight = fontSize
        self.lineNum = lineNum
        self.baseLine = baseLine
        self.textAlign = textAlign
        self.zindex = zindex
        self.font = font
        
class images:
    def __init__(self,x,y,url,width,height,zindex):
        self.x = x
        self.y = y
        self.url = url
        self.width = width
        self.height = height
        self.zindex = zindex

class lines:
    def __init__(self,startX,startY,endX,endY,width,color,index):
        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY
        self.width = width
        self.color = color
        self.index = index

def initTexts(keywordList):
    now = datetime.now()
    dt_date = datetime(now.year, now.month, now.day)
    date = ZhDate.from_datetime(dt_date)
    year = date.chinese()[-8:]
    da = date.chinese()[:-8]
    textsList = []
    yearText = texts(30,200,year,50,"zihun-110","#000")
    dateText = texts(30,280,da,45,"zihun-110","#000")
    keywordText1 = texts(25,760,keywordList[0],80,"zihun-24","#00C957")
    keywordText2 = texts(25,900,keywordList[1],80,"zihun-24","#00C957")
    keywordText3 = texts(25,1440,keywordList[2],80,"zihun-24","#FF0000")
    keywordText4 = texts(25,1580,keywordList[3],80,"zihun-24","#FF0000")
    textsList.append(vars(yearText))
    textsList.append(vars(dateText))
    textsList.append(vars(keywordText1))
    textsList.append(vars(keywordText2))
    textsList.append(vars(keywordText3))
    textsList.append(vars(keywordText4))
    return textsList

def initImages():
    imagesList = []
    imagesList.append(vars(images(0,0,"kuafu_modelpage.png",1237,1960,0)))
    return imagesList

def initBlocks():
    blocksList = []
    blocksList.append(vars(blocks(128,540,384,540,"#000",13,2)))
    return blocksList

def initLines():
    linesList = []
    return linesList

def init(keywordList):
    return config(1237,1960,"#000",initBlocks(),initTexts(keywordList),initImages(),initLines())

def countdb(mydb):
    query = mydb.cursor()
    query.execute("explain select * from keyword_table;")
    count = query.fetchall()[0][9]
    return count

def getRandId(row):
    randList = []
    i=0
    while i < 4:
        exist = False
        rand = random.randint(1,row)
        #print(rand)
        for key_id in randList :
            if key_id == rand :
                exist = True
                break
        if exist == False :
            randList.append(rand)
            i += 1
    return randList

def getKeyWord(randList):
    keywordList = []
    for keyword in randList :
        query = mydb.cursor()
        sql = 'select keyword from keyword_table where id = "%s";' 
        query.execute(sql,keyword)
        #print(keyword)
        keywordList.append(query.fetchall()[0][0]) 
    return keywordList

if __name__ == "__main__":

    #数据库随机去拉数据

    mydb = mysql.connector.connect(
        host="localhost",              #数据库名
        user="root",                   #用户
        passwd="root",                 #密码
        auth_plugin="mysql_native_password",
        database= "kuafuzhuri"         #数据库
    )
  
    row = countdb(mydb)
    randList = getRandId(row)
    keywordList = getKeyWord(randList)
    #print(keywordList)
    #config = init(keyword1,keyword2,keyword3,keyword4)
    #print(json.dumps(vars(init(keyword1,keyword2,keyword3,keyword4))))
    body = json.dumps(vars(init(keywordList)))
    #print(body)
    #poster server api
    rep=requests.post("http://1.117.71.185:8000/poster",headers={'content-type':'application/json'},data=body)
    print(rep.text)