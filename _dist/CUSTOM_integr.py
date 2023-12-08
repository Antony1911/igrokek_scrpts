import os
import xml.etree.ElementTree as ET
import os.path
import PySimpleGUI as sg
import shutil
import random
import time
from colorama import Back, Style, Fore
sg.theme('DarkGrey13')

#=========================================================
# SETUP
#=========================================================
def Ask_Path(): 
    layout = [
        [sg.Text("[WFPC_master] path", text_color='yellow')],
        [sg.InputText(default_text = r"e:\\partner_WPC\\wfpc_mrg\\main", key = "-MASTER-"),sg.FolderBrowse()],
        [sg.Text("Temp Folder", text_color='yellow')],
        [sg.InputText(default_text = r"d:\\temp_custom", key = "-MOD-"), sg.FolderBrowse()],
        [sg.OK(key='OK'), sg.Cancel()]
    ]
    window = sg.Window('\U0001f638 integCustomWeapon', layout)

    while True:
        event, values = window.read(close=True)
        
        # MERS
        mersList = {"ar":"R", "sr":"S","shg":"M","smg":"E", "kn":"MERS", "pt":"MERS"}
        
        # ---------------------------------
        custom = values["-MOD-"] + '\\Game\\Objects\\Weapons\\'
        for _,dirs,_ in os.walk(custom):
            # dirs = dirs
            for i in dirs:
                values_custom = i
            break
        # ---------------------------------
        hashable = values_custom.strip('0123456789')
        
        print(values['-MOD-'])
        print('----'*13)
        print(gSpace + "new custom = " + values_custom)
        print(gSpace + f"weapon type = {hashable}")
        
        mers =  mersList[hashable]
        
        master, mod_repo, custom_Weapon = values["-MASTER-"], values["-MOD-"], values_custom
        if event == 'OK':
            return master, mod_repo, custom_Weapon, mers
        if event in ('Cancel', None) or event == sg.WIN_CLOSED:
            break
        
    window.close()
#---------------------------------------------------------
def random_BoxPistol(BoxPistol):
    lenboxpistol = len(BoxPistol[mers])
    time.sleep(0.125)
    randomNum = random.randint(0, lenboxpistol) 
    time.sleep(0.125)
    randomPistol = BoxPistol[mers][randomNum-1]
    time.sleep(0.125)
    print(gSpace + f'mers = {mers}')
    print(gSpace + f"lenboxpistol = {lenboxpistol}")
    print(gSpace + f"randomBoxPistol = {randomPistol}")
    return randomPistol
#---------------------------------------------------------
def list_to_string(l):
    str1 = '\n'
    return (str1.join(l))
#---------------------------------------------------------
def fileStructure(createTempFolders):

    def check_and_create(pppath):
        if os.path.exists(pppath) == True:
            pass
        else:
            os.makedirs(pppath)
    
    def copyFile(temp, master):
        if os.path.exists(temp):
            pass
        else:
            shutil.copyfile(master, temp)
    
    for tempFolder in createTempFolders:
        check_and_create(tempFolder)
    
    # WeaponFilter
    copyFile(temp_ItemsFilter_weapon, master_ItemsFilter_weapon)
    # RandomboxFilter
    copyFile(temp_ItemsFilter_randombox, master_ItemsFilter_randombox)
    # CardFilter
    copyFile(temp_ItemsFilter_cards, master_ItemsFilter_cards)
    # UI
    copyFile(temp_UIweaponsItemsIcons, master_UIweaponsItemsIcons)
    copyFile(temp_UIattachmentsItemsIcons, master_UIattachmentsItemsIcons)
    copyFile(temp_UIrandomBoxesIcons, master_UIrandomBoxesIcons)
    copyFile(temp_UIchallengesIcons, master_UIchallengesIcons)
    copyFile(temp_UICombatLogIcons, master_UICombatLogIcons)
    copyFile(temp_UIcards, master_UIcards)
    # Animation
    copyFile(temp_Animations_cba, master_Animations_cba)
    # MasterServerCards
    copyFile(temp_card_progressions_01, master_card_progressions_01)
    copyFile(temp_card_progressions_02, master_card_progressions_02)
    copyFile(temp_card_progressions_03, master_card_progressions_03)   
    # catalog_offers_IGR
    copyFile(temp_catalog_offers_IGR, master_catalog_offers_IGR)
