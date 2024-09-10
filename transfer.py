from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import socket
import os

root=Tk()
root.title("Shareit")
root.geometry("450x560+500+200")
root.configure(bg="#f4fdfe")
root.resizable(False,False)

#icon
image_icon=PhotoImage(file="image.png")
root.iconphoto(False,image_icon)


Label(root,text="File transfer",font=('Acumin Variable Concept',20,'bold'),bg="#f4fdfe").place(x=20,y=30)

Frame(root,width=400,height=2,bg="#f3f5fe").place(x=25,y=80)

send_image=PhotoImage(file="send.jpg")
send=Button(root,image=send_image,bg="#f4fdfe",bd=0)
send.place(x=50,y=100)

root.mainloop()
