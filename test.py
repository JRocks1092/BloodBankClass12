from tkinter.ttk import *
from tkinter import Toplevel, StringVar, messagebox, Tk, END
import mysql.connector
from datetime import datetime

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
    qry = "select * from Donations"
    if UserID != 0:
        qry += " where UserID={}".format(UserID)
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
    cur.execute("insert into Users(UserID,BloodType,Date,Place) values({},'{}','{}','{}');".format(
        userDTO[0], userDTO[5], datestr, place))
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
        dateOfLastDonation = datetime.strptime(
            db_getDonations(userID)[0][3], '%Y-%m-%d %H:%M:%S')
        if (dateNowStr - dateOfLastDonation).days < 90:
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

    donations = db_getDonations()
    DataTableRows = Table(scrAdminMain, donations, 2, 4)

    def btnAddNewDonationOnPress():
        NewDonation()

    btnAddNewDonation = Button(scrAdminMain, text="Add Donation",
                               command=btnAddNewDonationOnPress)
    btnAddNewDonation.grid(column=2, row=2)

    createBloodLevelBars(scrAdminMain, 0, 0)

    scrAdminMain.mainloop()


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


def Table(root, dataRows, startx, starty):
    rows = []
    for i in range(len(dataRows)):
        cells = []
        for j in range(5):
            e = Entry(root, width=20, fg='blue',
                      font=('Arial', 16, 'bold'), state='disabled')
            e.grid(row=startx+i, column=starty+j)
            e.insert(END, dataRows[i][j])
            cells.append(e)
        rows.append(cells)
    return rows


def UserMain(userDto):
    scrUserMain = Toplevel()
    scrUserMain.title("User")
    scrUserMain.geometry("500x500")
    donations = db_getDonations(userDto[0])
    DataTableRows = Table(scrUserMain, donations, 2, 4)

    btn2 = Button(scrUserMain, text="Edit",
                  command=lambda: UserEdit(userDto))
    btn2.grid(column=1, row=1)
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
            UserMain(phone)
    btnSubmit = Button(scrUserSignUpOrCreate,
                       text="Sign Up", command=clicked_btnsubmit)
    btnSubmit.grid(column=2, row=4)

    scrUserSignUpOrCreate.mainloop()


def Start():
    scrStart = Tk("Blood Donation Assistant")
    scrStart.title("Blood Donation Assistant")
    scrStart.geometry("500x500")
    style = Style(scrStart)
    style.theme_use("xpnative")
    style.configure("Red.Vertical.TProgressbar", background='red')
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
