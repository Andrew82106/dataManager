"""
用户登录表：user id(INT),name(VARCHAR(30)),password(VARCHAR(30))
用户信息：user id,register time(DATE),brief description(TEXT)
用户资源表(user id)：source id(INT),source name(TEXT),source location(TEXT),source size(MB)(FLOAT)
-->登录：从数据库中查询是否有用户
-->注册：插入用户和密码，创建用户信息，创建用户资源表
"""


class BaseConfig:
    class Mysql:
        Host = "180.76.162.227"
        User = "root"
        Password = "123456"
        Port = 23306
        mainDatabase = "origin"  # 存储所有信息的database

        class SettledTable:
            allAttribute = {  # 注册所有的属性及类型
                "UserID": "INT UNSIGNED AUTO_INCREMENT",
                "Name": "VARCHAR(30)",
                "Password": "VARCHAR(30)",
                "RegisterTime": "DATETIME",
                "BriefDescription": "VARCHAR(200)",
                "SourceID": "INT UNSIGNED AUTO_INCREMENT",
                "SourceName": "VARCHAR(100)",
                "SourceLocation": "VARCHAR(100)",
                "SourceSize": "FLOAT",
                "SourceIntroduction": "TEXT",
                "SourceUploadTime": "DATETIME"
            }
            UserLoginTable = [  # 用户登录表
                "UserID",
                "Name",
                "Password"
            ]
            UserLoginTablePrimaryKey = "UserID"
            UserLoginTableInMysql = "client"  # 用户登录表在mysql中的表名
            UserInfoTable = [  # 用户信息
                "UserID",
                "RegisterTime",
                "BriefDescription",
            ]
            UserInfoTablePrimaryKey = "UserID"
            UserInfoTableInMysql = "clientInfo"  # 用户信息表在mysql中的表名
            UserSourceTable = [  # 用户资源表
                "SourceID",
            ]
            UserSourceTablePrimaryKey = "SourceID"
            UserSourceTableInMysql = "user{}SourceInfo"  # 用户资源表在mysql中的表名
            AllSourceTable = [  # 资源汇总表
                "SourceID",
                "SourceName",
                "SourceLocation",
                "SourceSize",
                "SourceIntroduction",
                "SourceUploadTime",
            ]
            AllSourceTablePrimaryKey = "SourceID"
            AllSourceTableInMysql = "allSource"  # 资源汇总表在mysql中的表名


BC = BaseConfig()
