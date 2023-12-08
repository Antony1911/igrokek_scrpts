import os
import xml.etree.ElementTree as ET
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
        [sg.Text("[WFPC_master] path", text_color='yellow')],
        [sg.InputText(default_text = r"e:\\partner_WPC\\wfpc_mrg\\main", key = "-MASTER-"),sg.FolderBrowse()],
        [sg.Text("Temp Folder", text_color='yellow')],
        [sg.InputText(default_text = r"d:\\temp_achievements", key = "-MOD-"), sg.FolderBrowse()],
        [sg.OK(key='OK'), sg.Cancel()]
    ]
    window = sg.Window('\U0001f638 integAchievements', layout)

    while True:
        event, values = window.read(close=True)
        master, mod_repo = values["-MASTER-"], values["-MOD-"]
        
        for _,_,files in os.walk(mod_repo + "\\Game\\Libs\\Icons\\Challenges\\"):
            for i in files:
                if i.endswith('.tif'):
                    i = i.split('.')[0]
                    ach_list.append(i)
                    print(f"achievement -- {i}")
            
        if event == 'OK':
            return master, mod_repo
        if event in ('Cancel', None) or event == sg.WIN_CLOSED:
            break
        
    window.close()
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
    copyFile(temp_ItemsFilter_special, master_ItemsFilter_special)
    # UI
    copyFile(temp_UIchallengesIcons, master_UIchallengesIcons)
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
def get_repair_cost(path, skin):
    try:
        root = ET.parse(path).getroot()
        for elem in root.find('mmo_stats').findall('param'):
            if elem.attrib['name'] == "repair_cost":
                value = elem.attrib['value']
                print(f"{gSpace}... {skin} repair_cost = {value}")
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
                root = ET.parse(path01).getroot()
                a = int(root.attrib['id'])
                if temp[0] < a:
                    temp.clear()
                    temp.append(a)
        break
    print("last grep", temp[0])
    return int(temp[0])
#---------------------------------------------------------
# Achievements
#---------------------------------------------------------
def integrate_Items():
    idNumber = get_grep(master_achievements)
    
    for achieve in ach_list:
        
        smb = achieve.split('_')[1]
        skin = achieve.split('_')[-1]
        idNumber = int(idNumber) + 1
        print(f"{achieve} -- {idNumber}")
        Achievepath = temp + f"\\Game\\Libs\\Config\\Achievements\\{skin}_{smb}.xml"
       
        pattern_Achievements = f"""<?xml version="1.0" ?>
    <Achievement active="1" id="{idNumber}" kind="hidden" MS_side="1" amount="1">
        <UI name="@{skin}_{smb}" desc="@{skin}_{smb}_desc"/>
        <BannerImage image="{achieve}" type="{smb}"/>
    </Achievement>"""
        writeChanges(Achievepath, pattern_Achievements)
        
        pattern_ItemRandomBox = f"""<?xml version="1.0" ?>
    <shop_item name="unlock_{skin}_{smb}" type="meta_game">
        <mmo_stats>
            <param name="item_category" value="Emblem"/>
            <param name="shopcontent" value="1"/>
            <param name="classes" value="RESM"/>
            <param name="max_buy_amount" value="1"/>
        </mmo_stats>
        <UI_stats>
            <param name="name" value="@{skin}_{smb}"/>
            <param name="description" value="@{skin}_{smb}_desc"/>
            <param name="icon" value="{achieve}"/>
        </UI_stats>
        <metagame_stats>
            <on_activate unlock_achievement="{idNumber}"/>
        </metagame_stats>
    </shop_item>"""
        writeChanges(temp + f"\\Game\\Items\\ShopItems\\unlock_{skin}_{smb}.xml", pattern_ItemRandomBox)
