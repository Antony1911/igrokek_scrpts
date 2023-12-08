import PySimpleGUI as sg
import os


equip = []


# hands, helmet, vest
equip_path = r"c:/wf-skins-minsk/Game/Items/Armor"
for _, _, files in os.walk(equip_path):
    for i in files:
        new = os.path.splitext(i)[0]
        i = new
        equip.append(i)

hands = list(filter(lambda i: "hands" in i, equip))
helmet = list(filter(lambda i: "helmet" in i, equip))
vest = list(filter(lambda i: "vest" in i, equip))


# FBS
fbs_path = r"c:\wf-skins-minsk\Game\Items\Skins"
for _, _, files in os.walk(fbs_path):
    for i in files:
        new = os.path.splitext(i)[0]
        i = new
        equip.append(i)

fbs = list(filter(lambda i: "fbs" in i, equip))







##############################################################################################
# Equipemnt window
layout = [
    [sg.Text('Hands')],
    [sg.InputCombo(hands, default_value="> hands", key='-HANDS-', size=(77, 25))],

    [sg.Text('Helmet')],
    [sg.InputCombo(helmet, default_value="> helmet", key='-HELMET-', size=(77, 25))],

    [sg.Text('Vest')],
    [sg.InputCombo(vest, default_value="> vest", key='-VEST-', size=(77, 25))],

    [sg.Text()],
    [sg.Checkbox("FBS"), sg.InputCombo(fbs, key='-FBS-', size=(68, 25))],

    [sg.OK(), sg.Cancel()]
]
window = sg.Window('Choose your armor', layout)


# Driving events from Buttons
while True:
    event, values = window.read()

    if event in ('OK', sg.OK()):
        stuff = values
        break

    if event in ('Cancel', sg.Cancel()) or event == sg.WIN_CLOSED:
        break

window.close()


# -----------------------------------------------------------------------------
config_path = r"c:/wf-skins-minsk/Game/Libs/Config/presets/EditorSoldier.lua"
# -----------------------------------------------------------------------------

a = open(config_path, 'r+', encoding = "utf-8").readlines()
for line in a:
    if 'helmet' in a[7]:
        pass
    else:
        a.insert(7, '> helmet\n')
        open(config_path, 'r+', encoding = "utf-8").writelines(a)
        break
# -----------------------------------------------------------------------------

content = open(config_path, 'r+', encoding = "utf-8").readlines()
num = -1

for line in content:
    num += 1

# Hands    
    if 'hands' in line:
        hands_num = num
        txt = '\t\t\t{ name = ' + '"' + stuff['-HANDS-'] + '"' + ' },\n'
        #if 'hands' not in content: 
        content.pop(hands_num)
        content.insert(hands_num, txt)
    
# Vest
    if 'vest' in line:
        vest_num = num
        txt = '\t\t\t{ name = ' + '"' + stuff['-VEST-'] + '"' + ' },\n'
        #if 'vest' not in content:
        content.pop(vest_num)
        content.insert(vest_num, txt)

# Helmet
    if 'helmet' in line:
        helmet_num = num
        txt = '\t\t\t{ name = ' + '"' + stuff['-HELMET-'] + '"' + ' },\n'
        #if 'helmet' not in content:
        content.pop(helmet_num)
        content.insert(helmet_num, txt)
    else:
        pass

open(config_path, 'w', encoding = "utf-8").writelines(content)