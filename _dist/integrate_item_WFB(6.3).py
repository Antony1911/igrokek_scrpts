import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from xml.parsers.expat import ParserCreate, ExpatError, errors
import shutil
import logging
import subprocess
from pathlib import Path
import fnmatch, re
import sys
import colorama
from colorama import init, Fore, Back, Style
import copy
import PySimpleGUI as sg


def resources_copy(src, dst, resources):
    for k in resources:
        dst_f = os.path.abspath(k.replace(src.replace('\\', '/'), os.path.join(dst.replace('\\', '/'), 'Game\\')))
        try:
            shutil.copyfile(k, dst_f)
        except IOError as io_err:
            os.makedirs(dst_f.replace(dst_f.split('\\')[-1],''))
            shutil.copyfile(k, dst_f)
        
    
def walkfolder(folder, filetype):
    temp_list = []
    for root, dirs, files in os.walk(folder):
        for name in files:
            fullpath = os.path.join(root, name).replace('\\', '/')
            if filetype != '':
                if fullpath.endswith(filetype):
                    temp_list.append(fullpath)
            else:
                temp_list.append(fullpath)
    return temp_list


def splitTifFiles(icon_tif,repo):
    files_to_record = []
    if icon_tif.replace('\\', '/').split('/')[-2].lower() != 'full':
        splitter = subprocess.Popen(
            ['python', os.path.join(repo, r'MRGTools/make_mini_images.py'), '--config', '1024_512_256_128_64',
            icon_tif])    
        streamdata = splitter.communicate()[0]
        splitter.wait()
        for mips in mip_list:
            try:
                if (icon_tif.replace('\\', '/').split('/')[-1].lower().startswith('wardens_fbs') or
                    icon_tif.replace('\\', '/').split('/')[-1].lower().startswith('reapers_fbs')):
                    icon_tif_mip = icon_tif.replace(mips.replace('_shop', ''),'').replace('.tif', mips.replace('_shop', '') + '.tif')
                elif (icon_tif.replace('\\', '/').split('/')[-1].lower().startswith('armor_')):
                    icon_tif_mip = icon_tif.replace(mips.replace('_shop', ''),'').replace('.tif', mips.replace('_shop', '') + '.tif')
                elif icon_tif.replace('\\', '/').split('/')[-1].lower().startswith('victorypose'):
                    icon_tif_mip = (icon_tif.replace('.tif','') + mips).replace('_shop','') + '.tif'
                else:
                    icon_tif_mip = icon_tif.replace('_shop', mips)
                ddser = subprocess.Popen(
                        ['python', os.path.join(repo, r'MRGTools/tiff_preset_tool.py'), '--preset',
                        '//M=50,50,50,50,50,50 /preset=UserInterface_Compressed_nomips', '--make-dds',
                        icon_tif_mip])
                ddser.wait()      
                print(Fore.GREEN + icon_tif_mip.replace('\\', '/') + ' Has been generated' + Fore.WHITE)
                print(Fore.GREEN + icon_tif_mip.replace('.tif', '.dds').replace('\\', '/') + ' Has been generated' + Fore.WHITE)
            except:
                print(Fore.RED+ 'Somethong went wrong with icon-splitter or default icon'+ Fore.WHITE)
    else:
        splitter = subprocess.Popen(
        ['python', os.path.join(repo, r'MRGTools/make_mini_images.py'), '--config', '1024_512',
        icon_tif])    
        streamdata = splitter.communicate()[0]
        splitter.wait()
        try:
            icon_tif_mip = icon_tif.replace('full', 'full_mip512')
            ddser = subprocess.Popen(
                    ['python', os.path.join(repo, r'MRGTools/tiff_preset_tool.py'), '--preset',
                    '//M=50,50,50,50,50,50 /preset=UserInterface_Compressed_nomips', '--make-dds',
                    icon_tif_mip])
            ddser.wait()      
            print(Fore.GREEN + icon_tif_mip.replace('\\', '/') + ' Has been generated' + Fore.WHITE)
            print(Fore.GREEN + icon_tif_mip.replace('.tif', '.dds').replace('\\', '/') + ' Has been generated' + Fore.WHITE)
        except:
            print(Fore.RED+ 'Somethong went wrong with icon-splitter or default icon'+ Fore.WHITE)
    
       
def pretty_print(element, indent=None):
    if indent is None:
        indent = "    "
    original = ET.tostring(element, 'utf8')
    reparsed = minidom.parseString(original)
    indented = reparsed.toprettyxml(indent=indent, newl='\n')
    return '\n'.join([s for s in indented.splitlines() if s.strip()])


def integration_function(repo):
        ss = 'Select your item type: \n 1 - New weapon\n 2 - New weapon skin\n 3 - New knife\n 4 - New knife skin\n 5 - New equipment\n 6 - New FBS\n 7 - New victory animation'
        print (ss)
        item_type = int(sg.popup_get_text(ss),base=10)
        
        if item_type == 1:
            integrate_new_weapon(repo)
        elif item_type == 2:
            integrate_new_weapon_skin(repo)
        elif item_type == 3:
            def knife_name():
                print('insert your knife name')
                knife_name = input()+'_shop'
                check_name = knife_name.isascii()
                if not check_name:
                    print('insert your knife name correct')
                    knife_name()
                else:
                    icons_prefix = ['.tif', '_mip64.tif', '_mip128.tif', '_mip256.tif', '_mip512.tif' ]
                    icon_tif = os.path.join(repo, 'Game\\Libs\\Icons\\weapons\\Knives\\weapons_' + knife_name + icons_prefix[0]) 
                    splitTifFiles(icon_tif, repo) 
                    integrate_new_knife(repo, knife_name,icons_prefix)
            knife_name()
        elif item_type == 4:
            integrate_new_knife_skin(repo)
        elif item_type == 5:
            integrate_new_equipment(repo)
        elif item_type == 6:
            integrate_new_fbs(repo)
        elif item_type == 7:
            victory_animation(repo)
        else:
            print('your item type is wrong! Please insert the correct item type!')
            integration_function()


def another_item_to_integrate(repo):
    print ("------------------------Do you have another item to intgrate?---------------------y-yes, n-no---------------")
    another = sg.popup_get_text("Do you have another item to intgrate?  y/n")
    if another == 'y':
        integration_function(repo)
    else:
        sys.exit()


def integrate_new_weapon(repo):
    print('insert your weapon type')


def integrate_new_weapon_skin(repo):
    proc = subprocess.Popen([os.path.join(repo, 'integrate_weapon_skin.exe')])
    print(proc.communicate()[0])
    proc.wait()
    another_item_to_integrate(repo)


