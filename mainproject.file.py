from tkinter import Tk,Label,Frame,Entry,Button,messagebox,simpledialog,filedialog
from tkinter.ttk import Combobox
import random
import mygenerator
import dbhandler
import mailhandler
import time 
import sqlite3
from PIL import Image,ImageTk
import shutil
import os
import re

def update_time():
    t=time.strftime("%A ,%b %d %y ⏰%r")
    lbl_dt.configure(text=t)
    lbl_dt.after(1000,update_time)


def customer_screen():
    frm=Frame(root,highlightbackground='black',highlightthickness=2) 
    frm.configure(bg='Ghost White')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.8)     
    
    def logout_click():
         frm.destroy()
         main_screen()
    
    def viewdetails_screen():   

         ifrm=Frame(frm,highlightbackground='black',highlightthickness=2) 
         ifrm.configure(bg='light Blue')
         ifrm.place(relx=.2,rely=.20,relwidth=.75,relheight=.75)  

         lbl_ftitle=Label(ifrm,text="[This is view details screen]",
                  font=('poppins',20,'bold'),bg='light Blue',fg='purple')
         lbl_ftitle.pack()

         conobj=sqlite3.connect(database='bank.sqlite')
         curobj=conobj.cursor()
         query='select*from users where acn=?'
         curobj.execute(query,(user_acn,))
         row=curobj.fetchone()
         conobj.close()
         details=f'''Name={row[1]}
         ACN={row[0]}
         bal={row[7]}
         adhar={row[6]}
         adhar={row[5]}

         open date={row[9]}'''

         lbl_details=Label(ifrm,text=details,
                  font=('poppins',20,'bold'),bg='light Blue',fg='black')
         lbl_details.place(x=160,y=100)
    
    def updatedetails_screen():  
     
         ifrm=Frame(frm,highlightbackground='black',highlightthickness=2) 
         ifrm.configure(bg='light blue')
         ifrm.place(relx=.2,rely=.20,relwidth=.75,relheight=.75) 

         def  up_details():
              name=e_name.get()
              pwd=e_pass.get()
              email=e_email.get()
              mob=e_mob.get()

              conobj=sqlite3.connect(database='bank.sqlite')
              curobj=conobj.cursor() 
              query='update users set name=?,pass=?,email=?,mob=? where acn=?'
              curobj.execute(query,(name,pwd,email,mob,user_acn,))
              conobj.commit()  
              #conobj.close()
              messagebox.showinfo("Update","Details Updated") 
              customer_screen()
              conobj.close()

         lbl_ftitle=Label(ifrm,text="[This is update details screen]",
                  font=('poppins',20,'bold'),bg='light Blue',fg='purple')
         lbl_ftitle.pack()

         lbl_name=Label(ifrm,text="Name",
                  font=('poppins',20,),bg='light Blue')
         lbl_name.place(relx=.15,rely=.07)

         e_name=Entry(ifrm,font=('poppins',20,'bold'),bd=6)
         e_name.place(relx=.15,rely=.17)
        
         lbl_email=Label(ifrm,text="Email",
                  font=('poppins',20,),bg='light Blue')
         lbl_email.place(relx=.15,rely=.34)

         e_email=Entry(ifrm,font=('poppins',20,'bold'),bd=6)
         e_email.place(relx=.15,rely=.44)

         lbl_mob=Label(ifrm,text="Mobile ",
                  font=('poppins',20,),bg='light Blue')
         lbl_mob.place(relx=.5,rely=.10)

         e_mob=Entry(ifrm,font=('poppins',20,'bold'),bd=6)
         e_mob.place(relx=.5,rely=.20)

         lbl_pass=Label(ifrm,text="pass",
                  font=('poppins',20,),bg='light Blue')
         lbl_pass.place(relx=.5,rely=.34)

         e_pass=Entry(ifrm,font=('poppins',20,'bold'),bd=6)
         e_pass.place(relx=.5,rely=.44)

         up_btn= Button (frm,text='Update Details',bd=5,
                    font=('poppins',12,'bold'),width=16,bg='grey',command=up_details)
         up_btn.place(relx=.5,rely=.7)

         conobj=sqlite3.connect(database='bank.sqlite')
         curobj=conobj.cursor() 
         query='select name ,pass,email,mob from  users where acn=?'
         curobj.execute(query,(user_acn,))
         tup=curobj.fetchone()
         conobj.close()

         e_name.insert(0,tup[0])
         e_pass.insert(0,tup[1])
         e_email.insert(0,tup[2])
         e_mob.insert(0,tup[3])



    def deposit_screen():  
     
         ifrm=Frame(frm,highlightbackground='black',highlightthickness=2) 
         ifrm.configure(bg='light Blue')
         ifrm.place(relx=.2,rely=.20,relwidth=.75,relheight=.75)  

         lbl_ftitle=Label(ifrm,text="[This is deposit details screen]",
                  font=('poppins',20,'bold'),bg='light Blue',fg='purple')
         lbl_ftitle.pack()

         amt=simpledialog.askfloat("Deposit Amount","Enter Amount")
         if amt==None:
              return
         conobj=sqlite3.connect(database='bank.sqlite')
         curobj=conobj.cursor() 
         query='update users set bal=bal+? where acn=?'
         curobj.execute(query,(amt,user_acn,))
         conobj.commit()  
         conobj.close()
         messagebox.showinfo("Deposit","Amount Deposited")

    def withdraw_screen():  
     
         ifrm=Frame(frm,highlightbackground='black',highlightthickness=2) 
         ifrm.configure(bg='light Blue')
         ifrm.place(relx=.2,rely=.20,relwidth=.75,relheight=.75)  

         lbl_ftitle=Label(ifrm,text="[This is withdraw screen]",
                  font=('poppins',20,'bold'),bg='light Blue',fg='purple')
         lbl_ftitle.pack()

         amt=simpledialog.askfloat("Withdraw Amount","Enter Amount")
         if amt==None:
              return
         conobj=sqlite3.connect(database='bank.sqlite')
         curobj=conobj.cursor() 
         query='select bal from  users where acn=?'
         curobj.execute(query,(user_acn,))
         bal=curobj.fetchone()[0]
         conobj.close()

         if amt>bal:
              messagebox.showerror("Withdraw","Insufficient Bal")
              return

         conobj=sqlite3.connect(database='bank.sqlite')
         curobj=conobj.cursor() 
         query='update users set bal=bal-? where acn=?'
         curobj.execute(query,(amt,user_acn,))
         conobj.commit()  
         conobj.close()
         messagebox.showinfo("Withdraw","Amount Withdraw")
     

    def transfer_screen():  
     
         ifrm=Frame(frm,highlightbackground='black',highlightthickness=2) 
         ifrm.configure(bg='light Blue')
         ifrm.place(relx=.2,rely=.20,relwidth=.75,relheight=.75)  

         lbl_ftitle=Label(ifrm,text="[This is Transfer screen]",
                  font=('poppins',20,'bold'),bg='light Blue',fg='purple')
         lbl_ftitle.pack()  

         to_acn=simpledialog.askinteger("Transfer Amount","Enter To ACN")
         if to_acn==None:
                  return
         conobj=sqlite3.connect(database='bank.sqlite')
         curobj=conobj.cursor() 
         query='select * from  users where acn=?'
         curobj.execute(query,(to_acn,))
         row=curobj.fetchone()
         conobj.close()
         if row==None:
              messagebox.showerror("Transfer Amount","To ACN does not exist")
              return
         
         amt=simpledialog.askfloat("Withdraw Amount","Enter Amount")
         if amt==None:
            return
         conobj=sqlite3.connect(database='bank.sqlite') 
         curobj=conobj.cursor() 
         query='select bal from  users where acn=?'
         curobj.execute(query,(user_acn,))
         bal=curobj.fetchone()[0]
         conobj.close()

         if amt>bal:
              messagebox.showerror("Transfer Amount","Insufficient Bal")
              return

         conobj=sqlite3.connect(database='bank.sqlite')
         curobj=conobj.cursor() 
         query1='update users set bal=bal-? where acn=?'
         query2='update users set bal=bal+? where acn=?'

         curobj.execute(query1,(amt,user_acn))
         curobj.execute(query2,(amt,to_acn))

         conobj.commit()  
         conobj.close()
         messagebox.showinfo("Transfer Amount",f"{amt}Amount Transfered to ACN{to_acn} from ACN{user_acn}")


    def dp():
          filepath=filedialog.askopenfilename(filetypes=[('Image Files','*.jpg *.png *.jpeg')])       
          shutil.copy(filepath,f'{user_acn}.jpg')

          img1=Image.open(f'{user_acn}.jpg').resize((100,80))          # logo(image)
          imgtk=ImageTk.PhotoImage(img1,master=root)

          dp_lbl=Label(frm,image=imgtk)
          dp_lbl.image=imgtk
          dp_lbl.place(relx=.05, rely=0.05)

    
    logout_btn= Button (frm,text='logout',bd=5,
                    font=('poppins',12,'bold'),width=8,bg='light blue',command=logout_click)
    logout_btn.place(relx=.92,rely=0)

    conobj=sqlite3.connect(database='bank.sqlite')
    curobj=conobj.cursor() 
    query='select  name from users where acn =?'
    curobj.execute(query,user_acn,)
    name=curobj.fetchone()[0]   
    conobj.close()


    lbl_wel=Label(frm,text=f"Welcome,{name}",
                  font=('poppins',12,'bold'),bg='light blue')
    lbl_wel.place(relx=0,rely=0) 

    if os.path.exists(f'{user_acn}.jpg') :
         filepath=f'{user_acn}.jpg'
    else:
         filepath='default.jpg'
     
         

    img=Image.open("Default image1.jpg").resize((100,80))
    imagetk=ImageTk.PhotoImage(img,master=root)
    dp_lbl=Label(frm,image=imgtk)
    dp_lbl.image=imgtk
    dp_lbl.place(relx=.05, rely=0.05,relheight=.15)

    updatedp_btn= Button (frm,text='Update DP',bd=5,
                    font=('poppins',8,'bold'),bg='red',fg='White',width=15,command=dp)
    updatedp_btn.place(relx=.06,rely=.22)


    view_btn= Button (frm,text='View Details',bd=10,
                    font=('poppins',16,'bold'),bg='Deep Sky Blue',width=14,command=viewdetails_screen)
    view_btn.place(relx=0,rely=.30)

    update_btn= Button (frm,text='Update Details',bd=10,
                    font=('poppins',16,'bold'),bg='Deep Sky Blue',width=14,command=updatedetails_screen)
    update_btn.place(relx=0,rely=.45)

    deposit_btn= Button (frm,text='Deposite Details',bd=10,
                    font=('poppins',16,'bold'),bg='Deep Sky blue',width=14,command=deposit_screen)
    deposit_btn.place(relx=0,rely=.60)
     
    
    withdraw_btn= Button (frm,text='Withdraw Details',bd=10,
                    font=('poppins',16,'bold'),bg='Deep Sky blue',width=14,command=withdraw_screen)
    withdraw_btn.place(relx=0,rely=.77) 

    transfer_btn= Button (frm,text='Transfer Details',bd=10,
                    font=('poppins',16,'bold'),bg='Deep Sky blue',width=14,command=transfer_screen)
    transfer_btn.place(relx=0,rely=.90) 


