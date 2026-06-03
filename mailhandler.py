import gmail

mail_id=''   #your gmil id 
app_pwd=''   # app pass of gmail id 

def send_openacn_email(to,name,acn,pwd):
    con=gmail.GMail(mail_id,app_pwd)
    text=f'''Hello,{name},
we have successfully opened your account with following credentails
Account No={acn}
Passwor{pwd}

kindely change your password on first login

Thanks
ABC Bank
Delhi
'''
    msg=gmail.message(to=to ,text=text,subject='Account Opened')
    con.send(msg)

def send_closeacn_email(to,name,otp,adhar):
    con=gmail.GMail(mail_id,app_pwd)
    text=f'''Hello,{name},
Your OTP for closing Account is ={otp},
adhar={adhar}

Kindly share with Bank Admin

Do not share this OTP with anyone ?

Thanks
ABC Bank
Noida
'''
    msg=gmail.Message(to=to,text=text,subject='Account Closing OTP')
    con.send(msg)   