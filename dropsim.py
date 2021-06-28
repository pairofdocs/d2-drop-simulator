
import logging

from tkinter import *

from data_util import final_roll_from_tc, name_from_armo_weap_misc

# log drops to file
logging.basicConfig(filename='session.txt', filemode='w', format='%(message)s', level=logging.INFO)


DIFFICULTIES = {'Normal': '', 'Nightmare': ' (N)', 'Hell': ' (H)'}

# root window
root = Tk()

# root window title and dimension
root.title("Andariel Quest Drop Simulator")
# width, height
root.geometry('640x480')


# function to display loot
num_runs = 0
def clicked():
    global num_runs
    num_runs += 1
    logging.info(f"{num_runs})")

    mon_str = 'Andarielq' + DIFFICULTIES[diffi.get()]
    players_str = txt.get()
    mf_str = txtmf.get()
    drops = [] # 6 items at most.  7 picks from andariel
    
    lbl3.configure(text = "Loot:")
    # clean all previous drops
    for i in range(6):
        loot_labels[i].configure(text = '', fg = '#f5f5f5')

    for i in range(7):
        if len(drops) == 6:
            break
        loot_item = final_roll_from_tc(mon_str, players_str)   # output is '' if NoDrop
        if loot_item:
            loot_item = name_from_armo_weap_misc(loot_item, mf_str, mon_str)
            drops.append(loot_item)


    for i,loot_item in enumerate(drops):
        if "uni~" in loot_item:
            if "failed uni~" in loot_item:
                if 'potion' in loot_item.lower(): #loot_labels
                    loot_labels[i].configure(text = loot_item.replace('failed uni~ ',''), fg = '#f5f5f5')  # default gray
                else:
                    loot_labels[i].configure(text = loot_item.replace('failed uni~ ',''), fg = '#ebe134')  # rare/yellow
                    if "charm" in loot_item.lower():
                        loot_labels[i].configure(text = loot_item.replace('failed uni~ ',''), fg = '#8f82ff')    # undo rare color for charm
            else:
                loot_labels[i].configure(text = loot_item.replace('uni~ ',''), fg = '#ba8106')  # unique
                logging.info(f"{loot_item}")

        elif "set~" in loot_item:
            if "failed set~" in loot_item:
                if 'potion' in loot_item.lower():
                    loot_labels[i].configure(text = loot_item.replace('failed set~ ',''), fg = '#f5f5f5')  # default gray
                else:
                    loot_labels[i].configure(text = loot_item.replace('failed set~ ',''), fg = '#8f82ff')  # magic/blue
            else:
                loot_labels[i].configure(text = loot_item.replace('set~ ',''), fg = '#33d61a')   # green
                logging.info(f"{loot_item}")
        
        elif "rare~" in loot_item:
            if 'potion' in loot_item.lower():
                loot_labels[i].configure(text = loot_item.replace('rare~ ',''), fg = '#f5f5f5')  # default gray
            else:
                loot_labels[i].configure(text = loot_item.replace('rare~ ',''), fg = '#ebe134')  # rare/yellow
                if "charm" in loot_item.lower():
                    loot_labels[i].configure(text = loot_item.replace('rare~ ',''), fg = '#8f82ff')    # undo rare color for charm

        elif ("essence of" in loot_item.lower() or " rune" in loot_item.lower()):
            loot_labels[i].configure(text = loot_item, fg = '#eb721c')
        else:
            # reset color
            loot_labels[i].configure(text = loot_item, fg = '#f5f5f5')
        
        # final str fixes
        loot_str = loot_labels[i].cget('text')
        loot_str = loot_str.replace("Charm Large", "Grand Charm").replace("Charm Medium", "Large Charm").replace("Charm Small", "Small Charm")
        # if "charm" in loot_str.lower(): print("**************************charm", loot_str)
        loot_labels[i].configure(text = loot_str)
    logging.info(" ")

# background image
bckgrd_image = PhotoImage(file="./img/andy-d2r-resize.png")
bckgrd_label = Label(root, image=bckgrd_image)
bckgrd_label.place(x=0, y=34, relwidth=1, relheight=1)


# button
btn = Button(root, text = "Run" , fg = "red", command=clicked, font=('Segoe UI', 10))
# set button grid
btn.grid(column=0, row=0)


# players setting
lbl1 = Label(root, text = "/players", font=('Segoe UI', 10), width=15)
lbl1.grid(column=1, row=0)

# entry Field
txt = Entry(root, width=4, font=('Segoe UI', 10))
txt.insert(0, "1")
txt.grid(column=2, row=0)

# MF settings
lbl2 = Label(root, text = "+Magic Find", font=('Segoe UI', 10), width=15)
lbl2.grid(column=1, row=1)
# entry Field
txtmf = Entry(root, width=4, font=('Segoe UI', 10))
txtmf.insert(0, "0")
txtmf.grid(column=2, row=1)

# difficulty settings dropdown
diffi = StringVar(root)
diffi.set(list(DIFFICULTIES.keys())[2]) # default value

w = OptionMenu(root, diffi, *DIFFICULTIES)
w.configure(width=10, font=('Segoe UI', 9))
w.grid(column=3, row=0)


# instructions label and loot output
lbl3 = Label(root, text = "Ready to Farm? Click 'Run'", width=25, font=('Segoe UI', 10), fg='#f5f5f5', bg='#242020')
lbl3.place(x=340, y=130+23)

# rows for loot drops. 6 loot rows total
# lbl4 = Label(root, text = "", width=25, font=('Segoe UI', 10), fg='#f5f5f5', bg='#242020')
# lbl4.place(x=340, y=130+23)
lbl5 = Label(root, text = "", width=25, font=('Segoe UI', 10), fg='#f5f5f5', bg='#242020')
lbl5.place(x=340, y=130+23*2)
lbl6 = Label(root, text = "", width=25, font=('Segoe UI', 10), fg='#f5f5f5', bg='#242020')
lbl6.place(x=340, y=130+23*3)
lbl7 = Label(root, text = "", width=25, font=('Segoe UI', 10), fg='#f5f5f5', bg='#242020')
lbl7.place(x=340, y=130+23*4)
lbl8 = Label(root, text = "", width=25, font=('Segoe UI', 10), fg='#f5f5f5', bg='#242020')
lbl8.place(x=340, y=130+23*5)
lbl9 = Label(root, text = "", width=25, font=('Segoe UI', 10), fg='#f5f5f5', bg='#242020')
lbl9.place(x=340, y=130+23*6)
lbl10 = Label(root, text = "", width=25, font=('Segoe UI', 10), fg='#f5f5f5', bg='#242020')
lbl10.place(x=340, y=130+23*7)

loot_labels = [lbl5, lbl6, lbl7, lbl8, lbl9, lbl10]


root.mainloop()


### Possible TODO: 'run X times'
# 100 andy runs with one click. then see the Loot!
# add a scroll window. how would i add colored text?
