
import logging

from tkinter import *
from playsound import playsound

from data_util import final_rolls_from_tc, name_from_armo_weap_misc

# log drops to file
logging.basicConfig(filename='session.txt', filemode='w', format='%(message)s', level=logging.INFO)


DIFFICULTIES = {'Normal': '', 'Nightmare': ' (N)', 'Hell': ' (H)'}
TCNames = ['Andariel', 'Duriel', 'Mephisto', 'Diablo', 'Baal', 'Cow', 'Countess', 'Council']  # can add Pindle, Eldrich
TCPicks = {TCNames[0]: 7,
           TCNames[1]: 5,
           TCNames[2]: 7,
           TCNames[3]: 7,
           TCNames[4]: 7,  # this data is from TreasureClassEx.txt
           TCNames[5]: 1,
           TCNames[6]: 1,  # Countess. pick 1 for negative pickNum, logic in data_util reads -pickNum and outputs list of outcomes}
           TCNames[7]: 3}  # Trav council.  councilmember2 in monstats.txt
BOSS_IMGS = {TCNames[0]: "./img/andy-d2r-resize.png",
             TCNames[1]: "./img/duri-d2r-resize2.png",
             TCNames[2]: "./img/meph-d2r-resize2.png",
             TCNames[3]: "./img/diab-d2r-resize2.png",
             TCNames[4]: "./img/baal-d2r-resize2.png",
             TCNames[5]: "./img/cowlvl-d2r-resize2.png",
             TCNames[6]: "./img/countess-d2r-resize2.png",
             TCNames[7]: "./img/council-d2r-resize2.png"}
             # Need an HD baal pic. use Arreat summit image?

# root window
root = Tk()

# root window title and dimension (width x height)
root.title("Bossq and Monster Drop Simulator")
root.geometry('640x480')


# function to display loot
num_runs = 0
running_once = True
def run_clicked():
    global num_runs, runx

    # run x times logic. do not play sound if running >1
    try:
        xtimes = max(int(runx.get()),1)  # if neg. int, xtimes -> 1
        running_once = False if xtimes > 1 else True
    except:
        xtimes, running_once = 1, True

    # boss selected from a dropdown: boss.get().  e.g.  'Andariel', 'Cow', ...
    mon_str = boss.get()
    if mon_str in TCNames[0:5]:
        mon_str += 'q' + DIFFICULTIES[diffi.get()]
    else:
        mon_str += DIFFICULTIES[diffi.get()]

    players_str = txt.get()
    mf_str = txtmf.get()
    seed_str = txtseed.get()
    lbl3.configure(text = "Loot:")
        
    for r in range(xtimes):
        num_runs += 1
        logging.info(f"{num_runs})")
        drops = [] # 6 items at most.  7 picks from bosses
        # clean all previous drops
        for i in range(6):
            loot_labels[i].configure(text = '', fg = '#f5f5f5')

        for i in range(TCPicks[boss.get()]):  # bosses have pick = 7, cows pick = 1
            if len(drops) == 6:
                break
            # output is [] if NoDrop.  else ~ [{'rolleditemtc': 'armo18', 'rootclass': 'Durielq (N) - Base'}...]
            loot_items = final_rolls_from_tc(mon_str, players_str, seed_str)
            loot_items = [name_from_armo_weap_misc(it['rolleditemtc'], mf_str, it['rootclass']) for it in loot_items]   # expanded item names
            if loot_items:
                for loot_item in loot_items:
                    if len(drops) < 6:
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
            elif "magic~" in loot_item:
                if 'potion' in loot_item.lower():
                    loot_labels[i].configure(text = loot_item.replace('magic~ ',''), fg = '#f5f5f5')  # default gray
                else:
                    loot_labels[i].configure(text = loot_item.replace('magic~ ',''), fg = '#8f82ff')  # magic/blue
            elif "normal~" in loot_item:
                loot_labels[i].configure(text = loot_item.replace('normal~ ',''), fg = '#f5f5f5')  # default gray
                    
            elif ("essence of" in loot_item.lower() or " rune" in loot_item.lower() or "key of" in loot_item.lower() or "puzzlebox" in loot_item.lower()):
                loot_labels[i].configure(text = loot_item, fg = '#eb721c')
                logging.info(f"{loot_item}")
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
        if sound_btn.config('relief')[-1] == 'sunken' and running_once:
            playsound('./sound/dropsound.mp3', False)


# background image
def draw_bckgrd(boss_str=TCNames[0]):
    global bckgrd_image, bckgrd_label
    bckgrd_image = PhotoImage(file=BOSS_IMGS[boss_str])
    bckgrd_label = Label(root, image=bckgrd_image)
    bckgrd_label.place(x=0, y=34, relwidth=1, relheight=1)

draw_bckgrd()

# Run button
btn = Button(root, text = "Run x times", width=9, fg = "red", command=run_clicked, font=('Segoe UI', 10))
# set button grid
btn.grid(column=0, row=0)

# players setting
lbl1 = Label(root, text = "/players", font=('Segoe UI', 10), width=15)
lbl1.grid(column=1, row=0)
# players entry field
txt = Entry(root, width=4, font=('Segoe UI', 10))
txt.insert(0, "1")
txt.grid(column=2, row=0)

# MF settings and run x field
def draw_mf_runx_settings(mf_str="0", runx_str="1"):
    global lbl2, txtmf, runx
    lbl2 = Label(root, text = "+Magic Find", font=('Segoe UI', 10), width=15)
    lbl2.grid(column=1, row=1)
    # entry field
    txtmf = Entry(root, width=4, font=('Segoe UI', 10))
    txtmf.insert(0, mf_str)
    txtmf.grid(column=2, row=1)
    # run x times entry field
    runx = Entry(root, width=8, font=('Segoe UI', 10))
    runx.insert(0, runx_str)
    runx.grid(column=0, row=1)

draw_mf_runx_settings()

# difficulty settings dropdown
diffi = StringVar(root)
diffi.set(list(DIFFICULTIES.keys())[2]) # default value
w = OptionMenu(root, diffi, *DIFFICULTIES)
w.configure(width=10, font=('Segoe UI', 9))
w.grid(column=3, row=0)


def change_bkgrd_and_draw_labels(*args):
    prev_mf, prev_runx = txtmf.get(), runx.get()
    draw_bckgrd(boss.get())
    # redraw MF label. it's cut off once background image is drawn
    draw_mf_runx_settings(prev_mf, prev_runx)
    # redraw loot labels if boss dropdown callback is used. Had issue where duriel -> duriel click would remove the loot labels from FOV
    draw_lootlabels()
    # # play sound andy, duri, meph, diablo. The audio beginning is abrupt
    # playsound('./sound/andy-fear-me.mp3')


# bosses settings dropdown
boss = StringVar(root)
boss.set(TCNames[0])
wboss = OptionMenu(root, boss, *TCNames)
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
# seed entry field
txtseed = Entry(root, width=4, font=('Segoe UI', 10))
txtseed.insert(0, "")
txtseed.grid(column=7, row=0)


root.mainloop()