#---------------------------------------------------------
def remove_lastline(path):
    fd=open(path,"r")
    d=fd.read()
    fd.close()
    m=d.split("\n")
    s="\n".join(m[:-1])
    fd=open(path,"w+")
    for i in range(len(s)):
        fd.write(s[i])
    fd.close()
#---------------------------------------------------------
def writeChanges(path, template):
    try:
        open(path, 'a').close()
        open(path, 'r+').write(template)
        print(Fore.GREEN + f"Complete... {path}" + Style.RESET_ALL + Fore.BLUE + " ...Added" + Style.RESET_ALL)
    except:
        print(Fore.RED + f"---FAILED... {path}" + Style.RESET_ALL)
#---------------------------------------------------------
def modifyChanges(path, template, prompt01, prompt02):
    
    file = open(path)
    item = prompt01 + custom_Weapon + prompt02
    try:
        if (item in file.read()):
            print(Fore.YELLOW + f"--- WARNING...  {item} in {path}  ...already exists" + Style.RESET_ALL)
        else:
            remove_lastline(path)
            with open(path, 'a') as f:
                f.writelines(template)
            f.close()
            print(Fore.GREEN + f"Complete... {path}" + Style.RESET_ALL + Fore.MAGENTA + " ...Modified" + Style.RESET_ALL)
    except:
        print(Fore.RED + f"---FAILED... {path}" + Style.RESET_ALL)
#---------------------------------------------------------
def get_repair_cost(path):
    try:
        root = ET.parse(path).getroot()
        for elem in root.find('mmo_stats').findall('param'):
            if elem.attrib['name'] == "repair_cost":
                value = elem.attrib['value']
                print(f"{gSpace}... {custom_Weapon} repair_cost = {value}")
                return value
    except FileNotFoundError:
        print(Fore.RED + f"--- FileNotFoundError... {path}" + Style.RESET_ALL)
#---------------------------------------------------------
def get_grep(path):
    temp = [0]
    for inroot,_,files in os.walk(path):
        for file in files:
            if ".xml" in file:
                path01 = os.path.join(inroot,file)
                # print(f"path01 = {path01}")
                root = ET.parse(path01).getroot()
                a = int(root.attrib['id'])
                # print(f"id = {a}")
                if temp[0] < a:
                    temp.clear()
                    temp.append(a)
        break
    print("last grep", temp[0])
    return str(temp[0] + 1)
#---------------------------------------------------------


#---------------------------------------------------------
# Items + Achievements
#---------------------------------------------------------
def custom_ItemRandomBox(contentList):
    
    randomPistol = random_BoxPistol(BoxPistol)
    
    pattern_ItemRandomBox = f"""<shop_item name="box_{custom_Weapon}" type="random_box">
	<mmo_stats>
		<param name="item_category" value="RandomBox"/>
		<param name="shopcontent" value="1"/>
		<param name="classes" value="RESMH"/>
		<param name="max_buy_amount" value="32000" />
		<param name="stackable" value="1" />
	</mmo_stats>
	<UI_stats>
		<param name="name" value="@box_{custom_Weapon}_name"/>
		<param name="description" value="@box_1_item_desc"/>
		<param name="icon" value="icons_randombox_{custom_Weapon}"/>
	</UI_stats>
	<random_box>
		<group>
			<item name="{custom_Weapon}_shop" weight="10"/>
            <item name="{randomPistol}" weight="10"/>
			<item name="{custom_Weapon}_shop" expiration="3h" weight="180"/>
			<item name="{contentList[0]}" expiration="3h" weight="160"/>
			<item name="{contentList[1]}" expiration="3h" weight="160"/>
			<item name="{contentList[2]}" expiration="3h" weight="160"/>
			<item name="{contentList[3]}" expiration="3h" weight="160"/>
			<item name="{contentList[4]}" expiration="3h" weight="160"/>
		</group>
	</random_box>\n</shop_item>"""

    writeChanges(temp_ShopItemsBox, pattern_ItemRandomBox)
