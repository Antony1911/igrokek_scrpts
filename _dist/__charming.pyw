import os
import PySimpleGUI as sg
sg.theme('DarkGrey13')

#---------------------------------------------------------
def Ask_Path():

    path_widget = [

        [sg.Text('Insert your WFC repo path', text_color='#ebd234')],
        [sg.InputText(default_text = r"c:\wf-skins-minsk", key = "-REPO-"), sg.FolderBrowse()],

        [sg.OK(key='OK'), sg.Cancel()]
    ]
    window = sg.Window('', path_widget, no_titlebar=True)

    while True:
        event, values = window.read(close=True)

        wfc_repo = values["-REPO-"]

        if event == 'OK':
            return wfc_repo
        if event in ('Cancel', None) or event == sg.WIN_CLOSED:
            break
        
    window.close()
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
def droplist(list_there):
    widget = [

        [sg.Text('Choose your charm', text_color='#ebd234')],
        [sg.Listbox(list_there, key = "-REPO-", size=(17, 11))],

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
def parse_it(items_path):
    
    def open_lst(num, pathh):
        lst = []
        f = open(pathh, 'r')
        for line in f:
            lst.append(line)

        charms = seek_and_deploy(charm_path)
        charm_name = droplist(charms)[0]

        string = f"""\t\t\t<support helper="charm" name="{charm_name}" />\n"""
        
        lst.remove(lst[num])
        lst.insert(num, string)
        open(pathh, 'w').writelines(lst)
    
    open_lst(166, items_path[0])
    open_lst(173, items_path[1])
#---------------------------------------------------------
def main():
    # seek_and_deploy(charm_path)
    parse_it(items_path)
    # input('>')
    sg.popup_auto_close("Complete", auto_close_duration=0.4, no_titlebar=True)
#---------------------------------------------------------
if __name__ == "__main__":

    wfc_repo = Ask_Path()
    
    # # ==================TEST_PATH==================================
    # wfc_repo = os.path.abspath("c:/wf-skins-minsk")
    # # ==================TEST_PATH==================================
    
    items_path_01 = wfc_repo + "/Game/Items/Weapons/ar35.xml"
    items_path_02 = wfc_repo + "/Game/Items/Weapons/pt39.xml"
    items_path = [items_path_01, items_path_02]
    charm_path = wfc_repo + "/Game/Objects/Attachments/charms"
    main()