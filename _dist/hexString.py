import binascii
from Crypto.Cipher import AES
import getpass
import PySimpleGUI as sg
from tkinter import *
import json
sg.theme('SystemDefault1')

# charlyConfigPath = f"C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\Charles\\charles.config"

def readDictPath(path):
    with open(path, "r", encoding='utf-8') as f:
        content = f.read()
    return content
def decodeConfig(hex_bytes, key,  iv):
    # hex_bytes = readDictPath(path)
    # for elem in [hex_bytes[i:i+31] for i in range(0, len(hex_bytes), 31)]:
    #     print(elem)

    # конвертация hexadecimal-байтов в байты
    bytes = binascii.unhexlify(hex_bytes)

    # конвертация ключа в байты
    key = binascii.unhexlify(key)

    # получение 32-байтового IV от пользователя
    # iv = input("Введите 32-байтовый IV: ")
    # iv = b'f115c755ed1e3dc1627306b3a95b2aba'

    # конвертация IV в байты
    iv = binascii.unhexlify(iv)

    # создание объекта AES cipher с mode-CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # декодирование байтов с помощью AES cipher
    decoded_bytes = cipher.decrypt(bytes)

    # конвертация декодированных байтов в строку
    decoded_string = decoded_bytes.decode('utf-8')
    # decoded_string = decoded_bytes.decode('utf-8')
    
    # ------------------------------------------
    text_without_hex = ''.join(['' if ord(c) < 32 or ord(c) > 126 else c for c in decoded_string])
    parsed = json.loads(text_without_hex)
    prettyPrint = json.dumps(parsed, indent=4)
    resultWindow(prettyPrint)
    # ------------------------------------------

def encodeConfig(text, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(text.encode())
    hex_text = ciphertext.hex()
    sg.Print(hex_text)

def startMenu(): 
    layout =  [
        [sg.Input(size=(55,1), default_text="5a677564567332496852716157716a376f774d774e5763314d766b6a36477548", key='key', enable_events=True,
                  readonly=True, disabled=True), sg.Text("64-byte key", text_color='green')],
        [sg.Multiline("""""", size=(70,13), key='mLine', focus=True)],
        [sg.Button('decode', size=(12, 1)), sg.CloseButton('Close', size=(12, 1))]
    ]
    
    window = sg.Window('', layout, no_titlebar=True, grab_anywhere=True)
    while True:
        event, value = window.read(close=True)
        
        # if event == 'go':
        #     getConfig(value['hex'], value['key'], value['iv'])
        
        if event == 'decode':
            data = json.loads(value['mLine'])
            decodeConfig(data['data']['dataHex'], value['key'], data['data']['ivHex'])
        
        
        if event in ('Close', None) or event == sg.WIN_CLOSED:
            try:
                exit(0)
            except:
                break
        window.close()
def resultWindow(resultText):

    #to create a window
    root = Tk()
    root.title('RemoteConfig')
    # root.geometry("600x900")
    
    #root window is the parent window
    fram = Frame(root)

    #adding label to search box
    Label(fram,text='Text to find: ',).pack(side=LEFT)
    
    
    #adding of single line text box
    edit = Entry(fram, width=40)

    #positioning of text box
    edit.pack(side=LEFT, fill=BOTH, expand=1)
    
    #setting focus
    edit.focus_set()
# =================================================================
    # TEST
    buttEncode = Button(fram, text='Encode')
    buttEncode.pack(side=RIGHT)
# =================================================================

    buttClear = Button(fram, text='Clear') 
    buttClear.pack(side=RIGHT)
    
    buttFind = Button(fram, text='Find') 
    buttFind.pack(side=RIGHT)

    fram.pack(side=TOP)
    # fram.pack(side=TOP)

    
    #  scrollBar
    v = Scrollbar(root, orient = 'vertical')
    v.pack(side=RIGHT, fill = 'y')
    
    #text box in root window
    text = Text(root, height=40, width=70, font=('Consolas',14), yscrollcommand=v.set)
    v.config(command=text.yview)
    text.pack(expand=True)
    # text.insert('1.0',open("C:\\Users\\frolov.an\\Desktop\\testHex.txt", 'r').read())
    text.insert("1.0", resultText)
    # text.config(state='disabled')

    def encode():
        iv = '5a677564567332496852716157716a376f774d774e5763314d766b6a36477548'
        key = '76817c188555fbf361df382e92f9bc8c'
        text = open("C:\\Users\\frolov.an\\Desktop\\testEncode.txt").read()        
        
        text = binascii.hexlify(text)
        key = binascii.hexlify(key)
        iv = binascii.hexlify(iv) 
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(text.encode())
        
        sg.Print(ciphertext.hex())
        input()


        # bytes = binascii.unhexlify(hex_bytes)
        # key = binascii.unhexlify(key)
        # iv = binascii.unhexlify(iv)
        
        # cipher = AES.new(key, AES.MODE_CBC, iv)
        # decoded_bytes = cipher.decrypt(bytes)
        # decoded_string = decoded_bytes.decode('utf-8')
        
        
    #function to search string in text
    def clear():
        text.tag_remove('found', '1.0', END)
        edit.delete(0, END)
        
    def find():
        #remove tag 'found' from index 1 to END
        text.tag_remove('found', '1.0', END)
        
        #returns to widget currently in focus
        s = edit.get()
        if s:
            idx = '1.0'
            while 1:
                #searches for desired string from index 1
                idx = text.search(s, idx, nocase=1,
                                stopindex=END)
                if not idx: break
                
                #last index sum of current index and
                #length of text
                lastidx = '%s+%dc' % (idx, len(s))
                
                #overwrite 'Found' at idx
                text.tag_add('found', idx, lastidx)
                idx = lastidx
                # text.mark_set("insert", lastidx)
            
            #mark located string as red
            text.tag_config('found', background='yellow')
            text.see(lastidx)

        edit.focus_set()
   
    buttEncode.config(command=encode)
    buttClear.config(command=clear)
    buttFind.config(command=find)
    
    root.mainloop()
startMenu()

