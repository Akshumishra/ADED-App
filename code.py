from tkinter import *
from tkinter import messagebox
import base64
import os

def decrypt():
    password = code.get()

    if password:
        screen2 = Toplevel(screen)
        screen2.title("Decryption")
        screen2.geometry("400x200")
        screen2.configure(bg="#00bd56")

        message = text1.get(1.0, END)
        try:
            decode_message = base64.b64decode(message.encode("ascii"))
            decode_message = bytearray(decode_message)
            for i in range(len(decode_message)):
                decode_message[i] ^= ord(password[i % len(password)])
            decrypt = decode_message.decode("ascii")

            Label(screen2, text="DECRYPT", font="arial", fg="white", bg="#00bd56").place(x=10, y=0)
            text2 = Text(screen2, font="Roboto 10", bg="white", relief=GROOVE, wrap=WORD, bd=0)
            text2.place(x=10, y=40, width=380, height=150)

            text2.insert(END, decrypt)
        except:
            messagebox.showerror("Decryption", "Invalid message or password")

    elif password == "":
        messagebox.showerror("Decryption", "Input password")

def encrypt():
    password = code.get()

    if password:
        screen1 = Toplevel(screen)
        screen1.title("Encryption")
        screen1.geometry("400x200")
        screen1.configure(bg="#ed3833")

        message = text1.get(1.0, END).strip()
        message_bytes = message.encode("ascii")
        message_bytes = bytearray(message_bytes)
        for i in range(len(message_bytes)):
            message_bytes[i] ^= ord(password[i % len(password)])
        base64_bytes = base64.b64encode(message_bytes)
        encrypt = base64_bytes.decode("ascii")

        Label(screen1, text="ENCRYPT", font="arial", fg="white", bg="#ed3833").place(x=10, y=0)
        text2 = Text(screen1, font="Roboto 10", bg="white", relief=GROOVE, wrap=WORD, bd=0)
        text2.place(x=10, y=40, width=380, height=150)

        text2.insert(END, encrypt)
    elif password == "":
        messagebox.showerror("Encryption", "Input password")

def main_screen():
    global screen
    global code
    global text1

    screen = Tk()
    screen.geometry("375x398")
    # icon
    image_icon = PhotoImage(file="logo.png")
    screen.iconphoto(False, image_icon)
    screen.title("ADED App")

    # command for reset button
    def reset():
        code.set("")
        text1.delete(1.0, END)

    # input section   
    Label(text="Enter text for encryption and decryption", fg="black", font=("Times New Roman", 13)).place(x=10, y=10)
    text1 = Text(font="Roboto 20", bg="white", relief=GROOVE, wrap=WORD, bd=0)
    text1.place(x=10, y=50, width=355, height=100)

    Label(text="Enter secret key for encryption and decryption", fg="black", font=("Times New Roman", 13)).place(x=10, y=170)

    code = StringVar()
    Entry(textvariable=code, width=19, bd=0, font=("arial", 25), show="*").place(x=10, y=200)

    # Buttons section
    Button(text="ENCRYPT", height="2", width=23, bg="#ed3833", bd=0, command=encrypt).place(x=10, y=250)
    Button(text="DECRYPT", height="2", width=23, bg="#00bd56", fg="white", bd=0, command=decrypt).place(x=200, y=250)
    Button(text="RESET", height="2", width=50, bg="#1089ff", fg="white", bd=0, command=reset).place(x=10, y=300)

    screen.mainloop()

main_screen()
