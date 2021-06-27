import csv
import random


TCDICT = {}
ARMORDICT = {}
WEAPDICT = {}
MISCDICT = {}
ITEMTYPESDICT = {}
ITEMRATIO = []
UNIQUES = []
SETS = []

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



# read itemtypes csv into dictionary
filepath = "data-113d/ItemTypes.txt"
with open(filepath, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter='\t', quotechar='"', skipinitialspace=True)
    for row in csv_reader:
        # the key-value contains 'name' redundantly.  row = {'name': 'Cap/hat', 'version': '0', ... }
        ITEMTYPESDICT[row['ItemType']] = row


def load_csv_to_list(path_in, list_in):
    with open(path_in, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter='\t', quotechar='"', skipinitialspace=True)
        for row in csv_reader:
            list_in.append(row)


# read itemratio csv rows into list (not dictionary like above)
filepath = "data-113d/itemratio.txt"
load_csv_to_list(filepath, ITEMRATIO)
# are the last 4 rows the only ones needed?   Uber and Class specific?

# read uniqueitems csv rows into list (not dictionary like above)
filepath = "data-113d/UniqueItems.txt"
load_csv_to_list(filepath, UNIQUES)

# read setitems csv rows into list (not dictionary like above)
filepath = "data-113d/SetItems.txt"
load_csv_to_list(filepath, SETS)


# # choice from a list with weighted probability
# random.choices(items, weights=probs, k=1)[0]

# debuggin with breakpoints -v'  I can see local vars in the function ~~~

def one_roll_from_tc(tc_name_str, players_str):
    """
    Return a random selection (based on Item Probs) from a row (Treasureclass)
    one_roll_from_tc('Andarielq (H)')
    Out[210]: 'Act 2 (H) Equip A'
    """
    rowdict = TCDICT[tc_name_str]
    items, probs = [], []

    try:
        players_int = int(players_str)
        if players_int < 1:
            players_int = 1
        elif players_int > 8:
            players_int = 8
    except:
        players_int = 1
    # no drop exponent.  /players 1 or 2 -> nd_exp 1,   3 or 4 -> nd_exp 2,    5 or 6 -> nd_exp 3,     7 or 8 -> nd_exp 4
    nd_exp = int(float(players_int)/2.0 + 0.5)
    
    for k,v in rowdict.items():
        if k.startswith("Item") and v:
            # add item to item list and probability to prob list
            items.append(v)
            probs.append(int(rowdict[f'Prob{len(items)}']))
    if rowdict['NoDrop']:
        nodrop_orig = int(rowdict['NoDrop'])
        sumprobs = sum(probs)
        probs_and_nd = nodrop_orig + sumprobs
        nodrop_final = (((nodrop_orig/probs_and_nd)**nd_exp)/(1-(nodrop_orig/probs_and_nd)**nd_exp))*sumprobs + 0.01
        
        items, probs = items + [''], probs + [int(nodrop_final)]

    # choice from a list with weighted probability
    outcome = random.choices(items, weights=probs, k=1)[0]
    
    return outcome


def final_roll_from_tc(tc_name_str, players_str):
    """
    weap18, weap48, armo60, armo6, weap12, amu, armo36   ~~~ drops work!  
    """
    while tc_name_str and tc_name_str in TCDICT:
        tc_name_str = one_roll_from_tc(tc_name_str, players_str)
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
    items, probs, levels, types = [], [], [], []
    for k,v in itemdict.items():
        if v['level'] and (lvl-3 < int(v['level']) <= lvl):
            items.append(v['name'])
            # account for rarity = '' in data.  probability is 1/rarity
            rarity = int(v['rarity']) if v['rarity'] else 1
            probs.append(1/rarity)
            levels.append(v['level'])
            types.append(v['type'])
    
    # choice from a list with weighted probability
    outcomeidx = random.choices(list(range(len(items))), weights=probs, k=1)[0]

    return items[outcomeidx], levels[outcomeidx], types[outcomeidx]

# TODO: when determining unique, set, rare, use the item code and lookup unique/set names  (# follow 'code', 'namestr', and 'name' columns)


def name_from_misc(item_str):
    out_name = "not found"
    for row in MISCDICT.values():
        if row['code'] == item_str:
            out_name = row['name'].title()
            level = row['level']
    
    return out_name, level



