from tkinter import *

from data_util import final_roll_from_tc, name_from_armo_weap_misc


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
    loot_list = []
    andy_str = 'Andarielq (H)'
    
    for i in range(5):
        loot_list.append(name_from_armo_weap_misc(final_roll_from_tc(andy_str)))
    loot_str = "\n".join(loot_list)
    
    lbl2.configure(text = f"players {txt.get()} \nLoot: \n\n{loot_str}")


# button
btn = Button(root, text = "Run" , fg = "red", command=clicked, font=('Segoe UI', 10))
# set button grid
btn.grid(column=0, row=0)


# players setting
lbl1 = Label(root, text = "      /players", font=('Segoe UI', 10))
lbl1.grid(column=1, row=0)

# entry Field
txt = Entry(root, width=3, font=('Segoe UI', 10))
txt.insert(0, "x")
txt.grid(column=2, row=0)

# instructions label and loot output
lbl2 = Label(root, text = "Ready to Farm? Click 'Run'", width=50, font=('Segoe UI', 10), fg='#f5f5f5', bg='#242020')
lbl2.grid(column=3, row=1)


root.mainloop()

### get items from TC first, then determine quality (unique, set, rare, magic)


### TODO: 'run X times'
# 100 andy runs with one click. then see the Loot!

### Credits
# https://www.geeksforgeeks.org/create-first-gui-application-using-python-tkinter/
# https://www.geeksforgeeks.org/how-to-change-the-tkinter-label-font-size/
# https://d2mods.info/forum/kb/viewarticle?a=368
# https://d2mods.info/forum/kb/viewarticle?a=2
