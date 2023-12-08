import os, glob
from traceback import print_tb
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os.path
from os import name, path
import PySimpleGUI as sg
import shutil
sg.theme('DarkGrey13')



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
#---------------------------------------------------------
def droplist_BASE(list_there, we_item):
    widget = [

        [sg.Text(f'Choose your base for new weapon ==> {we_item}', text_color='#ebd234')],
        [sg.Combo(list_there, default_value=list_there[0], key = "-BASE-", size=(31, 13))],

        [sg.OK(key='OK'), sg.Cancel()]
    ]
    window = sg.Window('', widget, no_titlebar=True)

    while True:
        event, values = window.read(close=True)

        ask_base = values["-BASE-"]

        if event == 'OK':
            return ask_base
        if event in ('Cancel', None) or event == sg.WIN_CLOSED:
            break
        
    window.close()
#=========================================================
# SA (knives and weapons)
#=========================================================
def SA_Obj(i, kn_item, kn_Files, sa_Obj_SkinPath):

    item = i.split('.')[0]
    material = i.split('_')[1]
    num = i.split('_')[-1].strip('sa.').split('.')[0]

    sa_addon = ''
    for elem in kn_Files:
        if '_tp.cgf' in elem:
            sa_addon = f"""\n\t\t<thirdperson slot="sa_tp" name="Objects/Weapons/{kn_item}/{item}_tp.cgf" offset="0.00000,0.0,0.00000" angles="0.000,0.000,0.000"/>"""

    sa_sample = f"""<item_view name="{item}">
    <geometry>
    \t<firstperson slot="sa" name="Objects/Weapons/{kn_item}/{item}.cgf" offset="0.00000,0.0,0.00000" angles="0.000,0.000,0.000"/>{sa_addon}
    </geometry>
    <helpers>
    \t<helper name="{kn_item}_{material}_saslot{num}" offset="-0.00000,0.0,-0.00000" angles="0.000,0.000,0.000"/>
    </helpers>
    \t<materials>
    \t<material name="{material}" file="objects/weapons/{kn_item}/{item}.mtl" tpfile="objects/weapons/{kn_item}/{item}_tp.mtl"/>
    </materials>\n</item_view>"""

    open(sa_Obj_SkinPath, 'a').close()
    with open(sa_Obj_SkinPath, 'w') as f:
        f.writelines(sa_sample)
        f.close()
#---------------------------------------------------------
def SA_Acc(i, kn_item, sa_Acc_SkinPath):
    
    name = i.split('.')[0]
    item = i.split('_')[0]
    num = i.split('_')[-1].strip('sa.').split('.')[0]
    if name == f'{item}_sa{num}':
        material = ''
    else:
        material = '_' + i.split('_')[1]
    
    sa_sample = f"""<item class="K01_Item" name="{name}" type="attachment" view_settings="Objects/Weapons/{kn_item}/{name}.xml">
  <UI_stats>
    <param name="name" value="@sp_default_name"/>
    <param name="description" value="@ui_accessories_sp_default"/>
    <param name="icon" value="ccs_nonitem"/>
  </UI_stats>
  <content>
		<item name="{name}"/>
	</content>
  <drop_params>
    <item name="{name}" type="attachment"/>
  </drop_params>
  <settings/>
  <sockets/>
  <types>
    <type helper="{kn_item}{material}_saslot{num}" name="{name}"/>
  </types>\n</item>"""

    open(sa_Acc_SkinPath, 'a').close()
    with open(sa_Acc_SkinPath, 'w') as f:
        f.writelines(sa_sample)
        f.close()
