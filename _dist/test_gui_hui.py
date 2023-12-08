from PySimpleGUI.PySimpleGUI import LISTBOX_SELECT_MODE_MULTIPLE, PopupAnnoying
import PySimpleGUI as sg

sg.theme('Dark2')

kn = ['some01', 'some02','some03',
        'some04', 'some05', 'some06',
        'some07', 'some08']

pt = ['come01', 'come02','come03',
        'come04', 'come05', 'come06',
        'come07', 'come08']        

smg = ['mome01', 'mome02','mome03',
        'mome04', 'mome05', 'mome06',
        'mome07', 'mome08'] 

ar = ['nome01', 'nome02','nome03',
        'nome04', 'nome05', 'nome06',
        'nome07', 'nome08'] 

shg = ['gome01', 'gome02','gome03',
        'gome04', 'gome05', 'gome06',
        'gome07', 'gome08']

sr = ['home01', 'home02','home03',
        'home04', 'home05', 'home06',
        'home07', 'home08']

mg = ['pome01', 'pome02','pome03',
        'pome04', 'pome05', 'pome06',
        'pome07', 'pome08']

#src_path = r"c:\wf-skins-minsk\Game\Libs\Config\presets\EditorSoldier.lua"
#os.link(src=src_path, dst=r"c:\wf-skins-minsk\Game\Libs\Config\presets\_backup_EditorSoldier\EditorSoldier.lua")


layout = [
    [sg.Listbox(kn, size=(10, 16), text_color='orange', select_mode=LISTBOX_SELECT_MODE_MULTIPLE, key='01', enable_events=True),
    sg.Listbox(pt, size=(10, 16), text_color='red', select_mode=LISTBOX_SELECT_MODE_MULTIPLE, key='02', enable_events=True),
    sg.Listbox(smg, size=(10, 16), text_color='green', select_mode=LISTBOX_SELECT_MODE_MULTIPLE, key='03', enable_events=True),
    sg.Listbox(ar, size=(10, 16), text_color='blue', select_mode=LISTBOX_SELECT_MODE_MULTIPLE, key='04', enable_events=True),
    sg.Listbox(shg, size=(10, 16), text_color='grey', select_mode=LISTBOX_SELECT_MODE_MULTIPLE, key='05', enable_events=True),
    sg.Listbox(sr, size=(10, 16), text_color='purple', select_mode=LISTBOX_SELECT_MODE_MULTIPLE, key='06', enable_events=True),
    sg.Listbox(mg, size=(10, 16), text_color='black', select_mode=LISTBOX_SELECT_MODE_MULTIPLE, key='07', enable_events=True) ],

    [sg.Text('kn', text_color='orange'), sg.Input(key='-INPUT01-', size=(71, 144))],
    [sg.Text('pt',  text_color='red'), sg.Input(key='-INPUT02-', size=(71, 144))],
    [sg.Text('smg', text_color='green'), sg.Input(key='-INPUT03-', size=(71, 144))],
    [sg.Text('ar', text_color='blue'), sg.Input(key='-INPUT04-', size=(71, 144))],
    [sg.Text('shg', text_color='grey'), sg.Input(key='-INPUT05-', size=(71, 144))],
    [sg.Text('sr', text_color='pink'), sg.Input(key='-INPUT06-', size=(71, 144))],
    [sg.Text('mg', text_color='black'), sg.Input(key='-INPUT07-', size=(71, 144))],

    [sg.OK(), sg.Cancel()]
]
window = sg.Window('Choose your weapons', layout)

stuff = []
kn = []

while True:
    event, values = window.read()
# ------------------------------------------------------------

# knives
    if event in ('01', sg.Listbox(kn)):
        window.FindElement('-INPUT01-').update(values['01'])
        kn = values['01']


# pistols
    if event in ('02', sg.Listbox(pt)):    
        window.FindElement('-INPUT02-').update(values['02'])
        pt = values['02']

# smg
    if event in ('03', sg.Listbox(smg)):    
        window.FindElement('-INPUT03-').update(values['03'])
        smg = values['03']


# assault rifles
    if event in ('04', sg.Listbox(ar)):    
        window.FindElement('-INPUT04-').update(values['04'])
        pt = values['04']


# shotguns
    if event in ('05', sg.Listbox(shg)):    
        window.FindElement('-INPUT05-').update(values['05'])
        pt = values['05']


# sniper rifles
    if event in ('06', sg.Listbox(sr)):    
        window.FindElement('-INPUT06-').update(values['06'])
        sr = values['06']

  
# machine guns
    if event in ('07', sg.Listbox(mg)):    
        window.FindElement('-INPUT07-').update(values['07'])
        mg = values['07']


# ------------------------------------------------------------
    if event in ('OK', sg.OK()):
        stuff = kn + pt + smg + ar + shg + sr + mg
        PopupAnnoying('Done!!')
        break

    if event in ('Cancel', sg.Cancel()) or event == sg.WIN_CLOSED:
        break
      
window.close()

print(stuff)