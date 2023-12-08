from logging import root
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os.path
import PySimpleGUI as sg
import shutil
from colorama import init, Style, Fore
init(convert=True)

sg.theme('Reds')
#---------------------------------------------------------
#                       --- GLOBAL---
#---------------------------------------------------------
def AskPath():
    layout = [
        [sg.Text("WPC_master", text_color='yellow')],
        [sg.InputText(default_text = f"{ProjPath}", key = "-MASTER-"),sg.FolderBrowse()],
        [sg.Text("Weapons Folder", text_color='yellow', key="weapon")],
        [sg.InputText(default_text = r"d:\\_WfPC_rep\\wfpc_work\\2022\\WFPC_Content_Pack_14\\14_6_March_Battle_Pass_Cheap_Skin_x6\\", key = "-MOD-"), sg.FolderBrowse()],
        [sg.OK(key='OK'), sg.Cancel()]
    ]
    window = sg.Window(f'weapons ^-^ ', layout)

    while True:
        event, values = window.read(close=True)
        master, mod_repo = values["-MASTER-"], values["-MOD-"]
        print(Fore.BLUE + "----"*13 + Style.RESET_ALL + f"\n{mod_repo}\n" + Fore.BLUE + "----"*13 + Style.RESET_ALL)
        if event == 'OK':
            return master, mod_repo
        
        if values == None:
            exit(0)
        if event in ('Cancel', None) or event == sg.WIN_CLOSED:
            break
    window.close()
def list_to_string(l):
    str1 = '\n'
    return (str1.join(l))
def remove_lastline(path):
    fd=open(path,"r")
    d=fd.read()
    fd.close()
    m=d.split("\n")
    s="\n".join(m[:-1])
    fd=open(path,"w+")
    for i in range(len(s)):
        fd.write(s[i])
    fd.close()
def writeChanges(path, template):
    try:
        open(path, 'a').close()
        open(path, 'r+').write(template)
        print(Fore.GREEN + f"Complete... {path}" + Style.RESET_ALL + Fore.LIGHTBLUE_EX + " ...Added" + Style.RESET_ALL)
    except:
        print(Fore.RED + f"---FAILED... {path}" + Style.RESET_ALL)
def modifyChanges(path, template, skins, prompt01, prompt02):
    
    file = open(path)
    item = prompt01 + skins + prompt02
    try:
        if (item in file.read()):
            print(Fore.YELLOW + f"--- WARNING...  {item} in {path}  ...already exists" + Style.RESET_ALL)
        else:
            remove_lastline(path)
            remove_lastline(path)
            with open(path, 'a') as f:
                f.writelines(template)
            f.close()
            print(Fore.GREEN + f"Complete... {path}" + Style.RESET_ALL + Fore.LIGHTMAGENTA_EX + f" {skins} ...Modified" + Style.RESET_ALL)
    except:
        print(Fore.RED + f"---FAILED... {path}" + Style.RESET_ALL)
def copyFile(temp, master):
    if os.path.exists(temp):
        pass
    else:
        shutil.copyfile(master, temp)
def check_and_create(path):
    if os.path.exists(path) == True:
        pass
    else:
        os.makedirs(path)
def pretty_print(element, indent=None):
    if indent is None:
        indent = "\t"
    original = ET.tostring(element, 'utf8')
    reparsed = minidom.parseString(original)
    indented = reparsed.toprettyxml(indent=indent, newl='\n')
    return '\n'.join([s for s in indented.splitlines() if s.strip()])
#---------------------------------------------------------
def get_ProjPath():
    path = os.path.dirname(os.path.realpath(__name__)) + "\\Integration_Starter.ini"
    if os.path.exists(path) and len(open(path).read()) > 0 and os.path.exists(open(path).read()):
        pass
    else:
        projectPath = sg.popup_get_folder('Project path...', no_titlebar=True, grab_anywhere=True)
        open(path, 'a').close()
        open(path, 'w').write(projectPath)
    ProjPath = open(path).read()
    return ProjPath
def get_Material(weapon):
    material = weapon.split("_")[1]
    return material
