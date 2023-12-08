from datetime import time
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

#---------------------------------------------------------
def pretty_print(element, indent=None):
    if indent is None:
        indent = "    "
    original = ET.tostring(element, 'utf8')
    reparsed = minidom.parseString(original)
    indented = reparsed.toprettyxml(indent=indent, newl='\n')
    return '\n'.join([s for s in indented.splitlines() if s.strip()])
#---------------------------------------------------------
def ReplaceLineInFile(fileName, sourceText, replaceText):
    file = open(fileName, 'r')  # Opens the file in read-mode
    text = file.read()  # Reads the file and assigns the value to a variable
    file.close()  # Closes the file (read session)
    file = open(fileName, 'w')  # Opens the file again, this time in write-mode
    file.write(text.replace(sourceText, replaceText))  # replaces all instances of our keyword
    # and writes the whole output when done, wiping over the old contents of the file
    file.close()  # Closes the file (write session)
    print (Fore.GREEN + fileName, 'All went well, the modifications are done' + Fore.WHITE)
#---------------------------------------------------------
def createSkinFileAccesorise(file, folder_skin, variation_name):
    print ("folder_skinfolder_skin", folder_skin)
    print (file)
    print (Fore.YELLOW + variation_name + Fore.WHITE)
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
#--------------------------------------------------------
def check_TextureUpper(file, extension):
    if ''.join(file.split('/')[-1].split('.')[0].split('_')[-1:]).isupper() != True:
        file_folder = '/'.join(file.split('/')[:-1]) + '/'
        file_name_new = '_'.join(file.split('_')[:-1]) + '_' + file.split('_')[-1].split('.')[0].upper() + '.dds'
        if extension == 'dds':
            os.rename(file, file_name_new)
            
            print (Fore.BLUE +'RENAMED: ', file, 'TO', file_name_new + Fore.WHITE)
#---------------------------------------------------------
def check_TP(file, extension):
    if extension == 'tif' or extension == 'dds' or extension == 'psd':
        if file.endswith(extension):
            check_TextureUpper(file, extension)
            if '_tp' in file:
                if not file.replace('_' + file.split('_')[-1], '').endswith('_tp'):
                    collectErrors(
                        f"ERROR! {file} contain wrong naming! _tp should be in the end of the filename and before the name of the mask")
#---------------------------------------------------------
def checkNaming(file_list):
    for files in file_list:
        check_TP(files, 'mtl')
        check_TP(files, 'tif')
        check_TP(files, 'dds')
        check_TP(files, 'psd')
#---------------------------------------------------------
def readMTL(res_list):
    print (Fore.BLUE + "Checking existing textures" + Fore.WHITE)

    for elems in res_list:
        reading = open(elems, 'r').readlines()
        for strings in reading:
            if 'Texture Map=' in strings:
                clear_strings = path_skin + '/' + strings.split('File="')[1].split('"')[0]
                if '_ddn.tif' not in clear_strings:
                    if os.path.isfile(clear_strings):
                        continue
                    elif os.path.isfile(root + '/' + 'Game' + clear_strings.split('Game/')[1]):
                        continue
                    elif os.path.isfile(root + '/' + 'Game' + clear_strings.split('Game/')[1].replace('.tif', '.dds')):
                        message = "Warning. TIF file is empty, but DDS is exist:", root + '/' + 'Game' + \
                                                                               clear_strings.split('Game/')[1].replace(
                                                                                   '.tif', '.dds')
                        print (Fore.RED + message + Fore.WHITE)
                    else:
                        collectErrors(
                            f"ERROR! File: {elems} Empty files {clear_strings}")
#---------------------------------------------------------
def checkMTL(mtl_file, original_name, variation_name):
    print (Fore.BLUE + "Checking naming *mtl files for skin variation" + Fore.WHITE)

    for elems in mtl_file:
        if variation_name == original_name + '.mtl':
            collectErrors(f"Error! Contain default name. Need rename resource: {mtl_file}")
        elif variation_name == original_name + '_tp.mtl':
            collectErrors(f"Error! Contain default name. Need rename resource: {mtl_file}")
#---------------------------------------------------------
def collectErrors(message):
    contain_error = message
    if contain_error not in errors:
        errors.append(f'{contain_error}')
