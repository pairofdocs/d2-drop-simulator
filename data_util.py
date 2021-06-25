import csv
import random
from tkinter import DoubleVar

TCDICT = {}
ARMORDICT = {}
WEAPDICT = {}
MISCDICT = {}

# read TCX csv into dictionary
filepath = "data-113d/TreasureClassEx.txt"
with open(filepath, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter='\t', quotechar='"', skipinitialspace=True)
    for row in csv_reader:
        # the key-value contains 'Treasure Class' redundantly.  row = {'Treasure Class': '', 'group': '', ... }
        TCDICT[row['Treasure Class']] = row
        
# TCDICT['Andarielq (H)']
# TCDICT['Andarielq (H)']['Picks']
# TCDICT['Andarielq (H)']['NoDrop']

# read armor csv into dictionary
filepath = "data-113d/armor.txt"
with open(filepath, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter='\t', quotechar='"', skipinitialspace=True)
    for row in csv_reader:
        # the key-value contains 'name' redundantly.  row = {'name': 'Cap/hat', 'version': '0', ... }
        ARMORDICT[row['name']] = row

# ARMORDICT['Cap/hat']
# {'name': 'Cap/hat',
#  ...
#  'rarity': '1',
#  ...
#  'level': '1',


# read weapons csv into dictionary
filepath = "data-113d/weapons.txt"
with open(filepath, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter='\t', quotechar='"', skipinitialspace=True)
    for row in csv_reader:
        # the key-value contains 'name' redundantly.  row = {'name': 'Cap/hat', 'version': '0', ... }
        WEAPDICT[row['name']] = row

# WEAPDICT['War Staff']
#  {'name': 'War Staff',
#   'code': 'wst',
#   'namestr': 'wst',
#   'rarity': '2',
#   'level': '24'


# read misc csv into dictionary
filepath = "data-113d/misc.txt"
with open(filepath, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter='\t', quotechar='"', skipinitialspace=True)
    for row in csv_reader:
        # the key-value contains 'name' redundantly.  row = {'name': 'Cap/hat', 'version': '0', ... }
        MISCDICT[row['name']] = row

# MISCDICT['Emerald']
#  {'name': 'Emerald',
#   'code': 'gsg'


# # choice from a list with weighted probability
# random.choices(items, weights=probs, k=1)[0]

# debuggin with breakpoints -v'  I can see local vars in the function ~~~

def one_roll_from_tc(tc_name_str):
    """
    Return a random selection (based on Item Probs) from a row (Treasureclass)
    one_roll_from_tc('Andarielq (H)')
    Out[210]: 'Act 2 (H) Equip A'
    """
    rowdict = TCDICT[tc_name_str]
    items, probs = [], []
    for k,v in rowdict.items():
        if k.startswith("Item") and v:
            # add item to item list and probability to prob list
            items.append(v)
            probs.append(int(rowdict[f'Prob{len(items)}']))

    # choice from a list with weighted probability
    outcome = random.choices(items, weights=probs, k=1)[0]
    
    return outcome

# andy_str = 'Andarielq (H)'
# one_roll_from_tc(andy_str)

def final_roll_from_tc(tc_name_str):
    """
    weap18, weap48, armo60, armo6, weap12, amu, armo36   ~~~ drops work!  
    """
    while tc_name_str in TCDICT:
        tc_name_str = one_roll_from_tc(tc_name_str)
    return tc_name_str


def roll_from_armo_weap_lvl(item_str):
    """
    armo6 (or weap6) -->  all rows from armor.txt (or weapons.txt) with level 4,5,6 (2 levels below and current level)
    take into account rarity when picking an item from a list
    e.g. 'armo60'  contains: Embossed Plate, Mage Plate, Shako, Heater, Wyrmhide Boots, Carnage Helm, Minion Skull
    """
    type_str = item_str[0:4]
    if type_str == "armo":
        itemdict = ARMORDICT
    else:
        itemdict = WEAPDICT
    lvl = int(item_str[4:])
    items, probs = [], []
    for k,v in itemdict.items():
        if v['level'] and (lvl-3 < int(v['level']) <= lvl):
            items.append(v['name'])
            # account for rarity = '' in data.  probability is 1/rarity
            rarity = int(v['rarity']) if v['rarity'] else 1
            probs.append(1/rarity)  
    
    # choice from a list with weighted probability
    outcome = random.choices(items, weights=probs, k=1)[0]

    return outcome

# TODO: when determining unique, set, rare, use the item code and lookup unique/set names  (# follow 'code', 'namestr', and 'name' columns)


def name_from_misc(item_str):
    out_name = "not found"
    for row in MISCDICT.values():
        if row['code'] == item_str:
            out_name = row['name'].title()
    
    return out_name



def name_from_armo_weap_misc(item_str):
    """
    return an item name given armoX, weapX, or a misc. item string
    """
    type_str = item_str[0:4]
    if type_str in ['armo', 'weap']:
        out_name = roll_from_armo_weap_lvl(item_str)
    else:
        out_name = name_from_misc(item_str)
    
    return out_name

### Read in misc.txt.  assemble dict  'code' --> 'name'

# andy_str = 'Andarielq (H)'
# out = final_roll_from_tc(andy_str)
# name_from_armo_weap_misc(out)    # 'Twin Axe', 'Ring', 'Hard Leather Armor'


### NEXT
# loop for 7 trials with NoDrop.  if 6 items are dropped. end

# replacing the code in dropsim.py
# for i in range(5):
#     loot_list.append(name_from_armo_weap_misc(final_roll_from_tc(andy_str)))


### NEXT
# Add text color for uniques, sets, rare, magic
# for each drop, have to specify the color 'fg' foreground.
# add Label() with row +1 in dropsim tkinter app

# function for dropping quality
# def drop_uni_set_rare()     'weap60' --> determine name.   Shako.  see if unique, set, rare is selected. and if item can be quality.


### add Andy image in Catacombs, dark background for the Loot list text






# https://courses.cs.washington.edu/courses/cse140/13wi/csv-parsing.html        
# The keys are the names of the columns (from the first row of the file, which is skipped over)


# Andarielq (H)

# load in treasureclassex.txt     maybe read csv?  would be nice to access columns by name  (convert to python table?)