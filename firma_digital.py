from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import ttk
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from PIL import ImageTk, Image
import tkinter as tk
import os, sys
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

raiz=Tk()
raiz.title("RSA Team 1 Cryptography")
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
combo['values']=('Encrypt','Decrypt')

def generar_llaves():
    os.system("openssl req -new -x509 -newkey rsa:2048 -keyout privkey.out -pubkey -out pubkey.out -days 365 -nodes -sha256")

def seleccionar_funcion():
        combo_sel=combo.get()
        if combo_sel == "Encrypt":
            generate_signature(key, data, sig_f)
            messagebox.showinfo("Success","Mensaje Encrypted Correctly")
        elif combo_sel == "Decrypt":
            verify_signature(key, data, sig_f)
            #messagebox.showinfo("Success","Message Decrypted Correctly")
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


sel=Button(raiz, text="Start process",command=seleccionar_funcion)
sel.place(x=50,y=180)

sel=Button(raiz, text="Generate Keys",command=generar_llaves)
sel.place(x=200,y=180)

data_f = "mensaje.txt"
key_f = "privkey.out"
sig_f = "mensaje_C_D.txt"

def generate_signature(key, data, sig_f):
    print("Generating Signature")
    h = SHA256.new(data)
    rsa = RSA.importKey(key)
    signer = PKCS1_v1_5.new(rsa)
    signature = signer.sign(h)
    with open(sig_f, 'wb') as f: f.write(signature)

def verify_signature(key, data, sig_f):
    print("Verifying Signature")
    h = SHA256.new(data)
    rsa = RSA.importKey(key)
    signer = PKCS1_v1_5.new(rsa)
    with open(sig_f, 'rb') as f: signature = f.read()
    rsp = "Success" if (signer.verify(h, signature)) else " Verification Failure"
    print(rsp)

# Read all file contents
with open(key_f, 'rb') as f: key = f.read()