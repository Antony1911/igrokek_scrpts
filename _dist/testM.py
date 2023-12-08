import PySimpleGUI as sg
from tkinter import *
from tkinter.ttk import *
from tkinter.ttk import Widget

testText = """We're also setting up an event loop to handle user interactions with the window. When the user clicks the 'Search' button (or presses Enter), we're displaying a popup asking them to enter the search term. If the user enters a search term and clicks 'OK', we're calling our `search_output` function to look for that text in the output."""


# import PySimpleGUI as sg

# text = """
# This program is designed to turn a black and white image into a double-knit template.
# If your image doesn't display as desired, adjusting the contrast might help.
# """.strip()

# lines = text.split('\n')
# index1 = lines[0].index("image")
# index2 = lines[1].index("image")
# indexes = [(f'1.{index1}', f'1.{index1+5}'), (f'2.{index2}', f'2.{index2+5}')]

# sg.theme('DarkBlue3')
# font1 = ('Courier New', 10)
# font2 = ('Courier New', 10, 'bold')
# sg.set_options(font=font1)

# layout = [
#     [sg.Multiline(text, size=(40, 8), key='-MULTILINE')],
#     [sg.Push(), sg.Button('Highlight'), sg.Button('Remove')],
# ]
# window = sg.Window('Title', layout, finalize=True)
# multiline = window['-MULTILINE']
# widget = multiline.Widget
# widget.tag_config('HIGHLIGHT', foreground='white', background='blue', font=font2)
# # widget.tag_config('HIGHLIGHT', foreground=multiline.BackgroundColor, background=multiline.TextColor, font=font2)

# while True:

#     event, values = window.read()

#     if event == sg.WIN_CLOSED:
#         break
#     elif event == 'Highlight':
#         for index1, index2 in indexes:
#             widget.tag_add('HIGHLIGHT', index1, index2)
#         window['Highlight'].update(disabled=True)
#     elif event == 'Remove':
#         for index1, index2 in indexes:
#             widget.tag_remove('HIGHLIGHT', index1, index2)
#         window['Highlight'].update(disabled=False)

# window.close()


# ------------------------------------------------------------------------------------------------------------------------
# def search_text(window, search_term):
#   text = window['-MULTILINE-'].get()
#   match_start = text.find(search_term)
#   if match_start != -1:
#     window['-MULTILINE-'].set_focus()
#     window['-MULTILINE-'].Widget.tag_add('found', f'1.{match_start}', f'1.{match_start+len(search_term)}')
#     window['-MULTILINE-'].Widget.see(f'1.{match_start}')
#   else:
#     sg.popup('No matches found')

# layout = [
#   [sg.Multiline(default_text=testText,key='-MULTILINE-', size=(50, 10), font=('Courier', 12), enable_events=True)],
#   [sg.Text('Search:'), sg.Input(key='-SEARCH-'), sg.Button('Find')]
# ]

# window = sg.Window('Text Search Demo', layout)

# while True:
#   event, values = window.read()
#   if event in [sg.WIN_CLOSED, 'Exit']:
#     break
#   elif event == 'Find':
#     search_term = values['-SEARCH-']
#     search_text(window, search_term)
# window.close()

# -----------------------------------------------------------------------------------------------------------------------
# def highlight_text(text, phrase):
#   '''
#   Function to find and highlight a specific phrase in a given text.
#   '''
#   highlighted_text = text.replace(phrase, f"\033[1;42;37m{phrase}\033[m") # replace the phrase with highlighted version
#   return highlighted_text

# # Testing the function with sample inputs
# input_text = input("Enter a text: ")
# highlight_phrase = input("Enter a phrase to highlight: ")
# output_text = highlight_text(input_text, highlight_phrase)
# print("Highlighted text: ")
# print(output_text)
# -----------------------------------------------------------------------------------------------------------------------
# import PySimpleGUI as sg

# def find_and_highlight(search_str, text_input):
#   start = 0
#   while True:
#     start = text_input.find(search_str, start)
    
#     if start == -1:
#         break
#     end = start + len(search_str)
#     # text_input = f'{text_input[:start]}[[{search_str}]]{text_input[end:]}'
#     text_input = f'{text_input[:start]}[[{search_str}]]{text_input[end:]}'
    
#     start = end + 8  # adjust for the added highlight code
#     print(f"{start} <-------------------------------- {text_input}")
#     return text_input