#---------------------------------------------------------
def choiseWeaponType(files, repo):
    attach_patterns = []
    for file in files:
        if not file.endswith('_tp.mtl') and not file.endswith('_d.mtl') and not re.search('sa[0-9]{0,2}.mtl', file):
            message = 'Which weapon your new gun based on? (Example : shg08)'
            
            print (Fore.YELLOW + message + Fore.WHITE)
            #-----------------------UI
            gui_item = file.replace('/','\\').split('\\')[-1].split('.')[0]
            parent_gun = sg.popup_get_text("Base for new weapon", default_text=gui_item)
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
                #---------UI
                no_parent_gun()

                choiseWeaponType(files, repo)
            new_gun = file.replace('mtl','xml')
        elif file.endswith('_d.mtl'):
            d_attach_pattern = (file.replace('/','\\').replace(path_skin.replace('\\Game',''), repo)
                               .replace(file.replace('/','\\').split('\\')[-1].split('_')[0], parent_gun)).replace('.mtl','.xml')
            attach_patterns.append(d_attach_pattern)
    return weapon_type, parent_gun, weapon_pattern, new_gun, attach_patterns
#---------------------------------------------------------
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
#------------------------------------------------------------------------------------------
#                               Game/Objects/Weapons
#------------------------------------------------------------------------------------------
def adding_new_weapon(weapon_objects, repo, skin_path):

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
    
    if new_gun.startswith('kn'):
        pass
    else:

        for helper in weapon_root.find('helpers').findall('helper'):
            if helper.attrib['name'].startswith(parent_gun):
                for weapon_object in weapon_objects:
                    if (helper.attrib['name'].replace(parent_gun, '') == (weapon_object.replace('/','\\').split('\\')[-1]
                        .replace('.mtl','').replace(new_gun,''))):
                        helper.attrib['name'] = helper.attrib['name'].replace(parent_gun, new_gun)
        
        for material in weapon_root.find('materials').findall('material'):
            weapon_root.find('materials').remove(material)

        def_material = ET.SubElement(weapon_root.find('materials'), 'material',
                                    name="default", 
                                    file=new_object_weapon.split('Game/')[1].replace('xml','mtl'),
                                    tpfile=new_object_weapon.split('Game/')[1].replace('.xml','_tp.mtl'))

    with open(new_object_weapon, 'wt') as f:
        f.write(pretty_print(weapon_root))

    # -------------------------------------------
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

    chrparams_root = ET.parse(chrparams_pattern).getroot()
    for animation in chrparams_root.find('AnimationList').findall('Animation'):
        if re.search(parent_gun, animation.attrib['path']):
            animation.attrib['path'] = animation.attrib['path'].replace(parent_gun, new_gun)
            if not os.path.isfile(os.path.join(skin_path, animation.attrib['path'])):
                ascendancy = animation.attrib['path']
                
                print(Fore.RED + 'Warning! There are no new aimations here ' + ascendancy + Fore.WHITE)
                #---------------------UI
                no_new_animations(ascendancy)

    if os.path.isfile(new_chrparams):
        os.remove(new_chrparams)
    with open(new_chrparams, 'wt') as f:
        f.write(pretty_print(chrparams_root))