#=========================================================
# old Knives
#=========================================================
def KN_exist_Obj(kn_Files, Obj_SkinPath, sa_list):

    root = ET.parse(Obj_SkinPath).getroot()

    for i in kn_Files:
        if i.endswith('_tp.mtl') and 'sa0' not in i:
    
    # define material
            if 'console' in i:
                name = i.split('_tp')[0]
                item = name.split('_')[0]
                if i.split('_')[0] + '_console' == name:
                    material = 'default'
                else:
                    material = name.split('_')[1] + '_console'
                
            else:
                name = i.split('_tp')[0]
                item  = i.split('_')[0]
                if name == item:
                    material = 'default'
                else:
                    material = name.split('_')[1]
                
    # remove skin material if exist, except 'default'
    for element in root.find('materials').findall('material'):
        if element.attrib['name'] == "default":
            pass
        elif element.attrib['name'] == material:
            root.find('materials').remove(element)
            break

    # if "helpers" tag doesnt exist
    with open(Obj_SkinPath, 'r+') as f:
        if "<helpers>" not in f and len(sa_list) > 0:
            ET.SubElement(root, 'helpers')
            f.close()
        else:
            pass
        f.close()

    # create helper, if "sa" enabled
    for sa in sa_list:
        ET.SubElement(root.find('helpers'), 'helper',
                                angles="0.000,-0.000,0.000",
                                bone="weapon",
                                name=f"{name}_saslot{sa.strip('sa')}",
                                offset="0.00000,0.00000,0.00000")
    
    # add new skinmaterial
    for element in root.find('materials').findall('material'):
        if element.attrib['name'] == material:
            root.find('materials').remove(element)

        ET.SubElement(root.find('materials'), 'material',
                                name=material,
                                file=f"objects/weapons/{item}/{name}.mtl",
                                tpfile=f"objects/weapons/{item}/{name}_tp.mtl")
        break

    with open(Obj_SkinPath, 'wt') as f:
        f.write(pretty_print(root))    
#---------------------------------------------------------
def KN_exist_It(kn_Files, It_SkinPath, sa_list):
    
    for i in kn_Files:
        if i.endswith('_tp.mtl') and 'sa0' not in i:
    # define material
            item = i.split('_')[0]
            if 'console' in i:
                material = i.split('_')[1] + '_console'
            else:
                material = i.split('_')[1]

    root = ET.parse(It_SkinPath).getroot()

    # remove skin if exists
    for element in root.find('skins').findall('material'):
        if element.attrib['name'] == material:
            root.find('skins').remove(element)
    
    # add new skin
    ET.SubElement(root.find('skins'), 'material', name=material)
    
    # add "sa" socket
    if len(sa_list) == 0:
        pass
    else:
        for sa in sa_list:
            for sa_skin in root.find('skins').findall('material'):
                if sa_skin.attrib['name'] == material:
                    ET.SubElement(sa_skin,'attach',
                                    socket=f'custom_socket_{item}_{material}_{sa}')
    
    for sa in sa_list:
        ET.SubElement(ET.SubElement(root.find('sockets'),
                                    'socket',
                                            can_be_empty="0",
                                            name=f'custom_socket_{item}_{material}_{sa}'),
                                            
                                    'support',
                                            helper=f"{item}_{material}_saslot{sa.strip('sa')}",
                                            name=f"{item}_{material}_{sa}")

    # remove tag "skin_content"
    for skin_content in root.findall('skin_content'):
        root.remove(skin_content)
    
    # add new tag "skin_content"
    ET.SubElement(ET.SubElement(root, 'skin_content'), 'item')
    for skin_material in root.find('skins').findall('material'):
        ET.SubElement(root.find('skin_content'),'item', name=f"{item}_{skin_material.attrib['name']}_shop")

    with open(It_SkinPath, 'wt') as f:
        f.write(pretty_print(root))    
