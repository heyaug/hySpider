from DBUtils.PooledDB import PooledDB
from pymongo import MongoClient
from config.setting import mySql, monGo
import pymysql


class MysqlPool:
    """
    单例模式+连接池
    """
    __instance = None
    __isFirstInit = False

    def __new__(cls):
        if not cls.__instance:
            MysqlPool.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        if not self.__isFirstInit:
            MysqlPool.__isFirstInit = True
            config = {
                'creator': pymysql,
                'host': mySql["host"],
                'port': mySql["port"],
                'user': mySql["user"],
                'password': mySql["password"],
                'maxconnections': 30,
                'cursorclass': pymysql.cursors.DictCursor
            }
            pool = PooledDB(**config)
            self.conn = pool.connection()
            self.cursor = self.conn.cursor()

    def execute_sql(self, sqlStr, fetch=False):
        """
        fetch标记是否取数据，如select等
        :param sqlStr:
        :param fetch:
        :return:
        """
        self.cursor.execute(sqlStr)
        self.conn.commit()
        if fetch:
            return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()


class MongoDB:
    def __init__(self, db, table):
        self.client = MongoClient(monGo["host"], monGo["port"])
        if monGo.get("user") and monGo.get("password"):
            self.client.admin.authenticate(monGo["user"], monGo["password"])
        self.db = self.client[db]
        self.table = self.db[table]
        self.con = self.table

    def updateOne(self, _id, data):
        """
        通用插入方式，存在更新 不存在插入，_id唯一
        :param _id:
        :param data:
        :return:
        """
        return self.con.update_one({"_id": _id}, {"$set": data}, True)

    def MongoConn(self):
        """
        其他 获取游标
        :return:
        """
        return self.con
