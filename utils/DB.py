import pymysql
from utils.configs import BC

"""
用户登录表：name,password,user id
用户信息：user id,register time,brief description
用户资源表(user id)：source id,source name,source location,source size
-->登录：从数据库中查询是否有用户
-->注册：插入用户和密码，创建用户信息，创建用户资源表
"""


class DB:
    __tableList = []

    def __init__(self):
        self.__db = pymysql.connect(host=BC.Mysql.Host, user=BC.Mysql.User, password=BC.Mysql.Password,
                                    port=BC.Mysql.Port)
        self.__cursor = self.__db.cursor()
        self.__tableList = {i_[0]: [] for i_ in self.__Run("show databases")}
        for _name in self.__tableList:
            self.__Run("use {}".format(_name))
            self.__tableList[_name] = [i_[0] for i_ in self.__Run("show tables")]
        self.__Database = ""
        self.__Table = ""
        if BC.Mysql.mainDatabase not in self.__tableList:
            self.__CreateDatabase(BC.Mysql.mainDatabase)
        SETTLED_TABLE = BC.Mysql.SettledTable
        self.__UseDatabase(BC.Mysql.mainDatabase)
        if SETTLED_TABLE.UserInfoTableInMysql not in self.__tableList[BC.Mysql.mainDatabase]:
            self.__CreateTable(SETTLED_TABLE.UserInfoTableInMysql, SETTLED_TABLE.UserInfoTable,
                               SETTLED_TABLE.UserInfoTablePrimaryKey)
        if SETTLED_TABLE.UserLoginTableInMysql not in self.__tableList[BC.Mysql.mainDatabase]:
            self.__CreateTable(SETTLED_TABLE.UserLoginTableInMysql, SETTLED_TABLE.UserLoginTable,
                               SETTLED_TABLE.UserLoginTablePrimaryKey)
        if SETTLED_TABLE.AllSourceTableInMysql not in self.__tableList[BC.Mysql.mainDatabase]:
            self.__CreateTable(SETTLED_TABLE.AllSourceTableInMysql, SETTLED_TABLE.AllSourceTable,
                               SETTLED_TABLE.AllSourceTablePrimaryKey)
        # 如果没有创建对应的表，就先创建

    def reConnect(self):
        self.__db.close()
        self.__init__()

    def __del__(self):
        # print("::debug::销毁db实例前查询所有资源:{}".format(self.QueryAllResources()))
        self.__db.close()

    def __Run(self, command):
        # print("::debug::运行{}命令ing".format(command))
        try:
            self.__cursor.execute(command)
            self.__cursor.connection.commit()  # 这玩意。。。我tm真的服了。。。不加这一句提交不上去，也不知道为啥。。。。
            return self.__cursor.fetchall()
        except Exception as e:
            raise Exception("运行{}命令出错：\n{}".format(command, e))

    def __UseDatabase(self, dataBase: str):
        if dataBase not in self.__tableList:
            raise Exception("ERROR::不存在数据库{}".format(dataBase))
        self.__cursor.execute("use {}".format(dataBase))
        self.__Database = dataBase
        self.__Table = ""

    def __CreateDatabase(self, dataBase: str):
        if dataBase in self.__tableList:
            raise Warning("Warning::数据库已经存在")
        self.__cursor.execute("create database {}".format(dataBase))
        self.__tableList[dataBase] = []

    def __DeleteDatabase(self, dataBase: str):
        if dataBase not in self.__tableList:
            raise Exception("ERROR::数据库不存在")
        self.__cursor.execute("drop database {}".format(dataBase))
        del self.__tableList[dataBase]

    def __CreateTable(self, _table: str, SettledTable: list, PrimaryKey: str):
        """
        选定一些注册好的属性来创建一个表
        :param _table: 表名
        :param SettledTable: 表的属性名（必须是注册好的属性才行））
        :param PrimaryKey: 表的主键
        :return:
        """
        if PrimaryKey not in SettledTable:
            raise Exception("ERROR::主键{}不在输入的表中".format(PrimaryKey))
        for i in SettledTable:
            if i not in BC.Mysql.SettledTable.allAttribute:
                raise Exception("ERROR::输入表中{}不在注册好的属性中".format(i))
        if self.__Database == "":
            raise Exception("ERROR::还未指定数据库")
        if _table in self.__tableList[self.__Database]:
            raise Warning("Warning::数据库{}中已经存在{}".format(self.__Database, _table))
        command = "create table if not exists `{}`(".format(_table)
        for i in SettledTable:
            command += "`" + i + "`" + " " + BC.Mysql.SettledTable.allAttribute[i] + ","
        command += "PRIMARY KEY ( `{}` ))ENGINE=InnoDB DEFAULT CHARSET=utf8mb4".format(PrimaryKey)
        self.__cursor.execute(command)
        self.__tableList[self.__Database].append(_table)

    def __DeleteTable(self, _table: str):
        if self.__Database == "":
            raise Exception("ERROR::还未指定数据库")
        if _table not in self.__tableList[self.__Database]:
            raise Exception("ERROR::数据库{}不存在表{}".format(self.__Database, _table))
        self.__cursor.execute("drop table {}".format(_table))

    def __GetUserID(self, UserName: str):
        if BC.Mysql.mainDatabase not in self.__tableList:
            # self.__CreateDatabase(BC.Mysql.mainDatabase)
            raise Exception("ERROR::未创建origin数据库")
        self.__UseDatabase(BC.Mysql.mainDatabase)
        SETTLED_TABLE = BC.Mysql.SettledTable
        X_ = self.__Run("select UserID from {} where Name='{}'".format(SETTLED_TABLE.UserLoginTableInMysql, UserName))
        if not len(X_):
            raise Exception("ERROR::不存在{}用户".format(UserName))
        if len(X_) != 1:
            raise Exception("FATAL::出现了多个同名用户")
        UserID = X_[0][0]
        return UserID

    def __GetSourceID(self, SourceName: str):
        if BC.Mysql.mainDatabase not in self.__tableList:
            # self.__CreateDatabase(BC.Mysql.mainDatabase)
            raise Exception("ERROR::未创建origin数据库")
        self.__UseDatabase(BC.Mysql.mainDatabase)
        SETTLED_TABLE = BC.Mysql.SettledTable
        X_ = self.__Run(
            "select SourceID from {} where SourceName='{}'".format(SETTLED_TABLE.AllSourceTableInMysql, SourceName))
        if not len(X_):
            raise Exception("ERROR::不存在{}资源".format(SourceName))
        if len(X_) != 1:
            raise Exception("FATAL::出现了多个同名资源")
        SourceID = X_[0][0]
        return SourceID

    def QueryAllUser(self):
        SETTLED_TABLE = BC.Mysql.SettledTable
        if BC.Mysql.mainDatabase not in self.__tableList:
            # self.__CreateDatabase(BC.Mysql.mainDatabase)
            raise Exception("ERROR::未创建origin数据库")
        self.__UseDatabase(BC.Mysql.mainDatabase)
        X_ = self.__Run("select Name from {}".format(SETTLED_TABLE.UserLoginTableInMysql))
        RES = []
        for I in X_:
            RES.append(I[0])
        return RES

    def AddUser(self, UserName: str, Password: str):
        """
        增加一个用户，1：在用户登录表中增加用户，2：同时在用户信息表中增加用户，3：同时增加用户的用户资源表
        :param UserName:
        :param Password:
        :return:success: 1 failure: 0
        """
        SETTLED_TABLE = BC.Mysql.SettledTable
        if BC.Mysql.mainDatabase not in self.__tableList:
            # self.__CreateDatabase(BC.Mysql.mainDatabase)
            raise Exception("ERROR::未创建origin数据库")
        self.__UseDatabase(BC.Mysql.mainDatabase)
        if SETTLED_TABLE.UserLoginTableInMysql not in self.__tableList[BC.Mysql.mainDatabase]:
            self.__CreateTable(SETTLED_TABLE.UserLoginTableInMysql, SETTLED_TABLE.UserLoginTable,
                               SETTLED_TABLE.UserLoginTablePrimaryKey)
        # self.UseTable(SETTLED_TABLE.UserLoginTableInMysql)
        X_ = self.__Run("select UserID from {} where Name='{}'".format(SETTLED_TABLE.UserLoginTableInMysql, UserName))
        if len(X_):  # 说明有重复的用户名
            return 0
        command = "insert into {}".format(SETTLED_TABLE.UserLoginTableInMysql)
        command += "(Name,Password) values('{}','{}')".format(UserName, Password)
        self.__Run(command)
        X_ = self.__Run("select UserID from {} where Name='{}'".format(SETTLED_TABLE.UserLoginTableInMysql, UserName))
        UserID = X_[0][0]
        # 1
        if SETTLED_TABLE.UserInfoTableInMysql not in self.__tableList[BC.Mysql.mainDatabase]:
            self.__CreateTable(SETTLED_TABLE.UserInfoTableInMysql, SETTLED_TABLE.UserInfoTable,
                               SETTLED_TABLE.UserInfoTablePrimaryKey)
        # self.UseTable(SETTLED_TABLE.UserInfoTableInMysql)
        command = "insert into {}".format(SETTLED_TABLE.UserInfoTableInMysql)
        command += "(UserID,RegisterTime) values({},NOW())".format(UserID)
        self.__Run(command)
        # 2
        if SETTLED_TABLE.UserSourceTableInMysql.format(UserID) not in self.__tableList[BC.Mysql.mainDatabase]:
            self.__CreateTable(SETTLED_TABLE.UserSourceTableInMysql.format(UserID), SETTLED_TABLE.UserSourceTable,
                               SETTLED_TABLE.UserSourceTablePrimaryKey)
        # 3
        return 1

    def DeleteUser(self, UserName: str):
        SETTLED_TABLE = BC.Mysql.SettledTable
        if BC.Mysql.mainDatabase not in self.__tableList:
            # self.__CreateDatabase(BC.Mysql.mainDatabase)
            raise Exception("ERROR::未创建origin数据库")
        self.__UseDatabase(BC.Mysql.mainDatabase)
        X_ = self.__Run("select UserID from {} where Name='{}'".format(SETTLED_TABLE.UserLoginTableInMysql, UserName))
        if not len(X_):
            raise Exception("ERROR::不存在{}用户".format(UserName))
        if len(X_) != 1:
            raise Exception("FATAL::出现了多个同名用户")
        UserID = X_[0][0]
        command = "delete from {} where Name = '{}'".format(SETTLED_TABLE.UserLoginTableInMysql, UserName)
        self.__Run(command)
        command = "delete from {} where UserID = '{}'".format(SETTLED_TABLE.UserInfoTableInMysql, UserID)
        self.__Run(command)
        self.__DeleteTable(SETTLED_TABLE.UserSourceTableInMysql.format(UserID))

    def QueryUserPas(self, UserName: str):
        SETTLED_TABLE = BC.Mysql.SettledTable
        if BC.Mysql.mainDatabase not in self.__tableList:
            # self.__CreateDatabase(BC.Mysql.mainDatabase)
            raise Exception("ERROR::未创建origin数据库")
        self.__UseDatabase(BC.Mysql.mainDatabase)
        X_ = self.__Run("select Password from {} where Name='{}'".format(SETTLED_TABLE.UserLoginTableInMysql, UserName))
        if not len(X_):
            raise Exception("ERROR::不存在{}用户".format(UserName))
        if len(X_) != 1:
            raise Exception("FATAL::出现了多个同名用户")
        return X_[0][0]

    def QueryUserInfo(self, UserName: str):
        SETTLED_TABLE = BC.Mysql.SettledTable
        if BC.Mysql.mainDatabase not in self.__tableList:
            # self.__CreateDatabase(BC.Mysql.mainDatabase)
            raise Exception("ERROR::未创建origin数据库")
        self.__UseDatabase(BC.Mysql.mainDatabase)
        X_ = self.__Run("select UserID from {} where Name='{}'".format(SETTLED_TABLE.UserLoginTableInMysql, UserName))
        if not len(X_):
            raise Exception("ERROR::不存在{}用户".format(UserName))
        if len(X_) != 1:
            raise Exception("FATAL::出现了多个同名用户")
        UserID = X_[0][0]

        X_ = self.__Run(
            "select RegisterTime from {} where UserID='{}'".format(SETTLED_TABLE.UserInfoTableInMysql, UserID))
        RegisterTime = X_[0][0]
        X_ = self.__Run(
            "select BriefDescription from {} where UserID='{}'".format(SETTLED_TABLE.UserInfoTableInMysql, UserID))
        return RegisterTime, X_[0][0]

    def UploadResource(self, SourceName, SourceLocation, SourceSize: float, UserName, Intro="用户上传的资源"):
        # print("::debug::开始上传数据")
        UserID = self.__GetUserID(UserName)
        SETTLED_TABLE = BC.Mysql.SettledTable
        self.__UseDatabase(BC.Mysql.mainDatabase)
        if BC.Mysql.mainDatabase not in self.__tableList:
            # self.__CreateDatabase(BC.Mysql.mainDatabase)
            raise Exception("ERROR::未创建origin数据库")
        X_ = self.__Run(
            "select SourceID from {} where SourceName='{}'".format(SETTLED_TABLE.AllSourceTableInMysql, SourceName))
        # pymysql.err.OperationalError: (1054, "Unknown column 'SourceName' in 'where clause'")
        if len(X_):
            raise Exception("ERROR::存在资源{}".format(SourceName))
        # print("::debug::插入前查询资源：{}".format(self.QueryAllResources()))
        command = "insert into {}".format(SETTLED_TABLE.AllSourceTableInMysql)
        command += "(SourceName,SourceLocation,SourceSize,SourceIntroduction,SourceUploadTime) values('{}','{}',{},'{}',NOW())".format(
            SourceName, SourceLocation,
            SourceSize, Intro)
        self.__Run(command)
        # 在总表里插入当前资源
        # print("::debug::插入后查询资源：{}".format(self.QueryAllResources()))
        X_ = self.__Run(
            "select SourceID from {} where SourceName='{}'".format(SETTLED_TABLE.AllSourceTableInMysql,
                                                                   SourceName))
        if not len(X_):
            raise Exception("ERROR::资源插入失败")
        # SourceID = self.__GetSourceID(SourceName)
        # print("::debug::插入后查询资源2：{}".format(self.QueryAllResources()))
        SourceID = X_[0][0]
        X_ = self.__Run(
            "select SourceID from {} where SourceID='{}'".format(SETTLED_TABLE.UserSourceTableInMysql.format(UserID),
                                                                 SourceID))
        if len(X_):
            raise Exception("ERROR::用户{}已存在资源{}", format(UserName, SourceName))
        # print("::debug::插入后查询资源3：{}".format(self.QueryAllResources()))
        command = "insert into {}".format(SETTLED_TABLE.UserSourceTableInMysql.format(UserID))
        command += "(SourceID) values({})".format(SourceID)
        self.__Run(command)
        # print("::debug::插入后查询资源4：{}".format(self.QueryAllResources()))
        # print("::debug::结束上传数据")
        # 在用户资源表中插入资源

    def DeleteResourceInUser(self, SourceName: str, UserID):
        if BC.Mysql.mainDatabase not in self.__tableList:
            # self.__CreateDatabase(BC.Mysql.mainDatabase)
            raise Exception("ERROR::未创建origin数据库")
        self.__UseDatabase(BC.Mysql.mainDatabase)
        SETTLED_TABLE = BC.Mysql.SettledTable
        self.__Run(
            "delete from {} where Name = '{}'".format(SETTLED_TABLE.UserSourceTableInMysql.format(UserID),
                                                      SourceName))
        # 在用户资源表中删除资源

    def DeleteResourceInAllTable(self, SourceName: str, UserID):
        if BC.Mysql.mainDatabase not in self.__tableList:
            # self.__CreateDatabase(BC.Mysql.mainDatabase)
            raise Exception("ERROR::未创建origin数据库")
        SETTLED_TABLE = BC.Mysql.SettledTable
        self.__UseDatabase(BC.Mysql.mainDatabase)
        X_ = self.__Run(
            "select SourceID from {} where SourceName='{}'".format(SETTLED_TABLE.AllSourceTableInMysql, SourceName))
        if not len(X_):
            raise Exception("ERROR::不存在名为{}的资源".format(SourceName))
        self.__Run(
            "delete from {} where Name = '{}'".format(SETTLED_TABLE.AllSourceTableInMysql, SourceName))
        self.DeleteResourceInUser(SourceName, UserID)

    def QueryResourcesByID(self, SourceID: int):
        if BC.Mysql.mainDatabase not in self.__tableList:
            # self.__CreateDatabase(BC.Mysql.mainDatabase)
            raise Exception("ERROR::未创建origin数据库")
        self.__UseDatabase(BC.Mysql.mainDatabase)
        SETTLED_TABLE = BC.Mysql.SettledTable
        self.__UseDatabase(BC.Mysql.mainDatabase)
        X_ = self.__Run("select * from {} where SourceID = {}".format(SETTLED_TABLE.AllSourceTableInMysql, SourceID))
        return X_

    def QueryUserResources(self, UserName):
        if BC.Mysql.mainDatabase not in self.__tableList:
            # self.__CreateDatabase(BC.Mysql.mainDatabase)
            raise Exception("ERROR::未创建origin数据库")
        self.__UseDatabase(BC.Mysql.mainDatabase)
        SETTLED_TABLE = BC.Mysql.SettledTable
        UserID = self.__GetUserID(UserName)
        X_ = self.__Run(
            "select * from {}".format(SETTLED_TABLE.UserSourceTableInMysql.format(UserID)))
        return X_

    def QueryAllResources(self):
        if BC.Mysql.mainDatabase not in self.__tableList:
            # self.__CreateDatabase(BC.Mysql.mainDatabase)
            raise Exception("ERROR::未创建origin数据库")
        self.__UseDatabase(BC.Mysql.mainDatabase)
        SETTLED_TABLE = BC.Mysql.SettledTable
        X_ = self.__Run(
            "select * from {}".format(SETTLED_TABLE.AllSourceTableInMysql))
        return X_


if __name__ == '__main__':
    db = DB()
    print("::debug::完成初始化")
    # db.AddUser("Tomy", "123321")
    # db.AddUser("root", "123321")
    # x = db.QueryUserInfo("root")
    db.UploadResource("S1.zip", "ROOT", 23.3, "root")
    # db.UploadResource("S2.zip", "ROOT", 23.3, "root")
    # db.UploadResource("S3.zip", "ROOT", 23.3, "root")
    # print("::debug::插入函数执行完后查询所有资源:{}".format(db.QueryAllResources()))
    # x = db.QueryUserResources("root")
    # print("::debug::查询函数执行完后查询所有资源:{}".format(db.QueryAllResources()))
    # print(x)
    x = db.QueryAllUser()
    print(x)
    # print("::debug::程序结束前查询所有资源:{}".format(db.QueryAllResources()))
    print("end")
