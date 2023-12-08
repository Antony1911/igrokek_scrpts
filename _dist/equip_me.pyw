import os.path
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import LISTBOX_SELECT_MODE_MULTIPLE
import xml.etree.ElementTree as ET
import shutil


#-----------------------------------------------------------------------------------------------------------------
sg.theme('Dark2')
#-----------------------------------------------------------------------------------------------------------------
script_path = os.path.dirname(os.path.realpath(__file__)) + "script_path.ini"

if os.path.exists(script_path) and len(open(script_path).read()) > 3 and os.path.exists(open(script_path).read()):

    exists_content = open(script_path).read()
    w_cont = sg.popup_yes_no("Continue with path? ", exists_content)

    if w_cont == 'Yes':
        cl = exists_content
        pass
            
    if w_cont == 'No':
        client = sg.popup_get_folder("Client Path?", "Choose where 'Game' Folder is" )
            
        cl = client.strip("Game")
        out_file = open(script_path, "w")
        out_file.write(cl)
        out_file.close()
            
else:        
    t = "Recreating script path " + script_path
    client = sg.popup_get_folder("Client Path?", t)

    cl = client
    out_file = open(script_path, "w")
    out_file.write(cl)
    out_file.close()

#-----------------------------------------------------------------------------------------------------------------
def enable_inventory(editor):
    try:
        if "i_enable_inventory_select 1" in open(editor, 'r').read():
            pass
        else:
            open(editor, 'a').write("""
                                        \ni_enable_inventory_select 1
                                        \ng_preroundtime 0
                                        \ni_inventory_capacity = 100
                                        \nui_close_screen console_hud
                                        \nui_close_screen HUD
                                        \nhud_crosshair = 0
                                        \nr_displayInfo = 0
                                        
                                        \n""")
    except(AttributeError):
        pass

#-----------------------------------------------------------------------------------------------------------------
def reset_func(cl):
    folder = cl + r"/Game/Libs/Config/presets/_backup_EditorSoldier/EditorSoldier.lua"
    if os.path.exists(folder):
        back_to_deafult = sg.PopupYesNo("Restore default config?")

        if back_to_deafult == 'Yes':
            if os.path.exists(folder):
                with open(path, 'w', encoding='utf-8') as f:
                    f.writelines(open(folder, 'r', encoding='utf-8'))
                    f.close()
        else:
            pass
    else:
        sg.PopupAnnoying("No, Restore path doesn't exist...yet")