#------------------------------------------------------------------------------------------
#                               Game/Items/Weapons
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
#                               Game/Items/Accesories
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
#------------------------------------------------------------------------------------------
def makeVariation_object(repo, variation_name, weapon_objects, weapon_folder):
    object_list = []
    weapon_xml = os.path.join(repo, 'Game\Objects\Weapons', weapon_folder, weapon_folder + '.xml')
    object_root = ET.parse(weapon_xml).getroot()
    num = -1
    for weapon_object in weapon_objects:
        num += 1
        if weapon_object.replace('/','\\').split('\\')[-1].startswith(weapon_folder + '_' + variation_name + '.mtl'):
            for element in object_root.find('materials').findall('material'):
                if element.attrib['name'] == variation_name:
                    object_root.find('materials').remove(element)

            new_material = ET.SubElement(object_root.find('materials'), 'material',
                                        name = variation_name, 
                                        file = weapon_object.split('Game/')[1],
                                        tpfile = weapon_object.split('Game/')[1].replace('.mtl','_tp.mtl'))

            with open(weapon_xml.replace('Game','').replace(repo, path_skin), 'wt') as f:
                f.write(pretty_print(object_root))                   

        elif re.search('sa[0-9]{0,2}', weapon_object):

    # remove all donnor _saslot0
            for element in object_root.findall('helpers'):
                for helper in element.findall('helper'):
                    if helper.attrib['name'].startswith(f'{weapon_folder}_{variation_name}_saslot0'):
                        element.remove(helper)

    # add saslot for manual edit
            sa_list = sasa_list(weapon_objects)
            for sa in sa_list:
                ET.SubElement(object_root.find('helpers'), 'helper',
                    name=f"{weapon_folder}_{variation_name}_saslot{sa.strip('sa')}",
                    offset="0.00000,0.00000,0.00000",
                    angles="0.000,0.000,0.000",
                    bone="MANUAL_EDIT")
                sg.PopupAnnoying(f'Objects/Weapons/{weapon_folder}/{weapon_folder}.xml\nEdit manualy bone for SA, \nprompt MANUAL_EDIT', keep_on_top=True)
                collectErrors(f'Objects/Weapons/{weapon_folder}/{weapon_folder}.xml\nEdit manualy bone for SA, \nprompt MANUAL_EDIT')

            #-------------------------------------------------------
            # Objects/Weapons/smg51/smg51_hr00001_sa01.xml
            #-------------------------------------------------------
            sa_xml_pattern = os.path.join(repo, 'Game/Objects/Weapons/ar02/ar02_winter01_console_sa01.xml')
            sa_xml = weapon_object.replace('mtl','xml')
            sa_xml_root = ET.parse(sa_xml_pattern).getroot()
            
            sa_xml_root.attrib['name'] = weapon_object.replace('/','\\').split('\\')[-1].replace('.mtl','')

            sa_xml_root.find('geometry').find('firstperson').attrib['name'] = weapon_object.split('Game/')[1].replace('mtl','cgf')
            sa_xml_root.find('geometry').find('thirdperson').attrib['name'] = weapon_object.split('Game/')[1].replace('.mtl','_tp.cgf')
            
            weapon_name = weapon_object.split('Game/Objects/Weapons/')[1].split('/')[0]
            sa_xml_root.find('helpers').find('helper').attrib['name'] = f"{weapon_name}_{variation_name}_saslot0{num}"

            for elem in sa_xml_root.findall('materials'):
                sa_xml_root.remove(elem)
            
            if os.path.isfile(sa_xml):
                os.remove(sa_xml)
            with open(sa_xml, 'wt') as f:
                f.write(pretty_print(sa_xml_root))
            with open(weapon_xml.replace('Game','').replace(repo, path_skin), 'wt') as f:
                f.write(pretty_print(object_root))
#---------------------------------------------------------
def sasa_list(weapon_objects):
    sa_list = []
    for obj in weapon_objects:
        sa = obj.split('.')[0].rsplit('_')[-1]
        if 'sa0' in sa:
            sa_list.append(sa)
    return sa_list
#------------------------------------------------------------------------------------------
#   (Sa_items xml)              Game\Items\Accessories\smg51_hr00001_sa01.xml
#------------------------------------------------------------------------------------------
def It_Acc_sa(repo, rep_acc, weapon_folder, variation_name, sa):

    xml_name = f"{weapon_folder}_{variation_name}_{sa}"
    dest = f"{rep_acc}\\{xml_name}.xml"
    num = sa.strip('sa')

    if os.path.exists(dest):
        os.remove(dest)
    else:
        pass

    content_sa = f"""
    <item class="K01_Item" name="{xml_name}" type="attachment" view_settings="Objects/Weapons/{weapon_folder}/{xml_name}.xml">
        <drop_params>
            <item name="{xml_name}" type="attachment"/>
        </drop_params>
        <types>
            <type helper="{weapon_folder}_{variation_name}_saslot{num}" name="{xml_name}"/>
        </types>
    </item>"""

    open(dest, 'a').close()
    with open(dest, 'r+') as file:
        file.writelines(content_sa)
        file.close()
#---------------------------------------------------------
# Items/Weapons/smg51/smg51_hr00001.xml             <---- 535
# Items/Weapos/smg_hr00001_shop.xml                 <---- 632
# Items/Weapons/smg51_hr00001skin_shop.xml          <---- 703
# Items/Weapons/smg51.xml  (Special sockets)        <---- 738   -- if variation_name exists == suck, else == ok [smg51.xml, smg51_shop.xml]
# Items/Weapons/smg51_shop.xml  (Shop xml)          <---- 790
#------------------------------------------------------------------------------------------
def createSkinFile(repo, weapon_objects, variation_name, weapon_folder):    
    file_list = []

    for weapon_object in weapon_objects:

        ss_mtl = weapon_object.replace('/','\\').split('\\')[-1]  # smg51_hr00001.mtl, smg51_hr00001_sa01.mtl
        weapon_name = weapon_object.replace('/','\\').split('\\')[-1].split('_')[0]   # smg51
        no_ext_mtl = weapon_object.replace('/','\\').split('\\')[-1].replace('.mtl','') # smg51_hr00001

        if ss_mtl.split('_')[1].endswith('.mtl'):
            original_weapon = os.path.join(repo, 'Game\\Items\\Weapons\\', weapon_folder + '.xml')
            
            root = ET.parse(original_weapon).getroot()
            
            for element in root.find('skins').findall('material'):
                if element.attrib['name'] == variation_name:
                    root.find('skins').remove(element)
            
            new_skin = ET.SubElement(root.find('skins'), 'material', name = variation_name)
            with open(original_weapon.replace(repo, path_skin.replace('Game','')), 'wt') as f:
                f.write(pretty_print(root))

