import os
from os import path
from typing import ItemsView
import PySimpleGUI as sg
import time

sg.theme('Dark2')

#---------------------------------------------------------
def Ask_Path():

    path_widget = [

        [sg.Text('Insert your WFC repo path', text_color='#ebd234')],
        [sg.InputText(default_text = r"c:\wf-skins-minsk", key = "-REPO-"), sg.FolderBrowse()],
        [sg.Text("Skin absolute path ('Game' folder)", text_color='#ebd234')],
        [sg.InputText(default_text = r"d:\__some_get_come__\_test_Armor\Game", key = "-SKINS-"), sg.FolderBrowse()],

        [sg.OK(key='OK'), sg.Cancel()]
    ]
    window = sg.Window('', path_widget, no_titlebar=True)

    while True:
        event, values = window.read(close=True)

        wfc_repo = values["-REPO-"]
        skin_repo = values["-SKINS-"]

        if event == 'OK':
            return wfc_repo, skin_repo
        if event in ('Cancel', None) or event == sg.WIN_CLOSED:
            break
        
    window.close()
# --------------------------------------------------------
def fileStructure(skin_repo):
    
    items_armor = skin_repo + '\\Items\\Armor'
    items_skins = skin_repo + '\\Items\\Skins'

    # ==============================
    def check_and_create(pppath):
        if os.path.exists(pppath) == True:
            pass
            sg.Print(f'{items_armor} already exists', text_color='blue')
        else:
            os.makedirs(pppath)
            sg.Print(f'Created path: {items_armor}', text_color='blue')
    # ==============================

    check_and_create(items_armor)
    check_and_create(items_skins)
#---------------------------------------------------------
def create_empty_xml(xml):
    try:
        open(xml, 'a').close()
        sg.Print(f"> Creating xml...\n{xml}", text_color='grey20')
    except FileExistsError:
        pass
#---------------------------------------------------------
def if_no_chr(root, lst, container):
    for file in lst:
        lst_file = []
        if file.endswith('chr'):
            lst_file.append(file)
            break
        else:
            pass
    
        if len(lst_file) == 0:
            # print(f'\n{root}\n')
            item = root.split('\\')[-1]

            separator = '----'*13
            sg.Print(f"\n{separator}\nClarifying .chr for [{item}]")
            
            ask = sg.PopupGetText(f"What .chr was used for [{item}] ?",
                                    size=(60, 20),
                                    title=f"Clarifying .chr for [{item}]",
                                    no_titlebar=True,
                                    text_color='#ebd234')
            ask_it = []
            ask_it.append(ask)
            ask_it.append(root.replace('\\', '/'))

            sg.Print(f'{ask}\n{separator}', text_color='purple')
            if '_hands_' in file:
                if '_b' in file:
                    container.update({item:ask_it})
                    container.update({f"{item}_b":ask_it})
                    container.update({f"{item}_fp":ask_it})
                    container.update({f"{item}_fp_b":ask_it})
                    container.update({f"{item}_hp":ask_it})
                    container.update({f"{item}_hp_b":ask_it})
                    break
                else:
                    container.update({item:ask_it})
                    container.update({f"{item}_fp":ask_it})
                    container.update({f"{item}_hp":ask_it})
                    break

            if '_helmet' in file:
                if '_b' in file:
                    container.update({item:ask_it})
                    container.update({f"{item}_b":ask_it})
                    break
                else:
                    container.update({item:ask_it})
                    break

            if '_shoes_' in file:
                if '_b' in file:
                    container.update({item:ask_it})
                    container.update({f"{item}_b":ask_it})
                    break
                else:
                    container.update({item:ask_it})
                    break

            if '_vest_' in file:
                if '_b' in file:
                    container.update({item:ask_it})
                    container.update({f"{item}_b":ask_it})
                    break
                else:
                    container.update({item:ask_it})
                    break
        else:
            pass
# --------------------------------------------------------
def extsort(files):
    return sorted(files,key=lambda x: os.path.splitext(x)[1]) #    *.xml, *chr, *.mtl ---> *chr, *.mtl, *.xml,   
#---------------------------------------------------------
def templates_Promt(wfc_repo, special_word):
    templates_path = wfc_repo + "\\Game\\Objects\\Characters\\!Templates"
    t_prompt = []
    
    for t_root, t_dir, t_files in os.walk(templates_path):
        for i in t_files:
            if "AI_" in i:
                pass
            
            for elem in special_word:
                if elem in i.lower():
                    t_prompt.append(i.split('.')[0])
                else:
                    pass
    return t_prompt