def admin_screen():
    frm=Frame(root,highlightbackground='black',highlightthickness=2) 
    frm.configure(bg='Ghost White')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.8)     
    
    def logout_click():
         frm.destroy()
         main_screen()

    def openacn_screen():
         ifrm=Frame(frm,highlightbackground='black',highlightthickness=2) 
         ifrm.configure(bg='light blue')
         ifrm.place(relx=.1,rely=.25,relwidth=.80,relheight=.65)  
     
         def create_account():
              name=e_name.get()
              email=e_email.get()
              adhar=e_adhar.get()
              mob=e_mob.get()
              age=e_age.get()
              gender=cb_gender.get()

              if len(name)==0:
                   messagebox.showerror("Open Account","name is required")
              match_name = re.fullmatch(r"[a-zA-Z ]{3,50}", name)
              if match_name == None:
                   messagebox.showerror("Open Account", "Invalid Name (letters only, 3-50 characters)")
                   return         

              if len(email)==0:
                   messagebox.showerror("Open Account","email is required") 
              #match=re.fullmatch(r"[a-zA-Z0-9_.$]+@[a-zA-Z0-9]+/.[a-zA-Z]+",email)
              match_email = re.fullmatch(r"[a-zA-Z0-9._]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}", email)
              if match_email==None:
                   messagebox.showerror("Open Account ","Invalid Email")
                   return
              
              if len(adhar)==0:
                   messagebox.showerror("Open Account","adhar is required")
              match_adhar = re.fullmatch(r"[0-9]{12}", adhar)
              if match_adhar == None:
                  messagebox.showerror("Open Account", "Invalid Aadhar (must be 12 digits)")
                  return

              if len(mob)==0:
                   messagebox.showerror("Open Account","mob is required") 
              match_mob = re.fullmatch(r"[6-9][0-9]{9}", mob)
              if match_mob == None:
                  messagebox.showerror("Open Account", "Invalid Mobile (must be 10 digits, start with 6-9)")
                  return

              if len(age)==0:
                   messagebox.showerror("Open Account","age is required") 
              match_age = re.fullmatch(r"[0-9]{1,3}", age)
              if match_age == None:
                   messagebox.showerror("Open Account", "Invalid Age (numbers only)")
                   return
              if int(age) < 18 or int(age) > 100:
                   messagebox.showerror("Open Account", "Age must be between 18 and 100")
                   return
              
              bal=0
              opendate= time.strftime("%A,%b %d %y %r")
              pwd=mygenerator.generate_password()

              conobj=sqlite3.connect(database='bank.sqlite')
              curobj=conobj.cursor() 
              query='insert into users values(null,?,?,?,?,?,?,?,?,?)'
              curobj.execute(query,(name,pwd,email,mob,adhar,age,bal,gender,opendate))
              conobj.commit()
              conobj.close()
              
              #messagebox.showinfo("Opened Account")

              conobj=sqlite3.connect(database='bank.sqlite')
              curobj=conobj.cursor() 
              query='select max(acn) from users'
              curobj.execute(query)
              acn=curobj.fetchone()[0]
              conobj.close()

              mailhandler.send_openacn_email(email,name,acn,pwd)
              messagebox.showinfo("Create Account"," Account Opened and Credentials are sent to email")
         lbl_ftitle=Label(ifrm,text="This is open account screen",
                  font=('poppins',15),bg='light Blue',fg='purple')
         lbl_ftitle.pack()

         lbl_name=Label(ifrm,text="Name",
                  font=('poppins',20,),bg='light Blue')
         lbl_name.place(relx=.15,rely=.07)

         e_name=Entry(ifrm,font=('poppins',20,'bold'),bd=6)
         e_name.place(relx=.15,rely=.17)
        
         lbl_email=Label(ifrm,text="Email",
                  font=('poppins',20,),bg='light Blue')
         lbl_email.place(relx=.15,rely=.34)

         e_email=Entry(ifrm,font=('poppins',20,'bold'),bd=6)
         e_email.place(relx=.15,rely=.44)

         lbl_mob=Label(ifrm,text="Mobile ",
                  font=('poppins',20,),bg='light Blue')
         lbl_mob.place(relx=.15,rely=.59)

         e_mob=Entry(ifrm,font=('poppins',20,'bold'),bd=6)
         e_mob.place(relx=.15,rely=.69)

         lbl_adhar=Label(ifrm,text="adhar",
                  font=('poppins',20,),bg='light Blue')
         lbl_adhar.place(relx=.6,rely=.34)

         e_adhar=Entry(ifrm,font=('poppins',20,'bold'),bd=6)
         e_adhar.place(relx=.6,rely=.44)

         lbl_age=Label(ifrm,text="Age",
                  font=('poppins',20,),bg='light Blue')
         lbl_age.place(relx=.6,rely=.08)

         e_age=Entry(ifrm,font=('poppins',20,'bold'),bd=6)
         e_age.place(relx=.6,rely=.18)

         lbl_gender=Label(ifrm,text="Gender ",
                  font=('poppins',20,),bg='light Blue')
         lbl_gender.place(relx=.6,rely=.59)

         e_gender=Entry(ifrm,font=('poppins',20,'bold'),bd=6)
         e_gender.place(relx=.6,rely=.69)

         cb_gender= Combobox(ifrm,font=('poppins',18,),values=['Male','Female','Other'])
         cb_gender.current(0)
         cb_gender.place(relx=.6,rely=.69)

         reset_btn= Button (ifrm,text='Reset',bd=5,font=('poppins',12),bg='Deep Sky Blue')
         reset_btn.place(relx=.4,rely=.85)
         
         submit_btn= Button (ifrm,text= 'Submit',bd=5,font=('poppins',12),bg='Deep Sky Blue',command=create_account)
         submit_btn.place(relx=.6,rely=.85)


    def viewacn_screen():
         ifrm=Frame(frm,highlightbackground='black',highlightthickness=2) 
         ifrm.configure(bg='light blue')
         ifrm.place(relx=.1,rely=.25,relwidth=.80,relheight=.65)  
              
         def search():
              acn=int(e_acn.get())
              conobj=sqlite3.connect(database='bank.sqlite')
              curobj=conobj.cursor() 
              query='select name,bal,opendate,email,adhar from users where acn=?'
              curobj.execute(query,(acn,))
              row=curobj.fetchone()
              conobj.close()
              if row ==None:
                   messagebox.showerror("search","Account does not exist")
              else :
                   #messagebox.showinfo("search",row)
                   details=f'Name=  {row[0]}\nBal={row[1]}\nopendate={row[2]}\nemail={row[3]}\nadhar={row[4]}'
                   messagebox.showinfo("search",details)


         lbl_ftitle=Label(ifrm,text="This is view account screen",
                  font=('poppins',20,'bold'),bg='light Blue',fg='purple')
         lbl_ftitle.pack()

         lbl_acn=Label(ifrm,text="Account",
                  font=('poppins',20,),bg='light Blue')
         lbl_acn.place(relx=.2,rely=.2)

         e_acn=Entry(ifrm,font=('poppins',20,'bold'),bd=6)
         e_acn.place(relx=.35,rely=.2)

         search_btn= Button (ifrm,text='🔍Search',bd=5,font=('poppins',14,'bold'),bg='Deep Sky Blue',width=16,command=search)
         search_btn.place(relx=.70,rely=.2)


    def closeacn_screen():
         ifrm=Frame(frm,highlightbackground='black',highlightthickness=2) 
         ifrm.configure(bg='light blue')
         ifrm.place(relx=.1,rely=.25,relwidth=.80,relheight=.65)  
          
         def close ():
             acn=int(e_acn.get())

             conobj=sqlite3.connect(database='bank.sqlite')  
             curobj=conobj.cursor() 
             query='select name,email,adhar from users where acn=?'
             curobj.execute(query,(acn,))
             row=curobj.fetchone()
             conobj.close()

             if row==None :
                  messagebox.showerror("close Account","Account does not exist")
                  return

             else: 
                  gen_otp=random.randint(1000,9999)   
                  user_otp=simpledialog.askinteger("Close Account","Enter OTP sent to your Email")
                  if user_otp==gen_otp:
                      conobj=sqlite3.connect(database='bank.sqlite')  
                      curobj=conobj.cursor() 
                      query='delete from users where acn=?'
                      curobj.execute(query,(acn,))
                      conobj.commit()
                      conobj.close()
                      messagebox.showinfo("Close Account","Account Closed Successfully")
                      return
                  else:
                       messagebox.showerror("Close Account","Invalid OTP,Try Again")
         lbl_ftitle=Label(ifrm,text="This is close account screen",
                  font=('poppins',20),bg='light Blue',fg='purple')
         lbl_ftitle.pack()   
        
         lbl_acn=Label(ifrm,text="Account",
                  font=('poppins',20,),bg='light Blue')
         lbl_acn.place(relx=.2,rely=.2)

         e_acn=Entry(ifrm,font=('poppins',20,'bold'),bd=6)
         e_acn.place(relx=.35,rely=.2)

         close_btn= Button (ifrm,command=close ,text='Close',bd=5,font=('poppins',14,'bold'),bg='Deep Sky Blue',width=16)
         close_btn.place(relx=.70,rely=.2)

    logout_btn= Button (frm,text='logout',bd=10,
                    font=('poppins',12,'bold'),bg='red',width=16,command=logout_click)
    logout_btn.place(relx=.9,rely=0)

    lbl_wel=Label(frm,text="Click On One ➡",
                  font=('poppins',20,'bold'))
    lbl_wel.place(relx=0,rely=0)

    openacn_btn= Button (frm,text='Open Account',bd=10,
                    font=('poppins',12,'bold'),bg='Deep Sky Blue',width=14,command=openacn_screen)
    openacn_btn.place(relx=.1,rely=.08)

    viewacn_btn= Button (frm,text='View Account',bd=10,
                    font=('poppins',12,'bold'),bg='Deep Sky Blue',width=14,command=viewacn_screen)
    viewacn_btn.place(relx=.4,rely=.08)

    closeacn_btn= Button (frm,text='Close Account',bd=10,
                    font=('poppins',12,'bold'),bg='Deep Sky blue',width=14,command=closeacn_screen)
    closeacn_btn.place(relx=.7,rely=.08)


