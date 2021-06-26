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
    # TODO: drop loot taking into account /players setting (txt.get() below)
    # TODO: account for MF   txtmf.get()
    print('\n')
    loot_list = []
    andy_str = 'Andarielq (H)'
    mf_str = txtmf.get()
    
    lbl3.configure(text = "Loot:")

    for i in range(5):
        # loot_list.append(name_from_armo_weap_misc(final_roll_from_tc(andy_str)))
        loot_item = name_from_armo_weap_misc(final_roll_from_tc(andy_str), mf_str)
        
        if "uni~" in loot_item:
            if "failed uni~" in loot_item:
                if 'potion' in loot_item.lower():
                    eval(f"lbl{i+5}.configure(text = loot_item.replace('failed uni~ ',''), fg = '#f5f5f5')")  # default gray
                else:
                    eval(f"lbl{i+5}.configure(text = loot_item.replace('failed uni~ ',''), fg = '#ebe134')")  # rare/yellow
                    if "charm" in loot_item.lower():
                        eval(f"lbl{i+5}.configure(text = loot_item.replace('failed uni~ ',''), fg = '#8f82ff')")    # undo rare color for charm
            else:
                eval(f"lbl{i+5}.configure(text = loot_item.replace('uni~ ',''), fg = '#ba8106')")  # unique

        elif "set~" in loot_item:
            if "failed set~" in loot_item:
                if 'potion' in loot_item.lower():
                    eval(f"lbl{i+5}.configure(text = loot_item.replace('failed set~ ',''), fg = '#f5f5f5')")  # default gray
                else:
                    eval(f"lbl{i+5}.configure(text = loot_item.replace('failed set~ ',''), fg = '#8f82ff')")  # magic/blue
            else:
                eval(f"lbl{i+5}.configure(text = loot_item.replace('set~ ',''), fg = '#33d61a')")   # green
        
        elif "rare~" in loot_item:
            if 'potion' in loot_item.lower():
                eval(f"lbl{i+5}.configure(text = loot_item.replace('rare~ ',''), fg = '#f5f5f5')")  # default gray
            else:
                eval(f"lbl{i+5}.configure(text = loot_item.replace('rare~ ',''), fg = '#ebe134')")  # rare/yellow
                if "charm" in loot_item.lower():
                    eval(f"lbl{i+5}.configure(text = loot_item.replace('rare~ ',''), fg = '#8f82ff')")    # undo rare color for charm

        elif ("essence of" in loot_item.lower() or " rune" in loot_item.lower()):
            eval(f"lbl{i+5}.configure(text = loot_item, fg = '#eb721c')")
        else:
            # reset color
            eval(f"lbl{i+5}.configure(text = loot_item, fg = '#f5f5f5')")
        
        # final str fixes
        exec(f"loot_str = lbl{i+5}.cget('text')")
        exec('loot_str = loot_str.replace("Charm Large", "Grand Charm").replace("Charm Medium", "Large Charm").replace("Charm Small", "Small Charm")')
        exec('if "charm" in loot_str.lower(): print("**************************charm", loot_str)')
        eval(f"lbl{i+5}.configure(text = loot_str)")



# button
btn = Button(root, text = "Run" , fg = "red", command=clicked, font=('Segoe UI', 10))
# set button grid
btn.grid(column=0, row=0)


# players setting
lbl1 = Label(root, text = "/players", font=('Segoe UI', 10), width=15)
lbl1.grid(column=1, row=0)

# entry Field
txt = Entry(root, width=4, font=('Segoe UI', 10))
txt.insert(0, "x")
txt.grid(column=2, row=0)

# TODO: MF settings
lbl2 = Label(root, text = "+Magic Find", font=('Segoe UI', 10), width=15)
lbl2.grid(column=1, row=1)
# entry Field
txtmf = Entry(root, width=4, font=('Segoe UI', 10))
txtmf.insert(0, "0")
txtmf.grid(column=2, row=1)


# instructions label and loot output
lbl3 = Label(root, text = "Ready to Farm? Click 'Run'", width=50, font=('Segoe UI', 10), fg='#f5f5f5', bg='#242020')
lbl3.grid(column=3, row=2)

# rows for loot drops. 6 loot rows total
lbl4 = Label(root, text = "", width=50, font=('Segoe UI', 10), fg='#f5f5f5', bg='#242020')
lbl4.grid(column=3, row=3)
lbl5 = Label(root, text = "", width=50, font=('Segoe UI', 10), fg='#f5f5f5', bg='#242020')
lbl5.grid(column=3, row=4)
lbl6 = Label(root, text = "", width=50, font=('Segoe UI', 10), fg='#f5f5f5', bg='#242020')
lbl6.grid(column=3, row=5)
lbl7 = Label(root, text = "", width=50, font=('Segoe UI', 10), fg='#f5f5f5', bg='#242020')
lbl7.grid(column=3, row=6)
lbl8 = Label(root, text = "", width=50, font=('Segoe UI', 10), fg='#f5f5f5', bg='#242020')
lbl8.grid(column=3, row=7)
lbl9 = Label(root, text = "", width=50, font=('Segoe UI', 10), fg='#f5f5f5', bg='#242020')
lbl9.grid(column=3, row=8)
lbl10 = Label(root, text = "", width=50, font=('Segoe UI', 10), fg='#f5f5f5', bg='#242020')
lbl10.grid(column=3, row=9)


root.mainloop()

### get items from TC first, then determine quality (unique, set, rare, magic)


### TODO: 'run X times'
# 100 andy runs with one click. then see the Loot!
# add a scroll window. how would i add colored text?


### Credits
# https://www.geeksforgeeks.org/create-first-gui-application-using-python-tkinter/
# https://www.geeksforgeeks.org/how-to-change-the-tkinter-label-font-size/
# https://d2mods.info/forum/kb/viewarticle?a=368
# https://d2mods.info/forum/kb/viewarticle?a=2
# https://d2mods.info/forum/kb/viewarticle?a=320