#-------------------------------------------------------
#                               Items/Weapons/smg51/smg51_hr00001.xml
#-------------------------------------------------------
            for material in root.find('skins').findall('material'):
                find_skin = os.path.join(repo, 'Game\\Items\\Weapons\\', weapon_folder + '_' + material.get('name') + '.xml')
                if os.path.isfile(find_skin):
                    skin_pattern = find_skin
                    break
                else:
                    continue
            try:
                skin_root = ET.parse(skin_pattern).getroot() 
                skin_root.attrib['name'] = weapon_folder + '_' + variation_name

                if not ss_mtl.startswith('kn'):
                    skin_root.find('icons').find('ui_icon').attrib['name'] = weapon_folder
                    skin_root.find('drop_params').find('item').attrib['name'] = weapon_folder + '_' + variation_name
                skin_root.find('skins').find('material').attrib['name'] = variation_name
                
                for w_object in weapon_objects:
                    sa_word = w_object.split('.')[0].rsplit('_')[-1]    # sa[num]: sa01, sa02...
                    if sa_word in w_object and sa_word != variation_name:

                        ET.SubElement(skin_root.find('skins').find('material'), 'attach', socket=f'custom_socket_{variation_name}_{sa_word}')

    # idempotency--------------------------------------------------------
                try:
                    for material in skin_root.find('skins').findall('material'):
                        if material.attrib['name'] == variation_name:
                            for element in material.findall('attach'):
                                if element.attrib['socket'].startswith('custom_socket'):
                                    material.remove(element)
                except ValueError:
                    continue

                try:
                    for socket in skin_root.find('sockets').findall('socket'):
                        if socket.attrib['name'].startswith(f'custom_socket_{variation_name}'):
                            socket.remove(element)
                except ValueError:
                    continue

    # ------------------------------------------------------------------
                sa_list = sasa_list(weapon_objects)
                for sa_word in sa_list:
                    new_sa_up = ET.SubElement(material, 'attach', socket=f'custom_socket_{variation_name}_{sa_word}')
                    new_sa_down = ET.SubElement(skin_root.find('sockets'), 'socket', can_be_empty="0", name=f"custom_socket_{variation_name}_{sa_word}")

                    for i in skin_root.find('sockets').findall('socket'):
                        if i.attrib['name'].startswith('custom'):

                            ET.SubElement(i, 'support', helper=f"{weapon_folder}_{variation_name}_saslot{sa_word.strip('sa')}",
                                                        name=f"{weapon_folder}_{variation_name}_{sa_word}")
                    
                    It_Acc_sa(repo, rep_acc, weapon_folder, variation_name, sa_word)

    # ------------------------------------------------------------------
                def support_func(item):
                    if '_' in item.attrib['name']:
                        a = item.attrib['name']
                        try:
                            item.attrib['name'] = a.split('_')[0] + '_' + a.split('_')[2] + '_' + a.split('_')[3]
                        except IndexError:
                            try:
                                item.attrib['name'] = item.attrib['name'].split('_')[0]
                            except IndexError:
                                pass
                    else:
                        pass

    # idempotency--------------------------------------------------------
                for element in skin_root.find('sockets').findall('socket'):
                    if element.attrib['name'].startswith('custom'):
                        for support in element.findall('support'):

                            # sa01 == sa01
                            if element.attrib['name'].rsplit('_')[-1] == support.attrib['name'].rsplit('_')[-1]:
                                pass
                            else:
                                element.remove(support)

    # cleanuping xml -----------------------------------------------------
                    if element.attrib['name'].startswith('scope'):
                        for item in element.findall('support'):
                            support_func(item)

                    if element.attrib['name'].startswith('muzzle'):
                        for item in element.findall('support'):
                            support_func(item)

                    if element.attrib['name'].startswith('underbarrel'):
                        for item in element.findall('support'):
                            support_func(item)

                if os.path.isfile(os.path.join(repo, 'Game\\Items\\Weapons\\', weapon_folder + '_' + variation_name + '.xml')):
                    os.remove(os.path.join(repo, 'Game\\Items\\Weapons\\', weapon_folder + '_' + variation_name + '.xml'))
                
                with open(os.path.join(path_skin, 'Items\\Weapons\\', weapon_folder + '_' + variation_name + '.xml'), 'wt') as f:
                    f.write(pretty_print(skin_root))
