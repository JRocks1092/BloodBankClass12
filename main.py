from tkinter.ttk import *
from tkinter import *
from tkinter import Toplevel, StringVar, messagebox, Tk, END
import mysql.connector
from datetime import datetime


con = mysql.connector.connect(
    host='localhost', password="mastermind2901", user='root', charset='utf8')

# DB


def setBloodReserveTable():
    cur = con.cursor()
    allGroups = ["A+",   "A-",        "B+",        "B-",
                 "AB+",        "AB-",        "O+",        "O-",]
    for i in allGroups:
        cur.execute(
            "select BloodType from BloodReserve where BloodType='{}'".format(i))
        if len(cur.fetchall()) < 1:
            cur.execute(
                "insert into BloodReserve(BloodType,BloodLevel) values ('{}',0);".format(i))
    con.commit()


def SetupDB():
    cur = con.cursor()
    cur.execute("Create Database if not exists BloodbankDB;")
    cur.execute("use BloodBankDB;")
    cur.execute("Create Table if not exists Users(ID INT primary key Auto_Increment, PhoneNumber VarChar(10) Not Null,Name VarChar(30), Age INT, Gender VarChar(2),BloodType Varchar(5));")
    cur.execute("Create Table if not exists Donations(ID INT primary key Auto_Increment, UserID INT,BloodType Varchar(5), Date Date,Place VarChar(30));")
    cur.execute("Create Table if not exists BloodReserve(ID INT primary key Auto_Increment, BloodType Varchar(5), BloodLevel Decimal(3,2));")
    setBloodReserveTable()
    print("Database ready!")


def db_createUser(name, gender, age, phonenumber, bloodtype):
    cur = con.cursor()
    cur.execute("insert into Users(PhoneNumber,Name, Age, Gender,BloodType) values('{}','{}',{},'{}','{}');".format(
        phonenumber, name, age, gender, bloodtype))
    con.commit()


def db_updateUser(userid, name, age, phonenumber):
    cur = con.cursor()
    qry = "update Users set PhoneNumber='{}',Name='{}', Age={} where ID={};".format(
        phonenumber, name, age, userid)
    cur.execute(qry)
    con.commit()


def db_getDonations(UserID=0):
    cur = con.cursor()
    qry = "select d.ID,u.Name,u.PhoneNumber,u.Age,u.Gender,d.BloodType,d.Date,d.Place from Donations d,Users u where d.UserID = u.ID"
    if UserID != 0:
        qry += " and UserID={}".format(UserID)
    qry += " order by Date desc;"
    cur.execute(qry)
    return cur.fetchall()


def db_getBloodReserve():
    cur = con.cursor()
    cur.execute("select * from BloodReserve;")
    return cur.fetchall()


def db_getUser(phoneNumber):
    cur = con.cursor()
    cur.execute(
        "select * from Users where PhoneNumber='{}';".format(phoneNumber))
    return cur.fetchall()


def db_createNewDonation(place, userDTO):
    datestr = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur = con.cursor()
    cur.execute("insert into Donations(UserID,BloodType,Date,Place) values({},'{}','{}','{}');".format(
        userDTO[0], userDTO[5], datestr, place))
    cur.execute("update BloodReserve set BloodLevel=BloodLevel+1 where BloodType='{}';".format(
        userDTO[5]))
    con.commit()


# Screens
def progressBar(scr, bloodlevel, x, y):
    bar = Progressbar(
        scr, length=100,
        style='Red.Vertical.TProgressbar', orient="vertical")

    bar['value'] = bloodlevel[2]
    bar.grid(column=x, row=y)
    lblBar = Label(scr, text=bloodlevel[1])
    lblBar.grid(column=x, row=y+1)
    return bar


def isUserAbleToDonate(userID):
    dateNowStr = datetime.now()
    userDonations = db_getDonations(userID)
    if len(userDonations) > 0:
        if (dateNowStr - db_getDonations(userID)[0][6]).days > 90:
            return True
        else:
            return False
    else:
        return True


