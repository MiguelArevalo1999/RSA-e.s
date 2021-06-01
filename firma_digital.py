from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import ttk
import tkinter as tk
import os, sys
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Hash import SHA1
from Crypto.Signature import pkcs1_15
from sys import getsizeof
import linecache

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
    key_alice = RSA.generate(2048)
    private_key_alice = key_alice.export_key()
    file_out = open("private_alice.pem", "wb")
    file_out.write(private_key_alice)
    file_out.close()

    public_key_alice = key_alice.publickey().export_key()
    file_out = open("public_alice.pem", "wb")
    file_out.write(public_key_alice)
    file_out.close()

    key_bob = RSA.generate(2048)
    private_key_bob = key_bob.export_key()
    file_out = open("private_bob.pem", "wb")
    file_out.write(private_key_bob)
    file_out.close()

    public_key_bob = key_bob.publickey().export_key()
    file_out = open("public_bob.pem", "wb")
    file_out.write(public_key_bob)
    file_out.close()


def seleccionar_funcion():
        global signature_v
        combo_sel=combo.get()
        if combo_sel == "Signature":
            with open('strawberry.txt') as f:
                message = f.readlines()
                message = ''.join(message)
            encoded_string = message.encode("ISO-8859-1")
            byte_array_message = bytearray(encoded_string)
            message_to_sign = generate_digest(byte_array_message)
            signature_v = generate_signature(message_to_sign)

        elif combo_sel == "Verification":
            with open('message_s.txt') as f:
                file = f.readlines()
                message = file[0:37]
                message = ''.join(message)
                message = message.replace("\n\n","")
                sign = file[38:39]
                sign = ''.join(sign)
                print(message)
            encoded_string = message.encode("ISO-8859-1")
            byte_array_message = bytearray(encoded_string)
            digest_to_compare = generate_digest(byte_array_message)
            verify_signature(digest_to_compare, signature_v)

        else:
            messagebox.showinfo("Error ","You must select an option")

def abrirArchivo_a_Usar():
    raiz.archivo=filedialog.askopenfilename(initialdir="C:",title = "Select a txt file to sign or to verify",filetypes=(("txt files","*.txt"),("all files","*.*")))

def seleccionar_llave():
    raiz.llave=filedialog.askopenfilename(initialdir="C:",title = "Select private or public key",filetypes=(("pem files","*.pem"),("all files","*.*")))

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
    key = RSA.import_key(open('private_alice.pem').read())
    message_to_sign = message_to_sign.encode("ISO-8859-1")
    h = SHA256.new(message_to_sign)
    signature = pkcs1_15.new(key).sign(h)
    message_signed = signature.decode("ISO-8859-1")

    signed_file = open("message_s.txt", "w",encoding='utf-8')
    with open('strawberry.txt') as f:
        message_strawberry = f.readlines()
        message_strawberry = ''.join(message_strawberry)
    signed_file.write(message_strawberry)
    signed_file.write("\n\n")
    signed_file.write(message_signed)
    signed_file.close()



    return signature

def verify_signature(message, signature_v):
    key = RSA.import_key(open('public_alice.pem').read())
    message = message.encode("ISO-8859-1")
    h = SHA256.new(message)
    try:
        pkcs1_15.new(key).verify(h, signature_v)
        messagebox.showinfo("Success","Message verified correctly valid signature")
    except (ValueError, TypeError) as e:
        messagebox.showinfo("Error","Signature not valid")

raiz.mainloop()
