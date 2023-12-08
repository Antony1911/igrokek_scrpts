#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
# [Enable inventory select]
#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
import os.path
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import LISTBOX_SELECT_MODE_MULTIPLE, PopupAnnoying
import xml.etree.ElementTree as ET
import shutil

def main():    

    sg.theme('Dark2')
    script_path = r"d:\script_path.txt"

    cl = r"c:/wf-skins-minsk"
    editor = cl + r"/Game/config/editor.cfg"

        
#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
# [add_weapons_to_lua]
#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    # path to lua config
    path = str(cl + r"/Game/Libs/Config/presets/EditorSoldier.lua")

    search_items = 'items'
    search_ammo = 'ammo'
    search_att = 'attachments'

#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #


    content = open(path, 'r+', encoding = "utf-8").readlines()
    cont_list = []

# Creating lists of available weapons as a prompt for user

    guns = cl + r"/Game/Objects/Weapons"

    for _, dirs, _ in os.walk(guns):
        some = dirs
        break


    kn = list(filter(lambda i: "kn" in i, some))
    pt = list(filter(lambda i: "pt" in i, some))
    smg = list(filter(lambda i: "smg" in i, some))
    ar = list(filter(lambda i: "ar" in i, some))
    shg = list(filter(lambda i: "shg" in i, some))
    sr = list(filter(lambda i: "sr" in i, some))
    mg = list(filter(lambda i: "mg" in i, some))

# nonblocking windows with prompt above    
    sg.PopupNonBlocking('Knives', kn, line_width=80, location=(1350, 0), text_color='Yellow', keep_on_top=1, no_titlebar=1)
    sg.PopupNonBlocking('Pistols', pt, line_width=90, location=(1350, 120), text_color='Green', keep_on_top=1, no_titlebar=1)
    sg.PopupNonBlocking('SMG', smg, line_width=90, location=(1350, 240), text_color='Orange', keep_on_top=1, no_titlebar=1)
    sg.PopupNonBlocking('Asault Rifles', ar, line_width=90, location=(1350, 380), text_color='Red', keep_on_top=1, no_titlebar=1)
    sg.PopupNonBlocking('Shotguns', shg, line_width=110, location=(1350, 500), text_color='Pink', keep_on_top=1, no_titlebar=1)
    sg.PopupNonBlocking('Sniper Rifles', sr, line_width=90, location=(1350, 620), text_color='White', keep_on_top=1, no_titlebar=1)
    sg.PopupNonBlocking('Machine Guns', mg, line_width=110, location=(1350, 740), text_color='Grey', keep_on_top=1, no_titlebar=1)

    
# ------------------------------------------------------------

    try:
        weapon_list = stuff
    except(AttributeError, UnboundLocalError):
        exit(0)
        
    str_nums = 0
    for line in content:
        str_nums += 1
        cont_list.append(line)
        
        if search_items in line:
            items = str_nums
        
        if search_att in line:
            attachments = str_nums

        if search_ammo in line:
            ammo = str_nums


# Adding Ammo
    def ammo_func(w, cont_list, ammo):
        ammo_list = []

        way = cl + r"/Game/Items/Weapons/" + f"{w}.xml"
        root = ET.parse(way).getroot()

        for A_sub in root:
            for B_sub in A_sub:
                for C_sub in B_sub.findall('param'):
                    value = C_sub.get('value')
                    if 'bullet_' in value:
                        ammo_list.append(value)

        for i in ammo_list:
            txt_ammo = '\t\t\t{ name = ' + f'"{i}"' + ',' + ' amount = 150 },\n'
            if txt_ammo not in cont_list:
                cont_list.insert(ammo, txt_ammo)
###############################################################################
    for w in weapon_list:
        if 'kn' in w:
            pass
        else:
            ammo_func(w, cont_list, ammo)
############################################################################ 


# attachments from items
    
    def att_func(w, cont_list, attachments):
        att_list = []
        way = cl + r"/Game/Items/Weapons/" + f"{w}.xml"
        root = ET.parse(way).getroot()
        for A_sub in root:
            for B_sub in A_sub.findall('socket'):
                sub = B_sub.attrib
                for x in sub.values():
                    if x == '0':
                        for C_sub in B_sub.findall('support'):
                            name = C_sub.get('name')
                            att_list.append(name)
                    elif x == '1' and x != "muzzle_flash_effect":
                        for C_sub in B_sub.findall('support'):
                            name = C_sub.get('name')
                            att_list.append(name)                    
                    else:
                        pass

        for i in att_list:
            if i == 'muzzle_flash_light' or i == 'muzzle_flash_effect':
                pass
            else:
                txt_att = '\t\t\t' + "{ name = " + f'"{i}"' + ',' + """ attachTo=""" + f'"{w}"' + """, id=12},""" + '\n'
                if txt_att not in cont_list:
                    cont_list.insert(attachments + 1, txt_att)

# ------------------------------------------------------------------------------------------
    for w in weapon_list:
        if 'kn' in w:
            pass
        else:
            att_func(w, cont_list, attachments)
# ------------------------------------------------------------------------------------------



# # # # # # backup # # # # # # # need # # # # # # # # # backup # # # # # # # # # # need  # # # #
    try:                                                                                       #
        back_folder = cl + r"/Game/Libs/Config/presets/_backup_EditorSoldier"                  #
        if not os.path.exists(back_folder):                                                    #
            os.makedirs(back_folder)                                                           #
        else:                                                                                  # 
            pass                                                                               # 
# ------------------------------------------------------------------------------------------   #                                                                                             # 
        backup = cl + r"/Game/Libs/Config/presets/_backup_EditorSoldier/EditorSoldier.lua"     #
# ------------------------------------------------------------------------------------------   #      
        if not os.path.exists(backup):                                                         #
            src_path = r"c:\wf-skins-minsk\Game\Libs\Config\presets\EditorSoldier.lua"        #                                                #
            shutil.copyfile(src_path, backup)                                                  #                                                   #
    except:                                                                                    #
        pass                                                                                   #
# # # # # # backup # # # # # # # need # # # # # # # # # backup # # # # # # # # # # need  # # # #
               


# Adding Items

    try:
        for i in weapon_list:
            txt_items = '\t\t\t{ name = ' + f'"{i}"' + ','+ " ui_name = " + f'"@{i}_shop_name"' + '},\n'
            if txt_items not in cont_list:
                cont_list.insert(items + 1, txt_items)
    except:
        pass

# Drive this stuff

    try:
        open(path, 'w', encoding = "utf-8").writelines(cont_list)
        #sg.PopupAnnoying("...Done", weapon_list)#print('...Done')
    except(FileNotFoundError):
        sg.PopupError()

if __name__ == '__main__':
    main()
    