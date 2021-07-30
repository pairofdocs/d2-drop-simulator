import csv
import random


TCDICT = {}
ARMORDICT = {}
WEAPDICT = {}
MISCDICT = {}
ITEMTYPESDICT = {}
MONSTATSDICT = {}
ITEMRATIO = []
UNIQUES = []
SETS = []
MISC_THROW_POTS = {
    "gps": {"name": "Rancid Gas Potion", "level": "32"},
    "ops": {"name": "Oil Potion", "level": "28"},
    "gpm": {"name": "Choking Gas Potion", "level": "20"},
    "opm": {"name": "Exploding Potion", "level": "16"},
    "gpl": {"name": "Strangling Gas Potion", "level": "8"},
    "opl": {"name": "Fulminating Potion", "level": "4"},
}
MONSTATSDICT_EXTRA = {
    "countess": {"Level": "11", "Level(N)": "45", "Level(H)": "82"}
}
seed_set = False


def load_csv_to_dict(path_in, dict_in, row_key):
    with open(path_in, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter='\t', quotechar='"', skipinitialspace=True)
        for row in csv_reader:
            # the key-value contains 'Treasure Class'/row_key redundantly.  row = {'Treasure Class': '', 'group': '', ... }
            dict_in[row[row_key]] = row


# read TCX csv into dictionary
filepath = "data-113d/TreasureClassEx.txt"
load_csv_to_dict(filepath, TCDICT, 'Treasure Class')

# read armor csv into dictionary
filepath = "data-113d/armor.txt"
load_csv_to_dict(filepath, ARMORDICT, 'name')
# ARMORDICT['Cap/hat']
# {'name': 'Cap/hat',
#  ...
#  'rarity': '1',
#  ...
#  'level': '1',

# read weapons csv into dictionary
filepath = "data-113d/weapons.txt"
load_csv_to_dict(filepath, WEAPDICT, 'name')
# WEAPDICT['War Staff']
#  {'name': 'War Staff',
#   'code': 'wst',
#   'namestr': 'wst',
#   'rarity': '2',
#   'level': '24'

# read misc csv into dictionary
filepath = "data-113d/misc.txt"
load_csv_to_dict(filepath, MISCDICT, 'name')
# MISCDICT['Emerald']
#  {'name': 'Emerald',
#   'code': 'gsg'

# read itemtypes csv into dictionary
filepath = "data-113d/ItemTypes.txt"
load_csv_to_dict(filepath, ITEMTYPESDICT, 'Code')  # index by 'Code' so I can reference ITEMTYPESDICT['Code']

# read monstats csv into dictionary
filepath = "data-113d/monstats.txt"
load_csv_to_dict(filepath, MONSTATSDICT, 'Id')


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


