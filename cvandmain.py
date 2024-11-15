
import cv2
import mediapipe as mp
from PIL import ImageTk, Image
import numpy as np
from tkinter import Tk, PhotoImage, Label, Entry, Button, Frame, Checkbutton, IntVar
import time

global flag_win
flag_win = 1

def Login_Window():
    login_win = Tk()
    login_win.geometry("540x360+400+200")
    login_win.resizable(width=0, height=0)
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
    lab3 = Label(login_win, font = ("맑은고딕", "10"), background = "lightblue", fg="red")
    def login():
        user_ID = ent1.get()
        user_PW = ent2.get()
        if user_ID == "1234" and user_PW == "1234":
            global flag_win
            flag_win=4
            login_win.destroy()
        else:
            lab3.config(text="아이디와 비밀번호를 다시 확인해주세요")
    lab3.pack()
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
    join_win.geometry("540x400+420+200")
    join_win.resizable(width=0, height=0)
    join_win.title("HPE_Join")
    join_win.configure(bg = 'lightblue')
    join_win.option_add("*Font", "맑은고딕 20")

    lab1 = Label(join_win, font = ("맑은고딕", "20"), background = "lightblue")
    lab1.config(text="Name Input")
    lab1.pack()
    ent1 = Entry(join_win, font=("맑은고딕", "20"))
    ent1.insert(0,"최성현")
    def clear1(event):
        if ent1.get() == "최성현":
            ent1.delete(0,len(ent1.get()))
    ent1.bind("<Button-1>",clear1)
    ent1.pack()

    lab2 = Label(join_win, font = ("맑은고딕", "20"), background = "lightblue")
    lab2.config(text="ID Input")
    lab2.pack()
    ent2 = Entry(join_win, font=("맑은고딕", "20"))
    ent2.insert(0,"doq1324@naver.com")
    def clear2(event):
        if ent2.get() == "doq1324@naver.com":
            ent2.delete(0,len(ent2.get()))
    ent2.bind("<Button-1>",clear2)
    ent2.pack()

    lab3 = Label(join_win, font = ("맑은고딕", "20"), background = "lightblue")
    lab3.config(text="PW Input")
    lab3.pack()
    ent3 = Entry(join_win, font=("맑은고딕", "20"))
    ent3.config(show="*")
    ent3.pack()

    lab4 = Label(join_win, font = ("맑은고딕", "20"), background = "lightblue")
    lab4.config(text="PW check")
    lab4.pack()
    ent4 = Entry(join_win, font=("맑은고딕", "20"))
    ent4.config(show="*")
    ent4.pack()

    lab5 = Label(join_win, font = ("맑은고딕", "10"), background = "lightblue", fg="red")
    btn_a = Button(join_win)
    btn_a.config(width=10, height=1)
    btn_a.config(text = "Next")
    def click():
        input_name = ent1.get()
        input_ID = ent2.get()
        input_Password = ent3.get()
        Check_Password = ent4.get()
        if (input_Password == Check_Password) and (len(input_name) != 0 and len(input_ID) != 0 and len(input_Password) != 0):
            '''
            데이터 베이스로 개인정보(이름, 아이디, 비밀번호) 넘기는 부분
            '''
            global flag_win
            flag_win=3
            join_win.destroy()
        else:
            lab5.config(text="입력 정보를 다시 확인해 주세요.")

    lab5.pack()
    btn_a.config(command=click)
    btn_a.pack()

    join_win.protocol('WM_DELETE_WINDOW', quit)

    join_win.mainloop()


def RegiPose_Window():
    regi_win = Tk()
    regi_win.geometry("1000x600+100+100")
    regi_win.title("HPE_Login")
    regi_win.configure(bg='lightblue')
    regi_win.option_add("*Font", "맑은고딕 20")

    lab1 = Label(regi_win, font=("맑은고딕", "10"), background="lightblue")
    lab1.config(text="카메라를 10초간 응시하세요. 사용자 자세 등록을 실행 중 입니다.")
    lab1.pack()

    frm = Frame(regi_win, bg="lightblue", width=120, height=120)
    frm.pack()

    lbl_video = Label(frm)
    lbl_video.pack()

    cap = cv2.VideoCapture(0)
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    def video_play():
        success, image = cap.read()
        if not success:
            print("카메라 없음")
            return

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)

        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            results = pose.process(image)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
                )
        
        img = Image.fromarray(image)
        imgtk = ImageTk.PhotoImage(image=img)
        lbl_video.imgtk = imgtk
        lbl_video.configure(image=imgtk)
        lbl_video.after(10, video_play)

    video_play()

    btn_a = Button(regi_win)
    btn_a.config(width=10, height=1)
    btn_a.config(text="Register")

    def click():
        global flag_win
        flag_win = 1
        regi_win.destroy()

    btn_a.config(command=click)
    btn_a.pack()

    regi_win.protocol('WM_DELETE_WINDOW', quit)
    regi_win.mainloop()