#------------------------------------------------------------------------------------------
#                               Items/Weapos/smg_hr00001_shop.xml
#------------------------------------------------------------------------------------------
                if not ss_mtl.startswith('kn'):
                    for material in root.find('skins').findall('material'):
                        find_skin_shop = os.path.join(repo, 'Game\\Items\\Weapons\\', weapon_folder + '_' + material.get('name') + '_shop.xml')
                        
                        if os.path.isfile(find_skin_shop):
                            skin_pattern_shop = find_skin_shop  
                            break                  
                        else:
                            continue
                        
                    skin_shop_root = ET.parse(skin_pattern_shop).getroot()
                    skin_shop_root.attrib['name'] = f"{weapon_folder}_{variation_name}_shop"
                    
                    for element in skin_shop_root.find('UI_stats').findall('param'):
                        if element.attrib['name'] == "name":
                            element.attrib['value'] = f"@{weapon_folder}_{variation_name}_shop_name"
                        
                        elif element.attrib['name'] == "description":
                            element.attrib['value'] = f"@ui_weapons_{weapon_folder}_{variation_name}"
                        
                        elif element.attrib['name'] == "icon":
                            element.attrib['value'] = f"{weapon_folder}_{variation_name}"
                        
                        elif element.attrib['name'] == "rarity":
                            rarity = rarityButt(weapon_folder + '_' + variation_name)
                            element.attrib['value'] = rarity
    # clenup xml
                    try: 
                        skin_shop_root.find('content').find('item').attrib['name'] = f"{weapon_folder}_{variation_name}"
                        for elem in skin_shop_root.find('content').find('item').findall('item'):
                            if 'sa0' in elem.attrib['name']:
                                pass
                            else:
                                support_func(elem)
                    except AttributeError:
                        continue
        
    # add 'sa' elements
                    try:
                        sa_list = sasa_list(weapon_objects)
                        for sa in sa_list:
                            ET.SubElement(skin_shop_root.find('content').find('item'), 'item', 
                                            name= f"{weapon_folder}_{variation_name}_{sa}")
                    except IOError:
                        pass


                    if os.path.isfile(os.path.join(repo, 'Game\\Items\\Weapons\\', weapon_folder + '_' + variation_name + '_shop.xml')):
                        os.remove(os.path.join(repo, 'Game\\Items\\Weapons\\', weapon_folder + '_' + variation_name + '_shop.xml'))
                    with open(os.path.join(path_skin, 'Items\\Weapons\\', weapon_folder + '_' + variation_name + '_shop.xml'), 'wt') as f:
                        f.write(pretty_print(skin_shop_root))
            #------------------------------------------------------------------------------------------
            #                                       Pattern?
            #------------------------------------------------------------------------------------------
                for material in root.find('skins').findall('material'):
                        find_pattern_skin_shop = os.path.join(repo, 'Game\\Items\\Weapons\\', 
                                                weapon_folder + '_' + material.get('name') + 'skin_shop.xml')
                        
                        if os.path.isfile(find_pattern_skin_shop):
                            skin_pattern_skin_shop = find_pattern_skin_shop  
                            break                  
                        else:
                            continue
