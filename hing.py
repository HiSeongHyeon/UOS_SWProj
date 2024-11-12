
import cv2
from tkinter import *

global flag_win
flag_win = 1


def Login_Window():
    login_win = Tk()
    login_win.geometry("640x480")
    login_win.title("HPE_Login")
    login_win.configure(bg = 'lightblue')
    login_win.option_add("*Font", "맑은고딕 20")

    img1 = PhotoImage(file="C:/Users/jihwa/Desktop/worksp/program/title.png", master=login_win)
    img1 = img1.subsample(4)
    lab_logo = Label(login_win)
    lab_logo.config(image=img1, background = "lightblue")
    lab_logo.pack()

    lab1 = Label(login_win, font = ("맑은고딕", "20"), background = "lightblue")
    lab1.config(text="ID")
    lab1.pack()

    ent1 = Entry(login_win, font=("맑은고딕", "20"))
    ent1.pack()

    lab2 = Label(login_win, font = ("맑은고딕", "20"), background = "lightblue")
    lab2.config(text="PW")
    lab2.pack()

    ent2 = Entry(login_win)
    ent2.config(show = "*")
    ent2.pack()
    
    btn1 = Button(login_win)
    btn1.config(width=10, height=1)
    btn1.config(text = "Login")
    def login():
        user_ID = ent1.get()
        user_PW = ent2.get()
        if user_ID == "1234" and user_PW == "1234":
            global flag_win
            flag_win=4
            login_win.destroy()
    btn1.config(command=login)
    btn1.pack()

    btn2 = Button(login_win)
    btn2.config(width=10, height=1)
    btn2.config(text = "Join")
    def join():
        global flag_win
        flag_win=2
        login_win.destroy()
    btn2.config(command=join)
    btn2.pack()
    
    login_win.mainloop()
    

def Join_Window():
    join_win = Tk()
    join_win.geometry("640x480")
    join_win.title("HPE_Login")
    join_win.configure(bg = 'lightblue')
    join_win.option_add("*Font", "맑은고딕 20")

    lab0 = Label(join_win, font = ("맑은고딕", "20"), background = "lightblue")
    lab0.config(text="Name Input")
    lab0.pack()

    ent1 = Entry(join_win, font=("맑은고딕", "20"))
    ent1.pack()

    lab1 = Label(join_win, font = ("맑은고딕", "20"), background = "lightblue")
    lab1.config(text="ID Input")
    lab1.pack()

    ent1 = Entry(join_win, font=("맑은고딕", "20"))
    ent1.pack()

    lab2 = Label(join_win, font = ("맑은고딕", "20"), background = "lightblue")
    lab2.config(text="PW Input")
    lab2.pack()

    ent2 = Entry(join_win, font=("맑은고딕", "20"))
    ent2.pack()

    btn_a = Button(join_win)
    btn_a.config(width=10, height=1)
    btn_a.config(text = "Next")
    def click():
        global flag_win
        flag_win=3
        join_win.destroy()
    btn_a.config(command=click)
    btn_a.pack()


    join_win.mainloop()

def regiPose_Window():
    regi_win = Tk()
    regi_win.geometry("640x480")
    regi_win.title("HPE_Login")
    regi_win.configure(bg = 'lightblue')
    regi_win.option_add("*Font", "맑은고딕 20")


    btn_a = Button(regi_win)
    btn_a.config(width=10, height=1)
    btn_a.config(text = "Register")
    def click():
        global flag_win
        flag_win=1
        regi_win.destroy()
    btn_a.config(command=click)
    btn_a.pack()

    regi_win.mainloop()



while True:
    if (flag_win == 1):
        Login_Window()
    elif (flag_win == 2):
        Join_Window()
    elif (flag_win == 3):
        regiPose_Window()
    else:
        quit()