def createBloodLevelBars(scr, startx, starty):
    bars = []
    bloodlevels = db_getBloodReserve()
    print(bloodlevels)
    for i in range(len(bloodlevels)):
        bars.append(progressBar(scr, bloodlevels[i], startx+i, starty))


def NewDonation():
    scrNewDonation = Toplevel()
    scrNewDonation.title("Sign Up")
    scrNewDonation.geometry("500x500")

    txtPlace = Entry(scrNewDonation)
    txtPhoneno = Entry(scrNewDonation)
    lblPlace = Label(scrNewDonation, text="Place")
    lblPhoneNo = Label(scrNewDonation, text="PhoneNo")

    lblPlace.grid(column=1, row=1)
    lblPhoneNo.grid(column=1, row=2)
    txtPlace.grid(column=2, row=1)
    txtPhoneno.grid(column=2, row=2)

    def clicked_AddBtn():
        phone = txtPhoneno.get()
        userDto = db_getUser(phone)
        if not (phone.isnumeric() and len(phone) == 10):
            messagebox.showwarning('Warning!', 'Invalid phone no!')
            return
        elif len(userDto) < 1:
            messagebox.showwarning('Warning!', "No user found!")
            return
        userDto = userDto[0]
        if not isUserAbleToDonate(userDto[0]):
            messagebox.showwarning('Warning!', "This user cannot donate now!")
        else:
            db_createNewDonation(txtPlace.get(), userDto)
            scrNewDonation.destroy()

    btnAdd = Button(scrNewDonation,
                    text="Add", command=clicked_AddBtn)
    btnAdd.grid(column=2, row=4)

    scrNewDonation.mainloop()


def AdminMain():
    scrAdminMain = Toplevel()
    scrAdminMain.title("Admin")
    scrAdminMain.geometry("500x500")

    btnAddNewDonation = Button(scrAdminMain, text="Add Donation",
                               command=NewDonation)
    btnAddNewDonation.grid(column=9, row=0)
    btnShowDonationsTable = Button(scrAdminMain, text="All Donations",
                                   command=DonationsTableScreen)
    btnShowDonationsTable.grid(column=9, row=1)
    createBloodLevelBars(scrAdminMain, 0, 0)
    scrAdminMain.mainloop()


def AdminLogon():
    scrAdminLogon = Toplevel()
    scrAdminLogon.geometry("570x505")
    scrAdminLogon.title("Admin Sign In")
    txtPassword = Entry(scrAdminLogon, bd=4, bg="Red")
    password1 = "bloodbank1"

    def btnSubmitOnPress():
        if txtPassword.get() == password1:
            scrAdminLogon.destroy()
            AdminMain()
        else:
            messagebox.showwarning('Warning!', "Invalid Password!")
    photoAdmin = PhotoImage(
        file=r"./Screenshot 2023-10-24 231427.png")
    btnSubmit = Button(scrAdminLogon, text="SIGN IN", width=20, height=5,
                       command=btnSubmitOnPress, font='Helvetica')
    btnImage = Button(scrAdminLogon, image=photoAdmin, bd=0, bg='Black')
    btnDummy1 = Button(scrAdminLogon, bd=0, bg="Red", width=20, height=5)
    btnDummy2 = Button(scrAdminLogon, bd=0, bg="Green", width=20, height=5)
    btnDummy3 = Button(scrAdminLogon, bd=0, bg="Cyan", width=20, height=5)
    lblPassword = Label(scrAdminLogon, text="PASSWORD!",
                        font=('Helvetica', 10))
    lblPassword.grid(column=0, row=1)
    txtPassword.grid(column=0, row=0)
    # btnDummy1.grid(column=0,row=0)
    # btnDummy2.grid(column=0,row=2)
    # btnDummy3.grid(column=1,row=0)
    btnSubmit.grid(column=0, row=3)
    btnImage.grid(column=0, row=4)

    scrAdminLogon.mainloop()


