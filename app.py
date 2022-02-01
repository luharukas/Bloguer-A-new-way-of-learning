# Import important modules
from flask import *
from flask.templating import render_template_string
from pymongo import MongoClient
import random
from function import send_sms



app=Flask(__name__)

###################Database connection ######################
client=MongoClient("mongodb+srv://luharukas:Qwerasdf@authentication.k68mm.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db=client.get_database('Bloguer')
login_record=db.Login
user_record=db.User
otp_record=db.Otp
preferences=db.Interested_topic
blogs=db.blogs

#################################################################

#################### Routing pages ##############################
class global_cred:
    def __init__(self) -> None:
        self.head_username=None
    def save(self,username):
        self.head_username=username
    
global_cred_var=global_cred()


        
@app.route('/')
@app.route('/login')
def login():
    return render_template("login.html",username=global_cred_var.head_username)


@app.route('/validation', methods=['GET','POST'])
def validation():
    if request.method=='POST':
        login_username=request.form.get('login_username')
        login_password=request.form.get('login_password')

        global_cred_var.save(login_username)

        login_username=login_username.lower()
        details=login_record.find_one({'username':login_username})
        if details==None:
            login_msg="Username not found"
        else:
            if login_password==details['password']:
                return redirect('/home')
            else:
                login_msg="Password is incorrect"

    return render_template('login.html',value=login_msg,username=global_cred_var.head_username)

@app.route('/home')
def home():
    if global_cred_var.head_username:
        pref_list=list(preferences.find({'username':global_cred_var.head_username.lower()}))
        print(pref_list)
        pref_list=[x['preference'] for x in pref_list]
        print(pref_list)
        arr=[]
        for x in blogs.find():
            if x['types'] in set(pref_list):
                arr.append(x)
        print(arr)
        
        return render_template('home.html',username=global_cred_var.head_username.upper(), data=arr)
    else:
        return redirect('/login')


@app.route('/reset_password')
def reset_password():
    pass
            

@app.route('/complete_reset',methods=['GET','POST'])
def complete_reset():
    pass




@app.route('/signupdesc',methods=['GET','POST'])
def signupdesc():
    if request.method=="POST":
        signup_username=request.form.get('signup_username').lower()
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
        desc_preferred_topic=request.form.getlist('preferred_topic')
        desc_github=request.form.get('github')
        desc_linkedin=request.form.get('linkedin')
        desc_dob_month=request.form.get('month')
        desc_dob_day=request.form.get('day')
        desc_dob_year=request.form.get('year')
        desc_gender=request.form.get('gender')
        
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
            for i in desc_preferred_topic:
                preferences.insert_one({'username':global_cred_var.head_username,'preference':i})

            return render_template('login.html',username=global_cred_var.head_username)

    return render_template_string(ret_msg)

############################### home page option ############################################### 
@app.route('/dashboard')
def dashboard():
    a=list(user_record.find({'username':global_cred_var.head_username.lower()}))[0]
    return render_template('dashboard.html',fn=a['fname'],ln=a['lname'],email=a['email'],github=a['github'],linkedin=a['linkedin'],dob=a['dob'],)

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/logout')
def logout():
    global_cred_var.head_username=None
    return redirect('/login')

############################### home page option done ###############################################

###################### Routing Pages End ########################### 




























































































































#################### Main Function ###################################
if __name__=='__main__':
    app.run(debug=True)

#################### End Function ###################################