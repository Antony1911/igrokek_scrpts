import os, glob
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os.path
from os import name, path
import PySimpleGUI as sg
import shutil
sg.theme('DarkGrey13')


#=========================================================
# SETUP
#=========================================================
def Ask_Path():

    layout = [
        [sg.Text("Insert your WFC/WFPC repo path ('Game' folder)", text_color='yellow')],
        [sg.InputText(
            default_text = r"e:\\wfpc-minsk\\Game",
            key = "-REPO-"),
            sg.FolderBrowse()],

        [sg.Text("Skin absolute path ('Game' folder)", text_color='yellow')],
        [sg.InputText(
            default_text = r"d:\\_WfPC_rep\wfpc_work\\WFPC_Content_Pack_12\\12_4_WFPC_Weapon_Skins_Shop_x4\\Game",
            key = "-SKINS-"),
            sg.FolderBrowse()],

        [sg.OK(key='OK'), sg.Cancel()]
    ]
    window = sg.Window('Super WFC vs.WFPC XMLer Ultimate Pro++ Extended v0.0228 No Bug Edition Premium DEluxe 910 - Genesis', layout)

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
def materialle(elem):
    try:
        elem = elem.split('_tp')[0]
    except:
        elem = elem
    
    if 'console' in elem:
        try:
            mat_name = elem.split('_')[1:][0]+'_'+elem.split('_')[1:][1] + '_'+elem.split('_')[1:][2]
        except IndexError:
            try:
                mat_name = elem.split('_')[1:][0]+'_'+elem.split('_')[1:][1]
            except IndexError:
                try:
                    mat_name = elem.split('_')[1:][0]
                except IndexError:
                    mat_name = 'default'
    else:
        try:
            mat_name = elem.split('_')[1:][1]
            if len(mat_name) > 3:
                pass
            else:
                try:
                    mat_name = elem.split('_')[1:][2]
                except IndexError:
                    try:
                        mat_name = elem.split('_')[1:][0]
                    except IndexError:
                        mat_name = 'default'
        except IndexError:
            try:
                mat_name = elem.split('_')[1:][2]
            except IndexError:
                try:
                    mat_name = elem.split('_')[1:][0]
                except IndexError:
                    mat_name = 'default'
    return mat_name
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
        [sg.Combo(list_there, default_value=f"{we_item.strip('0123456789')}01", key = "-BASE-", size=(31, 13))],

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
#---------------------------------------------------------
def spec_window(hard, soft):
    ask = [
            [sg.Text(f'item_name: [{hard}]')],
            [sg.Radio(hard, "RADIO1", key='1', default=True), sg.Radio(soft, "RADIO1", key='2')],
            [sg.OK(), sg.Cancel()]

        ]

    ask_window = sg.Window('Specify your weapon',ask)
    while True:
        event, values = ask_window.read(close=True)

        if values['1'] == True:
            print(hard)
            return hard
        if values['2'] == True:
            print(soft)
            return soft

        if event in ('OK', sg.OK()):
            break
        if event in ('Cancel', sg.Cancel()) or event == sg.WIN_CLOSED:
            break  
    ask_window.close()
