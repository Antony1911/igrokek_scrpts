import os, glob
import xml.etree.ElementTree as ET
from xml.dom import minidom
import shutil
import logging
import subprocess
import colorama
from colorama import init, Fore, Back, Style
import sys
import re
import PySimpleGUI as sg
sg.theme('Dark2')
# check repo
# check naming
# check files inside folder from Minsk
# are all files on place?
# do u know variation name?
# try to modify/create files (items: modify xml; create skin xml; objects: modify xml; icons mapping; translation
# copy


def pretty_print(element, indent=None):
    if indent is None:
        indent = "    "
    original = ET.tostring(element, 'utf8')
    reparsed = minidom.parseString(original)
    indented = reparsed.toprettyxml(indent=indent, newl='\n')
    return '\n'.join([s for s in indented.splitlines() if s.strip()])


def ReplaceLineInFile(fileName, sourceText, replaceText):
    file = open(fileName, 'r')  # Opens the file in read-mode
    text = file.read()  # Reads the file and assigns the value to a variable
    file.close()  # Closes the file (read session)
    file = open(fileName, 'w')  # Opens the file again, this time in write-mode
    file.write(text.replace(sourceText, replaceText))  # replaces all instances of our keyword
    # and writes the whole output when done, wiping over the old contents of the file
    file.close()  # Closes the file (write session)
    print (Fore.GREEN + fileName, 'All went well, the modifications are done' + Fore.WHITE)
    sg.Print(f'{fileName} All went well, the modifications are done', text_color='light green', background_color='grey20')
    main_output.append('All went well, the modifications are done\n')
    #-------------UI
    well_done_modif()
    #-------------

#---------------------------------------------------------
def createSkinFileAccesorise(file, folder_skin, variation_name):
    print ("folder_skinfolder_skin", folder_skin)
    sg.Print(f"folder_skinfolder_skin {folder_skin}", background_color='grey20')
    main_output.append(f"folder_skinfolder_skin {folder_skin}\n")
    print (file)
    sg.Print(file, background_color='grey20')
    main_output.append(file)
    print (Fore.YELLOW + variation_name + Fore.WHITE)
    sg.Print(variation_name, text_color='yellow', background_color='black')
    main_output.append(variation_name)
    print (os.path.join(folder_skin, file.replace(variation_name, '')[:-1] + '.xml'))
    original_accessorise_full = os.path.join(folder_skin, file.replace(variation_name, '')[:-1] + '.xml')
    sg.Print (os.path.join(folder_skin, file.replace(variation_name, '')[:-1] + '.xml'))
    original_accessorise_full = os.path.join(folder_skin, file.replace(variation_name, '')[:-1] + '.xml', background_color='grey20')

    if os.path.exists(original_accessorise_full):
        original_accessorise = file.split('_')[0]
        new_file = original_accessorise_full.replace(original_accessorise, file)
        shutil.copyfile(original_accessorise_full, new_file)
        ReplaceLineInFile(new_file, '"' + original_accessorise + '"', '"' + file + '"')
        tree = ET.parse(new_file)
        root = tree.getroot()
        skins = ET.SubElement(root, 'skins')
        material = ET.SubElement(skins, 'material', name=file.split('_')[1])
        with open(folder_skin + '\\' + file + '.xml', 'wt') as f:
            f.write(pretty_print(root))

    else:
        print (Fore.BLUE + 'Folder with original Accesorise is not exist' + Fore.WHITE)
        sg.Print('Folder with original Accesorise is not exist', text_color='light blue', background_color='grey20')
        main_output.append('Folder with original Accesorise is not exist\n')
#--------------------------------------------------------

def check_TextureUpper(file, extension):
    if ''.join(file.split('/')[-1].split('.')[0].split('_')[-1:]).isupper() != True:
        file_folder = '/'.join(file.split('/')[:-1]) + '/'
        file_name_new = '_'.join(file.split('_')[:-1]) + '_' + file.split('_')[-1].split('.')[0].upper() + '.dds'
        if extension == 'dds':
            os.rename(file, file_name_new)
            print (Fore.BLUE +'RENAMED: ', file, 'TO', file_name_new + Fore.WHITE)
            sg.Print(f'RENAMED: {file} TO {file_name_new}', text_color='yellow', background_color='grey20')
            main_output.append(f"RENAMED: {file} TO {file_name_new}\n")


def check_TP(file, extension):
    if extension == 'tif' or extension == 'dds' or extension == 'psd':
        if file.endswith(extension):
            check_TextureUpper(file, extension)
            if '_tp' in file:
                if not file.replace('_' + file.split('_')[-1], '').endswith('_tp'):
                    # print 'ERROR!!!', file, "contain wrong naming! _tp should be in the end of the filename and before the name of the mask"
                    collectErrors(
                        f"ERROR! {file} contain wrong naming! _tp should be in the end of the filename and before the name of the mask")
                    sg.Print(f"ERROR! {file} contain wrong naming! _tp should be in the end of the filename and before the name of the mask", text_color='red', background_color='grey20')

def checkNaming(file_list):
    for files in file_list:
        check_TP(files, 'mtl')
        check_TP(files, 'tif')
        check_TP(files, 'dds')
        check_TP(files, 'psd')


def readMTL(res_list):
    # checking inside mtl file. Parsing strings with textures and check there existing
    print (Fore.BLUE + "Checking existing textures" + Fore.WHITE)
    sg.Print("Checking existing textures", text_color='#1877b6', background_color='grey20')
    main_output.append("Checking existing textures\n")
    for elems in res_list:
        reading = open(elems, 'r').readlines()
        for strings in reading:
            if 'Texture Map=' in strings:
                clear_strings = path_skin + '/' + strings.split('File="')[1].split('"')[0]
                if '_ddn.tif' not in clear_strings:
                    if os.path.isfile(clear_strings):
                        # print 'Warning!!! Contain original NormalMap. Contact with LeadArt, is it ok?\n', elems, clear_strings
                        continue
                    elif os.path.isfile(root + '/' + 'Game' + clear_strings.split('Game/')[1]):
                        continue
                    elif os.path.isfile(root + '/' + 'Game' + clear_strings.split('Game/')[1].replace('.tif', '.dds')):
                        message = "Warning. TIF file is empty, but DDS is exist:", root + '/' + 'Game' + \
                                                                               clear_strings.split('Game/')[1].replace(
                                                                                   '.tif', '.dds')
                        print (Fore.RED + message + Fore.WHITE)
                        sg.Print(message, text_color='red', background_color='grey20')
                        main_output.append(f'{message}\n')
                    else:
                        collectErrors(
                            f"ERROR! File: {elems} Empty files {clear_strings}")
                        sg.Print(f"ERROR! File: {elems} Empty files {clear_strings}", text_color='red', background_color='grey20')

def checkMTL(mtl_file, original_name, variation_name):
    # checking mtl file. If we have skin variation, it's mean, that mtl file should have _skinName.
    print (Fore.BLUE + "Checking naming *mtl files for skin variation" + Fore.WHITE)
    sg.Print("Checking naming *mtl files for skin variation", text_color='#1877b6', background_color='grey20')
    main_output.append("Checking naming *mtl files for skin variation\n")
    for elems in mtl_file:
        if variation_name == original_name + '.mtl':
            collectErrors(f"Error! Contain default name. Need rename resource: {mtl_file}")
            sg.Print(f"Error! Contain default name. Need rename resource: {mtl_file}", text_color='red', background_color='grey20')
        elif variation_name == original_name + '_tp.mtl':
            collectErrors(f"Error! Contain default name. Need rename resource: {mtl_file}")
            sg.Print(f"Error! Contain default name. Need rename resource: {mtl_file}", text_color='red', background_color='grey20')


def collectErrors(message):
    contain_error = message
    if contain_error not in errors:
        errors.append(f'{contain_error}')


