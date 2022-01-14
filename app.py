# Import important modules
from datetime import date
from flask import Flask,render_template,request
import os
from flask.templating import render_template_string
from pymongo import MongoClient
import re
app=Flask(__name__)

###################Database connection ######################
client=MongoClient("mongodb+srv://luharukas:Qwerasdf@authentication.k68mm.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db=client.get_database('Bloguer')
login_record=db.Login
user_record=db.User

#################################################################

#################### Routing pages ##############################
class global_cred:
    def __init__(self) -> None:
        self.head_username=None
    def save(self,username):
        self.head_username=username
    
global_cred_var=global_cred()
        
@app.route('/')
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
        details=login_record.find_one({'username':signup_username})
        if details!=None:
            ret_msg="Username Exist"
        elif len(signup_password)>16 or len(signup_password)<8:
            ret_msg="Password length should be between 8 to 16"
        else:
            login_record.insert_one({'username':signup_username,'password':signup_password})
            global_cred_var.save(signup_username)
            return render_template("signupdesc.html")
    return render_template("signup.html",value=ret_msg,un=signup_username,pd=signup_password)

@app.route('/signing',methods=['GET','POST'])
def signing():
    if request.method=='POST':
        desc_firstname=request.form.get('firstname')
        desc_lastname=request.form.get('lastname')
        desc_email=request.form.get('email')
        desc_phone_no=request.form.get('phone_no')
        desc_organization=request.form.get('organization')
        desc_preferred_topic=request.form.get('preferred_topic')
        desc_github=request.form.get('github')
        desc_linkedin=request.form.get('linkedin')
        desc_dob_month=request.form.get('month')
        desc_dob_day=request.form.get('day')
        desc_dob_year=request.form.get('year')
        desc_gender=request.form.get('gender')
        print(desc_preferred_topic)
        print(type(desc_preferred_topic))
        
        if len(str(desc_phone_no)) not in [10,12]:
            ret_msg="Invalid Phone no"
        else:
            desc_github=desc_github.split("/")[-1]
            desc_linkedin=desc_linkedin.split("/")[-2]
            
            desc_dob=desc_dob_day+"-"+desc_dob_month+"-"+desc_dob_year
            info_dict={'username':global_cred_var.head_username,
                    'fname':desc_firstname,
                    'lname':desc_lastname,
                    'email':desc_email,
                    'phone_no':desc_phone_no,
                    'organization': desc_organization,
                    'github':desc_github,
                    'linkedin':desc_linkedin,
                    'dob':desc_dob,
                    'gender':desc_gender
            }
            user_record.insert_one(info_dict)
            return render_template('home.html',value=global_cred_var.head_username)

    return render_template_string(ret_msg)


@app.route('/home',methods=['GET','POST'])
def home():
    if request.method=='POST':
        login_username=request.form.get('login_username')
        login_password=request.form.get('login_password')
        login_username=login_username.lower()
        details=login_record.find_one({'username':login_username})
        if details==None:
            login_msg="Username not found"
        else:
            if login_password==details['password']:
                global_cred_var.save(login_username)
                return render_template('home.html')
            else:
                login_msg="Password is incorrect"

    return render_template('login.html',value=login_msg)

@app.route('/password_reset',methods=['GET','POST'])
def reset():
    return render_template_string("Page under Development")

###################### Routing Pages End ########################### 


#################### Main Function ###################################
if __name__=='__main__':
    app.run(debug=True)

#################### End Function ###################################