def integrate_new_knife(repo, knife_name,icons_prefix):   
        def modify_weaponitemsIcons():
            icons = []
            weaponitemsIconsFile = os.path.join(repo, 'Game\\Libs\\Config\\UI\\weaponsItemsIcons.xml')
            weaponitemsIcons = ET.parse(weaponitemsIconsFile)
            for icon_prefix in icons_prefix:
                icon = os.path.join(repo, 'Game\\Libs\\Icons\\weapons\\Knives\\weapons_' + knife_name + icon_prefix)    
                icons.append(icon) 
            for icon in icons:
                if not os.path.isfile(icon):
                    print('please! Check your knife icons!' + icon)
            for icon_prefix in icons_prefix:
                for child in weaponitemsIcons.getroot():
                    if re.match((knife_name + icon_prefix).replace('_shop',''), child.attrib.get('name')):
                        weaponitemsIcons.getroot().remove(child)
                        #------In this block we clear the old tryes to modify file
            for icon_prefix in icons_prefix:
                size = (icon_prefix.replace('_mip','').replace('.tif',''))
                if icon_prefix == '.tif':
                    size = '1024'
                image = ET.SubElement(weaponitemsIcons.getroot(), 'image', name=(knife_name + icon_prefix).replace('_shop','').replace('.tif',''),
                file='Libs\\Icons\\weapons\\Knives\\weapons_' + 
                knife_name + icon_prefix, pos="0,0", size=(size + ',' + size))
                with open(weaponitemsIconsFile, 'w') as f:
                    f.write(pretty_print(weaponitemsIcons.getroot()))
            print('weaponsItemsIcons has been modifyed')     
        modify_weaponitemsIcons()
        def modify_combatlogicons():
            print('what position of your combatlog icon? See the Game\\Libs\\Icons\\CombatLog\\CombatLogIcons_kn.tif')
            pos = sg.popup_get_text('what position of your combatlog icon? See the Game\\Libs\\Icons\\CombatLog\\CombatLogIcons_kn.tif')
            checkPos = re.match('[0-9],[0-9]', pos)
            if checkPos:
                CombatlogIconsFile = os.path.join(repo, 'Game\\Libs\\Config\\UI\\CombatlogIcons.xml')
                CombatlogIcons = ET.parse(CombatlogIconsFile)
                Combatlog = knife_name.replace('_shop','') + '_combatLog'
                root = CombatlogIcons.getroot()
                ElementsToChange = root.findall('image_set')
                for Elements in ElementsToChange:
                    if Elements.attrib['file']=="Libs\\Icons\\CombatLog\\CombatLogIcons_kn.tif":
                        Check_rows = Elements.findall('image')
                        for Check_row in Check_rows:
                            if re.match(Combatlog, Check_row.attrib.get('name')):
                                Elements.remove(Check_row)
                        Image_set=ET.SubElement(Elements,'image', name=Combatlog, pos=pos )
                with open(CombatlogIconsFile, 'w') as f:
                    f.write(pretty_print(CombatlogIcons.getroot()))
                    print('CombatlogIcons has been modifyed')     
            elif re.match(' ', pos):
                pass
            else:
                print('Please, isert the corect position')
                modify_combatlogicons()
        modify_combatlogicons()
        def modify_appearance():
            Appierence_file = os.path.join(repo, 'Game\\Libs\\Config\\Shop\\appearance.xml')
            Appierence = ET.parse(Appierence_file)
            offer = knife_name.replace('_shop','')
            root = Appierence.getroot()
            ElementsToChange = root.findall('category')
            for Element in ElementsToChange:  
                if Element.attrib['name']=="melee":
                    Check_rows = Element.findall('offer')
                    for Check_row in Check_rows:
                        if re.match(offer, Check_row.attrib.get('name')):
                            Element.remove(Check_row)
                    appierence_set=ET.SubElement(Element,'offer', name=offer)
            with open(Appierence_file, 'w') as f:
                f.write(pretty_print(root))
                print('Appierence has been modifyed')     
        modify_appearance()
        def modify_ItemsFilter_kn():
            ItemsFilterFile = os.path.join(repo, 'Game\\Libs\\Config\\ItemsFilter_kn.xml')
            ItemsFilter = ET.parse(ItemsFilterFile)
            item = knife_name.replace('_shop','')
            root = ItemsFilter.getroot()
            for Element in root:
                if re.match(item, Element.attrib.get('name')):
                    root.remove(Element)
            NewItem = ET.SubElement(root,'Item', name=item)
            print('What is the knife fraction?: 1 - Wardens, 2 - Reapers, 3 - Both')
            def fraction_choise():
                fraction = int(sg.popup_get_text('What is the knife fraction?: 1 - Wardens, 2 - Reapers, 3 - Both'))
                if fraction == 3:
                    ET.SubElement(NewItem, 'Reaper', level='1')
                    ET.SubElement(NewItem, 'Warden', level='1')
                elif fraction == 2:
                    ET.SubElement(NewItem, 'Reaper', level='1')
                    ET.SubElement(NewItem, 'Warden')
                elif fraction == 1:
                    ET.SubElement(NewItem, 'Reaper')
                    ET.SubElement(NewItem, 'Warden', level='1')
                else:
                    print("Please! Choose the correct fraction")
                    sg.popup_notify("Please! Choose the correct fraction")
                    fraction_choise()
            fraction_choise()
            with open(ItemsFilterFile, 'w') as f:
                f.write(pretty_print(root))
            print('ItemsFilter_kn has been modifyed')    
        modify_ItemsFilter_kn()
        def modify_Text_weapons():
            print('Please, enter your knife game name:')
            game_name = sg.popup_get_text('Please, enter your knife game name:')
            check_name = game_name.isascii()
            if not check_name:
                print('insert your knife game_name correct')
                sg.popup_notify('insert your knife game_name correct')
                modify_Text_weapons()
            text_weaponsFile = os.path.join(repo, 'Game\\Languages\\Console\\text_weapons.xml')
            tex_weapons = ET.parse(text_weaponsFile)
            root = tex_weapons.getroot()
            ElementsToChange = root.findall('entry')
            for Element in ElementsToChange:
                if Element.attrib['key']==knife_name + '_name':
                    root.remove(Element)
            New_entry = ET.SubElement(root,'entry', key=knife_name + '_name')
            ET.SubElement(New_entry, 'original', value=game_name)
            ET.SubElement(New_entry, 'translation', value="")
            with open(text_weaponsFile, 'w') as f:
                f.write(pretty_print(root))
                print('text_weapons has been modifyed') 
        modify_Text_weapons()
        def modify_EntityScheduler():
            EntitySchedulerFile = os.path.join(repo, 'Game\\Scripts\\Network\\EntityScheduler.xml')
            EntitySheduler = ET.parse(EntitySchedulerFile)
            root = EntitySheduler.getroot()
            item = knife_name.replace('_shop','')
            for Element in root.findall('Class'):
                if re.match(item, Element.attrib.get('name')):
                    root.remove(Element)
            NewItem = ET.SubElement(root,'Class', name=item, policy="gun")
            root[:] = sorted(root, key=lambda child:(child.tag, child.get('policy'), child.get('name')))
            with open(EntitySchedulerFile, 'w') as f:
                f.write(pretty_print(root))
            print('EntitySchedulerFile has been modifyed')
        modify_EntityScheduler()
        another_item_to_integrate(repo)


def integrate_new_knife_skin(repo):
    proc = subprocess.Popen([os.path.join(repo, 'integrate_weapon_skin.exe')]) 
    print(proc.communicate()[0])
    proc.wait()
    another_item_to_integrate(repo)