#-----------------------------------------------------------------------------------------------------------------
def weapons_func(guns):
    for _, _, files in os.walk(guns):
        _temp = files
        break
    
    some = []

    for item_name in _temp:
        if item_name.endswith('.xml'):
            if 'shop' in item_name: 
                pass
            elif 'test' in item_name:
                pass
            else:
                item = item_name.split('.')[0]

                try:
                    if item.split('_')[1] == 'console':
                        some.append(item)
                except IndexError:
                    pass
                
                try:
                    if len(item) > 5:
                        pass
                    else:
                        some.append(item)
                except IOError:
                    pass

                # root = ET.parse(guns + '/' + item_name).getroot()

                # for skins in root.findall('skins/material'):
                #     skin = skins.get('name')
                #     if skin is not None:
                #         some.append(f'{item}:{skin}')
                
    

    kn = list(filter(lambda i: "kn" in i, some))
    kn_default = list(filter(lambda i: "default" in i, kn))

    pt = list(filter(lambda i: "pt" in i, some))
    pt_default = list(filter(lambda i: "default" in i, pt))

    smg = list(filter(lambda i: "smg" in i, some))
    smg_default = list(filter(lambda i: "default" in i, smg))

    ar = list(filter(lambda i: "ar" in i, some))
    ar_default = list(filter(lambda i: "default" in i, ar))
    
    shg = list(filter(lambda i: "shg" in i, some))
    shg_default = list(filter(lambda i: "default" in i, shg))

    sr = list(filter(lambda i: "sr" in i, some))
    sr_default = list(filter(lambda i: "default" in i, sr))

    mg = list(filter(lambda i: 'mg'  in i, some))
    mg_default = list(filter(lambda i: 'default'  in i, mg))

    Choices = [

        [sg.Listbox(kn, size=(13, 25), text_color='orange',select_mode=LISTBOX_SELECT_MODE_MULTIPLE, key='01', enable_events=True),
        sg.Listbox(pt, size=(13, 25), text_color='red', select_mode=LISTBOX_SELECT_MODE_MULTIPLE, key='02', enable_events=True),
        sg.Listbox(smg, size=(13, 25), text_color='green', select_mode=LISTBOX_SELECT_MODE_MULTIPLE, key='03', enable_events=True),
        sg.Listbox(ar, size=(13, 25), text_color='blue', select_mode=LISTBOX_SELECT_MODE_MULTIPLE, key='04', enable_events=True),
        sg.Listbox(shg, size=(13, 25), text_color='grey', select_mode=LISTBOX_SELECT_MODE_MULTIPLE, key='05', enable_events=True),
        sg.Listbox(sr, size=(13, 25), text_color='purple', select_mode=LISTBOX_SELECT_MODE_MULTIPLE, key='06', enable_events=True),
        sg.Listbox(mg, size=(13, 25), text_color='black', select_mode=LISTBOX_SELECT_MODE_MULTIPLE, key='07', enable_events=True) ],

        [sg.Input(key='-INPUT01-', size=(95, 144)), sg.Text('kn', text_color='orange', background_color='white'), sg.Button('give_all_kn', key='-DEF_KN-')],
        [sg.Input(key='-INPUT02-', size=(95, 144)), sg.Text('pt', text_color='red', background_color='white'), sg.Button('give_all_pt', key='-DEF_PT-')],
        [sg.Input(key='-INPUT03-', size=(95, 144)), sg.Text('smg', text_color='green', background_color='white'), sg.Button('give_all_smg', key='-DEF_SMG-')],
        [sg.Input(key='-INPUT04-', size=(95, 144)), sg.Text('ar', text_color='blue', background_color='white'), sg.Button('give_all_ar', key='-DEF_AR-')],
        [sg.Input(key='-INPUT05-', size=(95, 144)), sg.Text('shg', text_color='grey', background_color='white'), sg.Button('give_all_shg', key='-DEF_SHG-')],
        [sg.Input(key='-INPUT06-', size=(95, 144)), sg.Text('sr', text_color='purple', background_color='white'), sg.Button('give_all_sr', key='-DEF_SR-')],
        [sg.Input(key='-INPUT07-', size=(95, 144)), sg.Text('mg', text_color='black', background_color='white'), sg.Button('give_all_mg', key='-DEF_MG-')]

    ]


    layout = [

        [
            sg.Column(Choices)
        ],

        [sg.OK(), sg.Cancel()]
    ]


    window = sg.Window('Choose your weapons', layout)

    stuff = set(())
    while True:
        event, values = window.read()
        #---------------------------------------------------
        def listbox_func(key01, key02):
            if event == key01:
                window.FindElement(key02).update(values[key01])
                stuff.update(values[key01])
                return stuff
            
        #---------------------------------------------------
        def default_func(list, key, input):
            if event == key:
                window.FindElement(input).update(list)
                stuff.update(list)
                return stuff

        #---------------------------------------------------

        if event is None:
            break
        else:
            listbox_func('01', '-INPUT01-')
            default_func(kn, '-DEF_KN-', '-INPUT01-')

            listbox_func('02', '-INPUT02-')
            default_func(pt, '-DEF_PT-', '-INPUT02-')

            listbox_func('03', '-INPUT03-')
            default_func(smg, '-DEF_SMG-', '-INPUT03-')

            listbox_func('04', '-INPUT04-')
            default_func(ar, '-DEF_AR-', '-INPUT04-')

            listbox_func('05', '-INPUT05-')
            default_func(shg, '-DEF_SHG-', '-INPUT05-')

            listbox_func('06', '-INPUT06-')
            default_func(sr, '-DEF_SR-', '-INPUT06-')

            listbox_func('07', '-INPUT07-')
            default_func(mg, '-DEF_MG-', '-INPUT07-')
        
        if event in ('OK', sg.OK()):
            break

        if event in ('Cancel', sg.Cancel()) or event == sg.WIN_CLOSED:
            exit(1)

    window.close()
    
    try:
        weapon_list = sorted(stuff)
    except(AttributeError, UnboundLocalError):
        exit(0)
