from flask import Flask, render_template, url_for, redirect, flash, session
from flask_wtf.form import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length
from utils.DB import DB

db = DB()
app = Flask(__name__)  # 开头必写，创建一个Flask对象从而进行后续操作
app.config["SECRET_KEY"] = "ABCDsdfcmndqidadFWA"  # 为防CSRF提供一个密匙


class LoginForm(FlaskForm):
    UserName = StringField("用户名", validators=[InputRequired(message="需要一个用户名捏"),
                                                 Length(min=3, max=20, message="输入长度不合法")])
    PassWord = PasswordField("用户密码", validators=[InputRequired(message="没密码咋行"),
                                                     Length(min=6, max=20, message="输入长度不合法")])
    SubmitButton = SubmitField("提交")


@app.route('/mainview/')
def hello_world():  # 这是视图函数
    UserName = session.get("UserName")
    if UserName is None:
        return redirect(url_for("login"))
    RegisterTime, BriefDesc = db.QueryUserInfo(UserName)
    UserSourceList = db.QueryUserResources(UserName)
    # UserSourceList:((1,),(2,),(3,),(4,),(5,)...)
    SourceDetails = []
    for ID in UserSourceList:
        Detail = db.QueryResourcesByID(ID[0])[0]
        SourceDetails.append([Detail[0], Detail[1], Detail[2], Detail[3], Detail[4], Detail[5]])
    return render_template("dashboard.html", UserName=UserName, RegisterTime=RegisterTime, BriefDescription=BriefDesc,
                           NumOfSources=len(UserSourceList), SourceDetails=SourceDetails)


@app.route('/', methods=["GET", "POST"])
def login():
    Form = LoginForm()
    if Form.validate_on_submit():
        Name = Form.UserName.data
        Pas = Form.PassWord.data
        print(Name)
        print(Pas)
        try:
            x = db.QueryUserPas(Name)
            if x == Pas:
                print("Login Success")
                session['UserName'] = Name
                return redirect(url_for("hello_world", UserName=Name))
            else:
                flash("密码错误")
                print("Login Failed")
                return redirect(url_for("login"))
        except Exception as e:
            flash("用户名错误")
            print(e)
            return redirect(url_for("login"))
    return render_template("login.html", form=Form)


@app.route('/logout', methods=['POST', 'GET'])
def Out():
    session.clear()
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True, port=1000, host='0.0.0.0')
