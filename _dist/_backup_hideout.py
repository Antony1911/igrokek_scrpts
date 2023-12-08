import PySimpleGUI as sg
import os
import xml.etree.ElementTree as ET
import shutil

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
#multiply a few presets


#def char(char):
#    if not os.path.exists(char):
#        src_path = cl + r"/Game/Objects/Characters/Presets/default_editor.cpf"
#        os.link(src=src_path, dst=char)

#char(char01)
#char(char02)
#char(char03)
#char(char04)
# -----------------------------------------------------------------------------
# Customization window
# hands, helmet, vest
# -----------------------------------------------------------------------------
    def layout(way):
        equip = []
# -----------------------------------------------------------------------------
        item_path = cl + r"/Game/Items/Armor"
        for _, _, files in os.walk(item_path):
            global item_list
            item_list = files
            break

#parse xml from item_path to know equip availables
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

# FBS maybe later
# -----------------------------------------------------------------------------
#    fbs_path = cl + r"\Game\Items\Skins"
# -----------------------------------------------------------------------------
#    for _, _, files in os.walk(fbs_path):
#        for i in files:
#            new = os.path.splitext(i)[0]
#            i = new
#            equip.append(i)

#    fbs = list(filter(lambda i: "fbs" in i, equip))

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

            [sg.Text()],
            [sg.Checkbox("Disable head", key='head')],

            [sg.OK(), sg.Cancel()]
        ]
        window = sg.Window('Choose your armor', layout)
        some = []

        while True:
            event, values = window.read()

            some.append(values['-HANDS-'])
            some.append(values['-HELMET-'])
            some.append(values['-VEST-'])

            jacket = ' <Part name='+'"'+ 'soldier_jacket_01' + '" '+ 'material="soldier_jacket_01' + '" '+ 'surface_type='+'" '+ 'mat_default'+'"/>\n'

            if values['head'] == True:
                some.append(' \n')
                some.append(jacket)
            else:
                head = ' <Part name='+'"'+ 'shared_head_01' + '" '+ 'material="default' + '" '+ 'surface_type='+'" '+ 'mat_armor_head'+'"/>\n'
                some.append(head)
                some.append(jacket)

            if event in ('OK', sg.OK()):
                break

            if event in ('Cancel', sg.Cancel()) or event == sg.WIN_CLOSED:
                break
      
        window.close()
# ---------------------------------------------------------------------------
#def setup(way):
        setup = []
        setup = open(way, 'r', encoding='utf-8').readlines()

        han = ' <Part name='+'"'+ f'{some[0]}' + '" '+ 'material="default' + '" '+ 'surface_type='+'" '+ 'mat_armor_arms'+'"/>\n'
        hel = ' <Part name='+'"'+ f'{some[1]}' + '" '+ 'material="default' + '" '+ 'surface_type='+'" '+ 'mat_armor_head'+'"/>\n'
        ves = ' <Part name='+'"'+ f'{some[2]}' + '" '+ 'material="default' + '" '+ 'surface_type='+'" '+ 'mat_armor_body'+'"/>\n'

#hands
        setup.pop(4)
        setup.insert(4, han)
#helmet
        setup.pop(6)
        setup.insert(6, hel)
#vest
        setup.pop(9)
        setup.insert(9, ves)
#head
        setup.pop(5)
        setup.insert(5, some[3])
# jacket
        for line in setup:
            if some[4] in setup[10]:
                pass
            else:
                setup.insert(10, some[4])
                break

        with open(way, 'w', encoding='utf-8') as f:
            f.writelines(setup)
            f.close()
# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
    char00 = cl + r"/Game/Objects/Characters/Presets/default_editor.cpf"        
    char01 = cl + r"/Game/Objects/Characters/Presets/default_editor_01.cpf"
    char02 = cl + r"/Game/Objects/Characters/Presets/default_editor_02.cpf"
    char03 = cl + r"/Game/Objects/Characters/Presets/default_editor_03.cpf"
    char04 = cl + r"/Game/Objects/Characters/Presets/default_editor_04.cpf"
# ---------------------------------------------------------------------------
    def char(char):
        if not os.path.exists(char):
            src_path = cl + r"/Game/Objects/Characters/Presets/default_editor.cpf" 
            shutil.copyfile(src_path, char)
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