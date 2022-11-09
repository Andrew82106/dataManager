from flask import Flask, render_template
import utils.ConfigLocation as ConfigLoc
import os

app = Flask(__name__)  # 开头必写，创建一个Flask对象从而进行后续操作
app.config["SECRET_KEY"] = "ABCDFWA"  # 为防CSRF提供一个密匙


@app.route('/mainview')
def hello_world():  # 这是视图函数
    return render_template("dashboard.html")


@app.route('/')
def login():
    return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True,port=1000,host='0.0.0.0')