# sg.theme('DarkGrey2')
# layout = [
#   [sg.Text('Search for:'), sg.Input(key='-SEARCH-')],
#   [sg.Multiline(default_text=testText, key='-TEXT-', size=(50, 10))],
#   [sg.Button('Search'), sg.Button('Clear')]
# ]

# window = sg.Window('Find and Highlight', layout)

# while True:
#   event, values = window.read()
  
# #   multiline = window['-TEXT-']
# #   widget = multiline.Widget
# #   widget.tag_config('HIGHLIGHT', foreground='white', background='blue')
  
#   if event == 'Search':
#     search_str = values['-SEARCH-']
#     text_input = values['-TEXT-']
#     highlighted_text = find_and_highlight(search_str, text_input)
#     window['-TEXT-'].update(highlighted_text, background_color='yellow')
#     # window['-TEXT-'].update(value=highlighted_text, background_color_for_value='green')
#   elif event == 'Clear':
#     window['-SEARCH-'].update('')
#     # window['-TEXT-'].update('')
#     window['-TEXT-'].update(background_color='white')
    
#   elif event == sg.WIN_CLOSED:
#     break
# window.close()

# -----------------------------------------------------------------------------------------------------------------------
from tkinter import *

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
 
#adding of search button
buttClear = Button(fram, text='Clear') 
buttClear.pack(side=RIGHT)
butt = Button(fram, text='Find') 
butt.pack(side=RIGHT)
fram.pack(side=TOP)
# fram.pack(side=TOP)

 
#  scrollBar
v = Scrollbar(root, orient = 'vertical')
v.pack(side=RIGHT, fill = 'y')
 
#text box in root window
text = Text(root, height=40, width=70, font=('Consolas',14), yscrollcommand=v.set)
v.config(command=text.yview)
text.pack(expand=True)
text.insert('1.0',open("C:\\Users\\frolov.an\\Desktop\\testHex.txt", 'r').read())
# text.config(state='disabled')

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
buttClear.config(command=clear)
butt.config(command=find)
 
root.mainloop()


# ---------------------------------------------------------------------------------------------------------

# import sys
# from PyQt5 import QtWidgets, QtGui, QtCore
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui     import *
# from PyQt5.QtCore    import *


# class Ui_MainWindow(object):
#     def setupUi(self, MainWindow):
#         MainWindow.setObjectName("MainWindow")
#         MainWindow.resize(600, 900)
#         self.centralwidget = QtWidgets.QWidget(MainWindow)
#         self.centralwidget.setObjectName("centralwidget")
#         self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
#         self.gridLayout.setObjectName("gridLayout")
#         self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
#         self.textEdit.setObjectName("textEdit")
#         self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)
#         MainWindow.setCentralWidget(self.centralwidget)
#         self.menubar = QtWidgets.QMenuBar(MainWindow)
#         self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
#         self.menubar.setObjectName("menubar")
#         self.menuFile = QtWidgets.QMenu(self.menubar)
#         self.menuFile.setObjectName("menuFile")
#         self.menuSearch = QtWidgets.QMenu(self.menubar)
#         self.menuSearch.setObjectName("menuSearch")
#         MainWindow.setMenuBar(self.menubar)
#         self.statusbar = QtWidgets.QStatusBar(MainWindow)
#         self.statusbar.setObjectName("statusbar")
#         MainWindow.setStatusBar(self.statusbar)
#         self.actionOpen = QtWidgets.QAction(MainWindow)
#         self.actionOpen.setObjectName("actionOpen")
#         self.actionSave = QtWidgets.QAction(MainWindow)
#         self.actionSave.setObjectName("actionSave")
#         self.actionExit = QtWidgets.QAction(MainWindow)
#         self.actionExit.setObjectName("actionExit")
#         self.actionFind = QtWidgets.QAction(MainWindow)
#         self.actionFind.setObjectName("actionFind")
#         self.actionWord_Count = QtWidgets.QAction(MainWindow)
#         self.actionWord_Count.setObjectName("actionWord_Count")
#         self.actionNew = QtWidgets.QAction(MainWindow)
#         self.actionNew.setObjectName("actionNew")
#         self.menuFile.addAction(self.actionNew)
#         self.menuFile.addAction(self.actionOpen)
#         self.menuFile.addAction(self.actionSave)
#         self.menuFile.addAction(self.actionExit)
#         self.menuSearch.addAction(self.actionFind)
#         self.menuSearch.addAction(self.actionWord_Count)
#         self.menubar.addAction(self.menuFile.menuAction())
#         self.menubar.addAction(self.menuSearch.menuAction())