#---------------------------------------------------------
def custom_ItemRandomboxBoxCard():
    
    pattern_ItemRandomboxBoxCard = f"""<shop_item name="box_{custom_Weapon}_card" type="random_box">
	<mmo_stats>
		<param name="item_category" value="RandomBox"/>
		<param name="shopcontent" value="1"/>
		<param name="classes" value="RESMH"/>
		<param name="max_buy_amount" value="32000"/>
		<param name="stackable" value="1"/>
	</mmo_stats>
	<UI_stats>
		<param name="name" value="@box_{custom_Weapon}_cards_name"/>
		<param name="description" value="@box_2_item_desc"/>
		<param name="icon" value="icons_randombox_{custom_Weapon}_cards"/>
	</UI_stats>
	<random_box>
		<group>
			<item name="{custom_Weapon}_card" amount="1000" weight="5"/>
			<item name="{custom_Weapon}_card" amount="500" weight="6"/>
			<item name="{custom_Weapon}_card" amount="250" weight="7"/>
			<item name="{custom_Weapon}_card" amount="100" weight="10"/>
			<item name="{custom_Weapon}_card" amount="50" weight="11"/>
			<item name="{custom_Weapon}_card" amount="25" weight="25"/>
			<item name="{custom_Weapon}_card" amount="10" weight="70"/>
			<item name="{custom_Weapon}_card" amount="5" weight="400"/>
			<item name="{custom_Weapon}_card" amount="1" weight="466"/>
		</group>
		<group>
			<item name="{custom_Weapon}_shop" expiration="3h" weight="33"/>
			<item name="{custom_Weapon}_shop" expiration="6h" weight="32"/>
			<item name="{custom_Weapon}_shop" expiration="9h" weight="30"/>
			<item name="{custom_Weapon}_shop" expiration="12h" weight="28"/>
			<item name="{custom_Weapon}_shop" expiration="18h" weight="22"/>
			<item name="{custom_Weapon}_shop" expiration="1d" weight="10"/>
		</group>
	</random_box>\n</shop_item>"""

    writeChanges(temp_ShopItemsBoxCard, pattern_ItemRandomboxBoxCard)
#---------------------------------------------------------
def custom_ItemCard():
    
    pattern_ItemCard = f"""<shop_item name="{custom_Weapon}_card" type="card">
  <mmo_stats>
    <param name="item_category" value="Card" />
    <param name="shopcontent" value="1" />
    <param name="max_buy_amount" value="32000" />
    <param name="stackable" value="1" />
    <param name="priority" value="1" />
    <param name="classes" value="{mers}"/>
  </mmo_stats>
  <UI_stats>
    <param name="name" value="@{custom_Weapon}_card_name" />
    <param name="description" value="@{custom_Weapon}_card_desc" />
    <param name="icon" value="icons_{custom_Weapon}_template" />
  </UI_stats>\n</shop_item>"""
    
    writeChanges(temp_ItemsCards, pattern_ItemCard)
#---------------------------------------------------------
def custom_Achievements():
    
    # idNumber = int(sg.popup_get_text(f"{temp_configAchievements}\n grep_id...", default_text=12345678))
    idNumber = get_grep(master_achievements)
    print(gSpace + 'Achievements grep_id = ' + str(idNumber))
    
    pattern_Achievements = f"""<Achievement active="1" id="{idNumber}" kind="kills" MS_side="0" amount="1500">
	<UI name="@{custom_Weapon}_Kill" desc="@{custom_Weapon}_Kill_desc"/>
	<Filters>
		<Filter kind="enemy" param="1"/>
		<Filter kind="weapon" param="{custom_Weapon}_shop"/>
		<Filter kind="claymore" param="0"/>
		<Filter kind="grenade" param="0"/>
		<Filter kind="kill_zone" param="0"/>
		<Filter kind="explosion" param="0"/>
	</Filters>
	<BannerImage image="challenge_stripe_{custom_Weapon}" type="stripe"/>\n</Achievement>"""
    
    writeChanges(temp_configAchievements, pattern_Achievements)
#---------------------------------------------------------
def integrate_Items():
    custom_ItemRandomBox                ([
        content_Randombox[mers][0],
        content_Randombox[mers][1],
        content_Randombox[mers][2],
        content_Randombox[mers][3],
        content_Randombox[mers][4]
                                        ])
    custom_ItemRandomboxBoxCard()
    custom_ItemCard()
    custom_Achievements()
