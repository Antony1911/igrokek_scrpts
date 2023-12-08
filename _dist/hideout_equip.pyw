import PySimpleGUI as sg
import os
import xml.etree.ElementTree as ET
import shutil

from PySimpleGUI.PySimpleGUI import Column
    
# --------------------------------------------------------
def extsort(files):
    return sorted(files,key=lambda x: os.path.splitext(x)[1]) #    *.xml, *chr, *.mtl ---> *chr, *.mtl, *.xml,   
#---------------------------------------------------------
def main():
    sg.theme('DarkGrey13')

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
        t = "Recreating script path " + script_path
        
        client = sg.popup_get_folder("Client Path?", t)

        cl = client
        out_file = open(script_path, "w")
        out_file.write(cl)
        out_file.close()
    #-------------------------------------------------------------------------------------------
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
            hands = extsort(list(filter(lambda i: "hands" in i, equip)))
            helmet = extsort(list(filter(lambda i: "helmet" in i, equip)))
            vest = extsort(list(filter(lambda i: "vest" in i, equip)))
            #-----------
            head = extsort(list(filter(lambda i: "head" in i, equip)))
            arms = extsort(list(filter(lambda i: "arms" in i, equip)))
            jacket = extsort(list(filter(lambda i: "jacket" in i, equip)))
            pants = extsort(list(filter(lambda i: "pants" in i, equip)))
            shoes = extsort(list(filter(lambda i: "shoes" in i, equip)))
            
            hands.sort()
            helmet.sort()
            vest.sort()
            head.sort()
            arms.sort()
            jacket.sort()
            pants.sort()
            shoes.sort()
            

            # Hands
            shared_hands = extsort(list(filter(lambda i: "shared" in i, hands)))
            soldier_hands = extsort(list(filter(lambda i: "soldier" in i, hands)))
            medic_hands = extsort(list(filter(lambda i: "medic" in i, hands)))
            engineer_hands = extsort(list(filter(lambda i: "engineer" in i, hands)))
            sniper_hands = extsort(list(filter(lambda i: "sniper" in i, hands)))

            # Helmet
            shared_helmet = extsort(list(filter(lambda i: "shared" in i, helmet)))
            soldier_helmet = extsort(list(filter(lambda i: "soldier" in i, helmet)))
            medic_helmet = extsort(list(filter(lambda i: "medic" in i, helmet)))
            engineer_helmet = extsort(list(filter(lambda i: "engineer" in i, helmet)))
            sniper_helmet = extsort(list(filter(lambda i: "sniper" in i, helmet)))

            # Vest
            shared_vest = extsort(list(filter(lambda i: "shared" in i, vest)))
            soldier_vest = extsort(list(filter(lambda i: "soldier" in i, vest)))
            medic_vest = extsort(list(filter(lambda i: "medic" in i, vest)))
            engineer_vest = extsort(list(filter(lambda i: "engineer" in i, vest)))
            sniper_vest = extsort(list(filter(lambda i: "sniper" in i, vest)))
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

            fbs_body = extsort(list(filter(lambda i: "body" in i, fbs)))
            fbs_legs = extsort(list(filter(lambda i: "legs" in i, fbs)))
            
            fbs_body.sort()
            fbs_legs.sort()

    # ---------------------------------------------------------------------------

    # ---------------------------------------------------------------------------
        ss_hand = list()

    # Equipemnt window
        main_equip = [
            [sg.Text('Main', text_color='red')],

            # [sg.Text('HANDS'),  sg.Radio('All', "R_HANDS", key='hand_All', default=True, text_color='orange'),
            #                     sg.Radio('Shared', "R_HANDS", key='hand_Shared'),
            #                     sg.Radio('Soldier', "R_HANDS", key='hand_Soldier', text_color='Green')],
            # [sg.Text('\t'),     sg.Radio('Medic', "R_HANDS", key='hand_Medic', text_color='Pink'),
            #                     sg.Radio('Engineer', "R_HANDS", key='hand_Engineer', text_color='#7a7ef5'),
            #                     sg.Radio('Sniper', "R_HANDS", key='hand_Sniper', text_color='#e20ced')],

            [sg.Text('HANDS')],
            [sg.InputCombo(hands, default_value="shared_hands_07", key='-HANDS-', size=(42, 25))],

            [sg.Text('HELMET')],
            [sg.InputCombo(helmet, default_value="soldier_helmet_08", key='-HELMET-', size=(42, 25))],

            [sg.Text('VEST')],
            [sg.InputCombo(vest, default_value="shared_vest_13", key='-VEST-', size=(42, 25))],

            [sg.Checkbox("Disable head", key='head')],
            [sg.Text()],

            [sg.Checkbox('FBS', key='on_fbs')],
            [sg.InputCombo(fbs_body, default_value='fbs_body', key='fbs_body', size=(42, 25))],
            [sg.InputCombo(fbs_legs, default_value='fbs_legs', key='fbs_legs', size=(42, 25))],
        # ]


        # sec_equip = [
            [sg.Text()],
            [sg.Text('Secondary', text_color='red')],
            [sg.Text('Head')],
            [sg.InputCombo(head, default_value="shared_head_01", key='-HEAD-', size=(42, 25))],

            [sg.Text('Arms')],
            [sg.InputCombo(arms, default_value="soldier_arms_03", key='-ARMS-', size=(42, 25))],

            [sg.Text('Jacket (optional)')],
            [sg.InputCombo(jacket, default_value="", key='-JACKET-', size=(42, 25))],

            [sg.Text('Pants')],
            [sg.InputCombo(pants, default_value="soldier_pants_03", key='-PANTS-', size=(42, 25))],

            [sg.Text('Shoes')],
            [sg.InputCombo(shoes, default_value="shared_shoes_09", key='-SHOES-', size=(42, 25))],


        ]


        layout = [
            [
                # sg.Image(r'c:\\Users\\a_frolov\\Desktop\\112.png'),
                # sg.VSeperator(),
                sg.Column(main_equip),
                # sg.Column(sec_equip),
                # sg.HSeperator(),
                
                
                #sg.Column(presets)
            ],
            [sg.OK(), sg.Cancel()]
        ]

        window = sg.Window('Choose your armor', layout)
        some = []

        while True:
            event, values = window.read()
    # ---------------
            # equip structure
            # if values['hand_All'] == True:
            #     ss_hand = hands
                
            # def listbox_func(key01, lst):
            #     if event == key01:
            #         window.FindElement(key02).update(values[key01])
            #         stuff.update(values[key01])
            #         return stuff
            
            if event == 'hand_Medic':
                
                sss = window.FindElement('-HANDS-') 
                ss_hand = medic_hands
                sss.update(ss_hand)
                
                
                # for ss_hand in main_equip:

                #     ss_hand = medic_hands

            # if values['hand_Medic'] == True:
            #     ss_hand = medic_hands
                # window.FindElement('-HANDS-').update()
    # ---------------
            eqq_l = [
                values['-ARMS-'],
                values['-HANDS-'],
                values['-ARMS-'],
                values['-HANDS-'],
                values['-HEAD-'],
                values['-HELMET-'],
                values['-PANTS-'],
                values['-SHOES-'],
                values['-VEST-'],
                values['-JACKET-'],
                values['fbs_body'],
                values['fbs_legs']
            ]
            # for line in eqq_l:
            #     open(f'{script_path}_equip.txt', 'a').writelines(f'\n{line}')
            # ls = []
            # f = open(f'{script_path}_equip.txt', 'r+').readline()
            # for l in f:
            #     ls.append(l)

            start = """<CharacterDefinition base="objects/characters/human/compound_base.chr" fatness="0" scale="1" gender="Male">\n"""
            arms_hp = ' <Part name='+'"'+ f"{values['-ARMS-']}" + '_hp' + '" '+ 'material="default' + '" '+ 'surface_type='+'" '+ 'mat_armor_arms'+'"/>\n'
            hands_hp = ' <Part name='+'"'+ f"{values['-HANDS-']}" + '_hp' + '" '+ 'material="default' + '" '+ 'surface_type='+'" '+ 'mat_armor_arms'+'"/>\n'
            arms = ' <Part name='+'"'+ f"{values['-ARMS-']}" + '" '+ 'material="default' + '" '+ 'surface_type='+'" '+ 'mat_armor_arms'+'"/>\n'
            hands = ' <Part name='+'"'+ f"{values['-HANDS-']}" + '" '+ 'material="default' + '" '+ 'surface_type='+'" '+ 'mat_armor_arms'+'"/>\n'
            head = ' <Part name='+'"'+ f"{values['-HEAD-']}" + '" '+ 'material="default' + '" '+ 'surface_type='+'" '+ 'mat_armor_head'+'"/>\n'
            helmet = ' <Part name='+'"'+ f"{values['-HELMET-']}" + '" '+ 'material="default' + '" '+ 'surface_type='+'" '+ 'mat_armor_head'+'"/>\n'
            pants = ' <Part name='+'"'+ f"{values['-PANTS-']}" + '" '+ 'material="default' + '" '+ 'surface_type='+'" '+ 'mat_armor_legs'+'"/>\n'
            shoes = ' <Part name='+'"'+ f"{values['-SHOES-']}" + '" '+ 'material="default' + '" '+ 'surface_type='+'" '+ 'mat_armor_legs'+'"/>\n'
            vest = ' <Part name='+'"'+ f"{values['-VEST-']}" + '" '+ 'material="default' + '" '+ 'surface_type='+'" '+ 'mat_armor_body'+'"/>\n'
            jacket = ' <Part name='+'"'+ f"{values['-JACKET-']}" + '" '+ 'material="' + f"{values['-JACKET-']}" + '" '+ 'surface_type='+'" '+ 'mat_default'+'"/>\n'
            end = """</CharacterDefinition>\n"""
            #--------------
            fbs_body = ' <Part name='+'"'+ f"{values['fbs_body']}" + '" '+ 'material="default' + '" '+ 'surface_type='+'" '+ 'mat_default'+'"/>\n'
            fbs_legs = ' <Part name='+'"'+ f"{values['fbs_legs']}" + '" '+ 'material="default' + '" '+ 'surface_type='+'" '+ 'mat_default'+'"/>\n'

    # ----------FBS
            if values['on_fbs'] == False:
                pass
            elif values['on_fbs'] == True:
                some.append(start)
                some.append(fbs_body)
                some.append(fbs_legs)
                some.append(end)
                pass

    # ----------hands, helmet, vest, no head                
            if values['head'] == True and values['on_fbs'] == False:
                some.append(start)
                some.append(arms_hp)
                some.append(hands_hp)
                some.append(arms)
                some.append(hands)
                some.append(' \n')
                some.append(helmet)
                some.append(pants)
                some.append(shoes)
                some.append(vest)
                some.append(jacket)
                some.append(end)
    # ----------hands, helmet, vest, with head
            elif values['head'] == False and values['on_fbs'] == False:
                some.append(start)
                some.append(arms_hp)
                some.append(hands_hp)
                some.append(arms)
                some.append(hands)
                some.append(head)
                some.append(helmet)
                some.append(pants)
                some.append(shoes)
                some.append(vest)
                some.append(jacket)
                some.append(end)
    # --------------
            if event in ('OK', sg.OK()):
                break
            if event in ('Cancel', sg.Cancel()) or event == sg.WIN_CLOSED:
                exit(0)   
        window.close()
    # ---------------------------------------------------------------------------
    #drive
        def setup(way, some):
            #-------------------
            if len(some)>4:
                with open(way, 'w', encoding='utf-8') as f:
                    f.writelines(some)
                    f.close()
            #-------------------
            else:
                with open(way, 'w', encoding='utf-8') as f:
                    f.writelines(some)
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
            try:
                shutil.copyfile(src_path, char)
            except:
                open(src_path, 'a').close()

                add = """<CharacterDefinition base="objects/characters/human/compound_base.chr" fatness="0" scale="1" gender="Male">
 <Part name="soldier_arms_03_hp" material="default" surface_type="mat_armor_arms"/>
 <Part name="shared_hands_07_hp" material="default" surface_type="mat_armor_arms"/>
 <Part name="soldier_arms_03" material="default" surface_type="mat_armor_arms"/>
 <Part name="shared_hands_07" material="default" surface_type=" mat_armor_arms"/>
 <Part name="shared_head_01" material="default" surface_type=" mat_armor_head"/>
 <Part name="soldier_helmet_08" material="default" surface_type=" mat_armor_head"/>
 <Part name="soldier_pants_03" material="default" surface_type="mat_armor_legs"/>
 <Part name="shared_shoes_09" material="default" surface_type="mat_armor_legs"/>
 <Part name="shared_vest_13" material="default" surface_type=" mat_armor_body"/>
 <Part name="soldier_jacket_01" material="soldier_jacket_01" surface_type=" mat_default"/>
</CharacterDefinition>"""
                open(src_path, 'w').write(add)
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
    script_path = os.path.dirname(os.path.realpath(__name__)) + "/hideout_script_path.ini"
    main()