def fp_screen():
    frm=Frame(root,highlightbackground='black',highlightthickness=2) 
    frm.configure(bg='Ghost White')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.8) 
    
    def back_click():
         frm.destroy()
         main_screen()

    back_btn= Button (frm,text='Back',bd=10,
                    font=('poppins',12),bg='light blue',width=16,command=back_click)
    back_btn.place(relx=0,rely=0)

    lbl_acn=Label(frm,text="User Account No.",
                  font=('poppins',15,'bold'),bg='light blue')
    lbl_acn.place(relx=.3,rely=.25)

    e_acn=Entry(frm,font=('poppins',20,'bold'),bd=5)
    e_acn.place(relx=.45,rely=.25)

    lbl_email=Label(frm,text="User Email No.",
                  font=('poppins',15,'bold'),bg='light blue')
    lbl_email.place(relx=.3,rely=.35)


    e_email=Entry(frm,font=('poppins',20,'bold'),bd=5)
    e_email.place(relx=.45,rely=.35)

    OTP_btn= Button (frm,text='Validate & Send OTP',bd=10,
                    font=('poppins',12),bg='light blue',width=16)
    OTP_btn.place(relx=.56,rely=.45)

def main_screen():
    frm=Frame(root,highlightbackground='black',highlightthickness=2) 
    frm.configure(bg='Ghost White')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.8) 
     
    def fp_click():
         frm.destroy()
         fp_screen()

    def reset():
         e_acn.delete(0,"end")
         e_pass.delete(0,"end")
         e_captcha.delete(0,"end")
         cb_user.current(2)
       
    def login_click():
         global user_acn
         user_type=cb_user.get()
         user_acn=e_acn.get()
         user_pass=e_pass.get()
         user_captcha=e_captcha.get()

         if user_type=='Admin' and user_acn=='1' and user_pass=="admin" and user_captcha==captcha.replace(' ','') :
            frm.destroy() 
            admin_screen() 
         elif user_type=='Customer':
            conobj=sqlite3.connect(database='bank.sqlite')  
            curobj=conobj.cursor() 
            query='select * from users where acn=? and pass=?'
            curobj.execute(query,(user_acn,user_pass))
            row=curobj.fetchone()
            conobj.close()
            if row==None:
                 messagebox.showerror("Login","Invalid ACN/Pass")
            else:

                frm.destroy()
                customer_screen()

         else :
              messagebox.showerror("user type","Invalid Credentials")   
                     
    lbl_user= Label(frm,text="User Type",
                     font=('poppins',18,'bold'),bg='white') 
    lbl_user.place(relx=.32,rely=.12)
    
    cb_user= Combobox(frm,values=['Customer','Admin','--Select--'],
                      font=('poppins',18,'bold'))
    cb_user.current(2)
    cb_user.config(state='readonly')
    cb_user.place(relx=.45,rely=.12)

    lbl_acn=Label(frm,text="User Account No.",
                  font=('poppins',15,'bold'),bg='light blue')
    lbl_acn.place(relx=.3,rely=.25)


    e_acn=Entry(frm,font=('poppins',20,'bold'),bd=5)
    e_acn.place(relx=.45,rely=.25)

    
    lbl_pass=Label(frm,text="User Password",
                  font=('poppins',15,'bold'),bg='light blue',width=14)
    lbl_pass.place(relx=.3,rely=.35)

    e_pass=Entry(frm,font=('poppins',20,'bold'),bd=5,show='*')
    e_pass.place(relx=.45,rely=.35)

    captcha=mygenerator.generate_captcha()
    lbl_show_cap=Label(frm,text= captcha , 
                  font=('comic sons',15,'bold'),bg='light blue',fg ='purple',width=8)
    lbl_show_cap.place(relx=.45,rely=.45)

    def refresh_captcha():
            nonlocal captcha
            captcha=mygenerator.generate_captcha()
            lbl_show_cap.configure(text=captcha)
    
    ref_btn= Button (frm,text='🔄 refresh',bd=5,font=('poppins',12),bg='light blue',command=refresh_captcha)
    ref_btn.place(relx=.54,rely=.44)

    lbl_captcha=Label(frm,text="User Captcha",
                  font=('poppins',15,'bold'),bg='light blue',width=14)
    lbl_captcha.place(relx=.3,rely=.55)

    e_captcha=Entry(frm,font=('poppins',20,'bold'),bd=5)
    e_captcha.place(relx=.45,rely=.55)


    login_btn= Button (frm,text='Login',bd=10,
                       font=('poppins',12),bg='light blue',command=login_click,width=8)
    login_btn.place(relx=.45,rely=.68)
    
    
    reset_btn= Button (frm,text='Reset',command=reset,bd=10,font=('poppins',12),bg='light blue',width=8)
    reset_btn.place(relx=.54,rely=.68)

    fp_btn= Button (frm,text='Forgot Password',bd=10,
                    font=('poppins',12),bg='light blue',width=16,command=fp_click)
    fp_btn.place(relx=.45,rely=.8)
     
root=Tk()
root.state('zoomed')
root.configure(bg='light blue')
root.resizable(width=False ,height=False)

lbl_title=Label (root,text="Banking simulation",       # Main Heading 
                 font=('Poppins',40,'underline'),bg='light blue') 
lbl_title.pack()
lbl_dt=Label(root,text=time.strftime("%A ,%b %d %y %r"),        #Datetime 
             font=('Poppins',10,'bold'),bg='light blue',fg='dark blue') 
lbl_dt.pack() 
update_time()

img1=Image.open('logo.jpg').resize((250,150))          # logo(image)
imgtk=ImageTk.PhotoImage(img1,master=root)

lbl_logo=Label(root,image=imgtk)
lbl_logo.place(relx=0,rely=0)

lbl_footer=Label (root,text="Developed By : Gaurav Saini ,@ 9528142656",      # footer heading 
                 font=('Poppins',10,'bold'), bg='light blue',fg='dark blue') 
lbl_footer.pack(side='bottom',pady=10)

main_screen()
root.mainloop()