def one_roll_from_tc(tc_name_str, players_str):
    """
    Return a random selection (based on Item Probs) from a row (Treasureclass)
    one_roll_from_tc('Andarielq (H)')   picks 7    ---    Act 2 Equip A	19    	Act 2 Good	3
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
        ratio = (nodrop_orig/(nodrop_orig + sumprobs))**nd_exp
        nodrop_final = ((ratio)/(1-ratio))*sumprobs
        # do the dropcalcs take int() here? this could lead to diff avg drop %s, diff item drop %s.  item generation tutorial rounds 
        items, probs = items + [''], probs + [round(nodrop_final)]

    # choice from a list with weighted probability
    outcome = random.choices(items, weights=probs, k=1)[0]
    
    return outcome


def final_rolls_from_tc(tc_name_str, players_str, seed_str):
    """
    weap18, weap48, armo60, armo6, weap12, amu, armo36   ~~~ drops work!  
    roll multiple times if TCDICT inner has picks > 1.   if TCDICT has picks < 1 assemble a sequence of TCs and do nested rolls
    return outcomes list ~  ['weap12', 'weap12', 'weap12', 'armo9', 'armo15', 'weap12']  for 6 drops of 'Durielq - Base'
                            [{'rolleditemtc': 'armo18', 'rootclass': 'Durielq (N) - Base'}]         storing itemname and root TClass
                            [] for a noDrop outcome
    """
    global seed_set
    # set random seed if not set already. only set once for duration of app
    if seed_str and not seed_set:
        try:
            seedint = int(seed_str)
        except:
            seedint = 666
        random.seed(seedint)
        seed_set = True
    
    qboss = tc_name_str.split('(')[0].rstrip() in ['Andarielq', 'Durielq', 'Mephistoq', 'Diabloq', 'Baalq']
    
    outcomes = []         # store itemTC and TC class.  Needed for keeping the uni/set/rare mf values
    rootpicknum = int(TCDICT[tc_name_str]['Picks'])
    
    if rootpicknum < 0:
        # get inner TCs and probNums then roll in order  [TC1, TC1, TC2, TC2] and append to outcomes
        innertcs, rollnum, rollseq = [], [], []
        for k,v in TCDICT[tc_name_str].items():
            if k.startswith("Item") and v:
                # add item to item list and rollNum to prob list
                innertcs.append(v)
                rollnum.append(int(TCDICT[tc_name_str][f'Prob{len(innertcs)}']))
        # assemble sequence of TCs
        for i in range(len(innertcs)):
            rollseq += rollnum[i]*[innertcs[i]]   # ['Countess Item', 'Countess Rune']
        for tc_roll in rollseq[0:abs(rootpicknum)]:     # champs always drop 2 pots (Act x Cpot x gives 2),   uniques 4 pots (pick=-3)
            if len(outcomes) < 6:
                outcomes += nested_rolls_in_tc(tc_roll, players_str, qboss, positive_picks=False, neg_root_tc=tc_name_str)
        outcomes = outcomes[0:6] # take the first 6, remove any extra drops 
        
    else:  # rootpicknum > 0
        outcomes = nested_rolls_in_tc(tc_name_str, players_str, qboss, positive_picks=True, neg_root_tc='')

    return outcomes


def nested_rolls_in_tc(tc_name_str, players_str, qboss, positive_picks=True, neg_root_tc=''):
    """
    Nested picking from tc_name_str doing multiple picks (e.g. Duriel --> Duriel Base  and   Countess --> Countess Item and Rune)
    if negative picks are selected. a root_tc is input,  e.g. 'Countess'.  uni/set/rare qual values are used from this tc
    """
    # get first inner pick and pick number.  (remove 'mul='  if gld is picked)
    if positive_picks:
        tc_name_str1 = one_roll_from_tc(tc_name_str, players_str).split(',mul=')[0]
    else:
        tc_name_str1 = tc_name_str  # e.g. 'Countess Item'. one_roll_from_tc is not used since it randomly chooses a pick. a sequence of picks is used
    
    inner_pick_num = 0
    outcomes = []
    if tc_name_str1:
        if tc_name_str1 in TCDICT:
            rowdict = TCDICT[tc_name_str1]
            inner_pick_num = int(rowdict['Picks']) if rowdict['Picks'] else 1
        else:
            # 'tsc', 'gld' rolled and it's not a row in the TCDICT
            outcomes += [{'rolleditemtc': tc_name_str1, 'rootclass': tc_name_str}]       # when not 'Durielq - Base' rolled from Durielq

    for i in range(inner_pick_num):
        tc_name_during_pick = tc_name_str1
        # keep traversing Treasure classes.  limit of 6 items dropped from a monster  (detail left out: gold can be a 7th drop for qbosses)
        while tc_name_during_pick and tc_name_during_pick in TCDICT and len(outcomes) < 6:
            tc_name_during_pick = one_roll_from_tc(tc_name_during_pick, players_str).split(',mul=')[0]
        
        if tc_name_during_pick and len(outcomes) < 6:
            # need monster name in TC for 'Cow'. 
            # TODO:  this logic should be improved if using TC classes for uniques or regular monsters.  check if TCDICT has Unique val. Countess/ Council
            rootclass = neg_root_tc if neg_root_tc else tc_name_str   # for negative pick nums  use the input neg_root_tc string
            # if tc_name_str is a questboss
            if qboss:
                rootclass = tc_name_str if TCDICT[tc_name_str]['Unique'] else tc_name_str1      # if Unique qual values are in base TC, use it. else use 1st inner pick (duri - base)
            
            outcomes += [{'rolleditemtc': tc_name_during_pick, 'rootclass': rootclass}]
            # question: are multiple gold drops allowed? I think so, they get added to a 'gold pile' in-game
    return outcomes


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
    # probability -> itemtypes.txt rarity.  3 for axe.  1 for staves, ...   use ITEMTYPESDICT
    for k,v in itemdict.items():
        if v['level'] and (lvl-3 < int(v['level']) <= lvl):
            items.append(v['name'])
            # account for rarity = '' in data.  weapons.txt rarity is for chests.  look at itemtypes.txt
            try:
                rarity = int(ITEMTYPESDICT[v['type']]['Rarity'])  # e.g [3, 3, 3, 3, 3, 3, 1, 3, 3, 2, 1] for 'weap09'  axe-3, wristblade-2, orb-1
            except:
                rarity = 3  # default to 3 for normal (non class specific items)
                # print('Rarity not found in ITEMTYPEDICT')
            probs.append(rarity)
            levels.append(v['level'])
            types.append(v['type'])
    
    # choice from a list with weighted probability
    outcomeidx = random.choices(list(range(len(items))), weights=probs, k=1)[0]

    return items[outcomeidx], levels[outcomeidx], types[outcomeidx]


def name_from_misc(item_str):
    out_name = 'Misc'
    level = ''
    for row in MISCDICT.values():
        if row['code'] == item_str:
            out_name = row['name'].title()
            level = row['level']
    # use misc throwing potions (gas, oil small,med,large) name and level from weapons.txt
    if out_name == 'Misc':
        out_name = MISC_THROW_POTS[item_str]['name']
        level = MISC_THROW_POTS[item_str]['level']
    return out_name, level


def get_mlvl(mon_str):
    if mon_str.endswith(" - Base"):
        mon_str = mon_str.replace(" - Base", "")
    mon_name = mon_str.split(' (')[0].lower()
    if mon_name[0:4] == 'baal':
        mon_name = 'baalcrab'
    elif mon_name[0:3] == 'cow':    # account for 'Cow King' if he's added to the tclist
        mon_name = 'hellbovine'
    elif mon_name[0:7] == 'council':
        mon_name = 'councilmember1'

    mon_diffi = ('(' + mon_str.split(' (')[1]) if '(' in mon_str else ''  # '', '(N)', '(H)'
    mon_name = mon_name[0:-1] if mon_name.endswith('q') else mon_name
    if mon_name.lower().startswith('countess'):  # account for monsters not in monstats.txt
        mlvl = int(MONSTATSDICT_EXTRA['countess']['Level'+mon_diffi])
    else:
        mlvl = int(MONSTATSDICT[mon_name]['Level'+mon_diffi])

    return mlvl


def name_from_armo_weap_misc(item_str, mf_str, mon_str):
    """
    return an item name given armoX, weapX, or a misc. item string. mon_str ~ 'Andarielq (H)'
    """
    type_str = item_str[0:4]
    mlvl = get_mlvl(mon_str)
    if type_str in ['armo', 'weap']:
        out_name, level, itemtype = roll_from_armo_weap_lvl(item_str)
        # check for quality. unique, set, rare, magic.   out_name 'uni~ Balanced Knife'
        out_name, success = check_uni_or_set(out_name, level, is_class_specific(itemtype), mlvl, mon_str, mf_str, 'uni')
        
        if not success: 
            # print(out_name, 'uni check failed. checking set')
            out_name, success = check_uni_or_set(out_name, level, is_class_specific(itemtype), mlvl, mon_str, mf_str, 'set')
            # return rare quality
            if not success:
                out_name, success = check_uni_or_set(out_name, level, is_class_specific(itemtype), mlvl, mon_str, mf_str, 'rar')
                # check_rare roll, add magic~ or nonmagic~   (quest bosses and monsters logic will be same, referencing TC uni/set/rare col)
                if not success:
                    out_name, success = check_uni_or_set(out_name, level, is_class_specific(itemtype), mlvl, mon_str, mf_str, 'mag')
                    if not success:  
                        out_name = 'normal~ ' + out_name

    # else misc
    else:
        out_name, level = name_from_misc(item_str)
        # misc.txt has lvl>0 for ring, amu, charm, rune.  do not check uniques of gems, runes, ...
        if level and int(level) > 0 and "rune" not in out_name.lower():
            out_name, success = check_uni_or_set(out_name, level, False, mlvl, mon_str, mf_str, 'uni')

            if not success: 
                out_name, success = check_uni_or_set(out_name, level, False, mlvl, mon_str, mf_str, 'set')
                # return rare quality
                name_lower = out_name.lower()
                if not success and ("jewel" in name_lower or "ring" in name_lower or "amulet" in name_lower or "charm" in name_lower):
                    # check roll for rare, magic
                    out_name, success = check_uni_or_set(out_name, level, False, mlvl, mon_str, mf_str, 'rar')
                    if not success:
                        out_name = 'magic~ ' + out_name      # jewel, ring, ammy, charm must be magic if rare roll fails
    
    return out_name


def is_class_specific(type_str):
    """
    class specific -- non-empty column "class" in ItemTypes.txt
    is_class_specific('abow') --> True
    """
    class_str = ITEMTYPESDICT[type_str]['Class']
    return bool(class_str)


def check_uni_or_set(name_str, level_str, is_class_spec, mlvl_int, mon_str, mf_str='0', qual_type='uni'):
    """
    inputs ~ ('Balanced Knife', '13', False -- for 'tkni')
    normal vs elite check isn't needed for Andy. uni,set,rare,magic have same values (rows 4 and 5 in itemratio.txt)
    """
    # if roll_success, no need to check next quality (set, rare)
    roll_success = False
    # mon lvl looks in monstats.txt.  monstats['andariel']['LevelH'].  The TC name can be looked up here too
    # monlvl = TCDICT['Andarielq (H)']['level']  
    # ilvl = 75  # monlvl  # hard coded for now
    qlvl = int(level_str)  # level column in armor/weapon.txt.  quality lvl of base item
    if is_class_spec:
        row = ITEMRATIO[4]    # 'Unique': '240'
    else:
        row = ITEMRATIO[2]    # 'Unique': '400'

    if qual_type == 'uni':
        qual = int(row['Unique']) 
        qual_divisor = int(row['UniqueDivisor'])
        qual_min = int(row['UniqueMin'])
        qual_col = TCDICT[mon_str]['Unique']
        # MF diminishing returns factor is 250 for unique, 500 for set and 600 for rare
        factor = 250
    elif qual_type == 'set':
        qual = int(row['Set']) 
        qual_divisor = int(row['SetDivisor'])
        qual_min = int(row['SetMin'])
        qual_col = TCDICT[mon_str]['Set']
        factor = 500
    elif qual_type == 'rar':
        # quest drop always has success on rare item roll. This matches TCX values of 1024 for Rare, Magic cols
        qual = int(row['Rare']) 
        qual_divisor = int(row['RareDivisor'])
        qual_min = int(row['RareMin'])
        qual_col = TCDICT[mon_str]['Rare']
        factor = 600
    else:
        qual = int(row['Magic']) 
        qual_divisor = int(row['MagicDivisor'])
        qual_min = int(row['MagicMin'])
        qual_col = TCDICT[mon_str]['Magic']

    qual_col = int(qual_col) if qual_col else 0

    # (BaseChance - ((mlvl_int-qlvl)/Divisor)) * 128    https://www.purediablo.com/forums/threads/item-generation-tutorial.110/
    # this is not a 'probability', more like a 'chance number'
    chance = (qual - ((mlvl_int-qlvl)/qual_divisor)) * 128
    # take abs() of mf if the input can be parsed to an int
    try: 
        mf = abs(int(mf_str))
    except:
        mf = 0
    effect_mf = mf*factor/(mf+factor) if qual_type != 'mag' else mf
    chance = (chance*100)/(100 + effect_mf)

    if chance < qual_min:
        chance = qual_min
    
    chance = chance - (chance*qual_col/1024)

    if random.randrange(0, max(int(chance),1)) < 128:
        roll_success = True
        # either unique or failed unique. (and set/ failed set)  for quest drops.   non quest monsters can have uni, set, rare, magic, normal
        ### TODO: charms either gheeds or magic(blue)
        out_str = check_if_qlvl_works(name_str, mlvl_int, qual_type)
    else:
        out_str = name_str
    
    return out_str, roll_success


def check_if_qlvl_works(name_str, ilvl, qual_type='uni'):
    """
    check for unique/set item's qlvl <= the monster lvl (ilvl)
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
    quallist = None

    if "charm large" in name_str.lower():
        name_str = "charm"     # shows up as "Charm" in blue when other charms appear as "Charm large"
        
    if qual_type == 'uni':
        quallist = UNIQUES
        namecol = '*type'
        prefix = "uni~ "
    elif qual_type == 'set':
        quallist = SETS
        namecol = '*item'
        prefix = "set~ "
    elif qual_type == 'rar':
        prefix = "rare~ "
    else:
        prefix = "magic~ "

    if quallist:
        for row in quallist:
            # remove (H), (M), (L) from gauntlets, gloves, belt.   Careful with the .split('(')  if unique/set items have '(' this fails. I fixed the item names. removed "(" from uni,set
            if row[namecol].lower().replace(' ','').replace("'","").replace("’","") == name_str.lower().split('(')[0].replace(' ', '').replace("'","").replace("’",""):
                # print(row[namecol], row['lvl'])
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
        if qual_type in ['uni', 'set']:
            outname = 'failed ' + prefix + name_str     # this should be rare or magic (for failed sets)
        else:
            outname = prefix + name_str

    return outname
