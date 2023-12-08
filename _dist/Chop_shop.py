import os
from os import path
from test import material
import xml.etree.ElementTree as ET
from xml.dom import minidom
import PySimpleGUI as sg

sg.theme('Dark2')

#---------------------------------------------------------
def Ask_Path():

    path_widget = [

        [sg.Text('Insert your WFC repo path', text_color='#ebd234')],
        [sg.InputText(default_text = r"c:\\wf-skins-minsk\\Game", key = "-REPO-"), sg.FolderBrowse()],

        [sg.OK(key='OK'), sg.Cancel()]
    ]
    window = sg.Window('', path_widget, no_titlebar=True)

    while True:
        event, values = window.read(close=True)

        wfc_repo = values["-REPO-"]

        if event == 'OK':
            return wfc_repo
        if event in ('Cancel', None) or event == sg.WIN_CLOSED:
            break
        
    window.close()
# --------------------------------------------------------
def choice(helms, hands, vest, shoes):
    widget = [

        [sg.Text(f'Helmet', text_color='#ebd234')],
        [sg.Combo(helms, default_value="soldier_helmet_11", key = "-HELMS-", size=(31, 13))],

        [sg.HSeparator()],

        [sg.Text(f'Hands', text_color='#ebd234')],
        [sg.Combo(hands, default_value="shared_hands_07", key = "-HANDS-", size=(31, 13))],
        
        [sg.HSeparator()],
        
        [sg.Text(f'Vest', text_color='#ebd234')],
        [sg.Combo(vest, default_value="shared_vest_13", key = "-VEST-", size=(31, 13))],
        
        [sg.HSeparator()],
        
        [sg.Text(f'Shoes', text_color='#ebd234')],
        [sg.Combo(shoes, default_value="shared_shoes_09", key = "-SHOES-", size=(31, 13))],
        
        [sg.OK(key='OK'), sg.Cancel()]
    ]
    window = sg.Window('', widget, no_titlebar=True)

    while True:
        event, values = window.read(close=True)

        ask_helms = values["-HELMS-"]
        ask_hands = values["-HANDS-"]
        ask_vest = values["-VEST-"]
        ask_shoes = values["-SHOES-"]

        if event == 'OK':
            return ask_helms, ask_hands, ask_vest, ask_shoes 
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
#---------------------------------------------------------
def hard_helm(path):
    ss = f01(path)
    insert01 = ss[0]
    insert02 = ss[1]

    helmet_donor = wfc_repo + "\\Objects\\Characters\\shared\\helmets\\shared_helmet_stpat00001\\shared_helmet_stpat00001.xml"
    h_helmet = f"""<CharacterPart Name="shared_helmet_stpat00001" Slot="Helmets" Template="Helmet_Type1">
 <Model File="{insert01}" FGTFile="" DecalsMask="" Gender="Male">
  <Morphs />
  <Switches />
  <Materials>
   <Material Name="default" File="{insert02}"/>
  </Materials>
  <Sockets />
 </Model>
 <Model File="" FGTFile="" DecalsMask="" Gender="Female">
  <Morphs />
  <Switches />
  <Materials />
  <Sockets />
 </Model>\n</CharacterPart>"""
    with open(helmet_donor, 'wt') as f:
        f.write(h_helmet)
#---------------------------------------------------------
def hard_hands(path):
    ss = f01(path)
    insert01 = ss[0]
    insert02 = ss[1]

    hands_donor = wfc_repo + "\\Objects\\Characters\\shared\\hands\\shared_hands_07\\shared_hands_07.xml"
    h_hand = f"""<CharacterPart Name="shared_hands_07" Slot="Hands" Template="Hands_Type0">
 <Model File="{insert01}" FGTFile="" DecalsMask="" Gender="Male">
  <Morphs />
  <Switches />
  <Materials>
   <Material Name="default" File="{insert02}"/>
  </Materials>
  <Sockets />
 </Model>
 <Model File="" FGTFile="" DecalsMask="" Gender="Female">
  <Morphs />
  <Switches />
  <Materials />
  <Sockets />
 </Model>\n</CharacterPart>"""
    with open(hands_donor, 'wt') as f:
        f.write(h_hand)
