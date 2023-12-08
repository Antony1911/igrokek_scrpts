import PySimpleGUI as sg
import os
import xml.etree.ElementTree as ET
import shutil
import time

def main():
    sg.theme('Dark2')
    script_path = r"d:\script_path.txt"

# Insert path to Game folder
    global cl
    if os.path.exists(script_path) and len(open(script_path).read()) > 3 and os.path.exists(open(script_path).read()):
        exists_content = open(script_path).read()
        w_cont = sg.popup_yes_no("Continue with path? ", exists_content)
    
        if w_cont == 'Yes':
            cl = exists_content
            pass

        if w_cont == 'No':
            client = sg.popup_get_folder("Client Path?", "Choose where 'Game' Folder is" )
            
            cl = client.strip("Game")
            out_file = open(script_path, "w")
            out_file.write(cl)
            out_file.close()

    else:
        t = "Recreating script path " + r"d:\script_path.txt"
        
        client = sg.popup_get_folder("Client Path?", t)

        cl = client #input("Client path? \n")
        out_file = open(script_path, "w")
        out_file.write(cl)
        out_file.close()



# backup "default_editor.cpf"
    try:                                                                                       
        back_folder = cl + r"/Game/Objects/Characters/Presets/_backup_default_editor"                  
        if not os.path.exists(back_folder):                                                    
                os.makedirs(back_folder)                                                           
        else:                                                                                   
            pass                                                                                
# ------------------------------------------------------------------------------------------                                                     
        backup = cl + r"/Game/Objects/Characters/Presets/_backup_default_editor/default_editor.cpf"     
# ------------------------------------------------------------------------------------------         
        if not os.path.exists(backup):                                                         
            src_path = cl + r"/Game/Objects/Characters/Presets/default_editor.cpf"                                         
            shutil.copyfile(src_path, backup)                                                                                                  
    except:                                                                                    
        pass

# -----------------------------------------------------------------------------
    def layout(way):
        equip = []
# -----------------------------------------------------------------------------
        item_path = cl + r"/Game/Items/Armor"
# -----------------------------------------------------------------------------
        for _, _, files in os.walk(item_path):
            item_list = files
            break
#hands, helmet, vest
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
        fbs_path = cl + r"/Game/Items/Skins"
# -----------------------------------------------------------------------------
        for _, _, files in os.walk(fbs_path):
            item_list = files
            break
        for i in item_list:
            root = ET.parse(fbs_path + '/' + i).getroot()
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
            fbs = list(filter(lambda i: "fbs" in i, equip))
            fbs_body = list(filter(lambda i: "body" in i, fbs))
            fbs_legs = list(filter(lambda i: "legs" in i, fbs))

# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Equipemnt window

        layout = [
            [sg.Text('Hands')],
            [sg.InputCombo(hands, default_value="shared_hands_07", key='-HANDS-', size=(42, 25))],

            [sg.Text('Helmet')],
            [sg.InputCombo(helmet, default_value="soldier_helmet_08", key='-HELMET-', size=(42, 25))],

            [sg.Text('Vest')],
            [sg.InputCombo(vest, default_value="shared_vest_13", key='-VEST-', size=(42, 25))],

            [sg.Checkbox("Disable head", key='head')],
            [sg.Text()],

            [sg.Checkbox('FBS', key='on_fbs')],
            [sg.InputCombo(fbs_body, default_value='fbs_body', key='fbs_body', size=(42, 25))],
            [sg.InputCombo(fbs_legs, default_value='fbs_legs', key='fbs_legs', size=(42, 25))],

            [sg.OK(), sg.Cancel()]
        ]
        window = sg.Window('Choose your armor', layout)
        some = []

        while True:
            event, values = window.read()
# ---------------
            # equip structure