# --------------------------------------------------------
def templ_window(file, special_word):
    
    t_prompt = templates_Promt(wfc_repo, special_word)
    
    file_widget = [

        [sg.Text(f'Choose your Template for [{file}]', text_color='#ebd234')],
        [sg.Combo(t_prompt, key = "-TEMPLATE-", size=(30, 13), default_value=t_prompt[0])],

        [sg.OK(key='OK'), sg.Cancel()]
    ]
    window = sg.Window('buy my game', file_widget, no_titlebar=True)

    while True:
        event, values = window.read(close=True)

        if event == 'OK':
            template = values["-TEMPLATE-"]
            return template
        if event in ('Cancel', None) or event == sg.WIN_CLOSED:
            break
    window.close()
#---------------------------------------------------------
def xml_Obj_CommonForm(path, file):

    material_file = file
    obj_path = path.split('Game/')[1]
    armor_type = file.split('_')[1].split('_')[0].title()

    if '_hands_' in file:
        if '_fp' in file:
            special_word = ['FP_', 'fp']

        elif '_hp' in file:
            special_word = ['HP_', 'hp']
            
        else:
            special_word = ['hands', 'arms']

    elif '_vest_' in file:
        special_word = ["_jacket", 'body', 'vest']

    elif '_shoes_' in file:
        special_word = ['pants', 'shoes', 'legs']

    elif 'helmet' in file:
        armor_type = f"Helmets"
        special_word = ['helmet', 'helmets', 'Head']

    # setup
    if "_hp" in file:
        armor_type = f"HP_{armor_type}"
        material_file = file.replace("_hp", "_fp")
    elif "_fp" in file:
        armor_type = f"FP_{armor_type}"
    else:
        pass

    template = templ_window(file, special_word)
    # ------------------------------
    if "_hands_" in file or "_shoes_" in file:
        xml_addon = ''
    else:
        xml_addon = f"""\n\t<Model File="" FGTFile="" DecalsMask="" Gender="Female">
        <Morphs />    <!-- MANUAL_EDIT -->
        <Switches />
        <Materials />
        <Sockets />
    </Model>"""
    # ------------------------------
    if file.endswith('_b'):
        ss = file.rsplit('_b', 1)[0]
    else:
        ss = file

    xml_content = f"""<CharacterPart Name="{file}" Slot="{armor_type}" Template="{template}">
    <Model File="{obj_path}/{ss}.chr" FGTFile="" DecalsMask="" Gender="Male">
        <Morphs />    <!-- MANUAL_EDIT -->
        <Switches />
        <Materials>
            <Material Name="default" File="{obj_path}/{file}.mtl"/>
        </Materials>
        <Sockets />
        </Model>{xml_addon}\n</CharacterPart>"""

    path = f"{path}/{file}.xml"
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(xml_content)
        sg.Print(f"{file}.xml done...\n", text_color="#9c5325")
        f.close()
#---------------------------------------------------------
def xml_Obj_FbsForm(path, file):

    material_file = file
    obj_path = path.split('Game/')[1]
    armor_type = file.split('_')[1].split('_')[0].title()

    if 'arms' in file:
        if '_fp' in file:
            armor_type = 'fbs_fp_arms'
            special_word = ['FP_', 'fp']

        elif '_hp' in file:
            armor_type = 'fbs_hp_arms'
            material_file = file.replace('_hp', '_fp')
            special_word = ['HP_', 'hp']
        else:
            special_word = ['hands', 'arms']

    elif 'body' in file:
        armor_type = 'fbs_body'
        special_word = ["_jacket", 'body', 'vest']

    elif 'legs' in file:
        armor_type = 'Shoes_Type4'
        special_word = ['pants', 'shoes', 'legs']

    elif 'helmet' in file:
        armor_type = 'fbs_helmet'
        special_word = ['helmet', 'helmets', 'Head']
        
    else:
        armor_type = "fbs_¯ \ _ (ツ) _ / ¯"

    template = templ_window(file, special_word)

    fbs_string = f"""
    <CharacterPart Name="{file}" Slot="{armor_type}" Template="{template}">
        <Model File="{obj_path}/{file}.chr" FGTFile="" DecalsMask="" Gender="Male">
        <Morphs>    <!-- MANUAL_EDIT -->
        </Morphs>    <!-- MANUAL_EDIT -->
        <Switches />    
        <Materials>
            <Material Name="default" File="{obj_path}/{material_file}.mtl"/>
        </Materials>
            <Sockets /> 
        </Model>
        <Model File="" FGTFile="" DecalsMask="" Gender="Female">
            <Morphs />
            <Switches />    
            <Materials />
            <Sockets />
        </Model>
    </CharacterPart>"""

    path = f"{path}/{file}.xml"
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(fbs_string)
        sg.Print(f"{file}.xml done...\n", text_color="#9c5338")
        f.close()
