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
        [sg.InputText(default_text = r"d:\\temp_skins", key = "-MOD-"), sg.FolderBrowse()],
        [sg.OK(key='OK'), sg.Cancel()]
    ]
    window = sg.Window('\U0001f638 integSkins', layout)

    while True:
        event, values = window.read(close=True)
        
        # MERS
        mersList = {"ar":"R", "sr":"S","shg":"M","smg":"E", "pt":"MERS_pt", "kn":"MERS_kn"}
        
        master, mod_repo = values["-MASTER-"], values["-MOD-"]
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
    copyFile(temp_ItemsFilter_skins, master_ItemsFilter_skins)
    # RandomboxFilter
    copyFile(temp_ItemsFilter_randombox, master_ItemsFilter_randombox)
    # UI
    copyFile(temp_UIweaponsItemsIcons, master_UIweaponsItemsIcons)
    copyFile(temp_UIrandomBoxesIcons, master_UIrandomBoxesIcons)
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
def get_Skins():
    mersList = {"ar":"R", "sr":"S","shg":"M","smg":"E", "pt":"MERS_pt", "kn":"MERS_kn"}
    for root,_,files in os.walk(temp + "\\Game\\Objects\\Weapons\\"):
        files = files
        
        for item in files:
            if  ".mtl" in item and "_d.mtl" not in item and "_tp" not in item:
                item = item.split('.')[0]
                # print(item)
            
                dest = os.path.join(root, '').replace(".mtl", ".xml")
                # print(dest)
                if "sa0" not in item and "_d_" not in item:
                    tempDict.update({item:dest})
    
    for i in tempDict:
        defaultAttach = []
        specialAttach = []
        identMers = []
        
        hashable = i.split('_')[0].strip('0123456789')
        mers =  mersList[hashable]
        identMers.append(mers)
        
        for _,_,files in os.walk(tempDict[i]):
            # print(files)
            break
        
        for defaultFile in files:
            if '_d.mtl' in defaultFile and '_tp' not in defaultFile:
                defaultAttach.append(defaultFile.split('.')[0])
            if '_sa0' in defaultFile and '_tp' not in defaultFile:
                specialAttach.append(defaultFile.split('.')[0])

            
        skinsDict.update({i:[defaultAttach,specialAttach, identMers]})
    
    for skin in skinsDict:
        print(f"skin -- {skin}\ndefaultAttach -- {skinsDict[skin][0]}\nspecialAttach -- {skinsDict[skin][1]}\nmers -- {skinsDict[skin][2]}\n")
#---------------------------------------------------------
def get_lastGrep(path):
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
    return int(temp[0])
#---------------------------------------------------------
def returnPose(item):
    root = ET.parse(temp + UIweaponsItemsIcons).getroot()

    for poseElement in root.findall('image'):
        poseInter = poseElement.attrib['name']
        if item + '_' in poseInter and '_thumbnail' in poseInter:
            print(f'_thumbnail -- {poseInter}')
            
            element_item = poseInter
            pos_thumnail = poseElement.attrib['pos']
            x_pos_thumbnail = pos_thumnail.split(',')[0]
            y_pos_thumbnail = pos_thumnail.split(',')[1]
            
            size_thumnail = poseElement.attrib['size']
            print('---'*10)
            print(f'pos = {pos_thumnail}, size = {size_thumnail}')
            print(f'x_pos = {x_pos_thumbnail}, y_pos = {y_pos_thumbnail}\n')
            break
    
    for sizeElement in root.findall('image'):
        sizeInter = sizeElement.attrib['name']
        if element_item.split('_thumbnail')[0] in sizeInter:
            print(f"donor skin -- {sizeInter}")
            
            pos_icon = sizeElement.attrib['pos']
            x_pos_icon = pos_icon.split(',')[0]
            y_pos_icon = pos_icon.split(',')[1]
            
            size_icon = sizeElement.attrib['size']
            x_size_icon = size_icon.split(',')[0]
            
            print('---'*10)
            print(f'pos = {pos_icon}, size = {size_icon}')
            print(f"x_pos = {x_pos_icon}, y_pos = {y_pos_icon}\n")
            # print(f"x_size_icon = {x_size_icon}\n")
            break
    
    xSize = int(x_size_icon)
    xPose_thumb = int(x_pos_thumbnail) - int(x_pos_icon)
    yPose_thumb = int(y_pos_thumbnail) - int(y_pos_icon)
    
    print(f" --- Returning for {item}:\nxSize = {xSize}\nxPose_thumb = {xPose_thumb}\nyPose_thumb = {yPose_thumb}")
    return xSize, xPose_thumb, yPose_thumb 
