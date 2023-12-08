import os
from re import template
import xml.etree.ElementTree as ET
import os.path
import PySimpleGUI as sg
import shutil
import random
import time
from colorama import init, Style, Fore
init(convert=True)

sg.theme('DarkGrey13')
#---------------------------------------------------------
#                       --- GLOBAL ---
#---------------------------------------------------------
def AskPath(key): 
    layout = [
        [sg.Text("WPC_master", text_color='yellow')],
        [sg.InputText(default_text = f"{ProjPath}", key = "-MASTER-"),sg.FolderBrowse()],
        [sg.Text("Temp Folder", text_color='yellow')],
        [sg.Text(r"path to content", text_color="grey")],
        [sg.InputText(default_text = r"d:\\", key = "-MOD-"), sg.FolderBrowse()],
        [sg.OK(key='OK'), sg.Cancel()]
    ]
    if key == None:
        exit(0)
    window = sg.Window(f'intagration -- {key}', layout)
    while True:
        event, values = window.read(close=True)
        master, mod_repo = values["-MASTER-"], values["-MOD-"]
        print(Fore.BLUE + "----"*26 + Style.RESET_ALL + f"\n{mod_repo}\n" + Fore.BLUE + "----"*26 + Style.RESET_ALL)
        # =========================
        if key == "custom" or key == "new":
            if event in ('Cancel', None) or event == sg.WIN_CLOSED:
                break
            mersList = {"ar":"R", "sr":"S","shg":"M","smg":"E", "kn":"MERS", "pt":"MERS_pt", "pt":"MERS_kn",}
            customPath = values["-MOD-"] + '\\Game\\Objects\\Weapons\\'
            for _,dirs,_ in os.walk(customPath):
                for i in dirs:
                    custom_Weapon = i
                break
            hashable = custom_Weapon.strip('0123456789')
            print("\t" + f"new {key} = " + custom_Weapon)
            print("\t" + f"weapon type = {hashable}")
            mers =  mersList[hashable]
            return master, mod_repo, custom_Weapon, mers
        # =========================
        if key == 'skin' or key == "charm":
            if event in ('Cancel', None) or event == sg.WIN_CLOSED:
                break
            mersList = {"ar":"R", "sr":"S","shg":"M","smg":"E", "pt":"MERS_pt", "kn":"MERS_kn"}
            return master, mod_repo, '', ''
        # =========================
        if key == "gearset":
            if event in ('Cancel', None) or event == sg.WIN_CLOSED:
                break
            for _,_,files in os.walk(mod_repo + "\\Game\\Items\\Armor\\"):
                for i in files:
                    gset = i.split('.')[0]
                    gset_partList.append(gset)
                    print(f'GSet part -- {gset}')
                    item = i.split('_')[1]
                    if item in GSetTemp_sss:
                        pass
                    else:
                        GSetTemp_sss.append(item)
            return master, mod_repo, '', ''
        # =========================
        if key == "fbs":
            if event in ('Cancel', None) or event == sg.WIN_CLOSED:
                break
            for _,_,files in os.walk(mod_repo + "\\Game\\Items\\Skins\\"):
                for i in files:
                    if "fbs" in i:
                        fbs = i.split('.')[0]
                        print(f'Fbs name -- {fbs}')
                    break
            return master, mod_repo, fbs, ''
        # =========================
        if key == "achieve":
            if event in ('Cancel', None) or event == sg.WIN_CLOSED:
                break
            for _,_,files in os.walk(mod_repo + "\\Game\\Libs\\Icons\\Challenges\\"):
                for i in files:
                    if i.endswith('.tif'):
                        i = i.split('.')[0]
                        ach_list.append(i)
                        print(f"achievement -- {i}")
            return master, mod_repo, '', ''
        # =========================
        if key == "bundle":
            if event in ('Cancel', None) or event == sg.WIN_CLOSED:
                break
            for _,_,files in os.walk(mod_repo + "\\Game\\Libs\\Icons\\"):
                for i in files:
                    if i.endswith('.tif') and "bundle_item" in i:
                        i = i.split('.')[0]
                        bundleList.append(i)
                        print(f"bundle item -- {i}")
            return master, mod_repo, '', ''
            
        # =========================
        if event in ('Cancel', None) or event == sg.WIN_CLOSED:
            break
    window.close()
def list_to_string(l):
    str1 = '\n'
    return (str1.join(l))
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
def writeChanges(path, template):
    try:
        open(path, 'a').close()
        open(path, 'r+').write(template)
        print(Fore.GREEN + f"Complete... {path}" + Style.RESET_ALL + Fore.LIGHTBLUE_EX + " ...Added" + Style.RESET_ALL)
    except:
        print(Fore.RED + f"---FAILED... PATH ---> {path}" + Style.RESET_ALL)
def modifyChanges_ALT(template, arg01):
    
    path = temp + ItemsFilter_weapon
    if arg01 == "_gold01":
        path = temp + ItemsFilter_skins
    
    file = open(path)
    item = var01 + f'{arg01}_shop'
    try:
        if (item in file.read()):
            print(Fore.YELLOW + f"--- WARNING...  {item} in {path}  ...already exists" + Style.RESET_ALL)
        else:
            with open(path, 'a') as f:
                f.writelines(template)
            f.close()
            print(Fore.GREEN + f"Complete... {path}" + Style.RESET_ALL)
    except:
        print(Fore.RED + f"---FAILED... {path}" + Style.RESET_ALL)
def modifyChanges_NC(path, template, prompt01, prompt02):
    
    file = open(path)
    item = prompt01 + var01 + prompt02
    try:
        if (item in file.read()):
            print(Fore.YELLOW + f"--- WARNING...  {item} in {path}  ...already exists" + Style.RESET_ALL)
        else:
            remove_lastline(path)
            with open(path, 'a') as f:
                f.writelines(template)
            f.close()
            print(Fore.GREEN + f"Complete... {path}" + Style.RESET_ALL + Fore.LIGHTMAGENTA_EX + " ...Modified" + Style.RESET_ALL)
    except:
        print(Fore.RED + f"---FAILED... {path}" + Style.RESET_ALL)
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
            print(Fore.GREEN + f"Complete... {path}" + Style.RESET_ALL + Fore.LIGHTMAGENTA_EX + f" {skins} ...Modified" + Style.RESET_ALL)
    except:
        print(Fore.RED + f"---FAILED... {path}" + Style.RESET_ALL)
def copyFile(temp, master):
    if os.path.exists(temp):
        pass
    else:
        shutil.copyfile(master, temp)
def check_and_create(path):
    if os.path.exists(path) == True:
        pass
    else:
        os.makedirs(path)
#---------------------------------------------------------
#                         GET
#---------------------------------------------------------
def get_ProjPath():
    path = os.path.dirname(os.path.realpath(__name__)) + "\\Integration_Starter.ini"
    if os.path.exists(path) and len(open(path).read()) > 0 and os.path.exists(open(path).read()):
        pass
    else:
        projectPath = sg.popup_get_folder('Project path...', no_titlebar=True, grab_anywhere=True)
        open(path, 'a').close()
        open(path, 'w').write(projectPath)
    ProjPath = open(path).read()
    return ProjPath
def get_Key():
    layout = [
        [sg.Button("Intagrate -- Custom weapon", key="custom")],
        [sg.Button("Intagrate -- New weapon (gold + default)", key="new")],
        [sg.Button("Intagrate -- Weapon Skins", key="skin")],
        [sg.Button("Intagrate -- Charms", key="charm")],
        [sg.Button("Intagrate -- Gear Sets", key="gearset")],
        [sg.Button("Intagrate -- FBS", key="fbs")],
        [sg.Button("Intagrate -- Achievements", key="achieve")],
        [sg.Button("Intagrate -- Bundle Item", key="bundle")],
        [sg.Cancel(button_color="RED")]
    ]
    window = sg.Window('\U0001f638 integ ver.0', layout, grab_anywhere=1)

    while True:
        event, _ = window.read(close=1)
        if event == "Cancel" or event == None:
            pass
        else:
            # Ask_Path(key=event)
            return event
        if event in ('Cancel', None) or event == sg.WIN_CLOSED:
            break
    window.close()
def get_RandomBoxPistol(BoxPistol):
    lenboxpistol = len(BoxPistol[var02])
    time.sleep(0.125)
    randomNum = random.randint(0, lenboxpistol) 
    time.sleep(0.125)
    randomPistol = BoxPistol[var02][randomNum-1]
    time.sleep(0.125)
    print(gSpace + f'mers = {var02}')
    print(gSpace + f"lenboxpistol = {lenboxpistol}")
    print(gSpace + f"randomBoxPistol = {randomPistol}")
    return randomPistol
def get_Charms():
    for _, dirs, _ in os.walk(f"{temp}\\Game\\Objects\\Attachments\\charms\\"):
        dirs = dirs
        break
    
    for i in dirs:
        print(f"get charm... {i}")
    return dirs
def get_playerClass():
    if var02 == 'M':
        playerClass = """<Rifleman/>
		<Recon/>
		<Engineer/>
		<Medic level="1"/>"""
    elif var02 == 'E':
        playerClass = """<Rifleman/>
		<Recon/>
		<Engineer level="1"/>
		<Medic/>"""
    elif var02 == 'S':
        playerClass = """<Rifleman/>
		<Recon level="1"/>
		<Engineer/>
		<Medic/>"""
    elif var02 == 'R':
        playerClass = """<Rifleman level="1"/>
		<Recon/>
		<Engineer/>
		<Medic/>"""
    else:
        playerClass = """<Rifleman level="1"/>
		<Recon level="1"/>
		<Engineer level="1"/>
		<Medic level="1"/>"""
  
    return playerClass
def get_AttachList():
    for _, _, files in os.walk(temp + AttachPath):
        files = files
        break
    
    playerClass = get_playerClass()
    
    attach_Lst = []
    for attach in files:
        if attach.endswith('_d.xml') or attach.endswith("_d_folded.xml"):
            attach = attach.split(".xml")[0]
            print(gSpace + f"attach --- {attach}")
            attach_Lst.append(f"""\n\t<Item name="{attach}">\n\t\t{playerClass}\n\t</Item>""")       

    return attach_Lst
def get_AttachList_GOLD():
    for _, _, files in os.walk(temp + AttachPath):
        files = files
        break
    
    playerClass = get_playerClass()
    
    GOLDattach_Lst = []
    for attach in files:
        if attach.endswith('_d.mtl') and "gold0" in attach:
            attach = attach.split(".mtl")[0]
            print(gSpace + f"GOLD_attach --- {attach}")
            GOLDattach_Lst.append(f"""\n\t<Item name="{attach}">\n\t\t{playerClass}\n\t</Item>""")
    
    return GOLDattach_Lst
def get_tempFolders():
    if key == "new":
        createTempFolders = [temp + "\\Game\\Items\\ShopItems",
                            temp + "\\Game\\Items\\KeyItems",
                            temp + "\\Game\\Libs\\Config\\Achievements",
                            temp + "\\Game\\Libs\\Config\\UI",
                            temp + "\\Game\\Libs\\Config\\Shop",
                            temp + "\\Game\\Animations"]
    if key == "custom":
        createTempFolders = [temp + "\\Game\\Items\\ShopItems",
                            temp + "\\Game\\Items\\Cards",
                            temp + "\\Game\\Libs\\Config\\Achievements",
                            temp + "\\Game\\Libs\\Config\\UI",
                            temp + "\\Game\\Libs\\Config\\MasterServer",
                            temp + "\\Game\\Libs\\Config\\Shop",
                            temp + "\\Game\\Animations"]
    if key == "skin":
        createTempFolders = [temp + "\\Game\\Items\\ShopItems",
                            temp + "\\Game\\Libs\\Config\\Achievements",
                            temp + "\\Game\\Libs\\Config\\UI",
                            temp + "\\Game\\Libs\\Config\\Shop"]
    if key == "gearset":
        createTempFolders = [temp + "\\Game\\Libs\\Config\\UI",
                            temp + "\\Game\\Libs\\Config\\Shop"]
    if key == "fbs":
        createTempFolders = [temp + "\\Game\\Items\\ShopItems",
                            temp + "\\Game\\Libs\\Config\\UI",
                            temp + "\\Game\\Libs\\Config\\Shop"]
    if key == "charm":
        createTempFolders = [temp + '\\Game\\Items\\Accessories',
                            temp + '\\Game\\Objects\\Attachments\\Charms',
                            temp + '\\Game\\Libs\\Icons',
                            temp + "\\Game\\Libs\\Config\\UI\\charms",
                            temp + "\\Game\\Libs\\Config\\Shop"]
    if key == "achieve":
        createTempFolders = [temp + "\\Game\\Items\\ShopItems",
                            temp + "\\Game\\Libs\\Config\\Achievements",
                            temp + "\\Game\\Libs\\Config\\UI",
                            temp + "\\Game\\Libs\\Config\\Shop"]
    if key == "bundle":
        createTempFolders = [temp + "\\Game\\Items\\ShopItems",
                            temp + "\\Game\\Libs\\Config\\UI",
                            temp + "\\Game\\Libs\\Config\\Shop"]
    return createTempFolders
