import smtplib
import random

def send_sms(otp,receiver):
    sender = 'luharukashubham4@gmail.com'
    message = "I heared that you forget your password. Don't worry use {} to reset your password".format(otp)
    print(message)
    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com',587)
        smtpObj.starttls()
        smtpObj.login(sender,"Luharukas@123")
        smtpObj.sendmail(sender, receiver, message)   
        smtpObj.quit()    
        return True
    except:
        return False