def integrate_new_equipment(repo):
    ss = "insert your path to Game folder with equpment folder\n" + "sample: e:\WorkFlow\Warface\3D\WFB\WFB_Season_03\43_Season_03_Helmet_Pack_Integration_Wardens_Reapers_x2\Game"
    equip_path = os.path.abspath(sg.popup_get_folder(ss))
    def check_files_and_icons():
        print(Fore.BLUE + '------------------Checking files------------------------------')
        reaper_structure = os.path.join(equip_path,'Objects\Characters\\reapers')
        warden_structure = os.path.join(equip_path,'Objects\Characters\\wardens')
        structure_list = [reaper_structure, warden_structure]
        armor_list = ['hands', 'helmets', 'vests']
        ext_list = ['.chr', '.xml', '.mtl']
        armor_by_sides_list = []
        common_arrays = []
        common_array = []
        common_array_xml = []
        common_array_mtl =[]
        common_array_fp = []
        common_array_chr = []
        mtl_files = walkfolder(equip_path, '.mtl')
        def check_structure():
            if os.path.exists(element):
                print(Fore.GREEN + element.split('\\')[-1] + ' structure exists' + Fore.WHITE)
                for armor in armor_list:
                    if os.path.exists(os.path.join(element, armor)):
                        print(Fore.YELLOW + element.split('\\')[-1] + ' ' + armor + ' found' + Fore.WHITE)
                        armor_by_sides_list.append(element.split('\\')[-1] + ' ' + armor)
        for element in structure_list:
            check_structure()


        def file_arrays():
            for element in armor_list:
                if (armor_by_side.startswith('reaper') and armor_by_side.endswith(element)):
                    for ext in ext_list:
                        r_armor_array = walkfolder(os.path.join(reaper_structure, element), ext)
                        common_arrays.append(r_armor_array)
                if (armor_by_side.startswith('wardens') and armor_by_side.endswith(element)):
                    for ext in ext_list:
                        w_armor_array = walkfolder(os.path.join(warden_structure, element), ext)
                        common_arrays.append(w_armor_array)
        for armor_by_side in armor_by_sides_list:
            file_arrays()

        for Items in common_arrays:
            for item in Items:
                item = item.split('/')[-1]
                common_array.append(item)
        for item in common_array:
            if item.endswith('.chr'):
                common_array_chr.append(item)
            elif item.endswith('.xml'):
                common_array_xml.append(item)
            elif item.endswith('.mtl'):
                common_array_mtl.append(item)
            elif (item.endswith('fp.chr') or item.endswith('fp.xml') or item.endswith('fp.mtl')):
                common_array_fp.append(item)
        icon_tifs = walkfolder(os.path.join(equip_path, 'Libs\Icons\Armor'), '.tif')
        icons_dds = walkfolder(os.path.join(equip_path, 'Libs\Icons\Armor'), '.dds')
        icons = []
        icons_chr_list = []
        for icon_tif in icon_tifs:
            for mip in mip_list:
                if not icon_tif.endswith(mip.replace('_shop','') + '.tif'):
                    icons_chr_list.append(icon_tif.replace('.tif','').split('/')[-1])
            icons.append(icon_tif.replace('.tif','').split('/')[-1])
        print(Fore.BLUE + "------------------Renaming icons------------------------------" + Fore.WHITE)
        for icon_tif in icon_tifs:
            try:
                os.rename(icon_tif, icon_tif.replace('armor_',''))
            except:
                continue
            icon_tif = icon_tif.replace('armor_','')
            try:
                os.rename(icon_tif, icon_tif.replace(icon_tif.split('/')[-1],'armor_' + icon_tif.split('/')[-1]))
            except:
                continue


        def check_icons():  
            succes = True    
            for icon in icons:
                icon_compare = False
                icon_chr = False
                dds_compare = False
                for icon_dds in icons_dds:
                    if icon_dds.replace('.dds','').split('/')[-1] == icon:
                        icon_compare = True
                if icon_compare == False:
                    print(Fore.RED + 'Pare dds - tif missed ' + icon_dds + Fore.WHITE)
                    succes = False
            for i in icons_chr_list:
                for wear in common_array_chr:
                    if i.endswith(wear.replace('.chr','')):
                        icon_chr = True
                if icon_chr == False:
                    print(Fore.RED + "can't find chr-icon pare for " + wear + Fore.WHITE)
                    succes = False
            if succes == True:
                print(Fore.GREEN + "------------------Icons has been checked and renamed succesfully------------------------------" + Fore.WHITE)
            for icon_dds in icons_dds:
                try:
                    os.rename(icon_dds, icon_dds.replace('armor_',''))
                except:
                    continue
                icon_dds = icon_dds.replace('armor_','')
                try:
                    os.rename(icon_dds, icon_dds.replace(icon_dds.split('/')[-1],'armor_' + icon_dds.split('/')[-1]))
                except:
                    continue
        check_icons()
        icon_tifs = walkfolder(os.path.join(equip_path, 'Libs\Icons\Armor'), '.tif')
        icons_dds = walkfolder(os.path.join(equip_path, 'Libs\Icons\Armor'), '.dds')
        print(Fore.YELLOW + 'Do you need mips?           y/n      ' + Fore.WHITE)
        need_mips = sg.popup_yes_no('Do you need mips?  y/n')
        if (need_mips != 'yes' and need_mips != 'no'):
            print(Fore.RED + 'I can not understand! Repeat, please!')
            check_icons()
        elif need_mips == 'y':
            for icon_tif in icon_tifs:
                splitTifFiles(icon_tif, repo)
        elif need_mips == 'n':
            print(Fore.GREEN + "Ok! I will continue!")
        def check_xml_chr():
            succes = True
            for element in common_array_chr:
                chr_xml_compare = False
                for item in common_array_xml:
                    if element.replace('.chr','') == item.replace('.xml',''):
                        chr_xml_compare = True
                if chr_xml_compare == False:
                    print(Fore.RED + "can't find chr-xml pare for " + element + Fore.WHITE)
                    succes = False
            for element in common_array_xml:
                chr_xml_compare = False
                for item in common_array_chr:
                    if element.replace('.xml','') == item.replace('.chr',''):
                        chr_xml_compare = True
                if chr_xml_compare == False:
                    print(Fore.RED + "can't find chr-xml pare for " + element + Fore.WHITE)
            if succes == True:
                print(Fore.GREEN + "-------------------xml and chr has been checked succesfully---------------------" + Fore.WHITE)
        check_xml_chr()
        def check_chr_mtl():
            succes = True
            for element in common_array_chr:
                chr_mtl_compare = False
                for item in common_array_mtl:
                    if element.replace('.chr','') == item.replace('.mtl',''):
                        chr_mtl_compare = True
                if chr_mtl_compare == False:
                    print(Fore.RED + "can't find chr-mtl pare for " + element + Fore.WHITE)
                    succes = False
            for element in common_array_mtl:
                chr_mtl_compare = False
                for item in common_array_chr:
                    if element.replace('.mtl','') == item.replace('.chr',''):
                        chr_mtl_compare = True
                if chr_mtl_compare == False:
                    print(Fore.RED + "can't find chr-mtl pare for " + element + Fore.WHITE)
                    succes = False
            if succes == True:
                print(Fore.GREEN + "-------------------mtl and chr has been checked succesfully---------------------" + Fore.WHITE)    
        check_chr_mtl()
        def check_textures():
            success = True
            print (Fore.BLUE + "-------------------------------Checking existing textures------------------------" + Fore.WHITE)
            for elems in mtl_files:
                reading = open(elems, 'r').readlines()
                for strings in reading:
                    if 'Texture Map=' in strings:
                        clear_strings = equip_path + '/' + strings.split('File="')[1].split('"')[0]
                        if (os.path.isfile(clear_strings) and os.path.isfile(clear_strings.replace('.tif','.dds'))):
                                # print 'Warning!!! Contain original NormalMap. Contact with LeadArt, is it ok?\n', elems, clear_strings
                                continue
                        elif os.path.isfile(clear_strings):
                            success = False
                            print (Fore.RED + "Warning. DDS file is empty, but TIF is exist:", equip_path + '/' + 'Game' + \
                                                                                    clear_strings.split('Game')[1].replace(
                                                                                        '.tif', '.dds') + Fore.WHITE)
                        elif os.path.isfile(clear_strings.replace('.tif', '.dds')):
                            success = False
                            print (Fore.RED + "Warning. TIF file is empty, but DDS is exist:", equip_path + '/' + 'Game' + \
                                                                                    clear_strings.split('Game')[1].replace(
                                                                                        '.tif', '.dds') + Fore.WHITE)
                        else:
                            print(Fore.RED + "ERROR! File: " + elems + ' Empty files ' + clear_strings + Fore.WHITE + '\n')  # print "ERROR! Empty files", clear_strings
                            success = False
            if success == True:
                print(Fore.GREEN + "-------------------textures from .mtl has been checked succesfully---------------------" + Fore.WHITE)
        check_textures()
        def copy_files():
            print(Fore.YELLOW + '------------------Should I copy resources to repository?------------y/n?----------------' + Fore.WHITE)
            ready_to_copy = sg.popup_yes_no("Should I copy resources to repository?")
            if (ready_to_copy != 'yes' and ready_to_copy != 'no'):
                print(Fore.RED + 'I can not understand, repeat, please!' + Fore.WHITE)
                copy_files()
            elif ready_to_copy == 'yes': 
                items = ['.tif','.dds','.chr', '.xml', '.mtl']
                print(Fore.BLUE + '------------------Copying files to repository------------------------------' + Fore.WHITE)
                for item in items:
                    try:
                        resources_copy(equip_path, repo, (walkfolder(equip_path, item)))
                        print(Fore.GREEN + '------------------Structure copied for ' + item + '------------------------------' + Fore.WHITE)
                    except:
                        print(Fore.RED + '------------------Can not copy, check your file structure------------------------------' + Fore.WHITE)
            elif ready_to_copy == 'n':
                print(Fore.YELLOW + '------------------Should I continue integration?------------y/n?----------------' + Fore.WHITE)
                continue_to_integrate = input()
                if (continue_to_integrate != 'y' and continue_to_integrate != 'n'):
                    print(Fore.RED + 'I can not understand, repeat, please!' + Fore.WHITE)
                    copy_files()
                elif continue_to_integrate == 'n':
                    print(Fore.YELLOW + 'Ok! See you!' + Fore.WHITE)
                    sys.exit()
                elif ready_to_copy == 'y': 
                    print(Fore.YELLOW + 'Ok! Continue!' + Fore.WHITE)
        copy_files()
        return armor_list, common_array_chr, icon_tifs
    print(Fore.BLUE + '------------------Icons and resources has been checked------------------------------' + Fore.WHITE)
    icons_and_chr = check_files_and_icons()
    common_array_chr = icons_and_chr[1]
    icon_tifs = icons_and_chr[2]
    def integrate_equip():
        def generate_xml():
            print(Fore.BLUE + '------------------generating xml-files in Game/Items/Armor------------------------------' + Fore.WHITE)
            for element in common_array_chr:
                def set_rarity_marker_since_exclusive():
                    print(Fore.YELLOW + '(y/n) Do you want to set attribs ' + element.replace('.chr','') +'------------------------------ '+ Fore.WHITE)
                    set_attribs = input()
                    if (set_attribs != 'y' and set_attribs != 'n'):
                            print(Fore.RED + "I can not understand! Repeat, please" + Fore.WHITE)
                            set_rarity_marker_since_exclusive()
                    if set_attribs == 'y':
                        print(Fore.YELLOW + "Insert rarity: \n1-common\n 2-uncommon\n 3-rare\n 4-epic\n 5-legendary\n" + Fore.WHITE)
                        rarity = input()
                        if rarity == '1':
                            rarity_choise = 'common'
                        elif rarity == '2':
                            rarity_choise = 'uncommon'
                        elif rarity == '3':
                            rarity_choise = 'rare'
                        elif rarity == '4':
                            rarity_choise = 'epic'
                        elif rarity == '5':
                            rarity_choise = 'legendary'
                        elif rarity != ('1' or '2' or '3' or '4' or '5'):
                            print(Fore.RED + "I can not understand! Repeat, please" + Fore.WHITE)
                        else:
                            rarity = 'common'
                        print(Fore.YELLOW + '(y/n) This item is exclusive ' + element.replace('.chr','') + '------------------------------' + Fore.WHITE)
                        set_exclisive = input()
                        if (set_exclisive != 'y' and set_exclisive != 'n'):
                            print(Fore.RED + "I can not understand! Repeat, please" + Fore.WHITE)
                            set_rarity_marker_since_exclusive()   
                        print(Fore.YELLOW + '(y/n) Do you want to set marker for ' + element.replace('.chr','')+ '------------------------------' + Fore.WHITE)
                        set_marker = input()
                        if (set_marker != 'y' and set_marker != 'n'):
                            print(Fore.RED + "I can not understand! Repeat, please" + Fore.WHITE)
                            set_rarity_marker_since_exclusive()
                        if set_marker == 'y':
                            print(Fore.YELLOW + "Insert your marker" + Fore.WHITE)
                            marker = input()
                        else:
                            marker = None  
                        print(Fore.YELLOW + '(y/n) Do you want to set since for ' + element.replace('.chr','')+ '------------------------------' + Fore.WHITE)
                        set_since = input()
                        if (set_since != 'y' and set_since != 'n'):
                            print(Fore.RED + "I can not understand! Repeat, please" + Fore.WHITE)
                            set_rarity_marker_since_exclusive()
                        if set_since == 'y':
                            print(Fore.YELLOW + "Insert your marker"+ '------------------------------' + Fore.WHITE)
                            since = input()
                        else:
                            since = None
                    else:
                        print (Fore.GREEN + 'Ok! Continue!')  
                        rarity_choise = None 
                        set_exclisive = None 
                        marker = None 
                        since = None 
                    return rarity_choise, set_exclisive, marker, since                     
                attributes = set_rarity_marker_since_exclusive()
                if not element.endswith('_fp.chr'):
                    print(element)
                    new_element = os.path.join(repo,'Game\Items\Armor\\', element.replace('.chr','.xml'))
                    if os.path.isfile(new_element):
                            os.remove(new_element)
                    if element.startswith('wardens_hands'):
                        pattern = os.path.join(repo,'Game\Items\Armor\\','wardens_hands_01.xml')
                        
                    elif element.startswith('wardens_helmet'):
                        pattern = os.path.join(repo,'Game\Items\Armor\\','wardens_helmet_01.xml')
                        
                    elif element.startswith('wardens_vest'):
                        pattern = os.path.join(repo,'Game\Items\Armor\\','wardens_vest_01.xml')
                        
                    elif element.startswith('reapers_hands'):
                        pattern = os.path.join(repo,'Game\Items\Armor\\','reapers_hands_01.xml')
                        
                    elif element.startswith('reapers_helmet'):
                        pattern = os.path.join(repo,'Game\Items\Armor\\','reapers_helmet_01.xml')
                        
                    elif element.startswith('reapers_vest'):
                        pattern = os.path.join(repo,'Game\Items\Armor\\','reapers_vest_01.xml')
                
                    shutil.copyfile(pattern, new_element)
                    root = ET.parse(new_element).getroot()
                    root.attrib['name'] = element.replace('.chr','')
                    for child in root.find('slots').find('slot').find('assets').findall('asset'):
                        if child.attrib['mode'] == "tp":
                            child.attrib['name'] = element.replace('.chr','')
                        elif child.attrib['mode'] == "fp":
                            child.attrib['name'] = element.replace('.chr','') + '_fp'
                    for child in root.find('mmo_stats'):
                        if child.attrib['name'] == "shopcontent":
                            child.attrib['value'] = '1'
                    for child in root.find('UI_stats'):
                        if child.attrib['name'] == 'name':
                            child.attrib['value'] = "@ui_armor_"+ element.replace('.chr','') + "_name"
                        if child.attrib['name'] == 'description':
                            child.attrib['value'] = "@ui_armor_"+ element.replace('.chr','') + "_desc"
                        if child.attrib['name'] == 'icon':
                            child.attrib['value'] = "armor_"+ element.replace('.chr','')
                        if child.attrib['name'] == 'rarity' and not (attributes[0] is None):
                            child.attrib['value'] = attributes[0]
                    if attributes[1] == 'y':
                        exclusive = ET.SubElement(root.find('UI_stats'), 'param', name="exclusive", value="1" )
                    if not (attributes[2] is None):
                        marker = ET.SubElement(root.find('UI_stats'), 'param', name="marker", value=attributes[2])
                    if not (attributes[3] is None):
                        marker = ET.SubElement(root.find('UI_stats'), 'param', name="since", value=attributes[3])
                    with open(new_element, 'w') as f:
                        f.write(pretty_print(root))             
        generate_xml()
        def append_xml():
            text_armors_file = os.path.join(repo, 'Game/Languages/Console/text_armors.xml')
            items_filter_helmet_file = os.path.join(repo, 'Game/Libs/Config/ItemsFilter_helmet.xml')
            items_filter_vest_file = os.path.join(repo, 'Game/Libs/Config/ItemsFilter_vest.xml')
            items_filter_hands_file = os.path.join(repo, 'Game/Libs/Config/ItemsFilter_hands.xml')
            appearance_file = os.path.join(repo, 'Game/Libs/Config/Shop/appearance.xml')
            armor_items_icons_file = os.path.join(repo, 'Game/Libs/Config/UI/armorItemsIcons.xml')
            xmls = [text_armors_file, 
                    items_filter_hands_file,
                    items_filter_helmet_file,
                    items_filter_vest_file,
                    appearance_file,
                    armor_items_icons_file]
            def modify_xml():
                for xml in xmls:
                    root = ET.parse(xml).getroot()
                    for element in common_array_chr:
                        if not element.endswith('_fp.chr'):
                            if xml == text_armors_file:
                                for child in root.findall('entry'):
                                    if (child.attrib['key'].endswith(element.replace('.chr', '_name')) or
                                    child.attrib['key'].endswith(element.replace('.chr', '_desc'))):
                                        root.remove(child)
                                for child in root.findall('entry'):
                                    if child.attrib['key'] == "ui_armor_shared_jacket_01_name":
                                        new_entry_name = copy.deepcopy(child)
                                        new_entry_name.attrib['key'] = 'ui_armor_'+ element.replace('_body','').replace('.chr', '_name')
                                        root.append(new_entry_name)
                                for child in root.findall('entry'):
                                    if child.attrib['key'] == "ui_armor_shared_jacket_01_name":
                                        new_entry_desc = copy.deepcopy(child)    
                                        new_entry_desc.attrib['key'] = 'ui_armor_'+ element.replace('_body','').replace('.chr', '_desc')
                                        root.append(new_entry_desc)
                            elif xml == appearance_file:
                                for category in root.findall('category'):
                                    if category.attrib['name'] == "bodyParts":
                                        for child in category.findall('category'):
                                            if child.attrib['name'].startswith(element.split('_')[1].replace('hands','gloves')):
                                                for i in child.findall('offer'):
                                                    if i.attrib['name'] == element.replace('.chr',''):
                                                        child.remove(i)
                                                new_offer = ET.SubElement(child, 'offer', name = element.replace('.chr',''))
                            elif xml == items_filter_hands_file:
                                if element.split('_')[1] == 'hands':
                                    for child in root.findall('Item'):
                                        if child.attrib['name'] == element.replace('.chr', ''):
                                            root.remove(child)
                                        if (element.startswith('wardens') and child.attrib['name'] == 'wardens_arms_01'):
                                            new_hands = copy.deepcopy(child)
                                        elif (element.startswith('reapers') and child.attrib['name'] == 'reapers_arms_01'):
                                            new_hands = copy.deepcopy(child)
                                    new_hands.attrib['name'] = element.replace('.chr','')
                                    root.append(new_hands)
                            elif xml == items_filter_vest_file:
                                if element.split('_')[1] == 'vest':
                                    for child in root.findall('Item'):
                                        if child.attrib['name'] == element.replace('.chr', ''):
                                            root.remove(child)
                                        if (element.startswith('wardens') and child.attrib['name'] == 'wardens_vest_01'):
                                            new_vest = copy.deepcopy(child)
                                        elif (element.startswith('reapers') and child.attrib['name'] == 'reapers_vest_01'):
                                            new_vest = copy.deepcopy(child)
                                    new_vest.attrib['name'] = element.replace('.chr','')
                                    root.append(new_vest)                
                            elif xml == items_filter_helmet_file:
                                if element.split('_')[1] == 'helmet':
                                    for child in root.findall('Item'):
                                        if child.attrib['name'] == element.replace('.chr', ''):
                                            root.remove(child)
                                        if (element.startswith('wardens') and child.attrib['name'] == 'wardens_helmet_01'):
                                            new_helmet = copy.deepcopy(child)
                                        elif (element.startswith('reapers') and child.attrib['name'] == 'reapers_helmet_01'):
                                            new_helmet = copy.deepcopy(child)
                                    new_helmet.attrib['name'] = element.replace('.chr','')
                                    root.append(new_helmet)
                    if xml == armor_items_icons_file:
                        icon_tifs = walkfolder(os.path.join(equip_path, 'Libs\Icons\Armor'), '.tif')
                        for icon_tif in icon_tifs:
                            try:
                                size = icon_tif.replace('.tif','').split('_mip')[1]
                            except IndexError:
                                size = '1024'
                            for child in root.findall('image'):
                                if child.attrib['file'].endswith(icon_tif.replace('/','\\').replace(equip_path,'').replace('\Libs','Libs')):
                                    root.remove(child)
                            new_icon = ET.SubElement(root, 'Image', file = icon_tif.replace('/','\\').replace(equip_path,'').replace('\Libs','Libs'), 
                            name= icon_tif.replace('.tif','').split('/')[-1], pos="0,0", size=size + ',' + size)                                        
                    with open(xml, 'w') as f:
                        f.write(pretty_print(root))
                    print(Fore.GREEN + "---------------All items has been integrated to " + xml + '--------------------' + Fore.WHITE)
            modify_xml()
        append_xml()    
    integrate_equip()
    print(Fore.GREEN + '---------------All items has been integrated My congratulations!---------------------------------' + Fore.WHITE)
    another_item_to_integrate(repo)


