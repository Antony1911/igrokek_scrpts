import PySimpleGUI as sg
import webbrowser


url = "https:/youtrack.plan365.org/issue/"

def dropdownMenu():
    
    layout = [
        [sg.Text("url"), sg.Input('', key="input")],
        [sg.Button('go')]
    ]
    
    window = sg.Window('url to go', layout)
    while True:
        event, value = window.read(close=True)
        
        if event == 'go':
            webbrowser.open(url + value["input"], new=0, autoraise=True)
            dropdownMenu()
            
        if event in ('Cancel', None) or event == sg.WIN_CLOSED:
            exit(0)
        window.close()
dropdownMenu()