def Table(master, headers, dataRows):
    dataRows = [headers]+dataRows
    print(dataRows)
    for x in range(len(dataRows)):
        for y in range(len(headers)):
            e = Entry(master, width=15, fg='blue', font=(
                'Timew New Roman', 13, 'italic'))
            e.grid(row=x, column=y)
            e.insert(END, dataRows[x][y])


def DonationsTableScreen(UserID=0):
    scrDonationsTableScreen = Toplevel()
    scrDonationsTableScreen.title("DonationsTableScreen")
    scrDonationsTableScreen.geometry("900x500")
    donations = db_getDonations(UserID)
    DataTableRows = Table(
        scrDonationsTableScreen, ("ID", "Name", "Phone Number", "Age", "Gender", "BloodType", "Date", "Place"), donations)
    scrDonationsTableScreen.mainloop()


def UserMain(userDto):
    scrUserMain = Toplevel()
    scrUserMain.title("User")
    scrUserMain.geometry("500x500")

    lblNameLabel = Label(scrUserMain, text="Name")
    lblPhoneNoLabel = Label(scrUserMain, text="PhoneNo")
    lblAgeLabel = Label(scrUserMain, text="Age")
    lblGenderLabel = Label(scrUserMain, text="Gender")
    lblBloodGroupLabel = Label(scrUserMain, text="BloodGroup")

    lblName = Label(scrUserMain, text=userDto[2])
    lblPhoneNo = Label(scrUserMain, text=userDto[1])
    lblAge = Label(scrUserMain, text=userDto[3])
    lblGender = Label(scrUserMain, text=userDto[4])
    lblBloodGroup = Label(scrUserMain, text=userDto[5])

    lblNameLabel.grid(column=1, row=1)
    lblPhoneNoLabel.grid(column=1, row=2)
    lblAgeLabel.grid(column=1, row=3)
    lblGenderLabel.grid(column=1, row=4)
    lblBloodGroupLabel.grid(column=1, row=5)

    lblName.grid(column=2, row=1)
    lblPhoneNo.grid(column=2, row=2)
    lblAge.grid(column=2, row=3)
    lblGender.grid(column=2, row=4)
    lblBloodGroup.grid(column=2, row=5)

    btn2 = Button(scrUserMain, text="Edit Profile",
                  command=lambda: UserEdit(userDto))
    btn2.grid(column=1, row=6)
    btnShowDonationsTable = Button(scrUserMain, text="Show History",
                                   command=lambda: DonationsTableScreen(userDto[0]))
    btnShowDonationsTable.grid(column=2, row=6)
    scrUserMain.mainloop()