#---------------------------------------------------------
def xml_Obj_NoChrForm(path, file, user_input):

    material_file = file
    obj_path = path.split('Game/')[1].split(file)[0]
    armor_type = file.split('_')[1].split('_')[0].title()

    # setup
    if '_hands_' in file:
        if '_fp' in file:
            special_word = ['FP_', 'fp']
        elif '_hp' in file:
            special_word = ['HP_', 'hp']
        else:
            special_word = ['hands', 'arms']

    elif '_vest_' in file:
        special_word = ["_jacket", 'body', 'vest']

    elif '_shoes_' in file:
        special_word = ['pants', 'shoes', 'legs']

    elif 'helmet' in file:
        armor_type = "Helmets"
        special_word = ['helmet', 'helmets', 'Head']

    if "_hp" in file:
        armor_type = f"HP_{armor_type}"
        material_file = file.replace('_hp', '_fp')
    elif "_fp" in file:
        armor_type = f"FP_{armor_type}"
    else:
        pass

    template = templ_window(file, special_word)
    # ------------------------------
    if "_alala_" in file:
        xml_addon = ''
    else:
        xml_addon = f"""\n\t<Model File="" FGTFile="" DecalsMask="" Gender="Female">
        <Morphs />    <!-- MANUAL_EDIT -->
        <Switches />
        <Materials />
        <Sockets />
    </Model>"""
    # ------------------------------

    xml_content = f"""<CharacterPart Name="{file}" Slot="{armor_type}" Template="{template}">
    <Model File="{obj_path.strip(obj_path.rsplit('/')[-1])}{user_input}/{user_input}.chr" FGTFile="" DecalsMask="" Gender="Male">
        <Morphs />    <!-- MANUAL_EDIT -->
        <Switches />
        <Materials>
            <Material Name="default" File="{obj_path}/{material_file}.mtl"/>
        </Materials>
        <Sockets />
    </Model>{xml_addon}\n</CharacterPart>"""

    path = f"{path}/{file}.xml"
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(xml_content)
        sg.Print(f"{file}.xml done...\n", text_color="#9c5325")
        f.close()
#---------------------------------------------------------
def xml_itemForm(file, files, path):
    item = file

    # maps
    # ----------------------
    val_map = {
        "sniper":"S",
        "engineer":"E",
        "medic":"M",
        "soldier":"R",
        "shared":"MERS",
        "gunner":"H"
    }
    # ----------------------
    apart_map = {
        "hands":["Gloves", "mat_armor_arms"],
        "helmet":["Helmet", "mat_head"],
        "vest":["Vest", "mat_armor_body"],
        "shoes":["Boots", "mat_armor_legs"]
    }
    # ----------------------

    item_class = item.split('_')[0]
    item_part = item.split('_')[1].split('_')[0]
    cl_val = val_map[item_class]

    item_string = f"""<GameItem name="{file}" type="armor">
	<mmo_stats>
		<param name="item_category" value="{apart_map[item_part][0]}"/>
		<param name="shopcontent" value="1"/>
		<param name="classes" value="{cl_val}"/>
		<param name="durability" value="36000"/>
		<param name="repair_cost" value="300_bucks"/>    <!-- MANUAL_EDIT -->
	</mmo_stats>
	<UI_stats>
		<param name="name" value="@ui_armor_{file}_name"/>
		<param name="description" value="@ui_armor_{file}"/>
		<param name="icon" value="{item}"/>    <!-- MANUAL_EDIT -->
	</UI_stats>
	<slots>
		<slot main="1" name="{item_part}">
			<materials>
				<Material default="1" display_name="black" icon="mat_black" name="default" surface_type="{apart_map[item_part][1]}"/>
			</materials>
			<assets>
			</assets>
		</slot>
	</slots>
	<GameParams>    <!-- MANUAL_EDIT -->
		<param name="armorHealth" value="125"/>
        <param name="extra_ammo_primary_mul" value="1.5"/>
        <param name="extra_ammo_pistol_mul" value="1.5"/>
        <param name="select_duration_mul" value="0.95"/>
        <param name="deselect_duration_mul" value="0.95"/>
	</GameParams>    <!-- MANUAL_EDIT -->\n</GameItem>"""


    open(path, 'a').close()
    with open(path, 'w') as f:
        f.writelines(item_string)
        f.close()
    lst = []
    with open(path, 'r+') as f:
        for i in f:
            lst.append(i)
    for file in files:
        lst.insert(19, f"\t\t\t\t{file}\n")

    with open(path, 'w') as ff:
        ff.writelines(lst)
        ff.close()