def name_from_armo_weap_misc(item_str, mf_str):
    """
    return an item name given armoX, weapX, or a misc. item string
    """
    type_str = item_str[0:4]
    if type_str in ['armo', 'weap']:
        out_name, level, itemtype = roll_from_armo_weap_lvl(item_str)
        # check for quality. unique, set, rare, magic.   out_name 'uni~ Balanced Knife'
        out_name, success = check_uni_or_set(out_name, level, is_class_specific(itemtype), mf_str, 'uni')
        
        if not success: 
            print(out_name, 'uni check failed. checking set')
            out_name, success = check_uni_or_set(out_name, level, is_class_specific(itemtype), mf_str, 'set')
            print(out_name, 'set check    >>>>>>>>>: ', success)

            # return rare quality
            if not success:
                out_name = 'rare~ ' + out_name

    # else misc    
    else:
        out_name, level = name_from_misc(item_str)
        # misc.txt has lvl>0 for ring, amu, charm, rune.  do not check uniques of gems, runes, ...
        if level and int(level) > 0 and "rune" not in out_name.lower():
            out_name, success = check_uni_or_set(out_name, level, False, mf_str, 'uni')
            ## TODO: charms are eigher gheeds or magic(blue)
            
            # print(out_name, 'success', success)
            if not success: 
                print(out_name, 'uni check failed. checking set')
                out_name, success = check_uni_or_set(out_name, level, False, mf_str, 'set')
                print(out_name, 'set check    >>>>>>>>>: ', success)

                ############ NEXT:     (for rings, amu, jewel, charm)
                # return rare quality
                name_lower = out_name.lower()
                if not success and ("jewel" in name_lower or "ring" in name_lower or "amulet" in name_lower or "charm" in name_lower):
                    out_name = 'rare~ ' + out_name
    
    return out_name


### Read in misc.txt.  assemble dict  'code' --> 'name'

# andy_str = 'Andarielq (H)'
# out = final_roll_from_tc(andy_str)
# name_from_armo_weap_misc(out)    # 'Twin Axe', 'Ring', 'Hard Leather Armor'



def is_class_specific(type_str):
    """
    class specific -- non-empty column "class" in ItemTypes.txt
    is_class_specific('abow') --> True
    """
    out = False
    for row in ITEMTYPESDICT.values():
        if row['Code'] == type_str and row['Class']:
            out = True
    return out


def check_uni_or_set(name_str, level_str, is_class_spec, mf_str='0', qual_type='uni'):
    """
    inputs ~ ('Balanced Knife', '13', False -- for 'tkni')
    normal vs elite check isn't needed for Andy. uni,set,rare,magic have same values (rows 4 and 5 in itemratio.txt)
    """
    # if roll_success, no need to check next quality (set, rare)
    roll_success = False
    # mon lvl looks in monstats.txt.  monstats['andariel']['LevelH'].  The TC name can be looked up here too
    # monlvl = TCDICT['Andarielq (H)']['level']  
    ilvl = 75  # monlvl  # hard coded for now
    qlvl = int(level_str)  # level column in armor/weapon.txt.  quality lvl of base item
    if is_class_spec:
        row = ITEMRATIO[4]    # 'Unique': '240'
    else:
        row = ITEMRATIO[2]    # 'Unique': '400'

    # (BaseChance - ((ilvl-qlvl)/Divisor)) * 128    https://www.purediablo.com/forums/threads/item-generation-tutorial.110/
    # this is not a 'probability', more like a 'chance number'
    if qual_type == 'uni':
        qual = int(row['Unique']) 
        qual_divisor = int(row['UniqueDivisor'])
        qual_min = int(row['UniqueMin'])
        qual_col = int(TCDICT['Andarielq (H)']['Unique'])     # Andy TC hard coded here
        # MF diminishing returns factor is 250 for unique, 500 for set and 600 for rare
        factor = 250
    elif qual_type == 'set':
        qual = int(row['Set']) 
        qual_divisor = int(row['SetDivisor'])
        qual_min = int(row['SetMin'])
        qual_col = int(TCDICT['Andarielq (H)']['Set'])     # Andy TC hard coded here
        factor = 500
    else:
        # quest drop always has success on rare item roll
        qual = int(row['Rare']) 
        qual_divisor = int(row['RareDivisor'])
        qual_min = int(row['RareMin'])
        qual_col = int(TCDICT['Andarielq (H)']['Rare'])     # Andy TC hard coded here
        factor = 600

    chance = (qual - ((ilvl-qlvl)/qual_divisor)) * 128
    # take abs() of mf if the input can be parsed to an int
    try: 
        mf = abs(int(mf_str))
    except:
        mf = 0
    effect_mf = mf*factor/(mf+factor)
    chance = (chance*100)/(100 + effect_mf)

    if chance < qual_min:
        chance = qual_min
    
    # uni_col = int(TCDICT['Andarielq (H)']['Unique'])     # Andy TC hard coded here
    chance = chance - (chance*qual_col/1024)

    if random.randrange(0, int(chance)) < 128:
        roll_success = True
        # either unique or failed unique. (and set/ failed set)
        ### TODO: charms either gheeds or magic(blue)
        out_str = check_if_qlvl_works(name_str, ilvl, qual_type)
    else:
        out_str = name_str
    
    return out_str, roll_success