#=========================================================
# SA (knives and weapons)
#=========================================================
def SA_Obj(i, kn_item, kn_Files, sa_Obj_SkinPath):

    item = i.split('.')[0]
    num = i.split('_')[-1].strip('sa.').split('.')[0]

    if 'sa_d' in i:
        material = "default"
        evo01 = 'scope'
        helper = f"{i.split('.')[0]}"
    else:
        material = i.split('_')[1]
        evo01 = 'sa'
        helper = f"{kn_item}_{material}_saslot{num}"
    
    sa_addon = ''
    for elem in kn_Files:
        if '_tp.cgf' in elem:
            sa_addon = f"""\n\t\t<thirdperson slot="{evo01}_tp" name="Objects/Weapons/{kn_item}/{item}_tp.cgf" offset="0.00000,0.0,0.00000" angles="0.000,0.000,0.000"/>"""

    sa_sample = f"""<item_view name="{item}">
    <geometry>
    \t<firstperson slot="{evo01}" name="Objects/Weapons/{kn_item}/{item}.cgf" offset="0.00000,0.0,0.00000" angles="0.000,0.000,0.000"/>{sa_addon}
    </geometry>
    <helpers>
    \t<helper name="{helper}" offset="-0.00000,0.0,-0.00000" angles="0.000,0.000,0.000"/>
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
    
    if 'sa_d' in i:
        material = 'default'
        helper = i.split('.')[0]
    else:
        if name == f'{item}_sa{num}':
            material = ''
        else:
            material = '_' + i.split('_')[1]
        helper = f"{kn_item}{material}_saslot{num}"

    ui_stats = f"""\n\t<UI_stats>
    <param name="name" value="@sp_default_name"/>
    <param name="description" value="@ui_accessories_sp_default"/>
    <param name="icon" value="ccs_nonitem"/>
  </UI_stats>
  <content>
    \t<item name="{name}"/>
  </content>"""

    if 'sa_d' in i:
        ui_stats = ''

    sa_sample = f"""<item class="K01_Item" name="{name}" type="attachment" view_settings="Objects/Weapons/{kn_item}/{name}.xml">{ui_stats}
  <drop_params>
    <item name="{name}" type="attachment"/>
  </drop_params>
  <settings/>
  <sockets/>
  <types>
    <type helper="{helper}" name="{name}"/>
  </types>\n</item>"""

    open(sa_Acc_SkinPath, 'a').close()
    with open(sa_Acc_SkinPath, 'w') as f:
        f.writelines(sa_sample)
        f.close()
#=========================================================
# ATTACHMENTS (basic)
#=========================================================
def obj_att__vs__item_acc(client_att, rep_att):
    #------------------------------------------------------------------------------
    #                               Game/Objects/Attachments
    #------------------------------------------------------------------------------
    def obj_att_func(client_att, rep_att, i, mtl):

        xml = f'\\{i}\\{i}.xml'
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

                try:
                    var_name = m.split('_')[1]
                    if len(var_name) < 4:
                        var_name = 'default'
                    else:
                        pass
                except IndexError:
                    var_name = 'default'

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
                    break
            mtl.clear()

        # ----------------------------------------------------------------------------
        if  i == 'bp07':
            plan_b = f'\\{i}\\{i}_01.xml'
            crazy_source = client_att + plan_b
            crazy_destination = rep_att + plan_b
            shutil.copyfile(crazy_source, crazy_destination)
            _next_step(crazy_destination, mtl, i)
        
        else:   
            try:
                shutil.copyfile(client_xml, rep_xml)
                _next_step(rep_xml, mtl, i)
            except(FileNotFoundError):
                apath = path_skin + f'\\Objects\Attachments\\{i}'

                open(apath + f'\\{i}.xml', 'a').close()
                raw_att = i.strip('0123456789')
                donor_att = f'{raw_att}01'
                shutil.copyfile(client_att + f'\\{donor_att}\\{donor_att}.xml', rep_xml)
                
                # ------------------- make it worthy for new attachment
                shutil_OB_root = ET.parse(rep_xml).getroot()
                shutil_OB_root.attrib['name'] = i
                
                for elem in shutil_OB_root.find('geometry').findall('firstperson'):
                    elem.attrib['name'] = f"objects/attachments/{i}/{i}.cgf"
                for elem in shutil_OB_root.find('geometry').findall('thirdperson'):
                    elem.attrib['name'] = f"objects/attachments/attachments/{i}/{i}_tp.cgf"
                        
                for elem in shutil_OB_root.find('materials').findall('material'):
                    if elem.attrib['name'] == "default":
                        elem.attrib['file'] = f"objects/weapons/attachments/{i}/{i}.mtl"
                        elem.attrib['tpfile'] = f"objects/weapons/attachments/{i}/{i}_tp.mtl"
                    elif elem.attrib['name'] != "default":
                        shutil_OB_root.find('materials').remove(elem)

                with open(rep_xml, 'wt') as f:
                    f.write(pretty_print(shutil_OB_root))
                _next_step(rep_xml, mtl, i)
    #------------------------------------------------------------------------------
    def add_material_att(rep_acc_xml, skin_item, mtl):

        tree = ET.parse(rep_acc_xml)
        root = tree.getroot()

        for skin_item in mtl:
            if '.mtl' in mtl:
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
            else:
                pass
    #------------------------------------------------------------------------------
    def att_No_Skin_xml(repo_xml, item):
        tree = ET.parse(repo_xml)
        root = tree.getroot()

        old_item = root.attrib['name']
        new_item = f'{item}'

        try:
            root.attrib['name'] = root.attrib['name'].replace(old_item, new_item)
            root.attrib['view_settings'] = root.attrib['view_settings'].replace(old_item, new_item)
            try:
                for text in root.findall('description_ingame'):
                    text.attrib['text'] = text.attrib['text'].replace(old_item, new_item)
            except:
                pass
            try:
                for param in root.find('UI_stats').findall('param'):
                    param.attrib['value'] = param.attrib['value'].replace(old_item, new_item)
            except:
                pass

            if not repo_xml.split('\\')[-1].startswith('fl'):
                try:
                    for item in root.find('content').findall('item'):
                        item.attrib['name'] = item.attrib['name'].replace(old_item, new_item)
                except:
                    pass
            try:    
                for model in root.findall('drop_params'):
                    model.attrib['model'] = model.attrib['model'].replace(old_item, new_item)
            except:
                pass
            try:
                for item in root.find('drop_params'):
                    item.attrib['name'] = item.attrib['name'].replace(old_item, new_item)
            except:
                pass
            try:
                for types in root.find('types').findall('type'):
                    types.attrib['name'] = types.attrib['name'].replace(old_item, new_item)
            except:
                pass
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
        try:
            old_material = old_skin.split('_')[1]
        except IndexError:
            old_material = 'default'

        new_skin = skin_item
        new_item = f'{skin_item}'.split('_')[0]
        try:
            new_material = new_skin.split('_')[1]
        except IndexError:
            new_material = 'default'

        if old_material == 'default' or new_material == 'default':
            pass
        else:
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
    #---------------------------------------------------------
    #                               Game/Items/Accessories
    #---------------------------------------------------------
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
                if '.mtl' in m:
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
                            if 'mount0' in string:
                                pass
                            else:
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
                                if 'mount' in xml:
                                    pass
                                else:
                                    shutil.copyfile(path, rep_acc_xml)
                                    shutil.copyfile(a_path, b_path)
                                #---------
                                    att_No_Skin_xml(rep_acc_xml, item)
                                    add_material_att(rep_acc_xml, skin_item, mtl)
                                    att_Skin_xml(b_path, skin_item, item)
                else:
                    pass
    #---------------------------------------------------------
    mtl = []
    for _, dirs, _ in os.walk(rep_att):
        item_list = dirs
        break

    for i in item_list:
        obj_att_func(client_att, rep_att, i, mtl)
        item_acc_func(rep_att)
#=========================================================
# ATTACHMENTS (default _d)
#=========================================================
def Default_attach(i, weapon, skin, def_att):
    list_ss = {
            'ar13_drum_01_console':'ar13',
            'smg04_tape01_console':'smg04',
            'shg01_rope01_console':'shg01',
            'shg40_rift01_console':'shg40',
            }
            
    # ----------------
    # to Objects '_d'
    # ----------------
    if weapon in list_ss:
        if 'ar13' in weapon:
            src_obj_path = f"{wfc_repo}\\Objects\\Weapons\\{weapon}\\{weapon}_{def_att}.xml"
            dst_obj_path = obj_weap_Skin + f'\\{weapon}\\{weapon}_{def_att}.xml'
        else:
            src_obj_path = f"{wfc_repo}\\Objects\\Weapons\\{list_ss[weapon]}\\{weapon}_{def_att}.xml"
            dst_obj_path = obj_weap_Skin + f'\\{list_ss[weapon]}\\{weapon}_{def_att}.xml'
    else:
        src_obj_path = f"{wfc_repo}\\Objects\\Weapons\\{weapon}\\{weapon}_{def_att}.xml"
        dst_obj_path = obj_weap_Skin + f'\\{weapon}\\{weapon}_{def_att}.xml'
    
    if os.path.exists(src_obj_path):
        shutil.copyfile(src_obj_path, dst_obj_path)
    else:
        open(dst_obj_path, 'a').close()
        for root, dirs, files in os.walk(obj_weap_Repo):
            files = files
            for file in files:
                if def_att + '.xml' in file:
                    donor = file
                    break
        
        print('[donor]')
        print(donor)
        donor_weapon = donor.split('_')[0]
        shutil.copyfile(f"{obj_weap_Repo}\\{donor_weapon}\\{donor}", dst_obj_path)

    # ------------------- make it worthy for Objects
    shutil_OB_root = ET.parse(dst_obj_path).getroot()

    # some fix
    try:
        shutil_OB_root.attrib['name'] = f"{weapon}_{def_att}"
    except:
        pass

    # fix gp_d
    if def_att == 'gp_d':
        shutil_OB_root.attrib['name'] = weapon + '_' + def_att
        shutil_OB_root.attrib['item_view'] = weapon + '_' + def_att
    else:
        pass
        # if shutil_OB_root.attrib['item_view'] == None:
        #     pass
        # else:
        #     shutil_OB_root.attrib['item_view'] = weapon + '_' + def_att

    # fix sp_d
    if def_att == 'sp_d':
        try:
            for elem in shutil_OB_root.find('effects').find('muzzleflash').findall('firstperson'):
                elem.attrib['effect'] = f"muzzleflash_{weapon.strip('0123456789')}.{weapon}_fp"
            for elem in shutil_OB_root.find('effects').find('muzzleflash').findall('thirdperson'):
                elem.attrib['effect'] = f"muzzleflash_{weapon.strip('0123456789')}.{weapon}_tp"
        except:
            pass
        try:
            for elem in shutil_OB_root.find('helpers').findall('helper'):
                if def_att in elem.attrib['name']:
                    elem.attrib['name'] = f"{weapon}_{def_att}"
        except:
            pass
    else:
        for elem in shutil_OB_root.find('helpers').findall('helper'):
            if def_att in elem.attrib['name']:
                elem.attrib['name'] = f"{weapon}_{def_att}"

    # common settings
    for elem in shutil_OB_root.find('geometry').findall('firstperson'):
        elem.attrib['name'] = f"objects/weapons/{weapon}/{weapon}_{def_att}.cgf"
    for elem in shutil_OB_root.find('geometry').findall('thirdperson'):
        elem.attrib['name'] = f"objects/weapons/{weapon}/{weapon}_{def_att}_tp.cgf"

    for elem in shutil_OB_root.find('materials').findall('material'):
        if elem.attrib['name'] == "default":
            if skin == 'default':
                elem.attrib['file'] = f"objects/weapons/{weapon}/{weapon}_{def_att}.mtl"
                elem.attrib['tpfile'] = f"objects/weapons/{weapon}/{weapon}_{def_att}_tp.mtl"
            else:
                elem.attrib['file'] = f"objects/weapons/{weapon}/{weapon}_{def_att}.mtl"
                elem.attrib['tpfile'] = f"objects/weapons/{weapon}/{weapon}_{def_att}_tp.mtl"
        elif elem.attrib['name'] != "default":
            pass
            # shutil_OB_root.find('materials').remove(elem)

    with open(dst_obj_path, 'wt') as f:
        f.write(pretty_print(shutil_OB_root))
        # ------------------- 

    root_obj = ET.parse(dst_obj_path).getroot()
    
    if skin == 'default':
        pass
    else:
        # remove skin material if exists
        for element in root_obj.find('materials').findall('material'):
            if element.attrib['name'] == skin:
                root_obj.find('materials').remove(element)

        # add new material
        for element in root_obj.find('materials').findall('material'):
            ET.SubElement(root_obj.find('materials'), 'material',
                            name=skin,
                            file=f"objects/weapons/{weapon}/{i}",
                            tpfile=f"objects/weapons/{weapon}/{i.replace('.', '_tp.')}")
            break

    with open(dst_obj_path, 'wt') as f:
        f.write(pretty_print(root_obj))

    # ----------------
    # to Accessories '_d'
    # ----------------
    
    if 'fl0' in def_att:
        # fl fix
        src_acc_path = it_acc_Repo + f'\\fl02_rift01_console.xml'
        dst_acc_path = it_acc_Skin + f'\\fl02_rift01_console.xml'
    else:
        # work path
        src_acc_path = it_acc_Repo + f'\\{weapon}_{def_att}.xml'
        dst_acc_path = it_acc_Skin + f'\\{weapon}_{def_att}.xml'
    try:
        shutil.copyfile(src_acc_path, dst_acc_path)
    except FileNotFoundError:
        
        open(dst_acc_path, 'a').close()
        
        # if attach doesn't exist
        for root, dirs, files in os.walk(it_acc_Repo):
            files = files
            break
        
        for file in files:
            if def_att + '.xml' in file:
                acc_donor = file
            else:
                continue
            break
        shutil.copyfile(f"{it_acc_Repo}\\{acc_donor}", dst_acc_path)

    # ----------------- make it worthy for Items
    shutil_root = ET.parse(dst_acc_path).getroot()
    shutil_root.attrib['name'] = weapon + '_' + def_att
    shutil_root.attrib['view_settings'] = f"objects/weapons/{weapon}/{weapon}_{def_att}.xml"
    try:
        for elem in shutil_root.find('content').findall('item'):
            elem.attrib['name'] = weapon + '_' + def_att
    except:
        pass
    for elem in shutil_root.find('drop_params').findall('item'):
        elem.attrib['name'] = weapon + '_' + def_att
    # for elem in shutil_root.find('types').findall('type'):
    #     elem.attrib['name'] = weapon + '_' + def_att
    with open(dst_acc_path, 'wt') as f:
        f.write(pretty_print(shutil_root))
    # -----------------

    root_acc = ET.parse(dst_acc_path).getroot()

    # if default material doesn't exist
    for element in root_acc:
        if element.tag == 'skins':
            break
        else:
            ET.SubElement(root_acc, 'skins')
            ET.SubElement(root_acc.find('skins'), 'material', name='default')
            break

    # remove skin if exists
    for elem in root_acc.find('skins').findall('material'):
        if elem.attrib['name'] == skin:
            root_acc.find('skins').remove(elem)

    # add new skin
    ET.SubElement(root_acc.find('skins'), 'material', name=skin)

    with open(dst_acc_path, 'wt') as f:
        f.write(pretty_print(root_acc))
#=========================================================
# KNIVES (old)
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
                
    # remove skin material if exists, except 'default'
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
    
    # add new skin material
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
# WEAPONS (old)
#=========================================================
def WE_exist_Obj(kn_Files, Obj_SkinPath, sa_list):

    root = ET.parse(Obj_SkinPath).getroot()

    for i in kn_Files:
        if '.mtl' in i:
            if ' ' in i:
                sg.popup_error(f'Unavailable indent in naming\n[{i}]')
                idi = i.replace(' .mtl', '.mtl')
                kn_Files.remove(i)
                kn_Files.append(idi)

    for i in kn_Files:
        if i.endswith('_tp.mtl') and 'sa0' not in i:

    # define material
            name = i.split('_tp')[0]
            item = name.split('_')[0]
            material = materialle(i)

    # if "helpers" tag doesnt exist
    with open(Obj_SkinPath, 'r+') as f:
        if "<helpers>" not in f and len(sa_list) > 0:
            ET.SubElement(root, 'helpers')
            f.close()
        else:
            pass
        f.close()

    # remove equal helper if exist
    try:
        for elem in root.find('helpers').findall('helper'):
            if material in elem.attrib['name']:
                root.find('helpers').remove(elem)
    except:
        pass

    # create helper, if "sa" enabled  
    for sa in sa_list:
        ET.SubElement(root.find('helpers'), 'helper',
                                angles="0.000,-0.000,0.000",
                                bone="weapon",
                                name=f"{name}_saslot{sa.strip('sa')}",
                                offset="0.00000,0.00000,0.00000")
    
    # skin material if exist
    try:
        for element in root.find('materials').findall('material'):
            if element.attrib['name'] == material:
                if material == 'default':
                    pass
                else:
                    root.find('materials').remove(element)
    except:
        pass

    # add new skinmaterial
    try:
        for element in root.find('materials').findall('material'):
            if material == 'default':
                pass
            else:
                ET.SubElement(root.find('materials'), 'material',
                                name=material,
                                file=f"objects/weapons/{item}/{name}.mtl",
                                tpfile=f"objects/weapons/{item}/{name}_tp.mtl")
            break
    except:
        pass
    with open(Obj_SkinPath, 'wt') as f:
        f.write(pretty_print(root))    
#---------------------------------------------------------
def WE_exist_It(kn_Files, It_SkinPath, sa_list):
    
    for i in kn_Files:
        if i.endswith('_tp.mtl') and 'sa0' not in i:

            # define material
            material = materialle(i)
            name = i.split('_tp')[0]
            item = name.split('_')[0]

    root = ET.parse(It_SkinPath).getroot()

    # remove skin if exists
    try:
        for element in root.find('skins').findall('material'):
            if element.attrib['name'] == material:
                root.find('skins').remove(element)
    except:
        pass
    
    # add new skin
    try:
        ET.SubElement(root.find('skins'), 'material', name=material)
    except:
        pass
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
    try:
        ET.SubElement(ET.SubElement(root, 'skin_content'), 'item')
        for skin_material in root.find('skins').findall('material'):
            ET.SubElement(root.find('skin_content'),'item',
                                            name=f"{item}_{skin_material.attrib['name']}_shop")
    except:
        pass

    with open(It_SkinPath, 'wt') as f:
        f.write(pretty_print(root))
    
    # --------------------------------
    # create equal xml for skin
    # --------------------------------
    try:
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
    except:
        pass
#=========================================================
# KNIVES (new)
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
# WEAPONS (new)
#=========================================================
def WE_new_Obj(kn_Files, Obj_SkinPath, sa_list):
    kn_Files.sort(reverse=True)
    
    temp_ss = []
    root = ET.parse(Obj_SkinPath).getroot()
    
    for i in kn_Files:
        if i.endswith('_tp.mtl') and 'sa0' not in i:
            temp_ss.append(i)
    
    for i in kn_Files:
        if i.endswith('_tp.mtl') and 'sa0' not in i:
    # define material
            if '_console' in i:
                name = i.split('_tp')[0]
                item = name.split('_')[0]
                material = materialle(i)

                if material == 'default':
                    file = f"objects/weapons/{item}/{item}.mtl"
                    tpfile = f"objects/weapons/{item}/{item}_tp.mtl"
                else:
                    file = f"objects/weapons/{item}/{item}.mtl"
                    tpfile = f"objects/weapons/{item}/{item}_tp.mtl"

            else:
                name = i.split('_tp')[0]
                item  = i.split('_')[0]
                material = materialle(i)

                
                if material == 'default':
                    file = f"objects/weapons/{item}/{item}.mtl"
                    tpfile = f"objects/weapons/{item}/{item}_tp.mtl"
                else:
                    file = f"objects/weapons/{item}/{item}_{material}.mtl"
                    tpfile = f"objects/weapons/{item}/{item}_{material}_tp.mtl"

    # if "helpers" tag doesnt exist
    with open(Obj_SkinPath, 'r+') as f:
        if "<helpers>" not in f and len(sa_list) > 0:
            ET.SubElement(root, 'helpers')
            f.close()
        else:
            pass
        f.close()

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

    for model in kn_Files:
        if '.chr' in model and material in model:
            for geometry in root.find('geometry').findall('firstperson'):
                geometry.attrib['name'] = f"objects/weapons/{item}/{model}"
        elif '_tp.cgf' in model and material in model and 'sa0' not in model:
            for geometry in root.find('geometry').findall('thirdperson'):
                geometry.attrib['name'] = f"objects/weapons/{item}/{model}"
        else:
            pass
    
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
    for it in temp_ss:
        full = it.split('_tp')[0]
        weapon = it.split('_')[0]
        ET.SubElement(root.find('materials'), 'material',
                                    name=materialle(it.split('_tp')[0]),
                                    file=f"objects/weapons/{weapon}/{full}.mtl",
                                    tpfile=f"objects/weapons/{weapon}/{full}_tp.mtl")

    #     ET.SubElement(root.find('materials'), 'material',
    #                             name=material,
    #                             file=file,
    #                             tpfile=tpfile)
        
    
    with open(Obj_SkinPath, 'wt') as f:
        f.write(pretty_print(root)) 
#---------------------------------------------------------
def WE_new_It(kn_Files, It_SkinPath, sa_list):
    
    temp_ss = []
    for i in kn_Files:
        if i.endswith('_tp.mtl') and 'sa0' not in i:
            temp_ss.append(i)
    
    for i in kn_Files:
        if i.endswith('_tp.mtl') and 'sa0' not in i:
            temp_ss.append(i)
    
    # define material
            if '_console' in i:
                name = i.split('_tp')[0]
                item = name.split('_')[0]
                material = materialle(i)
            
            else:
                name = i.split('_tp')[0]
                item  = i.split('_')[0]
                material = materialle(i)
            break

    root = ET.parse(It_SkinPath).getroot()

    # remove tags
    try:
        for skin_content in root.find('skins').findall('material'):
            if skin_content.attrib['name'] != material:
                root.find('skins').remove(skin_content)
        for skin_content in root.find('skins').findall('attach'):
            root.find('skins').remove(skin_content)
        
        if material == 'default':
            pass
        else:
            ET.SubElement(root.find('skins'), 'material', name=material)
    except AttributeError:
        ET.SubElement(ET.SubElement(root, 'skins'), 'material', name=material)

    # КОСТЫЛИ УРА
    for it in temp_ss:
        mat = materialle(it.split('_tp')[0])
        if mat == 'default':
            pass
        else:
            ET.SubElement(root.find('skins'), 'material',
                                    name=mat)

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

        if 'kn49' in kn_item:
            It_RepoPath = it_weap_Repo + f"\\kn49_chrome_console.xml"
            Obj_RepoPath = obj_weap_Repo + f"\\{kn_item}\\kn49_chrome_console.xml"

            It_SkinPath = it_weap_Skin + f"\\kn49_chrome_console.xml"
            Obj_SkinPath = obj_weap_Skin + f"\\{kn_item}\\kn49_chrome_console.xml"
        
        else:
            # working path
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
    ss_list = {
                'ar13':'ar13_drum_01_console',
                'ar13_drum_01_console':'ar13',
                'smg04':'smg04_tape01_console',
                'shg01':'shg01_rope01_console',
                'shg40':'shg40_rift01_console',
                'sr02':'sr02_tape02_console'
                }
    # working path
    for we_item in weapons_orig:
        if we_item not in ss_list:
            It_RepoPath = it_weap_Repo + f"\\{we_item}.xml"
            Obj_RepoPath = obj_weap_Repo + f"\\{we_item}\\{we_item}.xml"

            It_SkinPath = it_weap_Skin + f"\\{we_item}.xml"
            Obj_SkinPath = obj_weap_Skin + f"\\{we_item}\\{we_item}.xml"
        
        else:
            if 'ar13' in we_item:
                we_item_spec = spec_window(we_item, ss_list[we_item])
                # ----------
                It_RepoPath = it_weap_Repo + f"\\{we_item_spec}.xml"
                Obj_RepoPath = obj_weap_Repo + f"\\{we_item_spec}\\{we_item_spec}.xml"

                It_SkinPath = it_weap_Skin + f"\\{we_item_spec}.xml"
                Obj_SkinPath = obj_weap_Skin + f"\\{we_item_spec}\\{we_item_spec}.xml"
                
            else:
                we_item_spec = spec_window(we_item, ss_list[we_item])
                # ----------
                It_RepoPath = it_weap_Repo + f"\\{we_item_spec}.xml"
                Obj_RepoPath = obj_weap_Repo + f"\\{we_item}\\{we_item_spec}.xml"

                It_SkinPath = it_weap_Skin + f"\\{we_item_spec}.xml"
                Obj_SkinPath = obj_weap_Skin + f"\\{we_item}\\{we_item_spec}.xml"
        
        # items list (for knives)
        we_Files = scan(obj_weap_Skin, we_item)

        # sa_list
        sa_list = list()
        for i in we_Files:
            if '_sa' in i and i.endswith('.mtl') and 'tp' not in i:
                if 'sa_d' in i:
                    i = i.split('.')[0]
                else:
                    i = i.split('_')[-1].split('.')[0]
                sa_list.append(i)

        for i in we_Files:
            if '_sa' in i:
                sa_Acc_SkinPath = f"{it_acc_Skin}\\{i.split('.')[0]}.xml"
                sa_Obj_SkinPath = obj_weap_Skin + f"\\{we_item}\\{i.split('.')[0]}.xml"

                if i.endswith(".cgf") and '_tp' not in i:

                    SA_Obj(i, we_item, we_Files, sa_Obj_SkinPath)
                    SA_Acc(i, we_item, sa_Acc_SkinPath)
            else:
                pass

        # _d files
        ss = ['ss', 'sc', 'gp', 'sp', 'is', 'rds', 'as', 'gs', 'bp', 'fl', 'sa' ]
        for i in we_Files:
            
            if i.endswith('_d.mtl') and 'console' not in i and 'sa0' not in i:
                # weapon name
                weapon = i.split('_')[0]

                # _d attachment type
                complex_naming = i.split('.')[0].split('_')
                complex_naming.remove(complex_naming[-1])

                for elem in complex_naming:
                    if elem.strip('0123456789') in ss:
                        def_att = elem + '_d'
                        break

                # material name
                if len(complex_naming[1]) > 4:
                    try:
                        skin = i.split('_')[1]
                    except IndexError:
                        skin = 'default'
                else:
                    skin = 'default'

                # _d attachments
                Default_attach(i, weapon, skin, def_att)
            
            # complex old attachment [console_sp01, console_rds01]
            
            elif i.split('_')[0] in ss_list and i.split('_')[-1].split('.')[0].strip('0123456789') in ss and i.endswith('.mtl'):
                com_attach = i.split('_')[-1].split('.')[0].split('.')[0]

                # skin = materialle(i.split('.')[0])
                s = i.split('_'+com_attach)[0]
                skin = materialle(s)

                print("[com_attach]")
                print(com_attach)
                print("[item]")
                print(i)
                print("[skin]")
                print(skin)
                print('---------------')
                atl_weapon = i.split('_')[0]
                # try:
                weapon = ss_list[atl_weapon]

                Default_attach(i, weapon, skin, com_attach)
                # except:
                    # pass
                # ---------------

        if path.exists(It_RepoPath) and path.exists(Obj_RepoPath):
            try:
                shutil.copyfile(Obj_RepoPath, Obj_SkinPath)
                shutil.copyfile(It_RepoPath, It_SkinPath)
            except FileNotFoundError:
                sg.popup_error(f'invalid source path\n{Obj_RepoPath}\n{It_RepoPath}')
                break

            # old weapon
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

            try:
                shutil.copyfile(f"{obj_weap_Repo}\\{ask_base}\\{ask_base}.xml", Obj_SkinPath)
                shutil.copyfile(f"{it_weap_Repo}\\{ask_base}.xml", It_SkinPath)
            except FileNotFoundError:
                sg.popup_error(f'{i} FileNotFoundError')

            
            # new weapons
            WE_new_Obj(we_Files, Obj_SkinPath, sa_list)
            WE_new_It(we_Files, It_SkinPath, sa_list)
    
    print('dd')
    print('dd')
#---------------------------------------------------------
def create_XML(obj_weap_Skin):
    for path_root, path_dirs, path_files in os.walk(obj_weap_Skin):
        for it in path_dirs:
            if 'kn' in it:
                weapons_kn.append(it)
            elif 'kn' not in it and '_console' not in it:
                weapons_orig.append(it)

            elif 'kn' not in it and '_console' in it:
                weapons_orig.append(it)
                weapons_console.append(it)
        break
    
    print('knives\n',weapons_kn,'\n')
    print('weapons\n', weapons_orig, '\n')
    print('console_weapons\n', weapons_console, '\n')

    Knives(weapons_kn)
    Weapons(weapons_orig)
    # console_Weapons(weapons_console)

#=========================================================
# DRIVE
#=========================================================
def main():
    fileStructure(it_weap_Skin, it_acc_Skin, obj_weap_Skin, obj_att_Skin)
    create_XML(obj_weap_Skin)
    obj_att__vs__item_acc(client_att, rep_att)
    sg.popup_notify('Complete')

if __name__ == "__main__":
    
    wfc_repo, skin_repo = Ask_Path()
    
    # split
    weapons_kn = list()
    weapons_orig = list()
    weapons_console = list()

    # # ==================TEST_PATH==================================
    # wfc_repo = os.path.abspath("e:\\wfpc-minsk\\Game")
    # skin_repo = os.path.abspath("d:\\__some_get_come__\\__test_Weapon\\Game")
    # skin_repo = os.path.abspath("d:\\__some_get_come__\\console_weapons\\Game")
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

    #---------third party script path
    path_skin = skin_repo
    client_att = obj_att_Repo
    rep_att = obj_att_Skin
    acc_att = it_acc_Repo
    rep_acc = it_acc_Skin

    main()
    
