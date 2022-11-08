import pymysql


class DB:
    def __init__(self):
        self.db = pymysql.connect(host="180.76.162.227", user="root", password="123456", port=23306)
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()

    def ShowAllDataBases(self):
        self.cursor.execute("SHOW DATABASES;")
        print(self.cursor.fetchall())

    def QueryDataInAllTable(self, tableName):
        self.cursor.execute("SELECT * from {}".format(tableName))
        print(self.cursor.fetchall())

    def Run(self, command):
        self.cursor.execute(command)
        print(self.cursor.fetchall())


db = DB()
db.Run("use mysql")
db.Run("show tables")
db.Run("select * from db")