def choiseWeaponType(files, repo):
    attach_patterns = []
    for file in files:
        if not file.endswith('_tp.mtl') and not file.endswith('_d.mtl') and not re.search('sa[0-9]{0,2}.mtl', file):
            message = 'Which weapon your new gun based on? (Example : shg08)'
            print (Fore.YELLOW + message + Fore.WHITE)
            sg.Print(message, text_color='orange', background_color='grey20')
            main_output.append('Which weapon your new gun based on? (Example : shg08)\n')
            
            #-----------------------UI
            gui_item = file.replace('/','\\').split('\\')[-1].split('.')[0]
            parent_gun = base_for_weapon(gui_item)
            #-----------------------

            if file.replace('/','\\').split('\\')[-1].startswith('ar') or file.split('/')[-1].startswith('mg'):
                weapon_type = 'Assault_Rifles'
            elif file.replace('/','\\').split('\\')[-1].startswith('kn'):
                weapon_type = 'Knives'
            elif file.replace('/','\\').split('\\')[-1].startswith('pt'):
                weapon_type = 'Pistols'
            if file.replace('/','\\').split('\\')[-1].startswith('shg'):
                weapon_type = 'Shotguns'
            elif file.replace('/','\\').split('\\')[-1].startswith('smg'):
                weapon_type = 'Smg'
            elif file.replace('/','\\').split('\\')[-1].startswith('sr'):
                weapon_type = 'Sniper_Rifles'
            try:
                weapon_pattern = os.path.join(repo, 'Game/Objects/Weapons', parent_gun, parent_gun + '.xml')
            except FileNotFoundError:
                print(Fore.RED + 'There is no such parent gun ' + parent_gun + Fore.WHITE)
                sg.Print(f'There is no such parent gun {parent_gun}', text_color='red')
                main_output.append(f'There is no such parent gun {parent_gun}\n')
                
                #---------UI
                no_parent_gun()

                choiseWeaponType(files, repo)
            new_gun = file.replace('mtl','xml')
        elif file.endswith('_d.mtl'):
            d_attach_pattern = (file.replace('/','\\').replace(path_skin.replace('\\Game',''), repo)
                               .replace(file.replace('/','\\').split('\\')[-1].split('_')[0], parent_gun)).replace('.mtl','.xml')
            attach_patterns.append(d_attach_pattern)
    return weapon_type, parent_gun, weapon_pattern, new_gun, attach_patterns


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


# def setRarity(item):
# 
    # -------------UI
    # rarityButt(item)
    # ask_rarity = f"Please choose the rarity for {item} : Common; Uncommon; Rare; Epic; Legendary\n"
    # choice = input(ask_rarity)
    # 
    # main_output.append(ask_rarity)
    # rarities = {
        # "1": "common",
        # "2": "uncommon",
        # "3": "rare",
        # "4": "epic",
        # "5": "legendary",
    # }
    # if choice in rarities:
        # return rarities[choice]
    # exit(1)


def adding_new_weapon(weapon_objects, repo, skin_path):

            #------------------------------------------------------------------------------------------
            #                                   Game/Objects/Weapons
            #------------------------------------------------------------------------------------------ 
    weapon_data = choiseWeaponType(weapon_objects, repo)
    parent_gun = weapon_data[1]
    weapon_pattern = weapon_data[2]
    new_object_weapon = weapon_data[3]
    attach_patterns = weapon_data[4]
    new_gun = new_object_weapon.replace('/','\\').split('\\')[-1].replace('.xml','')
    weapon_root = ET.parse(weapon_pattern).getroot()
    weapon_root.attrib['name'] = new_gun
    weapon_root.find('geometry').find('firstperson').attrib['name'] = new_object_weapon.split('Game/')[1].replace('xml','chr') 
    weapon_root.find('geometry').find('thirdperson').attrib['name'] = new_object_weapon.split('Game/')[1].replace('.xml','_tp.cgf')
    for helper in weapon_root.find('helpers').findall('helper'):
        if helper.attrib['name'].startswith(parent_gun):
            for weapon_object in weapon_objects:
                if (helper.attrib['name'].replace(parent_gun, '') == (weapon_object.replace('/','\\').split('\\')[-1]
                    .replace('.mtl','').replace(new_gun,''))):
                    helper.attrib['name'] = helper.attrib['name'].replace(parent_gun, new_gun)
    for material in weapon_root.find('materials').findall('material'):
        weapon_root.find('materials').remove(material)
    def_material = ET.SubElement(weapon_root.find('materials'), 'material', name="default", 
                                file=new_object_weapon.split('Game/')[1].replace('xml','mtl'), tpfile=new_object_weapon.split('Game/')[1].replace('.xml','_tp.mtl'))
    with open(new_object_weapon, 'wt') as f:
        f.write(pretty_print(weapon_root))
    try:
        shutil.copyfile(new_object_weapon, os.path.join(repo, 'Game') + new_object_weapon.lower().split('game')[1])
    except FileNotFoundError:
        os.makedirs((os.path.join(repo, 'Game') + new_object_weapon.lower().split('game')[1]).replace((os.path.join(repo, 'Game') + new_object_weapon.lower().split('game')[1]).replace('/','\\').split('\\')[-1],''))
        shutil.copyfile(new_object_weapon, os.path.join(repo, 'Game') + new_object_weapon.lower().split('game')[1])
    for attach_pattern in attach_patterns:
        for weapon_object in weapon_objects:
            if (attach_pattern.replace('/','\\').split('\\')[-1].replace(parent_gun, '').replace('.xml','') == weapon_object.replace('/','\\').split('\\')[-1]
                .replace('.mtl','').replace(new_gun,'')):
                attach_root = ET.parse(attach_pattern).getroot()
                attach_root.attrib['name'] = weapon_object.replace('/','\\').split('\\')[-1].replace('.mtl','')
                attach_root.find('geometry').find('firstperson').attrib['name'] = weapon_object.split('Game/')[1].replace('mtl','cgf') 
                attach_root.find('geometry').find('thirdperson').attrib['name'] = weapon_object.split('Game/')[1].replace('.mtl','_tp.cgf')
                attach_root.find('helpers').find('helper').attrib['name'] = weapon_object.replace('/','\\').split('\\')[-1].replace('.mtl','')
                for material in attach_root.find('materials').findall('material'):
                    if material.attrib['name'] != 'default':
                        attach_root.find('materials').remove(material)
                attach_root.find('materials').find('material').attrib['name'] = 'default'
                attach_root.find('materials').find('material').attrib['file'] = weapon_object.split('Game/')[1]
                attach_root.find('materials').find('material').attrib['tpfile'] = weapon_object.split('Game/')[1].replace('.mtl','_tp.mtl')
                if os.path.isfile(weapon_object.replace('mtl','xml')):
                    os.remove(weapon_object.replace('mtl','xml'))
                with open(weapon_object.replace('mtl','xml'), 'wt') as f:
                    f.write(pretty_print(attach_root))
    chrparams_pattern = weapon_pattern.replace('xml','chrparams')
    new_chrparams = new_object_weapon.replace('xml','chrparams')
    print(Fore.BLUE + 'Cloning .chrparams' + Fore.WHITE)
    sg.Print('Cloning .chrparams', text_color='blue', background_color='grey20')
    main_output.append('Cloning .chrparams')
    chrparams_root = ET.parse(chrparams_pattern).getroot()
    for animation in chrparams_root.find('AnimationList').findall('Animation'):
        if re.search(parent_gun, animation.attrib['path']):
            animation.attrib['path'] = animation.attrib['path'].replace(parent_gun, new_gun)
            if not os.path.isfile(os.path.join(skin_path, animation.attrib['path'])):
                ascendancy = animation.attrib['path']
                print(Fore.RED + 'Warning! There are no new aimations here ' + ascendancy + Fore.WHITE)
                sg.Print(f'Warning! There are no new aimations here {ascendancy}', text_color='red', background_color='grey20')
                main_output.append(f'Warning! There are no new aimations here {ascendancy}')
                
                #---------------------UI
                no_new_animations(ascendancy)

    if os.path.isfile(new_chrparams):
        os.remove(new_chrparams)
    with open(new_chrparams, 'wt') as f:
        f.write(pretty_print(chrparams_root))

            #------------------------------------------------------------------------------------------
            #                                   Game/Items/Weapons
            #------------------------------------------------------------------------------------------ 
    item_pattern = weapon_pattern.replace('Objects', 'Items').replace(parent_gun,'').replace('.xml','') + parent_gun + '.xml'
    if not parent_gun.startswith('kn'):
        shop_pattern = weapon_pattern.replace('Objects', 'Items').replace(parent_gun,'').replace('.xml','') + parent_gun + '_shop.xml'
        shop_root = ET.parse(shop_pattern).getroot()
        new_shop = new_object_weapon.replace('Objects', 'Items').replace(new_gun,'').replace('.xml','') + new_gun + '_shop.xml'
        shop_root.attrib['name'] = shop_root.attrib['name'].replace(parent_gun, new_gun)
        for element in shop_root.find('UI_stats').findall('param'):
            element.attrib['value'] = element.attrib['value'].replace(parent_gun, new_gun)
        for element in shop_root.find('content').findall('item'):
            element.attrib['name'] = element.attrib['name'].replace(parent_gun, new_gun)
        shop_root.remove(shop_root.find('skin_content'))
        try:
            with open(new_shop, 'wt') as f:
                f.write(pretty_print(shop_root))
        except FileNotFoundError:
            os.makedirs(new_item.replace(new_item.replace('/','\\').split('\\')[-1],''))
            with open(new_shop, 'wt') as f:
                f.write(pretty_print(shop_root))
    item_root = ET.parse(item_pattern).getroot()
    new_item = new_object_weapon.replace('Objects', 'Items').replace(new_gun,'').replace('.xml','') + new_gun + '.xml'
    item_root.attrib['name'] = new_gun
    item_root.attrib['view_settings'] = item_root.attrib['view_settings'].replace(parent_gun, new_gun)
    for material in item_root.find('skins').findall('material'):
        if not material.attrib['name'] == 'default':
            item_root.find('skins').remove(material)
    if not parent_gun.startswith('kn'):
        item_root.find('icons').find('ui_icon').attrib['name'] = new_gun
        item_root.find('drop_params').find('item').attrib['name'] = new_gun
        item_root.find('icons').find('combatlog').attrib['icon'] = new_gun + '_combatLog'
    else:
        item_root.find('icons').find('weaponpanel').attrib['icon'] = new_gun + '_combatLog'
        try:
            item_root.remove(item_root.find('skin_content'))
        except:
            pass
        for stat in item_root.find('UI_stats').findall('param'):
            stat.attrib['value'] = stat.attrib['value'].replace(parent_gun, new_gun)
        item_root.find('icons').find('combatlog').attrib['melee'] = new_gun + '_combatLog'
        item_root.find('content').find('item').attrib['name'] = new_gun
    for socket in item_root.find('sockets').findall('socket'):
        for support in socket.findall('support'):
            if support.attrib['name'].startswith(parent_gun) or support.attrib['helper'].startswith(parent_gun):
                support.attrib['name'] = support.attrib['name'].replace(parent_gun, new_gun)
                support.attrib['helper'] = support.attrib['helper'].replace(parent_gun, new_gun)
    if os.path.isfile(new_item):
        os.remove(new_item)
    try:
        with open(new_item, 'wt') as f:
            f.write(pretty_print(item_root)) 
    except FileNotFoundError:
        os.makedirs(new_item.replace(new_item.replace('/','\\').split('\\')[-1],''))
        with open(new_item, 'wt') as f:
            f.write(pretty_print(item_root))
    shutil.copyfile(new_item, os.path.join(repo, 'Game') + new_item.lower().split('game')[1])

            #------------------------------------------------------------------------------------------
            #                                   Game/Items/Accesories
            #------------------------------------------------------------------------------------------
    for attach_pattern in attach_patterns:
        attach_item_pattern = (attach_pattern.replace('Objects', 'Items').replace('Weapons', 'Accessories').replace(attach_pattern.replace('/','\\').split('\\')[-1],'')
                                .replace(parent_gun,'') + attach_pattern.replace('/','\\').split('\\')[-1]).replace('\\\\','\\')
        new_attach_file = attach_item_pattern.replace(repo + '\\Game', skin_path).replace(parent_gun, new_gun)
        new_attach = attach_pattern.replace('/','\\').split('\\')[-1].replace('.xml','').replace(parent_gun, new_gun)
        attach_root = ET.parse(attach_item_pattern).getroot()
        attach_root.attrib['name'] = new_attach
        attach_root.attrib['view_settings'] = attach_item_pattern.split('Game/')[1].replace(parent_gun, new_gun)
        attach_root.find('drop_params').find('item').attrib['name'] = new_attach
        attach_root.find('types').find('type').attrib['name'] = new_attach
        attach_root.find('types').find('type').attrib['helper'] = new_attach
        try:
            with open(new_attach_file, 'wt') as f:
                f.write(pretty_print(attach_root)) 
        except FileNotFoundError:
            os.makedirs(new_attach_file.replace(new_attach_file.replace('/','\\').split('\\')[-1],''))
            with open(new_attach_file, 'wt') as f:
                f.write(pretty_print(attach_root)) 
        

