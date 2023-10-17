from tkinter import *

from tkinter.ttk import Progressbar

from tkinter import ttk

window = Tk()

window.title("Welcome to LikeGeeks app")

window.geometry('350x200')

style = ttk.Style()

style.theme_use('default')

style.configure("green.Vertical.TProgressbar", background='red')

bar = Progressbar(window, length=100,
                  style='green.Vertical.TProgressbar', orient="vertical")

bar['value'] = 25
bar.grid(column=0, row=0)

window.mainloop()


class Table:

    def __init__(self, root):

        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):

                self.e = Entry(root, width=20, fg='blue',
                               font=('Arial', 16, 'bold'))

                self.e.grid(row=i, column=j)
                self.e.insert(END, lst[i][j])


# take the data
lst = [(1, 'Raj', 'Mumbai', 19),
       (2, 'Aaryan', 'Pune', 18),
       (3, 'Vaishnavi', 'Mumbai', 20),
       (4, 'Rachna', 'Mumbai', 21),
       (5, 'Shubham', 'Delhi', 21)]

# find total number of rows and
# columns in list
total_rows = len(lst)
total_columns = len(lst[0])

# create root window
root = Tk()
t = Table(root)
root.mainloop()