#---------------------------------------------------------
# ItemsFilter
#---------------------------------------------------------
def ItemsFilter_weaponn():
        
    if mers == 'M':
        playerClass = """<Rifleman/>
		<Recon/>
		<Engineer/>
		<Medic level="1"/>"""
    elif mers == 'E':
        playerClass = """<Rifleman/>
		<Recon/>
		<Engineer level="1"/>
		<Medic/>"""
    elif mers == 'S':
        playerClass = """<Rifleman/>
		<Recon level="1"/>
		<Engineer/>
		<Medic/>"""
    elif mers == 'R':
        playerClass = """<Rifleman level="1"/>
		<Recon/>
		<Engineer/>
		<Medic/>"""
    
    for _, _, files in os.walk(temp_AttachPath):
       files = files
       break

    attach_Lst = []
    for attach in files:
        if attach.endswith('_d.xml'):
            attach = attach.split(".xml")[0]
            print(gSpace + f"attach --- {attach}")
            attach_Lst.append(f"""\n\t<Item name="{attach}">\n\t\t{playerClass}\n\t</Item>""")


    template_base = f"""
    <Item name="{custom_Weapon}">
		{playerClass}
	</Item>
	<Item name="{custom_Weapon}_shop">
		{playerClass}
	</Item>\n</ClassFilters>"""
 
    if len(attach_Lst) != 0:
        modifyChanges(temp_ItemsFilter_weapon, attach_Lst, '', '')

        file = open(temp_ItemsFilter_weapon)
        item = custom_Weapon + '_shop'
        try:
            if (item in file.read()):
                print(Fore.YELLOW + f"--- WARNING...  {item} in {temp_ItemsFilter_weapon}  ...already exists" + Style.RESET_ALL)
            else:
                with open(temp_ItemsFilter_weapon, 'a') as f:
                    f.writelines(template_base)
                f.close()
                print(Fore.GREEN + f"Complete... {temp_ItemsFilter_weapon}" + Style.RESET_ALL)
        except:
            print(Fore.RED + f"---FAILED... {temp_ItemsFilter_weapon}" + Style.RESET_ALL)
    else:
        modifyChanges(temp_ItemsFilter_weapon, template_base, '', '')            
#---------------------------------------------------------
def ItemsFilter_randomboxx():

    template_ItemsFilter_randombox = f"""
    <Item name="box_{custom_Weapon}">
		<Rifleman level="1"/>
		<Recon level="1"/>
		<Engineer level="1"/>
		<Medic level="1"/>
		<Heavy level="1"/>
	</Item>
	<Item name="box_{custom_Weapon}_card">
		<Rifleman level="1"/>
		<Recon level="1"/>
		<Engineer level="1"/>
		<Medic level="1"/>
		<Heavy level="1"/>
	</Item>\n</ClassFilters>"""
   
    modifyChanges(temp_ItemsFilter_randombox, template_ItemsFilter_randombox, "box_", "_card")
    
    # with open(temp_ItemsFilter_randombox, 'rb+') as f:
    #     f.seek(-1, os.SEEK_END)
    #     f.truncate()
#---------------------------------------------------------
def ItemsFilter_cardss():

    level = 'level="1"'
    m=e=r=s=''
        
    if mers == 'M':
        m = level
    elif mers == 'E':
        e = level
    elif mers == 'R':
        r = level
    elif mers == 'S':
        s = level    
    
    template_ItemsFilter_cards = f"""
	<Item name="{custom_Weapon}_card">
		<Rifleman {r}/>
		<Recon {s}/>
		<Engineer {e}/>
		<Medic {m}/>
		<Heavy />
	</Item>\n</ClassFilters>"""
    
    modifyChanges(temp_ItemsFilter_cards, template_ItemsFilter_cards,'', "_card")
#---------------------------------------------------------
def intagrate_ItemFilter():
    ItemsFilter_weaponn()
    ItemsFilter_randomboxx()
    ItemsFilter_cardss()
