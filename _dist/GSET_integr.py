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
        [sg.Text("Insert your [WFPC_master] path ('Game' folder)", text_color='yellow')],
        [sg.InputText(default_text = r"e:\\partner_WPC\\wfpc_mrg\\main", key = "-MASTER-"),sg.FolderBrowse()],
        [sg.Text("Temp Folder", text_color='yellow')],
        [sg.InputText(default_text = r"d:\\temp_gset", key = "-MOD-"), sg.FolderBrowse()],
        [sg.OK(key='OK'), sg.Cancel()]
    ]
    window = sg.Window('\U0001f638 integGSet', layout)

    while True:
        event, values = window.read(close=True)
        master, mod_repo = values["-MASTER-"], values["-MOD-"]
        
        for _,_,files in os.walk(mod_repo + "\\Game\\Items\\Armor\\"):
            for i in files:
                gset = i.split('.')[0]
                gset_partList.append(gset)
                print(f'GSet part -- {gset}')
                
                item = i.split('_')[1]
                if item in sss:
                    pass
                else:
                    sss.append(item)
                    
        if event == 'OK':
            return master, mod_repo
        if event in ('Cancel', None) or event == sg.WIN_CLOSED:
            break
    window.close()
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

    for item in sss:
        copyFile(temp + f"\\Game\\Libs\\Config\\ItemsFilter_{item}.xml", master + f"\\Game\\Libs\\Config\\ItemsFilter_{item}.xml")
        
    copyFile(temp_assetsItemsIcons, master_assetsItemsIcons)
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
def get_repair_cost(path):
    try:
        root = ET.parse(path).getroot()
        for elem in root.find('mmo_stats').findall('param'):
            if elem.attrib['name'] == "repair_cost":
                value = elem.attrib['value']
                item01 = path.split('\\')[-1].split(".")[0]
                print(f"\t... {item01} repair_cost = {value}")
                return value
    except FileNotFoundError:
        print(Fore.RED + f"--- FileNotFoundError... {path}" + Style.RESET_ALL)
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
def ItemsFilter_gset():

    add = ' level="1"'
    # rif = rec = eng = med = ''
    
    for part in gset_partList:
        SkinClass = part.split('_')[0]
        
        if SkinClass == "soldier":
            rif = add
            rec = eng = med = ''
        elif SkinClass == "sniper":
            rec = add
            rif = eng = med = ''
        elif SkinClass == "engineer":
            eng = add
            rif = rec = med = ''
        elif SkinClass == "medic":
            med = add
            rif = rec = eng = ''
        elif SkinClass == "shared":
            rif = rec = eng = med = add

        replacer = part.replace(SkinClass, "shared")

    
        template_ItemsFilter = f"""
    <Item name="{part}">
        <Rifleman{rif}/>
        <Recon{rec}/>
        <Engineer{eng}/>
        <Medic{med}/>
    </Item>\n</ClassFilters>"""

        j = part.split('_')[1]
        modifyChanges(temp + f"\\Game\\Libs\\Config\\ItemsFilter_{j}.xml", template_ItemsFilter, part, '+', "")
#---------------------------------------------------------
def assetsItemsIcons_gset():
    gpart = gset_partList[0].split('_')[2]
    commiten = f"\n\t<!-- {gpart} -->\n</images>"
    modifyChanges(temp_assetsItemsIcons, commiten, gpart, '', "")
    
    for part in gset_partList:
        template_assetsItemsIcons = f"""\n\t<image name="{part}" file="Libs\Icons\\assets\{part.split('_')[2]}\\assets_{part}.tif" pos="0,0" size="200,200" />\n</images>"""
        modifyChanges(temp_assetsItemsIcons, template_assetsItemsIcons, part, '', "")
#---------------------------------------------------------
def catalog_offers_IGR():
    gpart = gset_partList[0].split('_')[2]
    commiten = f"\n\t<!-- GearSet... {gpart} -->\n</offers>"
    modifyChanges(temp_catalog_offers_IGR, commiten, gpart, '', "... cny02 -->")
    
    root = ET.parse(temp_catalog_offers_IGR).getroot()
    temp_store = []
    for elem in root.findall('offer'):
        count_store_id = elem.attrib['store_id']
        temp_store.append(count_store_id)
    store_id = int(temp_store[-1])
    print("\t" + "... catalog_offers_IGR")
    
    for part in gset_partList:
        # ---
        repair_cost = get_repair_cost(temp + f"\\Game\\Items\\Armor\\{part}.xml")
        # ---
        print("\t" + "... last store_id = ", store_id)
        store_id = store_id + 1
        template_ItemsFilter_offer = f"""\n\t<offer store_id="{store_id}" item_name="{part}" description="@ui_armor_{part}" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="36000" repair_cost="{repair_cost}" quantity="0" offer_status="NEW" key_item_name="" game_money="15000" cry_money="0" crown_money="0" key_item_money="0"/>\n</offers>"""

        modifyChanges(temp_catalog_offers_IGR, template_ItemsFilter_offer, part, '', "")
#=========================================================
# DRIVE
#=========================================================
def main():
    fileStructure(createTempFolders)
    ItemsFilter_gset()
    assetsItemsIcons_gset()
    catalog_offers_IGR()
    input(Fore.LIGHTBLUE_EX + '...Complete ' + Style.RESET_ALL)

if __name__ == "__main__":
    
    gset_partList = []
    sss = []
    master, temp = Ask_Path()

    master_ItemsFilter_randombox = master + "\\Game\\Libs\\Config\\ItemsFilter_randombox.xml"
    master_assetsItemsIcons = master + "\\Game\\Libs\\Config\\UI\\assetsItemsIcons.xml"
    master_randomBoxesIcons = master + "\\Game\\Libs\\Config\\UI\\randomBoxesIcons.xml"
    master_catalog_offers_IGR = master + "\\Game\\Libs\\Config\\Shop\\catalog_offers_IGR.xml"
# ----------------
    temp_ItemsFilter_randombox = temp + "\\Game\\Libs\\Config\\ItemsFilter_randombox.xml"
    temp_assetsItemsIcons = temp + "\\Game\\Libs\\Config\\UI\\assetsItemsIcons.xml"
    temp_randomBoxesIcons = temp + "\\Game\\Libs\\Config\\UI\\randomBoxesIcons.xml"
    temp_catalog_offers_IGR = temp + "\\Game\\Libs\\Config\\Shop\\catalog_offers_IGR.xml"

    createTempFolders = [temp + "\\Game\\Libs\\Config\\UI",
                        temp + "\\Game\\Libs\\Config\\Shop"]
    main()
    