# ---------------
            #00
            start = """<CharacterDefinition base="objects/characters/human/compound_base.chr" fatness="0" scale="1" gender="Male">\n"""
            #01
            arms_hp = ' <Part name='+'"'+ 'soldier_arms_03_hp' + '" '+ 'material="default' + '" '+ 'surface_type='+'" '+ 'mat_armor_arms'+'"/>\n'
            #02
            hands_hp = ' <Part name='+'"'+ 'shared_hands_07_hp' + '" '+ 'material="default' + '" '+ 'surface_type='+'" '+ 'mat_armor_arms'+'"/>\n'
            #03
            arms = ' <Part name='+'"'+ 'soldier_arms_03' + '" '+ 'material="default' + '" '+ 'surface_type='+'" '+ 'mat_armor_arms'+'"/>\n'
            #04
            #----hands
            #05
            head = ' <Part name='+'"'+ 'shared_head_01' + '" '+ 'material="default' + '" '+ 'surface_type='+'" '+ 'mat_armor_head'+'"/>\n'
            #06
            #----helmet
            #07
            pants = ' <Part name='+'"'+ 'soldier_pants_03' + '" '+ 'material="default' + '" '+ 'surface_type='+'" '+ 'mat_armor_legs'+'"/>\n'
            #08
            shoes = ' <Part name='+'"'+ 'shared_shoes_09' + '" '+ 'material="default' + '" '+ 'surface_type='+'" '+ 'mat_armor_legs'+'"/>\n'
            #09
            #----vest
            #10
            jacket = ' <Part name='+'"'+ 'soldier_jacket_01' + '" '+ 'material="soldier_jacket_01' + '" '+ 'surface_type='+'" '+ 'mat_default'+'"/>\n'
            #11
            end = """</CharacterDefinition>\n"""

# ----------FBS
            if values['on_fbs'] == False:
                pass
            elif values['on_fbs'] == True:
                some.append(start)
                some.append(values['fbs_body'])
                some.append(values['fbs_legs'])
                some.append(end)
                pass
# ----------hands, helmet, vest, no head                
            if values['head'] == True and values['on_fbs'] == False:
                some.append(start)
                some.append(arms_hp)
                some.append(hands_hp)
                some.append(arms)
                some.append(values['-HANDS-'])
                some.append(' \n')
                some.append(values['-HELMET-'])
                some.append(pants)
                some.append(shoes)
                some.append(values['-VEST-'])
                some.append(jacket)
                some.append(end)
# ----------hands, helmet, vest, with head
            elif values['head'] == False and values['on_fbs'] == False:
                some.append(start)
                some.append(arms_hp)
                some.append(hands_hp)
                some.append(arms)
                some.append(values['-HANDS-'])
                some.append(head)
                some.append(values['-HELMET-'])
                some.append(pants)
                some.append(shoes)
                some.append(values['-VEST-'])
                some.append(jacket)
                some.append(end)
# --------------
            if event in ('OK', sg.OK()):
                break
            if event in ('Cancel', sg.Cancel()) or event == sg.WIN_CLOSED:
                break   
        window.close()
# ---------------------------------------------------------------------------
#drive
        def setup(way, some):
            setup = []
            setup = open(way, 'r', encoding='utf-8').readlines()

            if len(some)>4:

                han = ' <Part name='+'"'+ f'{some[4]}' + '" '+ 'material="default' + '" '+ 'surface_type='+'" '+ 'mat_armor_arms'+'"/>\n'
                hel = ' <Part name='+'"'+ f'{some[6]}' + '" '+ 'material="default' + '" '+ 'surface_type='+'" '+ 'mat_armor_head'+'"/>\n'
                ves = ' <Part name='+'"'+ f'{some[9]}' + '" '+ 'material="default' + '" '+ 'surface_type='+'" '+ 'mat_armor_body'+'"/>\n'
#start
                setup.pop(0)
                setup.insert(0, some[0])
#arms_hp
                setup.pop(1)
                setup.insert(1, some[1])
#hands_hp
                setup.pop(2)
                setup.insert(2, some[2])
#arms
                setup.pop(3)
                setup.insert(3, some[3])               
#hands
                setup.pop(4)
                setup.insert(4, han)
#head
                setup.pop(5)
                setup.insert(5, some[5])
#helmet
                setup.pop(6)
                setup.insert(6, hel)

                setup.pop(7)
                setup.insert(7, some[7])

                setup.pop(8)
                setup.insert(6, some[8])
#vest
                setup.pop(9)
                setup.insert(9, ves)