#---------------------------------------------------------
# Animation
#---------------------------------------------------------
def Animation_cbaa():
    try:
        template_Animation_cba = f"""	<!-- //animation definitions for the {custom_Weapon} (weapon type) -->
        <AnimationDefinition>
            <Model File="/../objects/weapons/{custom_Weapon}/{custom_Weapon}.chr"/>
            <Animation Path="1st_person/weapons/{custom_Weapon}"/>
            <Database Path="1st_person/weapons/{custom_Weapon}/{custom_Weapon}.dba"/>
            <COMPRESSION value="0"/>
            <RotEpsilon value="0.000001"/>
            <PosEpsilon value="0.01"/>
        </AnimationDefinition>\n</Definitions>"""
        
        modifyChanges(temp_Animations_cba, template_Animation_cba, '', "")
    except:
        pass
#---------------------------------------------------------
def Anim_handposes(handpose):
    try:
        temp_list = []
        temp_list.append('\n')
        file = open(temp + handpose).readlines()
        for line in file:
            if custom_Weapon in line:
                temp_list.append(line)
        temp_list.append("\t</handsPosesAnim>\n</handsPoses>")
        # -----------------------------        
        shutil.copyfile(master + handpose, temp + handpose)
        modifyChanges(temp + handpose, temp_list, custom_Weapon, '')
    except:
        pass
#---------------------------------------------------------
def Anim_chrparams(handpose):
    try:
        temp_list = []
        temp_list.append('\n')
        file = open(temp + handpose).readlines()
        for line in file:
            if "ik_aim_pose_" + custom_Weapon in line:
                temp_list.append(line)
        temp_list.append("\t</AnimationList>\n</Params>")
        # -----------------------------        
        shutil.copyfile(master + handpose, temp + handpose)
        remove_lastline(temp + handpose)
        modifyChanges(temp + handpose, temp_list, custom_Weapon, '')
    except:
        pass
#---------------------------------------------------------
def intagrate_Animations():
    Animation_cbaa()
    Anim_handposes(handposes01)
    Anim_handposes(handposes02)
    Anim_chrparams(handposes_ch)
#---------------------------------------------------------
# UI
#---------------------------------------------------------
def UI_cardss():
    
    template_UI_cards = f"""\n
    <image name="{custom_Weapon}_circuit" file="Libs\Icons\cards\craft_cards\{custom_Weapon}_circuit.tif" pos="0,0" size="560,248"/>
	<image name="{custom_Weapon}_progression" file="Libs\Icons\cards\craft_cards\{custom_Weapon}_progression.tif" pos="0,0" size="560,248"/>\n</images>"""

    modifyChanges(temp_UIcards, template_UI_cards,'', "_progression")
#---------------------------------------------------------
def UI_randomBoxesIconss():
    
    template_UI_randomBoxesIconss = f"""\n
	<image name="icons_randombox_{custom_Weapon}" file="Libs\Icons\RandomBoxes\Weapons\icons_randombox_{custom_Weapon}.tif" pos="0,0" size="256,128" />
	<image name="icons_randombox_{custom_Weapon}_cards" file="Libs\Icons\RandomBoxes\CraftCards\icons_randombox_{custom_Weapon}_craft.tif" pos="0,0" size="256,128" />
	<image name="icons_{custom_Weapon}_template" file="Libs\Icons\RandomBoxes\Templates\icons_{custom_Weapon}_template.tif" pos="0,0" size="512,256"/>\n</images>"""

    modifyChanges(temp_UIrandomBoxesIcons, template_UI_randomBoxesIconss,'icons_randombox_', "")
#---------------------------------------------------------
def UI_challengesIconss():
    
    template_UI_challengesIconss = f"""\n\t<image name="challenge_stripe_{custom_Weapon}" file="Libs/Icons/Challenges/challenge_stripe_{custom_Weapon}.tif" pos="0,0" size="512,128"/>\n</images>"""

    modifyChanges(temp_UIchallengesIcons, template_UI_challengesIconss,'challenge_stripe_', "")
#---------------------------------------------------------
def UI_weaponsItemsIconss():
    
    x_size = '400'
    if mers == 'R':
        x_size = '500'
    if mers == 'S':
        x_size = '700'
        
    template_UI_weaponsItemsIconss = f"""\n
    <image name="{custom_Weapon}" file="Libs\Icons\weapons\{custom_Weapon}\weapons_{custom_Weapon}.tif" pos="0,0" size="{x_size},200" />\n</images>"""

    modifyChanges(temp_UIweaponsItemsIcons, template_UI_weaponsItemsIconss,'', "")
