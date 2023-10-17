from tkinter.ttk import *
from tkinter import Toplevel,Tk,StringVar,messagebox
import mysql.connector

con = mysql.connector.connect(host='localhost', password="mastermind2901",user='root',charset='utf8')
# Screens

def SetupDB():
    cur = con.cursor()
    cur.execute("Create Database if not exists BloodbankDB;")
    cur.execute("use BloodBankDB;")
    cur.execute("Create Table if not exists Users(ID INT primary key Auto_Increment, PhoneNumber VarChar(10) Not Null,Name VarChar(30), Age INT, Gender VarChar(2));")
    cur.execute("Create Table if not exists Donations(ID INT primary key Auto_Increment, UserID INT,BloodType Varchar(5), Date Date,Place VarChar(30));")
    cur.execute("Create Table if not exists BloodReserve(ID INT primary key Auto_Increment, BloodType Varchar(5), BloodLevel Decimal(3,2));")
    print("Database ready!")
    
def db_createUser(name, gender, age, phonenumber):
    cur = con.cursor()
    cur.execute("insert into Users(PhoneNumber,Name, Age, Gender) values('{}','{}',{},'{}');".format(phonenumber,name,age,gender))
    con.commit()    

def AdminMain():    
    scrUserMain = Toplevel()
    scrUserMain.title("Admin")
    scrUserMain.geometry("500x500")
    scrUserMain.mainloop()


def AdminLogon():
    scrAdminLogon = Toplevel()
    scrAdminLogon.geometry("500x500")
    scrAdminLogon.title("Admin Sign In")
    txtPassword = Entry(scrAdminLogon)
    password1 = "bloodbank1"

    def btnSubmitOnPress():
        if txtPassword.get() == password1:
            scrAdminLogon.destroy()
            AdminMain()
        else:
            messagebox.showwarning('Warning!', "Invalid Password!")
    btnSubmit = Button(scrAdminLogon, text="Sign In",
                       command=btnSubmitOnPress)

    lblPassword = Label(scrAdminLogon, text="Password")
    lblPassword.grid(column=1, row=1)
    txtPassword.grid(column=2, row=1)
    btnSubmit.grid(column=2, row=2)

    scrAdminLogon.mainloop()


def UserMain():
    scrUserMain = Toplevel()
    scrUserMain.title("User")
    scrUserMain.geometry("500x500")
    scrUserMain.mainloop()


def UserSelectSignOption():
    scrUserSelectSignOption = Toplevel()
    scrUserSelectSignOption.title("Select sign in option")
    scrUserSelectSignOption.geometry("500x500")
    btn1 = Button(scrUserSelectSignOption, text="Sign In", command=UserSignIn)
    btn2 = Button(scrUserSelectSignOption, text="Sign Up",
                  command=lambda: UserSignUpOrCreate("Sign Up"))
    btn1.grid(column=1, row=1)
    btn2.grid(column=2, row=1)
    scrUserSelectSignOption.mainloop()


def UserSignIn():
    scrUserSignIn = Toplevel()
    scrUserSignIn.geometry("500x500")
    scrUserSignIn.title("Sign In")
    txtPhoneNumber = Entry(scrUserSignIn)

    def btnSubmitOnPress():
        if txtPhoneNumber.get().isnumeric():
            scrUserSignIn.destroy()
            UserMain()
        else:
            messagebox.showwarning('Warning!', "Invalid Input!")
    btnSubmit = Button(scrUserSignIn, text="Sign In",
                       command=btnSubmitOnPress)

    lblPhoneNumber = Label(scrUserSignIn, text="Phone Number")
    lblPhoneNumber.grid(column=1, row=1)
    txtPhoneNumber.grid(column=2, row=1)
    btnSubmit.grid(column=2, row=2)

    scrUserSignIn.mainloop()


def UserSignUpOrCreate(ScreenTitle):
    scrUserSignUpOrCreate = Toplevel()
    scrUserSignUpOrCreate.title(ScreenTitle)
    scrUserSignUpOrCreate.geometry("500x500")
    selectedGender = StringVar()            
    rad1mGender= Radiobutton(scrUserSignUpOrCreate, text ='Male' , variable= selectedGender , value='M')
    rad2fGender= Radiobutton(scrUserSignUpOrCreate, text ='Female', variable= selectedGender , value='F')      
    txtName = Entry(scrUserSignUpOrCreate)
    txtPhoneno = Entry(scrUserSignUpOrCreate)
    txtAge = Entry(scrUserSignUpOrCreate)
    lblGender = Label(scrUserSignUpOrCreate, text="Gender")
    lblName = Label(scrUserSignUpOrCreate, text="Name")
    lblPhoneNo = Label(scrUserSignUpOrCreate, text="PhoneNo")
    lblAge = Label(scrUserSignUpOrCreate, text="Age")

    lblGender.grid(column=0, row=0)
    rad1mGender.grid(column=1, row=0)
    rad2fGender.grid(column=2, row=0)
    lblName.grid(column=1, row=1)
    lblPhoneNo.grid(column=1, row=2)
    lblAge.grid(column=1, row=3)
    txtName.grid(column=2, row=1)
    txtPhoneno.grid(column=2, row=2)
    txtAge.grid(column=2, row=3)

    def clicked_Messagebox():
        age = txtAge.get()
        name = txtName.get()
        phone = txtPhoneno.get()
        gender = selectedGender.get()                
        if not age.isnumeric():
            messagebox.showwarning('Warning!', "Invalid Age!")
        elif int(age) < 18:
            messagebox.showwarning('Warning!', 'Under age!')
        elif txtName.get().strip() == "":
            messagebox.showwarning('Warning!', 'Name cannot be empty!')
        elif not (phone.isnumeric() and len(phone) == 10):
            messagebox.showwarning('Warning!', 'Invalid phone no!')
        elif gender=="":
            messagebox.showwarning('Warning!', 'Invalid phone no!')
        else:
            scrUserSignUpOrCreate.destroy()
            db_createUser(name, gender, age,phone)
            UserMain()
    btnSubmit = Button(scrUserSignUpOrCreate, text=ScreenTitle,command=clicked_Messagebox)
    btnSubmit.grid(column=2, row=4)

    scrUserSignUpOrCreate.mainloop()


def Start():
    scrStart = Tk("Blood Donation Assistant")
    scrStart.title("Blood Donation Assistant")
    scrStart.geometry("500x500")
    btnUser = Button(scrStart, text="User", command=UserSelectSignOption)
    btnAdmin = Button(scrStart, text="Admin", command=AdminLogon)
    btnUser.grid(column=1, row=1)
    btnAdmin.grid(column=2, row=1)
    scrStart.mainloop()


def app():
    print("Blood Donation Assistant")
    print("version 0.1")
    SetupDB()
    Start()


app()
