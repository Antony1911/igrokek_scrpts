import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os.path
import PySimpleGUI as sg
import shutil
from colorama import Back, Style, Fore

sg.theme('DarkGrey13')

#=========================================================
# SETUP
#=========================================================
def Ask_Path():
    layout = [
        [sg.Text("Insert your [WFPC_master] path ('Game' folder)", text_color='yellow')],
        [sg.InputText(default_text = r"e:\\partner_WPC\\wfpc_mrg\\main", key = "-MASTER-"),sg.FolderBrowse()],
        [sg.Text("Temp Folder", text_color='yellow')],
        [sg.InputText(default_text = r"d:\\temp_fbs", key = "-MOD-"), sg.FolderBrowse()],
        [sg.OK(key='OK'), sg.Cancel()]
    ]
    window = sg.Window('\U0001f638 integFBS', layout)

    while True:
        event, values = window.read(close=True)
        master, mod_repo = values["-MASTER-"], values["-MOD-"]
        
        for _,_,files in os.walk(mod_repo + "\\Game\\Items\\Skins\\"):
            for i in files:
                if "fbs" in i:
                    fbs = i.split('.')[0]
                    print(f'Fbs name -- {fbs}')
                break
        
        if event == 'OK':
            return master, mod_repo, fbs
        if event in ('Cancel', None) or event == sg.WIN_CLOSED:
            break
        
    window.close()
#---------------------------------------------------------
def pretty_print(element, indent=None):
    if indent is None:
        indent = "\t"
    original = ET.tostring(element, 'utf8')
    reparsed = minidom.parseString(original)
    indented = reparsed.toprettyxml(indent=indent, newl='\n')
    return '\n'.join([s for s in indented.splitlines() if s.strip()])
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
    
    for tempFolder in createTempFolders:
        check_and_create(tempFolder)

    if os.path.exists(temp_ItemsFilter_fbs):
        pass
    else:
        shutil.copyfile(master_ItemsFilter_fbs, temp_ItemsFilter_fbs)
    if os.path.exists(temp_ItemsFilter_randombox):
        pass
    else:
        shutil.copyfile(master_ItemsFilter_randombox, temp_ItemsFilter_randombox)
    if os.path.exists(temp_assetsItemsIcons):
        pass
    else:
        shutil.copyfile(master_assetsItemsIcons, temp_assetsItemsIcons)
    if os.path.exists(temp_randomBoxesIcons):
        pass
    else:
        shutil.copyfile(master_randomBoxesIcons, temp_randomBoxesIcons)
    if os.path.exists(temp_catalog_offers_IGR):
        pass
    else:
        shutil.copyfile(master_catalog_offers_IGR, temp_catalog_offers_IGR)
#---------------------------------------------------------
def mersClass():
    if SkinClass == "soldier":
        mers = "R"
    elif SkinClass == "sniper":
        mers = "S"
    elif SkinClass == "medic":
        mers = "M"
    elif SkinClass == "engineer":
        mers = "E"
    else:
        mers = "MERS"
    return mers
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
def modifyChanges(path, template, skins, prompt01, prompt02):
    
    file = open(path)
    item = prompt01 + skins + prompt02
    try:
        if (item in file.read()):
            print(Fore.YELLOW + f"--- WARNING...  {item} in {path}  ...already exists" + Style.RESET_ALL)
        else:
            remove_lastline(path)
            with open(path, 'a') as f:
                f.writelines(template)
            f.close()
            print(Fore.GREEN + f"Complete... {path}" + Style.RESET_ALL + Fore.MAGENTA + f" {skins} ...Modified" + Style.RESET_ALL)
    except:
        print(Fore.RED + f"---FAILED... {path}" + Style.RESET_ALL)
#---------------------------------------------------------
def ShopItemsBox(list):

    knive = sg.popup_get_text('Nanimokamo nandemonai nanimo ?', default_text="kn19_coldwar01",
                              no_titlebar=1, grab_anywhere=1)
    fbs_name = fbs.split('fbs_')[1]
    
    # if "shared" in fbs:
    #     shared_addon = ''
    # else:
    
    fbs_ShopItemsBox_template = f"""<shop_item name="box_{fbs}" type="random_box">
    <mmo_stats>
        <param name="item_category" value="RandomBox"/>
        <param name="shopcontent" value="1"/>
        <param name="classes" value="MERSH"/>
        <param name="max_buy_amount" value="32000" />
        <param name="stackable" value="1" />
    </mmo_stats>
    <UI_stats>
        <param name="name" value="@box_{fbs}_name"/>
        <param name="description" value="@box_1_item_desc"/>
        <param name="icon" value="bundle_icon_fbs_{fbs_name}"/>
    </UI_stats>
    <random_box>
        <group>
            <item name="{fbs}" weight="10"/>
            <item name="{knive}" weight="10"/>
            <item name="{list[0]}" expiration="3h" weight="200"/>
            <item name="{list[1]}" expiration="3h" weight="195"/>
            <item name="{list[2]}" expiration="3h" weight="195"/>
            <item name="{list[3]}" expiration="3h" weight="195"/>
            <item name="{list[4]}" expiration="3h" weight="195"/>
        </group>
    </random_box>\n</shop_item>"""

    writeChanges(temp_ShopItemsBox, fbs_ShopItemsBox_template)