#---------------------------------------------------------
def xml_itemFBS(file, files, path):
    item = file

    val_map = {
        "sniper":"S",
        "engineer":"E",
        "medic":"M",
        "soldier":"R",
        "shared":"MERS"
    }

    if item.startswith('f_'):
        item_class = item.split('f_')[1].split('_')[0]
        cl_val = val_map[item_class]
    else:
        item_class = item.split('_')[0]
        cl_val = val_map[item_class]
    

    if item.startswith('f_'):
        female_addon = """\n\t\t<optional_stats>
            <param name="voice_alias" value="voice_6"/>
            <param name="compound_base_override" value="objects/characters/human/compound_base_female.chr"/>
        </optional_stats>"""
    else:
        female_addon = ''

    item_string = f"""<GameItem name="{file}" type="armor">
	<mmo_stats>
		<param name="item_category" value="skin"/>
		<param name="shopcontent" value="1"/>
		<param name="classes" value="{cl_val}"/>
	</mmo_stats>
	<UI_stats>
		<param name="name" value="@ui_armor_{file}_name"/>
		<param name="description" value="@ui_armor_{file}"/>
		<param name="icon" value="{file}"/>
	</UI_stats>{female_addon}
    <visually_hidden_slots>
        <slot name = "vest"/>
        <slot name = "shoes"/>
        <slot name = "helmet"/>
        <slot name = "chest"/>
        <slot name = "arms"/>
        <slot name = "gloves"/>
        <slot name = "pants"/>
        <slot name = "boots"/>
        <slot name = "legarmor"/>
    </visually_hidden_slots>
	<slots>
		<slot main="1" name="skin">
			<materials>
				<Material default="1" display_name="black" icon="mat_black" name="default" surface_type="mat_armor_body"/>
			</materials>
			<assets>
			</assets>
		</slot>
	</slots>
	<GameParams>    <!-- MANUAL_EDIT -->
        <param name="sprint_time_mul" value="1.4"/>
	</GameParams>    <!-- MANUAL_EDIT -->\n</GameItem>"""

    open(path, 'a').close()
    with open(path, 'w') as f:
        f.writelines(item_string)
        f.close()
    lst = []
    with open(path, 'r+') as f:
        for i in f:
            lst.append(i)
    for file in files:
        if len(female_addon) < 10:
            lst.insert(29, f"\t\t\t\t{file}\n")
        else:
            lst.insert(32, f"\t\t\t\t{file}\n")

    with open(path, 'w') as ff:
        ff.writelines(lst)
        ff.close()
#---------------------------------------------------------
def scan_path(skin_repo):

    root_worklist = []
    yes_chr = []
    no_chr = {}

    for root, dirs, files in os.walk(skin_repo):
        path_dirs = dirs

        for d in path_dirs:
            if 'textures' in d:
                root_worklist.append(root)

    for root in root_worklist:

        # items_emptyXML
        # ===============================
        file_name = root.split("\\")[-1]
        if '_fbs_' in root:
            xml_item_path = f"{skin_repo}\\Items\\Skins\\{file_name}.xml"
            create_empty_xml(xml_item_path)
        else:
            xml_item_path = f"{skin_repo}\\Items\\Armor\\{file_name}.xml"
            create_empty_xml(xml_item_path)
        # ===============================

        for b_root, _, b_files in os.walk(root):

            check_files = []
            for element in b_files:
                if '.chr' in element:
                    check_files.append(element)
                elif '.mtl' in element:
                    check_files.append(element)
                else:
                    pass

            check_files = extsort(check_files)
            for f in check_files:
                b_root = b_root.replace("\\", "/")
                
                if f.endswith('.chr'):
                    item = f.split('.')[0]
                    a_item = (b_root, item)
                    if a_item not in yes_chr:
                        yes_chr.append(a_item)
                        sg.Print(f'\nWorking with [.chr] {root}', text_color='blue')
                
                if '_b.mtl' in f:
                    for f in check_files:
                        if '.chr' in f:
                            item_01 = f.split('.')[0]
                            item_02 = f.replace('.chr', '_b')

                            item = (b_root, item_01)
                            b_item = (b_root, item_02)

                            if item not in yes_chr:
                                yes_chr.append(item)
                                sg.Print(f'\nWorking with [.mtl] {root}', text_color='dark blue')
                            if b_item not in yes_chr:
                                yes_chr.append(b_item)
                                sg.Print(f'\nWorking with [.mtl] {root}', text_color='dark blue')

            # ======================================
            if_no_chr(root, check_files, no_chr)
            # ======================================
        
    sg.Print('\nRequired xml:', text_color='orange')
    time.sleep(0.5)

    separator = '----'*13

    for i in yes_chr:
        sg.Print(f">> Root:\n{i[0]}\n>> Files:\n{i[1]}.xml\n{separator}", text_color='dark green')
        # time.sleep(0.1)

    for i in no_chr:
        sg.Print(f">> Root:\n{no_chr[i][1]}\n>> Files:\n{i}.xml\n>> Clarifying\n{no_chr[i][0]}\n{separator}", text_color='dark green')
        # time.sleep(0.1)
    return yes_chr, no_chr
