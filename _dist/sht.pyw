import PySimpleGUI as sg
import os
import xml.etree.ElementTree as ET

sg.theme('Dark2')
equip = []

work_path = r"d:\script_path.ini"
work = open(work_path).read()



# hands, helmet, vest
# -----------------------------------------------------------------------------
item_path = work + r"/Game/Items/Armor"
# -----------------------------------------------------------------------------
for _, _, files in os.walk(item_path):
    for i in files:
        new = os.path.splitext(i)[0]
        i = new
        equip.append(i)


for _, _, files in os.walk(item_path):
    item_list = files
    break
for i in item_list:
    root = ET.parse(item_path + '/' + i).getroot()

    for a_dir in root:
        for b_dir in a_dir:
            for c_dir in b_dir:
                for d_dir in c_dir:
                    name = d_dir.attrib.get('name')
                    if '_fp' in name:
                        pass
                    elif '_hp' in name:
                        pass
                    elif 'default' in name:
                        pass
                    else:
                        equip.append(name)


hands = list(filter(lambda i: "hands" in i, equip))
helmet = list(filter(lambda i: "helmet" in i, equip))
vest = list(filter(lambda i: "vest" in i, equip))



# FBS
# -----------------------------------------------------------------------------
fbs_path = work + r"\Game\Items\Skins"
# -----------------------------------------------------------------------------
for _, _, files in os.walk(fbs_path):
    for i in files:
        new = os.path.splitext(i)[0]
        i = new
        equip.append(i)
        #equip.append(i + '_b')

fbs = list(filter(lambda i: "fbs" in i, equip))

# -----------------------------------------------------------------------------
# Equipemnt window
layout = [
    [sg.Text('Hands')],
    [sg.InputCombo(hands, default_value="shared_hands_08", key='-HANDS-', size=(42, 25))],

    [sg.Text('Helmet')],
    [sg.InputCombo(helmet, default_value="soldier_helmet_01", key='-HELMET-', size=(42, 25))],

    [sg.Text('Vest')],
    [sg.InputCombo(vest, default_value="shared_vest_13", key='-VEST-', size=(42, 25))],


    [sg.Text()],
    [sg.Checkbox("FBS", key='-IN-'), sg.InputCombo(fbs, key='-FBS-', size=(33, 25))],

    [sg.OK(), sg.Cancel()]
]
window = sg.Window('Choose your armor', layout)


# Driving events from Buttons
some = []
while True:
    event, values = window.read()

    if values['-IN-'] == True:
        some.append(values['-HANDS-'])
        some.append(values['-HELMET-'])
        some.append(values['-VEST-'])
        some.append(values['-FBS-'])

    else:
        some.append(values['-HANDS-'])
        some.append(values['-HELMET-'])
        some.append(values['-VEST-'])
        some.append('> fbs')
        some.append('>')

    if event in ('OK', sg.OK()):
        print('OK')
        break

    if event in ('Cancel', sg.Cancel()) or event == sg.WIN_CLOSED:
        break
      
window.close()
print(some)

# -----------------------------------------------------------------------------
config_path = work + r"/Game/Libs/Config/presets/EditorSoldier.lua"
# -----------------------------------------------------------------------------

a = open(config_path, 'r+', encoding = "utf-8").readlines()
for line in a:
    if 'helmet' in a[7]:
        pass
    if 'fbs' in a[13]:
        pass
    else:
        a.insert(7, '\t\t\t{ name = ' + '"' + '> helmet' + '"' + ' },\n')
        a.insert(13, '\t\t\t---{ name = ' + '"' + '> fbs' + '"' + ' },\n')
        open(config_path, 'r+', encoding = "utf-8").writelines(a)
        break
# -----------------------------------------------------------------------------

content = open(config_path, 'r+', encoding = "utf-8").readlines()
num = -1

for line in content:
    #if '--' in line:
    #    content.remove(line)

    num += 1

# Hands    
    if 'hands' in line:
        hands_num = num
        txt = '\t\t\t{ name = ' + '"' + some[0] + '"' + ' },\n'

        content.pop(hands_num)
        content.insert(hands_num, txt)
    
# Vest
    if 'vest' in line:
        vest_num = num
        txt = '\t\t\t{ name = ' + '"' + some[2] + '"' + ' },\n'

        content.pop(vest_num)
        content.insert(vest_num, txt)

# Helmet
    if 'helmet' in line:
        helmet_num = num
        txt = '\t\t\t{ name = ' + '"' + some[1] + '"' + ' },\n'

        content.pop(helmet_num)
        content.insert(helmet_num, txt)
    else:
        pass


# FBS
    if 'fbs' in line:
        helmet_num = num
        if len(some) == 4:
            txt = '\t\t\t{ name = ' + '"' + some[3] + '"' + ' },\n'

            content.pop(helmet_num)
            content.insert(helmet_num, txt)

        else:
            txt = '\t\t\t---{ name = ' + '"' + some[3] + '"' + ' },\n'
            content.pop(helmet_num)
            content.insert(helmet_num, txt)
    else:
        pass

# drive
open(config_path, 'w', encoding = "utf-8").writelines(content)
sg.popup_auto_close('Complete!!', auto_close_duration=0.4)