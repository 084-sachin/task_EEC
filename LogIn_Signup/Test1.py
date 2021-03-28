from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/database'
db = SQLAlchemy(app)

app.config.update(DEBUG=True, MAIL_SERVER='smtp.gmail.com', MAIL_PORT=465, MAIL_USE_SSL=True, MAIL_USERNAME= '',MAIL_PASSWORD = '')

mail = Mail(app)
mydb = mysql.connector.connect(host="localhost", user="root", database="database")

class userdetails(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    emailid = db.Column(db.String(100))
    password = db.Column(db.String(100))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup")
def index1():
    return render_template("signup.html")

@app.route("/adduser",methods=["post"])
def adduser():
    username = request.form.get("username")
    email = request.form.get("email")
    contact = request.form.get("contact")
    password = request.form.get("password")
    #print(username, email, contact, password)
    admin = userdetails(username=username, emailid=email, password=password)
    db.session.add(admin)
    db.session.commit()
    msg = Message("Send Mail Tutorial!", sender="", recipients=[email])
    msg.body = "Verify This Email by clicking on this link"
    msg.html=render_template("email.html",msg=email)
    mail.send(msg)


    return render_template("pop.html")

@app.route("/login", methods=["post"])
def login():
    email=request.form.get("email")
    password=request.form.get("password")
    mycursor=mydb.cursor()
    sql="select * from userdetails where emailid='"+email+"'"
    mydata=mycursor.execute(sql)
    data=mycursor.fetchone()
    if data is not None:
        if (data[2] == email):
            if (data[3] == password):
                if(data[4]==1):
                    return render_template("pop1.html")
                else:
                    return render_template("pop4.html")
            else:
                return render_template("index.html", error="incorrect password")
        else:
            return render_template("index.html", error="you are not a registered user")
    else:
        return render_template("index.html", error="you are not a registered user")

@app.route("/verifyEmail", methods=["post"])
def verifyEmail():
    email=request.form.get("email")
    mycursor=mydb.cursor()
    sql="update userdetails set isVerify=1 where emailid='"+email+"'"
    mycursor.execute(sql)
    mydb.commit()
    return render_template("pop.html")

@app.route("/forgotpassword")
def forgotpassword():
    return render_template("forgotpassword.html")

@app.route("/resetpassword", methods=["post"])
def resetpassword():
    email = request.form.get("email")
    mycursor = mydb.cursor()
    sql = "select * from userdetails where emailid='"+email+"'"
    mydata = mycursor.execute(sql)
    data = mycursor.fetchone()
    msg = Message("Send Mail Tutorial!", sender="sachinlalwani1234@gmail.com", recipients=[email])
    msg.body = "Change Your Password"
    msg.html = render_template("resetpassword.html", msg=email)
    if data is not None:
        mail.send(msg)
        return render_template("pop2.html")
    else:
        return render_template("pop3.html")

app.run()


