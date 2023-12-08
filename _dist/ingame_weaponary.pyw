import os.path
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import LISTBOX_SELECT_MODE_EXTENDED
import xml.etree.ElementTree as ET
import pyperclip


# September 28th, daylight. The monsters have overtaken the city. Somehow, I'm still alive.....
#-----------------------------------------------------------------------------------------------------------------
sg.theme('Dark2')
#-----------------------------------------------------------------------------------------------------------------
script_path = os.path.dirname(os.path.realpath(__name__)) + "\\script_path.ini"

if os.path.exists(script_path) and len(open(script_path).read()) > 3 and os.path.exists(open(script_path).read()):

    exists_content = open(script_path).read()
    w_cont = sg.popup_yes_no("Continue with path? ", exists_content, no_titlebar=True,)

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
def enable_inventory(config):
    try:
        content = ['r_displayInfo = 0\n',
                    'hud_crosshair = 0\n',
                    'ui_close_screen HUD\n',
                    'ui_close_screen console_hud\n',
                    'i_enable_inventory_select 1\n'
                    'i_inventory_capacity = 100\n'
                    
                    ]
        open(config, 'w', encoding='utf-8').writelines(content)
    except(AttributeError):
        pass
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
                item = item_name.split('.')[0].split('_')[0]

                root = ET.parse(guns + '/' + item_name).getroot()
                for skins in root.findall('skins/material'):
                    skin = skins.get('name')
                    if skin is not None:
                        some.append(f'{item}:{skin}')
                try:
                    default = f'{item}:default'
                    if default in some:
                        pass
                    else:
                        some.append(f'{item}:default')
                except:
                    pass


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

        [sg.Listbox(kn, size=(20, 25), text_color='orange', select_mode=LISTBOX_SELECT_MODE_EXTENDED, key='01', enable_events=True),
        sg.Listbox(pt, size=(20, 25), text_color='red', select_mode=LISTBOX_SELECT_MODE_EXTENDED, key='02', enable_events=True),
        sg.Listbox(smg, size=(20, 25), text_color='green', select_mode=LISTBOX_SELECT_MODE_EXTENDED, key='03', enable_events=True),
        sg.Listbox(ar, size=(20, 25), text_color='blue', select_mode=LISTBOX_SELECT_MODE_EXTENDED, key='04', enable_events=True),
        sg.Listbox(shg, size=(20, 25), text_color='grey', select_mode=LISTBOX_SELECT_MODE_EXTENDED, key='05', enable_events=True),
        sg.Listbox(sr, size=(20, 25), text_color='purple', select_mode=LISTBOX_SELECT_MODE_EXTENDED, key='06', enable_events=True),
        sg.Listbox(mg, size=(20, 25), text_color='black', select_mode=LISTBOX_SELECT_MODE_EXTENDED, key='07', enable_events=True) ],

        [sg.Input(key='-INPUT01-', size=(95, 144)), sg.Text('kn', text_color='orange', background_color='white'), sg.Button('give_all_kn', key='-DEF_KN-'), sg.Text("Soul of the mind, key to life's ether.")],
        [sg.Input(key='-INPUT02-', size=(95, 144)), sg.Text('pt', text_color='red', background_color='white'), sg.Button('give_all_pt', key='-DEF_PT-'), sg.Text("Let strength be granted, so the world might be mended.")],
        [sg.Input(key='-INPUT03-', size=(95, 144)), sg.Text('smg', text_color='green', background_color='white'), sg.Button('give_all_smg', key='-DEF_SMG-'), sg.Text("Soul of the lost, withdrawn from its vessel.")],
        [sg.Input(key='-INPUT04-', size=(95, 144)), sg.Text('ar', text_color='blue', background_color='white'), sg.Button('give_all_ar', key='-DEF_AR-'), sg.Text("Let strength be granted, so the world might be mended.")],
        [sg.Input(key='-INPUT05-', size=(95, 144)), sg.Text('shg', text_color='grey', background_color='white'), sg.Button('give_all_shg', key='-DEF_SHG-'), sg.Text("Soul of the lost, withdrawn from its vessel.")],
        [sg.Input(key='-INPUT06-', size=(95, 144)), sg.Text('sr', text_color='purple', background_color='white'), sg.Button('give_all_sr', key='-DEF_SR-'), sg.Text("May thine strength help the world be mended")],
        [sg.Input(key='-INPUT07-', size=(95, 144)), sg.Text('mg', text_color='black', background_color='white'), sg.Button('give_all_mg', key='-DEF_MG-'), sg.Text("So the world might be mended.")]

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
            default_func(kn_default, '-DEF_KN-', '-INPUT01-')

            listbox_func('02', '-INPUT02-')
            default_func(pt_default, '-DEF_PT-', '-INPUT02-')

            listbox_func('03', '-INPUT03-')
            default_func(smg_default, '-DEF_SMG-', '-INPUT03-')

            listbox_func('04', '-INPUT04-')
            default_func(ar_default, '-DEF_AR-', '-INPUT04-')

            listbox_func('05', '-INPUT05-')
            default_func(shg_default, '-DEF_SHG-', '-INPUT05-')

            listbox_func('06', '-INPUT06-')
            default_func(sr_default, '-DEF_SR-', '-INPUT06-')

            listbox_func('07', '-INPUT07-')
            default_func(mg_default, '-DEF_MG-', '-INPUT07-')
        
        if event in ('OK', sg.OK()):
            break

        if event in ('Cancel', sg.Cancel()) or event == sg.WIN_CLOSED:
            exit(0)

    window.close()
    
    try:
        weapon_list = sorted(stuff)
    except(AttributeError, UnboundLocalError):
        exit(0)
#-----------------------------------------------------------------------------------------------------------------
    weapons = []
    for i in weapon_list:
        weapons.append(f"i_giveitem {i}\n")
    
    gunz = open(config, 'a', encoding='utf-8')
    gunz.writelines(weapons)
    gunz.close()

#-----------------------------------------------------------------------------------------------------------------
def SubProccess():
    pass

#==============================================================================================
#==============================================================================================
def main():

        enable_inventory(config)
        weapons_func(guns)
        pyperclip.copy('exec pyw')


#==============================================================================================
#==============================================================================================
if __name__ == '__main__':
    
    config = cl + '/' + 'pyw.cfg'
    guns = cl + r"/Game/Items/Weapons"
    
#==============================================================================================  
    main()
    sg.PopupAutoClose("Art thou done ?", auto_close_duration=0.4, no_titlebar=True)
    
#==============================================================================================  