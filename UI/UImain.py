
import cv2
import mediapipe as mp
from PIL import ImageTk, Image
import numpy as np
from tkinter import Tk, PhotoImage, Label, Entry, Button, Frame, Checkbutton, IntVar
import time
import math

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import config
from HPE.class_mod import *

# DB 연결부
from DB.Database import * # import <사용할 클래스 혹은 함수>


# 화면 1. 로그인
def Login_Window(db):

    login_win = Tk()
    login_win.geometry("540x360+400+200")
    login_win.resizable(width=0, height=0)
    login_win.title("HPE_Login")
    login_win.configure(bg = 'lightblue')
    login_win.option_add("*Font", "맑은고딕 20")

    img1 = PhotoImage(file="UI/image/title.png", master=login_win)
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

    # 내부 함수 1. login
    def login():
        user_ID = ent1.get()
        user_PW = ent2.get()

        # 데이터베이스를 이용해 로그인 확인
        if db.log_in(user_ID, user_PW):
            # global flag_win
            config.flag_win = 4
            login_win.destroy()
        else:
            lab3.config(text="아이디와 비밀번호를 다시 확인해주세요")

    lab3.pack()
    btn1.config(command=login)
    btn1.pack()

    btn2 = Button(login_win)
    btn2.config(width=10, height=1)
    btn2.config(text = "Join")

    # 내부 함수 2. join
    def join():
        #global flag_win
        config.flag_win = 2
        login_win.destroy()
    btn2.config(command=join)
    btn2.pack()
    login_win.protocol("WM_DELETE_WINDOW", quit)

    login_win.mainloop()



# 화면 2. 회원가입
def Join_Window(db):
    join_win = Tk()
    join_win.geometry("540x340+420+200")
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
            
            # 데이터 베이스로 개인정보(ID, PW, 이름) 넘기는 부분
            db.sign_up(input_ID, input_Password, input_name)

            # global flag_win
            config.flag_win=3
            join_win.destroy()
        else:
            lab5.config(text="입력 정보를 다시 확인해 주세요.")

    lab5.pack()
    btn_a.config(command=click)
    btn_a.pack()

    join_win.protocol('WM_DELETE_WINDOW', quit)

    join_win.mainloop()


def RegiPose_Window(db):
    regi_win = Tk()
    regi_win.geometry("1000x650+100+50")
    regi_win.title("HPE_Login")
    regi_win.configure(bg='lightblue')
    regi_win.option_add("*Font", "맑은고딕 20")

    lab1 = Label(regi_win, font=("맑은고딕", "15", "bold"), background="lightblue")
    lab1.config(text="\n카메라를 10초간 응시하세요. 사용자 자세 등록을 실행 중 입니다.\n")
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
        config.flag_win = 1
        regi_win.destroy()

    btn_a.config(command=click)
    btn_a.pack()

    regi_win.protocol('WM_DELETE_WINDOW', quit)
    regi_win.mainloop()