#---------------------------------------------------------
# Items + Achievements
#---------------------------------------------------------
def skin_ItemRandomBox():
    
    for skin in skinsDict:
        weapon_type = skin.split('_')[0].strip("0123456789")
        if weapon_type == 'kn':
            skin01 = skin
        else:
            skin01 = skin + "_shop"
        
        
        pattern_ItemRandomBox = f"""<shop_item name="box_{skin}" type="random_box">
        <mmo_stats>
            <param name="item_category" value="RandomBox"/>
            <param name="shopcontent" value="1"/>
            <param name="classes" value="RESMH"/>
            <param name="max_buy_amount" value="32000" />
            <param name="stackable" value="1" />
        </mmo_stats>
        <UI_stats>
            <param name="name" value="@box_{skin}_name"/>
            <param name="description" value="@box_1_item_desc"/>
            <param name="icon" value="icons_randombox_{skin}"/>
        </UI_stats>
        <random_box>
            <group>
                <item name="{skin01}" weight="10"/>
                <item name="{skin01}" expiration="3h" weight="150"/>
                <item name="{SKINcontent_Randombox[weapon_type][0]}" expiration="3h" weight="168"/>
                <item name="{SKINcontent_Randombox[weapon_type][1]}" expiration="3h" weight="168"/>
                <item name="{SKINcontent_Randombox[weapon_type][2]}" expiration="3h" weight="168"/>
                <item name="{SKINcontent_Randombox[weapon_type][3]}" expiration="3h" weight="168"/>
                <item name="{SKINcontent_Randombox[weapon_type][4]}" expiration="3h" weight="168"/>
            </group>
        </random_box>\n</shop_item>"""

        writeChanges(temp + f"\\Game\\Items\\ShopItems\\box_{skin}.xml", pattern_ItemRandomBox)
#---------------------------------------------------------
def skin_Achievements():
    
    idNumber = get_lastGrep(master_achievements)
    for skin in skinsDict:
        Achievepath = temp + f"\\Game\\Libs\\Config\\Achievements\\{skin}_Kill.xml"
        idNumber = idNumber + 1
        print(gSpace + 'Achievements grep_id = ' + str(idNumber))
        
        weapon_type = skin.split('_')[0].strip("0123456789")
        if weapon_type == 'kn':
            skin01 = skin
        else:
            skin01 = skin + "_shop"
        
        pattern_Achievements = f"""<Achievement active="1" id="{idNumber}" kind="kills" MS_side="0" amount="1500">
        <UI name="@{skin}_Kill" desc="@{skin}_Kill_desc"/>
        <Filters>
            <Filter kind="enemy" param="1"/>
            <Filter kind="weapon" param="{skin01}"/>
            <Filter kind="claymore" param="0"/>
            <Filter kind="grenade" param="0"/>
            <Filter kind="kill_zone" param="0"/>
            <Filter kind="explosion" param="0"/>
        </Filters>
        <BannerImage image="challenge_stripe_{skin}" type="stripe"/>\n</Achievement>"""
        
        writeChanges(Achievepath, pattern_Achievements)
#---------------------------------------------------------
def integrate_Items():
    skin_ItemRandomBox()
    skin_Achievements()
#---------------------------------------------------------
# ItemsFilter
#---------------------------------------------------------
def ItemsFilter_skin():
    
    for skin in skinsDict:
        weapon_type = skin.split('_')[0].strip("0123456789")
        
        if weapon_type == 'shg':
            add = """\n\t\t<Rifleman/>
        <Recon/>
        <Engineer/>
        <Medic level="1"/>"""
        elif weapon_type == 'smg':
            add = """\n\t\t<Rifleman/>
        <Recon/>
        <Engineer level="1"/>
        <Medic/>"""
        elif weapon_type == 'ar':
            add = """\n\t\t<Rifleman level="1"/>
        <Recon/>
        <Engineer/>
        <Medic/>"""
        elif weapon_type == 'sr':
            add = """\n\t\t<Rifleman/>
        <Recon level="1"/>
        <Engineer/>
        <Medic/>"""
        else:
            add = """\n\t\t<Rifleman level="1"/>
        <Recon level="1"/>
        <Engineer level="1"/>
        <Medic level="1"/>"""
        
        
        if weapon_type == 'kn':
            skin01 = skin
            template_base = f"""\n\t<Item name="{skin}">
        <Rifleman level="1"/>
        <Recon level="1"/>
        <Engineer level="1"/>
        <Medic level="1"/>\n\t</Item>\n\t<Item name="{skin}skin_shop">
        <Rifleman level="1"/>
        <Recon level="1"/>
        <Engineer level="1"/>
        <Medic level="1"/>\n\t</Item>\n</ClassFilters>"""
        else:
            template_base = f"""\n\t<Item name="{skin}">{add}
    </Item>	
    <Item name="{skin}_shop">{add}
    </Item>	
    <Item name="{skin}skin_shop">{add}\n\t</Item>\n</ClassFilters>"""
            skin01 = skin + "_shop"

        modifyChanges(temp_ItemsFilter_skins, template_base, skin, '', '')
