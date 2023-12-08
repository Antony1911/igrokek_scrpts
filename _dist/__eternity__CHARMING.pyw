import os
import PySimpleGUI as sg
import shutil

sg.theme('DarkGrey13')

#---------------------------------------------------------
def Ask_Path():
    if os.path.exists(script_path) and len(open(script_path).read()) > 3 and os.path.exists(open(script_path).read()):
        papath = open(script_path).read()
    else:
        papath = '¯\_(ツ)_/¯¯\_(ツ)_/¯¯\_(ツ)_/¯¯\_(ツ)_/¯¯\_(ツ)_/¯'
    

    path_widget = [

        [sg.Text('Insert your WFC/WFPC repo path', text_color='#ebd234')],
        [sg.InputText(default_text = f"{papath}", key = "-REPO-"), sg.FolderBrowse()],

        [sg.OK(key='OK'), sg.Cancel()]
    ]
    window = sg.Window('', path_widget, no_titlebar=True)

    while True:
        event, values = window.read(close=True)

        wfc_repo = values["-REPO-"]

        if event == 'OK':
            try:
                open(script_path, 'a').close()
                ss = open(script_path, 'w')
                ss.write(wfc_repo)
                ss.close()
            except:
                pass

            return wfc_repo
        if event in ('Cancel', None) or event == sg.WIN_CLOSED:
            break
        
    window.close()
#---------------------------------------------------------
def uppercase(charm_path):
    for root, dirs, files in os.walk(charm_path):
        
        # uppercase case
        for name in dirs:
            if "T" in name:
                os.rename(root + '/' + name, root + '/' + 'textures')
#---------------------------------------------------------
def seek_and_deploy(charm_path):
    charms = []
    for root, dirs, files in os.walk(charm_path):

        if "textures" in dirs:
            if len(files)>0:
                    charm_temp = files

                    for file in charm_temp:
                        if file.endswith('.xml'):
                            charms.append(file.split('.xml')[0])
    return charms
#---------------------------------------------------------
def droplist(list_there, item01, item02, item03):
    widget = [

        [sg.Text(f'Choose your charm for\n> {item01},  > {item02}\n{item03}', text_color='#ebd234')],
        [sg.Listbox(list_there, key = "-REPO-", size=(24, 17))],

        [sg.OK(key='OK'), sg.Cancel()]
    ]
    window = sg.Window('', widget, no_titlebar=True)

    while True:
        event, values = window.read(close=True)

        char = values["-REPO-"]

        if event == 'OK':
            return char
        if event in ('Cancel', None) or event == sg.WIN_CLOSED:
            break
        
    window.close()
# --------------------------------------------------------
def parse_it():

    iter_num = int(sg.popup_get_text('How many charms?', default_text='4'))
    
    # remove all test guns from the last script
    for i in range(1, iter_num + 1):
        try:
            for root, dirs, files in os.walk(test_path):
                filen = files
                for file in filen:
                    if 'ar35_test01' in file or 'pt39_test01' in file:
                        pass
                    elif 'ar35_test' in file or 'pt39_test' in file:
                        os.remove(test_path + '/' + file)
        except i == 1:
            pass

    # create new necessary test guns
    for i in range(1, iter_num + 1):
        if i==1:
            pass
        else:
            new_test_ar = f'/ar35_test0{i}.xml'
            new_test_pt = f'/pt39_test0{i}.xml'
            shutil.copyfile(test_path + '/ar35_test01.xml', test_path + new_test_ar)
            shutil.copyfile(test_path + '/pt39_test01.xml', test_path + new_test_pt)

    for i in range(1, iter_num + 1):
        new_test_ar = f'/ar35_test0{i}.xml'
        new_test_pt = f'/pt39_test0{i}.xml'
        add_list.append(f"i_giveitem ar35_test0{i}:default\n")
        add_list.append(f"i_giveitem pt39_test0{i}:default\n")
        
        lst01 = []
        lst02 = []
        f01 = open(test_path + '/ar35_test01.xml', 'r')
        f02 = open(test_path + '/pt39_test01.xml', 'r')

        for line in f01:
            lst01.append(line)
        for line in f02:
            lst02.append(line)

        item01 = f'ar35_test0{i}'
        item02 = f'pt39_test0{i}'
        item03 = f'remaining : {iter_num+1-i}'
        charm_name = droplist(charms, item01, item02, item03)[0]

        new_name_string_ar = f"""<item category="heavy" class="K01_Item" name="ar35_test0{i}" net_policy="weapon" priority="49" view_settings="objects/weapons/ar35_test/ar35.xml">\n"""
        new_name_string_pt = f"""<item category="medium" class="K01_Item" name="pt39_test0{i}" net_policy="weapon" priority="22" view_settings="objects/weapons/pt39_test/pt39.xml">\n"""
        string = f"""\t\t\t<support helper="charm" name="{charm_name}" />\n"""
        
        lst01.remove(lst01[166])
        lst01.insert(166, string)
        lst01.remove(lst01[1])
        lst01.insert(1, new_name_string_ar)
        open(test_path + new_test_ar, 'w').writelines(lst01)

        lst02.remove(lst02[173])
        lst02.insert(173, string)
        lst02.remove(lst02[1])
        lst02.insert(1, new_name_string_pt)
        open(test_path + new_test_pt, 'w').writelines(lst02)

    gunz = open(config, 'a', encoding='utf-8')
    gunz.writelines(add_list)
    gunz.close()
#---------------------------------------------------------
def enable_inventory(config):
    try:
        content = ['r_displayInfo = 0\n',
                    'hud_crosshair = 0\n',
                    'ui_close_screen HUD\n',
                    'ui_close_screen console_hud\n',
                    'i_enable_inventory_select 1\n'
                    'i_inventory_capacity = 100\n'
                    
                    ]
        open(config, 'w', encoding='utf-8').writelines(content)
    except(AttributeError):
        pass
#---------------------------------------------------------
def prog_met():
    BAR_MAX = 100

    # layout the Window
    layout = [[sg.Text('Processing...')],
            [sg.ProgressBar(BAR_MAX, orientation='h', size=(20,20), key='-PROG-')],
            [sg.Cancel()]]

    # create the Window
    window = sg.Window('Processing...', layout, no_titlebar=100)
    # loop that would normally do something useful
    for i in range(100):
        # check to see if the cancel button was clicked and exit loop if clicked
        event, values = window.read(timeout=10)
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
            # update bar with loop value +1 so that bar eventually reaches the maximum
        window['-PROG-'].update(i+1)
    # done with loop... need to destroy the window as it's still open
    window.close()
#---------------------------------------------------------
def main():
    # seek_and_deploy(charm_path)
    enable_inventory(config)
    parse_it()
    # input('>')
    print(add_list)
    # prog_met()
    sg.popup_auto_close("Complete", auto_close_duration=0.4, no_titlebar=True)
#---------------------------------------------------------
if __name__ == "__main__":

    script_path = os.path.dirname(os.path.realpath(__file__)) + "/ETERNITY_CHARMING_script_path.ini"
    wfc_repo = Ask_Path()
    add_list = list()
    config = wfc_repo + '\\Game\\config\\charm.cfg'
    # copy('exec charm')
    
    # # ==================TEST_PATH==================================
    # wfc_repo = os.path.abspath("c:/wf-skins-minsk")
    # # ==================TEST_PATH==================================
    
    test_path = wfc_repo + "/Game/Items/Weapons"
    charm_path = wfc_repo + "/Game/Objects/Attachments/charms"
    uppercase(charm_path)
    charms = seek_and_deploy(charm_path)
    
    main()