def Main_Window():
    main_win = Tk()
    main_win.geometry("1280x720+10+10")
    main_win.minsize(1280,720)
    main_win.resizable(width=0, height=0)
    main_win.title("HPE_Main: Posture Correction Program")
    main_win.configure(bg = 'lightblue')
    main_win.option_add("*Font", "맑은고딕 20")

    img_logo = PhotoImage(file="C:/Users/jihwa/Desktop/worksp/program/title.png", master=main_win)
    img_logo = img_logo.subsample(3)
    lab_logo = Label(main_win)
    lab_logo.config(image=img_logo, background = "lightblue")
    lab_logo.place(x=50, y=10)

    frm1 = Frame(main_win, bg = "LightCyan2", width=900, height=100)
    frm1.place(x=350, y=35)
    lab_alarm = Label(frm1, font = ("Courier", "20", "bold"), background= "LightCyan2")
    lab_alarm.config(text="최성현  |  "+"최근알림:척추 측만증 경고가 발생하였습니다.(1분전)")
    lab_alarm.place(x=10, y=32)


    # 동영상 라벨 만들기 파트
    # 동영상이 들어갈 프레임 선언
    frm = Frame(main_win, bg = "lightblue", width=100, height=100)
    frm.place(x=50, y=195)
    # 동영상을 프레임에 위치 시킴
    lbl_video = Label(frm)
    lbl_video.pack()
    # videocapture 객체를 통해 동영상 재생
    cap = cv2.VideoCapture(0)
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    # 체크박스 변수와 버튼을 regiPose_Window 내에서 정의
    CheckVar1 = IntVar()
    c1 = Checkbutton(main_win, text="Visualization", variable=CheckVar1, bg="lightblue", font=("Arial", "15", "bold"))
    c1.place(x=545, y=680)

    def video_play():
        success, image = cap.read()
        if not success:
            print("카메라 없음")
            return

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)

        if CheckVar1.get() == 1:  # 체크박스가 선택된 경우 랜드마크 표시
            with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
                results = pose.process(image)

                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        results.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
                    )
        
        img = Image.fromarray(image)
        imgtk = ImageTk.PhotoImage(image=img)
        lbl_video.imgtk = imgtk
        lbl_video.configure(image=imgtk)
        lbl_video.after(10, video_play)

    video_play()

    img1 = PhotoImage(file="C:/Users/jihwa/Desktop/worksp/program/picture1.png", master=main_win)
    img1 = img1.subsample(5)
    lab_img1 = Label(main_win)
    lab_img1.config(image=img1, background = "lightblue")
    lab_img1.place(x=750, y=200)

    img2 = PhotoImage(file="C:/Users/jihwa/Desktop/worksp/program/picture2.png", master=main_win)
    img2 = img2.subsample(5)
    lab_img2 = Label(main_win)
    lab_img2.config(image=img2, background = "lightblue")
    lab_img2.place(x=1000, y=200)

    img3 = PhotoImage(file="C:/Users/jihwa/Desktop/worksp/program/picture3.png", master=main_win)
    img3 = img3.subsample(5)
    lab_img3 = Label(main_win)
    lab_img3.config(image=img3, background = "lightblue")
    lab_img3.place(x=750, y=450)

    img4 = PhotoImage(file="C:/Users/jihwa/Desktop/worksp/program/picture4.png", master=main_win)
    img4 = img4.subsample(5)
    lab_img4 = Label(main_win)
    lab_img4.config(image=img4, background = "lightblue")
    lab_img4.place(x=1000, y=450)

    main_win.protocol('WM_DELETE_WINDOW', quit)

    main_win.mainloop()


while True:
    if (flag_win == 1):
        Login_Window()
    elif (flag_win == 2):
        Join_Window()
    elif (flag_win == 3):
        RegiPose_Window()
    elif (flag_win == 4):
        Main_Window()
    else:
        print("비정상적으로 프로그램 작동함.\n")
        quit()