#-----------------------------------------------------------------------------------------------------------------
    content = open(path, 'r+', encoding = "utf-8").readlines()
    cont_list = []
    search_items = 'items'
    search_ammo = 'ammo'
    search_att = 'attachments'

    try:
        weapon_list = sorted(stuff)
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

    #---------------------------------------------------
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
            txt_ammo = '\t\t\t{ name = ' + f'"{i}"' + ',' + ' amount = 15000 },\n'
            if txt_ammo not in cont_list:
                cont_list.insert(ammo, txt_ammo)

    for w in weapon_list:
        if 'kn' in w:
            pass
        else:
            ammo_func(w, cont_list, ammo)

    #---------------------------------------------------
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

    for w in weapon_list:
        if 'kn' in w:
            pass
        else:
            att_func(w, cont_list, attachments)
# ------------------------------------------------------------------------------------------
    for i in weapon_list:
        txt_items = '\t\t\t{ name = ' + f'"{i}"' + ','+ " ui_name = " + f'"@{i}_shop_name"' + '},\n'
        if txt_items not in cont_list:
            cont_list.insert(items + 1, txt_items)
        else:
            pass

    try:
        open(path, 'w', encoding = "utf-8").writelines(cont_list)
        sg.PopupAnnoying("...Done", weapon_list)
    except:
        sg.PopupError("Doesn't exist, anyway, buy my game")

# ------------------------------------------------------------------------------------------
def backup(back_folder, backup_path, path):
    try:
        if not os.path.exists(back_folder):
            os.makedirs(back_folder)
        else:
            pass

        if not os.path.exists(backup_path):
            shutil.copyfile(path, backup_path)
    except:
        pass