#---------------------------------------------------------
def ItemsFilter_skin_SA():
    
    for skin in skinsDict:
        for attach in skinsDict[skin][1]:
            print(attach)

            specialAttach = f"""
    <Item name="{attach}">
        <Rifleman level="1"/>
        <Recon level="1"/>
        <Engineer level="1"/>
        <Medic level="1"/>
    </Item>\n</ClassFilters>"""
            
            modifyChanges(temp_ItemsFilter_skins, specialAttach, attach, '', '')
#---------------------------------------------------------
def ItemsFilter_randomboxx():
    for skin in skinsDict:
        
        template_ItemsFilter_randombox = f"""
    <Item name="box_{skin}">
        <Rifleman level="1"/>
        <Recon level="1"/>
        <Engineer level="1"/>
        <Medic level="1"/>
        <Heavy level="1"/>
    </Item>\n</ClassFilters>"""
    
        modifyChanges(temp_ItemsFilter_randombox, template_ItemsFilter_randombox, skin, "", "")
#---------------------------------------------------------
def intagrate_ItemFilter():
    ItemsFilter_skin()
    ItemsFilter_skin_SA()
    ItemsFilter_randomboxx()
#---------------------------------------------------------

#---------------------------------------------------------
# UI
#---------------------------------------------------------
def UI_randomBoxesIconss():
    for skin in skinsDict:
        template_UI_randomBoxesIconss = f"""\n\t<image name="icons_randombox_{skin}" file="Libs\Icons\RandomBoxes\Weapons\icons_randombox_{skin}.tif" pos="0,0" size="256,128" />\n</images>"""
        modifyChanges(temp_UIrandomBoxesIcons, template_UI_randomBoxesIconss, skin, 'icons_randombox_', "")
#---------------------------------------------------------
def UI_challengesIconss():
    for skin in skinsDict:
    
        template_UI_challengesIconss = f"""\n\t<image name="challenge_stripe_{skin}" file="Libs/Icons/Challenges/challenge_stripe_{skin}.tif" pos="0,0" size="512,128"/>\n</images>"""

        modifyChanges(temp_UIchallengesIcons, template_UI_challengesIconss, skin, 'challenge_stripe_', "")
#---------------------------------------------------------поправить позицию _thumbnail, или забить болт и править руками
def UI_weaponsItemsIconss():
    for skin in skinsDict:

        weapon_type = skin.split('_')[0]
        try:
            x_size, x_pose, y_pose = returnPose(weapon_type)
        except:
            # что здесь еще можно сделать
            weapon_type = skin.split('_')[0].strip("0123456789")
            x_size = '400'
            if weapon_type == 'ar':
                x_size = '500'
            if weapon_type == 'sr':
                x_size = '700'

            x_pose = '230'
            y_pose = '30'

        template_UI_weaponsItemsIconss = f"""\n
    <image name="{skin}" file="Libs\Icons\weapons\{skin.split('_')[0]}\weapons_{skin}.tif" pos="0,0" size="{x_size},200" />
    <image name="{skin}_thumbnail" file="Libs\Icons\weapons\{skin.split('_')[0]}\weapons_{skin}.tif" pos="{x_pose},{y_pose}" size="140,140" />\n</images>"""

        modifyChanges(temp_UIweaponsItemsIcons, template_UI_weaponsItemsIconss, skin,'', "")
#---------------------------------------------------------
def intagrate_UI():
    UI_randomBoxesIconss()
    UI_challengesIconss()
    UI_weaponsItemsIconss()
#---------------------------------------------------------
# catalog_offers_IGR
#---------------------------------------------------------
def intagrate_catalog_offers_IGR():

    for skin in skinsDict:
        
        weapon_type = skin.split('_')[0].strip("0123456789")
        if weapon_type == 'kn':
            skin01 = skin
        else:
            skin01 = skin + "_shop"
            
        root = ET.parse(temp_catalog_offers_IGR).getroot()
        temp_store = []
        for elem in root.findall('offer'):
            count_store_id = elem.attrib['store_id']
            temp_store.append(count_store_id)
        
        store_id = int(temp_store[-1])
        print(gSpace + "... catalog_offers_IGR")
        print(gSpace + "... last store_id = ", store_id)

        repair_cost = get_repair_cost(temp + f"\\Game\\Items\\Weapons\\{skin01}.xml", skin)
        commiten = f"<!-- skin... {skin} -->"
        
        
        template_catalog_offers_IGR = f"""\n\t{commiten}
    <offer store_id="{store_id + 1}" item_name="{skin01}" description="@{skin01}" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="{repair_cost}" quantity="0" offer_status="NEW" key_item_name="" game_money="15000" cry_money="0" crown_money="0" key_item_money="0"/>
    <offer store_id="{store_id + 2}" item_name="box_{skin}" description="@box_1_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="5" crown_money="0"/>
    <offer store_id="{store_id + 3}" item_name="box_{skin}" description="@box_1_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="4" crown_money="0"/>
    <offer store_id="{store_id + 4}" item_name="box_{skin}" description="@box_1_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="3" crown_money="0"/>
    <offer store_id="{store_id + 5}" item_name="box_{skin}" description="@box_1_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="2" crown_money="0"/>
    <offer store_id="{store_id + 6}" item_name="box_{skin}" description="@box_1_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="1" crown_money="0"/>\n</offers>"""
        
        modifyChanges(temp_catalog_offers_IGR, template_catalog_offers_IGR, skin, '', '')
