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
def Ask_Path():

    layout = [
        [sg.Text('Insert your WFC repo path', text_color='yellow')],
        [sg.InputText(
            default_text = r"c:\\wf-skins-minsk\\Game",
            key = "-REPO-"),
            sg.FolderBrowse()],

        [sg.Text("Skin absolute path ('Game' folder)", text_color='yellow')],
        [sg.InputText(
            default_text = r"d:\\_WFC_rep\WFC_Content_Pack_29\\29_1_Weapon_Skins_Desert_Dog_Pack_x3_Basic\\Game",
            key = "-SKINS-"),
            sg.FolderBrowse()],

        [sg.OK(key='OK'), sg.Cancel()]
    ]
    window = sg.Window('__wfc__KNWE Ultimate +  v0.001', layout, no_titlebar=False)

    while True:
        event, values = window.read(close=True)

        wfc_repo = values["-REPO-"]
        skin_repo = values["-SKINS-"]

        if event == 'OK':
            return wfc_repo, skin_repo

        if event in ('Cancel', None) or event == sg.WIN_CLOSED:
            break
        
    window.close()
#---------------------------------------------------------
def pretty_print(element, indent=None):
    if indent is None:
        indent = "    "
    original = ET.tostring(element, 'utf8')
    reparsed = minidom.parseString(original)
    indented = reparsed.toprettyxml(indent=indent, newl='\n')
    return '\n'.join([s for s in indented.splitlines() if s.strip()])
#------------------------------------------------------------------------------




#                               Game/Objects/Attachments
#------------------------------------------------------------------------------
def obj_att_func(client_att, rep_att, i):

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
            os.makedirs(skin_repo + f'\\Objects\Attachments\\{i}')
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
                pass
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
def attachments(client_att, rep_att):

    for _, dirs, _ in os.walk(rep_att):
        item_list = dirs
        break

    for i in item_list:
        obj_att_func(client_att, rep_att, i)
        item_acc_func(rep_att)
# ===============================================================================
def main():
    attachments(client_att, rep_att)

if __name__ == "__main__":
    
    #----------UI Insert path
    # wfc_repo, skin_repo = Ask_Path()

    # # ==================TEST_PATH==================================
    wfc_repo = os.path.abspath("c:\\wf-skins-minsk\\Game")
    skin_repo = os.path.abspath("d:\\__some_get_come__\\__test_Weapon\\Game")
    # skin_repo = os.path.abspath("d:\\__some_get_come__\\__test_Weapon\\kn_Game")
    # # ==================TEST_PATH==================================

        # skin path
    it_weap_Skin = skin_repo + '\\Items\\Weapons'
    it_acc_Skin = skin_repo + '\\Items\\Accessories'
    obj_weap_Skin = skin_repo + '\\Objects\\Weapons'
    obj_att_Skin = skin_repo + '\\Objects\\Attachments'
    # repo path
    it_weap_Repo = wfc_repo + '\\Items\\Weapons'
    it_acc_Repo = wfc_repo + '\\Items\\Accessories'
    obj_weap_Repo = wfc_repo + '\\Objects\\Weapons'
    obj_att_Repo = wfc_repo + '\\Objects\\Attachments'
    
    Objects_Attachments = "\Objects\Attachments"
    Items_Accessories = "\Items\Accessories"
    Game_Objects_Attachments = "\Objects\Attachments"
    Game_Items_Accessories = "\Items\Accessories"

    client_att = wfc_repo + Game_Objects_Attachments
    rep_att = skin_repo + Objects_Attachments
    acc_att = wfc_repo + Game_Items_Accessories
    rep_acc = skin_repo + Items_Accessories

    #---------
    errors = []
    main_output = []
    main()
    