#         self.retranslateUi(MainWindow)
#         QtCore.QMetaObject.connectSlotsByName(MainWindow)

#     def retranslateUi(self, MainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
#         self.menuFile.setTitle(_translate("MainWindow", "File"))
#         self.menuSearch.setTitle(_translate("MainWindow", "Search"))
#         self.actionOpen.setText(_translate("MainWindow", "Open"))
#         self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
#         self.actionSave.setText(_translate("MainWindow", "Save"))
#         self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
#         self.actionExit.setText(_translate("MainWindow", "Exit"))
#         self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
#         self.actionFind.setText(_translate("MainWindow", "Find"))
#         self.actionFind.setShortcut(_translate("MainWindow", "Ctrl+F"))
#         self.actionWord_Count.setText(_translate("MainWindow", "Word Count"))
#         self.actionNew.setText(_translate("MainWindow", "New"))
#         self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))

# class Ui_Dock_Find(object):
#     def setupUi(self, Dock_Find):
#         Dock_Find.setObjectName("Dock_Find")
#         Dock_Find.resize(320, 65)
#         Dock_Find.setMinimumSize(QtCore.QSize(320, 65))
#         font = QtGui.QFont()
#         font.setPointSize(10)
#         Dock_Find.setFont(font)
#         icon = QtGui.QIcon()

# #        icon.addPixmap(QtGui.QPixmap(":/image/graphy_100px.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
#         icon.addPixmap(QtGui.QPixmap("Ok.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

#         Dock_Find.setWindowIcon(icon)
#         self.dockWidgetContents = QtWidgets.QWidget()
#         self.dockWidgetContents.setObjectName("dockWidgetContents")
#         self.serachLabel = QtWidgets.QLabel(self.dockWidgetContents)
#         self.serachLabel.setGeometry(QtCore.QRect(10, 10, 71, 16))
#         self.serachLabel.setObjectName("serachLabel")
#         self.findLine = QtWidgets.QLineEdit(self.dockWidgetContents)
#         self.findLine.setGeometry(QtCore.QRect(80, 10, 151, 20))
#         self.findLine.setObjectName("findLine")
#         self.findButton = QtWidgets.QPushButton(self.dockWidgetContents)
#         self.findButton.setGeometry(QtCore.QRect(240, 10, 75, 23))
#         self.findButton.setObjectName("findButton")
#         Dock_Find.setWidget(self.dockWidgetContents)

#         self.retranslateUi(Dock_Find)
#         QtCore.QMetaObject.connectSlotsByName(Dock_Find)

#     def retranslateUi(self, Dock_Find):
#         _translate = QtCore.QCoreApplication.translate
#         Dock_Find.setWindowTitle(_translate("Dock_Find", "Find"))
#         self.serachLabel.setText(_translate("Dock_Find", "Search For:"))
#         self.findButton.setText(_translate("Dock_Find", "Find"))

# class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
#     def __init__(self, parent=None):
#         super(MainWindow, self).__init__(parent)
#         self.setupUi(self)

#         self.actionNew.triggered.connect(self.newFile)
#         self.actionOpen.triggered.connect(self.openFile)
#         self.actionSave.triggered.connect(self.saveFile)
#         self.actionExit.triggered.connect(self.exitFile)
#         self.actionFind.triggered.connect(self.findWord)
#         self.actionWord_Count.triggered.connect(self.countWord)
#         self.show()
#         # self.showMaximized()

#         self.textEdit.setFont(QFont('Decorative', 12))                      # +
#         self.countWords = 0                                                 # +++

#     def newFile(self):
#         self.textEdit.clear()

#     def openFile(self):
#         filename = QFileDialog.getOpenFileName(self, 'Open File', ".","(*.txt *.py)")   # + *.py
#         if filename[0]:
#             fmt = QTextCharFormat()
#             fmt.setForeground(QColor(0, 0, 0))
#             fmt.setFontPointSize(12)
#             self.textEdit.mergeCurrentCharFormat(fmt)

#             f = open(filename[0], 'rt')
#             with f:
#                 data = f.read()
#                 self.textEdit.setText(data)

#     def saveFile(self):
#         filename = QFileDialog.getSaveFileName(self, 'Save File', ".", "(*.txt)")
#         if filename[0]:
#             f = open(filename[0], 'wt')
#             with f:
#                 text = self.textEdit.toPlainText()
#                 f.write(text)
#                 QMessageBox.about(self, "Save File", "File Saved Successfully")

