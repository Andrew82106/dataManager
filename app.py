from flask import Flask, render_template, url_for, redirect, flash, session, send_from_directory
from flask_wtf.form import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo, DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed
from utils.DB import DB
from utils.ConfigLocation import ConfiglocalSources
import os
db = DB()
app = Flask(__name__)  # 开头必写，创建一个Flask对象从而进行后续操作
app.config["SECRET_KEY"] = "ABCDsdfcmndqidadFWA"  # 为防CSRF提供一个密匙


class LoginForm(FlaskForm):
    UserName = StringField("用户名", validators=[InputRequired(message="需要一个用户名捏"),
                                                 Length(min=3, max=20, message="输入长度不合法")])
    PassWord = PasswordField("用户密码", validators=[InputRequired(message="没密码咋行"),
                                                     Length(min=6, max=20, message="输入长度不合法")])
    SubmitButton = SubmitField("提交")


class RegisterForm(FlaskForm):
    UserName1 = StringField(u"用户名", validators=[DataRequired(),
                                                   Length(min=3, max=20)])
    PassWord1 = PasswordField(u"用户密码", validators=[DataRequired(),
                                                       Length(min=6, max=20)])
    PassWordConfirm1 = PasswordField(u"用户密码确认", validators=[DataRequired(),
                                                                  Length(min=6, max=20),
                                                                  EqualTo("PassWord1")])
    SubmitButton1 = SubmitField(u"提交")


class UploadData(FlaskForm):
    photo = FileField('Upload Image', validators=[FileRequired(), FileAllowed(['xls', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'gif', 'zip', '7z', 'pdf', 'xlsx', 'rar'])])
    fileName = StringField("资源名", validators=[DataRequired(),
                                                   Length(min=3, max=20)])
    submit = SubmitField()


@app.route('/mainview/', methods=['GET', 'POST'])
def hello_world():  # 这是视图函数
    Up = UploadData()
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
    if Up.validate_on_submit():
        f = Up.photo.data
        filename = Up.fileName.data
        f.save(os.path.join(ConfiglocalSources(), f.filename))
        SIZE = os.path.getsize(os.path.join(ConfiglocalSources(), f.filename))
        db.UploadResource(filename, "::{}".format(f.filename), SIZE/(1024*1024), UserName)
        return redirect(url_for("hello_world"))
    return render_template("dashboard.html", UserName=UserName, RegisterTime=RegisterTime, BriefDescription=BriefDesc,
                           NumOfSources=len(UserSourceList), SourceDetails=SourceDetails, Up=Up)


@app.route('/download/<FileName>', methods=['GET', 'POST'])
def Download(FileName: str):
    return send_from_directory(ConfiglocalSources(), FileName.replace("::", ""), as_attachment=True)


@app.route('/', methods=['GET', 'POST'])
def login():
    db.reConnect()
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
                print("Login Failed")
                flash("密码错误")
                return redirect(url_for("login"))
        except Exception as e:
            print(e)
            flash("用户名错误")
            return redirect(url_for("login"))
    return render_template("login.html", form=Form)


@app.route('/logout', methods=['POST', 'GET'])
def Out():
    session.clear()
    return redirect(url_for("login"))


@app.route('/register', methods=['POST', 'GET'])
def Register():
    Form = RegisterForm()
    print("INFUN")
    print(Form.errors)
    if Form.is_submitted():
        if not Form.validate() or Form.UserName1.data in db.QueryAllUser():
            if Form.PassWord1.data != Form.PassWordConfirm1.data:
                flash("两次密码不一致")
                return redirect(url_for("Register"))
            UserName = Form.UserName1.data
            Password = Form.PassWord1.data
            if db.AddUser(UserName, Password) == 0:
                flash("已存在用户")
                return redirect(url_for("Register"))
            else:
                print("注册成功")
                return redirect(url_for("login"))
        UserName = Form.UserName1.data
        Password = Form.PassWord1.data
        db.AddUser(UserName, Password)
        print("注册成功")
        return redirect(url_for("login"))
    return render_template("register.html", Form=Form)


if __name__ == '__main__':
    app.run(debug=True, port=1000, host='0.0.0.0')