def UserEdit(userDto):
    scrUserEdit = Toplevel()
    scrUserEdit.title("User")
    scrUserEdit.geometry("500x500")
    txtName = Entry(scrUserEdit)
    txtName.insert(0, str(userDto[2]))
    txtPhoneno = Entry(scrUserEdit)
    txtPhoneno.insert(0, str(userDto[1]))
    txtAge = Entry(scrUserEdit)
    txtAge.insert(0, str(userDto[3]))

    lblName = Label(scrUserEdit, text="Name")
    lblPhoneNo = Label(scrUserEdit, text="PhoneNo")
    lblAge = Label(scrUserEdit, text="Age")

    def EditButton_Pressed():
        age = txtAge.get()
        name = txtName.get()
        phone = txtPhoneno.get()
        users = db_getUser(phone)
        if not age.isnumeric():
            messagebox.showwarning('Warning!', "Invalid Age!")
        elif int(age) < 18:
            messagebox.showwarning('Warning!', 'Under age!')
        elif txtName.get().strip() == "":
            messagebox.showwarning('Warning!', 'Name cannot be empty!')
        elif not (phone.isnumeric() and len(phone) == 10):
            messagebox.showwarning('Warning!', 'Invalid phone no!')
        elif len(users) > 1 and users[0][0] == userDto[0]:
            messagebox.showwarning('Warning!', "Phone number already used!")
        else:
            scrUserEdit.destroy()
            db_updateUser(userDto[0], name, age, phone)
            messagebox.showinfo("Message", "User Edited Succesfully!")
    btnSubmit = Button(scrUserEdit,
                       text="Edit", command=EditButton_Pressed)
    btnSubmit.grid(column=2, row=4)

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
    scrUserSelectSignOption.geometry("500x550")
    photo2 = PhotoImage(
        file=r"./Screenshot 2023-10-19 212917.png")
    btn1 = Button(scrUserSelectSignOption, width=55, height=5,
                  text="SIGN IN", font='Helvetica', command=UserSignIn)
    btn2 = Button(scrUserSelectSignOption, width=55, height=5, text="SIGN UP", font='Helvetica',
                  command=UserSignUpOrCreate)
    btnImageSign = Button(scrUserSelectSignOption,
                          image=photo2, bd=0, bg='Black')

    labelSign = Label(scrUserSelectSignOption,
                      text="SELECT SIGN OPTION!", font='Helvetica')
    labelSign.grid(column=2, row=3)
    btn1.grid(column=2, row=0)
    btn2.grid(column=2, row=1)
    btnImageSign.grid(column=2, row=5)
    scrUserSelectSignOption.mainloop()


def UserSignIn():
    scrUserSignIn = Toplevel()
    scrUserSignIn.geometry("500x500")
    scrUserSignIn.title("Sign In")
    txtPhoneNumber = Entry(scrUserSignIn)

    def btnSubmitOnPress():
        phone = txtPhoneNumber.get()
        userdto = db_getUser(phone)
        if not phone.isnumeric():
            messagebox.showwarning('Warning!', "Invalid Input!")
        elif len(userdto) < 1:
            messagebox.showwarning('Warning!', "No user found!")
        else:
            scrUserSignIn.destroy()
            UserMain(userdto[0])

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

    def clicked_btnsubmit():
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
        elif selecteBloodGroup.get() == "None" or selecteBloodGroup.get() == "Select blood group":
            messagebox.showwarning('Warning!', "Select Blood group!")
        else:
            scrUserSignUpOrCreate.destroy()
            db_createUser(name, gender, age, phone, selecteBloodGroup.get())
            user = db_getUser(phone)
            UserMain(user)
    btnSubmit = Button(scrUserSignUpOrCreate,
                       text="Sign Up", command=clicked_btnsubmit)
    btnSubmit.grid(column=2, row=4)

    scrUserSignUpOrCreate.mainloop()


def Start():
    scrStart = Tk("Blood Donation Assistant")
    scrStart.title("Blood Donation Assistant")
    scrStart.geometry("500x550")
    style = Style(scrStart)
    # style.theme_use("xpnative")
    style.configure("Red.Vertical.TProgressbar", background='red')
    photo1 = PhotoImage(
        file=r"./Screenshot 2023-10-19 212746.png")
    labelWelcome = Label(
        scrStart, text="WELCOME TO BLOODBANK!", font='Helvetica')
    btnUser = Button(scrStart, text="USER", width=55, height=5,
                     font='Helvetica', activebackground='Red', command=UserSelectSignOption)
    btnAdmin = Button(scrStart, text="ADMIN", width=55, height=5,
                      font='Helvetica', activebackground='Red', command=AdminLogon)
    btnImage = Button(scrStart, image=photo1, bd=0, bg='Black')

    btnUser.grid(column=2, row=0)
    btnAdmin.grid(column=2, row=1)
    labelWelcome.grid(column=2, row=3)
    btnImage.grid(column=2, row=5)
    scrStart.mainloop()


def app():
    print("Blood Donation Assistant")
    print("version 0.1")
    SetupDB()
    Start()


app()