#=========================================================
# old Weapons
#=========================================================
def WE_exist_Obj(kn_Files, Obj_SkinPath, sa_list):

    root = ET.parse(Obj_SkinPath).getroot()

    for i in kn_Files:
        if i.endswith('_tp.mtl') and 'sa0' not in i:
    
    # define material
            if 'console' in i:
                name = i.split('_tp')[0]
                item = name.split('_')[0]
                if i.split('_')[0] + '_console' == name:
                    material = 'default'
                else:
                    material = name.split('_')[1] + '_console'
                
            else:
                name = i.split('_tp')[0]
                item  = i.split('_')[0]
                if name == item:
                    material = 'default'
                else:
                    material = name.split('_')[1]

    # if "helpers" tag doesnt exist
    with open(Obj_SkinPath, 'r+') as f:
        if "<helpers>" not in f and len(sa_list) > 0:
            ET.SubElement(root, 'helpers')
            f.close()
        else:
            pass
        f.close()

    # remove equal helper if exist
    for elem in root.find('helpers').findall('helper'):
        if material in elem.attrib['name']:
            root.find('helpers').remove(elem)

    # create helper, if "sa" enabled  
    for sa in sa_list:
        ET.SubElement(root.find('helpers'), 'helper',
                                angles="0.000,-0.000,0.000",
                                bone="weapon",
                                name=f"{name}_saslot{sa.strip('sa')}",
                                offset="0.00000,0.00000,0.00000")
    
    # remove skin material if exist
    for element in root.find('materials').findall('material'):
        if element.attrib['name'] == material:
            root.find('materials').remove(element)

    # add new skinmaterial
    for element in root.find('materials').findall('material'):
        ET.SubElement(root.find('materials'), 'material',
                        name=material,
                        file=f"objects/weapons/{item}/{name}.mtl",
                        tpfile=f"objects/weapons/{item}/{name}_tp.mtl")
        break

    with open(Obj_SkinPath, 'wt') as f:
        f.write(pretty_print(root))    
#---------------------------------------------------------
def WE_exist_It(kn_Files, It_SkinPath, sa_list):
    
    for i in kn_Files:
        if i.endswith('_tp.mtl') and 'sa0' not in i:
            
    # define material
            if 'console' in i:
                name = i.split('_tp')[0]
                item = name.split('_')[0]
                if i.split('_')[0] + '_console' == name:
                    material = 'default'
                else:
                    material = name.split('_')[1] + '_console'
                
            else:
                name = i.split('_tp')[0]
                item  = i.split('_')[0]
                if name == item:
                    material = 'default'
                else:
                    material = name.split('_')[1]

    root = ET.parse(It_SkinPath).getroot()

    # remove skin if exists
    for element in root.find('skins').findall('material'):
        if element.attrib['name'] == material:
            root.find('skins').remove(element)
    
    # add new skin
    ET.SubElement(root.find('skins'), 'material', name=material)
    
    # add "sa" socket Up
    if len(sa_list) == 0:
        pass
    else:
        for sa in sa_list:
            for sa_skin in root.find('skins').findall('material'):
                if sa_skin.attrib['name'] == material:
                    ET.SubElement(sa_skin,'attach',
                                            socket=f'custom_socket_{item}_{material}_{sa}')
    # add "sa" socket Down
    for sa in sa_list:
        ET.SubElement(ET.SubElement(root.find('sockets'),
                                    'socket',
                                            can_be_empty="0",
                                            name=f'custom_socket_{item}_{material}_{sa}'),
                                    'support',
                                            helper=f"{item}_{material}_saslot{sa.strip('sa')}",
                                            name=f"{item}_{material}_{sa}")

    # remove tag "skin_content"
    for skin_content in root.findall('skin_content'):
        root.remove(skin_content)
    
    # add tag "skin_content" for materials
    ET.SubElement(ET.SubElement(root, 'skin_content'), 'item')
    for skin_material in root.find('skins').findall('material'):
        ET.SubElement(root.find('skin_content'),'item',
                                            name=f"{item}_{skin_material.attrib['name']}_shop")

    with open(It_SkinPath, 'wt') as f:
        f.write(pretty_print(root))
    
    # --------------------------------
    # create equal xml for skin
    # --------------------------------
    if material == 'default':
        pass
    else:
        # remove unused materials 
        for element in root.find('skins').findall('material'):
            if element.attrib['name'] == material:
                pass
            else:
                root.find('skins').remove(element)

        # remove unused tags
        for skin_content in root.findall('skin_content'):
            root.remove(skin_content)

        equal_xml = it_weap_Skin + f'\\{item}_{material}.xml'
        open(equal_xml, 'a').close()
        with open(equal_xml, 'wt') as f:
            f.write(pretty_print(root))