#=========================================================
# DRIVE
#=========================================================
def main():
    fileStructure(createTempFolders)
    integrate_Items()
    intagrate_ItemFilter()
    intagrate_UI()
    intagrate_catalog_offers_IGR()
    input(Fore.LIGHTBLUE_EX + '...Complete ' + Style.RESET_ALL)

if __name__ == "__main__":
    
    tempDict = {}
    skinsDict = {}
    gSpace = "\t"
    master, temp = Ask_Path()
    get_Skins()
    
    ItemsFilter_skins = f"\\Game\\Libs\\Config\\ItemsFilter_skins.xml"
    ItemsFilter_randombox = "\\Game\\Libs\\Config\\ItemsFilter_randombox.xml"
    
    UIweaponsItemsIcons = "\\Game\\Libs\\Config\\UI\\weaponsItemsIcons.xml"
    UIattachmentsItemsIcons = "\\Game\\Libs\\Config\\UI\\attachmentsItemsIcons.xml"
    UIrandomBoxesIcons = "\\Game\\Libs\\Config\\UI\\randomBoxesIcons.xml"
    UIchallengesIcons = "\\Game\\Libs\\Config\\UI\\challengesIcons.xml"

    catalog_offers_IGR = "\\Game\\Libs\\Config\\Shop\\catalog_offers_IGR.xml"

    master_achievements = master + "\\Game\\Libs\\Config\\Achievements\\"
    master_ItemsFilter_skins = master + ItemsFilter_skins
    master_ItemsFilter_randombox = master + ItemsFilter_randombox
    master_UIweaponsItemsIcons = master + UIweaponsItemsIcons
    master_UIattachmentsItemsIcons = master + UIattachmentsItemsIcons
    master_UIrandomBoxesIcons = master + UIrandomBoxesIcons
    master_UIchallengesIcons = master + UIchallengesIcons
    master_catalog_offers_IGR = master + catalog_offers_IGR
# ----------------
    temp_ItemsFilter_skins = temp + ItemsFilter_skins
    temp_ItemsFilter_randombox = temp + ItemsFilter_randombox
    temp_UIweaponsItemsIcons = temp + UIweaponsItemsIcons
    temp_UIattachmentsItemsIcons = temp + UIattachmentsItemsIcons
    temp_UIrandomBoxesIcons = temp + UIrandomBoxesIcons
    temp_UIchallengesIcons = temp + UIchallengesIcons
    temp_catalog_offers_IGR = temp + catalog_offers_IGR
    

#=========================================================
# Global stuff
#=========================================================

    createTempFolders = [temp + "\\Game\\Items\\ShopItems",
                        temp + "\\Game\\Libs\\Config\\Achievements",
                        temp + "\\Game\\Libs\\Config\\UI",
                        temp + "\\Game\\Libs\\Config\\Shop"]

    SKINcontent_Randombox =                                             {
        "ar":[       'ar13_drum_01_console_shop',
                    'ar45_shop',
                    'ar37_shop',
                    'ar43_shop',
                    'ar35_shop'],
        "shg":[       'shg40_rift01_console_shop',
                    'shg58_shop',
                    'shg54_shop',
                    'shg57_shop',
                    'shg50_shop'],
        "smg":[       'smg51_shop',
                    'smg50_shop',
                    'smg09_custom_shop',
                    'smg54_shop',
                    'smg49_shop'],
        "sr":[       'sr51_shop',
                    'sr52_shop',
                    'sr47_shop',
                    'sr48_shop',
                    'sr42_shop'],
        "pt":[ 'pt39_shop',
                    'pt36_shop',
                    'pt38_shop',
                    'pt37_shop',
                    'pt33_shop'],
        "kn":[ 'kn19',
                    'kn21',
                    'kn45',
                    'kn00004',
                    'kn52_console']
                                                                    }
    main()