# Import important modules
from urllib import response
from flask import *
from flask.templating import render_template_string
from pymongo import MongoClient
import random
from function import send_sms
from datetime import date


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
        self.display_content=None
    def save(self,username):
        self.head_username=username
    def saveBlog(self,title):
        self.display_content=title
    
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


@app.route('/content/<content>')
def success(content):
    data=blogs.find_one({'title':content})
    global_cred_var.saveBlog(content)
    path=data['path']
    file=open(path,'r')
    content_file=file.read()
    return render_template('display.html',title=data['title'],final_cnt=content_file,username=global_cred_var.head_username)

@app.route('/submit',methods=['GET','POST'])
@app.route('/create_blog',methods=['GET','POST'])
def create_blog():
    ret=None
    if request.method=='POST':
        title=request.form.get('title')
        content_file=request.form.get('full_content')
        num=random.randint(10000,99999)
        prefix=random.choice(['algorithm','ai','c','c++','ds','java','ml','python','quantum'])
        if prefix=='algorithm':
            filename="blogs\\algorithms\\"+prefix+str(num)+".txt"
        if prefix=='ai':
            filename="blogs\\artificial_intelligence\\"+prefix+str(num)+".txt"
        if prefix=='c':
            filename="blogs\\c\\"+prefix+str(num)+".txt"
        if prefix=='c++':
            filename="blogs\\c++\\"+prefix+str(num)+".txt"
        if prefix=='ds':
            filename="blogs\\data_structure\\"+prefix+str(num)+".txt"
        if prefix=='java':
            filename="blogs\\java\\"+prefix+str(num)+".txt"
        if prefix=='ml':
            filename="blogs\\machine_learning\\"+prefix+str(num)+".txt"
        if prefix=='python':
            filename="blogs\\python\\"+prefix+str(num)+".txt"
        if prefix=='quantum':
            filename="blogs\\quantum_computing\\"+prefix+str(num)+".txt"
        file_to_write=open(filename,'w')
        file_to_write.write(content_file)
        file_to_write.close()
        data={'blogid':prefix+str(num),'title':title,'path':".\\"+filename,'rating':"5",'like':"1",'dislikes':"1",'types':filename.split("\\")[1],'by':global_cred_var.head_username,'on':str(date.today())}
        blogs.insert_one(data)
        ret="1"
        print(global_cred_var.head_username)
        print(user_record.find_one({'username':global_cred_var.head_username.lower()}))
        user_record.find_one_and_update({'username':global_cred_var.head_username.lower()},{'$inc':{'no_of_publication':1}})
        
    return render_template('create.html',response=ret)


############################### home page option ############################################### 
@app.route('/dashboard')
def dashboard():
    a=list(user_record.find({'username':global_cred_var.head_username.lower()}))[0]
    return render_template('dashboard.html',fn=a['fname'],ln=a['lname'],email=a['email'],github=a['github'],linkedin=a['linkedin'],dob=a['dob'],nop=a['no_of_publication'])

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/logout')
def logout():
    global_cred_var.head_username=None
    return redirect('/login')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/reset_password')
def reset_password():

    return render_template('otp.html')
    
############################### home page option done ###############################################


################################ Current working routing ###############################################

@app.route('/sendotp',methods=['GET','POST'])
def sendotp():
    if request.method=='POST':
        username=request.form.get('username')
        username=username.lower()
        global_cred_var.save(username)
        otp_record.insert_one({'username':username,'otp':random.randint(100000,999999)})
        return render_template('otp.html',username=username)

@app.route('/like')
def like():
    blogs.find_one_and_update({'title':global_cred_var.display_content},{'$inc':{'like':1}})
    return redirect('/content/'+global_cred_var.display_content)
    
@app.route('/dislike')
def dislike():
    blogs.find_one_and_update({'title':global_cred_var.display_content},{'$inc':{'dislikes':1}})
    return redirect('/content/'+global_cred_var.display_content)


#######################################################################################################


###################### Routing Pages End ########################### 




#################### Main Function ###################################
if __name__=='__main__':
    app.run(debug=True)

#################### End Function ###################################