def modifyItemXML(xml, mode, node_value, file_image=None, tpfile_image=None, pos=None, size=None):
    print(Fore.CYAN + 'Placeholder modifyItemXML' + Fore.WHITE)
    sg.Print('Placeholder modifyItemXML', text_color='orange', background_color='grey20')
    main_output.append('Placeholder modifyItemXML\n')


def makeVariation_object(repo, variation_name, weapon_objects, weapon_folder):
    object_list = []
    weapon_xml = os.path.join(repo, 'Game\Objects\Weapons', weapon_folder, weapon_folder + '.xml')
    object_root = ET.parse(weapon_xml).getroot()
    for weapon_object in weapon_objects:
        if weapon_object.replace('/','\\').split('\\')[-1].startswith(weapon_folder + '_' + variation_name + '.mtl'):
            for element in object_root.find('materials').findall('material'):
                if element.attrib['name'] == variation_name:
                    object_root.find('materials').remove(element)
            new_material = ET.SubElement(object_root.find('materials'), 'material', name = variation_name, 
                                        file = weapon_object.split('Game/')[1], tpfile = weapon_object.split('Game/')[1].replace('.mtl','_tp.mtl'))
            with open(weapon_xml.replace('Game','').replace(repo, path_skin), 'wt') as f:
                f.write(pretty_print(object_root))                                      
        elif re.search('sa[0-9]{0,2}', weapon_object):
            new_helper = lambda a : ET.SubElement(a.find('helpers'), 'helper', angles="0.000,-0.000,0.000",
                                        bone="weapon", offset="0.00000,0.00000,0.00000", 
                                        name = weapon_folder + '_' + variation_name + '_sa'  + 
                                                weapon_object.replace('/','\\').split('\\')[-1].split('_')[2].replace('sa','').replace('.mtl','') + '_slot')
            try:
                for element in object_root.find('helpers').findall('helper'):
                    if element.attrib['name'] == (weapon_folder + '_' + variation_name + '_saslot' +
                                                weapon_object.replace('/','\\').split('\\')[-1].split('_')[2].replace('sa','').replace('.mtl','')):
                        object_root.find('helpers').remove(element)
                new_helper(a=object_root)
            except AttributeError:
                helpers = ET.SubElement(object_root, 'helpers')
                new_helper(a=object_root)            
            sa_xml_pattern = os.path.join(repo, 'Game/Objects/Weapons/ar02/ar02_winter01_console_sa01.xml')
            sa_xml = weapon_object.replace('mtl','xml')           
            sa_xml_root = ET.parse(sa_xml_pattern).getroot()
            sa_xml_root.attrib['name'] = weapon_object.replace('/','\\').split('\\')[-1].replace('.mtl','')
            sa_xml_root.find('geometry').find('firstperson').attrib['name'] = weapon_object.split('Game/')[1].replace('mtl','cgf') 
            sa_xml_root.find('geometry').find('thirdperson').attrib['name'] = weapon_object.split('Game/')[1].replace('.mtl','_tp.cgf')
            sa_xml_root.find('helpers').find('helper').attrib['name'] = weapon_object.split('Game/')[1].replace('.mtl','_slot').split('/')[-1]
            sa_xml_root.find('materials').find('material').attrib['name'] = variation_name
            sa_xml_root.find('materials').find('material').attrib['file'] = weapon_object.split('Game/')[1]
            sa_xml_root.find('materials').find('material').attrib['tpfile'] = weapon_object.split('Game/')[1].replace('.mtl','_tp.mtl')
            if os.path.isfile(sa_xml):
                os.remove(sa_xml)
            with open(sa_xml, 'wt') as f:
                f.write(pretty_print(sa_xml_root))
            with open(weapon_xml.replace('Game','').replace(repo, path_skin), 'wt') as f:
                f.write(pretty_print(object_root))