#     def exitFile(self):
#         choice = QMessageBox.question(self, 'Close', "Do you want to close?", QMessageBox.Yes | QMessageBox.No)
#         if choice == QMessageBox.Yes:
#             self.saveFile()
#             self.close()
#         else:
#             pass

#     def findWord(self):

#         self.dock = Dock_Find()
#         self.addDockWidget(Qt.TopDockWidgetArea, self.dock)
#         self.dock.show()
#         self.dock.findButton.clicked.connect(self.handleFind)

# ### +++ vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

#     def mergeFormatOnWordOrSelection(self, format):
#         cursor = self.textEdit.textCursor()
#         if not cursor.hasSelection():
#             cursor.select(QTextCursor.WordUnderCursor)
#         cursor.mergeCharFormat(format)
#         self.textEdit.mergeCurrentCharFormat(format)

#     def handleFind(self):
#         text = self.dock.findLine.text()
#         self.textEdit.moveCursor(QTextCursor.Start)
        
#         if not text:
#             return
#         col = QColorDialog.getColor(self.textEdit.textColor(), self)

#         if not col.isValid():
#             return
#         fmt = QTextCharFormat()
#         fmt.setBackground(col)
#         # print("\nfmt.setForeground(col)", col)
#         # fmt.setFontPointSize(14)     

#         self.textEdit.moveCursor(QTextCursor.Start)

#         self.countWords = 0
#         while self.textEdit.find(text, QTextDocument.FindWholeWords):      # Find whole words
#             self.mergeFormatOnWordOrSelection(fmt)
#             self.countWords += 1

# #         QMessageBox.information(self, 
# #             "Information", 
# # #            f"word->`{text}` found in the text `{self.countWords}` times."
# #              "word->`{text}` found ----in the text `{countWords}` times.".format(text=text, countWords=self.countWords)
# #         )

# ### +++ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    

#     """ ---
#         self.dock = Dock_Find()
#         self.addDockWidget(Qt.TopDockWidgetArea, self.dock)
#         self.dock.show()

#         def handleFind():
#             text = self.dock.findLine.text()
#             if self.textEdit.find(text):
#                 return
#             else:
#                 fmt = QTextCharFormat()
#                 fmt.setBackground(Qt.yellow)
#                 self.textEdit.moveCursor(QTextCursor.Start)
#                 while self.textEdit.find(text, QTextDocument.FindWholeWords):
#                     self.mergeFormatOnWordsSelection(fmt)
#                 if self.textEdit.find(text):
#                     while self.textEdit.moveCursor(QTextCursor.EndOfWord):
#                         QMessageBox.about(self, "End of Line", "No Further More Words")
#                     return
#             QMessageBox.about(self, "No Match", "No Words Found")
#         self.dock.findButton.clicked.connect(handleFind)

#     def mergeFormatOnWordsSelection(self, format):
#         cursor = self.textEdit.textCursor()
#         if not cursor.hasSelection():
#             cursor.select(QTextCursor.WordUnderCursor)
#         cursor.mergeCharFormat(format)
#         self.textEdit.mergeCurrentCharFormat(format)
#     """ 

#     def countWord(self):
#         textWord    = self.textEdit.textCursor().selectedText()
#         words   = str(len(textWord.split()))
#         symbols = str(len(textWord))

# #?        self.currenWords.setText(words)
# #?        self.currentSymbols.setText(symbols)

#         text = self.textEdit.toPlainText()
#         words = str(len(text.split()))
#         symbols = str(len(text))

# #?        self.totalWords.setText(words)
# #?        self.totalSymbols.setText(symbols)

# #        print(f"word->`{self.dock.findLine.text()}` found in the text `{self.countWords}` times.") # +
#         print("word->`{text}` found in the text `{countWords}` times."
#               "".format(text=self.dock.findLine.text(), countWords=self.countWords)) # +

#         QMessageBox.information(self, 
#             "Information", 
# #            f"word->`{textWord}` found in the text `{self.countWords}` times."
#             "word->`{textWord}` found in the text `{countWords}` times."
#             "".format(textWord=textWord, countWords=self.countWords)
#         )

# class Dock_Find(QtWidgets.QDockWidget, Ui_Dock_Find):
#     def __init__(self, parent=None):
#         super(Dock_Find, self).__init__(parent)
#         self.setupUi(self)
#         self.findLine.setPlaceholderText("Type Here")


# if __name__== '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     qt_app = MainWindow()
#     qt_app.show()
#     sys.exit(app.exec_())