#=========================================================
# new Knives
#=========================================================
def KN_new_Obj(kn_Files, Obj_SkinPath, sa_list):
    
    for i in kn_Files:
        if i.endswith('_tp.mtl') and 'sa0' not in i:
    
    # define material
            if '_console' in i:
                item = i.split('_tp')[0]    # kn00
            else:
                item = i.split('_')[0] + '_console'
            material = 'default'
            file = f"objects/weapons/{item}/{item}.mtl"
            tpfile = f"objects/weapons/{item}/{item}_tp.mtl"
            break

    # root
    root = ET.parse(Obj_SkinPath).getroot()

    # if "helpers" tag doesnt exist
    with open(Obj_SkinPath, 'r+') as f:
        if "<helpers>" not in f and len(sa_list) > 0:
            ET.SubElement(root, 'helpers')
            f.close()
        else:
            pass
        f.close()

    # create helper, if "sa" enabled
    for sa in sa_list:
        ET.SubElement(root.find('helpers'), 'helper',
                                angles="0.000,-0.000,0.000",
                                bone="weapon",
                                name=f"{name}_saslot{sa.strip('sa')}",
                                offset="0.00000,0.00000,0.00000")
    
    # create "default" material
    ET.SubElement(ET.SubElement(root, 'materials'), 'material',
                                name=material,
                                file=file,
                                tpfile=tpfile)

    #  adjust right cgf/chr
    for geometry in root.find('geometry').findall('firstperson'):
        geometry.attrib['name'] = geometry.attrib['name'].replace('kn01', item)
    for geometry in root.find('geometry').findall('thirdperson'):
        geometry.attrib['name'] = geometry.attrib['name'].replace('kn01', item)
    

    with open(Obj_SkinPath, 'wt') as f:
        f.write(pretty_print(root)) 
#---------------------------------------------------------
def KN_new_It(kn_Files, It_SkinPath, sa_list):
    
    for i in kn_Files:
        if i.endswith('_tp.mtl') and 'sa0' not in i:
    
    # define material
            if 'console' in i:
                item = i.split('_')[0] + '_console'
                if i.split('_tp')[0] == item:
                    material = 'default'
                else:
                    material = i.split('_')[1] + '_console'
            else:
                item = i.split('_')[0]
                if i.split('_tp')[0] == item:
                    material = 'default'
                else:
                    material = i.split('_')[1]

    root = ET.parse(It_SkinPath).getroot()

    # add new skin
    ET.SubElement(ET.SubElement(root, 'skins'), 'material', name=material)
    
    # add "sa" socket
    if len(sa_list) == 0:
        pass
    else:
        for sa in sa_list:
            for sa_skin in root.find('skins').findall('material'):
                if sa_skin.attrib['name'] == material:
                    ET.SubElement(sa_skin,
                                    'attach',
                                            socket=f'custom_socket_{item}_{material}_{sa}')
    for sa in sa_list:
        ET.SubElement(ET.SubElement(root.find('sockets'),
                                    'socket',
                                            can_be_empty="0",
                                            name=f'custom_socket_{item}_{material}_{sa}'),
                                            
                                    'support',
                                            helper=f"{item}_{material}_saslot{sa.strip('sa')}",
                                            name=f"{item}_{material}_{sa}")

    root.attrib['name'] = root.attrib['name'].replace('kn01', item)
    root.attrib['view_settings'] = root.attrib['view_settings'].replace('kn01', item)

    # UI stats
    for ui in root.find('UI_stats').findall('param'):
        if ui.attrib['name'] == 'name':
            ui.attrib['value'] = ui.attrib['value'].replace('kn01', item)
        if ui.attrib['name'] == 'description':
            ui.attrib['value'] = ui.attrib['value'].replace('kn01', item)
        if ui.attrib['name'] == 'icon':
            ui.attrib['value'] = ui.attrib['value'].replace('kn01', item)
    
    # icons
    for icon in root.find('icons').findall('combatlog'):
        icon.attrib['melee'] = f"{item.title()}_combatLog"
    for icon in root.find('icons').findall('weaponpanel'):
        icon.attrib['icon'] = f"{item.title()}_combatLog"

     
    with open(It_SkinPath, 'wt') as f:
        f.write(pretty_print(root))    
