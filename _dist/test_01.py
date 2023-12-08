import os
import PySimpleGUI as sg

# lst = [ 'f_sniper_fbs_gorgona_arms_01_hp_b',
#         'f_sniper_fbs_gorgona_legs_01',
#         'shared_fbs_natan_00001_arms_fp',
#         'shared_fbs_natan_00001_arms_fp_b']

# file = 'sniper_01'
# # ------------------------------------------------------------------------
# path_widget = [

#     [sg.Text(f'Choose your template for [{file}]', text_color='yellow')],
#     [sg.Combo(lst, key = "-TEMPLATE-")],

#     [sg.OK(key='OK'), sg.Cancel()]
# ]
# window = sg.Window('', path_widget)

# while True:
#     event, values = window.read(close=True)

#     if event == 'OK':
#         template = values["-TEMPLATE-"]
#         print(template)
#         break
#     if event in ('Cancel', None) or event == sg.WIN_CLOSED:
#         break
# window.close()

a = "shared_hands_comp_18_01_fp_b"

b = a.split('_b')[0]

print(b)