#---------------------------------------------------------
#  ItemsFilter
#---------------------------------------------------------
def intagrate_ItemFilter():
    
    for achieve in ach_list:

        smb = achieve.split('_')[1]
        skin = achieve.split('_')[-1]
        
        template_special = f"""\n\t<Item name="unlock_{skin}_{smb}">
        <Rifleman level="1"/>
        <Recon level="1"/>
        <Engineer level="1"/>
        <Medic level="1"/>
        <Heavy/>
    </Item>\n</ClassFilters>"""

        modifyChanges(temp_ItemsFilter_special, template_special, skin, '', '')
#---------------------------------------------------------
#  UI
#---------------------------------------------------------
def intagrate_UI():
    for achieve in ach_list:
        
        skin = achieve.split('_')[-1]
        num = '128'
        if "strip" in achieve:
            num = '512'
    
        template_UI_challengesIconss = f"""\n\t<image name="{achieve}" file="Libs/Icons/Challenges/{achieve}.tif" pos="0,0" size="{num},128"/>\n</images>"""
        modifyChanges(temp_UIchallengesIcons, template_UI_challengesIconss, skin, '', "")
#---------------------------------------------------------
# catalog_offers_IGR
#---------------------------------------------------------
def intagrate_catalog_offers_IGR():
    gpart = ach_list[0].split('_')[-1]
    commiten = f"\n\t<!-- Achievements... {gpart} -->\n</offers>"
    modifyChanges(temp_catalog_offers_IGR, commiten, gpart, '', "")
                   
    root = ET.parse(temp_catalog_offers_IGR).getroot()
    temp_store = []
    for elem in root.findall('offer'):
        count_store_id = elem.attrib['store_id']
        temp_store.append(count_store_id)
    
    store_id = int(temp_store[-1])
    print(gSpace + "... catalog_offers_IGR")
    print(gSpace + "... last store_id = ", store_id)

    for achieve in ach_list:

        smb = achieve.split('_')[1]
        skin = achieve.split('_')[-1]
        store_id = store_id + 1
        
        template_catalog_offers_IGR = f"""
    <offer store_id="{store_id}" item_name="unlock_{skin}_{smb}" description="@{skin}_{smb}_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="123" crown_money="0"/>\n</offers>"""
        modifyChanges(temp_catalog_offers_IGR, template_catalog_offers_IGR, f"{skin}_{smb}", '', '')
# =========================================================
# DRIVE
# =========================================================
def main():
    fileStructure(createTempFolders)
    integrate_Items()
    intagrate_ItemFilter()
    intagrate_UI()
    intagrate_catalog_offers_IGR()
    input(Fore.LIGHTBLUE_EX + '...Complete ' + Style.RESET_ALL)

if __name__ == "__main__":
    ach_list = []
    
    gSpace = "\t"
    master, temp = Ask_Path()
    
    ItemsFilter_special = f"\\Game\\Libs\\Config\\ItemsFilter_special.xml"
    UIchallengesIcons = "\\Game\\Libs\\Config\\UI\\challengesIcons.xml"

    catalog_offers_IGR = "\\Game\\Libs\\Config\\Shop\\catalog_offers_IGR.xml"

    master_achievements = master + "\\Game\\Libs\\Config\\Achievements\\"
    master_ItemsFilter_special = master + ItemsFilter_special
    master_UIchallengesIcons = master + UIchallengesIcons
    master_catalog_offers_IGR = master + catalog_offers_IGR
# ----------------
    temp_ItemsFilter_special = temp + ItemsFilter_special
    temp_UIchallengesIcons = temp + UIchallengesIcons
    temp_catalog_offers_IGR = temp + catalog_offers_IGR
#=========================================================
# Global stuff
#=========================================================

    createTempFolders = [temp + "\\Game\\Items\\ShopItems",
                        temp + "\\Game\\Libs\\Config\\Achievements",
                        temp + "\\Game\\Libs\\Config\\UI",
                        temp + "\\Game\\Libs\\Config\\Shop"]
    main()