def createSkinFile(repo, weapon_objects, variation_name, weapon_folder):    
    file_list = []
    for weapon_object in weapon_objects:
        if weapon_object.replace('/','\\').split('\\')[-1].split('_')[1].endswith('.mtl'):
            original_weapon = os.path.join(repo, 'Game\\Items\\Weapons\\', weapon_object.replace('/','\\').split('\\')[-1].split('_')[0] + '.xml')
            root = ET.parse(original_weapon).getroot()
            for element in root.find('skins').findall('material'):
                if element.attrib['name'] == variation_name:
                    root.find('skins').remove(element)
            new_skin = ET.SubElement(root.find('skins'), 'material', name = variation_name)
            with open(original_weapon.replace(repo, path_skin.replace('Game','')), 'wt') as f:
                f.write(pretty_print(root))
            #------------------------------------------------------------------------------------------
            #                                           Skin
            #------------------------------------------------------------------------------------------
            for material in root.find('skins').findall('material'):
                find_skin = os.path.join(repo, 'Game\\Items\\Weapons\\', 
                                            weapon_object.replace('/','\\').split('\\')[-1].split('_')[0] + '_' + 
                                            material.get('name') + '.xml')
                if os.path.isfile(find_skin):
                    skin_pattern = find_skin
                    break
                else:
                    continue
            try:
                skin_root = ET.parse(skin_pattern).getroot() 
                skin_root.attrib['name'] = weapon_folder + '_' + variation_name
                if not weapon_object.replace('/','\\').split('\\')[-1].startswith('kn'):
                    skin_root.find('icons').find('ui_icon').attrib['name'] = weapon_folder + '_' + variation_name
                    skin_root.find('drop_params').find('item').attrib['name'] = weapon_folder + '_' + variation_name
                skin_root.find('skins').find('material').attrib['name'] = variation_name
                if os.path.isfile(os.path.join(repo, 'Game\\Items\\Weapons\\', weapon_folder + '_' + variation_name + '.xml')):
                    os.remove(os.path.join(repo, 'Game\\Items\\Weapons\\', weapon_folder + '_' + variation_name + '.xml'))
                with open(os.path.join(path_skin, 'Items\\Weapons\\', weapon_folder + '_' + variation_name + '.xml'), 'wt') as f:
                    f.write(pretty_print(skin_root))

            #------------------------------------------------------------------------------------------
            #                                         Skin shop
            #------------------------------------------------------------------------------------------
                if not weapon_object.replace('/','\\').split('\\')[-1].startswith('kn'):
                    for material in root.find('skins').findall('material'):
                        find_skin_shop = os.path.join(repo, 'Game\\Items\\Weapons\\', 
                                                weapon_object.replace('/','\\').split('\\')[-1].split('_')[0] + '_' + 
                                                material.get('name') + '_shop' + '.xml')
                        if os.path.isfile(find_skin_shop):
                            skin_pattern_shop = find_skin_shop  
                            break                  
                        else:
                            continue
                    skin_shop_root = ET.parse(skin_pattern_shop).getroot() 
                    skin_shop_root.attrib['name'] = weapon_folder + '_' + variation_name + '_shop'
                    for element in skin_shop_root.find('UI_stats').findall('param'):
                        if element.attrib['name'] == "name":
                            element.attrib['value'] = "@" + weapon_folder + '_' + variation_name +"_shop_name"
                        elif element.attrib['name'] == "description":
                            element.attrib['value'] = "@ui_weapons_" + weapon_folder + '_' + variation_name
                        elif element.attrib['name'] == "icon":
                            element.attrib['value'] = weapon_folder + '_' + variation_name
                        elif element.attrib['name'] == "rarity":
                            rarity = rarityButt(weapon_folder + '_' + variation_name)
                            element.attrib['value'] = rarity
                    try:
                        skin_shop_root.find('content').find('item').attrib['name'] = weapon_folder + '_' + variation_name
                    except AttributeError:
                        continue
                    if os.path.isfile(os.path.join(repo, 'Game\\Items\\Weapons\\', weapon_folder + '_' + variation_name + '_shop.xml')):
                        os.remove(os.path.join(repo, 'Game\\Items\\Weapons\\', weapon_folder + '_' + variation_name + '_shop.xml'))
                    with open(os.path.join(path_skin, 'Items\\Weapons\\', weapon_folder + '_' + variation_name + '_shop.xml'), 'wt') as f:
                        f.write(pretty_print(skin_shop_root))

            #------------------------------------------------------------------------------------------
            #                                       Pattern
            #------------------------------------------------------------------------------------------
                for material in root.find('skins').findall('material'):
                        find_pattern_skin_shop = os.path.join(repo, 'Game\\Items\\Weapons\\', 
                                                weapon_object.replace('/','\\').split('\\')[-1].split('_')[0] + '_' + 
                                                material.get('name') + 'skin_shop' + '.xml')
                        if os.path.isfile(find_pattern_skin_shop):
                            skin_pattern_skin_shop = find_pattern_skin_shop  
                            break                  
                        else:
                            continue
                skin_pattern_skin_shop_root = ET.parse(skin_pattern_skin_shop).getroot() 
                skin_pattern_skin_shop_root.attrib['name'] = weapon_folder + '_' + variation_name + 'skin_shop'
                for element in skin_pattern_skin_shop_root.find('UI_stats').findall('param'):
                    if element.attrib['name'] == "name":
                        element.attrib['value'] = "@" + weapon_folder + '_' + variation_name +"skin_shop_name"
                    elif element.attrib['name'] == "description":
                        element.attrib['value'] = "@" + weapon_folder + '_' + variation_name + 'skin_shop'
                    elif element.attrib['name'] == "icon":
                        element.attrib['value'] = weapon_folder + '_' + variation_name
                for element in skin_pattern_skin_shop_root.find('skin').findall('param'):
                    if element.attrib['name'] == "thumbnail_icon":
                        element.attrib['value'] = weapon_folder + '_' + variation_name +"__thumbnail"
                    elif element.attrib['name'] == "material":
                        element.attrib['value'] = variation_name
                if os.path.isfile(os.path.join(repo, 'Game\\Items\\Weapons\\', weapon_folder + '_' + variation_name + 'skin_shop.xml')):
                    os.remove(os.path.join(repo, 'Game\\Items\\Weapons\\', weapon_folder + '_' + variation_name + 'skin_shop.xml'))
                with open(os.path.join(path_skin, 'Items\\Weapons\\', weapon_folder + '_' + variation_name + 'skin_shop.xml'), 'wt') as f:
                    f.write(pretty_print(skin_pattern_skin_shop_root))

            #------------------------------------------------------------------------------------------
            #                                       Shop xml
            #------------------------------------------------------------------------------------------
                if not weapon_object.replace('/','\\').split('\\')[-1].startswith('kn'):
                    shop = os.path.join(repo, 'Game\\Items\\Weapons\\', 
                                                weapon_object.replace('/','\\').split('\\')[-1].split('_')[0] + '_shop' + '.xml')   
                    shop_root = ET.parse(shop).getroot()
                    for element in shop_root.find('skin_content').findall('item'):
                        if element.attrib['name'] == weapon_folder + '_' + variation_name + 'skin_shop.xml':
                            shop_root.find('skin_content').remove(element)
                    New_skin = ET.SubElement(shop_root.find('skin_content'), 'item', name = weapon_folder + '_' + variation_name + 'skin_shop.xml')
                    with open(os.path.join(path_skin, 'Items\\Weapons\\', weapon_folder + '_shop.xml'), 'wt') as f:
                        f.write(pretty_print(shop_root))  
            except UnboundLocalError:
                print (Fore.CYAN + 'Your weapon is new! Create your first skin directly!'+ Fore.WHITE)
                sg.Print('Your weapon is new! Create your first skin directly!', text_color='light green', background_color='grey20')
                main_output.append('Your weapon is new! Create your first skin directly!\n')
                
                your_weapon_is_new(weapon_folder)

            #------------------------------------------------------------------------------------------
            #                                       Special sockets
            #------------------------------------------------------------------------------------------
        elif re.search('sa[0-9]{0,2}', weapon_object):
            NeedNewSocket = True
            original_weapon = os.path.join(path_skin, 'Items\\Weapons\\', weapon_object.replace('/','\\').split('\\')[-1].split('_')[0] + '.xml')
            root = ET.parse(original_weapon).getroot()
            for material in root.find('skins').findall('material'):
                        if material.attrib['name'] == variation_name:
                            for element in material.findall('attach'): 
                                if element.attrib['socket'].startswith('special_socket'):
                                    material.remove(element)
                            new_skin = ET.SubElement(material, 'attach', socket = 'special_socket01')
            for element in root.find('sockets').findall('socket'):
                        if element.attrib['name'].startswith('special_socket'):
                            for i in element.findall('support'):
                                if i.attrib['name'] == weapon_object.replace('/','\\').split('\\')[-1].replace('.mtl',''):
                                    element.remove(i)
            if not weapon_object.replace('/','\\').split('\\')[-1].startswith('kn'):
                        for element in root.find('sockets').findall('socket'):
                            if element.attrib['name'].startswith('special_socket'):
                                NeedNewSocket = False
                                break
                        if NeedNewSocket == True:
                            new_socket = ET.SubElement(root.find('sockets'), 'socket', can_be_empty="0", name="special_socket01")
                            
                        for element in root.find('sockets').findall('socket'):
                            if element.attrib['name'].startswith('special_socket'):
                                new_helper = ET.SubElement(element, 'support', helper=weapon_object.replace('/','\\').split('\\')[-1].split('_')[0] + "_" + variation_name +
                                                            '_sa' + weapon_object.replace('/','\\').split('\\')[-1].split('_')[-1].replace('.mtl','').replace('sa','') + '_slot', 
                                                                name=weapon_object.replace('/','\\').split('\\')[-1].replace('.mtl',''))
                        with open(original_weapon, 'wt') as f:
                            f.write(pretty_print(root))
                        skin_pattern_shop = os.path.join(repo, 'Game\\Items\\Weapons\\', 
                                                    weapon_object.replace('/','\\').split('\\')[-1].split('_')[0] + '_' + 
                                                    (root.find('skins')[1]).get('name') + '_shop' + '.xml')   
                        skin_shop_root = ET.parse(skin_pattern_shop).getroot()
                        NewItem = ET.SubElement(skin_shop_root.find('content'), 'item', 
                                                name = weapon_object.replace('/','\\').split('\\')[-1].replace('.mtl',''))
                        with open(os.path.join(path_skin, 'Items\\Weapons\\', weapon_folder + '_' + variation_name + '_shop.xml'), 'wt') as f:
                            f.write(pretty_print(skin_shop_root))
                        shop = os.path.join(repo, 'Game\\Items\\Weapons\\', 
                                                    weapon_object.replace('/','\\').split('\\')[-1].split('_')[0] + '_shop' + '.xml')   
                        shop_root = ET.parse(shop).getroot() 
                        for element in shop_root.find('content').findall('item'):
                            if element.attrib['name'] == weapon_object.replace('/','\\').split('\\')[-1].replace('.mtl',''):
                                shop_root.find('content').remove(element)
                        New_item = ET.SubElement(shop_root.find('content'), 'item', name = weapon_object.replace('/','\\').split('\\')[-1].replace('.mtl',''))
                        with open(os.path.join(path_skin, 'Items\\Weapons\\', weapon_folder + '_shop.xml'), 'wt') as f:
                            f.write(pretty_print(shop_root))
                        file_list.append(os.path.join(repo, 'Game\\Items\\Weapons\\', weapon_folder + '_shop.xml'))

            #------------------------------------------------------------------------------------------
            #                                   Sa_items xml
            #------------------------------------------------------------------------------------------
            sa_pattern = os.path.join(repo, 'Game\\Items\\Accessories\\', 'smg46_tape01_console_sa01.xml')
            sa_root = ET.parse(sa_pattern).getroot()
            sa_root.attrib['name'] = weapon_object.replace('/','\\').split('\\')[-1].replace('.mtl','')
            sa_root.attrib['view_settings'] = ('Objects/Weapons/' + weapon_object.replace('/','\\').split('\\')[-1].split('_')[0]
                                                + '/' + weapon_object.replace('/','\\').split('\\')[-1].replace('.mtl','.xml'))
            for element in sa_root.find('drop_params').findall('item'):
                element.attrib['name'] = weapon_object.replace('/','\\').split('\\')[-1].replace('.mtl','')
            for element in sa_root.find('types').findall('type'):
                element.attrib['name'] = weapon_object.replace('/','\\').split('\\')[-1].replace('.mtl','')
                element.attrib['helper'] = weapon_object.replace('/','\\').split('\\')[-1].replace('.mtl','') + '_slot'
            if os.path.isfile(os.path.join(repo, 'Game\\Items\\Accessories\\', weapon_object.replace('/','\\').split('\\')[-1].replace('.mtl','.xml'))):
                os.remove(os.path.join(repo, 'Game\\Items\\Accessories\\', weapon_object.replace('/','\\').split('\\')[-1].replace('.mtl','.xml')))
            with open(os.path.join(path_skin, 'Items\\Accessories\\', weapon_object.replace('/','\\').split('\\')[-1].replace('.mtl','.xml')), 'wt') as f:
                f.write(pretty_print(sa_root))

            #------------------------------------------------------------------------------------------
            #                                   default attachments
            #------------------------------------------------------------------------------------------
        elif weapon_object.replace('/','\\').split('\\')[-1].endswith('_d.mtl'):
            d_attach = os.path.join(repo, 'Game\\Items\\Accessories\\', 
                                    weapon_object.replace('/','\\').split('\\')[-1].replace('_' + variation_name,'')
                                    .replace('.mtl','.xml'))
            d_attach_root = ET.parse(d_attach).getroot()
            try:
                for material in d_attach_root.find('skins').findall('material'):
                    if material.attrib['name'] == variation_name:
                        d_attach_root.find('skins').remove(material)
            except AttributeError:
                new_skins = ET.SubElement(d_attach_root, 'skins')
            New_skin = ET.SubElement(d_attach_root.find('skins'), 'material', name = variation_name)
            with open(d_attach.replace('Game','').replace(repo, path_skin), 'wt') as f:
                f.write(pretty_print(d_attach_root))


