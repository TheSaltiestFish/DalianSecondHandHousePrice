from typing import Counter
import pymongo
import csv
from pymongo import collection
from pymongo.mongo_client import MongoClient

def conn(): #连接数据库，选中所需集合house
    myclient = pymongo.MongoClient('mongodb://127.0.0.1:27017')
 #   myclient.admin.authenticate("user_mongo","123456",mechanism='SCRAM-SHA-1')
    mydb = myclient['mongoproject']
    mycol = mydb['house']
    db=myclient.mongoproject
    set1 = db.house
    return set1

def insert_to_db(set1):#从爬出的csv文件中筛选出想要的关键字并插入house里
    with open("house_price.csv",encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for each in reader:
            del each['type']
            del each['total']
            del each['name']
            set1.insert_one(each)

def find_by_area(ar):#根据区域查找
    set2 = conn()
    return set2.find({'area':ar})

def main():
    set1 = conn()
    insert_to_db(set1)

main()