#---------------------------------------------------------
def UI_attachmentsItemsIconss():    
    
    for _, _, filen in os.walk(temp_AttachPath):
       filen = filen
       break

    attach_Lst = []
    for attach in filen:
        if attach.endswith('_d.xml'):
            attach = attach.split(".xml")[0]
            
            x_size = '300'
            if "sr" in attach and 'gp_d' in attach:
                x_size = "300"
            if "gp_d" in attach or "bp_d" in attach or "sp_d" in attach:
                x_size = "200"
            
            attach_Lst.append(f"""\n\t<image name="{attach}" file="Libs\Icons\weapons\{custom_Weapon}\\attachmentsItemsIcons_{attach}.tif" pos="0,0" size="{x_size},200" cache="1"/>""")

    attach_Lst.append("\n</images>")
    
    if len(attach_Lst) != 0:
        modifyChanges(temp_UIattachmentsItemsIcons, attach_Lst, 'attachmentsItemsIcons_', '')
#---------------------------------------------------------
def UI_CombatLogIconss():
    
    template_UI_CombatLogIconss = f"""
 	<image_set file="Libs\Icons\CombatLog\CombatLogIcons_{custom_Weapon}.tif" offset_x="0" offset_y="0" size_x="192" size_y="96">
		<image name ="{custom_Weapon}_combatLog"	pos="0,0"	/>
 	</image_set>\n</images>"""

    modifyChanges(temp_UICombatLogIcons, template_UI_CombatLogIconss,'CombatLogIcons_', "")
#---------------------------------------------------------
def intagrate_UI():
    UI_cardss()
    UI_randomBoxesIconss()
    UI_challengesIconss()
    UI_weaponsItemsIconss()
    UI_attachmentsItemsIconss()
    UI_CombatLogIconss()
#---------------------------------------------------------
# MasterServer
#---------------------------------------------------------
def integrate_MasterServer():
    
    template_MasterServerr = f"""
    <progression name="{custom_Weapon}_card" cards_required="1000" item="{custom_Weapon}_shop"/>\n</card_progressions_config>"""

    modifyChanges(temp_card_progressions_01, template_MasterServerr,'', "_card")
    modifyChanges(temp_card_progressions_02, template_MasterServerr,'', "_card")
    modifyChanges(temp_card_progressions_03, template_MasterServerr,'', "_card")
#---------------------------------------------------------
# catalog_offers_IGR
#---------------------------------------------------------
def intagrate_catalog_offers_IGR():

    root = ET.parse(temp_catalog_offers_IGR).getroot()
    temp_store = []
    for elem in root.findall('offer'):
        count_store_id = elem.attrib['store_id']
        temp_store.append(count_store_id)
    
    store_id = int(temp_store[-1])
    print(gSpace + "... catalog_offers_IGR")
    print(gSpace + "... last store_id = ", store_id)

    repair_cost = get_repair_cost(temp + f"\\Game\\Items\\Weapons\\{custom_Weapon}_shop.xml")
    commiten = f"<!-- NewCustom... {custom_Weapon} -->"
    
    
    template_catalog_offers_IGR = f"""\n\t{commiten}
    <offer store_id="{store_id + 1}" item_name="{custom_Weapon}_shop" description="@{custom_Weapon}_shop" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="{repair_cost}" quantity="0" offer_status="NEW" key_item_name="" game_money="15000" cry_money="0" crown_money="0" key_item_money="0"/>
	<offer store_id="{store_id + 2}" item_name="box_{custom_Weapon}" description="@box_1_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="5" crown_money="0"/>
	<offer store_id="{store_id + 3}" item_name="box_{custom_Weapon}" description="@box_1_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="4" crown_money="0"/>
	<offer store_id="{store_id + 4}" item_name="box_{custom_Weapon}" description="@box_1_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="3" crown_money="0"/>
	<offer store_id="{store_id + 5}" item_name="box_{custom_Weapon}" description="@box_1_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="2" crown_money="0"/>
	<offer store_id="{store_id + 6}" item_name="box_{custom_Weapon}" description="@box_1_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="1" crown_money="0"/>
	<offer store_id="{store_id + 7}" item_name="box_{custom_Weapon}_card" description="@box_2_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="5" crown_money="0"/>
	<offer store_id="{store_id + 8}" item_name="box_{custom_Weapon}_card" description="@box_2_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="4" crown_money="0"/>
	<offer store_id="{store_id + 9}" item_name="box_{custom_Weapon}_card" description="@box_2_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="3" crown_money="0"/>
	<offer store_id="{store_id + 10}" item_name="box_{custom_Weapon}_card" description="@box_2_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="2" crown_money="0"/>
	<offer store_id="{store_id + 11}" item_name="box_{custom_Weapon}_card" description="@box_2_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="1" crown_money="0"/>\n</offers>"""
    
    modifyChanges(temp_catalog_offers_IGR, template_catalog_offers_IGR, '', '_shop')
