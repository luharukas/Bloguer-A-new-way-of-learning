# Import important modules
from flask import Flask,render_template,request
import os
from flask.templating import render_template_string
from pymongo import MongoClient
app=Flask(__name__)

###################Database connection ######################
client=MongoClient("mongodb+srv://luharukas:Qwerasdf@authentication.k68mm.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db=client.get_database('Bloguer')
#login_record=db.Login

#################################################################

#################### Routing pages ##############################
@app.route('/',methods=['GET','POST'])
def login():
    return render_template("login.html")


@app.route('/login',methods=['GET','POST'])
def login2():
    return render_template('login.html')


@app.route('/signup',methods=['GET','POST'])
def signup():
    return render_template('signup.html')


@app.route('/signupdesc',methods=['GET','POST'])
def signupdesc():
    if request.method=="POST":
        signup_username=request.form.get('signup_username')
        signup_password=request.form.get('signup_password')
        signup_re_enter_password=request.form.get('signup_re_enter_password')
        print(signup_username,signup_password,signup_re_enter_password)
    return render_template('signupdesc.html')


@app.route('/home',methods=['GET','POST'])
def home():
    if request.method=='POST':
        login_username=request.form.get('login_username')
        login_password=request.form.get('login_password')
        print(login_username,login_password)
    return render_template('home.html')


@app.route('/password_reset',methods=['GET','POST'])
def reset():
    return render_template_string("Page under Development")

###################### Routing Pages End ########################### 


#################### Main Function ###################################
if __name__=='__main__':
    app.run(debug=True)

#################### End Function ###################################