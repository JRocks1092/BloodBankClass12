from tkinter import *
mainloop = Tk("main")
scrUserSignUpOrCreate = Toplevel(mainloop)
scrUserSignUpOrCreate.title("hello")
scrUserSignUpOrCreate.geometry("500x500")
selectedGender = StringVar()        
rad1mGender= Radiobutton(scrUserSignUpOrCreate, text ='Male' , variable= selectedGender , value='M')
rad2fGender= Radiobutton(scrUserSignUpOrCreate, text ='Female', variable= selectedGender , value='F')  
rad1mGender.grid(column=1, row=0)
rad2fGender.grid(column=2, row=0)
btnSubmit = Button(scrUserSignUpOrCreate, text="Hello",command=lambda: print(selectedGender.get()))
btnSubmit.grid(column=2, row=4)
scrUserSignUpOrCreate.mainloop()