#==============================================================================================
#==============================================================================================
def main():

        enable_inventory(editor)
        reset_func(cl)
        weapons_func(guns)
        backup(back_folder, backup_path, path)

        work = open(script_path).read()
        equip = []

        # hands, helmet, vest
        # -----------------------------------------------------------------------------
        item_path = work + r"/Game/Items/Armor"
        # -----------------------------------------------------------------------------
        for _, _, files in os.walk(item_path):
            for i in files:
                new = os.path.splitext(i)[0]
                i = new
                equip.append(i)


        for _, _, files in os.walk(item_path):
            item_list = files
            break
        for i in item_list:
            root = ET.parse(item_path + '/' + i).getroot()

            for a_dir in root:
                for b_dir in a_dir:
                    for c_dir in b_dir:
                        for d_dir in c_dir:
                            name = d_dir.attrib.get('name')
                            if '_fp' in name:
                                pass
                            elif '_hp' in name:
                                pass
                            elif 'default' in name:
                                pass
                            else:
                                equip.append(name)


        hands = list(filter(lambda i: "hands" in i, equip))
        helmet = list(filter(lambda i: "helmet" in i, equip))
        vest = list(filter(lambda i: "vest" in i, equip))



        # FBS
        # -----------------------------------------------------------------------------
        fbs_path = work + r"\Game\Items\Skins"
        # -----------------------------------------------------------------------------
        for _, _, files in os.walk(fbs_path):
            for i in files:
                new = os.path.splitext(i)[0]
                i = new
                equip.append(i)
                #equip.append(i + '_b')

        fbs = list(filter(lambda i: "fbs" in i, equip))

        # -----------------------------------------------------------------------------
        # Equipemnt window
        layout = [
            [sg.Text('Hands')],
            [sg.InputCombo(hands, default_value="shared_hands_08", key='-HANDS-', size=(42, 25))],

            [sg.Text('Helmet')],
            [sg.InputCombo(helmet, default_value="soldier_helmet_01", key='-HELMET-', size=(42, 25))],

            [sg.Text('Vest')],
            [sg.InputCombo(vest, default_value="shared_vest_13", key='-VEST-', size=(42, 25))],


            [sg.Text()],
            [sg.Checkbox("FBS", key='-IN-'), sg.InputCombo(fbs, key='-FBS-', size=(33, 25))],

            [sg.OK(), sg.Cancel()]
        ]
        window = sg.Window('Choose your armor', layout)


        # Driving events from Buttons
        some = []
        while True:
            event, values = window.read()

            if values['-IN-'] == True:
                some.append(values['-HANDS-'])
                some.append(values['-HELMET-'])
                some.append(values['-VEST-'])
                some.append(values['-FBS-'])

            else:
                some.append(values['-HANDS-'])
                some.append(values['-HELMET-'])
                some.append(values['-VEST-'])
                some.append('> fbs')
                some.append('>')

            if event in ('OK', sg.OK()):
                print('OK')
                break

            if event in ('Cancel', sg.Cancel()) or event == sg.WIN_CLOSED:
                exit(0)
            
        window.close()
        print(some)

        # -----------------------------------------------------------------------------
        config_path = work + r"/Game/Libs/Config/presets/EditorSoldier.lua"
        # -----------------------------------------------------------------------------

        a = open(config_path, 'r+', encoding = "utf-8").readlines()
        for line in a:
            if 'helmet' in a[7]:
                pass
            if 'fbs' in a[13]:
                pass
            else:
                a.insert(7, '\t\t\t{ name = ' + '"' + '> helmet' + '"' + ' },\n')
                a.insert(13, '\t\t\t---{ name = ' + '"' + '> fbs' + '"' + ' },\n')
                open(config_path, 'r+', encoding = "utf-8").writelines(a)
                break
        # -----------------------------------------------------------------------------

        content = open(config_path, 'r+', encoding = "utf-8").readlines()
        num = -1

        for line in content:
            #if '--' in line:
            #    content.remove(line)

            num += 1

        # Hands    
            if 'hands' in line:
                hands_num = num
                txt = '\t\t\t{ name = ' + '"' + some[0] + '"' + ' },\n'

                content.pop(hands_num)
                content.insert(hands_num, txt)
            
        # Vest
            if 'vest' in line:
                vest_num = num
                txt = '\t\t\t{ name = ' + '"' + some[2] + '"' + ' },\n'

                content.pop(vest_num)
                content.insert(vest_num, txt)

        # Helmet
            if 'helmet' in line:
                helmet_num = num
                txt = '\t\t\t{ name = ' + '"' + some[1] + '"' + ' },\n'

                content.pop(helmet_num)
                content.insert(helmet_num, txt)
            else:
                pass


        # FBS
            if 'fbs' in line:
                helmet_num = num
                if len(some) == 4:
                    txt = '\t\t\t{ name = ' + '"' + some[3] + '"' + ' },\n'

                    content.pop(helmet_num)
                    content.insert(helmet_num, txt)

                else:
                    txt = '\t\t\t---{ name = ' + '"' + some[3] + '"' + ' },\n'
                    content.pop(helmet_num)
                    content.insert(helmet_num, txt)
            else:
                pass

        # drive
        open(config_path, 'w', encoding = "utf-8").writelines(content)
        sg.popup_notify('Complete!!', display_duration_in_ms=88)
#==============================================================================================
#==============================================================================================
if __name__ == '__main__':
    
    editor = cl + r"/Game/config/editor.cfg"
    path = cl + r"/Game/Libs/Config/presets/EditorSoldier.lua"
    guns = cl + r"/Game/Items/Weapons"
    back_folder = cl + r"/Game/Libs/Config/presets/_backup_EditorSoldier"
    backup_path = cl + r"/Game/Libs/Config/presets/_backup_EditorSoldier/EditorSoldier.lua"
    
#==============================================================================================  
    main()
#==============================================================================================  