#---------------------------------------------------------
def create_XFile(skin_repo):
    yes_chr, no_chr = scan_path(skin_repo)

    # ----------------------------YES_CHR
    for content_tuple in yes_chr:
        obj_xml = content_tuple[0] + '\\' + content_tuple[1] + '.xml'
        create_empty_xml(obj_xml)

        if '_fbs_' in content_tuple[1]:
            xml_Obj_FbsForm(content_tuple[0], content_tuple[1])
        else:
            xml_Obj_CommonForm(content_tuple[0], content_tuple[1])

    # ----------------------------NO_CHR
    for content_map in no_chr:
        obj_xml = no_chr[content_map][1] + '\\' + content_map + '.xml'
        create_empty_xml(obj_xml)

        if '_fbs_' in content_map:
            pass
        else:
            xml_Obj_NoChrForm(
                        no_chr[content_map][1],    # file_root
                        content_map,               # file_name
                        no_chr[content_map][0])    # user input_name
#---------------------------------------------------------
def create_ZFile(skin_repo):
    # xml for "items" Folder

    xml_lst = []
    xml_items_path = skin_repo + "\\Items"
    for root, dies, files in os.walk(xml_items_path):
        for i in files:
            i = i.split('.')[0]

    # fbs, f_fbs
            if '_fbs_' in i:
                # f_female -------------------------------
                if i.startswith('f_'):

                    item_class = i.split('_fbs')[0].split('f_')[1]
                    work_path = skin_repo + f'\\Items\\Skins\\{i}.xml'
                    obj_path = skin_repo + f'\\Objects\\Characters\\{item_class}\\female\\fb_suits\\{i}'
                    # -----------
                    sg.Print("\n[f_female]", text_color='blue')
                    sg.Print(work_path.split('.xml')[0], '\n', text_color='green')
                    # -----------
                    for _,_,f in os.walk(obj_path):
                        for item in f:
                            if item.endswith('.xml'):
                                
                                if '_b.xml' in item:
                                    idi = 2
                                    if item.endswith('_fp_b.xml'):
                                        mode = 'fp'
                                    elif item.endswith('_hp_b.xml'):
                                        mode = 'hp'
                                    else:
                                        mode = 'tp'
                                    pass
                                else:
                                    idi = 1
                                    if item.endswith('_fp.xml'):
                                        mode = 'fp'
                                    elif item.endswith('_hp.xml'):
                                        mode = 'hp'
                                    else:
                                        mode = 'tp'

                                item = item.replace('.xml', '')
                                prompt = f"""<asset display="all" mode="{mode}" name="{item}" teamId="{idi}"/>"""
                            
                                xml_lst.append(prompt)
                                sg.Print(item)
                    
                    xml_lst.sort(reverse=True)
                    xml_itemFBS(i, xml_lst, work_path)
                    xml_lst.clear()
                
                # fbs --------------------------------------
                else:
                    item_class = i.split('_fbs_')[0]

                    work_path = work_path = skin_repo + f'\\Items\\Skins\\{i}.xml'
                    obj_path = skin_repo + f'\\Objects\\Characters\\{item_class}\\fb_suits\\{i}'
                    
                    # -----------
                    sg.Print("\n[FBS]", text_color='blue')
                    sg.Print(work_path.split('.xml')[0], '\n', text_color='green')
                    # -----------

                    for _,_,f in os.walk(obj_path):
                        for item in f:
                            if item.endswith('.xml'):
                                
                                if '_b.xml' in item:
                                    idi = 2
                                    if item.endswith('_fp_b.xml'):
                                        mode = 'fp'
                                    elif item.endswith('_hp_b.xml'):
                                        mode = 'hp'
                                    else:
                                        mode = 'tp'
                                    pass
                                else:
                                    idi = 1
                                    if item.endswith('_fp.xml'):
                                        mode = 'fp'
                                    elif item.endswith('_hp.xml'):
                                        mode = 'hp'
                                    else:
                                        mode = 'tp'

                                item = item.replace('.xml', '')
                                prompt = f"""<asset display="all" mode="{mode}" name="{item}" teamId="{idi}"/>"""
                            
                                xml_lst.append(prompt)
                                sg.Print(item)
                    
                    xml_lst.sort(reverse=True)
                    xml_itemFBS(i, xml_lst, work_path)
                    xml_lst.clear()

    # helmets, vests, shoes, hands
            else:
                item_class = i.split('_')[0]
                
                if 'helmet' in i:
                    armor = 'helmets'
                elif 'vest' in i:
                    armor = 'vests'
                else:
                    armor = i.split(f'{item_class}_')[1].split('_')[0]

                work_path = skin_repo + f'\\Items\\Armor\\{i}.xml'
                obj_path = skin_repo + f'\\Objects\\Characters\\{item_class}\\{armor}\\{i}'
                
                # -----------
                sg.Print("\n[hands, helmets, vest, shoes]", text_color='blue')
                sg.Print(work_path.split('.xml')[0], text_color='green')
                # -----------

                for a,dol,f in os.walk(obj_path):
                    
                    if 'textures' in dol:
                        fate_lst = f

                    for fate in fate_lst:
                        if fate.endswith('.xml'):
                            pass
                        else:
                            fate_lst.remove(fate)

                for elem in fate_lst:
                    if 'hands' in elem:
                        if len(fate_lst) == 3:
                            fate_lst.append('+'+fate_lst[0])
                            fate_lst.append('+'+fate_lst[1])
                            fate_lst.append('+'+fate_lst[2])
                        else:
                            pass
                        
                    elif 'helmet' in elem or 'vest' in elem or 'shoes' in elem:
                        if len(fate_lst) == 2:
                            pass
                        else:
                            fate_lst.append('+'+fate_lst[0])

                for item in fate_lst:
                    if 'hands' in item:
                        if '_b.xml' in item:
                            idi = 2
                            pass
                        elif '+' in item:
                            idi = 2
                            if item.endswith('_fp.xml'):
                                mode = 'fp'
                            elif item.endswith('_hp.xml'):
                                mode = 'hp'
                            else:
                                mode = 'tp'
                            pass

                        else:
                            idi = 1
                            if item.endswith('_fp.xml'):
                                mode = 'fp'
                            elif item.endswith('_hp.xml'):
                                mode = 'hp'
                            else:
                                mode = 'tp'
                    else:
                        if '_b.xml' in item:
                            idi = 2
                            mode = 'tp'
                            pass
                        elif '+' in item:
                            idi = 2
                        else:
                            idi = 1
                            mode = 'tp'

                    # ===============================
                    item = item.split('.xml')[0].strip('+')
                    prompt = f"""<asset display="all" mode="{mode}" name="{item}" teamId="{idi}"/>"""
                    xml_lst.append(prompt)
                    sg.Print(item)
                    # ===============================

                xml_lst.sort(reverse=True)
                xml_itemForm(i, xml_lst, work_path)
                xml_lst.clear()
#---------------------------------------------------------
def main():
    fileStructure(skin_repo)
    # scan_path(skin_repo)
    create_XFile(skin_repo)
    create_ZFile(skin_repo)
    # input('>')
    sg.PopupAnnoying('done..')
#---------------------------------------------------------
if __name__ == "__main__":

    wfc_repo, skin_repo = Ask_Path()
    
    # # ==================TEST_PATH==================================
    # wfc_repo = os.path.abspath("c:\\wf-skins-minsk")
    # skin_repo = os.path.abspath('d:\\__some_get_come__\\_test_Armor\\Game') 
    # # ==================TEST_PATH==================================
    main()