def integrate_new_fbs(repo):
    print("insert your path to Game folder with fbs folder\n" + 
            "sample: e:\WorkFlow\Warface\3D\WFB\WFB_Season_03\41_Season_03_FBS_Wardens_Integration\Game")
    equip_path = os.path.abspath(input())


    def check_files_and_icons():
        print(Fore.BLUE + '------------------Checking files------------------------------')
        reaper_structure = os.path.join(equip_path,'Objects\Characters\\reapers')
        warden_structure = os.path.join(equip_path,'Objects\Characters\\wardens')
        structure_list = [reaper_structure, warden_structure] 
        ext_list = ['.chr', '.xml', '.mtl']
        armor_by_sides_list = []
        fbs_arrays = []
        common_array = []
        common_array_xml = []
        common_array_mtl =[]
        common_array_fp = []
        common_array_chr = []
        mtl_files = walkfolder(equip_path, '.mtl')


        def check_structure():
            if os.path.exists(element) and os.path.exists(os.path.join(element, 'fb_suits')):
                print(Fore.GREEN + element.split('\\')[-1] + ' fbs structure exists' + Fore.WHITE)      
        for element in structure_list:
            check_structure()


        def file_arrays():
            for ext in ext_list:
                if os.path.isdir(reaper_structure):
                    r_armor_array = walkfolder(os.path.join(reaper_structure), ext)
                    fbs_arrays.append(r_armor_array)
                if os.path.isdir(warden_structure):
                    w_armor_array = walkfolder(os.path.join(warden_structure), ext)
                    fbs_arrays.append(w_armor_array)
        file_arrays()

        for Items in fbs_arrays:
            for item in Items:
                item = item.split('/')[-1]
                common_array.append(item)
        for item in common_array:
            if item.endswith('.chr'):
                common_array_chr.append(item)
            elif item.endswith('.xml'):
                common_array_xml.append(item)
            elif item.endswith('.mtl'):
                common_array_mtl.append(item)
            elif (item.endswith('fp.chr') or item.endswith('fp.xml') or item.endswith('fp.mtl')):
                common_array_fp.append(item)
        icon_tifs = walkfolder(os.path.join(equip_path, 'Libs\Icons\Armor'), '.tif')
        icons_dds = walkfolder(os.path.join(equip_path, 'Libs\Icons\Armor'), '.dds')
        icons = []
        source_icons = []
        icons_chr_list = []
        for icon_tif in icon_tifs:
            if not icon_tif.split('_')[-1].startswith('mip'):
                icons_chr_list.append(icon_tif.replace('.tif','').split('/')[-1])
                source_icons.append(icon_tif) 
            icons.append(icon_tif.replace('.tif','').split('/')[-1])
            

        def check_icons(): 
            try:
                succes = True    
                for icon in icons:
                    icon_compare = False
                    icon_chr = False
                    dds_compare = False
                    for icon_dds in icons_dds:
                        if icon_dds.replace('.dds','').split('/')[-1] == icon:
                            icon_compare = True
                    if icon_compare == False:
                        print(Fore.RED + 'Pare dds - tif missed ' + icon_dds + Fore.WHITE)
                        succes = False
                for i in icons_chr_list:
                    if i.endswith('_full'):
                        for wear in common_array_chr:
                            if (wear.split('_')[2] == 'body'):
                                icon_chr = True
                        if icon_chr == False:
                            print(Fore.RED + "can't find chr-icon pare for " + wear + Fore.WHITE)
                            succes = False
                if succes == True:
                    print(Fore.GREEN + "------------------Icons has been checked succesfully------------------------------" + Fore.WHITE)
            except UnboundLocalError:
                print(Fore.RED + "------------------Check your resources! Can not complicete chr array!------------------------------" + Fore.WHITE)
        check_icons()


        print(Fore.YELLOW + 'Do you need mips?           y/n      ' + Fore.WHITE)
        need_mips = input()
        if need_mips != 'y' and need_mips != 'n':
            print(Fore.RED + 'I can not understand! Repeat, please!')
            check_icons()
        elif need_mips == 'y':
            for icon_tif in source_icons:
                splitTifFiles(icon_tif, repo)
        elif need_mips == 'n':
            print(Fore.GREEN + "Ok! I will continue!")
        icons_full = walkfolder(os.path.join(equip_path, 'Libs\Icons\Armor\FBS\Full'), '.tif')
        for icon in icons_full:
            if icon.split('_')[-1] == 'mip512.tif':
                if not (os.path.isfile(icon.replace('mip512.tif','mip1024.tif'))):
                    icon = os.rename(icon, icon.replace('mip512.tif','mip1024.tif'))
                else:
                    os.remove(icon)
        icons_full_dds = walkfolder(os.path.join(equip_path, 'Libs\Icons\Armor\FBS\Full'), '.dds')
        for icon in icons_full_dds:
            if icon.split('_')[-1] == 'mip512.dds':
                if not (os.path.isfile(icon.replace('mip512.dds','mip1024.dds'))):
                    icon = os.rename(icon, icon.replace('mip512.dds','mip1024.dds'))
                else:
                    os.remove(icon)

        def check_xml_chr():
            try:
                bodyes = []
                succes = True
                for element in common_array_chr:
                    if element.split('_')[2] == 'body':
                        bodyes.append(element)
                for body in bodyes:
                    bodyes_check = False
                    for element in common_array_chr:
                        if element.split('_')[2] == 'legs' and element.endswith(body.split('_')[-1]):
                            bodyes_check = True
                        elif element.split('_')[2] == 'arms' and element.replace('_fp','').endswith(body.split('_')[-1]):
                            bodyes_check = True
                    if bodyes_check == True:
                        print(Fore.GREEN + body + ' FBS complect has been checked succesfully' + Fore.WHITE)
                    else:
                        print(Fore.RED + 'for ' + body + ' complect is not full' + Fore.WHITE)
                for element in common_array_chr:
                    chr_xml_compare = False
                    for item in common_array_xml:
                        if element.replace('.chr','') == item.replace('.xml',''):
                            chr_xml_compare = True
                    if chr_xml_compare == False:
                        print(Fore.RED + "can't find chr-xml pare for " + element + Fore.WHITE)
                        succes = False
                for element in common_array_xml:
                    chr_xml_compare = False
                    for item in common_array_chr:
                        if element.replace('.xml','') == item.replace('.chr',''):
                            chr_xml_compare = True
                    if chr_xml_compare == False:
                        print(Fore.RED + "can't find chr-xml pare for " + element + Fore.WHITE)
                if succes == True:
                    print(Fore.GREEN + "-------------------xml and chr has been checked succesfully---------------------" + Fore.WHITE)
                return bodyes
            except UnboundLocalError:
                print(Fore.RED + "------------------Check your resources! Can not complicete xml array!------------------------------" + Fore.WHITE)
        bodyes = check_xml_chr()

        def check_chr_mtl():
            succes = True
            for element in common_array_chr:
                chr_mtl_compare = False
                if element.split('_')[2] != 'legs':
                    for item in common_array_mtl:
                        if ((element.replace('.chr','') == item.replace('.mtl','')) or 
                            (element.replace('.chr','').replace('_body','') == item.replace('.mtl',''))):
                            chr_mtl_compare = True
                    if chr_mtl_compare == False:
                        print(Fore.RED + "can't find chr-mtl pare for " + element + Fore.WHITE)
                        succes = False
            for element in common_array_mtl:
                chr_mtl_compare = False
                for item in common_array_chr:
                    if (element.replace('.mtl','') == item.replace('.chr','') or 
                        item.replace('.chr','').replace('_body','') == element.replace('.mtl','')):
                        chr_mtl_compare = True
                if chr_mtl_compare == False:
                    print(Fore.RED + "can't find chr-mtl pare for " + element + Fore.WHITE)
            if succes == True:
                print(Fore.GREEN + "-------------------mtl and chr has been checked succesfully---------------------" + Fore.WHITE)    
        check_chr_mtl()
        def check_textures():
            success = True
            print (Fore.BLUE + "-------------------------------Checking existing textures------------------------" + Fore.WHITE)
            for elems in mtl_files:
                reading = open(elems, 'r').readlines()
                for strings in reading:
                    if 'Texture Map=' in strings:
                        clear_strings = equip_path + '/' + strings.split('File="')[1].split('"')[0]
                        if (os.path.isfile(clear_strings) and os.path.isfile(clear_strings.replace('.tif','.dds'))):
                                # print 'Warning!!! Contain original NormalMap. Contact with LeadArt, is it ok?\n', elems, clear_strings
                                continue
                        elif os.path.isfile(clear_strings):
                            success = False
                            print (Fore.RED + "Warning. DDS file is empty, but TIF is exist:", equip_path + '/' + 'Game' + \
                                                                                    clear_strings.split('Game')[1].replace(
                                                                                        '.tif', '.dds') + Fore.WHITE)
                        elif os.path.isfile(clear_strings.replace('.tif', '.dds')):
                            success = False
                            print (Fore.RED + "Warning. TIF file is empty, but DDS is exist:", equip_path + '/' + 'Game' + \
                                                                                    clear_strings.split('Game')[1].replace(
                                                                                        '.tif', '.dds') + Fore.WHITE)
                        else:
                            print(Fore.RED + "ERROR! File: " + elems + ' Empty files ' + clear_strings + Fore.WHITE + '\n')  # print "ERROR! Empty files", clear_strings
                            success = False
            if success == True:
                print(Fore.GREEN + "-------------------textures from .mtl has been checked succesfully---------------------" + Fore.WHITE)
        check_textures()
       
       
        def copy_files():
            print(Fore.YELLOW + '------------------Should I copy resources to repository?------------y/n?----------------' + Fore.WHITE)
            ready_to_copy = input()
            if (ready_to_copy != 'y' and ready_to_copy != 'n'):
                print(Fore.RED + 'I can not understand, repeat, please!' + Fore.WHITE)
                copy_files()
            elif ready_to_copy == 'y': 
                items = ['.tif','.dds','.chr', '.xml', '.mtl']
                print(Fore.BLUE + '------------------Copying files to repository------------------------------' + Fore.WHITE)
                for item in items:
                    try:
                        resources_copy(equip_path, repo, (walkfolder(equip_path, item)))
                        print(Fore.GREEN + '------------------Structure copied for ' + item + '------------------------------' + Fore.WHITE)
                    except:
                        print(Fore.RED + '------------------Can not copy, check your file structure------------------------------' + Fore.WHITE)
            elif ready_to_copy == 'n':
                print(Fore.YELLOW + '------------------Should I continue integration?------------y/n?----------------' + Fore.WHITE)
                continue_to_integrate = input()
                if (continue_to_integrate != 'y' and continue_to_integrate != 'n'):
                    print(Fore.RED + 'I can not understand, repeat, please!' + Fore.WHITE)
                    copy_files()
                elif continue_to_integrate == 'n':
                    print(Fore.YELLOW + 'Ok! See you!' + Fore.WHITE)
                    sys.exit()
                elif ready_to_copy == 'y': 
                    print(Fore.YELLOW + 'Ok! Continue!' + Fore.WHITE)
        copy_files()
        return bodyes, icon_tifs
    print(Fore.BLUE + '------------------Icons and resources has been checked------------------------------' + Fore.WHITE)
    icons_and_chr = check_files_and_icons()
    bodyes = icons_and_chr[0]
    icon_tifs = icons_and_chr[1]


    def integrate_equip():
        def generate_xml():
            print(Fore.BLUE + '------------------generating xml-files in Game/Items/------------------------------' + Fore.WHITE)
            for element in bodyes:
                def set_rarity_marker_since_exclusive():
                    print(Fore.YELLOW + '(y/n) Do you want to set attribs ' + element.replace('.chr','') +'------------------------------ '+ Fore.WHITE)
                    set_attribs = input()
                    if (set_attribs != 'y' and set_attribs != 'n'):
                            print(Fore.RED + "I can not understand! Repeat, please" + Fore.WHITE)
                            set_rarity_marker_since_exclusive()
                    if set_attribs == 'y':
                        print(Fore.YELLOW + "Insert rarity: \n1-common\n 2-uncommon\n 3-rare\n 4-epic\n 5-legendary\n" + Fore.WHITE)
                        rarity = input()
                        if rarity == '1':
                            rarity_choise = 'common'
                        elif rarity == '2':
                            rarity_choise = 'uncommon'
                        elif rarity == '3':
                            rarity_choise = 'rare'
                        elif rarity == '4':
                            rarity_choise = 'epic'
                        elif rarity == '5':
                            rarity_choise = 'legendary'
                        elif rarity != ('1' or '2' or '3' or '4' or '5'):
                            print(Fore.RED + "I can not understand! Repeat, please" + Fore.WHITE)
                        else:
                            rarity = 'common'
                        print(Fore.YELLOW + '(y/n) This item is exclusive ' + element.replace('.chr','') + '------------------------------' + Fore.WHITE)
                        set_exclisive = input()
                        if (set_exclisive != 'y' and set_exclisive != 'n'):
                            print(Fore.RED + "I can not understand! Repeat, please" + Fore.WHITE)
                            set_rarity_marker_since_exclusive()   
                        print(Fore.YELLOW + '(y/n) Do you want to set marker for ' + element.replace('.chr','')+ '------------------------------' + Fore.WHITE)
                        set_marker = input()
                        if (set_marker != 'y' and set_marker != 'n'):
                            print(Fore.RED + "I can not understand! Repeat, please" + Fore.WHITE)
                            set_rarity_marker_since_exclusive()
                        if set_marker == 'y':
                            print(Fore.YELLOW + "Insert your marker" + Fore.WHITE)
                            marker = input()
                        else:
                            marker = None  
                        print(Fore.YELLOW + '(y/n) Do you want to set since for ' + element.replace('.chr','')+ '------------------------------' + Fore.WHITE)
                        set_since = input()
                        if (set_since != 'y' and set_since != 'n'):
                            print(Fore.RED + "I can not understand! Repeat, please" + Fore.WHITE)
                            set_rarity_marker_since_exclusive()
                        if set_since == 'y':
                            print(Fore.YELLOW + "Insert your marker"+ '------------------------------' + Fore.WHITE)
                            since = input()
                        else:
                            since = None
                    else:
                        print (Fore.GREEN + 'Ok! Continue!')  
                        rarity_choise = None 
                        set_exclisive = None 
                        marker = None 
                        since = None 
                    return rarity_choise, set_exclisive, marker, since                     
                attributes = set_rarity_marker_since_exclusive()
                print(element)

                new_element = os.path.join(repo,'Game\Items\Skins\\', element.replace('_body','').replace('.chr','.xml'))
                if os.path.isfile(new_element):
                    os.remove(new_element)
                if element.startswith('wardens_fbs'):
                    pattern = os.path.join(repo,'Game\Items\Skins','wardens_fbs_01.xml')  
                if element.startswith('reapers_fbs'):
                    pattern = os.path.join(repo,'Game\Items\Skins','reapers_fbs_01.xml')
                shutil.copyfile(pattern, new_element)    
                root = ET.parse(new_element).getroot()
                root.attrib['name'] = element.replace('_body','').replace('.chr','')
                for child in root.find('UI_stats'):
                    if child.attrib['name'] == 'name':
                        child.attrib['value'] = "@ui_armor_"+ element.replace('_body','').replace('.chr','') + "_name"
                    if child.attrib['name'] == 'description':
                        child.attrib['value'] = "@ui_armor_"+ element.replace('_body','').replace('.chr','') + "_desc"
                    if child.attrib['name'] == 'icon':
                        child.attrib['value'] = element.replace('_body','').replace('.chr','')
                    if child.attrib['name'] == 'rarity' and not (attributes[0] is None):
                        child.attrib['value'] = attributes[0]
                    if child.attrib['name'] == 'exclusive' and attributes[1] == 'y':
                        child.attrib['value'] = '1'
                    if child.attrib['name'] == 'marker' and not (attributes[2] is None):
                        child.attrib['value'] = attributes[2]
                    if child.attrib['name'] == 'since' and not (attributes[3] is None):
                        child.attrib['value'] = attributes[3]
                for child in root.find('slots').find('slot').find('assets').findall('asset'):
                    if (child.attrib['name'] == "wardens_fbs_body_01" or child.attrib['name'] == "reapers_fbs_body_01"):
                        child.attrib['name'] = element.replace('.chr','')
                    if (child.attrib['name'] == "wardens_fbs_legs_01" or child.attrib['name'] == "reapers_fbs_legs_01"):
                        child.attrib['name'] = element.replace('body', 'legs').replace('.chr','')
                    if (child.attrib['name'] == "wardens_fbs_arms_01_fp" or child.attrib['name'] == "reapers_fbs_arms_01_fp"):
                        child.attrib['name'] = element.replace('body', 'arms').replace('.chr','_fp')
                with open(new_element, 'w') as f:
                    f.write(pretty_print(root))             
        generate_xml()
        def append_xml():
            text_armors_file = os.path.join(repo, 'Game/Languages/Console/text_armors.xml')
            items_filter_fbs_file = os.path.join(repo, 'Game/Libs/Config/ItemsFilter_fbs.xml')
            appearance_file = os.path.join(repo, 'Game/Libs/Config/Shop/appearance.xml')
            asset_items_icons_file = os.path.join(repo, 'Game/Libs/Config/UI/assetsItemsIcons.xml')
            xmls = [text_armors_file, 
                    items_filter_fbs_file,
                    appearance_file,
                    asset_items_icons_file]
            def modify_xml():
                for xml in xmls:
                    root = ET.parse(xml).getroot()
                    for element in bodyes:
                            if xml == text_armors_file:
                                for child in root.findall('entry'):
                                    if (child.attrib['key'].endswith(element.replace('_body','').replace('.chr', '_name')) or
                                    child.attrib['key'].endswith(element.replace('_body','').replace('.chr', '_desc'))):
                                        root.remove(child)
                                for child in root.findall('entry'):
                                    if child.attrib['key'] == "ui_armor_shared_jacket_01_name":
                                        new_entry_name = copy.deepcopy(child)
                                        new_entry_name.attrib['key'] = 'ui_armor_'+ element.replace('_body','').replace('.chr', '_name')
                                        root.append(new_entry_name)
                                for child in root.findall('entry'):
                                    if child.attrib['key'] == "ui_armor_shared_jacket_01_name":
                                        new_entry_desc = copy.deepcopy(child)    
                                        new_entry_desc.attrib['key'] = 'ui_armor_'+ element.replace('_body','').replace('.chr', '_desc')
                                        root.append(new_entry_desc)
                            elif xml == appearance_file:
                                for child in root.findall('category'):
                                    if child.attrib['name'] == 'skin':
                                        for i in child.findall('offer'):
                                            if i.attrib['name'] == element.replace('_body','').replace('.chr',''):
                                                child.remove(i)
                                        new_offer = ET.SubElement(child, 'offer', name = element.replace('_body','').replace('.chr',''))
                            elif xml == items_filter_fbs_file:
                                    for child in root.findall('Item'):
                                        if child.attrib['name'] == element.replace('_body','').replace('.chr',''):
                                            root.remove(child)
                                        if (element.startswith('wardens') and child.attrib['name'] == 'wardens_fbs_01'):
                                            new_fbs = copy.deepcopy(child)
                                        elif (element.startswith('reapers') and child.attrib['name'] == 'reapers_fbs_01'):
                                            new_fbs = copy.deepcopy(child)
                                    new_fbs.attrib['name'] = element.replace('_body','').replace('.chr','')
                                    root.append(new_fbs)                
                    if xml == asset_items_icons_file:
                        icon_tifs = walkfolder(os.path.join(equip_path, 'Libs\Icons\Armor'), '.tif')
                        for icon_tif in icon_tifs:
                            for child in root.findall('Image'):
                                if child.attrib['name'] == icon_tif.replace('\\','/').split('/')[-1].replace('.tif',''):
                                    root.remove(child)                    
                            try:
                                    size = icon_tif.replace('.tif','').split('_mip')[1]
                            except IndexError:
                                    size = '1024'
                            if not icon_tif.replace('\\', '/').split('/')[-2].lower().startswith('full'):
                                    new_icon = ET.SubElement(root, 'Image', file = icon_tif.replace('/','\\').replace(equip_path,'').replace('\Libs','Libs'), 
                                    name= icon_tif.replace('.tif','').split('/')[-1], pos="0,0", size=size + ',' + size)
                            elif icon_tif.split('_')[-1].lower().startswith('mip1024.tif'):
                                    new_icon = ET.SubElement(root, 'Image', file = icon_tif.replace('/','\\').replace(equip_path,'').replace('\Libs','Libs'), 
                                    name= icon_tif.replace('.tif','').split('/')[-1], pos="0,0", size=str(int(int(size)/2)) + ',' + size)
                            elif icon_tif.split('_')[-1].lower().startswith('full.tif'):
                                    new_icon = ET.SubElement(root, 'Image', file = icon_tif.replace('/','\\').replace(equip_path,'').replace('\Libs','Libs'), 
                                    name= icon_tif.replace('.tif','').split('/')[-1], pos="0,0", size=size + ',' + str(int(size)*2))                                   
                    with open(xml, 'w') as f:
                        f.write(pretty_print(root))
                    print(Fore.GREEN + "---------------All items has been integrated to " + xml + '--------------------' + Fore.WHITE)
            modify_xml()
        append_xml()    
    integrate_equip()
    print(Fore.GREEN + '---------------All items has been integrated My congratulations!---------------------------------' + Fore.WHITE)
    another_item_to_integrate(repo)


