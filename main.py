from tkinter.ttk import *
from tkinter import Toplevel, StringVar, messagebox, Tk, END
import mysql.connector

con = mysql.connector.connect(
    host='localhost', password="mastermind2901", user='root', charset='utf8')

# DB


def SetupDB():
    cur = con.cursor()
    cur.execute("Create Database if not exists BloodbankDB;")
    cur.execute("use BloodBankDB;")
    cur.execute("Create Table if not exists Users(ID INT primary key Auto_Increment, PhoneNumber VarChar(10) Not Null,Name VarChar(30), Age INT, Gender VarChar(2),BloodType Varchar(5));")
    cur.execute("Create Table if not exists Donations(ID INT primary key Auto_Increment, UserID INT,BloodType Varchar(5), Date Date,Place VarChar(30));")
    cur.execute("Create Table if not exists BloodReserve(ID INT primary key Auto_Increment, BloodType Varchar(5), BloodLevel Decimal(3,2));")
    print("Database ready!")


def db_createUser(name, gender, age, phonenumber, bloodtype):
    cur = con.cursor()
    cur.execute("insert into Users(PhoneNumber,Name, Age, Gender, BloodType) values('{}','{}',{},'{}','{}');".format(
        phonenumber, name, age, gender, bloodtype))
    con.commit()


def db_getDonations(UserID):
    cur = con.cursor()
    cur.execute(
        "select * from Donations where UserID={};".format(UserID))
    return cur.fetchall()


def db_getUser(phoneNumber):
    cur = con.cursor()
    cur.execute(
        "select * from Users where PhoneNumber='{}';".format(phoneNumber))
    return cur.fetchall()


# Screens
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


def donationsTable(root, list, startx, starty):
    cells = []
    for i in range(len(list)):
        for j in range(5):
            e = Entry(root, width=20, fg='blue',
                      font=('Arial', 16, 'bold'), state='disabled')
            e.grid(row=startx+i, column=starty+j)
            e.insert(END, list[i][j])
            cells.append(e)


def UserMain(PhoneNumber):
    scrUserMain = Toplevel()
    scrUserMain.title("User")
    scrUserMain.geometry("500x500")

    userDto = db_getUser(PhoneNumber)
    print(userDto)
    btn2 = Button(scrUserMain, text="Edit",
                  command=lambda: UserEdit(userDto))
    btn2.grid(column=1, row=1)
    scrUserMain.mainloop()


def UserEdit(userDto):

    scrUserEdit = Toplevel()
    scrUserEdit.title("User")
    scrUserEdit.geometry("500x500")
    txtName = Entry(scrUserEdit)
    txtName.insert(0, str(userDto[0][2]))
    txtPhoneno = Entry(scrUserEdit)
    txtPhoneno.insert(0, str(userDto[0][1]))
    txtAge = Entry(scrUserEdit)
    txtAge.insert(0, str(userDto[0][3]))

    lblName = Label(scrUserEdit, text="Name")
    lblPhoneNo = Label(scrUserEdit, text="PhoneNo")
    lblAge = Label(scrUserEdit, text="Age")

    lblName.grid(column=1, row=1)
    lblPhoneNo.grid(column=1, row=2)
    lblAge.grid(column=1, row=3)
    txtName.grid(column=2, row=1)
    txtPhoneno.grid(column=2, row=2)
    txtAge.grid(column=2, row=3)

    scrUserEdit.mainloop()


def UserSelectSignOption():
    scrUserSelectSignOption = Toplevel()
    scrUserSelectSignOption.title("Select sign in option")
    scrUserSelectSignOption.geometry("500x500")
    btn1 = Button(scrUserSelectSignOption, text="Sign In", command=UserSignIn)
    btn2 = Button(scrUserSelectSignOption, text="Sign Up",
                  command=UserSignUpOrCreate)
    btn1.grid(column=1, row=1)
    btn2.grid(column=2, row=1)
    scrUserSelectSignOption.mainloop()


def UserSignIn():
    scrUserSignIn = Toplevel()
    scrUserSignIn.geometry("500x500")
    scrUserSignIn.title("Sign In")
    txtPhoneNumber = Entry(scrUserSignIn)

    def btnSubmitOnPress():
        phone = txtPhoneNumber.get()
        if not txtPhoneNumber.get().isnumeric():
            messagebox.showwarning('Warning!', "Invalid Input!")
        elif len(db_getUser(txtPhoneNumber.get())) < 1:
            messagebox.showwarning('Warning!', "No user found!")
        else:
            scrUserSignIn.destroy()
            UserMain(phone)

    btnSubmit = Button(scrUserSignIn, text="Sign In",
                       command=btnSubmitOnPress)

    lblPhoneNumber = Label(scrUserSignIn, text="Phone Number")
    lblPhoneNumber.grid(column=1, row=1)
    txtPhoneNumber.grid(column=2, row=1)
    btnSubmit.grid(column=2, row=2)

    scrUserSignIn.mainloop()


def UserSignUpOrCreate():
    scrUserSignUpOrCreate = Toplevel()
    scrUserSignUpOrCreate.title("Sign Up")
    scrUserSignUpOrCreate.geometry("500x500")

    # Gender selector radio button
    selectedGender = StringVar()
    rad1mGender = Radiobutton(scrUserSignUpOrCreate,
                              text='Male', variable=selectedGender, value='M')
    rad2fGender = Radiobutton(
        scrUserSignUpOrCreate, text='Female', variable=selectedGender, value='F')

    # Blood group selector drop down
    bloodGroups = [
        "Select blood group",
        "A+",
        "A-",
        "B+",
        "B-",
        "AB+",
        "AB-",
        "O+",
        "O-",
    ]
    selecteBloodGroup = StringVar()
    selecteBloodGroup.set("None")
    dpwBloodGroup = OptionMenu(
        scrUserSignUpOrCreate, selecteBloodGroup, *bloodGroups)

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
    dpwBloodGroup.grid(column=3, row=4)

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
        elif gender == "":
            messagebox.showwarning('Warning!', 'Invalid phone no!')
        elif len(db_getUser(phone)) > 0:
            messagebox.showwarning('Warning!', "Phone number already used!")
        elif selecteBloodGroup.get() == "None":
            messagebox.showwarning('Warning!', "Phone number already used!")
        else:
            scrUserSignUpOrCreate.destroy()
            db_createUser(name, gender, age, phone, selecteBloodGroup.get())
            UserMain(phone)
    btnSubmit = Button(scrUserSignUpOrCreate,
                       text="Sign Up", command=clicked_Messagebox)
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
