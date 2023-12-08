import os, glob
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os.path
import PySimpleGUI as sg
import shutil
sg.theme('DarkGrey13')

#=========================================================
# SETUP
#=========================================================
def Ask_Path():

    layout = [
        [sg.Text("Insert your [WFPC_master] path ('Game' folder)", text_color='yellow')],
        [sg.InputText(
            default_text = r"e:\\partner_WPC\\wfpc_mrg\\main\\Game",
            key = "-MASTER-"),
            sg.FolderBrowse()],

        [sg.Text("Where to save modConfig?", text_color='yellow')],
        [sg.InputText(
            default_text = "d:\\some_get_come\\Game",
            key = "-MOD-"),
            sg.FolderBrowse()],
        
        [sg.Text("get weapons", text_color='yellow')],
        [sg.InputText(key = "-WE-")],

        [sg.OK(key='OK'), sg.Cancel()]
    ]
    window = sg.Window('\U0001f638 configMod', layout)

    while True:
        event, values = window.read(close=True)

        master, mod_repo, weapons = values["-MASTER-"], values["-MOD-"], values["-WE-"]

        if event == 'OK':
            return master, mod_repo, weapons

        if event in ('Cancel', None) or event == sg.WIN_CLOSED:
            break
        
    window.close()
#---------------------------------------------------------
def materialle(elem):
    try:
        elem = elem.split('_tp')[0]
    except:
        elem = elem
    
    if 'console' in elem:
        try:
            mat_name = elem.split('_')[1:][0]+'_'+elem.split('_')[1:][1] + '_'+elem.split('_')[1:][2]
        except IndexError:
            try:
                mat_name = elem.split('_')[1:][0]+'_'+elem.split('_')[1:][1]
            except IndexError:
                try:
                    mat_name = elem.split('_')[1:][0]
                except IndexError:
                    mat_name = 'default'
    else:
        try:
            mat_name = elem.split('_')[1:][1]
            if len(mat_name) > 3:
                pass
            else:
                try:
                    mat_name = elem.split('_')[1:][2]
                except IndexError:
                    try:
                        mat_name = elem.split('_')[1:][0]
                    except IndexError:
                        mat_name = 'default'
        except IndexError:
            try:
                mat_name = elem.split('_')[1:][2]
            except IndexError:
                try:
                    mat_name = elem.split('_')[1:][0]
                except IndexError:
                    mat_name = 'default'
    return mat_name
#---------------------------------------------------------
def pretty_print(element, indent=None):
    if indent is None:
        indent = "\t"
    original = ET.tostring(element, 'utf8')
    reparsed = minidom.parseString(original)
    indented = reparsed.toprettyxml(indent=indent, newl='\n')
    return '\n'.join([s for s in indented.splitlines() if s.strip()])
#---------------------------------------------------------
def del_xml(skin_repo):
    for root, dirs, files in os.walk(skin_repo):
        for name in files:
            if name.endswith('xml'):
                item = os.path.join(root, name)
                os.remove(item)
                print("\nremoved --> ", item)
#---------------------------------------------------------
def list_to_string(l):
    str1 = '\n'
    return (str1.join(l))
#---------------------------------------------------------
def stringToList(string):
    listRes = list(string.split(" "))
    return listRes
#---------------------------------------------------------
def fileStructure(raw_weapon, kitty_01, kitty_02, kitty_03, kitty_04, kitty_05):

    def check_and_create(pppath):
        if os.path.exists(pppath) == True:
            pass
        else:
            os.makedirs(pppath)

    check_and_create(kitty_01)
    check_and_create(kitty_02)
    check_and_create(kitty_03)
    check_and_create(kitty_04)
    check_and_create(kitty_05)


    shutil.copyfile(challengesIcons, c_LibsConfig_UI + "\\attachmentsItemsIcons.xml")
    shutil.copyfile(challengesIcons, c_LibsConfig_UI + "\\cards.xml")
    shutil.copyfile(challengesIcons, c_LibsConfig_UI + "\\challengesIcons.xml")
    shutil.copyfile(challengesIcons, c_LibsConfig_UI + "\\CombatLogIcons.xml")
    shutil.copyfile(randomBoxesIcons, c_LibsConfig_UI + "\\randomBoxesIcons.xml")
    shutil.copyfile(weaponsItemsIcons, c_LibsConfig_UI + "\\weaponsItemsIcons.xml")

    shutil.copyfile(ItemFilter_randombox, c_LibsConfig + "\\item_progession.xml")
    shutil.copyfile(ItemFilter_randombox, c_LibsConfig + "\\ItemFilter_cards.xml")
    shutil.copyfile(ItemFilter_randombox, c_LibsConfig + "\\ItemFilter_keys.xml")
    shutil.copyfile(ItemFilter_randombox, c_LibsConfig + f"\\ItemFilter_{raw_weapon}.xml")
    shutil.copyfile(ItemFilter_randombox, c_LibsConfig + "\\ItemsFilter_randombox.xml")
    shutil.copyfile(ItemFilter_skins, c_LibsConfig + "\\ItemFilter_skins.xml")

    shutil.copyfile(catalog_offers_IGR, c_LibsConfig_Shop + "\\catalog_offers_IGR.xml")
