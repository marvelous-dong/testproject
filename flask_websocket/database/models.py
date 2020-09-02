from database.exts import db


# 用户表
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, doc="序号")
    username = db.Column(db.String(100), doc="用户名")
    password = db.Column(db.String(50), doc="密码")


class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True, doc="序号")
    c_name = db.Column(db.String(100), doc="班级名称")