def searchWeaponObjects(mtl_list):
    weapon_objects = []
    for mtl in mtl_list:
        try:
            if mtl.endswith('_is_d.mtl'):
                weapon_objects.append(mtl)
            elif (re.search('_sa[0-9]{0,2}', mtl) and not mtl.endswith('_tp.mtl')):
                weapon_objects.append(mtl)
            elif mtl.endswith('sp_d.mtl'):
                weapon_objects.append(mtl)
            elif mtl.endswith('rds_d.mtl'):
                weapon_objects.append(mtl)
            elif mtl.endswith('ss_d.mtl'):
                weapon_objects.append(mtl)
            elif mtl.endswith('gp_d.mtl'):
                weapon_objects.append(mtl)
            elif mtl.endswith('as_d.mtl'):
                weapon_objects.append(mtl)
            elif mtl.endswith('sc_d.mtl'):
                weapon_objects.append(mtl)
            elif mtl.endswith('ugl_d.mtl'):
                weapon_objects.append(mtl)
            elif mtl.endswith('clip_d.mtl'):
                weapon_objects.append(mtl)
            elif mtl.endswith('bp_d.mtl'):
                weapon_objects.append(mtl)
            elif mtl.replace('/','\\').split('\\')[-1].split('_')[1].endswith('.mtl'):
                weapon_objects.append(mtl)
        except IndexError:
            weapon_objects.append(mtl)
    return weapon_objects


