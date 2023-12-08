import os, glob
import xml.etree.ElementTree as ET
from xml.dom import minidom
from os.path import abspath, split
import os.path
from os import name, path
import PySimpleGUI as sg
import shutil
sg.theme('DarkGrey13')



def Ask_Path():
    layout = [
        [sg.Text("WFPC project", text_color='yellow')],
        [sg.InputText(default_text = r"e:\\partner_WPC\\wfpc_mrg\\main", key = "PROJ"), sg.FolderBrowse()],
        [sg.Text("Path to weapons", text_color='yellow')],
        [sg.InputText(default_text = r"d:\\temp_xmler\\weapon_skin", key = "SKINS"),sg.FolderBrowse()],

        [sg.OK(key='OK'), sg.Cancel()]
    ]
    window = sg.Window('\U0001f638 XMLer', layout)

    while True:
        event, values = window.read(close=True)

        if event == 'OK':
            return values["PROJ"], values["SKINS"]

        if event in ('Cancel', None) or event == sg.WIN_CLOSED:
            window.close()

def get_Weapons():
    weapon_list = list()
    for root, dirs, _ in os.walk(work + "\\Game\\Objects\\Weapons\\"):
        for _object in dirs:
            item = os.path.join(root, _object)
            print(item)
            weapon_list.append(item)
        break
    return weapon_list

def get_Content():
    temp_weapon_list = get_Weapons()
    weapon_list = []
    attach_list = []
    sa_list = []
    
    for weapon in temp_weapon_list:
        for _, _, files in os.walk(weapon):
            for elem in files:                 
                if elem.endswith("_d.mtl"):
                    attach_elem = elem.split(".")[0]
                    attach_list.append(attach_elem)
                    
                    weapon_elem = attach_elem.split('_')
                    weapon_elem = weapon_elem[0] + '_' + weapon_elem[1]
                    if weapon_elem not in weapon_list: 
                        weapon_list.append(weapon_elem)
                    
                if "sa0" in elem and elem.endswith(".mtl") and "_tp" not in elem:
                    sa_elem = elem.split(".")[0]
                    sa_list.append(sa_elem)
    print(weapon_list)
    print(attach_list)
    print(sa_list)
    return weapon_list, attach_list, sa_list

def get_skinName(elem):
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
def modifyChanges(path, template, skins, prompt01, prompt02):
    
    file = open(path)
    item = prompt01 + skins + prompt02
    try:
        if (item in file.read()):
            print(Fore.YELLOW + f"--- WARNING...  {item} in {path}  ...already exists" + Style.RESET_ALL)
        else:
            remove_lastline(path)
            with open(path, 'a') as f:
                f.writelines(template)
            f.close()
            print(Fore.GREEN + f"Complete... {path}" + Style.RESET_ALL + Fore.LIGHTMAGENTA_EX + f" {skins} ...Modified" + Style.RESET_ALL)
    except:
        print(Fore.RED + f"---FAILED... {path}" + Style.RESET_ALL)

def mod_ObjWeapons(weapon_list):
    for weapon in weapon_list:
        skinName = get_skinName(weapon)
        weapon = weapon.split('_')[0]
        shutil.copyfile(master + f"\\Game\\Objects\\Weapons\\{weapon}\\{weapon}.xml")
        
        
        
        

def mod_ObjAttach(attach_list):
    pass

def mod_ObjSa(sa_list):
    pass

def modify_Objects():
    weapon_list, attach_list, sa_list = get_Content()
    mod_ObjWeapons(weapon_list)
    mod_ObjAttach(attach_list)
    mod_ObjSa(sa_list)
    

def main():
    modify_Objects()
    exit(0)

#---------------------------------------------------------
if __name__ == "__main__":
    
    master, work = Ask_Path()
    main()