# jacket
                for line in setup:
                    if some[10] in setup[10]:
                        pass
                    else:
                        setup.insert(10, some[10])
                        break

                setup.pop(11)
                setup.insert(11, some[11])

                if len(setup)>12:
                    setup.pop(11)
                else:
                    pass

                with open(way, 'w', encoding='utf-8') as f:
                    f.writelines(setup)
                    f.close()
            #-------------------
            else:
                fbs_i_body = ' <Part name='+'"'+ f'{some[1]}' + '" '+ 'material="default' + '" '+ 'surface_type='+'" '+ 'mat_default'+'"/>\n'
                fbs_i_legs = ' <Part name='+'"'+ f'{some[2]}' + '" '+ 'material="default' + '" '+ 'surface_type='+'" '+ 'mat_default'+'"/>\n'
                space = ' \n'

                setup.pop(0)
                setup.insert(0, some[0])

                setup.pop(1)
                setup.insert(1, space)

                setup.pop(2)
                setup.insert(2, space)

                setup.pop(3)
                setup.insert(3, space)

                setup.pop(4)
                setup.insert(4, space)

                setup.pop(5)
                setup.insert(5, space)

                setup.pop(6)
                setup.insert(6, space)

                setup.pop(7)
                setup.insert(7, space)

                setup.pop(8)
                setup.insert(8, space)

                setup.pop(9)
                setup.insert(9, fbs_i_body)

                setup.pop(10)
                setup.insert(10, fbs_i_legs)

                setup.pop(11)
                setup.insert(11, some[3])

                with open(way, 'w', encoding='utf-8') as f:
                    f.writelines(setup)
                    f.close()
                
# ----------------------------------------------------------------------------------------------------------------
        setup(way, some)
# ----------------------------------------------------------------------------------------------------------------
    char00 = cl + r"/Game/Objects/Characters/Presets/default_editor.cpf"        
    char01 = cl + r"/Game/Objects/Characters/Presets/default_editor_01.cpf"
    char02 = cl + r"/Game/Objects/Characters/Presets/default_editor_02.cpf"
    char03 = cl + r"/Game/Objects/Characters/Presets/default_editor_03.cpf"
    char04 = cl + r"/Game/Objects/Characters/Presets/default_editor_04.cpf"
# ---------------------------------------------------------------------------
    def char(char):
        src_path = cl + r"/Game/Objects/Characters/Presets/default_editor.cpf"
        if not os.path.exists(char):
            shutil.copyfile(src_path, char)
            jacket = ' <Part name='+'"'+ 'soldier_jacket_01' + '" '+ 'material="soldier_jacket_01' + '" '+ 'surface_type='+'" '+ 'mat_default'+'"/>\n'

            temp = open(char, 'r+', encoding='utf-8')
            hui = []
            for i in temp:
                hui.append(i)
                for line in hui:
                    if "jacket" in line[10]:
                        break
                    else:
                        hui.insert(10, jacket)
                        close = open(char, 'r+', encoding='utf-8')
                        close.writelines(hui)
                        close.close()
                        break
                    break
                break
            
        else:
            pass
# ---------------------------------------------------------------------------
    def del_char(char):
        try:
            os.remove(char)
        except:
            pass
# ---------------------------------------------------------------------------
    ask = [
        [sg.Text('How many armor sets you need?')],
        [sg.Radio('1 set', "RADIO1", key='1', default=True)],
        [sg.Radio('2 sets', "RADIO1", key='2')],
        [sg.Radio('3 sets', "RADIO1", key='3')],
        [sg.Radio('4 sets', "RADIO1", key='4')],
        [sg.Radio('5 sets', "RADIO1", key='5')],
        [sg.OK(), sg.Cancel()]

    ]

    ask_window = sg.Window('Choose integer of sets', ask)
    while True:
        event, values = ask_window.read()

        if values['1'] == True:
            layout(char00)

            del_char(char01)
            del_char(char02)
            del_char(char03)
            del_char(char04)
         
        if values['2'] == True:
            char(char01)

            layout(char00)
            layout(char01)
            del_char(char02)
            del_char(char03)
            del_char(char04)
            
        if values['3'] == True:
            char(char01)
            char(char02)

            layout(char00)
            layout(char01)
            layout(char02)
            del_char(char03)
            del_char(char04)
            
        if values['4'] == True:
            char(char01)
            char(char02)
            char(char03)
        
            layout(char00)
            layout(char01)
            layout(char02)
            layout(char03)
            del_char(char04)
        
        if values['5'] == True:
            char(char01)
            char(char02)
            char(char03)
            char(char04)

            layout(char00)
            layout(char01)
            layout(char02)
            layout(char03)
            layout(char04)
               
        if event in ('OK', sg.OK()):
            break
        if event in ('Cancel', sg.Cancel()) or event == sg.WIN_CLOSED:
            break  
    ask_window.close()
# --------------------------------------------------------------------------- 
    sg.popup_auto_close('Complete!!', auto_close_duration=0.4)

if __name__ == '__main__':
    main()