#=========================================================
# DRIVE
#=========================================================
def main():
    fileStructure(createTempFolders)
    integrate_Items()
    intagrate_ItemFilter()
    intagrate_Animations()
    intagrate_UI()
    integrate_MasterServer()
    intagrate_catalog_offers_IGR()
    input(Fore.LIGHTBLUE_EX + '...Complete ' + Style.RESET_ALL)

if __name__ == "__main__":
    
    gSpace = "\t"
    master, temp, custom_Weapon, mers = Ask_Path()
    
    handposes_ch = "\\Game\\Objects\\Characters\\Human\\handsposes.chrparams" 
    handposes01 = "\\Game\\Objects\\Characters\\Human\\handsposes.xml"
    handposes02 = "\\Game\\Objects\\Characters\\Human\\handsposes_female.xml"

    ShopItemsBox = f"\\Game\\Items\\ShopItems\\box_{custom_Weapon}.xml"
    ShopItemsBoxCard = f"\\Game\\Items\\ShopItems\\box_{custom_Weapon}_card.xml"
    ItemsCards = f"\\Game\\Items\\Cards\\{custom_Weapon}_card.xml"
    configAchievements = f"\\Game\\Libs\\Config\\Achievements\\{custom_Weapon}_Kill.xml"

    ItemsFilter_weapon = f"\\Game\\Libs\\Config\\ItemsFilter_{custom_Weapon.strip('0123456789')}.xml"
    ItemsFilter_randombox = "\\Game\\Libs\\Config\\ItemsFilter_randombox.xml"
    ItemsFilter_cards = "\\Game\\Libs\\Config\\ItemsFilter_cards.xml"
    Animations_cba = "\\Game\\Animations\\Animations.cba"
    AttachPath = "\\Game\\Objects\\Weapons\\" + custom_Weapon
    
    UIweaponsItemsIcons = "\\Game\\Libs\\Config\\UI\\weaponsItemsIcons.xml"
    UIattachmentsItemsIcons = "\\Game\\Libs\\Config\\UI\\attachmentsItemsIcons.xml"
    UIrandomBoxesIcons = "\\Game\\Libs\\Config\\UI\\randomBoxesIcons.xml"
    UIchallengesIcons = "\\Game\\Libs\\Config\\UI\\challengesIcons.xml"
    UICombatLogIcons = "\\Game\\Libs\\Config\\UI\\CombatLogIcons.xml"
    UIcards = "\\Game\\Libs\\Config\\UI\\cards.xml"

    card_progressions_01 = "\\Game\\Libs\\Config\\MasterServer\\card_progressions_config.xml"
    card_progressions_02 = "\\Game\\Libs\\Config\\MasterServer\\card_progressions_config.mycom.xml"
    card_progressions_03 = "\\Game\\Libs\\Config\\MasterServer\\card_progressions_config.russia.xml"
    catalog_offers_IGR = "\\Game\\Libs\\Config\\Shop\\catalog_offers_IGR.xml"

    master_achievements = master + "\\Game\\Libs\\Config\\Achievements\\"
    master_Animations_cba = master + Animations_cba
    master_ItemsFilter_weapon = master + ItemsFilter_weapon
    master_ItemsFilter_randombox = master + ItemsFilter_randombox
    master_ItemsFilter_cards = master + ItemsFilter_cards
    master_UIweaponsItemsIcons = master + UIweaponsItemsIcons
    master_UIattachmentsItemsIcons = master + UIattachmentsItemsIcons
    master_UIrandomBoxesIcons = master + UIrandomBoxesIcons
    master_UIchallengesIcons = master + UIchallengesIcons
    master_UICombatLogIcons = master + UICombatLogIcons
    master_UIcards = master + UIcards
    master_card_progressions_01 = master + card_progressions_01
    master_card_progressions_02 = master + card_progressions_02
    master_card_progressions_03 = master + card_progressions_03
    master_catalog_offers_IGR = master + catalog_offers_IGR