def get_pos(item):
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
def get_ContentRandombox():
    ContentRandombox = {
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
                    'sr42_shop'],
        
        "MERS_pt":[ 'pt39_shop',
                    'pt36_shop',
                    'pt38_shop',
                    'pt37_shop',
                    'pt33_shop'],
        
        "MERS_kn":[ 'kn19',
                    'kn21',
                    'kn45',
                    'kn00004',
                    'kn52_console'],
        }
    return ContentRandombox
def get_BoxPistol():
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
                'pt39_shdw00001_shop']}
    return BoxPistol
def get_repair_cost(path):
    try:
        root = ET.parse(path).getroot()
        for elem in root.find('mmo_stats').findall('param'):
            if elem.attrib['name'] == "repair_cost":
                value = elem.attrib['value']
                if "_gold01_" in path:
                    print(f"{gSpace}... {var01}_gold01 repair_cost = {value}")
                else:
                    print(f"{gSpace}... {var01} repair_cost = {value}")
                return value
    except FileNotFoundError:
        print(Fore.RED + f"--- FileNotFoundError... {path}" + Style.RESET_ALL)
def get_repair_cost_SKIN(path, skin):
    try:
        root = ET.parse(path).getroot()
        for elem in root.find('mmo_stats').findall('param'):
            if elem.attrib['name'] == "repair_cost":
                value = elem.attrib['value']
                print(f"{gSpace}... {skin} repair_cost = {value}")
                return value
    except FileNotFoundError:
        print(Fore.RED + f"--- FileNotFoundError... {path}" + Style.RESET_ALL)
def get_Skins():
    mersList = {"ar":"R", "sr":"S","shg":"M","smg":"E", "pt":"MERS_pt", "kn":"MERS_kn"}
    for root,_,files in os.walk(temp + "\\Game\\Objects\\Weapons\\"):
        files = files
        for item in files:
            if  ".mtl" in item and "_d.mtl" not in item and "_tp" not in item:
                item = item.split('.')[0]
                dest = os.path.join(root, '').replace(".mtl", ".xml")
                if "sa0" not in item and "_d_" not in item:
                    tempDict.update({item:dest})
    
    for i in tempDict:
        defaultAttach = []
        specialAttach = []
        identMers = []
        
        hashable = i.split('_')[0].strip('0123456789')
        mers =  mersList[hashable]
        identMers.append(mers)
        
        for rsa, rdir, rfiles in os.walk(tempDict[i]):
            rfiles = rfiles
            break
        for r in rfiles:
            if r.endswith('.cgf') and '_sa0' in r and '_tp' not in r:
                specialAttach.append(r.split('.')[0])
                
        for defaultFile in files:
            if '_d.mtl' in defaultFile and '_tp' not in defaultFile:
                defaultAttach.append(defaultFile.split('.')[0])
            # if defaultFile.endswith('_folded.xml'):
            #     defaultAttach.append(defaultFile.split('.')[0])
            #     print('********************************'*10 + defaultFile)
        #     if '_sa0' in defaultFile and '_tp' not in defaultFile:
        #         specialAttach.append(defaultFile.split('.')[0])
        skinsDict.update({i:[defaultAttach,specialAttach, identMers]})
    for skin in skinsDict:
        print(f"skin -- {skin}\ndefaultAttach -- {skinsDict[skin][0]}\nspecialAttach -- {skinsDict[skin][1]}\nmers -- {skinsDict[skin][2]}\n")
    for i in skinsDict:
        ShedulerList.append(i)
        ShedulerList.append(i + "skin_shop")
        if 'kn' not in i.split('_')[0]:
            ShedulerList.append(i + "_shop")

    return defaultAttach, specialAttach
def get_lastGrep():
    master_achievements = master + achievements
    temp = [0]
    for inroot,_,files in os.walk(master_achievements):
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
def get_AchieveSkin(achieve):
    if "_0" in achieve:
        test = achieve.split('_')[-1]
        item = "_" + test
        skin = achieve.split(item)[0].split('_')[-1]
        ending = "_" + achieve.split('_')[-1]
        
        print("++++"*13)
        print("SKIN ----- ", skin)
    elif "_fbs_" in achieve:
        skin = "fbs_" +  achieve.split('_')[-1]
        ending = ''
    else:
        skin = achieve.split('_')[-1]
        ending = ''
    return skin, ending
def get_bundleItem_content(testSkin):
    iconsPath = master + bundleItem
    bundleItem_contentList = []
       
    for _, _, files in os.walk(iconsPath):
        for searchingItem in files:
            if testSkin in searchingItem and searchingItem.endswith('.tif'):
                searchingItem = searchingItem.split('.tif')[0]
                
                if 'charm' in searchingItem:
                    searchingItem = searchingItem + "_shop"
                    bundleItem_contentList.append(f"""\n\t\t\t<item name="{searchingItem}" regular=""/>""")
                
                if "weapons_" in searchingItem:
                    searchingItem = searchingItem.split('weapons_')[1]
                    if "kn" in searchingItem.split('_')[0]:
                        bundleItem_contentList.append(f"""\n\t\t\t<item name="{searchingItem}" regular=""/>""")
                    else:
                        searchingItem01 = searchingItem + "_shop"
                        searchingItem02 = searchingItem + "skin_shop"
                        
                        bundleItem_contentList.append(f"""\n\t\t\t<item name="{searchingItem01}" regular=""/>""")
                        bundleItem_contentList.append(f"""\n\t\t\t<item name="{searchingItem02}" regular=""/>""")

                if "badge" in searchingItem or "mark" in searchingItem:
                    searchingItem = searchingItem.split('challenge_')[1]
                    if "_fbs_" in searchingItem:
                        specialType = searchingItem.split('_fbs_')[0]
                        searchingItem = f"unlock_fbs_{testSkin}_{specialType}"
                        bundleItem_contentList.append(f"""\n\t\t\t<item name="{searchingItem}" regular=""/>""")
                    else:
                        specialType_01 = searchingItem.split('_')[0]
                        specialType_02 = searchingItem.split(specialType_01 + "_")[1]
                        searchingItem = f"unlock_{specialType_02}_{specialType_01}"
                        bundleItem_contentList.append(f"""\n\t\t\t<item name="{searchingItem}" regular=""/>""")

                if f"stripe_{testSkin}" in searchingItem:
                    specialType = searchingItem.split("challenge_stripe_")[1]
                    searchingItem = f"unlock_{specialType}_stripe"
                    bundleItem_contentList.append(f"""\n\t\t\t<item name="{searchingItem}" regular=""/>""")
    bundleItem_contentList.sort()
    
    for _, _, files in os.walk(master + f"\\Game\\Items\\Skins"):
        for skin_Item in files:
            if testSkin in skin_Item:
                skin_Item = skin_Item.split('.')[0]
                bundleItem_contentList.insert(0, f"""\n\t\t\t<item name="{skin_Item}" regular=""/>""")
                
    bundleItem_contentList.append("""\n\t\t</bundle>\n\t</shop_item>""")
    
    return bundleItem_contentList
#---------------------------------------------------------
#                         TEMPLATE
#---------------------------------------------------------
def FileStructure():
      
    createTempFolders = get_tempFolders()
    for tempFolder in createTempFolders:
        check_and_create(tempFolder)
        
    if key == "new":
        copyFile(temp + ItemsFilter_weapon, master + ItemsFilter_weapon)
        copyFile(temp + ItemsFilter_randombox, master + ItemsFilter_randombox)
        copyFile(temp + ItemsFilter_key, master + ItemsFilter_key)
        copyFile(temp + ItemsFilter_skins, master + ItemsFilter_skins)
        copyFile(temp + UIweaponsItemsIcons, master + UIweaponsItemsIcons)
        copyFile(temp + UIattachmentsItemsIcons, master + UIattachmentsItemsIcons)
        copyFile(temp + UIrandomBoxesIcons, master + UIrandomBoxesIcons)
        copyFile(temp + UIchallengesIcons, master + UIchallengesIcons)
        copyFile(temp + UICombatLogIcons, master + UICombatLogIcons)
        copyFile(temp + Animations_cba, master + Animations_cba)
        copyFile(temp + catalog_offers_IGR, master + catalog_offers_IGR)
    if key == "custom":
        copyFile(temp + ItemsFilter_weapon, master + ItemsFilter_weapon)
        copyFile(temp + ItemsFilter_randombox, master + ItemsFilter_randombox)
        copyFile(temp + ItemsFilter_cards, master + ItemsFilter_cards)
        copyFile(temp + UIweaponsItemsIcons, master + UIweaponsItemsIcons)
        copyFile(temp + UIattachmentsItemsIcons, master + UIattachmentsItemsIcons)
        copyFile(temp + UIrandomBoxesIcons, master + UIrandomBoxesIcons)
        copyFile(temp + UIchallengesIcons, master + UIchallengesIcons)
        copyFile(temp + UICombatLogIcons, master + UICombatLogIcons)
        copyFile(temp + UIcards, master + UIcards)
        copyFile(temp + Animations_cba, master + Animations_cba)
        copyFile(temp + card_progressions_01, master + card_progressions_01)
        copyFile(temp + card_progressions_02, master + card_progressions_02)
        copyFile(temp + card_progressions_03, master + card_progressions_03)   
        copyFile(temp + catalog_offers_IGR, master + catalog_offers_IGR)
    if key == "skin":
        copyFile(temp + ItemsFilter_skins, master + ItemsFilter_skins)
        copyFile(temp + ItemsFilter_randombox, master + ItemsFilter_randombox)
        copyFile(temp + UIweaponsItemsIcons, master + UIweaponsItemsIcons)
        copyFile(temp + UIrandomBoxesIcons, master + UIrandomBoxesIcons)
        copyFile(temp + UIchallengesIcons, master + UIchallengesIcons)
        copyFile(temp + catalog_offers_IGR, master + catalog_offers_IGR)
    if key == "gearset":
        for item in GSetTemp_sss:
            copyFile(temp + f"\\Game\\Libs\\Config\\ItemsFilter_{item}.xml", master + f"\\Game\\Libs\\Config\\ItemsFilter_{item}.xml")
        copyFile(temp + assetsItemsIcons, master + assetsItemsIcons)
        copyFile(temp + catalog_offers_IGR, master + catalog_offers_IGR)
    if key == "fbs":
        copyFile(temp + ItemsFilter_fbs, master + ItemsFilter_fbs)
        copyFile(temp + ItemsFilter_randombox, master + ItemsFilter_randombox)
        copyFile(temp + assetsItemsIcons, master + assetsItemsIcons)
        copyFile(temp + UIrandomBoxesIcons, master + UIrandomBoxesIcons)
        copyFile(temp + catalog_offers_IGR, master + catalog_offers_IGR)
    if key == "charm":       
        copyFile(temp + ItemsFilter_charm, master + ItemsFilter_charm)
        copyFile(temp + UIcharm, master + UIcharm) 
        copyFile(temp + catalog_offers_IGR, master + catalog_offers_IGR)
    if key == "achieve":        
        copyFile(temp + ItemsFilter_special, master + ItemsFilter_special)
        copyFile(temp + UIchallengesIcons, master + UIchallengesIcons)
        copyFile(temp + catalog_offers_IGR, master + catalog_offers_IGR)
    if key == "bundle":
        copyFile(temp + ItemsFilter_randombox, master + ItemsFilter_randombox)
        copyFile(temp + UIrandomBoxesIcons, master + UIrandomBoxesIcons)
        copyFile(temp + catalog_offers_IGR, master + catalog_offers_IGR)