#=========================================================
# new Weapons
#=========================================================
def WE_new_Obj(kn_Files, Obj_SkinPath, sa_list):
    
    for i in kn_Files:
        if i.endswith('_tp.mtl') and 'sa0' not in i:
    
    # define material
            if '_console' in i:
                name = i.split('_tp')[0]
                item = name.split('_')[0]
                if i.split('_')[0] + '_console' == name:
                    material = 'default'
                else:
                    material = name.split('_')[1] + '_console'

                if material == 'default':
                    file = f"objects/weapons/{item}/{item}.mtl"
                    tpfile = f"objects/weapons/{item}/{item}_tp.mtl"
                else:
                    file = f"objects/weapons/{item}/{item}.mtl"
                    tpfile = f"objects/weapons/{item}/{item}_tp.mtl"

            else:
                name = i.split('_tp')[0]
                item  = i.split('_')[0]
                if name == item:
                    material = 'default'
                else:
                    material = name.split('_')[1]
                
                if material == 'default':
                    file = f"objects/weapons/{item}/{item}.mtl"
                    tpfile = f"objects/weapons/{item}/{item}_tp.mtl"
                else:
                    file = f"objects/weapons/{item}/{item}_{material}.mtl"
                    tpfile = f"objects/weapons/{item}/{item}_{material}_tp.mtl"

            break

    # root
    root = ET.parse(Obj_SkinPath).getroot()
    root.attrib['name'] = item

    # IK pose
    for pose in root.find('IKPoses').findall('tp_pose'):
        if pose.attrib['name'].startswith(item.strip('0123456789')):
            pose.attrib['name'] = f'{item}_base'

    #  adjust right cgf/chr
    for geometry in root.find('geometry').findall('firstperson'):
        geometry.attrib['name'] = f"objects/weapons/{item}/{item}.chr"
    for geometry in root.find('geometry').findall('thirdperson'):
        geometry.attrib['name'] = f"objects/weapons/{item}/{item}_tp.cgf"
    
    # if "helpers" tag doesnt exist
    with open(Obj_SkinPath, 'r+') as f:
        if "<helpers>" not in f and len(sa_list) > 0:
            ET.SubElement(root, 'helpers')
            f.close()
        else:
            pass
        f.close()

    # create helper, if "sa" enabled
    for sa in sa_list:
        ET.SubElement(root.find('helpers'), 'helper',
                                angles="0.000,-0.000,0.000",
                                bone="weapon",
                                name=f"{name}_saslot{sa.strip('sa')}",
                                offset="0.00000,0.00000,0.00000")

    # edit helpers
    for helper in root.find('helpers').findall('helper'):
        if 'slot' in helper.attrib['name']:
            root.find('helpers').remove(helper)
        
        raw = helper.attrib['name'].split('_')[0]
        raw_01 = item.strip('0123456789')
        
        if raw.startswith(raw_01):
            helper.attrib['name'] = helper.attrib['name'].replace(raw, item)


    # remove "donor" materials
    for element in root.find('materials').findall('material'):
        root.find('materials').remove(element)

    # create material
    ET.SubElement(root.find('materials'), 'material',
                                name=material,
                                file=file,
                                tpfile=tpfile)   

    with open(Obj_SkinPath, 'wt') as f:
        f.write(pretty_print(root)) 