#---------------------------------------------------------
def hard_vest(path):
    ss = f01(path)
    insert01 = ss[0]
    insert02 = ss[1]

    vest_donor = wfc_repo + "\\Objects\\Characters\\shared\\vests\\shared_vest_13\\shared_vest_13.xml"
    h_vest = f"""<CharacterPart Name="shared_vest_13" Slot="Vests" Template="Vest_Type0">
 <Model File="{insert01}" FGTFile="" DecalsMask="" Gender="Male">
  <Morphs />
   <Morph Switch="Helmet_Type1" Target="#jacket_vest_01"/>
   <Morph Switch="Helmet_Type2" Target="#jacket_vest_02"/>
   <Morph Switch="Helmet_Type3" Target="#jacket_vest_03"/>
  <Switches />
  <Materials>
   <Material Name="default" File="{insert02}"/>
  </Materials>
  <Sockets />
 </Model>
 <Model File="" FGTFile="" DecalsMask="" Gender="Female">
  <Morphs />
  <Switches />
  <Materials />
  <Sockets />
 </Model>\n</CharacterPart>"""
    with open(vest_donor, 'wt') as f:
        f.write(h_vest)
#---------------------------------------------------------
def hard_shoes(path):
    ss = f01(path)
    insert01 = ss[0]
    insert02 = ss[1]
    shoes_donor = wfc_repo + "\\Objects\\Characters\\shared\\shoes\\shared_shoes_09\\shared_shoes_09.xml"
    h_shoes = f"""<CharacterPart Name="shared_hands_07" Slot="Hands" Template="Hands_Type0">
 <Model File="{insert01}" FGTFile="" DecalsMask="" Gender="Male">
  <Morphs />
  <Switches />
  <Materials>
   <Material Name="default" File="{insert02}"/>
  </Materials>
  <Sockets />
 </Model>
 <Model File="" FGTFile="" DecalsMask="" Gender="Female">
  <Morphs />
  <Switches />
  <Materials />
  <Sockets />
 </Model>\n</CharacterPart>"""
    with open(shoes_donor, 'wt') as f:
        f.write(h_shoes)
#---------------------------------------------------------
def f01(path):
    ss = []
    ss.clear()
    root = minidom.parse(path)
    model = root.getElementsByTagName('Model')
    for elem in model:
        f_01 = elem.attributes['File'].value
        ss.append(f_01)
        break

    material = root.getElementsByTagName('Material')
    for elem in material:
        f_02 = elem.attributes['File'].value
        ss.append(f_02)
        break
    return ss
#---------------------------------------------------------
def determine_type(item):
    d_type = item.split('_')[0]
    d_item = item.split('_')[1]
    d_skin = item.split(d_type + '_' + d_item + '_')[1]

    # model = f"objects/characters/{d_type}/{d_item}/{item}/{item}.chr"
    # material = f"objects/characters/{d_type}/{d_item}/{item}/{item}.mtl"
    if d_item == 'helmet':
        d_item = 'helmets'
    elif d_item == 'vest':
        d_item = 'vests'
    else:
        pass
    
    try:
        path = wfc_repo + f'\\objects\\characters\\{d_type}\\{d_item}\\{item}\\{item}.xml'

    # -----------------


        hard_helm(path)
        hard_hands(path)
        hard_vest(path)
        hard_shoes(path)

    except FileNotFoundError:
        sg.popup_error(f'FileNotFoundError\n{path}')
        pass
#---------------------------------------------------------
def available_equip():
    
    item_path = wfc_repo + "\\Items\\Armor"

    for _, _, files in os.walk(item_path):
        item_list = files
        break

    #hands, helmet, vest, boots
    for i in item_list:

        if 'test' in i:
            pass
        elif 'default' in i:
            pass
        else:
            equip.append(i.split('.')[0])

        hands = list(filter(lambda i: "hands" in i, equip))
        helms = list(filter(lambda i: "helmet" in i, equip))
        vest = list(filter(lambda i: "vest" in i, equip))
        shoes = list(filter(lambda i: "shoes" in i, equip))
    
    # print(hands)
    # print('\n')
    # print(helms)
    # print('\n')
    # print(vest)
    # print('\n')
    # print(shoes)

    return helms, hands, vest, shoes
#---------------------------------------------------------
def exchange(ask_helms, ask_hands, ask_vest, ask_shoes):
    # print(ask_helms, ask_hands, ask_vest, ask_shoes)

    determine_type(ask_helms)
    determine_type(ask_hands)
    determine_type(ask_vest)
    determine_type(ask_shoes)
#---------------------------------------------------------
def main():
    hands, helms, vest, shoes = available_equip()
    ask_helms, ask_hands, ask_vest, ask_shoes = choice(hands, helms, vest, shoes)
    exchange(ask_helms, ask_hands, ask_vest, ask_shoes)
#---------------------------------------------------------
if __name__ == "__main__":

    # wfc_repo, skin_repo = Ask_Path() 
    equip = list()

    # # ==================TEST_PATH==================================
    wfc_repo = os.path.abspath("c:\\wf-skins-minsk\\Game")
    # skin_repo = os.path.abspath('d:\\__some_get_come__\\_test_Armor\\Game') 
    # # ==================TEST_PATH==================================

    main()