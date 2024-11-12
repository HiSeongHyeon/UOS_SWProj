
import cv2
import mediapipe as mp
from PIL import ImageTk, Image
import numpy as np
from tkinter import Tk, PhotoImage, Label, Entry, Button, Frame
import time

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
    global flag_win
    login_win.protocol("WM_DELETE_WINDOW", quit)

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

    join_win.protocol('WM_DELETE_WINDOW', quit)

    join_win.mainloop()

def regiPose_Window():
    regi_win = Tk()
    regi_win.geometry("1000x600+100+100")
    regi_win.title("HPE_Login")
    regi_win.configure(bg = 'lightblue')
    regi_win.option_add("*Font", "맑은고딕 20")

    # 동영상 라벨 만들기 파트
    # 동영상 위의 단어
    lab1 = Label(regi_win, font = ("맑은고딕", "20"), background = "lightblue")
    lab1.config(text="<카메라를 10초간 응시하세요. 사용자 자세 등록을 실행 중 입니다.>")
    lab1.pack()
    # 동영상이 들어갈 프레임 선언
    frm = Frame(regi_win, bg = "lightblue", width=120, height=120)
    frm.pack()
    # 동영상을 프레임에 위치 시킴
    lbl_video = Label(frm)
    lbl_video.pack()
    # videocapture 객체를 통해 동영상 재생
    cap = cv2.VideoCapture(0)
    def video_play():
        success, image = cap.read()
        if not success:
            print("카메라 없음")
            return
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        img = Image.fromarray(image)
        imgtk = ImageTk.PhotoImage(image=img)
        # opencv 동영상을 tkinter에 넣음
        lbl_video.imgtk = imgtk
        lbl_video.configure(image=imgtk)
        lbl_video.after(10, video_play)
    video_play()

    btn_a = Button(regi_win)
    btn_a.config(width=10, height=1)
    btn_a.config(text = "Register")
    def click():
        global flag_win
        flag_win=1
        regi_win.destroy()
    btn_a.config(command=click)
    btn_a.pack()

    regi_win.protocol('WM_DELETE_WINDOW', quit)

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
