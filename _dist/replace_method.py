import os, glob
import xml.etree.ElementTree as ET
import shutil
from xml.dom import minidom



#------------------------------------------------------------------------------
def pretty_print(element, indent=None):
    if indent is None:
        indent = "    "
    original = ET.tostring(element, 'utf8')
    reparsed = minidom.parseString(original)
    indented = reparsed.toprettyxml(indent=indent, newl='\n')
    return '\n'.join([s for s in indented.splitlines() if s.strip()])

#------------------------------------------------------------------------------
#   Game\Objects\Attachments
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
        os.makedirs(repo + '\Objects\Attachments\\' + f'{i}')
        shutil.copyfile(client_xml, rep_xml)

    f = open(rep_xml, 'r').readlines()
    for line in f:
        temp.append(line)
        

    for x in mtl:
        m = x.rstrip('.mtl')
        new_material = "    <material file=" + '"' + "objects/attachments/" + f'{i}/{m}.mtl' + '"' + ' name=' + '"' + m.split('_')[1] + '"' + """ tpfile="objects/attachments/""" + f'{i}/{m}_tp.mtl' + '"' + ' />\n'
        
        if new_material not in temp:
            if len(mtl)>1:
                a = len(temp) - 3
            else:
                a = len(temp) - 2

            temp.insert(a, new_material)
        else:
            pass

    f = open(rep_xml, 'w').writelines(temp)
    temp.clear()
    mtl.clear()
    #-----------------
    tree = ET.parse(rep_xml)
    root = tree.getroot()
    with open(rep_xml, 'w') as f:
        f.write(pretty_print(root))
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
            for skins in root.findall('skins'):
                skins.find('material')
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
#   Game\Items\Accessories
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
                shutil.copyfile(path, rep_acc_xml)
                shutil.copyfile(a_path, b_path)
                #---------
                att_No_Skin_xml(rep_acc_xml, item)
                add_material_att(rep_acc_xml, skin_item, mtl)
                att_Skin_xml(b_path, skin_item, item)
            
#------------------------------------------------------------------------------
# Game\Objects\Attachments + Game\Items\Accessories
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
#   File Structure
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
#==============================================================================

fileStructure(rep_att, rep_acc)
obj_att__vs__item_acc(client_att, rep_att)
#==============================================================================
if __name__ == "__main__":
#---------
    
    client = input("Client path?\n> ")
    root = client
#---------
    path_skin = input("path skin\n> ")
    repo = path_skin
#---------
    Objects_Attachments = "Objects\Attachments"
    Items_Accessories = "Items\Accessories"
    Game_Objects_Attachments = "Game\Objects\Attachments"
    Game_Items_Accessories = "Game\Items\Accessories"
#---------
    client_att = client + Game_Objects_Attachments
    rep_att = repo + Objects_Attachments
    acc_att = client + Game_Items_Accessories
    rep_acc = repo + Items_Accessories

#==============================================================================
    main()
#==============================================================================

#   client_att = client + Game_Objects_Attachments
#
#
#
#
#
#
#