def preparing_objects(weapon_objects, variation_name_list):
    temp_list = []
    for variation_name in variation_name_list:
        for weapon_object in weapon_objects:
            weapon_object = weapon_object.replace('_' + variation_name,'')
            temp_list.append(weapon_object)
    return temp_list


def getResources(path, repo):

            #------------------------------------------------------------------------------------------
            #                                   Skin item file
            #------------------------------------------------------------------------------------------
    temp_list = []
    objects = os.path.join(path, 'Objects/Weapons')
    attachments = os.path.join(path, 'Objects/Attachments')
    icons = path + '/Libs/Icons/Weapons'
    skin_attachments = (path + '/Items/Accessories') 
    for files in os.listdir(objects):
        mtl_list = []
        mtl_fp_list = []
        textures_list = []
        print (Fore.YELLOW + 'Weapon folder:' + Fore.WHITE, files)
        sg.Print(f'Weapon folder: {files}', text_color='white', background_color='black')
        main_output.append(f'Weapon folder: {files}\n')

        variation_name_list = []
        for resources in walkfolder(objects + '/' + files, ''):
            if resources.endswith('.mtl'):
                mtl_list.append(resources)
                if resources.endswith('mtl') and not resources.endswith('_tp.mtl') and not resources.endswith('_d.mtl') and not re.search('sa[0-9]{0,2}.mtl', resources):
                    try:
                        if '_' in resources:
                            item_variation = resources.split('/')[-1].split('_')[1].split('.')[0]
                            print (Fore.YELLOW + 'Variation_name:', item_variation + Fore.WHITE)
                            sg.Print(f'Variation_name: {item_variation}', text_color='orange', background_color='grey20')
                            main_output.append(f'Variation_name: {item_variation}\n')
                            variation_name_list.append(item_variation)
                        elif 'kn43_vdv' in resources:
                            item_variation = resources.split('/')[-1].split(files + '_')[1].split('.mtl')[0]
                            print (Fore.YELLOW + 'Variation_name:', item_variation + Fore.WHITE)
                            sg.Print(f'Variation_name: {item_variation}', text_color='orange', background_color='grey20')
                            main_output.append(f'Variation_name: {item_variation}\n')
                            variation_name_list.append(item_variation)
                        else:
                            collectErrors(f"Error! Can't get valid variation {resources}")
                            sg.Print(f"Error! Can't get valid variation {resources}", text_color='red', background_color='grey20')
                            print (Fore.RED + "Error! Can't get valid variation", resources + Fore.WHITE)
                            
                            #-----------------------GUI
                            non_valid_variation(resources)

                        mtl_fp_list.append(resources)
                    except IndexError:
                        continue
            if '/textures/' in resources.lower():
                textures_list.append(resources)
        weapon_objects = searchWeaponObjects(mtl_list)
        weapon_file = os.path.join(repo, 'Game/Objects/Weapons/', files, files + '.xml').replace('/','\\')
        if not os.path.isfile(weapon_file):
            if len(variation_name_list)>0:
                new_weapon_objects = preparing_objects(weapon_objects, variation_name_list)
                adding_new_weapon(new_weapon_objects, repo, path)
            else:
                adding_new_weapon(weapon_objects, repo, path)
        for elems in mtl_fp_list:
            if not os.path.isfile(elems.replace('.mtl', '_tp.mtl')):
                try:
                    
                    mtl_name01 = mtl_list[0]
                    mtl_name02 = mtl_list[1]
                    collectErrors(
                    f"Error! First person MTL name don't accordance to the Third Person MTL name: {mtl_name01}, {mtl_name02}")
                    sg.Print(f"Error! First person MTL name don't accordance to the Third Person MTL name: {mtl_name01}, {mtl_name02}", text_color='red', background_color='grey20')
                except IndexError:
                    
                    print(Fore.RED + "You haven't mtl's, which needed!" + Fore.WHITE)
                    sg.Print("You haven't mtl's, which needed!", text_color='red', background_color='grey20')
                    main_output.append("You haven't mtl's, which needed!\n")
                    collectErrors(f"MISSING mtl!        {weapon_objects}")
                    sg.Print(f"MISSING mtl! {weapon_objects} OMG!!", text_color='red', background_color='grey20')
                    
                    #---------GUI
                    missing_mtl(weapon_objects)

                    continue

        for variation_name in variation_name_list:
            if not variation_name and os.path.isdir(os.path.join(repo, 'Objects/Weapons', files)):
                print (Fore.RED + 'Can not detect variation name. Check naming of this files'+ Fore.WHITE, files, mtl_list)
                sg.Print(f'Can not detect variation name. Check naming of this files {files}, {mtl_list}', text_color='red', background_color='grey20')
                main_output.append(f'Can not detect variation name. Check naming of this files {files}, {mtl_list}')
                
                #----------------GUI
                cant_detect_var_Name(files, mtl_list)
            else:

                checkMTL(mtl_list, files, variation_name)
                readMTL(mtl_list)
                temp_list.append(files)
                print('Checking naming of the texture files')
                sg.Print('Checking naming of the texture files', text_color='#1877b6', background_color='grey20')
                main_output.append('Checking naming of the texture files\n')
                checkNaming(mtl_list)
                checkNaming(textures_list)
                print("Started modifying data...........")
                sg.Print("Started modifying data...........", text_color='#1877b6', background_color='grey20')
                sg.Print(f"Please choose the rarity for {files} : Common; Uncommon; Rare; Epic; Legendary\n", text_color='orange', background_color='grey20')
                main_output.append("Started modifying data...........\n\n"+f"Choose the rarity for {files} : Common; Uncommon; Rare; Epic; Legendary\n"+'---------'*8+"\n")                
                createSkinFile(root, weapon_objects, variation_name, files)
                makeVariation_object(root, variation_name, weapon_objects, files)

#------------------------------------------------------------------------------
#                           Game\Objects\Attachments
#------------------------------------------------------------------------------
def obj_att_func(client_att, rep_att, i, temp, mtl):

    xml = '\\' + f'{i}' + '\\' + f'{i}.xml'
    client_xml = client_att + xml
    rep_xml = rep_att + xml

    for _, _, files in os.walk(rep_att + '\\' + i):
        mtl = files
        for m in mtl:
            if '.xml' in m:
                mtl.remove(m)
            elif '_tp' in m:
                mtl.remove(m)
            else:
                pass
        break

    try:
        shutil.copyfile(client_xml, rep_xml)
    except(FileNotFoundError):
        os.makedirs(path_skin + '\Objects\Attachments\\' + f'{i}')
        shutil.copyfile(client_xml, rep_xml)

    f = open(rep_xml, 'r').readlines()
    for line in f:
        temp.append(line)
        
    for x in mtl:
        m = x.rstrip('.mtl')
        var_name = m.split('_')[1]
        tree = ET.parse(rep_xml)
        root = tree.getroot()

        item = False

        for element in root.find('materials').findall('material'):
            if element.attrib['name'] == var_name:
                item = True
        if item == True:
            continue
        else:
            ET.SubElement(root.find('materials'), 'material', name=f"{var_name}",
                        file=f"objects/attachments/{i}/{x}", tpfile=f"objects/attachments/{i}/{m}_tp.mtl")

        with open(rep_xml, 'w') as f:
            f.write(pretty_print(root))
    temp.clear()
    mtl.clear()
    
#------------------------------------------------------------------------------
def add_material_att(rep_acc_xml, skin_item, mtl):

    tree = ET.parse(rep_acc_xml)
    root = tree.getroot()

    for skin_item in mtl:
        skin_item = skin_item.split('_')[1].rstrip('.mtl')

        have_skins = False

        for _ in root.findall('skins'):
            
            have_skins = True

        if have_skins == True:
            
            for skins in root.find('skins').findall('material'):
                if skins.attrib['name'] == skin_item:
                    pass
                else:
                    ET.SubElement(root.find('skins'), 'material', name = f'{skin_item}')
        else:          
            skins = ET.SubElement(root, "skins")
            ET.SubElement(skins, "material", name = f'{skin_item}')   


        with open(rep_acc_xml, 'w') as f:
            f.write(pretty_print(root))

