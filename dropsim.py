
import logging

from tkinter import *
from playsound import playsound

from data_util import final_roll_from_tc, name_from_armo_weap_misc

# log drops to file
logging.basicConfig(filename='session.txt', filemode='w', format='%(message)s', level=logging.INFO)


DIFFICULTIES = {'Normal': '', 'Nightmare': ' (N)', 'Hell': ' (H)'}
BOSSES = ['Andariel', 'Duriel', 'Mephisto', 'Diablo', 'Baal']
BOSS_IMGS = {BOSSES[0]: "./img/andy-d2r-resize.png",
             BOSSES[1]: "./img/duri-d2r-resize2.png",
             BOSSES[2]: "./img/meph-d2r-resize2.png",
             BOSSES[3]: "./img/diab-d2r-resize2.png",
             BOSSES[4]: "./img/arreat-d2r-resize2.png"}
             # Need an HD baal pic. use Arreat summit image?

# root window
root = Tk()

# root window title and dimension (width x height)
root.title("Boss Quest Drop Simulator")
root.geometry('640x480')


# function to display loot
num_runs = 0
def run_clicked():
    global num_runs
    num_runs += 1
    logging.info(f"{num_runs})")

    # boss selected from a dropdown: boss.get().  e.g.  'Andariel'
    mon_str = boss.get() + 'q' + DIFFICULTIES[diffi.get()]
    players_str = txt.get()
    mf_str = txtmf.get()
    seed_str = txtseed.get()
    drops = [] # 6 items at most.  7 picks from bosses
    
    lbl3.configure(text = "Loot:")
    # clean all previous drops
    for i in range(6):
        loot_labels[i].configure(text = '', fg = '#f5f5f5')

    for i in range(7):
        if len(drops) == 6:
            break
        loot_item = final_roll_from_tc(mon_str, players_str, seed_str)   # output is '' if NoDrop
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

    # play drop sound
    if sound_btn.config('relief')[-1] == 'sunken':
        playsound('./sound/dropsound.mp3', False)


# background image
def draw_bckgrd(boss_str=BOSSES[0]):
    global bckgrd_image, bckgrd_label
    bckgrd_image = PhotoImage(file=BOSS_IMGS[boss_str])
    bckgrd_label = Label(root, image=bckgrd_image)
    bckgrd_label.place(x=0, y=34, relwidth=1, relheight=1)

draw_bckgrd()

# Run button
btn = Button(root, text = "Run" , fg = "red", command=run_clicked, font=('Segoe UI', 10))
# set button grid
btn.grid(column=0, row=0)

# players setting
lbl1 = Label(root, text = "/players", font=('Segoe UI', 10), width=15)
lbl1.grid(column=1, row=0)
# players entry Field
txt = Entry(root, width=4, font=('Segoe UI', 10))
txt.insert(0, "1")
txt.grid(column=2, row=0)

# MF settings
def draw_mf_settings(mf_str="0"):
    global lbl2, txtmf
    lbl2 = Label(root, text = "+Magic Find", font=('Segoe UI', 10), width=15)
    lbl2.grid(column=1, row=1)
    # entry Field
    txtmf = Entry(root, width=4, font=('Segoe UI', 10))
    txtmf.insert(0, mf_str)
    txtmf.grid(column=2, row=1)

draw_mf_settings()

# difficulty settings dropdown
diffi = StringVar(root)
diffi.set(list(DIFFICULTIES.keys())[2]) # default value
w = OptionMenu(root, diffi, *DIFFICULTIES)
w.configure(width=10, font=('Segoe UI', 9))
w.grid(column=3, row=0)


def change_bkgrd_and_draw_labels(*args):
    prev_mf = txtmf.get()
    draw_bckgrd(boss.get())
    # redraw MF label. it's cut off once background image is drawn
    draw_mf_settings(prev_mf)
    # redraw loot labels if boss dropdown callback is used. Had issue where duriel -> duriel click would remove the loot labels from FOV
    draw_lootlabels()
    # # play sound andy, duri, meph, diablo. The audio beginning is abrupt
    # playsound('./sound/andy-fear-me.mp3')


# bosses settings dropdown
boss = StringVar(root)
boss.set(BOSSES[0])
wboss = OptionMenu(root, boss, *BOSSES)
wboss.configure(width=10, font=('Segoe UI', 9))
wboss.grid(column=4, row=0)
# when boss dropdown value is changed draw the background and labels
boss.trace('w', change_bkgrd_and_draw_labels)


def draw_lootlabels():
    global lbl3, lbl5, lbl6, lbl7, lbl8, lbl9, lbl10, loot_labels

    # instructions label and loot output
    lbl3 = Label(root, text = "Ready to Farm? Click 'Run'", width=27, font=('Segoe UI', 10), fg='#f5f5f5', bg='#242020')
    lbl3.place(x=340, y=130+23)

    # rows for loot drops. 6 loot rows total
    # lbl4 = Label(root, text = "", width=27, font=('Segoe UI', 10), fg='#f5f5f5', bg='#242020')
    # lbl4.place(x=340, y=130+23)
    lbl5 = Label(root, text = "", width=27, font=('Segoe UI', 10), fg='#f5f5f5', bg='#242020')
    lbl5.place(x=340, y=130+23*2)
    lbl6 = Label(root, text = "", width=27, font=('Segoe UI', 10), fg='#f5f5f5', bg='#242020')
    lbl6.place(x=340, y=130+23*3)
    lbl7 = Label(root, text = "", width=27, font=('Segoe UI', 10), fg='#f5f5f5', bg='#242020')
    lbl7.place(x=340, y=130+23*4)
    lbl8 = Label(root, text = "", width=27, font=('Segoe UI', 10), fg='#f5f5f5', bg='#242020')
    lbl8.place(x=340, y=130+23*5)
    lbl9 = Label(root, text = "", width=27, font=('Segoe UI', 10), fg='#f5f5f5', bg='#242020')
    lbl9.place(x=340, y=130+23*6)
    lbl10 = Label(root, text = "", width=27, font=('Segoe UI', 10), fg='#f5f5f5', bg='#242020')
    lbl10.place(x=340, y=130+23*7)

    loot_labels = [lbl5, lbl6, lbl7, lbl8, lbl9, lbl10]

draw_lootlabels()


# drop sound toggle button. Used above in run_clicked()
def toggle_sound():
    if sound_btn.config('relief')[-1] == 'sunken':
        sound_btn.config(relief="raised", fg='black')
        sound_btn.config(text="Sound Off")
    else:
        sound_btn.config(relief="sunken", fg='#4ac936')  # green
        sound_btn.config(text="Sound On")

sound_btn = Button(text="Sound Off", width=8, relief="raised", command=toggle_sound)
sound_btn.grid(column=5, row=0)

# random seed setting
lblseed = Label(root, text = "Seed", font=('Segoe UI', 10), width=7)
lblseed.grid(column=6, row=0)
# seed entry Field
txtseed = Entry(root, width=4, font=('Segoe UI', 10))
txtseed.insert(0, "")
txtseed.grid(column=7, row=0)


root.mainloop()


### Possible TODO: 'run X times'
# 100 andy runs with one click. then see the Loot!
# add a scroll window. how would i add colored text?