#---------------------------------------------------------
def ItemsFilter_fbs():

    add = ' level="1"'
    rif = rec = eng = med = ''
    
    if SkinClass == "soldier":
        rif = add
    elif SkinClass == "sniper":
        rec = add
    elif SkinClass == "engineer":
        eng = add
    elif SkinClass == "medic":
        med = add
    else:
        rif = rec = eng = med = add

    replacer = fbs.replace(SkinClass, "shared")


    if "shared" in fbs:
        shared_addon = ''
    else:
        shared_addon = f"""
    <Item name="{replacer}">
		<Rifleman level="1"/>
		<Recon level="1"/>
		<Engineer level="1"/>
		<Medic level="1"/>
	</Item>"""
 
    template_ItemsFilter_fbs = f"""{shared_addon}
    <Item name="{fbs}">
		<Rifleman{rif}/>
		<Recon{rec}/>
		<Engineer{eng}/>
		<Medic{med}/>
	</Item>\n</ClassFilters>"""

    modifyChanges(temp_ItemsFilter_fbs, template_ItemsFilter_fbs, fbs, '', "")
#---------------------------------------------------------
def ItemsFilter_randombox():

    replacer = fbs.replace(SkinClass, "shared")

    if "shared" in fbs:
        shared_addon = ''
    else:
        shared_addon = f"""
    <Item name="box_{replacer}">
		<Rifleman level="1"/>
		<Recon level="1"/>
		<Engineer level="1"/>
		<Medic level="1"/>
        <Heavy level="1"/>
	</Item>"""
 
    template_ItemsFilter_randombox = f"""{shared_addon}
    <Item name="box_{fbs}">
		<Rifleman level="1"/>
		<Recon level="1"/>
		<Engineer level="1"/>
		<Medic level="1"/>
        <Heavy level="1"/>
	</Item>\n</ClassFilters>"""

    modifyChanges(temp_ItemsFilter_randombox, template_ItemsFilter_randombox, fbs, '', "")
#---------------------------------------------------------
def assetsItemsIcons():
    fbs01 = fbs.split('fbs_')[1]

    sss = r"Libs\Icons\assets\fbs_" + f"{fbs01}" + r"\assets_fb_suits_" + f"{fbs01}" + r'.tif'
    template_assetsItemsIcons = f"""\n
    <image name="{fbs}" file="{sss}" pos="0,0" size="450,200" />\n</images>"""

    modifyChanges(temp_assetsItemsIcons, template_assetsItemsIcons, fbs, '', "")
#---------------------------------------------------------
def randomBoxesIcons():
    fbs01 = fbs.split('fbs_')[1]
    sss = r"Libs\Icons\assets\fbs_" + f"{fbs01}" + r"\bundle_icon_fbs_" + f"{fbs01}" + r'.tif'
    template_randomBoxesIconss = f"""\n
    <image name="bundle_icon_fbs_{fbs01}" file="{sss}" pos="0,0" size="256,128" />\n</images>"""
    modifyChanges(temp_randomBoxesIcons, template_randomBoxesIconss, fbs, '', "")
#---------------------------------------------------------
def catalog_offers_IGR():
    
    root = ET.parse(temp_catalog_offers_IGR).getroot()
    temp_store = []
    for elem in root.findall('offer'):
        count_store_id = elem.attrib['store_id']
        temp_store.append(count_store_id)
    
    store_id = int(temp_store[-1])
    print("\t" + "... catalog_offers_IGR")
    print("\t" + "... last store_id = ", store_id)
    
    replacer = fbs.replace(SkinClass, "shared")
    commiten01 = f"<!-- FBS... {fbs} -->"
    commiten02 = f"<!-- FBS... {replacer} -->"

    if "shared" in fbs:
        shared_addon = ''
    else:
        shared_addon = f"""\n\t{commiten01}
    <offer store_id="{store_id + 7}" item_name="{fbs}" description="@ui_armor_{fbs}" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="0" quantity="0" offer_status="NEW" key_item_name="" game_money="300" cry_money="0" crown_money="0"/>
	<offer store_id="{store_id + 8}" item_name="box_{fbs}" description="box_{fbs}_description" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="5" crown_money="0"/>
	<offer store_id="{store_id + 9}" item_name="box_{fbs}" description="box_{fbs}_description" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="4" crown_money="0"/>
	<offer store_id="{store_id + 10}" item_name="box_{fbs}" description="box_{fbs}_description" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="3" crown_money="0"/>
	<offer store_id="{store_id + 11}" item_name="box_{fbs}" description="box_{fbs}_description" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="2" crown_money="0"/>
	<offer store_id="{store_id + 12}" item_name="box_{fbs}" description="box_{fbs}_description" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="1" crown_money="0"/>"""
 
    template_ItemsFilter_offer = f"""\n\t{commiten02}
    <offer store_id="{store_id + 1}" item_name="{replacer}" description="@ui_armor_{replacer}" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="0" quantity="0" offer_status="NEW" key_item_name="" game_money="300" cry_money="0" crown_money="0"/>
	<offer store_id="{store_id + 2}" item_name="box_{replacer}" description="box_{replacer}_description" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="5" crown_money="0"/>
	<offer store_id="{store_id + 3}" item_name="box_{replacer}" description="box_{replacer}_description" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="4" crown_money="0"/>
	<offer store_id="{store_id + 4}" item_name="box_{replacer}" description="box_{replacer}_description" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="3" crown_money="0"/>
	<offer store_id="{store_id + 5}" item_name="box_{replacer}" description="box_{replacer}_description" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="2" crown_money="0"/>
	<offer store_id="{store_id + 6}" item_name="box_{replacer}" description="box_{replacer}_description" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="1" crown_money="0"/>{shared_addon}\n</offers>"""

    modifyChanges(temp_catalog_offers_IGR, template_ItemsFilter_offer, fbs, '', "")