# ----------------
    temp_AttachPath = temp + AttachPath
    temp_Animations_cba = temp + Animations_cba
    temp_ShopItemsBox = temp + ShopItemsBox
    temp_ShopItemsBoxCard = temp + ShopItemsBoxCard
    temp_configAchievements = temp + configAchievements
    temp_ItemsCards = temp + ItemsCards
    temp_ItemsFilter_weapon = temp + ItemsFilter_weapon
    temp_ItemsFilter_randombox = temp + ItemsFilter_randombox
    temp_ItemsFilter_cards = temp + ItemsFilter_cards
    temp_UIweaponsItemsIcons = temp + UIweaponsItemsIcons
    temp_UIattachmentsItemsIcons = temp + UIattachmentsItemsIcons
    temp_UIrandomBoxesIcons = temp + UIrandomBoxesIcons
    temp_UIchallengesIcons = temp + UIchallengesIcons
    temp_UICombatLogIcons = temp + UICombatLogIcons
    temp_UIcards = temp + UIcards
    temp_card_progressions_01 = temp + card_progressions_01
    temp_card_progressions_02 = temp + card_progressions_02
    temp_card_progressions_03 = temp + card_progressions_03
    temp_catalog_offers_IGR = temp + catalog_offers_IGR
#=========================================================
# Global stuff
#=========================================================

    createTempFolders = [temp + "\\Game\\Items\\ShopItems",
                        temp + "\\Game\\Items\\Cards",
                        temp + "\\Game\\Libs\\Config\\Achievements",
                        temp + "\\Game\\Libs\\Config\\UI",
                        temp + "\\Game\\Libs\\Config\\MasterServer",
                        temp + "\\Game\\Libs\\Config\\Shop"]

    content_Randombox =                                             {
        "R":[       'ar13_drum_01_console_shop',
                    'ar45_shop',
                    'ar37_shop',
                    'ar43_shop',
                    'ar35_shop'],
        "M":[       'shg40_rift01_console_shop',
                    'shg58_shop',
                    'shg54_shop',
                    'shg57_shop',
                    'shg50_shop'],
        "E":[       'smg51_shop',
                    'smg50_shop',
                    'smg09_custom_shop',
                    'smg54_shop',
                    'smg49_shop'],
        "S":[       'sr51_shop',
                    'sr52_shop',
                    'sr47_shop',
                    'sr48_shop',
                    'sr42_shop']
                                                                    }
    BoxPistol = {
        "R":[       'pt33_set12_shop',
                    'pt33_rad01_shop',
                    'pt33_jp01_shop',
                    'pt33_friday01_shop',
                    'pt33_samurai01_shop',
                    'pt33_swat00003_shop',
                    'pt33_heist03_shop'],  
        
        "E":[       'pt38_bp06_shop',
                    'pt38_oc04_shop',
                    'pt38_friday01_shop',
                    'pt38_black01_shop',
                    'pt38_black03_shop',
                    'pt38_navy00003_shop',
                    'pt38_stream03_shop'],
        
        "M":[       'pt36_bp07_shop',
                    'pt36_black02_shop',
                    'pt36_gorgona02_shop',
                    'pt36_brazil02_shop',
                    'pt36_friday01_shop',
                    'pt36_secret00002_shop'],
         
        "S":[       'pt39_samurai01_shop',
                    'pt39_swarm03_shop',
                    'pt39_oc05_shop',
                    'pt39_brazil01_shop',
                    'pt39_heist02_shop',
                    'pt39_shdw00001_shop'], 
    }
    
    main()