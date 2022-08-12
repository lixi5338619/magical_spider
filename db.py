import os.path
import sqlite3
from models import *
from settings import magicalpath


def create_connection():
    db = sqlite3.connect(magicalpath)
    return db


def select_process():
    db = create_connection()
    con = db.cursor()
    con.execute("select * from process")
    res = con.fetchall()
    con.close()
    db.close()
    return res


def select_process_name(processName:str)->Process:
    db = create_connection()
    con = db.cursor()
    con.execute("select * from process where processName=?",(processName,))
    res = con.fetchone()
    con.close()
    db.close()
    return res

def select_process_id(processId:str)->Process:
    db = create_connection()
    con = db.cursor()
    con.execute("select * from process where processId=?",(processId,))
    res = con.fetchone()
    con.close()
    db.close()
    return res

def insert_process(process:Process)->Process:
    db = create_connection()
    cursor = db.cursor()
    try:
        cursor.execute("insert into process(processId, processName, processUrl, createTime) values ('%s','%s','%s','%s')" % (process.processId, process.processName, process.processUrl,datetime.datetime.now()))
        db.commit()
        cursor.close()
        db.close()
        return process
    except Exception as e:
        print(e)
        db.rollback()
        cursor.close()
        db.close()


def delete_process(process_name):
    db = create_connection()
    cursor = db.cursor()
    try:
        cursor.execute("delete FROM process where processName ='%s'" % (process_name))
        db.commit()
        cursor.close()
        db.close()
    except Exception as e:
        db.rollback()
        cursor.close()
        db.close()

def delete_process_id(processId):
    db = create_connection()
    cursor = db.cursor()
    try:
        cursor.execute("delete FROM process where processId ='%s'" % (processId))
        db.commit()
        cursor.close()
        db.close()
    except Exception as e:
        db.rollback()
        cursor.close()
        db.close()



if __name__ == '__main__':
    if not os.path.exists(magicalpath):
        con = sqlite3.connect(magicalpath)
        cursor = con.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS `process`(`processId` VARCHAR(90),`processName` VARCHAR(90) UNIQUE,`processUrl` VARCHAR(256),`createTime` DATA,`baseUrl` VARCHAR(256));")
        con.commit()