import binascii
from Crypto.Cipher import AES
import getpass
import PySimpleGUI as sg
from tkinter import *
import json
import hashlib

def encode():
    key = b'0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef'
    iv = b'0123456789abcdef0123456789abcdef'
    text = b'Hello World!'     
    # b'4f2edc4eedab0a8b9a4941d72ec1ca6d'
    
    key = binascii.unhexlify(key)
    text = binascii.hexlify(text)
    iv = binascii.unhexlify(iv)
    
    PAD_SIZE = 16
    pad = lambda s: s + (PAD_SIZE - len(s) % PAD_SIZE) * chr(PAD_SIZE - len(s) % PAD_SIZE).encode()
    message_padded = pad(text)
    cipher = AES.new(hashlib.sha256(key).digest(), AES.MODE_CBC, iv)
    encrypted_message = cipher.encrypt(message_padded)
    # print(encrypted_message)
    sg.Print(encrypted_message)

    
encode()