def template_NEW_ItemRandomBox():
    ContentRandombox = get_ContentRandombox()
    pattern_ItemRandomBox = f"""<shop_item name="box_{var01}" type="random_box">
	<mmo_stats>
		<param name="item_category" value="RandomBox"/>
		<param name="shopcontent" value="1"/>
		<param name="classes" value="RESMH"/>
		<param name="max_buy_amount" value="32000" />
		<param name="stackable" value="1" />
	</mmo_stats>
	<UI_stats>
		<param name="name" value="@box_{var01}_name"/>
		<param name="description" value="@box_1_item_desc"/>
		<param name="icon" value="icons_randombox_{var01}"/>
	</UI_stats>
	<random_box>
		<group>
			<item name="{var01}_gold01_shop" weight="1" top_prize_token="box_token_cry_money_{var01}" win_limit="1000"/>
			<item name="{var01}_shop" weight="10"/>
            <item name="bundle_smugglers_card_{var01}" weight="20"/>
            <item name="{var01}_shop" expiration="3h" weight="150"/>
            <item name="{ContentRandombox[var02][0]}" expiration="3h" weight="165"/>
			<item name="{ContentRandombox[var02][1]}" expiration="3h" weight="165"/>
			<item name="{ContentRandombox[var02][2]}" expiration="3h" weight="165"/>
			<item name="{ContentRandombox[var02][3]}" expiration="3h" weight="165"/>
			<item name="{ContentRandombox[var02][4]}" expiration="3h" weight="159"/>
		</group>
	</random_box>\n</shop_item>"""
    return pattern_ItemRandomBox
def template_NEW_Achievements():
    idNumber = get_lastGrep()
    idNumber = idNumber + 1
    print(gSpace + f'--- {var01} --- Achievements grep_id = ' + str(idNumber))
    
    pattern_Achievements = f"""<Achievement active="1" id="{idNumber}" kind="kills" MS_side="0" amount="2500">
	<UI name="@{var01}_Kill" desc="@{var01}_Kill_desc"/>
	<Filters>
		<Filter kind="enemy" param="1"/>
		<Filter kind="weapon" param="{var01}_shop"/>
		<Filter kind="claymore" param="0"/>
		<Filter kind="grenade" param="0"/>
		<Filter kind="kill_zone" param="0"/>
		<Filter kind="explosion" param="0"/>
	</Filters>
	<BannerImage image="challenge_stripe_{var01}" type="stripe"/>\n</Achievement>"""
    return pattern_Achievements, idNumber
def template_NEW_Achievements_GOLD(idNumber):
    idNumber = idNumber + 1
    print(gSpace + f'--- {var01}_gold01 --- Achievements grep_id = ' + str(idNumber))

    pattern_Achievements_GOLD = f"""<Achievement active="1" id="{idNumber}" kind="kills" MS_side="0" amount="999">
	<UI name="@{var01}_Kill" desc="@{var01}_Kill_desc"/>
	<Filters>
		<Filter kind="enemy" param="1"/>
		<Filter kind="weapon" param="{var01}_gold01_shop"/>
		<Filter kind="claymore" param="0"/>
		<Filter kind="grenade" param="0"/>
		<Filter kind="kill_zone" param="0"/>
		<Filter kind="explosion" param="0"/>
	</Filters>
	<BannerImage image="challenge_stripe_{var01}_gold01" type="stripe"/>\n</Achievement>"""
    return pattern_Achievements_GOLD
def template_NEW_keyItems():
    pattern_keyItems = f"""<shop_item name="key_box_{var01}" type="key">
	<mmo_stats>
		<param name="item_category" value="Misc"/>
		<param name="shopcontent" value="1"/>
		<param name="classes" value="RESMH"/>
		<param name="max_buy_amount" value="32000"/>
		<param name="stackable" value="0"/>
		<param name="testcontent" value="0"/>
	</mmo_stats>
	<UI_stats>
		<param name="name" value="@key_smugg_card"/>
		<param name="description" value="@key_box_{var01}_desc"/>
		<param name="icon" value="randombox_card_{var01}"/>
	</UI_stats>\n</shop_item>"""
    return pattern_keyItems
def template_NEW_box_token():
    pattern_box_token = f"""<shop_item name="box_token_cry_money_{var01}" type="top_prize_token">
	<mmo_stats>
		<param name="item_category" value="TopPrizeToken"/>
		<param name="shopcontent" value="1"/>
		<param name="classes" value="RESMH"/>
		<param name="max_buy_amount" value="32000"/>
		<param name="stackable" value="1"/>
	</mmo_stats>
	<UI_stats>
		<param name="name" value="@box_token_cry_money_{var01}_name"/>
		<param name="description" value="@box_token_cry_money_{var01}_description"/>
		<param name="icon" value="tbd_icon"/>
	</UI_stats>\n</shop_item>"""
    return pattern_box_token
def template_NEW_bundle_smugglers():
    pattern_bundle_smugglers = f"""<?xml version="1.0" ?>\n<shop_item name="bundle_smugglers_card_{var01}" type="bundle">
        <mmo_stats>
            <param name="item_category" value="Bundle"/>
            <param name="shopcontent" value="1"/>
            <param name="classes" value="RESMH"/>
        </mmo_stats>
        <UI_stats>
            <param name="name" value="@key_smugg_card"/>
            <param name="description" value="@ui_key_box_{var01}"/>
            <param name="icon" value="randombox_card_{var01}"/>
        </UI_stats>
        <bundle>
            <item name="key_box_{var01}" expiration="12h"/>
            <item name="{var01}_shop" expiration="1h"/>
        </bundle>\n</shop_item>"""
    return pattern_bundle_smugglers
def template_CUSTOM_ItemRandomBox():
    ContentRandombox = get_ContentRandombox()
    BoxPistol = get_BoxPistol()

    randomPistol = get_RandomBoxPistol(BoxPistol)
    pattern_ItemRandomBox = f"""<shop_item name="box_{var01}" type="random_box">
	<mmo_stats>
		<param name="item_category" value="RandomBox"/>
		<param name="shopcontent" value="1"/>
		<param name="classes" value="RESMH"/>
		<param name="max_buy_amount" value="32000" />
		<param name="stackable" value="1" />
	</mmo_stats>
	<UI_stats>
		<param name="name" value="@box_{var01}_name"/>
		<param name="description" value="@box_1_item_desc"/>
		<param name="icon" value="icons_randombox_{var01}"/>
	</UI_stats>
	<random_box>
		<group>
			<item name="{var01}_shop" weight="10"/>
            <item name="{randomPistol}" weight="10"/>
			<item name="{var01}_shop" expiration="3h" weight="180"/>
			<item name="{ContentRandombox[var02][0]}" expiration="3h" weight="160"/>
			<item name="{ContentRandombox[var02][1]}" expiration="3h" weight="160"/>
			<item name="{ContentRandombox[var02][2]}" expiration="3h" weight="160"/>
			<item name="{ContentRandombox[var02][3]}" expiration="3h" weight="160"/>
			<item name="{ContentRandombox[var02][4]}" expiration="3h" weight="160"/>
		</group>
	</random_box>\n</shop_item>"""
    return pattern_ItemRandomBox
def template_CUSTOM_ItemRandomboxBoxCard():
    pattern_ItemRandomboxBoxCard = f"""<shop_item name="box_{var01}_card" type="random_box">
        <mmo_stats>
            <param name="item_category" value="RandomBox"/>
            <param name="shopcontent" value="1"/>
            <param name="classes" value="RESMH"/>
            <param name="max_buy_amount" value="32000"/>
            <param name="stackable" value="1"/>
        </mmo_stats>
        <UI_stats>
            <param name="name" value="@box_{var01}_cards_name"/>
            <param name="description" value="@box_2_item_desc"/>
            <param name="icon" value="icons_randombox_{var01}_cards"/>
        </UI_stats>
        <random_box>
            <group>
                <item name="{var01}_card" amount="1000" weight="5"/>
                <item name="{var01}_card" amount="500" weight="6"/>
                <item name="{var01}_card" amount="250" weight="7"/>
                <item name="{var01}_card" amount="100" weight="10"/>
                <item name="{var01}_card" amount="50" weight="11"/>
                <item name="{var01}_card" amount="25" weight="25"/>
                <item name="{var01}_card" amount="10" weight="70"/>
                <item name="{var01}_card" amount="5" weight="400"/>
                <item name="{var01}_card" amount="1" weight="466"/>
            </group>
            <group>
                <item name="{var01}_shop" expiration="3h" weight="33"/>
                <item name="{var01}_shop" expiration="6h" weight="32"/>
                <item name="{var01}_shop" expiration="9h" weight="30"/>
                <item name="{var01}_shop" expiration="12h" weight="28"/>
                <item name="{var01}_shop" expiration="18h" weight="22"/>
                <item name="{var01}_shop" expiration="1d" weight="10"/>
            </group>
        </random_box>\n</shop_item>"""
    return pattern_ItemRandomboxBoxCard
def template_CUSTOM_ItemCard():
    pattern_ItemCard = f"""<shop_item name="{var01}_card" type="card">
  <mmo_stats>
    <param name="item_category" value="Card" />
    <param name="shopcontent" value="1" />
    <param name="max_buy_amount" value="32000" />
    <param name="stackable" value="1" />
    <param name="priority" value="1" />
    <param name="classes" value="{var02}"/>
  </mmo_stats>
  <UI_stats>
    <param name="name" value="@{var01}_card_name" />
    <param name="description" value="@{var01}_card_desc" />
    <param name="icon" value="icons_{var01}_template" />
  </UI_stats>\n</shop_item>"""
    return pattern_ItemCard
def template_CUSTOM_Achievements():
    idNumber = get_lastGrep() + 1
    print(gSpace + f'--- {var01} --- Achievements grep_id = ' + str(idNumber))
    
    pattern_Achievements = f"""<Achievement active="1" id="{idNumber}" kind="kills" MS_side="0" amount="1500">
	<UI name="@{var01}_Kill" desc="@{var01}_Kill_desc"/>
	<Filters>
		<Filter kind="enemy" param="1"/>
		<Filter kind="weapon" param="{var01}_shop"/>
		<Filter kind="claymore" param="0"/>
		<Filter kind="grenade" param="0"/>
		<Filter kind="kill_zone" param="0"/>
		<Filter kind="explosion" param="0"/>
	</Filters>
	<BannerImage image="challenge_stripe_{var01}" type="stripe"/>\n</Achievement>"""
    return pattern_Achievements
def template_SKIN_ItemRandomBox(skin):
    
    SKINcontent_Randombox = {
    "ar":[      'ar13_drum_01_console_shop',
                'ar45_shop',
                'ar37_shop',
                'ar43_shop',
                'ar35_shop'],
    
    "shg":[     'shg40_rift01_console_shop',
                'shg58_shop',
                'shg54_shop',
                'shg57_shop',
                'shg50_shop'],
    
    "smg":[     'smg51_shop',
                'smg50_shop',
                'smg09_custom_shop',
                'smg54_shop',
                'smg49_shop'],
    
    "sr":[       'sr51_shop',
                'sr52_shop',
                'sr47_shop',
                'sr48_shop',
                'sr42_shop'],
    
    "pt":[      'pt39_shop',
                'pt36_shop',
                'pt38_shop',
                'pt37_shop',
                'pt33_shop'],
    
    "kn":[      'kn19',
                'kn21',
                'kn45',
                'kn00004',
                'kn52_console']}
    
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
    return pattern_ItemRandomBox
def template_SKIN_Achievements(skin, idNumber):

    weapon_type = skin.split('_')[0].strip("0123456789")
    if weapon_type == 'kn':
        skin01 = skin
    else:
        skin01 = skin + "_shop"
    
    print(gSpace + f'--- {skin} --- Achievements grep_id = ' + str(idNumber))
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
    return pattern_Achievements