def Main_Window(db):
        


    main_win = Tk()
    main_win.geometry("1280x720+10+10")
    main_win.minsize(1280,720)
    main_win.resizable(width=0, height=0)
    main_win.title("HPE_Main: Posture Correction Program")
    main_win.configure(bg = 'lightblue')
    main_win.option_add("*Font", "맑은고딕 20")

    img_logo = PhotoImage(file="UI/image/title.png", master=main_win)
    img_logo = img_logo.subsample(3)
    lab_logo = Label(main_win)
    lab_logo.config(image=img_logo, background = "lightblue")
    lab_logo.place(x=50, y=10)

    frm1 = Frame(main_win, bg = "LightCyan2", width=900, height=100)
    frm1.place(x=350, y=35)
    lab_alarm = Label(frm1, font = ("Courier", "20", "bold"), background= "LightCyan2")
    lab_alarm.config(text="최성현  |  "+"최근 알림: 알림 없음")
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
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose
    # 체크박스 변수와 버튼을 regiPose_Window 내에서 정의
    CheckVar1 = IntVar()
    c1 = Checkbutton(main_win, text="Visualization", variable=CheckVar1, bg="lightblue", font=("Arial", "15", "bold"))
    c1.place(x=545, y=680)

    Initial_cnt = 0
    Initial_last_time = time.time()

    # 어깨
    img1_1 = PhotoImage(file="UI/image/picture1.png", master=main_win)    # 0단계(good)
    img1_2 = PhotoImage(file="UI/image/picture2.png", master=main_win)    # 1단계
    img1_3 = PhotoImage(file="UI/image/picture3.png", master=main_win)    # 2단계(bad)
    img1_1 = img1_1.subsample(5)
    img1_2 = img1_2.subsample(5)
    img1_3 = img1_3.subsample(5)
    lab_img1 = Label(main_win)
    lab_img1.config(image=img1_1, background = "lightblue")
    lab_img1.place(x=750, y=200)

    # 거북목
    img2_1 = PhotoImage(file="UI/image/picture1.png", master=main_win)
    img2_2 = PhotoImage(file="UI/image/picture2.png", master=main_win)
    img2_3 = PhotoImage(file="UI/image/picture3.png", master=main_win)
    img2_1 = img2_1.subsample(5)
    img2_2 = img2_2.subsample(5)
    img2_3 = img2_3.subsample(5)
    lab_img2 = Label(main_win)
    lab_img2.config(image=img2_1, background = "lightblue")
    lab_img2.place(x=1000, y=200)

    # 턱괴기
    img3_1 = PhotoImage(file="UI/image/picture1.png", master=main_win)
    img3_2 = PhotoImage(file="UI/image/picture2.png", master=main_win)
    img3_1 = img3_1.subsample(5)
    img3_2 = img3_2.subsample(5)
    lab_img3 = Label(main_win)
    lab_img3.config(image=img3_1, background = "lightblue")
    lab_img3.place(x=750, y=450)

    # 환경 밝기
    img4_1 = PhotoImage(file="UI/image/picture1.png", master=main_win)
    img4_2 = PhotoImage(file="UI/image/picture2.png", master=main_win)
    img4_3 = PhotoImage(file="UI/image/picture3.png", master=main_win)
    img4_1 = img4_1.subsample(5)
    img4_2 = img4_2.subsample(5)
    img4_3 = img4_3.subsample(5)
    lab_img4 = Label(main_win)
    lab_img4.config(image=img4_1, background = "lightblue")
    lab_img4.place(x=1000, y=450)



    def video_play(count_time = 1):
        if count_time == 1:
            last_time = Initial_last_time
            cnt = Initial_cnt

        # 1초마다 좌표를 출력하기 위해 시간 저장 변수 설정
        success, image = cap.read()
        if not success:
            print("카메라 없음")
            return

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)

        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            results = pose.process(image)
            if CheckVar1.get() == 1:  # 체크박스가 선택된 경우 랜드마크 표시
                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        results.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
                    )
        

        # [[판단 시간 설정]] 1초마다 좌표 추출 및 출력
        current_time = time.time()
        if current_time - last_time >= 1.0:
            # [[틀린 기준 판단]] HPE를 성공한다면 출력 - README 파일의 키포인트 넘버 확인
            if results.pose_landmarks:
                # 단일 키 포인트
                left_eye = results.pose_landmarks.landmark[2]
                right_eye = results.pose_landmarks.landmark[6]
                left_shoulder = results.pose_landmarks.landmark[11]
                right_shoulder = results.pose_landmarks.landmark[12]
                left_mouth = results.pose_landmarks.landmark[9]
                right_mouth = results.pose_landmarks.landmark[10]
                left_ankle = results.pose_landmarks.landmark[28]
                right_ankle = results.pose_landmarks.landmark[29]

                # 합성 키 포인트
                config.angle_waist.data = abs(math.degrees(math.atan(right_shoulder.y - left_shoulder.y)/(right_shoulder.x - left_shoulder.x)))
                center_shoulder_dist = (left_shoulder.z + right_shoulder.z)/2
                center_mouth_dist = (left_mouth.z + right_mouth.z)/2
                left_hand_distance = math.sqrt((left_mouth.x - left_ankle.x)**2 + (left_mouth.y - left_ankle.y)**2)
                right_hand_distance = math.sqrt((right_mouth.x - right_ankle.x)**2 + (right_mouth.y - right_ankle.y)**2)

                config.monitor_near.data = center_shoulder_dist
                config.monitor_far.data = center_shoulder_dist
                config.turttle_neck.data = center_mouth_dist
                config.hands.data = min(left_hand_distance, right_hand_distance)
                
                # 개인 별 바른 자세 데이터(어디에 만들지 잘 모르겠어서 일단 여기에 만들었음)
                center_shoulder_dist_cho = -0.5
                center_mouth_dist_cho = -1.1

                outputList = config.result_pose(config.estimation_pose(center_shoulder_dist_cho, center_mouth_dist_cho))
                # 어깨 판단
                if outputList[0] == 1:
                    lab_img1.config(image=img1_2, background = "lightblue")
                elif outputList[0] == 2:
                    lab_img1.config(image=img1_3, background = "lightblue")
                else:
                    lab_img1.config(image=img1_1, background = "lightblue")

                # 거북목 판단
                if outputList[3] == 1:
                    lab_img2.config(image=img2_2, background = "lightblue")
                elif outputList[3] == 2:
                    lab_img2.config(image=img2_3, background = "lightblue")
                else:
                    lab_img2.config(image=img2_1, background = "lightblue")

                # 턱괴기 판단
                if outputList[4] == 1:
                    lab_img3.config(image=img3_2, background = "lightblue")
                else:
                    lab_img3.config(image=img3_1, background = "lightblue")

                # 환경밝기 판단
                # if outputList[5] == 1:
                #     lab_img3.config(image=img4_2, background = "lightblue")
                # elif outputList[5] == 2:
                #     lab_img3.config(image=img4_3, background = "lightblue")
                # else:
                #     lab_img3.config(image=img4_1, background = "lightblue")

                # 메시지 변경
                if (outputList[0] != 0 or outputList[3] != 0 or outputList[4] != 0): 
                    lab_alarm.config(text="최성현  |  "+"최근알림: 자세 불량 경고 알림이 발생하였습니다.")
                else:
                    lab_alarm.config(text="최성현  |  "+"최근알림: 자세 알림이 없습니다.")


                for i in range(5):
                    print(outputList[i])


                #print(f"cnt = {angle_waist.cnt:.4f}")
                #print(f"data = {angle_waist.data:.4f}")
                #print(f"output = {angle_waist.output:.4f}")    
            else: 
                cnt += 1
                if cnt > 10: # 확인 빠르게 하기 위해 10초로 설정, 추후에 1분으로 고치면 될 듯
                    print(1)
                    cnt = 0 # 이 부분 어떻게 처리할 것인지. 확인을 누르면 cnt를 0으로 돌릴지 논의
                else:
                    print(0)


            # 마지막 출력 시간 갱신
            last_time = current_time
            count_time += 1



        img = Image.fromarray(image)
        imgtk = ImageTk.PhotoImage(image=img)
        lbl_video.imgtk = imgtk
        lbl_video.configure(image=imgtk)
        lbl_video.after(10, video_play)

    video_play()


    main_win.protocol('WM_DELETE_WINDOW', quit)

    main_win.mainloop()