#------------------------------------------------------------------------------
def att_No_Skin_xml(repo_xml, item):
    tree = ET.parse(repo_xml)
    root = tree.getroot()

    old_item = root.attrib['name']
    new_item = f'{item}'

    try:
        root.attrib['name'] = root.attrib['name'].replace(old_item, new_item)
        root.attrib['view_settings'] = root.attrib['view_settings'].replace(old_item, new_item)
        for text in root.findall('description_ingame'):
            text.attrib['text'] = text.attrib['text'].replace(old_item, new_item)
        for param in root.find('UI_stats').findall('param'):
            param.attrib['value'] = param.attrib['value'].replace(old_item, new_item)
        if not repo_xml.split('\\')[-1].startswith('fl'):
            for item in root.find('content').findall('item'):
                item.attrib['name'] = item.attrib['name'].replace(old_item, new_item)
        for model in root.findall('drop_params'):
            model.attrib['model'] = model.attrib['model'].replace(old_item, new_item)
        for item in root.find('drop_params'):
            item.attrib['name'] = item.attrib['name'].replace(old_item, new_item)
        for types in root.find('types').findall('type'):
            types.attrib['name'] = types.attrib['name'].replace(old_item, new_item)
    except(NameError, KeyError):
        pass

    with open(repo_xml, 'w') as f:
        f.write(pretty_print(root))

#------------------------------------------------------------------------------
def att_Skin_xml(repo_material_xml, skin_item, item):
    tree = ET.parse(repo_material_xml)
    root = tree.getroot()

    old_skin = root.attrib['name']
    old_item = root.attrib['name'].split('_')[0]
    old_material = old_skin.split('_')[1]

    new_skin = skin_item
    new_item = f'{skin_item}'.split('_')[0]
    new_material = new_skin.split('_')[1]

    try:    
        root.attrib['name'] = root.attrib['name'].replace(old_skin, new_skin)
        root.attrib['view_settings'] = root.attrib['view_settings'].replace(old_item, new_item)
        for text in root.findall('description_ingame'):
            text.attrib['text'] = text.attrib['text'].replace(old_item, new_item)
        for skins in root.find('skins').findall('material'):
            skins.attrib['name'] = skins.attrib['name'].replace(old_material, new_material)
        for param in root.find('UI_stats').findall('param'):
            if param.attrib['name'] == 'icon':
                param.attrib['value'] = param.attrib['value'].replace(old_skin, new_skin)
            elif param.attrib['name'] == 'description':
                param.attrib['value'] = param.attrib['value'].replace(old_skin, new_skin)
            elif param.attrib['name'] == 'name':
                param.attrib['value'] = param.attrib['value'].replace(old_skin, new_skin)
        for item in root.find('content').findall('item'):
            item.attrib['name'] = item.attrib['name'].replace(old_skin, new_skin)
        for item in root.find('drop_params').findall('item'):
            item.attrib['name'] = item.attrib['name'].replace(old_skin, new_skin)
        for types in root.find('types').findall('type'):
            types.attrib['name'] = types.attrib['name'].replace(old_skin, new_skin)
        for model in root.findall('drop_params'):
            model.attrib['model'] = model.attrib['model'].replace(old_item, new_item)
    except(NameError, KeyError):
        pass

    with open(repo_material_xml, 'r+') as f:
        f.write(pretty_print(root))

#------------------------------------------------------------------------------
#                           Game\Items\Accessories
#------------------------------------------------------------------------------
def item_acc_func(rep_att):

    for _, dirs, _ in os.walk(rep_att):
        item_list = dirs
        break

    for item in item_list:
        for _, _, files in os.walk(rep_att + '\\' + item):
            mtl = files

            for m in mtl:
                if '.xml' in m:
                    mtl.remove(m)
                elif '_tp' in m:
                    mtl.remove(m)
                else:
                    pass
            break

        for m in mtl:
            skin_item = m.rstrip(".mtl")
            xml = '\\' + f'{item}.xml'
            client_acc_xml = acc_att + xml
            rep_acc_xml = rep_acc + xml
            #---------    
            raw_gun = item.rstrip('0123456789')
            os.chdir(acc_att)
            num = '2'
            for file in glob.glob(f"{raw_gun}0{num}*.xml"):
                if len(file) > 9:
                    string = file
                    xml = string.split('_')[1]
                    break
            #---------
            path = acc_att + "\\" + raw_gun + f'0{num}.xml'
            a_path = acc_att + "\\" + raw_gun + f'0{num}_' + xml
            b_path = rep_acc + "\\" + f'{skin_item}.xml'

            try:
                shutil.copyfile(client_acc_xml, rep_acc_xml)
                att_No_Skin_xml(rep_acc_xml, item)
                add_material_att(rep_acc_xml, skin_item, mtl)
                att_Skin_xml(b_path, skin_item, item)
                
            except(FileNotFoundError):
                if (not path.split('\\')[-1].startswith('fl')):
                    shutil.copyfile(path, rep_acc_xml)
                    shutil.copyfile(a_path, b_path)
                    #---------
                    att_No_Skin_xml(rep_acc_xml, item)
                    add_material_att(rep_acc_xml, skin_item, mtl)
                    att_Skin_xml(b_path, skin_item, item)
            
#------------------------------------------------------------------------------
#            Game\Objects\Attachments + Game\Items\Accessories
#------------------------------------------------------------------------------
def obj_att__vs__item_acc(client_att, rep_att):
    temp = []
    mtl = []
    for _, dirs, _ in os.walk(rep_att):
        item_list = dirs
        break

    for i in item_list:
        obj_att_func(client_att, rep_att, i, temp, mtl)
        item_acc_func(rep_att)

#------------------------------------------------------------------------------
#                   add Attachments File Structure
#------------------------------------------------------------------------------
def fileStructure(rep_att, rep_acc):
    if os.path.exists(rep_att) == True:
        pass
    else:
        os.makedirs(rep_att)
    #--------
    if os.path.exists(rep_acc) == True:
        pass
    else:
        os.makedirs(rep_acc)

#------------------------------------------------------------------------------
#                                  Good Ending
#------------------------------------------------------------------------------
def copy_files(path_skin, repo):
    
    copy = sg.popup_yes_no(
        'Should I copy resources\n       to repository?',
        no_titlebar=True,
        grab_anywhere=True,
        modal=False)

    if copy == 'Yes':
        files_to_record = walkfolder(path_skin,'')
        for k in files_to_record:
            dst = k.replace(path_skin.replace('\\', '/'), os.path.join(root.replace('\\', '/'), 'Game'))
            if not os.path.isdir(dst.replace(dst.split('/')[-1],'')):
                os.makedirs(dst.replace(dst.split('/')[-1],''))
            if not k.endswith('.psd'):
                shutil.copyfile(k, dst)
                #-----------GUI       
                if_copy_YES()
    if copy == 'No':
        #-----------UI
        if_copy_NO()
    else:
        #-----------UI
        cant_understand()
        copy_files(path_skin, repo)

#===================================================================================
#                                       UI
#===================================================================================
def Ask_Path():

    layout = [
        [sg.Text('Insert your WFC repo path', text_color='yellow')],
        [sg.InputText(
            default_text = r"c:\wf-skins-minsk",
            key = "-REPO-"),
            sg.FolderBrowse()],

        [sg.Text("Skin absolute path ('Game' folder)", text_color='yellow')],
        [sg.InputText(
            default_text = r"d:\_WFC_rep\WFC_Content_Pack_27\27_6_Weapon_Skins_Hard_Rock_x10\Game",
            key = "-SKINS-"),
            sg.FolderBrowse()],

        [sg.OK(key='OK'), sg.Cancel()]
    ]
    window = sg.Window('', layout, no_titlebar=True, grab_anywhere=True)

    while True:
        event, values = window.read(close=True)

        wfc_repo = values["-REPO-"]
        skin_repo = values["-SKINS-"]

        if event == 'OK':
            return wfc_repo, skin_repo

        if event in ('Cancel', sg.Cancel()) or event == sg.WIN_CLOSED:
            break
        
    window.close()

