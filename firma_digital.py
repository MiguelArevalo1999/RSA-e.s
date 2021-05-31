from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import ttk
import tkinter as tk
import os, sys
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Hash import SHA1
from Crypto.Signature import pkcs1_15


message_v = None
key_v = None
signature_v = None


raiz=Tk()
raiz.title("Digital Signature")
raiz.resizable(0,0)

raiz.geometry("500x250")
raiz.config(bg="cyan")

myFrame=Frame()
myFrame.pack(side="top")
myFrame.config(bg="white")
#myFrame.config(width="350", height="350")

#Logo ESCOM
imagen=tk.PhotoImage(file="logoescom.png")
imagen_sub=imagen.subsample(12)
widget=ttk.Label(image=imagen_sub)
widget.place(x=5,y=5)

#Logo IPN
imageni=tk.PhotoImage(file="ipn.png")
imageni_sub=imageni.subsample(15)
widgeti=ttk.Label(image=imageni_sub)
widgeti.place(x=400,y=5)

text = Label(text="Escuela Superior de Computo\n Oswaldo Aguilar Martinez \n Miguel Angel Arevalo Andrade")
text.place(x=125,y=7)

combo=ttk.Combobox(raiz)
combo.place(x=200,y=100)
combo['values']=('Signature','Verification')

def generar_llaves():
    pass

def seleccionar_funcion():
        global message_v,key_v, signature_v
        combo_sel=combo.get()
        if combo_sel == "Signature":
            with open('strawberry.txt') as f:
                message = f.readlines()
            encoded_string = message.encode()
            byte_array_message = bytearray(encoded_string)
            message_to_sign = generate_digest(byte_array_message)
            message_v,key_v, signature_v = generate_signature(message_to_sign)

            messagebox.showinfo("Success","Mensaje encrypted and signed correctly")
        elif combo_sel == "Verification":
            global message_v,key_v, signature_v 
            verify_signature(message_v,key_v, signature_v)
            messagebox.showinfo("Success","Message verified correctly")
        else:
            messagebox.showinfo("Error ","You must select an option")

def abrirArchivo_a_Usar():
    raiz.archivo=filedialog.askopenfilename(initialdir="C:")

def seleccionar_llave():
    raiz.llave=filedialog.askopenfilename(initialdir="C:")

abrir=Button(raiz, text="Select File",command=abrirArchivo_a_Usar)
abrir.place(x=50,y=100)

pubkey=Button(raiz, text="Select Key",command=seleccionar_llave)
pubkey.place(x=50,y=140)


start=Button(raiz, text="Start process",command=seleccionar_funcion)
start.place(x=50,y=180)

sel=Button(raiz, text="Generate Keys",command=generar_llaves)
sel.place(x=200,y=180)

def generate_digest(message):
    h = SHA1.new()
    h.update(message)

    return h.hexdigest()

def generate_signature(message_to_sign):
    print("Generating Signature")
    key = RSA.import_key(open('private_key.der').read())
    h = SHA256.new(message_to_sign)
    signature = pkcs1_15.new(key).sign(h)
    message_signed = signature.decode('utf-8')

    signed_file = open("message_s.txt", "w")
    signed_file.write(message_signed)
    signed_file.close()

    return message_to_sign,key,signature

def verify_signature(message_v,key_v, signature_v):
    key = RSA.import_key(open('public_key.der').read())
    h = SHA256.new(message_v)
    try:
        pkcs1_15.new(key).verify(h, signature_v)
        messagebox.showinfo("Success","Message verified correctly valid signature")
    except (ValueError, TypeError):
        messagebox.showinfo("Error","Signature not valid")

raiz.mainloop()