# ----------------------------------------
#                               Items/Weapons/smg51_hr00001skin_shop.xml
# ----------------------------------------
                skin_pattern_skin_shop_root = ET.parse(skin_pattern_skin_shop).getroot() 
                skin_pattern_skin_shop_root.attrib['name'] = f"{weapon_folder}_{variation_name}skin_shop"
                
                for element in skin_pattern_skin_shop_root.find('UI_stats').findall('param'):
                    if element.attrib['name'] == "name":
                        element.attrib['value'] = "@" + weapon_folder + '_' + variation_name +"skin_shop_name"
                    
                    elif element.attrib['name'] == "description":
                        element.attrib['value'] = "@" + weapon_folder + '_' + variation_name + 'skin_shop'
                    
                    elif element.attrib['name'] == "icon":
                        element.attrib['value'] = weapon_folder + '_' + variation_name
                
                for element in skin_pattern_skin_shop_root.find('skin').findall('param'):
                    if element.attrib['name'] == "thumbnail_icon":
                        element.attrib['value'] = weapon_folder + '_' + variation_name +"_thumbnail"
                    
                    elif element.attrib['name'] == "material":
                        element.attrib['value'] = variation_name

                if os.path.isfile(os.path.join(repo, 'Game\\Items\\Weapons\\', weapon_folder + '_' + variation_name + 'skin_shop.xml')):
                    os.remove(os.path.join(repo, 'Game\\Items\\Weapons\\', weapon_folder + '_' + variation_name + 'skin_shop.xml'))
                with open(os.path.join(path_skin, 'Items\\Weapons\\', weapon_folder + '_' + variation_name + 'skin_shop.xml'), 'wt') as f:
                    f.write(pretty_print(skin_pattern_skin_shop_root))

            except UnboundLocalError:
                print (Fore.CYAN + 'Your weapon is new! Create your first skin directly!'+ Fore.WHITE)
                sg.Print('Your weapon is new! Create your first skin directly!', text_color='light green', background_color='grey20')
                main_output.append('Your weapon is new! Create your first skin directly!\n')
                your_weapon_is_new(weapon_folder)

#------------------------------------------------------------------------------------------
#   (Special sockets)           Game/Items/Weapons/smg51.xml    
#------------------------------------------------------------------------------------------
        elif re.search('sa[0-9]{0,2}', weapon_object):
            original_weapon = os.path.join(path_skin, 'Items\\Weapons\\', weapon_folder + '.xml')
            root = ET.parse(original_weapon).getroot()

    # idempotency--------------------------------------------------------
            try:
                for material in root.find('skins').findall('material'):
                    if material.attrib['name'] == variation_name:
                        for element in material.findall('attach'): 
                            if element.attrib['socket'].startswith('custom_socket'):
                                material.remove(element)
            except ValueError:
                continue

            try:
                for socket in root.find('sockets').findall('socket'):
                    if socket.attrib['name'].startswith(f'custom_socket_{variation_name}'):
                        socket.remove(element)         
            except ValueError:
                continue

            sa_list = sasa_list(weapon_objects)
            for sa_word in sa_list:
                new_sa_up = ET.SubElement(material, 'attach', socket = f'custom_socket_{variation_name}_{sa_word}')
                new_sa_down = ET.SubElement(root.find('sockets'), 'socket', can_be_empty="0", name=f"custom_socket_{variation_name}_{sa_word}")
                
                for i in root.find('sockets').findall('socket'):
                    if i.attrib['name'].startswith('custom'):

                        ET.SubElement(i, 'support', helper=f"{weapon_folder}_{variation_name}_saslot{sa_word.strip('sa')}", name=f"{weapon_folder}_{variation_name}_{sa_word}")

    # idempotency--------------------------------------------------------
            for element in root.find('sockets').findall('socket'):
                for support in element.findall('support'):
                    if element.attrib['name'].startswith('custom'):

                        if element.attrib['name'].rsplit('_')[-1] == support.attrib['name'].rsplit('_')[-1]: # sa01 == sa01
                            pass
                        else:
                            element.remove(support)

                with open(original_weapon, 'wt') as f:
                    f.write(pretty_print(root))