#----------------------------------------------------------------------------------------------------
def rarityButt(item):
    #prompt = print(f"""Please choose the rarity for item: "{item}"  \n1 - Common; 2 - Uncommon; 3 - Rare; 4 - Epic; 5 - Legendary """)
    #sg.Print(prompt, do_not_reroute_stdout=False, no_titlebar=True, text_color='green')
    weapon = item.split('_')[0]
    material = item.split('_')[1]
    layout = [

        [sg.Text('Weapon Folder: ',
            size=(20, 1)),
            sg.Text(f'{weapon}',
            text_color="#ffae00",
            size=(20, 1)),
            #sg.Text(WE.AR_weaponary[f'{weapon}'])
            ],

        [sg.HSeparator()],

        [sg.Text('Variation Name: ',
            size=(20, 1)),
            sg.Text(f'{material}',
            text_color="#ffae00")],

        [sg.HSeparator()],

        [sg.Output(key='-LOG-', background_color='black', text_color='green', size=(85, 20))],

# 
        # [sg.Multiline(main_output,
            # key='logger',
            # font=('Consolas', 10),
            # autoscroll=True,
            # size=(80, 20),
            # pad=(0, (15, 0)),
            # background_color='grey20',
            # text_color = "#3EF000",
            # do_not_clear=True,
            # disabled=True,
            # auto_refresh=True
            # focus=True
            # )],

        [sg.Text("\nPlease choose the rarity for item: " + item + "")],

        [sg.Button(
            button_text='Common',
            key='COMMON',
            size=(11, 1),
            enable_events=True,
            bind_return_key=True,
            button_color=(sg.COMMON[0], sg.BLACKED[0])),

        sg.Button(
            button_text='Uncommon',
            key='UNCOMMON',
            size=(11, 1),
            enable_events=True,
            bind_return_key=True,
            button_color=(sg.UNCOMMON[0], sg.BLACKED[0])),

        sg.Button(
            button_text='Rare',
            key='RARE',
            size=(11, 1),
            enable_events=True,
            bind_return_key=True,
            button_color=(sg.RARE[0], sg.BLACKED[0])),

        sg.Button(
            button_text='Epic',
            key='EPIC',
            size=(11, 1),
            enable_events=True,
            bind_return_key=True,
            button_color=(sg.EPIC[0], sg.BLACKED[0])),

        sg.Button(
            button_text='Legendary', 
            key='LEGENDARY',
            size=(11, 1),
            enable_events=True,
            bind_return_key=True,
            button_color=(sg.LEGENDARY[0], sg.BLACKED[0]))

        ],

        [sg.Button('EXIT')]

            ]

    window = sg.Window('Put in butt', layout, no_titlebar=True, grab_anywhere=True)

    while True:
        rarity = '0'
        event, value = window.read(close=True)

        #if event == 'logger':
        #    window.update(err)

        if event == 'COMMON':
            rarity == '1'
            sg.Print('COMMON', background_color='grey20', text_color='white')
            print('COMMON')
            return rarity
        if event == 'UNCOMMON':
            rarity == '2'
            sg.Print('UNCOMMON', background_color='grey20', text_color='white')
            print('UNCOMMON')
            return rarity
        if event == 'RARE':
            rarity == '3'
            sg.Print('RARE', background_color='grey20', text_color='white')
            print('RARE')
            return rarity
        if event == 'EPIC':
            rarity == '4'
            sg.Print('EPIC', background_color='grey20', text_color='white')
            print('EPIC')
            return rarity
        if event == 'LEGENDARY':
            rarity == '5'
            sg.Print('LEGENDARY', background_color='grey20', text_color='white')
            print('LEGENDARY')
            return rarity

        if event == 'EXIT'  or event == sg.WIN_CLOSED:      
            break
        else:
            break
    window.close()

#----------------------------------------------------------------------------------
def your_weapon_is_new(weapon):
    sg.PopupAnnoying(
        f'Your weapon {weapon} is new! Create your first skin directly!',
        text_color="light blue")

#----------------------------------------------------------------------------------
def base_for_weapon(file):
    sg.PopupGetText(f'What weapon is the base for new one {file}?',
    text_color='yellow',
    default_text=f'{file}',
    no_titlebar=True,
    grab_anywhere=True)

#----------------------------------------------------------------------------------
def no_parent_gun():
    sg.PopupAnnoying("Parent gun doesn't exist", text_color='red')

#----------------------------------------------------------------------------------
def no_new_animations(ascendancy):
    sg.PopupAnnoying(f"Warning! There are no new animations here ' {ascendancy}")

#----------------------------------------------------------------------------------
def if_copy_NO():
    sg.popup_auto_close('Whatever...',
    text_color='white',
    no_titlebar=True,
    auto_close_duration=0.5)

#----------------------------------------------------------------------------------
def if_copy_YES():
    sg.popup_auto_close('Copying some files to the repository...',
    text_color='light blue',
    no_titlebar=True, auto_close=True)

#----------------------------------------------------------------------------------
def cant_understand():
    sg.PopupAnnoying("Can't understand, \nsomething gona wrong",
        text_color='red')

#----------------------------------------------------------------------------------
def non_valid_variation(resources):
    sg.PopupError(f"Error! Can't to get valid variation {resources}")

#----------------------------------------------------------------------------------
def well_done_modif():
    sg.PopupAnnoying("All went well, the modifications are done", text_color='green')

#----------------------------------------------------------------------------------
def cant_detect_var_Name(files, mtl_list):
    sg.PopupAnnoying(f"Can't detect variation name. Check the naming of this files:\n{files}, {mtl_list}", text_color='red')

#----------------------------------------------------------------------------------
def missing_mtl(weapon_objects):
    sg.PopupAnnoying(f"There is no 'mtl' files {weapon_objects}", text_color='red')

#----------------------------------------------------------------------------------
def error_report(error_list):
    sg.Print(error_list,
        do_not_reroute_stdout=True,
        background_color='grey20',
        text_color='red',
        keep_on_top=True,
        font=('Consolas', 11),
        end='\n\n\n')

#----------------------------------------------------------------------------------
def i_am_done():
    sg.PopupAutoClose("I'am done!",
        auto_close_duration=0.5,
        no_titlebar=True)

#===================================================================================
#                                      main
#===================================================================================
def main():

    print ('path_skin', path_skin)

#---------weapon function 
    getResources(path_skin.replace(path_skin.split('\\')[-1],'Game'), root)
    
#---------attachment function
    fileStructure(rep_att, rep_acc)
    obj_att__vs__item_acc(client_att, rep_att)

#---------errors
    errors.sort()
    for i in errors:
        error_report(i)

    copy_files(path_skin, root)
    # i_am_done()

if __name__ == "__main__":
    init(convert=True)
    
#----------UI Insert path
    wfc_repo, skin_repo = Ask_Path()

#---------Weapon var-path
    root = os.path.abspath(wfc_repo)
    items_folder = os.path.join(root, 'Game/Items/Weapons')
    items_folder_weapons = os.path.join(root, 'Game/Items/Weapons')
    items_folder_accessories = os.path.join(root, 'Game/Items/Accessories')
    print(("Please enter the absolute path to the folder with new skins, like a F:\WFC\Wfc_git\weap\wfc-4189\Game\n"))
    path_skin = os.path.abspath(skin_repo)

#---------Attachment var-path
    Objects_Attachments = "\Objects\Attachments"
    Items_Accessories = "\Items\Accessories"
    Game_Objects_Attachments = "\Game\Objects\Attachments"
    Game_Items_Accessories = "\Game\Items\Accessories"

    client_att = root + Game_Objects_Attachments
    rep_att = path_skin + Objects_Attachments
    acc_att = root + Game_Items_Accessories
    rep_acc = path_skin + Items_Accessories

#---------
    errors = []
    main_output = []
    main()
    