#---------------------------------------------------------
def WE_new_It(kn_Files, It_SkinPath, sa_list):
    
    for i in kn_Files:
        if i.endswith('_tp.mtl') and 'sa0' not in i:
    
    # define material
            if '_console' in i:
                name = i.split('_tp')[0]
                item = name.split('_')[0]
                if i.split('_')[0] + '_console' == name:
                    material = 'default'
                else:
                    material = name.split('_')[1] + '_console'
            else:
                name = i.split('_tp')[0]
                item  = i.split('_')[0]
                if name == item:
                    material = 'default'
                else:
                    material = name.split('_')[1]
            break

    root = ET.parse(It_SkinPath).getroot()

    # remove tags
    try:
        for skin_content in root.find('skins').findall('material'):
            if skin_content.attrib['name'] != material:
                root.find('skins').remove(skin_content)
        for skin_content in root.find('skins').findall('attach'):
            root.find('skins').remove(skin_content)

        ET.SubElement(root.find('skins'), 'material', name=material)
    except AttributeError:
        ET.SubElement(ET.SubElement(root, 'skins'), 'material', name=material)

    # remove 'slot' tag from donor
    for sockets in root.find('sockets').findall('socket'):
        for socket in sockets:
            if 'slot' in socket.attrib['helper']:
                sockets.remove(socket)

    # add "sa" socket
    if len(sa_list) == 0:
        pass
    else:
        for sa in sa_list:
            for sa_skin in root.find('skins').findall('material'):
                if sa_skin.attrib['name'] == material:
                    ET.SubElement(sa_skin,
                                    'attach',
                                            socket=f'custom_socket_{item}_{material}_{sa}')
    for sa in sa_list:
        ET.SubElement(ET.SubElement(root.find('sockets'),
                                    'socket',
                                            can_be_empty="0",
                                            name=f'custom_socket_{item}_{material}_{sa}'),
                                            
                                    'support',
                                            helper=f"{item}_{material}_saslot{sa.strip('sa')}",
                                            name=f"{item}_{material}_{sa}")

    donor = root.attrib['name']

    root.attrib['name'] = item
    root.attrib['view_settings'] = f"objects/weapons/{item}/{item}.xml"

    # icons
    for icon in root.find('icons').findall('ui_icon'):
        icon.attrib['name'] = item
    for icon in root.find('icons').findall('combatlog'):
        icon.attrib['icon'] = f"{item.title()}_combatLog"

    # drop_params
    for param in root.find('drop_params').findall('item'):
        param.attrib['name'] = item

    
    with open(It_SkinPath, 'wt') as f:
        f.write(pretty_print(root))    
#=========================================================
# BODY
#=========================================================
def fileStructure(it_weap_Skin, it_acc_Skin, obj_weap_Skin, obj_att_Skin):

    def check_and_create(pppath):
        if os.path.exists(pppath) == True:
            pass
        else:
            os.makedirs(pppath)

    check_and_create(it_weap_Skin)
    check_and_create(it_acc_Skin)
    check_and_create(obj_weap_Skin)
    check_and_create(obj_att_Skin)
#---------------------------------------------------------
def scan(obj_weap_Skin, it_item):
    for _, _, check_files in os.walk(f"{obj_weap_Skin}/{it_item}"):
        it_Files = check_files
        # print(it_Files, '\n')
        return it_Files
#---------------------------------------------------------
def Knives(weapons_kn):
    for kn_item in weapons_kn:
        It_RepoPath = it_weap_Repo + f"\\{kn_item}.xml"
        Obj_RepoPath = obj_weap_Repo + f"\\{kn_item}\\{kn_item}.xml"

        It_SkinPath = it_weap_Skin + f"\\{kn_item}.xml"
        Obj_SkinPath = obj_weap_Skin + f"\\{kn_item}\\{kn_item}.xml"

        # items list (for knives)
        kn_Files = scan(obj_weap_Skin, kn_item)

        # sa_list
        sa_list = []
        for i in kn_Files:
            if 'sa0' in i and i.endswith('.mtl') and 'tp' not in i:
                i = i.split('_')[-1].split('.')[0]
                sa_list.append(i)

        for i in kn_Files:
            if 'sa0' in i:
                sa_Acc_SkinPath = f"{it_acc_Skin}\\{i.split('.')[0]}.xml"
                sa_Obj_SkinPath = obj_weap_Skin + f"\\{kn_item}\\{i.split('.')[0]}.xml"

                if i.endswith(".cgf") and '_tp' not in i:

                    SA_Obj(i, kn_item, kn_Files, sa_Obj_SkinPath)
                    SA_Acc(i, kn_item, sa_Acc_SkinPath)
            else:
                pass

        if path.exists(It_RepoPath) and path.exists(Obj_RepoPath):
            shutil.copyfile(Obj_RepoPath, Obj_SkinPath)
            shutil.copyfile(It_RepoPath, It_SkinPath)

            KN_exist_Obj(kn_Files, Obj_SkinPath, sa_list)
            KN_exist_It(kn_Files, It_SkinPath, sa_list)
        else:
            shutil.copyfile(f"{obj_weap_Repo}\\kn01\\kn01.xml", Obj_SkinPath)
            shutil.copyfile(f"{it_weap_Repo}\\kn01.xml", It_SkinPath)

            KN_new_Obj(kn_Files, Obj_SkinPath, sa_list)
            KN_new_It(kn_Files, It_SkinPath, sa_list)
