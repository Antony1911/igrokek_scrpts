import os
import xml.etree.ElementTree as ET
import shutil
import time
from xml.dom import minidom



#==============================================================================
#/Game/Objects/Attachments/*.xml
#==============================================================================

#------------------------------------------------------------------------------
def pretty_print(element, indent=None):
    if indent is None:
        indent = "    "
    original = ET.tostring(element, 'utf8')
    reparsed = minidom.parseString(original)
    indented = reparsed.toprettyxml(indent=indent, newl='\n')
    return '\n'.join([s for s in indented.splitlines() if s.strip()])


def obj_att_func(client_att, rep_att, i, temp, mtl):
 
    xml = '/' + f'{i}' + '/' + f'{i}.xml'
    client_xml = client_att + xml
    rep_xml = rep_att + xml
#------------------------------------------------------------------------------
    for _, _, files in os.walk(rep_att + '/' + i):
        mtl = files
        for m in mtl:
            if '.xml' in m:
                mtl.remove(m)
            else:
                pass
        break
# -----------------------------------------------------------------------------
    shutil.copyfile(client_xml, rep_xml)
# -----------------------------------------------------------------------------
    m = mtl[0].strip('.mtl')
# -----------------------------------------------------------------------------
    new_material = "  <material file=" + '"' + "objects/attachments/" + f'{i}/' + mtl[0] + '"' +  ' name=' + '"' + f'{m}' + '"' + """ tpfile="objects/attachments/""" + mtl[1] + '"' + ' />\n'
# -----------------------------------------------------------------------------
    f = open(rep_xml, 'r').readlines()
    for line in f:
        temp.append(line)
    
    a = len(temp) - 2
    temp.insert(a, new_material)
    f = open(rep_xml, 'w').writelines(temp)

    
    temp.clear()
    mtl.clear()




#==============================================================================
#/Game/Items/Accessories/[shared_attachment]*.xml
#==============================================================================
def item_acc_func(acc_att, rep_acc):

    att = []    

    for _, dirs, _ in os.walk(rep_att):
        item_list = dirs
        break
    for i in item_list:

        for _, _, files in os.walk(rep_att + '/' + i):
            mtl = files
            for m in mtl:
                if '.xml' in m:
                    mtl.remove(m)
                else:
                    pass
            break
#----------------------------------------------------------------------------------
        m = mtl[0].strip(f'{i}_.')[0:(len(mtl) - 6)]
#----------------------------------------------------------------------------------

        xml = '/' + f'{i}.xml'
        client_acc_xml = acc_att + xml
        rep_acc_xml = rep_acc + xml

#----------------------------------------------------------------------------------
        shutil.copyfile(client_acc_xml, rep_acc_xml)
#----------------------------------------------------------------------------------

        tree = ET.parse(rep_acc_xml)
        root = tree.getroot()

#----------------------------------------------------------------------------------------

        for a_dir in root:
       
            if 'skins' not in a_dir.tag:
                skins = ET.SubElement(root, "skins")
                ET.SubElement(skins, "material", name = f'{m}')

                with open(rep_acc_xml, 'r+') as output:
                    output.write(pretty_print(root))
                    break
        


            if 'skins' in a_dir.tag:
                for skins in root.findall('skins'):
                    material = skins.find('material')

                    new_material = ET.SubElement(root.find('skins'), 'material', name = f'{m}')
                    with open(rep_acc_xml, 'r+') as f:
                        f.write(pretty_print(root))
                        break
                break    


#=====================================================
def obj_att__vs__item_acc(client_att, rep_att, acc_att, rep_acc):
    temp = []
    mtl = []
    for _, dirs, _ in os.walk(rep_att):
        item_list = dirs
        break
#drive att_func
    for i in item_list:
        obj_att_func(client_att, rep_att, i, temp, mtl)
        item_acc_func(acc_att, rep_acc)
#=====================================================


client_att = path_skin + "/Objects/Attachments"
acc_att = path_skin + "/Items/Accessories"

rep_att = root + "/Game/Objects/Attachments"
rep_acc = items_folder_accessories

obj_att__vs__item_acc(client_att, rep_att, acc_att, rep_acc)