def check_if_qlvl_works(name_str, ilvl, qual_type='uni'):
    """
    check for unique/set item's qlvl <= the monster lvl
    pick unique with probability according to it's rarity
    check_if_qlvl_works('spiderweb sash', 75)  -->  'failed uni/set'
    NOTE: crystal sword 'Azurewrath' can be output. this function doesn't check the 'enabled' col
    NOTE: typo fixed in UniqueItems.txt :      Razorswitch  --> Jo Stalf  -- Jo Staff
    typo: Gaunlets(H) -->  Gauntlets(H)
    CedarBow --> Cedar Bow
    Rimeraven --> Raven Claw   (and Rogue's Bow, Stormstrike changed)
    Tresllised Armor --> Trellised
    Doomspittle --> Doomslinger
    Kris --> Kriss
    Hunter’s Bow  --> replace single quote/ apostrophe

    Bracers(M) -- Bracers in uniqueitems (chance guards code 'mgl')
    Mindrend --> Skull Splitter
    """
    possible_items = []
    probs = []

    ### TODO: charms should be magic if not gheeds
    if "charm large" in name_str.lower():
        name_str = "charm"     # shows up as "Charm" in blue when other charms appear as "Charm large"
        
    if qual_type == 'uni':
        quallist = UNIQUES
        namecol = '*type'
        prefix = "uni~ "
    else:
        quallist = SETS
        namecol = '*item'
        prefix = "set~ "
    for row in quallist:
        # remove (H), (M), (L) from gauntlets, gloves, belt
        if row[namecol].lower().replace(' ','').replace("'","").replace("’","") == name_str.lower().split('(')[0].replace(' ', '').replace("'","").replace("’",""):
            print(row[namecol], row['lvl'])

            if row['lvl'] and int(row['lvl']) > 0 and int(row['lvl']) <= ilvl:
                if not 'cow king' in row['index'].lower():
                    possible_items.append(row['index'])
                    probs.append(int(row['rarity']))
    if possible_items:
        outname = prefix + random.choices(possible_items, weights=probs, k=1)[0]
    else:
        # undo the large charm rename from above
        if name_str == 'charm':
            name_str = 'Charm Large'
        outname = 'failed ' + prefix + name_str     # this should be rare or magic (for failed sets)

    return outname

### TODO:                
### check for set amulet if rarity logic is working


 




### NEXT
# loop for 7 trials with NoDrop.  if 6 items are dropped. end

# replacing the code in dropsim.py
# for i in range(5):
#     loot_list.append(name_from_armo_weap_misc(final_roll_from_tc(andy_str)))


### NEXT   (itemratio.txt, monstats needed for ilvl. andy can have fixed ilvl)
# Add text color for uniques, sets, rare, magic
# for each drop, have to specify the color 'fg' foreground.
# add Label() with row +1 in dropsim tkinter app

# function for dropping quality
# def drop_uni_set_rare()     'weap60' --> determine name.   Shako.  see if unique, set, rare is selected. and if item can be quality.
#                                              ring, ammy, jewel can be left as Unique (not determined further) for now

### add Andy image in Catacombs, dark background for the Loot list text






# https://courses.cs.washington.edu/courses/cse140/13wi/csv-parsing.html        
# The keys are the names of the columns (from the first row of the file, which is skipped over)


# Andarielq (H)

# load in treasureclassex.txt     maybe read csv?  would be nice to access columns by name  (convert to python table?)