#---------------------------------------------------------
def Weapons(weapons_orig):
    for we_item in weapons_orig:

        It_RepoPath = it_weap_Repo + f"\\{we_item}.xml"
        Obj_RepoPath = obj_weap_Repo + f"\\{we_item}\\{we_item}.xml"

        It_SkinPath = it_weap_Skin + f"\\{we_item}.xml"
        Obj_SkinPath = obj_weap_Skin + f"\\{we_item}\\{we_item}.xml"

        # items list (for knives)
        we_Files = scan(obj_weap_Skin, we_item)

        # sa_list
        sa_list = list()
        for i in we_Files:
            if 'sa0' in i and i.endswith('.mtl') and 'tp' not in i:
                i = i.split('_')[-1].split('.')[0]
                sa_list.append(i)

        for i in we_Files:
            if 'sa0' in i:
                sa_Acc_SkinPath = f"{it_acc_Skin}\\{i.split('.')[0]}.xml"
                sa_Obj_SkinPath = obj_weap_Skin + f"\\{we_item}\\{i.split('.')[0]}.xml"

                if i.endswith(".cgf") and '_tp' not in i:

                    SA_Obj(i, we_item, we_Files, sa_Obj_SkinPath)
                    SA_Acc(i, we_item, sa_Acc_SkinPath)
            else:
                pass

        if path.exists(It_RepoPath) and path.exists(Obj_RepoPath):
            shutil.copyfile(Obj_RepoPath, Obj_SkinPath)
            shutil.copyfile(It_RepoPath, It_SkinPath)

            WE_exist_Obj(we_Files, Obj_SkinPath, sa_list)
            WE_exist_It(we_Files, It_SkinPath, sa_list)
        else:
            for root, dirs, temp_files in os.walk(it_weap_Repo):
                files = temp_files
                break
            
            temp = []
            for elem in files:
                a = elem.split('.')[0].split('_')[0]
                if a not in temp:
                    temp.append(a)
                else:
                    pass 
            
            we_class = we_item.strip('0123456789')
            lst = list(filter(lambda iii: f"{we_class}" in iii.split('.')[0], temp))

            ask_base = droplist_BASE(lst, we_item)

            shutil.copyfile(f"{obj_weap_Repo}\\{ask_base}\\{ask_base}.xml", Obj_SkinPath)
            shutil.copyfile(f"{it_weap_Repo}\\{ask_base}.xml", It_SkinPath)

            WE_new_Obj(we_Files, Obj_SkinPath, sa_list)
            WE_new_It(we_Files, It_SkinPath, sa_list)
#---------------------------------------------------------
def create_XML(obj_weap_Skin):
    for path_root, path_dirs, path_files in os.walk(obj_weap_Skin):
        for it in path_dirs:
            if 'kn' in it:
                weapons_kn.append(it)
            elif 'kn' not in it and '_console' not in it:
                weapons_orig.append(it)
            elif 'kn' not in it and '_console' in it:
                weapons_console.append(it)
        break
    
    print('knives\n',weapons_kn,'\n')
    print('weapons\n', weapons_orig, '\n')
    print('console_weapons\n', weapons_console, '\n')

    Knives(weapons_kn)
    Weapons(weapons_orig)
#=========================================================
# DRIVE
#=========================================================
def main():
    fileStructure(it_weap_Skin, it_acc_Skin, obj_weap_Skin, obj_att_Skin)
    create_XML(obj_weap_Skin)
    sg.popup_notify('Complite')

if __name__ == "__main__":
    
    wfc_repo, skin_repo = Ask_Path()
    
    # split
    weapons_kn = list()
    weapons_orig = list()
    weapons_console = list()

    # # ==================TEST_PATH==================================
    # wfc_repo = os.path.abspath("c:\\wf-skins-minsk\\Game")
    # skin_repo = os.path.abspath("d:\\__some_get_come__\\__test_Weapon\\Game")
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
    #---------
    main()
    
