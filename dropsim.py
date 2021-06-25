from tkinter import *
 
# root window
root = Tk()
 
# root window title and dimension
root.title("Andariel (H) Drop Simulator")   # can use quest drop
# width, height
root.geometry('640x480')

# add image of andariel.  ascii?

# function to display loot
def clicked():
    # drop loot taking into account /players setting (txt.get() below)
    lbl2.configure(text = f"players {txt.get()} \nLoot: \n[]")


# button
btn = Button(root, text = "Run" , fg = "red", command=clicked)
# set button grid
btn.grid(column=0, row=0)

 
# players setting
lbl1 = Label(root, text = "      /players")
lbl1.grid(column=1, row=0)

# entry Field
txt = Entry(root, width=3)
txt.insert(0, "1")
txt.grid(column=2, row=0)

# instructions label
lbl2 = Label(root, text = "Ready to Farm? Click 'Run'")
lbl2.grid(column=3, row=1)


root.mainloop()