#---------------------------------------------------------
def box_shopItem(skinweapon, box_list):

    box = f"""<shop_item name="box_{skinweapon}" type="random_box">
	<mmo_stats>
		<param name="item_category" value="RandomBox"/>
		<param name="shopcontent" value="1"/>
		<param name="classes" value="RESMH"/>
		<param name="max_buy_amount" value="32000"/>
		<param name="stackable" value="1"/>
	</mmo_stats>
	<UI_stats>
		<param name="name" value="@box_{skinweapon}_shop_name"/>
		<param name="description" value="@box_1_item_desc"/>
		<param name="icon" value="icons_randombox_{skinweapon}"/>
	</UI_stats>
	<random_box>
		<group>
			<item name="{skinweapon}_shop" weight="1"/>
            <item name="{box_list[0]}_shop" expiration="3h" weight="20"/>
            <item name="{box_list[1]}_shop" expiration="3h" weight="20"/>
            <item name="{box_list[2]}_shop" expiration="3h" weight="20"/>
            <item name="{box_list[3]}_shop" expiration="3h" weight="19"/>
		</group>
	</random_box>\n</shop_item>"""
#=========================================================
# DRIVE
#=========================================================
def main():
    # del_xml(mod_repo)
    weapons = stringToList(weaponary)
    raw_weapon = weapons[0].strip("0123456789")

    fileStructure(raw_weapon, c_It_Shopitems,
                    c_LibsConfig,
                    c_LibsConfig_Ach,
                    c_LibsConfig_UI,
                    c_LibsConfig_Shop,
                )
    
    print(weapons)
    sg.popup_notify('Complete')

if __name__ == "__main__":
    
    master, mod_repo, weaponary = Ask_Path()

    # # ==================TEST_PATH==================================
    # master = os.path.abspath("e:\\partner_WPC\\wfpc_mrg\\main\\Game")
    # mod_repo = os.path.abspath("d:\\some_get_come\\Game")
    # # ==================TEST_PATH==================================

    randombox_Path = master + "\\Items\\ShopItems"
    achievement_Path = master + "\\Libs\\Config\\Achievements"

    ItemFilter_randombox = master + "\\Libs\\Config\\ItemsFilter_randombox.xml"
    ItemFilter_skins = master + "\\Libs\\Config\\ItemsFilter_skins.xml"

    randomBoxesIcons = master + "\\Libs\\Config\\UI\\randomBoxesIcons.xml"
    weaponsItemsIcons = master + "\\Libs\\Config\\UI\\weaponsItemsIcons.xml"
    challengesIcons = master + "\\Libs\\Config\\UI\\challengesIcons.xml"

    catalog_offers_IGR = master + "\\Libs\\Config\\Shop\\catalog_offers_IGR.xml"

    # to_copy
    c_It_Shopitems = mod_repo + "\\Game\\Items\\ShopItems"
    c_LibsConfig = mod_repo + "\\Game\\Libs\\Config"
    c_LibsConfig_Ach = mod_repo + "\\Game\\Libs\\Config\\Achievements"
    c_LibsConfig_UI = mod_repo + "\\Game\\Libs\\Config\\UI"
    c_LibsConfig_Shop = mod_repo + "\\Game\\Libs\\Config\\Shop"

    ss = {
        "ar":[
        "ar13_drum_01_console",
        "ar45",
        "ar37",
        "ar43",
        "ar35"],

        "shg":[
        "shg40_rift01_console",
        "shg58",
        "shg54",
        "shg57",
        "shg50"],

        "pt":[
        "pt39",
        "pt36",
        "pt38",
        "pt37",
        "pt33"],

        "sr":[
        "sr51",
        "sr52",
        "sr47",
        "sr48",
        "sr42"],
    }

    main()

# randombox_Path = master + "\\Items\\ShopItems"
# achievement_Path = master + "\\Libs\\Config\\Achievements"

# ItemFilter_randombox = master + "\\Libs\\Config\\ItemsFilter_randombox.xml"
# ItemFilter_skins = master + "\\Libs\\Config\\ItemsFilter_skins.xml"
# randomBoxesIcons = master + "\\Libs\\Config\\UI\\randomBoxesIcons.xml"
# weaponsItemsIcons = master + "\\Libs\\Config\\UI\\weaponsItemsIcons.xml"
# challengesIcons = master + "\\Libs\\Config\\UI\\challengesIcons.xml"
# catalog_offers_IGR = master + "\\Libs\\Config\\Shop\\catalog_offers_IGR.xml"

# # to_copy
# c_It_Shopitems = mod_repo + "\\Game\\Items\\ShopItems"
# c_LibsConfig = mod_repo + "\\Game\\Libs\\Config"
# c_LibsConfig_Ach = mod_repo + "\\Game\\Libs\\Config\\Achievements"
# c_LibsConfig_UI = mod_repo + "\\Game\\Libs\\Config\\UI"
# c_LibsConfig_Shop = mod_repo + "\\Game\\Libs\\Config\\Shop"