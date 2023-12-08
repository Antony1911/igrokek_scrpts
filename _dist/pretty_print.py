import os
import xml.etree.ElementTree as ET
from xml.dom import minidom


#---------------------------------------------------------------------
def pretty_print(element, indent=None):
    if indent is None:
        indent = "    "
    original = ET.tostring(element, 'utf8')
    reparsed = minidom.parseString(original)
    indented = reparsed.toprettyxml(indent=indent, newl='\n')
    return '\n'.join([s for s in indented.splitlines() if s.strip()])
#---------------------------------------------------------------------


rep_acc_xml = r"d:/_WFC_rep/WFC_Content_Pack_20/20_2_Weapon_Skins_New_Year_x3_Basic/Game/Items/Accessories/rds07"

root = ET.parse(rep_acc_xml).getroot()


    #if root.findall('skins') == True:
    
child = ET.SubElement(root, "Skinsssssssssssssssssssssssssssssssssssss")
root.append(child)

with open(rep_acc_xml, 'r+') as output:
    output.write(pretty_print(root))