def template_FBS_ShopItemsBox():
    FBScontentCreation = {
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
    knive = sg.popup_get_text('Knive skin from the themepack...', default_text="kn19_coldwar01",
                              no_titlebar=1, grab_anywhere=1)
    fbs_name = var01.split('fbs_')[1]
    
    fbs_ShopItemsBox_template = f"""<shop_item name="box_{var01}" type="random_box">
    <mmo_stats>
        <param name="item_category" value="RandomBox"/>
        <param name="shopcontent" value="1"/>
        <param name="classes" value="MERSH"/>
        <param name="max_buy_amount" value="32000" />
        <param name="stackable" value="1" />
    </mmo_stats>
    <UI_stats>
        <param name="name" value="@box_{var01}_name"/>
        <param name="description" value="@box_1_item_desc"/>
        <param name="icon" value="bundle_icon_fbs_{fbs_name}"/>
    </UI_stats>
    <random_box>
        <group>
            <item name="{var01}" weight="10"/>
            <item name="{knive}" weight="10"/>
            <item name="{FBScontentCreation[SkinClass][0]}" expiration="3h" weight="200"/>
            <item name="{FBScontentCreation[SkinClass][1]}" expiration="3h" weight="195"/>
            <item name="{FBScontentCreation[SkinClass][2]}" expiration="3h" weight="195"/>
            <item name="{FBScontentCreation[SkinClass][3]}" expiration="3h" weight="195"/>
            <item name="{FBScontentCreation[SkinClass][4]}" expiration="3h" weight="195"/>
        </group>
    </random_box>\n</shop_item>"""

    # console template
    var02 = "shared" + var01.split(var01.split("_")[0])[1]
    fbs_ShopItemsBox_template_console = f"""<shop_item name="box_{var02}" type="random_box">
    <mmo_stats>
        <param name="item_category" value="RandomBox"/>
        <param name="shopcontent" value="1"/>
        <param name="classes" value="MERSH"/>
        <param name="max_buy_amount" value="32000" />
        <param name="stackable" value="1" />
    </mmo_stats>
    <UI_stats>
        <param name="name" value="@box_{var02}_name"/>
        <param name="description" value="@box_1_item_desc"/>
        <param name="icon" value="bundle_icon_fbs_{fbs_name}"/>
    </UI_stats>
    <random_box>
        <group>
            <item name="{var02}" weight="10"/>
            <item name="{knive}" weight="10"/>
            <item name="{FBScontentCreation[SkinClass][0]}" expiration="3h" weight="200"/>
            <item name="{FBScontentCreation[SkinClass][1]}" expiration="3h" weight="195"/>
            <item name="{FBScontentCreation[SkinClass][2]}" expiration="3h" weight="195"/>
            <item name="{FBScontentCreation[SkinClass][3]}" expiration="3h" weight="195"/>
            <item name="{FBScontentCreation[SkinClass][4]}" expiration="3h" weight="195"/>
        </group>
    </random_box>\n</shop_item>"""
    return fbs_ShopItemsBox_template, fbs_ShopItemsBox_template_console, var02
def template_ACHIEVE_ShopItems(achieve, idNumber):
    
    achieveType = achieve.split('_')[1]
    skin, ending = get_AchieveSkin(achieve)
    # skin = achieve.split('_')[-1]
    
    complexWord = "engineersoldiersnipermedic"
    if achieve.split(achieveType + "_")[1].split('_')[0] in complexWord:
        classWord = achieve.split(achieveType + "_")[1].split('_')[0] + "_"
    else:
        classWord = ''
    
    print(f"{achieve} -- {idNumber}")
    
    Achievepath = temp + f"\\Game\\Libs\\Config\\Achievements\\{classWord}{skin}{ending}_{achieveType}.xml"
    ItemRandomBoxPath = temp + f"\\Game\\Items\\ShopItems\\unlock_{classWord}{skin}{ending}_{achieveType}.xml"
    
    pattern_Achievements = f"""<?xml version="1.0" ?>
    <Achievement active="1" id="{idNumber}" kind="hidden" MS_side="1" amount="1">
        <UI name="@{classWord}{skin}_{achieveType}" desc="@{classWord}{skin}{ending}_{achieveType}_desc"/>
        <BannerImage image="{achieve}" type="{achieveType}"/>
    </Achievement>"""
    
    pattern_ItemRandomBox = f"""<?xml version="1.0" ?>
    <shop_item name="unlock_{classWord}{skin}{ending}_{achieveType}" type="meta_game">
        <mmo_stats>
            <param name="item_category" value="Emblem"/>
            <param name="shopcontent" value="1"/>
            <param name="classes" value="RESM"/>
            <param name="max_buy_amount" value="1"/>
        </mmo_stats>
        <UI_stats>
            <param name="name" value="@{classWord}{skin}{ending}_{achieveType}"/>
            <param name="description" value="@{classWord}{skin}{ending}_{achieveType}_desc"/>
            <param name="icon" value="{achieve}"/>
        </UI_stats>
        <metagame_stats>
            <on_activate unlock_achievement="{idNumber}"/>
        </metagame_stats>
    </shop_item>"""
    
    return Achievepath, pattern_Achievements, ItemRandomBoxPath, pattern_ItemRandomBox
def template_BUNDLE_ShopItems(bundle):
    skin = bundle.split("_")[-1]
    bundleItem_contentList = get_bundleItem_content(skin)
 
    BundleRandomBoxPath = temp + f"\\Game\\Items\\ShopItems\\{bundle}.xml"
    BundleRandomBoxPath_console = temp + f"\\Game\\Items\\ShopItems\\{bundle}_console.xml"

    pattern_bundle = f"""<?xml version="1.0" ?>
    <shop_item name="{bundle}" type="bundle">
        <mmo_stats>
            <param name="item_category" value="Bundle"/>
            <param name="shopcontent" value="1"/>
            <param name="classes" value="RESMH"/>
        </mmo_stats>
        <UI_stats>
            <param name="name" value="@{bundle}"/>
            <param name="description" value="@{bundle}_description"/>
            <param name="icon" value="{bundle}"/>
        </UI_stats>
        <bundle>"""
    
    pattern_bundle_console = f"""<?xml version="1.0" ?>
    <shop_item name="{bundle}_console" type="bundle">
        <mmo_stats>
            <param name="item_category" value="Bundle"/>
            <param name="shopcontent" value="1"/>
            <param name="classes" value="RESMH"/>
        </mmo_stats>
        <UI_stats>
            <param name="name" value="@{bundle}"/>
            <param name="description" value="@{bundle}_description"/>
            <param name="icon" value="{bundle}"/>
        </UI_stats>
        <bundle>"""
    return pattern_bundle, pattern_bundle_console, BundleRandomBoxPath, BundleRandomBoxPath_console
def template_ItemsFilter_weapon(arg01):
    playerClass = get_playerClass()
    
    template_NEW_ItemsFilter_weapon = f"""
    <Item name="{var01}{arg01}">
		{playerClass}
	</Item>
	<Item name="{var01}{arg01}_shop">
		{playerClass}
	</Item>\n</ClassFilters>"""
    return template_NEW_ItemsFilter_weapon
def template_NEW_ItemsFilter_randombox():
    template_ItemsFilter_randombox = f"""
    <Item name="box_{var01}">
		<Rifleman level="1"/>
		<Recon level="1"/>
		<Engineer level="1"/>
		<Medic level="1"/>
		<Heavy level="1"/>
	</Item>
 	<Item name="bundle_smugglers_card_{var01}">
		<Rifleman level="1"/>
		<Recon level="1"/>
		<Engineer level="1"/>
		<Medic level="1"/>
		<Heavy level="1"/>
	</Item>
	<Item name="box_token_cry_money_{var01}">
		<Rifleman level="1"/>
		<Recon level="1"/>
		<Engineer level="1"/>
		<Medic level="1"/>
		<Heavy level="1"/>
	</Item>\n</ClassFilters>"""
    return template_ItemsFilter_randombox
def template_NEW_ItemsFilter_key():
    template_ItemsFilter_key = f"""
    <Item name="key_box_{var01}">
		<Rifleman level="1"/>
		<Recon level="1"/>
		<Engineer level="1"/>
		<Medic level="1"/>
		<Heavy level="1"/>
	</Item>\n</ClassFilters>"""
    return template_ItemsFilter_key
def template_CUSTOM_ItemsFilter_randombox():
    template_ItemsFilter_randombox = f"""
    <Item name="box_{var01}">
		<Rifleman level="1"/>
		<Recon level="1"/>
		<Engineer level="1"/>
		<Medic level="1"/>
		<Heavy level="1"/>
	</Item>\n</ClassFilters>"""
    return template_ItemsFilter_randombox
def template_CUSTOM_ItemsFilter_cards():
    level = 'level="1"'
    m=e=r=s=''
    if var02 == 'M':
        m = level
    elif var02 == 'E':
        e = level
    elif var02 == 'R':
        r = level
    elif var02 == 'S':
        s = level    
    
    template_ItemsFilter_cards = f"""
	<Item name="{var01}_card">
		<Rifleman {r}/>
		<Recon {s}/>
		<Engineer {e}/>
		<Medic {m}/>
		<Heavy />
	</Item>\n</ClassFilters>"""
    return template_ItemsFilter_cards
def template_SKIN_ItemsFilter(skin):
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
    
    return template_base
def template_SKIN_ItemsFilter_skin_SA(attach):
    print(attach)
    specialAttach_template = f"""
    <Item name="{attach}">
        <Rifleman level="1"/>
        <Recon level="1"/>
        <Engineer level="1"/>
        <Medic level="1"/>
    </Item>\n</ClassFilters>"""
    return specialAttach_template
def template_SKIN_ItemsFilter_randombox(skin):
    template_ItemsFilter_randombox = f"""
    <Item name="box_{skin}">
        <Rifleman level="1"/>
        <Recon level="1"/>
        <Engineer level="1"/>
        <Medic level="1"/>
        <Heavy level="1"/>
    </Item>\n</ClassFilters>"""
    return template_ItemsFilter_randombox
def template_GSET_ItemsFilter_gset(part):
    add = ' level="1"'
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

    template_ItemsFilter = f"""
    <Item name="{part}">
        <Rifleman{rif}/>
        <Recon{rec}/>
        <Engineer{eng}/>
        <Medic{med}/>
    </Item>\n</ClassFilters>"""
    return template_ItemsFilter
def template_FBS_ItemsFilter_fbs():
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

    replacer = var01.replace(SkinClass, "shared")

    if "shared" in var01:
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
    <Item name="{var01}">
		<Rifleman{rif}/>
		<Recon{rec}/>
		<Engineer{eng}/>
		<Medic{med}/>
	</Item>\n</ClassFilters>"""
    return template_ItemsFilter_fbs
def template_FBS_ItemsFilter_randombox():
    replacer = var01.replace(SkinClass, "shared")
    if "shared" in var01:
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
    <Item name="box_{var01}">
		<Rifleman level="1"/>
		<Recon level="1"/>
		<Engineer level="1"/>
		<Medic level="1"/>
        <Heavy level="1"/>
	</Item>\n</ClassFilters>"""
    return template_ItemsFilter_randombox
def template_CHARM_ItemFilter(charm):
    template_ItemFilter = f"""\n\t<Item name="{charm}">
		<Rifleman level="1"/>
		<Recon level="1"/>
		<Engineer level="1"/>
		<Medic level="1"/>
		<Heavy/>\n\t</Item>\n</ClassFilters>"""
    return template_ItemFilter
def template_ACHIEVE_ItemFilter(achieve):
        skin, ending = get_AchieveSkin(achieve)
        
        achieveType = achieve.split('_')[1]
        complexWord = "engineersoldiersnipermedic"
        
        if achieve.split(achieveType + "_")[1].split('_')[0] in complexWord:
            classWord = achieve.split(achieveType + "_")[1].split('_')[0] + "_"
        else:
            classWord = ''
        
        template_special = f"""\n\t<Item name="unlock_{classWord}{skin}{ending}_{achieveType}">
        <Rifleman level="1"/>
        <Recon level="1"/>
        <Engineer level="1"/>
        <Medic level="1"/>
        <Heavy/>
    </Item>\n</ClassFilters>"""
        return template_special, skin
def template_BUNDLE_ItemFilter(bundle):
        template_bundle = f"""\n\t<Item name="{bundle}">
        <Rifleman level="1"/>
        <Recon level="1"/>
        <Engineer level="1"/>
        <Medic level="1"/>
        <Heavy level="1"/>
    </Item>\n</ClassFilters>"""
        
        template_bundle_console = f"""\n\t<Item name="{bundle}_console">
        <Rifleman level="1"/>
        <Recon level="1"/>
        <Engineer level="1"/>
        <Medic level="1"/>
        <Heavy level="1"/>
    </Item>\n</ClassFilters>"""
        return template_bundle, template_bundle_console
def template_NEW_UI_randomBoxesIcons():
    template_UI_randomBoxesIconss = f"""\n
	<image name="icons_randombox_{var01}" file="Libs\Icons\RandomBoxes\Weapons\icons_randombox_{var01}.tif" pos="0,0" size="1024,512" />
	<image name="randombox_card_{var01}" file="Libs\Icons\RandomBoxes\SmugglerCards\\randombox_card_{var01}.tif" pos="0,0" size="1024,512"/>\n</images>"""
    return template_UI_randomBoxesIconss
def template_NEW_UI_challengesIcons():
    template_UI_challengesIconss = f"""
    <image name="challenge_stripe_{var01}" file="Libs/Icons/Challenges/challenge_stripe_{var01}.tif" pos="0,0" size="1024,256"/>
    <image name="challenge_stripe_{var01}_gold01" file="Libs/Icons/Challenges/challenge_stripe_{var01}_gold01.tif" pos="0,0" size="1024,256"/>\n</images>"""
    return template_UI_challengesIconss
def template_NEW_UI_weaponsItemsIcons():
    
    x_size = '400'
    if var02 == 'R':
        x_size = '500'
    if var02 == 'S':
        x_size = '700'
        
    ShedulerList.append(var01)
    ShedulerList.append(var01 + "_shop")
    ShedulerList.append(var01 + "_gold01")
    ShedulerList.append(var01 + "_gold01_shop")

    template_UI_weaponsItemsIconss = f"""\n
    <image name="{var01}" file="Libs\Icons\weapons\{var01}\weapons_{var01}.tif" pos="0,0" size="{x_size},200" />
    <image name="{var01}_gold01" file="Libs\Icons\weapons\{var01}\weapons_{var01}_gold01.tif" pos="0,0" size="{x_size},200" />\n</images>"""
    return template_UI_weaponsItemsIconss
def template_NEW_UI_CombatLogIcons():
    template_UI_CombatLogIconss = f"""
 	<image_set file="Libs\Icons\CombatLog\CombatLogIcons_{var01}.tif" offset_x="0" offset_y="0" size_x="192" size_y="96">
		<image name ="{var01}_combatLog"	pos="0,0"	/>
 	</image_set>
    <image_set file="Libs\Icons\CombatLog\CombatLogIcons_{var01}_gold01.tif" offset_x="0" offset_y="0" size_x="192" size_y="96">
		<image name ="{var01}_gold01_combatLog"	pos="0,0"	/>
 	</image_set>\n</images>"""
    return template_UI_CombatLogIconss
def template_NEW_UI_attachmentsItemsIcons():
    for _, _, filen in os.walk(temp + AttachPath):
       filen = filen
       break
    attach_Lst = []
    for attach in filen:
        if attach.endswith('_d.xml'):
            attach = attach.split(".xml")[0]
            # ----
            ShedulerList.append(attach)
            # ----
            x_size = '300'
            if "sr" in attach and 'gp_d' in attach:
                x_size = "300"
            if "gp_d" in attach or "bp_d" in attach or "sp_d" in attach:
                x_size = "200"
    
            attach_Lst.append(f"""\n\t<image name="{attach}" file="Libs\Icons\weapons\{var01}\\attachmentsItemsIcons_{attach}.tif" pos="0,0" size="{x_size},200" cache="1"/>""")
        
        if attach.endswith('_d.mtl') and "gold0" in attach:
            attach = attach.split(".mtl")[0]
            # ----
            ShedulerList.append(attach)
            # ----
            x_size = '300'
            if "sr" in attach and 'gp_d' in attach:
                x_size = "300"
            if "gp_d" in attach or "bp_d" in attach or "sp_d" in attach:
                x_size = "200"
            attach_Lst.append(f"""\n\t<image name="{attach}" file="Libs\Icons\weapons\{var01}\\attachmentsItemsIcons_{attach}.tif" pos="0,0" size="{x_size},200" cache="1"/>""")
            
    attach_Lst.append("\n</images>")
    return attach_Lst
def template_CUSTOM_UI_cards():
    template_UI_cards = f"""\n
    <image name="{var01}_circuit" file="Libs\Icons\cards\craft_cards\{var01}_circuit.tif" pos="0,0" size="560,248"/>
	<image name="{var01}_progression" file="Libs\Icons\cards\craft_cards\{var01}_progression.tif" pos="0,0" size="560,248"/>\n</images>"""
    return template_UI_cards
def template_CUSTOM_UI_randomBoxesIcons():
    template_UI_randomBoxesIconss = f"""\n
	<image name="icons_randombox_{var01}" file="Libs\Icons\RandomBoxes\Weapons\icons_randombox_{var01}.tif" pos="0,0" size="1024,512" />
	<image name="icons_{var01}_template" file="Libs\Icons\RandomBoxes\Templates\icons_{var01}_template.tif" pos="0,0" size="1024,512"/>\n</images>"""
    return template_UI_randomBoxesIconss
def template_CUSTOM_UI_challengesIcons():
    template_UI_challengesIconss = f"""\n\t<image name="challenge_stripe_{var01}" file="Libs/Icons/Challenges/challenge_stripe_{var01}.tif" pos="0,0" size="1024,256"/>\n</images>"""
    return template_UI_challengesIconss
def template_CUSTOM_UI_weaponsItemsIcons():
    x_size = '400'
    if var02 == 'R':
        x_size = '500'
    if var02 == 'S':
        x_size = '700'

    ShedulerList.append(var01)
    ShedulerList.append(var01 + "_shop")
    
    template_UI_weaponsItemsIconss = f"""\n
    <image name="{var01}" file="Libs\Icons\weapons\{var01}\weapons_{var01}.tif" pos="0,0" size="{x_size},200" />\n</images>"""
    return template_UI_weaponsItemsIconss
def template_CUSTOM_UI_attachmentsItemsIcons():
    
    for _, _, filen in os.walk(temp + AttachPath):
       filen = filen
       break

    attach_Lst = []
    for attach in filen:
        if attach.endswith('_d.xml'):
            attach = attach.split(".xml")[0]
    
            ShedulerList.append(attach)
    
            x_size = '300'
            if "sr" in attach and 'gp_d' in attach:
                x_size = "300"
            if "gp_d" in attach or "bp_d" in attach or "sp_d" in attach:
                x_size = "200"
            
            attach_Lst.append(f"""\n\t<image name="{attach}" file="Libs\Icons\weapons\{var01}\\attachmentsItemsIcons_{attach}.tif" pos="0,0" size="{x_size},200" cache="1"/>""")

    attach_Lst.append("\n</images>")
    return attach_Lst
def template_CUSTOM_UI_CombatLogIcons():
    template_UI_CombatLogIconss = f"""
 	<image_set file="Libs\Icons\CombatLog\CombatLogIcons_{var01}.tif" offset_x="0" offset_y="0" size_x="192" size_y="96">
		<image name ="{var01}_combatLog"	pos="0,0"	/>
 	</image_set>\n</images>"""
    return template_UI_CombatLogIconss
def template_FBS_assetsItemsIcons():
    fbs01 = var01.split('fbs_')[1]
    attribFile = r"Libs\Icons\assets\fbs_" + f"{fbs01}" + r"\assets_fb_suits_" + f"{fbs01}" + r'.tif'
    template_assetsItemsIcons = f"""\n
    <image name="{var01}" file="{attribFile}" pos="0,0" size="900,400" />\n</images>"""
    return template_assetsItemsIcons
def template_FBS_randomBoxesIcons():
    fbs01 = var01.split('fbs_')[1]
    sss = r"Libs\Icons\assets\fbs_" + f"{fbs01}" + r"\bundle_icon_fbs_" + f"{fbs01}" + r'.tif'
    template_randomBoxesIcons = f"""\n
    <image name="bundle_icon_fbs_{fbs01}" file="{sss}" pos="0,0" size="1024,512" />\n</images>"""
    return template_randomBoxesIcons
def template_CHARM_Icons(charm):
    template_UI = f"""\n\t<image name="{charm}" file="Libs/Icons/charms/{charm}.tif" pos="0,0" size="512,512"/>
	<image name="{charm}_thumbnail" file="Libs/Icons/charms/{charm}.tif" pos="56,56" size="400,400"/>\n</images>"""
    return template_UI
def template_ACHIEVE_Icons(achieve):
    skin = achieve.split('_')[-1]
    if "_strip" in achieve:
        xSize = '1024'
        ySize = '256'
    else:
        xSize = ySize = "512"

    template_UI_challengesIcons = f"""\n\t<image name="{achieve}" file="Libs/Icons/Challenges/{achieve}.tif" pos="0,0" size="{xSize},{ySize}"/>\n</images>"""
    return template_UI_challengesIcons, skin
def template_BUNDLE_Icons(bundle):

    template_UI_BundleIcons = f"""\n\t<image name="{bundle}" file="Libs/Icons/{bundle}.tif" pos="0,0" size="1024,512"/>\n</images>"""
    return template_UI_BundleIcons
def template_NEW_catalog_offers_IGR():

    root = ET.parse(temp + catalog_offers_IGR).getroot()
    temp_store = []
    for elem in root.findall('offer'):
        count_store_id = elem.attrib['store_id']
        temp_store.append(count_store_id)
    
    store_id = int(temp_store[-1])
    print(gSpace + "... catalog_offers_IGR")
    print(gSpace + "... last store_id = ", store_id)

    repair_cost = get_repair_cost(temp + f"\\Game\\Items\\Weapons\\{var01}_shop.xml")
    repair_cost_GOLD = get_repair_cost(temp + f"\\Game\\Items\\Weapons\\{var01}_gold01_shop.xml")
    commiten = f"<!-- New Weapon... {var01} -->"
    
    template_catalog_offers_IGR = f"""\n\t{commiten}
    <offer store_id="{store_id + 1}" item_name="{var01}_shop" description="@{var01}_shop" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="{repair_cost}" quantity="0" offer_status="NEW" key_item_name="" game_money="15000" cry_money="0" crown_money="0" key_item_money="0"/>
    <offer store_id="{store_id + 2}" item_name="{var01}_shop" description="@{var01}_shop" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="0" quantity="0" offer_status="NEW" key_item_name="key_box_{var01}" game_money="15000" cry_money="0" crown_money="0" key_item_money="0"/>
    <offer store_id="{store_id + 3}" item_name="{var01}_gold01_shop" description="@{var01}_gold01_shop" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="{repair_cost_GOLD}" quantity="0" offer_status="NEW" key_item_name="" game_money="15000" cry_money="0" crown_money="0" key_item_money="0"/>
    <offer store_id="{store_id + 4}" item_name="box_{var01}" description="@box_1_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="5" crown_money="0"/>
	<offer store_id="{store_id + 5}" item_name="box_{var01}" description="@box_1_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="4" crown_money="0"/>
	<offer store_id="{store_id + 6}" item_name="box_{var01}" description="@box_1_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="3" crown_money="0"/>
	<offer store_id="{store_id + 7}" item_name="box_{var01}" description="@box_1_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="2" crown_money="0"/>
	<offer store_id="{store_id + 8}" item_name="box_{var01}" description="@box_1_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="1" crown_money="0"/>\n</offers>"""
    return template_catalog_offers_IGR
def template_CUSTOM_catalog_offers_IGR():
    root = ET.parse(temp + catalog_offers_IGR).getroot()
    temp_store = []
    for elem in root.findall('offer'):
        count_store_id = elem.attrib['store_id']
        temp_store.append(count_store_id)
    
    store_id = int(temp_store[-1])
    print(gSpace + "... catalog_offers_IGR")
    print(gSpace + "... last store_id = ", store_id)

    repair_cost = get_repair_cost(temp + f"\\Game\\Items\\Weapons\\{var01}_shop.xml")
    commiten = f"<!-- NewCustom... {var01} -->"
    
    template_catalog_offers_IGR = f"""\n\t{commiten}
    <offer store_id="{store_id + 1}" item_name="{var01}_shop" description="@{var01}_shop" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="{repair_cost}" quantity="0" offer_status="NEW" key_item_name="" game_money="15000" cry_money="0" crown_money="0" key_item_money="0"/>
	<offer store_id="{store_id + 2}" item_name="box_{var01}" description="@box_1_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="5" crown_money="0"/>
	<offer store_id="{store_id + 3}" item_name="box_{var01}" description="@box_1_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="4" crown_money="0"/>
	<offer store_id="{store_id + 4}" item_name="box_{var01}" description="@box_1_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="3" crown_money="0"/>
	<offer store_id="{store_id + 5}" item_name="box_{var01}" description="@box_1_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="2" crown_money="0"/>
	<offer store_id="{store_id + 6}" item_name="box_{var01}" description="@box_1_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="1" crown_money="0"/>\n</offers>"""
    return template_catalog_offers_IGR
def template_SKIN_catalog_offers_IGR(skin):
    
    weapon_type = skin.split('_')[0].strip("0123456789")
    if weapon_type == 'kn':
        skin01 = skin
    else:
        skin01 = skin + "_shop"
    root = ET.parse(temp + catalog_offers_IGR).getroot()
    temp_store = []
    for elem in root.findall('offer'):
        count_store_id = elem.attrib['store_id']
        temp_store.append(count_store_id)
    
    store_id = int(temp_store[-1])
    print(gSpace + "... catalog_offers_IGR")
    print(gSpace + "... last store_id = ", store_id)

    repair_cost = get_repair_cost_SKIN(temp + f"\\Game\\Items\\Weapons\\{skin01}.xml", skin)
    commiten = f"<!-- skin... {skin} -->"
    
    template_catalog_offers_IGR = f"""\n\t{commiten}
    <offer store_id="{store_id + 1}" item_name="{skin01}" description="@{skin01}" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="{repair_cost}" quantity="0" offer_status="NEW" key_item_name="" game_money="15000" cry_money="0" crown_money="0" key_item_money="0"/>
    <offer store_id="{store_id + 2}" item_name="{skin}skin_shop" description="@{skin}" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="0" quantity="0" offer_status="NEW" key_item_name="" game_money="0" cry_money="500" crown_money="0"/>
    <offer store_id="{store_id + 3}" item_name="box_{skin}" description="@box_1_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="5" crown_money="0"/>
    <offer store_id="{store_id + 4}" item_name="box_{skin}" description="@box_1_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="4" crown_money="0"/>
    <offer store_id="{store_id + 5}" item_name="box_{skin}" description="@box_1_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="3" crown_money="0"/>
    <offer store_id="{store_id + 6}" item_name="box_{skin}" description="@box_1_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="2" crown_money="0"/>
    <offer store_id="{store_id + 7}" item_name="box_{skin}" description="@box_1_item_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="1" crown_money="0"/>\n</offers>"""
    return template_catalog_offers_IGR
def template_FBS_catalog_offers_IGR():
    
    root = ET.parse(temp + catalog_offers_IGR).getroot()
    temp_store = []
    for elem in root.findall('offer'):
        count_store_id = elem.attrib['store_id']
        temp_store.append(count_store_id)
    
    store_id = int(temp_store[-1])
    print("\t" + "... catalog_offers_IGR")
    print("\t" + "... last store_id = ", store_id)
    
    replacer = var01.replace(SkinClass, "shared")
    commiten01 = f"<!-- FBS... {var01} -->"
    commiten02 = f"<!-- FBS... {replacer} -->"

    if "shared" in var01:
        shared_addon = ''
    else:
        shared_addon = f"""\n\t{commiten01}
    <offer store_id="{store_id + 7}" item_name="{var01}" description="@ui_armor_{var01}" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="0" quantity="0" offer_status="NEW" key_item_name="" game_money="300" cry_money="0" crown_money="0"/>
	<offer store_id="{store_id + 8}" item_name="box_{var01}" description="box_{var01}_description" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="5" crown_money="0"/>
	<offer store_id="{store_id + 9}" item_name="box_{var01}" description="box_{var01}_description" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="4" crown_money="0"/>
	<offer store_id="{store_id + 10}" item_name="box_{var01}" description="box_{var01}_description" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="3" crown_money="0"/>
	<offer store_id="{store_id + 11}" item_name="box_{var01}" description="box_{var01}_description" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="2" crown_money="0"/>
	<offer store_id="{store_id + 12}" item_name="box_{var01}" description="box_{var01}_description" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="1" crown_money="0"/>"""
 
    template_ItemsFilter_offer = f"""\n\t{commiten02}
    <offer store_id="{store_id + 1}" item_name="{replacer}" description="@ui_armor_{replacer}" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="0" quantity="0" offer_status="NEW" key_item_name="" game_money="300" cry_money="0" crown_money="0"/>
	<offer store_id="{store_id + 2}" item_name="box_{replacer}" description="box_{replacer}_description" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="5" crown_money="0"/>
	<offer store_id="{store_id + 3}" item_name="box_{replacer}" description="box_{replacer}_description" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="4" crown_money="0"/>
	<offer store_id="{store_id + 4}" item_name="box_{replacer}" description="box_{replacer}_description" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="3" crown_money="0"/>
	<offer store_id="{store_id + 5}" item_name="box_{replacer}" description="box_{replacer}_description" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="2" crown_money="0"/>
	<offer store_id="{store_id + 6}" item_name="box_{replacer}" description="box_{replacer}_description" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="1" crown_money="0"/>{shared_addon}\n</offers>"""
    return template_ItemsFilter_offer
def template_EntitySheduler(item):
    template_Sheduler = f"""\n\t<Class name="{item}" policy="gun"/>\n</EntityScheduler>"""
    return template_Sheduler
#---------------------------------------------------------
#                       - ITEMS -
#---------------------------------------------------------    
def NEW_ItemRandomBox():
    temp_ShopItemsBox = temp + ShopItemsBox
    pattern_ItemRandomBox = template_NEW_ItemRandomBox()
    writeChanges(temp_ShopItemsBox, pattern_ItemRandomBox)
def NEW_Achievements():
    temp_configAchievements = temp + configAchievements
    temp_configAchievements_GOLD = temp + configAchievements_GOLD
    
    pattern_Achievements, idNumber = template_NEW_Achievements()
    pattern_Achievements_GOLD = template_NEW_Achievements_GOLD(idNumber)
    writeChanges(temp_configAchievements, pattern_Achievements)
    writeChanges(temp_configAchievements_GOLD, pattern_Achievements_GOLD)
def NEW_keyItems():
    temp_keyItems = temp + keyItems
    pattern_keyItems = template_NEW_keyItems()
    writeChanges(temp_keyItems, pattern_keyItems)
def NEW_box_token():
    temp_box_token = temp + box_token
    pattern_box_token = template_NEW_box_token()
    writeChanges(temp_box_token, pattern_box_token)
def NEW_bundle_smugglers():
    temp_bundle_smugglers = temp + bundle_smugglers
    pattern_bundle_smugglers = template_NEW_bundle_smugglers()
    writeChanges(temp_bundle_smugglers, pattern_bundle_smugglers)
#---------------------------------------------------------
def CUSTOM_ItemRandomBox():
    temp_ShopItemsBox = temp + ShopItemsBox
    pattern_ItemRandomBox = template_CUSTOM_ItemRandomBox()
    writeChanges(temp_ShopItemsBox, pattern_ItemRandomBox)
def CUSTOM_ItemRandomboxBoxCard():
    temp_ShopItemsBoxCard = temp + ShopItemsBoxCard
    pattern_ItemRandomboxBoxCard = template_CUSTOM_ItemRandomboxBoxCard()
    writeChanges(temp_ShopItemsBoxCard, pattern_ItemRandomboxBoxCard)
def CUSTOM_ItemCard():
    temp_ItemsCards = temp + ItemsCards
    pattern_ItemCard = template_CUSTOM_ItemCard()    
    writeChanges(temp_ItemsCards, pattern_ItemCard)
def CUSTOM_Achievements():
    temp_configAchievements = temp + configAchievements
    pattern_Achievements = template_CUSTOM_Achievements()
    writeChanges(temp_configAchievements, pattern_Achievements)
#---------------------------------------------------------
def SKIN_ItemRandomBox():
    for skin in skinsDict:
        pattern_ItemRandomBox = template_SKIN_ItemRandomBox(skin)
        writeChanges(temp + f"\\Game\\Items\\ShopItems\\box_{skin}.xml", pattern_ItemRandomBox)
def SKIN_Achievements():
    idNumber = get_lastGrep()
    for skin in skinsDict:
        Achievepath = temp + f"\\Game\\Libs\\Config\\Achievements\\{skin}_Kill.xml"
        idNumber = idNumber + 1
        pattern_Achievements = template_SKIN_Achievements(skin, idNumber)
        
        writeChanges(Achievepath, pattern_Achievements)
#---------------------------------------------------------
def FBS_ShopItemsBox():
    fbs_ShopItemsBox_template, fbs_ShopItemsBox_template_console, var02 = template_FBS_ShopItemsBox()
    temp_ShopItemsBox = temp + ShopItemsBox
    temp_ShopItemsBox_console = f"\\Game\\Items\\ShopItems\\box_{var02}.xml"
    
    writeChanges(temp_ShopItemsBox, fbs_ShopItemsBox_template)
    writeChanges(temp_ShopItemsBox_console, fbs_ShopItemsBox_template_console)
#---------------------------------------------------------
def ACHIEVE_ShopItems():
    idNumber = get_lastGrep()
    
    for achieve in ach_list:
        idNumber = int(idNumber) + 1
        Achievepath, pattern_Achievements, ItemRandomBoxPath, pattern_ItemRandomBox = template_ACHIEVE_ShopItems(achieve, idNumber)
        
        writeChanges(Achievepath, pattern_Achievements)
        writeChanges(ItemRandomBoxPath, pattern_ItemRandomBox)
#---------------------------------------------------------
def BUNDLE_ShopItems():
    for bundle in bundleList:
        skin = bundle.split("_")[-1]
        bundleItem_contentList = get_bundleItem_content(skin)

        pattern_bundle,pattern_bundle_console, BundleRandomBoxPath, BundleRandomBoxPath_console = template_BUNDLE_ShopItems(bundle)
        
        writeChanges(BundleRandomBoxPath, pattern_bundle)
        writeChanges(BundleRandomBoxPath_console, pattern_bundle_console)
        
        with open(BundleRandomBoxPath, 'a') as f:
            f.writelines(bundleItem_contentList)
        with open(BundleRandomBoxPath_console, 'a') as f:
            f.writelines(bundleItem_contentList)
#---------------------------------------------------------
#                   -- ITEMFILTER --
#---------------------------------------------------------
def NEW_ItemsFilter_weapon():
    attach_Lst = get_AttachList()
    template_NEW_ItemsFilter_weapon = template_ItemsFilter_weapon('')
 
    if len(attach_Lst) != 0:
        modifyChanges_NC(temp + ItemsFilter_weapon, attach_Lst, '', '')
        modifyChanges_ALT(template_NEW_ItemsFilter_weapon,'')
    else:
        modifyChanges_NC(temp + ItemsFilter_weapon, template_NEW_ItemsFilter_weapon, '', '')
def NEW_ItemFilter_weapon_GOLD():
    AttachList_GOLD = get_AttachList_GOLD()
    template_NEW_ItemsFilter_weapon = template_ItemsFilter_weapon('_gold01')
 
    if len(AttachList_GOLD) != 0:
        modifyChanges_NC(temp + ItemsFilter_skins, AttachList_GOLD, '', '')
        modifyChanges_ALT(template_NEW_ItemsFilter_weapon, "_gold01")
    else:
        modifyChanges_NC(temp + ItemsFilter_skins, template_NEW_ItemsFilter_weapon, '', '')
def NEW_ItemsFilter_randombox():
    template_ItemsFilter_randombox = template_NEW_ItemsFilter_randombox()
    modifyChanges_NC(temp + ItemsFilter_randombox, template_ItemsFilter_randombox, "box_", "")
def NEW_ItemsFilter_key():
    template_ItemsFilter_key = template_NEW_ItemsFilter_key()
    modifyChanges_NC(temp + ItemsFilter_key, template_ItemsFilter_key, """<Item name="key_box_""", "")
#---------------------------------------------------------
def CUSTOM_ItemsFilter_weapon():
    attach_Lst = get_AttachList()
    template_CUSTOM_ItemsFilter_weapon = template_ItemsFilter_weapon('')
 
    if len(attach_Lst) != 0:
        modifyChanges_NC(temp + ItemsFilter_weapon, attach_Lst, '', '')
        modifyChanges_ALT(template_CUSTOM_ItemsFilter_weapon,'')
    else:
        modifyChanges_NC(temp + ItemsFilter_weapon, template_CUSTOM_ItemsFilter_weapon, '', '')       
def CUSTOM_ItemsFilter_randombox():
    template_ItemsFilter_randombox = template_CUSTOM_ItemsFilter_randombox()
    modifyChanges_NC(temp + ItemsFilter_randombox, template_ItemsFilter_randombox, "box_", "_card")
def CUSTOM_ItemsFilter_cards():
    template_ItemsFilter_cards = template_CUSTOM_ItemsFilter_cards()
    modifyChanges_NC(temp + ItemsFilter_cards, template_ItemsFilter_cards,'', "_card")
#---------------------------------------------------------
def SKIN_ItemsFilter_skin():
    for skin in skinsDict:
        template_base = template_SKIN_ItemsFilter(skin)
        modifyChanges(temp + ItemsFilter_skins, template_base, skin, '+', '')
def SKIN_ItemsFilter_skin_SA():
    for skin in skinsDict:
        for attach in skinsDict[skin][1]:
            specialAttach_template = template_SKIN_ItemsFilter_skin_SA(attach)
            modifyChanges(temp + ItemsFilter_skins, specialAttach_template, attach, '+', '')
def SKIN_ItemsFilter_randombox():
    for skin in skinsDict:
        template_ItemsFilter_randombox = template_SKIN_ItemsFilter_randombox(skin)
        modifyChanges(temp + ItemsFilter_randombox, template_ItemsFilter_randombox, skin, "", "")
#---------------------------------------------------------
def GSET_ItemsFilter_gset():
    for part in gset_partList:
        PartName = part.split('_')[1]
        template_ItemsFilter = template_GSET_ItemsFilter_gset(part)
        modifyChanges(temp + f"\\Game\\Libs\\Config\\ItemsFilter_{PartName}.xml", template_ItemsFilter, part, '', "")
#---------------------------------------------------------
def FBS_ItemsFilter_fbs():
    template_ItemsFilter_fbs = template_FBS_ItemsFilter_fbs()
    modifyChanges(temp + ItemsFilter_fbs, template_ItemsFilter_fbs, var01, '', "")
def FBS_ItemsFilter_randombox():
    template_ItemsFilter_randombox = template_FBS_ItemsFilter_randombox()
    modifyChanges(temp + ItemsFilter_randombox, template_ItemsFilter_randombox, var01, '', "")
#---------------------------------------------------------
def CHARM_ItemFilter():
    for charm in charms_list:
        template_ItemFilter = template_CHARM_ItemFilter(charm)
        modifyChanges(temp + ItemsFilter_charm, template_ItemFilter, charm, '', '')
#---------------------------------------------------------
def ACHIEVE_ItemFilter():
    temp_ItemsFilter_special = temp + ItemsFilter_special
    for achieve in ach_list:
        template_special, skin = template_ACHIEVE_ItemFilter(achieve)
        modifyChanges(temp_ItemsFilter_special, template_special, skin, achieve, '')
#---------------------------------------------------------
def BUNDLE_ItemFilter():
    for bundle in bundleList:
        skin = bundle.split('_')[-1]
        template_bundle, template_bundle_console = template_BUNDLE_ItemFilter(bundle)
        modifyChanges(temp + ItemsFilter_randombox, template_bundle, skin, bundle, '')
        modifyChanges(temp + ItemsFilter_randombox, template_bundle_console, skin, bundle, '')

#---------------------------------------------------------
#                  --- ANIMATIONS ---
#---------------------------------------------------------
def Animation_cbaa():
    try:
        template_Animation_cba = f"""	\n<!-- //animation definitions for the {var01} (weapon type) -->
        <AnimationDefinition>
            <Model File="/../objects/weapons/{var01}/{var01}.chr"/>
            <Animation Path="1st_person/weapons/{var01}"/>
            <Database Path="1st_person/weapons/{var01}/{var01}.dba"/>
            <COMPRESSION value="0"/>
            <RotEpsilon value="0.000001"/>
            <PosEpsilon value="0.01"/>
        </AnimationDefinition>\n</Definitions>"""
        
        modifyChanges_NC(temp + Animations_cba, template_Animation_cba, '', "")
    except FileNotFoundError:
        print("FileNotFoundError ---- Animations_cba")
def Anim_handposes(handpose):
    try:
        temp_list = []
        temp_list.append('\n')
        file = open(temp + handpose).readlines()
        for line in file:
            if var01 in line:
                temp_list.append(line)
        temp_list.append("\t</handsPosesAnim>\n</handsPoses>")
        # -----------------------------        
        shutil.copyfile(master + handpose, temp + handpose)
        modifyChanges_NC(temp + handpose, temp_list, var01, '')
    except:
        pass
def Anim_chrparams(handpose):
    try:
        temp_list = []
        temp_list.append('\n')
        file = open(temp + handpose).readlines()
        for line in file:
            if "ik_aim_pose_" + var01 in line:
                temp_list.append(line)
        temp_list.append("\t</AnimationList>\n</Params>")
        # -----------------------------        
        shutil.copyfile(master + handpose, temp + handpose)
        remove_lastline(temp + handpose)
        modifyChanges_NC(temp + handpose, temp_list, var01, '')
    except:
        pass
#---------------------------------------------------------
#                     ---- UI ----
#---------------------------------------------------------
def NEW_UI_randomBoxesIcons():
    template_UI_randomBoxesIconss = template_NEW_UI_randomBoxesIcons()
    modifyChanges_NC(temp + UIrandomBoxesIcons, template_UI_randomBoxesIconss,'icons_randombox_', "")
def NEW_UI_challengesIcons():
    template_UI_challengesIconss = template_NEW_UI_challengesIcons()
    modifyChanges_NC(temp + UIchallengesIcons, template_UI_challengesIconss,'challenge_stripe_', "")
def NEW_UI_weaponsItemsIcons():
    template_UI_weaponsItemsIconss = template_NEW_UI_weaponsItemsIcons()
    modifyChanges_NC(temp + UIweaponsItemsIcons, template_UI_weaponsItemsIconss,'', "")
def NEW_UI_CombatLogIcons():
    template_UI_CombatLogIconss = template_NEW_UI_CombatLogIcons()
    modifyChanges_NC(temp + UICombatLogIcons, template_UI_CombatLogIconss,'CombatLogIcons_', "")
def NEW_UI_attachmentsItemsIcons():
    attach_Lst = template_NEW_UI_attachmentsItemsIcons()
    if len(attach_Lst) != 0:
        modifyChanges_NC(temp + UIattachmentsItemsIcons, attach_Lst, 'attachmentsItemsIcons_', '')
#---------------------------------------------------------
def CUSTOM_UI_cards():
    template_UI_cards = template_CUSTOM_UI_cards()
    modifyChanges_NC(temp + UIcards, template_UI_cards,'', "_progression")
def CUSTOM_UI_randomBoxesIcons():
    template_UI_randomBoxesIconss = template_CUSTOM_UI_randomBoxesIcons()
    modifyChanges_NC(temp + UIrandomBoxesIcons, template_UI_randomBoxesIconss,'icons_randombox_', "")
def CUSTOM_UI_challengesIcons():
    template_UI_challengesIconss = template_CUSTOM_UI_challengesIcons()
    modifyChanges_NC(temp + UIchallengesIcons, template_UI_challengesIconss,'challenge_stripe_', "")
def CUSTOM_UI_weaponsItemsIcons():
    template_UI_weaponsItemsIconss = template_CUSTOM_UI_weaponsItemsIcons()
    modifyChanges_NC(temp + UIweaponsItemsIcons, template_UI_weaponsItemsIconss,'', "")
def CUSTOM_UI_attachmentsItemsIcons():
    attach_Lst = template_CUSTOM_UI_attachmentsItemsIcons()
    if len(attach_Lst) != 0:
        modifyChanges_NC(temp + UIattachmentsItemsIcons, attach_Lst, 'attachmentsItemsIcons_', '')
def CUSTOM_UI_CombatLogIcons():
    template_UI_CombatLogIconss = template_CUSTOM_UI_CombatLogIcons()
    modifyChanges_NC(temp + UICombatLogIcons, template_UI_CombatLogIconss,'CombatLogIcons_', "")
#---------------------------------------------------------
def integrate_MasterServer():
    
    template_MasterServerr = f"""
    <progression name="{var01}_card" cards_required="1000" item="{var01}_shop"/>\n</card_progressions_config>"""

    modifyChanges_NC(temp + card_progressions_01, template_MasterServerr,'', "_card")
    modifyChanges_NC(temp + card_progressions_02, template_MasterServerr,'', "_card")
    modifyChanges_NC(temp + card_progressions_03, template_MasterServerr,'', "_card")
#---------------------------------------------------------
def SKIN_UI_randomBoxesIcons():
    for skin in skinsDict:
        template_UI_randomBoxesIconss = f"""\n\t<image name="icons_randombox_{skin}" file="Libs\Icons\RandomBoxes\Weapons\icons_randombox_{skin}.tif" pos="0,0" size="1024,512" />\n</images>"""
        modifyChanges(temp + UIrandomBoxesIcons, template_UI_randomBoxesIconss, skin, 'icons_randombox_', "")
def SKIN_UI_challengesIcons():
    for skin in skinsDict:
        template_UI_challengesIconss = f"""\n\t<image name="challenge_stripe_{skin}" file="Libs/Icons/Challenges/challenge_stripe_{skin}.tif" pos="0,0" size="1024,256"/>\n</images>"""
        modifyChanges(temp + UIchallengesIcons, template_UI_challengesIconss, skin, 'challenge_stripe_', "")
def SKIN_UI_weaponsItemsIcons():
    for skin in skinsDict:

        weapon_type = skin.split('_')[0]
        try:
            x_size, x_pose, y_pose = get_pos(weapon_type)
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

        modifyChanges(temp + UIweaponsItemsIcons, template_UI_weaponsItemsIconss, skin,'', "")
#---------------------------------------------------------
def GSET_assetsItemsIcons():
    gpart = gset_partList[0].split('_')[2]
    commiten = f"\n\t<!-- {gpart} -->\n</images>"
    modifyChanges(temp + assetsItemsIcons, commiten, gpart, '', "")
    
    for part in gset_partList:
        template_assetsItemsIcons = f"""\n\t<image name="{part}" file="Libs\Icons\\assets\{part.split('_')[2]}\\assets_{part}.tif" pos="0,0" size="200,200" />\n</images>"""
        modifyChanges(temp + assetsItemsIcons, template_assetsItemsIcons, part, '', "")
#---------------------------------------------------------
def FBS_assetsItemsIcons():
    template_assetsItemsIcons = template_FBS_assetsItemsIcons()
    modifyChanges(temp + assetsItemsIcons, template_assetsItemsIcons, var01, '', "")
def FBS_randomBoxesIcons():
    template_randomBoxesIconss = template_FBS_randomBoxesIcons()
    modifyChanges(temp + UIrandomBoxesIcons, template_randomBoxesIconss, var01, '', "")
#---------------------------------------------------------
def CHARM_Icons():
    for charm in charms_list:
        template_UI = template_CHARM_Icons(charm)
        modifyChanges(temp + UIcharm, template_UI, charm, '', '')
#---------------------------------------------------------
def ACHIEVE_Icons():
    for achieve in ach_list:
        template_UI_challengesIconss, skin = template_ACHIEVE_Icons(achieve)
        modifyChanges(temp + UIchallengesIcons, template_UI_challengesIconss, skin, achieve, "")
#---------------------------------------------------------
def BUNDLE_Icons():
    for bundle in bundleList:
        skin = bundle.split('_')[-1]
        template_UI_BundleIconss = template_BUNDLE_Icons(bundle)
        modifyChanges(temp + UIrandomBoxesIcons, template_UI_BundleIconss, skin, bundle, "")

#---------------------------------------------------------
#                    ----- OFFER -----
#---------------------------------------------------------
def NEW_catalog_offers_IGR():
    template_catalog_offers_IGR = template_NEW_catalog_offers_IGR()
    modifyChanges_NC(temp + catalog_offers_IGR, template_catalog_offers_IGR, '', '_shop')
def CUSTOM_catalog_offers_IGR():
    template_catalog_offers_IGR = template_CUSTOM_catalog_offers_IGR()
    modifyChanges_NC(temp + catalog_offers_IGR, template_catalog_offers_IGR, '', '_shop')
def SKIN_catalog_offers_IGR():
    for skin in skinsDict:
        template_catalog_offers_IGR = template_SKIN_catalog_offers_IGR(skin)
        modifyChanges(temp + catalog_offers_IGR, template_catalog_offers_IGR, skin, '', '')
def GSET_catalog_offers_IGR():
    gpart = gset_partList[0].split('_')[2]
    commiten = f"\n\t<!-- GearSet... {gpart} -->\n</offers>"
    modifyChanges(temp + catalog_offers_IGR, commiten, gpart, '', "... cny02 -->")
    
    root = ET.parse(temp + catalog_offers_IGR).getroot()
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

        modifyChanges(temp + catalog_offers_IGR, template_ItemsFilter_offer, part, '', "")
def FBS_catalog_offers_IGR():
    template_ItemsFilter_offer = template_FBS_catalog_offers_IGR()
    modifyChanges(temp + catalog_offers_IGR, template_ItemsFilter_offer, var01, '', "")
def CHARM_catalog_offers_IGR():

    root = ET.parse(temp + catalog_offers_IGR).getroot()
    temp_store = []
    for elem in root.findall('offer'):
        count_store_id = elem.attrib['store_id']
        temp_store.append(count_store_id)
    
    store_id = int(temp_store[-1])
    print(gSpace + "... catalog_offers_IGR")
    print(gSpace + "... last store_id = ", store_id)
    
    for charm in charms_list:
        num = charms_list.index(charm) + 1
        
        commiten = f"<!-- charm... {charm} -->"
        template_offer = f"""\n\t{commiten}\n\t<offer store_id="{store_id + num}" item_name="{charm}_shop" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="0" quantity="0" offer_status="NEW" game_money="0" cry_money="123" crown_money="0"/>\n</offers>"""

        modifyChanges(temp + catalog_offers_IGR, template_offer, charm, '', '')
def ACHIEVE_catalog_offers_IGR():
    
    commitAchieveMessage, _ = get_AchieveSkin(ach_list[0])
    commiten = f"\n\t<!-- Achievements... {commitAchieveMessage} -->\n</offers>"
    modifyChanges(temp + catalog_offers_IGR, commiten, commitAchieveMessage, '+', "")
                   
    root = ET.parse(temp + catalog_offers_IGR).getroot()
    temp_store = []
    for elem in root.findall('offer'):
        count_store_id = elem.attrib['store_id']
        temp_store.append(count_store_id)
    
    store_id = int(temp_store[-1])
    print(gSpace + "... catalog_offers_IGR")
    print(gSpace + "... last store_id = ", store_id)

    for achieve in ach_list:
        
        skin, ending = get_AchieveSkin(achieve)
        store_id = store_id + 1
        achieveType = achieve.split('_')[1]
        complexWord = "engineersoldiersnipermedic"
        
        if achieve.split(achieveType + "_")[1].split('_')[0] in complexWord:
            classWord = achieve.split(achieveType + "_")[1].split('_')[0] + "_"
        else:
            classWord = ''
        
        template_catalog_offers_IGR = f"""
    <offer store_id="{store_id}" item_name="unlock_{classWord}{skin}{ending}_{achieveType}" description="@{classWord}{skin}{ending}_{achieveType}_desc" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="123" crown_money="0"/>\n</offers>"""
        modifyChanges(temp + catalog_offers_IGR, template_catalog_offers_IGR, f"{classWord}{skin}{ending}_{achieveType}+", "+", '')
def BUNDLE_catalog_offers_IGR():
    
    commitAchieveMessage, _ = get_AchieveSkin(bundleList[0])
    commiten = f"\n\t<!-- BundleItem... {commitAchieveMessage} -->\n</offers>"
    modifyChanges(temp + catalog_offers_IGR, commiten, commitAchieveMessage, '+', "")
                   
    root = ET.parse(temp + catalog_offers_IGR).getroot()
    temp_store = []
    for elem in root.findall('offer'):
        count_store_id = elem.attrib['store_id']
        temp_store.append(count_store_id)
    
    store_id = int(temp_store[-1])
    print(gSpace + "... catalog_offers_IGR")
    print(gSpace + "... last store_id = ", store_id)

    for bundle in bundleList:
        store_id = store_id + 1
        
        template_catalog_offers_IGR = f"""
    <offer store_id="{store_id}" item_name="{bundle}" description="@{bundle}_description" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="123" crown_money="0"/>
    <offer store_id="{store_id+1}" item_name="{bundle}_console" description="@{bundle}_console_description" item_category_override="" limited="0" amount="0" expiration_time="" durability_points="0" repair_cost="" quantity="1" offer_status="NEW" game_money="0" cry_money="123" crown_money="0"/>\n</offers>"""
        modifyChanges(temp + catalog_offers_IGR, template_catalog_offers_IGR, f"{bundle}", "+", '')
#---------------------------------------------------------



#====================== INTEGRATION ======================
def intagrate_Animations():
    Animation_cbaa()
    Anim_handposes(handposes01)
    Anim_handposes(handposes02)
    Anim_chrparams(handposes_ch)
def Integrate_NEW():
    NEW_ItemRandomBox()
    NEW_Achievements()
    NEW_keyItems()
    NEW_box_token()
    NEW_bundle_smugglers()
    NEW_ItemsFilter_weapon()
    NEW_ItemFilter_weapon_GOLD()
    NEW_ItemsFilter_randombox()
    NEW_ItemsFilter_key()
    intagrate_Animations()
    NEW_UI_randomBoxesIcons()
    NEW_UI_challengesIcons()
    NEW_UI_weaponsItemsIcons()
    NEW_UI_CombatLogIcons()
    NEW_UI_attachmentsItemsIcons()
    NEW_catalog_offers_IGR()
def Integrate_CUSTOM():
    CUSTOM_ItemRandomBox()
    # CUSTOM_ItemRandomboxBoxCard()
    CUSTOM_ItemCard()
    CUSTOM_Achievements()
    CUSTOM_ItemsFilter_weapon()
    CUSTOM_ItemsFilter_randombox()
    CUSTOM_ItemsFilter_cards()
    intagrate_Animations()
    CUSTOM_UI_cards()
    CUSTOM_UI_randomBoxesIcons()
    CUSTOM_UI_challengesIcons()
    CUSTOM_UI_weaponsItemsIcons()
    CUSTOM_UI_attachmentsItemsIcons()
    CUSTOM_UI_CombatLogIcons()
    integrate_MasterServer()
    CUSTOM_catalog_offers_IGR()
def Integrate_SKIN():
    SKIN_ItemRandomBox()
    SKIN_Achievements()
    SKIN_ItemsFilter_skin()
    SKIN_ItemsFilter_skin_SA()
    SKIN_ItemsFilter_randombox()
    SKIN_UI_randomBoxesIcons()
    SKIN_UI_challengesIcons()
    SKIN_UI_weaponsItemsIcons()
    SKIN_catalog_offers_IGR()
def Integrate_GSET():
    GSET_ItemsFilter_gset()
    GSET_assetsItemsIcons()
    GSET_catalog_offers_IGR()
def Integrate_FBS():
    FBS_ShopItemsBox()
    FBS_ItemsFilter_fbs()
    FBS_ItemsFilter_randombox()
    FBS_assetsItemsIcons()
    FBS_randomBoxesIcons()
    FBS_catalog_offers_IGR()
def Integrate_CHARM():
    CHARM_ItemFilter()
    CHARM_Icons()
    CHARM_catalog_offers_IGR()
def Integrate_ACHIEVE():
    ACHIEVE_ShopItems()
    ACHIEVE_ItemFilter()
    ACHIEVE_Icons()
    ACHIEVE_catalog_offers_IGR()
def Integrate_BUNDLE():
    BUNDLE_ShopItems()
    BUNDLE_ItemFilter()
    # ACHIEVE_ItemFilter()
    BUNDLE_Icons()
    BUNDLE_catalog_offers_IGR()
def IntegrateContent():
    if key == "new":
        Integrate_NEW()
    if key == "custom":
        Integrate_CUSTOM()
    if key == "skin":
        Integrate_SKIN()
    if key == "gearset":
        Integrate_GSET()
    if key == "fbs":
        Integrate_FBS()
    if key == "charm":
        Integrate_CHARM()
    if key == "achieve":
        Integrate_ACHIEVE()
    if key == "bundle":
        Integrate_BUNDLE()
def Sheduler():

    check_and_create(temp + "\\Game\\Scripts\\Network\\")
    copyFile(temp + EntitySheduler, master + EntitySheduler)

    for item in ShedulerList:
        template = template_EntitySheduler(item)
        modifyChanges_NC(temp + EntitySheduler, template, item, '')
#---------------------------------------------------------
def main():
    FileStructure()
    IntegrateContent()
    if key == 'new' or key == "custom" or key == 'skin' or key == 'charm':
        Sheduler()
    input("""\n...Complete (press "Enter" to continue)""")
#---------------------------------------------------------
#                       --- GEAR ---
#---------------------------------------------------------
if __name__ == "__main__":
    while True:
        ProjPath = get_ProjPath()
        ShedulerList = []
        ach_list = []
        bundleList = []
        gset_partList = []
        GSetTemp_sss = []
        tempDict = {}
        skinsDict = {}
        charms_list = {}
        gSpace = "\t"
        key = get_Key()
        sss = """
        # #   #     #   # # # #   # # #    # # #    # # #        #      # # # #   # #    # # #    #     #       
         #    # #   #      #      #       #         #    #      # #        #       #    #     #   # #   # 
         #    #  #  #      #      # # #   #   # #   # # #      #   #       #       #    #     #   #  #  #     
         #    #   # #      #      #       #     #   #   #     # # # #      #       #    #     #   #   # #         
        # #   #     #      #      # # #    # # #    #    #   #       #     #      # #    # # #    #     #"""
        print(sss)
        master, temp, var01, var02 = AskPath(key)
        if key == 'fbs':
            if 'f_' in  var01.split('_fbs')[0]:
                SkinClass = var01.split('f_')[1].split('_')[0]
            else:
                SkinClass = var01.split('_')[0]
        if key == "charm":
            charms_list = get_Charms()
            for i in charms_list:
                ShedulerList.append(i)
        if key == "skin":
            defaultAttach, specialAttach = get_Skins()
            for i in defaultAttach:
                ShedulerList.append(i)
            for i in specialAttach:
                ShedulerList.append(i)

        # special
        keyItems = f"\\Game\\Items\\KeyItems\\key_box_{var01}.xml"
        bundle_smugglers = f"\\Game\\Items\\ShopItems\\bundle_smugglers_card_{var01}.xml"
        box_token = f"\\Game\\Items\\ShopItems\\box_token_cry_money_{var01}.xml"
        configAchievements = f"\\Game\\Libs\\Config\\Achievements\\{var01}_Kill.xml"
        configAchievements_GOLD = f"\\Game\\Libs\\Config\\Achievements\\{var01}_gold01_Kill.xml"
        ItemsFilter_weapon = f"\\Game\\Libs\\Config\\ItemsFilter_{var01.strip('0123456789')}.xml"
        ItemsCards = f"\\Game\\Items\\Cards\\{var01}_card.xml"
        AttachPath = "\\Game\\Objects\\Weapons\\" + var01
        ShopItemsBox = f"\\Game\\Items\\ShopItems\\box_{var01}.xml"
        ShopItemsBoxCard = f"\\Game\\Items\\ShopItems\\box_{var01}_card.xml"
        itemsSkins = f"\\Game\\Items\\Skins\\{var01}.xml"

        # common
        EntitySheduler = "\\Game\\Scripts\\Network\\EntityScheduler.xml"
        bundleItem = "\\Game\\Libs\\icons"
        Attachment_Charms = "\\Game\\Objects\\Attachments\\Charms"
        assetsItemsIcons = "\\Game\\Libs\\Config\\UI\\assetsItemsIcons.xml"
        achievements = "\\Game\\Libs\\Config\\Achievements\\"
        ItemsFilter_special = f"\\Game\\Libs\\Config\\ItemsFilter_special.xml"
        UIcards = "\\Game\\Libs\\Config\\UI\\cards.xml"
        ItemsFilter_cards = "\\Game\\Libs\\Config\\ItemsFilter_cards.xml"
        ItemsFilter_charm = "\\Game\\Libs\\Config\\ItemsFilter_charm.xml"
        UIcharm = "\\Game\\Libs\\Config\\UI\\charms\\icons_charms.xml"
        handposes_ch = "\\Game\\Objects\\Characters\\Human\\handsposes.chrparams" 
        handposes01 = "\\Game\\Objects\\Characters\\Human\\handsposes.xml"
        handposes02 = "\\Game\\Objects\\Characters\\Human\\handsposes_female.xml"
        ItemsFilter_key = "\\Game\\Libs\\Config\\ItemsFilter_keys.xml"
        ItemsFilter_skins = f"\\Game\\Libs\\Config\\ItemsFilter_skins.xml"
        ItemsFilter_randombox = "\\Game\\Libs\\Config\\ItemsFilter_randombox.xml"
        ItemsFilter_fbs = "\\Game\\Libs\\Config\\ItemsFilter_fbs.xml"
        Animations_cba = "\\Game\\Animations\\Animations.cba"
        UIweaponsItemsIcons = "\\Game\\Libs\\Config\\UI\\weaponsItemsIcons.xml"
        UIattachmentsItemsIcons = "\\Game\\Libs\\Config\\UI\\attachmentsItemsIcons.xml"
        UIrandomBoxesIcons = "\\Game\\Libs\\Config\\UI\\randomBoxesIcons.xml"
        UIchallengesIcons = "\\Game\\Libs\\Config\\UI\\challengesIcons.xml"
        UICombatLogIcons = "\\Game\\Libs\\Config\\UI\\CombatLogIcons.xml"
        card_progressions_01 = "\\Game\\Libs\\Config\\MasterServer\\card_progressions_config.xml"
        card_progressions_02 = "\\Game\\Libs\\Config\\MasterServer\\card_progressions_config.mycom.xml"
        card_progressions_03 = "\\Game\\Libs\\Config\\MasterServer\\card_progressions_config.russia.xml"
        catalog_offers_IGR = "\\Game\\Libs\\Config\\Shop\\catalog_offers_IGR.xml"
        
        main()