#=========================================================
# DRIVE
#=========================================================
def main():
    fileStructure(createTempFolders)
    ShopItemsBox([  contentCreation[SkinClass][0],
                    contentCreation[SkinClass][1],
                    contentCreation[SkinClass][2],
                    contentCreation[SkinClass][3],
                    contentCreation[SkinClass][4]   ])
    ItemsFilter_fbs()
    ItemsFilter_randombox()
    assetsItemsIcons()
    randomBoxesIcons()
    catalog_offers_IGR()
    # input(Fore.LIGHTBLUE_EX + '...Complete ' + Style.RESET_ALL)

if __name__ == "__main__":
    
    master, temp, fbs = Ask_Path()

    if 'f_' in  fbs.split('_fbs')[0]:
        SkinClass = fbs.split('f_')[1].split('_')[0]
    else:
        SkinClass = fbs.split('_')[0]

    master_itemsSkins = master + f"\\Game\\Items\\Skins\\{fbs}.xml"
    master_ItemsFilter_fbs = master + "\\Game\\Libs\\Config\\ItemsFilter_fbs.xml"
    master_ItemsFilter_randombox = master + "\\Game\\Libs\\Config\\ItemsFilter_randombox.xml"
    master_assetsItemsIcons = master + "\\Game\\Libs\\Config\\UI\\assetsItemsIcons.xml"
    master_randomBoxesIcons = master + "\\Game\\Libs\\Config\\UI\\randomBoxesIcons.xml"
    master_catalog_offers_IGR = master + "\\Game\\Libs\\Config\\Shop\\catalog_offers_IGR.xml"
# ----------------
    temp_ShopItemsBox = temp + f"\\Game\\Items\\ShopItems\\box_{fbs}.xml"
    temp_ItemsFilter_fbs = temp + "\\Game\\Libs\\Config\\ItemsFilter_fbs.xml"
    temp_ItemsFilter_randombox = temp + "\\Game\\Libs\\Config\\ItemsFilter_randombox.xml"
    temp_assetsItemsIcons = temp + "\\Game\\Libs\\Config\\UI\\assetsItemsIcons.xml"
    temp_randomBoxesIcons = temp + "\\Game\\Libs\\Config\\UI\\randomBoxesIcons.xml"
    temp_catalog_offers_IGR = temp + "\\Game\\Libs\\Config\\Shop\\catalog_offers_IGR.xml"
#=========================================================
# Global stuff
#=========================================================
    createTempFolders = [temp + "\\Game\\Items\\ShopItems",
                        temp + "\\Game\\Libs\\Config\\UI",
                        temp + "\\Game\\Libs\\Config\\Shop"]
    
    contentCreation = {
        "soldier":[ 'ar13_drum_01_console_shop',
                    'ar45_shop',
                    'ar37_shop',
                    'ar43_shop',
                    'ar35_shop'],
        "medic":[ 'shg40_rift01_console_shop',
                    'shg58_shop',
                    'shg54_shop',
                    'shg57_shop',
                    'shg50_shop'],
        "engineer":[ 'smg51_shop',
                    'smg50_shop',
                    'smg09_custom_shop',
                    'smg54_shop',
                    'smg49_shop'],
        "sniper":[ 'sr51_shop',
                    'sr52_shop',
                    'sr47_shop',
                    'sr48_shop',
                    'sr42_shop'],
        "shared":[ 'ar13_drum_01_console_shop',
                    'ar45_shop',
                    'ar37_shop',
                    'ar43_shop',
                    'ar35_shop']        
    }

    main()
    