#------------------------------------------------------------------------------------------
#   (Shop xml)                  Items/Weapons/smg51_shop.xml  
#------------------------------------------------------------------------------------------
                shop = os.path.join(repo, 'Game\\Items\\Weapons\\', weapon_folder + '_shop.xml')   
                shop_root = ET.parse(shop).getroot() 
                for element in shop_root.find('content').findall('item'):
                    if element.attrib['name'] == weapon_folder:
                        for item in element.findall('item'):
                            if element.attrib['name'] == ss_mtl.replace('.mtl',''):
                                shop_root.find('content').remove(element)
                        
                        sa_list = sasa_list(weapon_objects)
                        for sa in sa_list:
                            ET.SubElement(element, 'item', name = f"{weapon_folder}_{variation_name}_{sa}")
                
                if not weapon_object.replace('/','\\').split('\\')[-1].startswith('kn'):
                    for element in shop_root.find('skin_content').findall('item'):
                        if element.attrib['name'] == weapon_folder + '_' + variation_name + 'skin_shop':
                            shop_root.find('skin_content').remove(element)
                        New_skin = ET.SubElement(shop_root.find('skin_content'), 'item', name = f"{weapon_folder}_{variation_name}skin_shop")
                
                with open(os.path.join(path_skin, 'Items\\Weapons\\', weapon_folder + '_shop.xml'), 'wt') as f:
                    f.write(pretty_print(shop_root))
                file_list.append(os.path.join(repo, 'Game\\Items\\Weapons\\', weapon_folder + '_shop.xml'))
                
            #------------------------------------------------------------------------------------------
            #                                   default attachments
            #------------------------------------------------------------------------------------------
        elif ss_mtl.endswith('_d.mtl'):
            d_attach = os.path.join(repo, 'Game\\Items\\Accessories\\', 
                                    ss_mtl.replace('_' + variation_name,'')
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
# ------------------------------------------------------------------
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
# ------------------------------------------------------------------
def preparing_objects(weapon_objects, variation_name_list):
    temp_list = []
    for variation_name in variation_name_list:
        for weapon_object in weapon_objects:
            weapon_object = weapon_object.replace('_' + variation_name,'')
            temp_list.append(weapon_object)
    return temp_list
#------------------------------------------------------------------------------------------
#   (Skin item file)
#------------------------------------------------------------------------------------------
def getResources(path, repo, client_att, rep_att, rep_acc):
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

        variation_name_list = []
        for resources in walkfolder(objects + '/' + files, ''):
            if resources.endswith('.mtl'):
                mtl_list.append(resources)
                if resources.endswith('mtl') and not resources.endswith('_tp.mtl') and not resources.endswith('_d.mtl') and not re.search('sa[0-9]{0,2}.mtl', resources):
                    try:
                        if '_' in resources:
                            item_variation = resources.split('/')[-1].split('_')[1].split('.')[0]
                            print (Fore.YELLOW + 'Variation_name:', item_variation + Fore.WHITE)

                            variation_name_list.append(item_variation)
                        elif 'kn43_vdv' in resources:
                            item_variation = resources.split('/')[-1].split(files + '_')[1].split('.mtl')[0]
                            print (Fore.YELLOW + 'Variation_name:', item_variation + Fore.WHITE)

                            variation_name_list.append(item_variation)
                        else:
                            collectErrors(f"Error! Can't get valid variation {resources}")
                            sg.Print(f"Error! Can't get valid variation {resources}", text_color='red', background_color='grey20')
                            print (Fore.RED + "Error! Can't get valid variation", resources + Fore.WHITE)
                            
                            #-----------------------UI
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
                except IndexError:
                    
                    print(Fore.RED + "You haven't mtl's, which needed!" + Fore.WHITE)
                    collectErrors(f"MISSING mtl!        {weapon_objects}")
                    #---------UI
                    missing_mtl(weapon_objects)
                    continue

        for variation_name in variation_name_list:
            if not variation_name and os.path.isdir(os.path.join(repo, 'Objects/Weapons', files)):
                print (Fore.RED + 'Can not detect variation name. Check naming of this files'+ Fore.WHITE, files, mtl_list)
                
                #----------------UI
                cant_detect_var_Name(files, mtl_list)
            else:

                fileStructure(rep_att, rep_acc, skin_repo, files)
                checkMTL(mtl_list, files, variation_name)
                readMTL(mtl_list)
                temp_list.append(files)

                print('Checking naming of the texture files')
                
                checkNaming(mtl_list)
                checkNaming(textures_list)

                print("Started modifying data...........")
                
                createSkinFile(root, weapon_objects, variation_name, files)
                makeVariation_object(root, variation_name, weapon_objects, files)

    #---------attachment function(rds, bp, ss ...)
                obj_att__vs__item_acc(client_att, rep_att)
#------------------------------------------------------------------------------
#                               Game/Objects/Attachments
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

    def _next_step(path, mtl, i):
            
        for x in mtl:
            m = x.rstrip('.mtl')
            var_name = m.split('_')[1]
            tree = ET.parse(path)
            root = tree.getroot()

            item = False

            for element in root.find('materials').findall('material'):
                if element.attrib['name'] == var_name:
                    item = True
            if item == True:
                continue
            else:
                ET.SubElement(root.find('materials'), 'material',
                            name=f"{var_name}",
                            file=f"objects/attachments/{i}/{x}",
                            tpfile=f"objects/attachments/{i}/{m}_tp.mtl")

            with open(path, 'w') as f:
                f.write(pretty_print(root))
        mtl.clear()

    # ----------------------------------------------------------------------------
    if  i == 'bp07':
        plan_b = '\\' + f'{i}' + '\\' + f'{i}_01.xml'
        crazy_source = client_att + plan_b
        crazy_destination = rep_att + plan_b
        shutil.copyfile(crazy_source, crazy_destination)
        _next_step(crazy_destination, mtl, i)
    
    else:   
        try:
            shutil.copyfile(client_xml, rep_xml)
            _next_step(rep_xml, mtl, i)
        except(FileNotFoundError):
            os.makedirs(path_skin + f'\\Objects\Attachments\\{i}')
            shutil.copyfile(client_xml, rep_xml)
            _next_step(rep_xml, mtl, i)
#------------------------------------------------------------------------------
def add_material_att(rep_acc_xml, skin_item, mtl):

    tree = ET.parse(rep_acc_xml)
    root = tree.getroot()

    for skin_item in mtl:
        skin_item = skin_item.split('_')[1].rstrip('.mtl')

        have_skins = False

        for skin_tag in root.findall('skins'):
            
            have_skins = True

        if have_skins == True:
            material_exists = False

            for element in root.find('skins').findall('material'):
                if element.attrib['name'] == skin_item:
                    material_exists = True
                    
            if material_exists == True:
                continue
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
            text.attrib['text'] = f"@ui_{new_skin}_ingame"

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
#                               Game/Items/Accessories
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

            if item == 'bp07_01':
                print('d')
            else:

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
#                               Game/Objects/Attachments + Game/Items/Accessories
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
#   (Add File Structure)
#------------------------------------------------------------------------------
def fileStructure(rep_att, rep_acc, skin_repo, files):
    
    it_weap_path = skin_repo + '\\Items\\Weapons'
    obj_weap_path = skin_repo + f'\\Objects\\Weapons\\{files}'

    def check_and_create(pppath):
        if os.path.exists(pppath) == True:
            pass
        else:
            os.makedirs(pppath)

    check_and_create(rep_att)
    check_and_create(rep_acc)
    check_and_create(it_weap_path)
    check_and_create(it_weap_path)
#------------------------------------------------------------------------------
#   (Good Ending)
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
                if_copy_YES()
                shutil.copyfile(k, dst)
                
    if copy == 'No':
        #-----------UI
        if_copy_NO()
    else:
        #-----------UI
        cant_understand()
        copy_files(path_skin, repo)
#==================================================================================
#   (UI)
#==================================================================================
def Ask_Path():

    layout = [
        [sg.Text('Insert your WFC repo path', text_color='yellow')],
        [sg.InputText(
            default_text = r"c:\wf-skins-minsk",
            key = "-REPO-"),
            sg.FolderBrowse()],

        [sg.Text("Skin absolute path ('Game' folder)", text_color='yellow')],
        [sg.InputText(
            default_text = r"d:/_WFC_rep/WFC_Content_Pack_29/29_1_Weapon_Skins_Desert_Dog_Pack_x3_Basic/Game",
            key = "-SKINS-"),
            sg.FolderBrowse()],

        [sg.OK(key='OK'), sg.Cancel()]
    ]
    window = sg.Window('', layout, no_titlebar=True)

    while True:
        event, values = window.read(close=True)

        wfc_repo = values["-REPO-"]
        skin_repo = values["-SKINS-"]

        if event == 'OK':
            return wfc_repo, skin_repo

        if event in ('Cancel', None) or event == sg.WIN_CLOSED:
            break
        
    window.close()
#----------------------------------------------------------------------------------
def rarityButt(item):
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

        [sg.Output(key='OUT', background_color='black', text_color='green', size=(85, 20))],


        # [sg.Multiline(main_output,
        #     key='ML',
        #     font=('Consolas', 10),
        #     autoscroll=True,
        #     size=(80, 20),
        #     pad=(0, (15, 0)),
        #     background_color='grey20',
        #     text_color = "#3EF000",
        #     do_not_clear=True,
        #     disabled=True,
        #     auto_refresh=True,
        #     focus=True
        #     )],

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

        # if event == 'OUT':
        #     window.update()

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
    getResources(path_skin.replace(path_skin.split('\\')[-1],'Game'), root, client_att, rep_att, rep_acc)

    #---------errors    
    errors.sort()
    for i in errors:
        error_report(i)
    copy_files(path_skin, root)

#----------------------------------------------------------------------------------
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

    #---------main path
    client_att = root + Game_Objects_Attachments
    rep_att = path_skin + Objects_Attachments
    acc_att = root + Game_Items_Accessories
    rep_acc = path_skin + Items_Accessories
    #---------
    errors = []
    main_output = []
    main()
    