def victory_animation(repo):
    def check_anims_and_icons():
        print("insert your path to Game folder with result screen animations\n" + 
            "sample: e:\WorkFlow\Warface\3D\WFB\WFB_Season_03\35_Season_03_Victory_Pose_Pack_Halloween_Black_Friday_x2\Game")
        anim_path = os.path.abspath(input())
        print(Fore.BLUE + '--------------------------------Checking files-------------------------------------------------------')
        if os.path.exists(os.path.join(anim_path,'Animations\Human\male\special\Result_Screen')):
            print(Fore.GREEN + 'file structure exists' + Fore.WHITE)
        else:
            print(Fore.RED + 'file structure mistake' + Fore.WHITE)
        pose_files = walkfolder(os.path.join(anim_path,'Animations'), ".caf")
        poses=[]
        if os.path.exists(os.path.join(anim_path, 'Libs\Icons\VictoryPoses')):
            print(Fore.GREEN + 'icon structure exists' + Fore.WHITE)
        else:
            print(Fore.RED + 'icon structure mistake' + Fore.WHITE)
        for pose_file in pose_files:
            poses.append(pose_file.replace(".caf",'').split('/')[-1])
        icon_files = walkfolder(os.path.join(anim_path,'Libs\Icons\VictoryPoses'), ".tif")
        icons_dds = walkfolder(os.path.join(anim_path,'Libs\Icons\VictoryPoses'), ".dds")
        icon_tifs = []
        for icon_file in icon_files:
            icon_tif = os.path.split(icon_file)[1]
            icon_tifs.append(icon_tif)
            icon_compare = False
            for icon_dds in icons_dds:
                if icon_dds.replace('.dds','') == icon_file.replace('.tif',''):
                    icon_compare = True
            if icon_compare == False:
                print(Fore.RED + 'Pare dds - tif missed ' + icon_file + Fore.WHITE)
        for pose in poses:
            compare = False
            for icon_file in icon_files:
                try:
                    if ((icon_file.replace(".tif",'').split('/')[-1]).startswith('victorypose') and 
                    (icon_file.replace(".tif",'').split('/')[-1]).endswith((pose.split('_')[1]+ ('_') + pose.split('_')[3] + ('_') + pose.split('_')[4]).lower())): 
                        print (Fore.GREEN + 'pose icon found ' + icon_file.split('/')[-1] + Fore.WHITE)
                        compare = True
                except: 
                    print(Fore.RED + 'Wrong pose or icon naming ' + pose + Fore.WHITE)
                    break
            if compare == False:
                try:
                    print (Fore.RED + 'Check your poses and icons ' + icon_file + '--->' + pose + Fore.WHITE)
                    print ('example: pose =  ResultScreen_Lootbox_Pose_backscratching_01.caf\n icon shoul be = victorypose_lootbox_backscratching_01.tif')
                except:
                    print(Fore.RED + 'No icons at all ' + pose + Fore.WHITE)
        print(Fore.YELLOW + '------------------Should I continue integration?------------y/n?----------------' + Fore.WHITE)
        continue_to_integrate = input()
        if (continue_to_integrate != 'y' and continue_to_integrate != 'n'):
            print(Fore.RED + 'I can not understand, repeat, please!' + Fore.WHITE)
            check_anims_and_icons()
        elif continue_to_integrate == 'n':
            print(Fore.YELLOW + 'Ok! See you!' + Fore.WHITE)
            another_item_to_integrate(repo)
        print (Fore.BLUE + '--------------------------------Copying files-------------------------------------------------------')
        try:
            resources_copy(anim_path, repo, icon_files)
            resources_copy(anim_path, repo, pose_files)
            resources_copy(anim_path, repo, icons_dds)
            print(Fore.GREEN + 'structure with files copied to repository' + Fore.WHITE)
        except:
            print(Fore.RED + 'structure copy failed' + Fore.WHITE)
        return icon_tifs, poses
    attribs = check_anims_and_icons()
    icon_tifs = attribs[0]
    poses = attribs[1]
    def poses_mips():
        print (Fore.YELLOW + '--------------------------------Do you need new mips?-------------y/n---------------------' + Fore.WHITE)
        mips = input()
        if mips !='y' and mips !='n':
            print (Fore.RED + '-----------------------------Can not understand you-------------------------------' + Fore.WHITE)
            poses_mips()
        elif mips == 'y':
            for icon_tif in icon_tifs:
                icon_tif = os.path.join(repo, 'Game\Libs\Icons\VictoryPoses', icon_tif)
                splitTifFiles(icon_tif, repo)
        else:
            (Fore.GREEN + '------------------------------As you wish--------------------------------------' + Fore.WHITE)
    poses_mips()
    def modify_playerfullbody(poses):
        print(Fore.BLUE + '--------------------Modifiying playerfullbody.xml---------------------------------' + Fore.WHITE)
        player_fullbody_file = os.path.join(repo,"Game/Animations/graphs/playerfullbody.xml")
        player_fullbody = ET.parse(player_fullbody_file)
        root = player_fullbody.getroot()
        KeyStates = root.findall('KeyState') 
        for KeyState in KeyStates:
            if KeyState.attrib['name'] == "Action":
                keys = KeyState.findall('Key')
                for pose in poses:
                    for key in keys:
                        if key.attrib['value'] == pose:
                            KeyState.remove(key)
                for pose in poses:
                    new_element = ET.SubElement(KeyState, 'Key', value = pose)
        states = root.find('States')
        for i in root.find('Views'):
            if i.attrib['name'] == "ResultScreen":
                view_states = i
        links = root.find('Transitions')
        for pose in poses:
            for state in states:
                if state.attrib['id'] == ('X_[Stance]_'+ pose.replace(pose.split('_')[-1],'') + 'Null_[Item]' + "_" + pose.split('_')[-1]).replace('_Null','Null'):
                    states.remove(state)
                if state.attrib['id'] == ("x_[stance]_" + pose.replace(pose.split('_')[-1],'') + '[item]' + "_" + pose.split('_')[-1]):
                    states.remove(state)
            for view_state in view_states:
                if view_state.attrib['id'] == (("x_[stance]_" + pose.replace(pose.split('_')[-1],'') + '[item]' + "_" + pose.split('_')[-1])
                or ('X_[Stance]_'+ pose.replace(pose.split('_')[-1],'') + 'Null_[Item]' + "_" + pose.split('_')[-1]).replace('_Null','Null')):
                    view_states.remove(view_state)
            for link in links:
                if (link.attrib['from'] == (("x_[stance]_" + pose.replace(pose.split('_')[-1],'') + '[item]' + "_" + pose.split('_')[-1])
                or ('X_[Stance]_'+ pose.replace(pose.split('_')[-1],'') + 'Null_[Item]' + "_" + pose.split('_')[-1]).replace('_Null','Null')) 
                or link.attrib['to'] == (("x_[stance]_" + pose.replace(pose.split('_')[-1],'') + '[item]' + "_" + pose.split('_')[-1])
                or ('X_[Stance]_'+ pose.replace(pose.split('_')[-1],'') + 'Null_[Item]' + "_" + pose.split('_')[-1]).replace('_Null','Null'))):
                    links.remove(link)
        for pose in poses:
            node_name = ('X_[Stance]_'+ pose.replace(pose.split('_')[-1],'') + 'Null_[Item]' + "_" + pose.split('_')[-1]).replace('_Null','Null')
            node_anim_name = "x_[stance]_" + pose.replace(pose.split('_')[-1],'') + '[item]' + "_" + pose.split('_')[-1]
            arrx, arry = [],[]
            for state in states:
                if state.attrib['id'] == 'X_[Stance]_ResultScreen_Black_Friday_PoseNull_[Item]_01':
                    new_state = copy.deepcopy(state)
                    new_state.attrib['id'] = (node_name)
                    new_state.find('SelectWhen').find('Action').attrib['value'] = pose
                    states.append(new_state)
                if state.attrib['id'] == "x_[stance]_ResultScreen_Black_Friday_Pose_[item]_01":
                    new_anim_state = copy.deepcopy(state)
                    new_anim_state.attrib['id'] = (node_anim_name)
                    new_anim_state.find('SelectWhen').find('Action').attrib['value'] = pose
                    new_anim_state.find('ParameterizedData').attrib['animationName'] = pose
                    new_anim_state.find('AnimationLayer1').attrib['animation1'] = pose
                    states.append(new_anim_state)     
            for view_state in view_states:
                arrx.append(int(float(view_state.get('x'))))
                arry.append(int(float(view_state.get('y'))))
            x = max(arrx)
            y = max(arry)
            for view_state in view_states:
                if view_state.attrib['id'] == 'X_[Stance]_ResultScreen_Black_Friday_PoseNull_[Item]_01':
                    new_view_state = copy.deepcopy(view_state)
                    new_view_state.attrib['id'] = node_name
                    new_view_state.attrib['x'] = str(x)
                    new_view_state.attrib['y'] = str(y + 100)
                    view_states.append(new_view_state)
                if view_state.attrib['id'] == 'x_[stance]_ResultScreen_Black_Friday_Pose_[item]_01':
                    new_anim_view_state = copy.deepcopy(view_state)
                    new_anim_view_state.attrib['id'] = node_anim_name
                    new_anim_view_state.attrib['x'] = str(x)
                    new_anim_view_state.attrib['y'] = str(y + 200)
                    view_states.append(new_anim_view_state)
            for link in links:
                if (link.attrib['from'] == 'X_[Stance]_ResultScreen_Black_Friday_PoseNull_[Item]_01' 
                and 
                link.attrib['to'] == 'X_[Stance]_ResultScreen_IdleNull_[Item]'):
                    new_link = copy.deepcopy(link)
                    new_link.attrib['from'] = node_name
                    links.append(new_link)
                if (link.attrib['from'] == 'X_[Stance]_ResultScreen_Black_Friday_PoseNull_[Item]_01' 
                and 
                link.attrib['to'] == "x_[stance]_ResultScreen_Black_Friday_Pose_[item]_01"):
                    new_link = copy.deepcopy(link)
                    new_link.attrib['from'] = node_name 
                    new_link.attrib['to'] = node_anim_name
                    links.append(new_link)
                if (link.attrib['from'] == 'X_[Stance]_ResultScreen_IdleNull_[Item]' 
                and 
                link.attrib['to'] == "X_[Stance]_ResultScreen_Black_Friday_PoseNull_[Item]_01"):
                    new_link = copy.deepcopy(link) 
                    new_link.attrib['to'] = node_name
                    links.append(new_link)
                if (link.attrib['from'] == 'x_[stance]_ResultScreen_Black_Friday_Pose_[item]_01' 
                and 
                link.attrib['to'] == "X_[Stance]_ResultScreen_Black_Friday_PoseNull_[Item]_01"):
                    new_link = copy.deepcopy(link) 
                    new_link.attrib['from'] = node_anim_name
                    new_link.attrib['to'] = node_name
                    links.append(new_link)
                if (link.attrib['from'] == 'x_[stance]_ResultScreen_Black_Friday_Pose_[item]_01' 
                and 
                link.attrib['to'] == "X_[Stance]_ResultScreen_IdleNull_[Item]"):
                    new_link = copy.deepcopy(link) 
                    new_link.attrib['from'] = node_anim_name
                    links.append(new_link)
        with open(player_fullbody_file, 'w') as f:
            f.write(pretty_print(root))
        print(Fore.GREEN + '--------------------playerfullbody.xml has been modifyed---------------------' + Fore.WHITE)
    
    def rebuild_animations():
        print(Fore.BLUE + 'Please! Rebuild your playerfullbody.ag (just resave playerfullbody.xml in animgraph)' + Fore.WHITE)
        editor = subprocess.Popen(os.path.join(repo, 'Bin64\\Editor.exe'))
        input('\npress any key to continue!\n')
    
    def modify_common_xml():
        appearenceFile = os.path.join(repo, 'Game/Libs/Config/Shop/appearance.xml')
        items_victory_animation_file = os.path.join(repo, 'Game/Libs/Config/ItemsFilter_victoryposes.xml')
        dataorderFile = os.path.join(repo, 'Game/UI/dataorder.xml')
        victory_animation_file = os.path.join(repo, 'Game/Libs/Config/UI/victoryposes.xml')
        text_wfgo_items_file = os.path.join(repo, 'Game/Languages/Console/text_wfgo_items.xml')
        #-----------------------------------------------------roots---------------------------------------------------------------
        appearence_root = ET.parse(appearenceFile).getroot()
        items_victory_animation_root = ET.parse(items_victory_animation_file).getroot()
        dataorder_root = ET.parse(dataorderFile).getroot()
        text_wfgo_items_root = ET.parse(text_wfgo_items_file).getroot()
        victory_animation_root = ET.parse(victory_animation_file).getroot()
        #-----------------------------------------------------appearance----------------------------------------------------------
        categoryes = appearence_root.findall('category')
        for category in categoryes:
            if category.attrib['name'] == "bodyParts":
                for child in category.findall('category'):
                    if child.attrib['name'] == "victorypose":
                        offers = child.findall('offer')
                        for icon_tif in icon_tifs:
                            for offer in offers:
                                if offer.attrib['name'] == icon_tif.replace('.tif',''):
                                    child.remove(offer)
                        for icon_tif in icon_tifs:
                            new_offer= ET.SubElement(child, 'offer', name = icon_tif.replace('.tif',''))
        with open(appearenceFile, 'w') as f:
            f.write(pretty_print(appearence_root))
        print(Fore.GREEN + '-----------------appierence xml has been modyfiyed---------------------------' + Fore.WHITE)
        #----------------------------------------------------victory_poses-------------------------------------------------------
        icon_postfixes = ['.tif', '_mip64.tif', '_mip128.tif', '_mip256.tif', '_mip512.tif' ]
        for image in victory_animation_root.findall('image'):
            for icon_tif in icon_tifs:
                for icon_postfix in icon_postfixes:
                    if image.attrib['name'] == (icon_tif + icon_postfix).replace('.tif',''):
                        victory_animation_root.remove(image)
        for icon_tif in icon_tifs:        
            for icon_postsfix in icon_postfixes: 
                size = (icon_postsfix.replace('_mip','').replace('.tif',''))
                if icon_postsfix == '.tif':
                    size = '1024'  
                new_image = ET.SubElement(victory_animation_root, 'image', file=("Libs/Icons/VictoryPoses/" + icon_tif.replace('.tif', icon_postsfix)),
                name=(icon_tif.replace('.tif', icon_postsfix).replace('.tif','')), pos="0,0", size = (size + ',' + size))
        with open(victory_animation_file, 'w') as f:
            f.write(pretty_print(victory_animation_root))
        print(Fore.GREEN + '-----------------victoryposes.xml has been modyfiyed-------------------------' + Fore.WHITE)
        #-----------------------------------------------------Game/Languages/Console/text_wfgo_items.xml------------------------------
        entrys = text_wfgo_items_root.findall('entry')
        for entry in entrys:
            for icon_tif in icon_tifs:
                if entry.attrib['key'].startswith(icon_tif.replace('.tif','')):
                    text_wfgo_items_root.remove(entry)
        new_entrys = []
        for icon_tif in icon_tifs:
            new_entry_name = ET.SubElement(text_wfgo_items_root, 'entry', key = icon_tif.replace('.tif','_name'))
            new_entry_desc = ET.SubElement(text_wfgo_items_root, 'entry', key = icon_tif.replace('.tif','_desc'))
            new_entrys.append(new_entry_name)
            new_entrys.append(new_entry_desc)
        for new_entry in new_entrys:
            new_entry_original = ET.SubElement(new_entry, 'original', value="New ViCtOrY pOsE!!!!!!!!!!!!!!!!")
            new_entry_translation = ET.SubElement(new_entry, 'translation', value="New ViCtOrY pOsE!!!!!!!!!!!!!!!!")
        with open(text_wfgo_items_file, 'w') as f:
            f.write(pretty_print(text_wfgo_items_root))
        print(Fore.GREEN + '-----------------text_wfgo_items.xml has been modyfiyed----------------------' + Fore.WHITE)
        #-----------------------------------------------------ItemsFilter_victoryposes-----------------------------------------------
        for child in items_victory_animation_root.findall('Item'):
            for icon_tif in icon_tifs:
                if child.attrib['name'] == icon_tif.replace('.tif',''):
                    items_victory_animation_root.remove(child)
        for icon_tif in icon_tifs:
            new_filteritem = ET.SubElement(items_victory_animation_root, 'Item', name=icon_tif.replace('.tif',''))
            new_subline = ET.SubElement(new_filteritem, 'Warden', level="1")  
            new_subline = ET.SubElement(new_filteritem, 'Reaper', level="1")      
        with open(items_victory_animation_file, 'w') as f:
            f.write(pretty_print(items_victory_animation_root))
        print(Fore.GREEN + '-----------------ItemsFilter.xml has been modyfiyed-------------------------' + Fore.WHITE)
        #-------------------------------------------------------dataorder------------------------------------------------------------
        for child in dataorder_root:
            if child.attrib['name'] == "victorypose":
                for icon_tif in icon_tifs:
                    for data in child.findall('data'):
                        if data.attrib['name'] == icon_tif.replace('.tif',''):
                            child.remove(data)
                    new_data = ET.SubElement(child, 'data', name=icon_tif.replace('.tif',''))
        with open(dataorderFile, 'w') as f:
            f.write(pretty_print(dataorder_root))
        print(Fore.GREEN + '-----------------dataorder.xml has been modyfiyed---------------------------' + Fore.WHITE)
        #-------------------------------------------------------special.chrparams----------------------------------------------------
        special_chr_file = os.path.join(repo, 'Game\Objects\Characters\Human', 'special.chrparams')
        root = ET.parse(special_chr_file).getroot()
        for element in root.find('AnimationList').findall('Animation'):
            for pose in poses:
                if element.attrib['name'] == pose:
                    root.find('AnimationList').remove(element)
        for pose in poses:
            new_line = ET.SubElement(root.find('AnimationList'), 'Animation', name = pose, path = "special/Result_Screen/" + pose + '.caf')
        with open(special_chr_file, 'w') as f:
            f.write(pretty_print(root))  
        print(Fore.GREEN + '-----------------special.chrparams has been modyfiyed---------------------------' + Fore.WHITE)
    modify_common_xml()
    def create_poses_xml():
        print(Fore.BLUE + '-----------------creating poses xml-------------------------' + Fore.WHITE)
        pose_directory = os.path.join(repo, 'Game\Items\VictoryPoses')
        pattern = os.path.join(pose_directory,'victorypose_default_01.xml')
        for icon_tif in icon_tifs:
            pose_xml = pattern.replace('victorypose_default_01',icon_tif.replace('.tif',''))
            if os.path.isfile(pose_xml):
                os.remove(pose_xml)
            shutil.copyfile(pattern, pose_xml)
            root = ET.parse(pose_xml).getroot()
            root.attrib['name'] = icon_tif.replace('.tif','')
            def specify():
                print('-----------------do you want to specify the rarity, side and marker for pose? ' + icon_tif.replace('.tif','') + ' y/n-------------------------')
                specicy = input()
                if specicy != 'y' and specicy != 'n':
                    print(Fore.RED+'-----------------Sorry, Can not understand!-------------------------' + Fore.WHITE) 
                    specify()
                def specify_attribs():
                    print ('-----------------The pose ' + icon_tif.replace('.tif','') + ' is exlusive?-----y/n---------')
                    exclusive = input()
                    if exclusive != 'y' and exclusive != 'n':
                        print(Fore.RED+'-----------------Sorry, Can not understand!-------------------------' + Fore.WHITE)
                        specify_attribs()
                    print ('-----------------The pose ' + icon_tif.replace('.tif','') + ' for which side-----w/r/wr---------')
                    side = input()
                    if side != 'w' and side != 'r' and side != 'wr':
                        print(Fore.RED+'-----------------Sorry, Can not understand!-------------------------' + Fore.WHITE)
                        specify_attribs()
                    print ('-----------------The pose ' + icon_tif.replace('.tif','') + ' has some marker-----y/n---------')
                    marker = input()
                    if marker != 'y' and marker != 'n':
                        print(Fore.RED+'-----------------Sorry, Can not understand!-------------------------' + Fore.WHITE)
                        specify_attribs()
                    elif marker == 'y':
                        print ('-----------------insert the pose marker please! Smaple: for halloween pose is "halloween"---------')
                        marker = input()
                    return exclusive, side, marker
                if specicy == 'y':
                    (exclusive, side, marker) = specify_attribs() 
                    return (specicy, exclusive, side, marker) 
            specify = specify()
            if specify != None:
                if (specify[0] == 'y' and (specify[3] != None)):
                    new_marker = ET.SubElement(root.find('UI_stats'), 'param' , name="marker", value=specify[3])          
                for child in root.find('UI_stats'):
                    if (specify[0] == 'y' and specify[1] == 'y' and child.attrib['name'] == 'exclusive'):
                        child.attrib['value'] == '1'
                if (specify[0] == 'y' and specify[2] != None, child.attrib['name'] == 'exclusive'):
                    for child in root.find('mmo_stats'):
                        if child.attrib['name'] == "classes":
                            child.attrib['value'] = specify[2].upper()
            for child in root.find('mmo_stats'):
                if child.attrib['name'] == "shopcontent":
                    child.attrib['value'] = '1'   
            for child in root.find('UI_stats'):
                child.attrib['value'] = child.attrib['value'].replace('victorypose_default_01', icon_tif.replace('.tif',''))  
            for child in root.find('customization'):
                if child.attrib['name'] == "resource":
                    for pose in poses:
                        if icon_tif.replace(".tif",'').endswith((pose.split('_')[1] + ('_') + pose.split('_')[3] + ('_') + pose.split('_')[4]).lower()):
                            child.attrib['value'] = pose                 
            with open(pose_xml, 'w') as f:
                f.write(pretty_print(root))    
            print(Fore.GREEN + '-----------------pose ' + icon_tif.replace('.tif','') + ' created-------------------------' + Fore.WHITE)
    create_poses_xml()
    modify_playerfullbody(poses)
    rebuild_animations()
    another_item_to_integrate(repo)


def main():
    init(convert=True)
    print (Fore.YELLOW + 'Insert your repo adress' + Fore.WHITE)
    repo = os.path.abspath(sg.popup_get_folder('Insert your repo adress'))
    

    integration_function(repo)

if __name__ == "__main__":
    mip_list = ['_shop_mip64', '_shop_mip128', '_shop_mip256', '_shop_mip512', '_shop']
    main()