def get_Resources():
    weaponPath = temp + "\\Game\\Objects\\Weapons\\"
    attachPath = temp + "\\Game\\Objects\\attachments\\"

    kn_dict = {}
    weapons_dict = {}
    customAttach_dict = {}
    sharedAttach_dict = {}

    for _, _, files in os.walk(weaponPath):
        for item in files:
        # weapons + knives
            if item.endswith("_DDN.tif"):
                skin = item.split("_DDN.tif")[0]
                weapon = item.split("_")[0]
                # skin = item.split("_")[1]
                copyFile(temp + f"\\Game\\Objects\\Weapons\\{weapon}\\{weapon}.xml", master + f"\\Game\\Objects\\Weapons\\{weapon}\\{weapon}.xml")
                
                if "kn" in item:
                    kn_dict.update({weapon:skin})
                else:
                    weapons_dict.update({weapon:skin})
            break
            
        # # attach custom
        # for item in files:
        #     if item.endswith("_d.mtl"):
        #         skin = item.split(".mtl")[0]
        #         weapon = item.split("_")[0]
        #         skin = item.split("_")[1]
        #         customAttach = weapon + item.split(skin)[1]
        #         tempSkin = item.split('_')[1]
        #         # s = item.split('_')[0] + "_" + item.split(tempSkin)
                
        #         copyFile(temp + f"\\Game\\Objects\\Weapons\\{weapon}\\{customAttach}.xml", master + f"\\Game\\Objects\\Weapons\\{weapon}\\{customAttach}.xml")
        #         customAttach_dict.update({customAttach:skin})

# =============================
# Shared attach
# =============================
        # attach shared
        for _, _, files in os.walk(attachPath):
            for item in files:
                pass
            
    print("weapons_dict - ", weapons_dict)
    print("kn_dict - ", kn_dict)
    print("customAttach_dict - ", customAttach_dict)
    
    return weapons_dict, kn_dict, customAttach_dict

def xml_parseObjects(path, weapon, item):
    root = ET.parse(path).getroot()
    
    try:
        skin = item.split("_")[1]
        for element in root.find("materials").findall("material"):
            if element.attrib['name'] == skin:
                root.find('materials').remove(element)

        for element in root.find('materials').findall('material'):
            ET.SubElement(root.find('materials'), 'material',
                                    name=skin,
                                    file=f"objects/weapons/{weapon}/{item}.mtl",
                                    tpfile=f"objects/weapons/{weapon}/{item}_tp.mtl")
            break
    except:
        pass
    with open(path, 'wt') as f:
        f.write(pretty_print(root))    
    
def template_modObjects(weapon, skin):
    template = f"""\n  <material name="{skin}" file="objects/weapons/{weapon}/{weapon}_{skin}.mtl" tpfile="objects/weapons/{weapon}/{weapon}_{skin}_tp.mtl"/>\n </materials>\n</item_view>"""
    return template


def modObjects():
    weapons_dict, kn_dict, customAttach_dict = get_Resources()
    
    for weapon in weapons_dict:
        xml_parseObjects(path=temp + f"Game\Objects\Weapons\{weapon}\{weapon}.xml",
                         weapon=weapon,
                         item=weapon)
    
    for knive in kn_dict:
        xml_parseObjects(path=temp + f"Game\Objects\Weapons\{knive}\{knive}.xml",
                         weapon=knive,
                         item=knive)
    
    # for customAttach in customAttach_dict:
    #     weapon = customAttach.split('_')[0]
    #     xml_parseObjects(path=temp + f"Game\Objects\Weapons\{weapon}\{customAttach}.xml",
    #                      weapon=weapon,
    #                      item=customAttach,
    #                      skin=customAttach_dict[customAttach])
    
    #     template = template_modObjects(weapon, weapons_dict[weapon])
    #     modifyChanges(temp + f"\\Game\\Objects\\Weapons\\{weapon}\\{weapon}.xml", template, weapons_dict[weapon], '', '')
    
    # for weapon in kn_dict:
    #     template = template_modObjects(weapon, kn_dict[weapon])
    #     modifyChanges(temp + f"\\Game\\Objects\\Weapons\\{weapon}\\{weapon}.xml", template, kn_dict[weapon], '', '')
    
    # for weapon in customAttach_dict:
    #     template = template_modObjects(weapon, customAttach_dict[weapon])
    #     modifyChanges(temp + f"\\Game\\Objects\\Weapons\\{weapon.split('_')[0]}\\{weapon}.xml", template, customAttach_dict[weapon], '', '')
    
    
    

def modItems():
    pass


# def xml_Objects():
    # modifyChanges(path, template, skins, prompt01, prompt02)
#---------------------------------------------------------
def main():
    modObjects()
    # get_Resources()
    # input("""\n...Complete (press "Enter" to continue)""")
#---------------------------------------------------------
#                       --- GEAR ---
#---------------------------------------------------------
if __name__ == "__main__":
    ProjPath = get_ProjPath()
    master, temp = AskPath()
    
    main()