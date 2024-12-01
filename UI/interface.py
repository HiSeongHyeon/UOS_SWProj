import cv2
import mediapipe as mp
from PIL import ImageTk, Image
import numpy as np
from tkinter import Tk, PhotoImage, Label, Entry, Button, Frame, Checkbutton, IntVar, Toplevel, HORIZONTAL
import tkinter.ttk as ttk
import time
import math

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import config
from HPE.class_mod import *

# DB 연결부
from DB.db import * # import <사용할 클래스 혹은 함수>

#비디오 객체 담는 변수#
video_frames = [None]

# PyInstaller 경로 찾기 함수
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# 화면 1. 로그인
def Login_Window(db):

    # 기본 창 설정
    login_win = Tk()
    login_win.geometry("1080x608+150+60")
    login_win.resizable(width=0, height=0)
    login_win.title("HPE_Login")
    login_win.iconbitmap("UI/img/logo.ico")
    # 로그인 창에 들어갈 배경경 이미지 설정
    image_path1 = resource_path("UI/img/login_bg.png")
    login_win.frame_photo = PhotoImage(file = image_path1,master=login_win)
    frame_label = Label(login_win, border = 0, image = login_win.frame_photo)
    frame_label.pack(fill = "both", expand = True)
    
    #창닫기 함수 정의 
    def on_close():
        login_win.destroy()
        config.flag_win=0

    # ID 입력부
    ent_ID = Entry(login_win, font=("Arial", "15"), width = 22, bg = 'white', border = 0)
    ent_ID.insert(0,"Username")
    def clear1_1(event):
        if ent_ID.get() == "Username":
            ent_ID.delete(0, len(ent_ID.get()))
    def clear1_2(event):
        if ent_ID.get() == "":
            ent_ID.insert(0,"Username")
    ent_ID.bind("<FocusIn>", clear1_1)
    ent_ID.bind("<FocusOut>", clear1_2)
    ent_ID.place(x = 650, y = 195)


    # PW 입력부
    ent_PW = Entry(login_win, font=("Arial", "15"), width = 22, bg = 'white', border = 0)
    ent_PW.insert(0,"Password")
    def clear2_1(event):
        if ent_PW.get() == "Password":
            ent_PW.delete(0, len(ent_PW.get()))
    def clear2_2(event):
        if ent_PW.get() == "":
            ent_PW.config(show = "")
            ent_PW.insert(0,"Password")
    def clear2_3(event):
        ent_PW.config(show = "*")
    ent_PW.bind("<FocusIn>", clear2_1)
    ent_PW.bind("<FocusOut>", clear2_2)
    ent_PW.bind("<Key>", clear2_3)
    ent_PW.place(x = 650, y = 265)

    # 로그인 오류 메시지
    login_error_message = Label(login_win, font = ("Arial", "10"), background = "#E0E0E0", fg = "red")
    # 내부 함수 1. login: 입력값이 DB에 없으면 메세지 띄우기
    def login():
        user_ID = ent_ID.get()
        user_PW = ent_PW.get()

        # 데이터베이스를 이용해 로그인 확인
        if db.log_in(user_ID, user_PW):

            db.cur.execute("SELECT COUNT(*) FROM HPE WHERE ID=? AND PW=?", (user_ID, user_PW))
            hpe_count = db.cur.fetchone()[0]

            if hpe_count == 0:
                config.flag_win = 3
                login_win.destroy()
            else:
                config.flag_win = 5
                login_win.destroy()
        else:
            login_error_message.config(text = "Please check your ID or password.")
    login_error_message.place(x = 655, y = 320)
    # 로그인 버튼
    image_path2 = resource_path("UI/img/login_bt.png")
    login_win.login_image = PhotoImage(file = image_path2,master=login_win)
    login_button = Button(login_win, image = login_win.login_image, border = 0, bg = "#E0E0E0")
    login_button.config(command=login)
    login_button.place(x = 635, y = 350)

    # 엔터키 설정
    login_win.bind("<Return>", lambda event: login())

    # 내부 함수 2. join: 가입 버튼을 누르면 회원가입 창으로 바꿈
    def join():
        config.flag_win = 2
        login_win.destroy()
    # 회원가입 버튼
    image_path3 = resource_path("UI/img/create_account_bt.png")
    login_win.join_image = PhotoImage(file = image_path3,master=login_win)
    join_button = Button(login_win, image = login_win.join_image, border = 0, bg = "#E0E0E0")
    join_button.config(command=join)
    join_button.place(x = 635, y = 400)


    # 종료 키 및 창 루프 생성
    login_win.protocol("WM_DELETE_WINDOW", on_close)
    login_win.mainloop()



# 화면 2. 회원가입
def Join_Window(db):

    # 기본 창 설정
    join_win = Tk()
    join_win.geometry("466x600+400+80")
    join_win.resizable(width=0, height=0)
    join_win.title("HPE_Join")
    join_win.iconbitmap("UI/img/logo.ico")
    # 회원가입 창에 들어갈 배경경 이미지 설정
    image_path4 = resource_path("UI/img/join_bg.png")
    join_win.frame_photo = PhotoImage(file = image_path4,master=join_win)
    frame_label = Label(join_win, border = 0, image = join_win.frame_photo)
    frame_label.pack(fill = "both", expand = True)
    
    #창닫기 함수 정의
    def on_close():
        join_win.destroy()
        config.flag_win=0


    # Name 입력부
    ent_nickname = Entry(join_win, font=("맑은고딕", "15", "bold"), width = 23, bg = 'white', border = 0)
    ent_nickname.insert(0, "영어/한글/숫자 6자 이내")
    def clear1_1(event):
        if ent_nickname.get() == "영어/한글/숫자 6자 이내":
            ent_nickname.delete(0, len(ent_nickname.get()))
    def clear1_2(event):
        if ent_nickname.get() == "":
            ent_nickname.insert(0,"영어/한글/숫자 6자 이내")
    ent_nickname.bind("<FocusIn>", clear1_1)
    ent_nickname.bind("<FocusOut>", clear1_2)
    ent_nickname.place(x = 157, y = 163)


    # ID 입력부
    ent_ID = Entry(join_win, font=("맑은고딕", "15", "bold"), width = 23, bg = 'white', border = 0)
    ent_ID.insert(0, "영문+숫자 12자 이내")
    def clear2_1(event):
        if ent_ID.get() == "영문+숫자 12자 이내":
            ent_ID.delete(0, len(ent_ID.get()))
    def clear2_2(event):
        if ent_ID.get() == "":
            ent_ID.insert(0,"영문+숫자 12자 이내")
    ent_ID.bind("<FocusIn>", clear2_1)
    ent_ID.bind("<FocusOut>", clear2_2)
    ent_ID.place(x = 157, y = 239)


    # PW 입력부
    ent_PW = Entry(join_win, font=("맑은고딕", "15", "bold"), width = 23, bg = 'white', border = 0)
    ent_PW.insert(0, "영문,숫자,문자 12자 이내")
    def clear3_1(event):
        if ent_PW.get() == "영문,숫자,문자 12자 이내":
            ent_PW.delete(0, len(ent_PW.get()))
    def clear3_2(event):
        if ent_PW.get() == "":
            ent_PW.config(show = "")
            ent_PW.insert(0,"영문,숫자,문자 12자 이내")
    def clear3_3(event):
        ent_PW.config(show = "*")
    ent_PW.bind("<FocusIn>", clear3_1)
    ent_PW.bind("<FocusOut>", clear3_2)
    ent_PW.bind("<Key>", clear3_3)
    ent_PW.place(x = 157, y = 315)


    # PW check 입력부
    ent_PW_check = Entry(join_win, font=("맑은고딕", "15", "bold"), width = 23, bg = 'white', border = 0)
    ent_PW_check.config(show = "*")
    ent_PW_check.place(x = 157, y = 391)


    # 오류 메시지 및 데이터베이스
    join_error_message = Label(join_win, font = ("Arial", "10"), background = "#B0C6E1", fg = "red")
    # 내부 함수 1. click: 입력된 두 PW가 다르면 오류, 조건에 맞으면 DB에 저장
    def click():
        input_name = ent_nickname.get()
        input_ID = ent_ID.get()
        input_Password = ent_PW.get()
        check_Password = ent_PW_check.get()

        result = db.sign_up(input_ID, input_Password, input_name)

        if (len(input_name) == 0 or len(input_ID) == 0 or len(input_Password) == 0 or len(check_Password) == 0):  # 입력하지 않은 경우
            join_error_message.config(text = "    Please enter your information.   ")
        elif (input_Password != check_Password):                                        # PW와 PW check이 다른 경우
            join_error_message.config(text = "     Please check your password.     ")
        elif (result == False):               # DB에 이미 정보가 존재하는 경우
            join_error_message.config(text = "ID, PW already exist or are incorrect")
        else:
            config.flag_win = 1
            join_win.destroy()
    join_error_message.place(x = 125, y = 445)
    
    # 다음 버튼
    image_path5 = resource_path("UI/img/next_bt.png")
    join_win.next_image = PhotoImage(file = image_path5,master=join_win)
    next_button = Button(join_win, image = join_win.next_image, border = 0, bg = "#CBDAEC")
    next_button.config(command=click)
    next_button.place(x = 150, y = 480)

    # 엔터키 설정
    join_win.bind("<Return>", lambda event: click())

    # 종료 키 설정 및 창 루프 생성
    join_win.protocol("WM_DELETE_WINDOW", on_close)
    join_win.mainloop()



# 화면 3. 신체 정보 등록
def RegiPose_Window(db):

    # 기본 창 설정
    regi_win = Tk()
    regi_win.overrideredirect(True)
    regi_win.geometry("600x600+400+80")
    regi_win.resizable(width=0, height=0)
    regi_win.title("HPE_Register")
    regi_win.iconbitmap("UI/img/logo.ico")
    # 기본 창에 들어갈 전체 이미지 설정
    image_path6 = resource_path("UI/img/regi_bg.png")
    regi_win.frame_photo = PhotoImage(file = image_path6,master=regi_win)
    frame_label = Label(regi_win, border = 0, image = regi_win.frame_photo)
    frame_label.pack(fill = "both", expand = True)


    # 안내 메시지
    guide_lab = Label(regi_win, font=("맑은고딕", "12", "bold"), background="#E5EDF5")
    guide_lab.config(text="사용 전 자세 등록을 해야합니다. START 버튼을 눌러주세요", fg = "red")
    guide_lab.place(x = 82, y = 72)


    # 등록 완료 버튼 선언만
    image_path7 = resource_path("UI/img/register_bt.png")
    regi_win.register_image = PhotoImage(file = image_path7,master=regi_win)
    register_button = Button(regi_win, image = regi_win.register_image, border = 0, bg = "#CBDAEC")
    
    # 재등록 버튼 선언만
    regi_win.restart_image = PhotoImage(file = "UI/img/restart_bt.png",master=regi_win)
    restart_button = Button(regi_win, image = regi_win.restart_image, border = 0, bg = "#CBDAEC")

    # 등록 시작 버튼 선언만
    image_path8=resource_path("UI/img/start_bt.png")
    regi_win.start_image = PhotoImage(file = image_path8,master=regi_win)
    start_button = Button(regi_win, image = regi_win.start_image, border = 0, bg = "#CBDAEC")
    start_button.place(x = 205, y = 510)

    # 카메라 프레임 설정
    frm = Frame(regi_win, width = 520, height = 416)
    frm.place(x = 39, y = 115)
    lbl_video1 = Label(frm)
    lbl_video1.pack()
    
    # mediapipe & camera 켜기
    cap = cv2.VideoCapture(0)
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    
    #창닫기 함수
    def on_close():
        if cap.isOpened():
            cap.release()  # 카메라 리소스 해제
        regi_win.destroy()
        config.flag_win=0

    # 이후 판단을 위해 초깃값 생성
    Initial_last_time = time.time()
    Initial_cnt = 0

    def video_play():

        if config.count_time == 1:
            config.last_time = Initial_last_time
            config.cnt = Initial_cnt
            config.count_time += 1

        success, image = cap.read()
        if not success:
            print("카메라 없음")
            return
        

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        image = cv2.resize(image, (520, 360))

        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            results = pose.process(image)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
                )
        
        current_time = time.time()
        if current_time - config.last_time >= 1.0:

            # [[틀린 기준 판단]] HPE를 성공한다면 출력 - README 파일의 키포인트 넘버 확인
            if results.pose_landmarks:
                # left shoulder (index 11), right shoulder (index 12)
                # 단일 키 포인트
                left_shoulder = results.pose_landmarks.landmark[11]
                right_shoulder = results.pose_landmarks.landmark[12]
                left_mouth = results.pose_landmarks.landmark[9]
                right_mouth = results.pose_landmarks.landmark[10]
                left_ankle = results.pose_landmarks.landmark[28]
                right_ankle = results.pose_landmarks.landmark[29]

                # angle_shoulder 
                config.keyPoint_list[0] = abs(math.degrees(math.atan(right_shoulder.y - left_shoulder.y)/(right_shoulder.x - left_shoulder.x)))
                
                # center_shoulder_dist 
                config.keyPoint_list[1] = (left_shoulder.z + right_shoulder.z)/2
                
                # center_mouth_dist 
                config.keyPoint_list[2] = (left_mouth.z + right_mouth.z)/2
                
                # left_hand_distance 
                config.keyPoint_list[3] = math.sqrt(10*(left_mouth.x - left_ankle.x)**2 + (left_mouth.y - left_ankle.y)**2 + 10*(left_mouth.z - left_ankle.z)**2)
                
                # right_hand_distance 
                config.keyPoint_list[4] = math.sqrt(10*(right_mouth.x - right_ankle.x)**2 + (right_mouth.y - right_ankle.y)**2 + 10*(right_mouth.z - right_ankle.z)**2)
                
                i=0

                # 자세 등록
                # 매 초마다 keyPoint_list를 pose_list에 저장(~cnt 9까지), cnt가 10이 되면 기존에 저장해온 값을 평균내서 출력  
                config.pose_list = config.save_pose(config.cnt, config.keyPoint_list, config.pose_list, i)
                
                def click():
                    config.count_time = 1
                    config.last_time = 0
                    config.cnt = 0
                    db.insert_hpe_data(config.pose_list[0], config.pose_list[1], config.pose_list[2])
                    config.complete = 0
                    config.cnt_start = 0
                    config.flag_win = 4
                    regi_win.destroy()
                    
                    

                def start_reclick():
                    for j in range(5):      # 자세를 등록한 후 자세 정보 리스트 초기화
                        config.pose_list[j] = 0.0
                    config.cnt = 0
                    config.complete = 0
                    config.cnt_start = 1
                    guide_lab.config(text="카메라를 10초간 응시하세요. 사용자 자세 등록을 실행 중 입니다.", fg = "red")
                    guide_lab.place(x = 75, y = 72)
                    start_button.place_forget()

                start_button.config(command=start_reclick)
                

                if config.cnt_start:
                    # 확인용 출력 코드(이후 삭제 필요)                
                    if config.cnt > 9: 
                        guide_lab.config(text = "Restart 버튼을 눌러 재등록하거나 Register 버튼을 눌러 다음창으로 넘어가세요.", fg = "green")
                        guide_lab.place(x = 15, y = 72)

                        print(config.cnt)
                        for j in range(5):      # 자세를 등록한 후 자세 정보 리스트 초기화
                            print(config.pose_list[j])
                        config.complete = 1            # UI팀에게 넘겨줄 flag

                    def reclick():
                        for j in range(5):      # 자세를 등록한 후 자세 정보 리스트 초기화
                            config.pose_list[j] = 0.0
                        config.cnt = 0
                        config.complete = 0
                        config.cnt_start = 1
                        guide_lab.config(text="카메라를 10초간 응시하세요. 사용자 자세 등록을 실행 중 입니다.", fg = "red")
                        guide_lab.place(x = 65, y = 72)
                        register_button.place_forget()

                    if config.complete == 1:
                        restart_button.config(command=reclick)
                        restart_button.place(x = 205, y = 485)
                        
                        register_button.config(command=click)
                        register_button.place(x = 205, y = 540)
                        
                    config.cnt += 1

            else:
               # 화면에 keyPoint가 생성되지 않을 경우
               print("화면에 자세가 보이도록 앉아주세요.")

            # 마지막 출력 시간 갱신
            config.last_time = current_time

        #바다오 이미지 객체 변환 및 재생 
        img = Image.fromarray(image)
        imgtk = ImageTk.PhotoImage(image=img)         
        video_frames[0]=imgtk
        
        lbl_video1.configure(image=imgtk)
        lbl_video1.imgtk = imgtk
        lbl_video1.after(10, video_play)

    video_play()
    
    # 종료 키 설정 및 창 루프 생성
    regi_win.bind("<Shift-X>", on_close)
    regi_win.protocol("WM_DELETE_WINDOW", on_close)
    regi_win.mainloop()




# 화면 4. 손 정보 등록
def RegiHand_Window(db):

   # 기본 창 설정
    hand_win = Tk()
    hand_win.overrideredirect(True)
    hand_win.geometry("600x600+400+80")
    hand_win.resizable(width=0, height=0)
    hand_win.title("HPE_Hand_Register")
    hand_win.iconbitmap("UI/img/logo.ico")
    
    # 등록 창에 들어갈 배경 이미지 설정
    image_path9 = resource_path("UI/img/regi_bg.png")
    hand_win.frame_photo = PhotoImage(file = image_path9,master=hand_win)
    frame_label = Label(hand_win, border = 0, image = hand_win.frame_photo)
    frame_label.pack(fill = "both", expand = True)


    # 안내 메시지
    guide_lab = Label(hand_win, font=("맑은고딕", "12", "bold"), background="#E5EDF5")
    guide_lab.config(text="손 등록을 해야합니다. 손을 들고 START 버튼을 눌러주세요", fg = "red")
    guide_lab.place(x = 82, y = 72)


    # 등록 완료 버튼 선언만
    image_path10 = resource_path("UI/img/register_bt.png")
    hand_win.register_image = PhotoImage(file = image_path10,master=hand_win)
    register_button = Button(hand_win, image = hand_win.register_image, border = 0, bg = "#CBDAEC")
    
    # 재등록 버튼 선언만
    image_path11 = resource_path("UI/img/restart_bt.png")
    hand_win.restart_image = PhotoImage(file = image_path11,master=hand_win)
    restart_button = Button(hand_win, image = hand_win.restart_image, border = 0, bg = "#CBDAEC")

    # 등록 시작 버튼 선언만
    image_path12 = resource_path("UI/img/start_bt.png")
    hand_win.start_image = PhotoImage(file = image_path12,master=hand_win)
    start_button = Button(hand_win, image = hand_win.start_image, border = 0, bg = "#CBDAEC")
    start_button.place(x = 205, y = 510)

    # 카메라 프레임 설정
    frm = Frame(hand_win, width = 520, height = 416)
    frm.place(x = 39, y = 115)
    lbl_video2 = Label(frm)
    lbl_video2.pack()
    
    # mediapipe & camera 켜기
    cap = cv2.VideoCapture(0)
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    
    #창닫기 함수
    def on_close():
        if cap.isOpened():
            cap.release()  # 카메라 리소스 해제
        hand_win.destroy()
        config.flag_win=0

    # 이후 판단을 위해 초깃값 생성
    Initial_last_time = time.time()
    Initial_cnt = 0

    def video_play():

        if config.count_time == 1:
            config.last_time = Initial_last_time
            config.cnt = Initial_cnt
            config.count_time += 1

        success, image = cap.read()
        if not success:
            print("카메라 없음")
            return
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        image = cv2.resize(image, (520, 360))

        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            results = pose.process(image)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
                )
        
        current_time = time.time()
        if current_time - config.last_time >= 1.0:

            # [[틀린 기준 판단]] HPE를 성공한다면 출력 - README 파일의 키포인트 넘버 확인
            if results.pose_landmarks:
                # left shoulder (index 11), right shoulder (index 12)
                # 단일 키 포인트
                left_shoulder = results.pose_landmarks.landmark[11]
                right_shoulder = results.pose_landmarks.landmark[12]
                left_mouth = results.pose_landmarks.landmark[9]
                right_mouth = results.pose_landmarks.landmark[10]
                left_ankle = results.pose_landmarks.landmark[28]
                right_ankle = results.pose_landmarks.landmark[29]

                # angle_shoulder 
                config.keyPoint_list[0] = abs(math.degrees(math.atan(right_shoulder.y - left_shoulder.y)/(right_shoulder.x - left_shoulder.x)))
                
                # center_shoulder_dist 
                config.keyPoint_list[1] = (left_shoulder.z + right_shoulder.z)/2
                
                # center_mouth_dist 
                config.keyPoint_list[2] = (left_mouth.z + right_mouth.z)/2
                
                # left_hand_distance 
                config.keyPoint_list[3] = math.sqrt(10*(left_mouth.x - left_ankle.x)**2 + (left_mouth.y - left_ankle.y)**2 + 10*(left_mouth.z - left_ankle.z)**2)
                
                # right_hand_distance 
                config.keyPoint_list[4] = math.sqrt(10*(right_mouth.x - right_ankle.x)**2 + (right_mouth.y - right_ankle.y)**2 + 10*(right_mouth.z - right_ankle.z)**2)
                
                i=0

                # 자세 등록
                # 매 초마다 keyPoint_list를 pose_list에 저장(~cnt 9까지), cnt가 10이 되면 기존에 저장해온 값을 평균내서 출력  
                config.pose_list = config.save_pose(config.cnt, config.keyPoint_list, config.pose_list, i)
                
                def click():
                    config.count_time = 1
                    config.last_time = 0
                    config.cnt = 0
                    db.insert_hpe_hands_data(config.pose_list[3], config.pose_list[4])
                    config.complete = 0
                    config.cnt_start = 0
                    config.flag_win = 5
                    hand_win.destroy()

                def start_reclick():
                    for j in range(5):      # 자세를 등록한 후 자세 정보 리스트 초기화
                        config.pose_list[j] = 0.0
                    config.cnt = 0
                    config.complete = 0
                    config.cnt_start = 1
                    guide_lab.config(text="10초간 손을 들고 있으세요. 손 정보 등록을 실행 중 입니다.", fg = "red")
                    guide_lab.place(x = 95, y = 72)
                    start_button.place_forget()

                start_button.config(command=start_reclick)
                

                if config.cnt_start:
                    # 확인용 출력 코드(이후 삭제 필요)                
                    if config.cnt > 9: 
                        guide_lab.config(text = "Restart 버튼을 눌러 재등록하거나 Register 버튼을 눌러 등록을 완료하세요.", fg = "green")
                        guide_lab.place(x = 30, y = 72)

                        print(config.cnt)
                        for j in range(5):      # 자세를 등록한 후 자세 정보 리스트 초기화
                            print(config.pose_list[j])
                        config.complete = 1            # UI팀에게 넘겨줄 flag

                    def reclick():
                        for j in range(5):      # 자세를 등록한 후 자세 정보 리스트 초기화
                            config.pose_list[j] = 0.0
                        config.cnt = 0
                        config.complete = 0
                        config.cnt_start = 1
                        guide_lab.config(text="10초간 손을 들고 있으세요. 손 정보 등록을 실행 중 입니다.", fg = "red")
                        guide_lab.place(x = 95, y = 72)
                        register_button.place_forget()

                    if config.complete == 1:
                        restart_button.config(command=reclick)
                        restart_button.place(x = 205, y = 485)
                        
                        register_button.config(command=click)
                        register_button.place(x = 205, y = 540)
                        
                    config.cnt += 1
                    
            else:
               # 화면에 keyPoint가 생성되지 않을 경우
               print("화면에 자세가 보이도록 앉아주세요.")

            # 마지막 출력 시간 갱신
            config.last_time = current_time

        #비디오 객체 저장 및 재생
        img = Image.fromarray(image)
        imgtk = ImageTk.PhotoImage(image=img)
        video_frames[0]=imgtk
        lbl_video2.configure(image=imgtk)
        lbl_video2.imgtk = imgtk
        lbl_video2.after(10, video_play)

    video_play()
    
  

    # 종료 키 설정 및 창 루프 생성
    hand_win.bind("<Shift-X>", on_close)
    hand_win.protocol("WM_DELETE_WINDOW", on_close)
    hand_win.mainloop()


# 화면 5. 메인 window
def Main_Window(db):
    
    # 백그라운드 화면
    def on_minimize(event=None):
        main_win.withdraw()
        # 메인 윈도우가 최소화될 때 새로운 창 생성 및 활성화
        mini_win_activate()

    def mini_win_activate(event=None):
        new_win = Toplevel()  # 새 창을 Toplevel로 생성
        new_win.overrideredirect(True)
        new_win.config(background="azure")

        def slide(_):
            new_win.attributes('-alpha', slide_bar.get())
            slide_label.config(text=str(round(slide_bar.get(), 2)))
        def destroy_win():
            new_win.destroy()
            main_win.deiconify()
        style = ttk.Style()
        style.configure("TScale", background="azure")  # 슬라이더 배경색 변경

        global close
        close = PhotoImage(file="UI/img/close.png",master=new_win)
        btn=Button(new_win, image=close, border=0, bg = "azure")
        btn.config(command=destroy_win)
        btn.place(x=228,y=0)
        slide_label = Label(new_win, text="투명도 설정",background="azure")
        slide_label.pack(side="bottom")
        slide_bar = ttk.Scale(new_win, from_=0.1, to=1.0, value=1, orient=HORIZONTAL, command=slide, length=200,style="TScale")
        slide_bar.pack(side="bottom",pady=2)

        # 새 창의 크기 설정
        win_width = 250
        win_height = 150

        # 화면의 너비와 높이 가져오기
        screen_width = new_win.winfo_screenwidth()
        screen_height = new_win.winfo_screenheight()

        # 창을 화면의 우측 하단에 배치
        x_pos = screen_width - win_width - 10  # 10px 여백 추가
        y_pos = screen_height - win_height - 80  # 작업 표시줄 여백 고려

        new_win.geometry(f"{win_width}x{win_height}+{x_pos}+{y_pos}")
        new_win.attributes('-topmost', True)
        new_win.attributes('-alpha', 1)

        # 이미지 설정
        image_path13 = resource_path("UI/img/spine1.png")
        new_win.mini1_1 = PhotoImage(file=image_path13, master=new_win)
        image_path14 = resource_path("UI/img/spine2.png")
        new_win.mini1_2 = PhotoImage(file=image_path14, master=new_win)
        image_path15 = resource_path("UI/img/spine3.png")
        new_win.mini1_3 = PhotoImage(file=image_path15, master=new_win)
        image_path16 = resource_path("UI/img/neck1.png")
        new_win.mini2_1 = PhotoImage(file=image_path16, master=new_win)
        image_path17 = resource_path("UI/img/neck2.png")
        new_win.mini2_2 = PhotoImage(file=image_path17, master=new_win)
        image_path18 = resource_path("UI/img/neck3.png")
        new_win.mini2_3 = PhotoImage(file=image_path18, master=new_win)
        image_path19 = resource_path("UI/img/chin1.png")
        new_win.mini3_1 = PhotoImage(file=image_path19, master=new_win)
        image_path20 = resource_path("UI/img/chin2.png")
        new_win.mini3_2 = PhotoImage(file=image_path20, master=new_win)
        image_path21 = resource_path("UI/img/bright1.png")
        new_win.mini4_1 = PhotoImage(file=image_path21, master=new_win)
        image_path22 = resource_path("UI/img/bright2.png")
        new_win.mini4_2 = PhotoImage(file=image_path22, master=new_win)

        lab_img1 = Label(new_win)
        lab_img1.config(image=new_win.mini1_1, background="azure")
        lab_img1.place(x=10,y=45)
        lab_img2 = Label(new_win)
        lab_img2.config(image=new_win.mini2_1, background="azure")
        lab_img2.place(x=70,y=45)
        lab_img3 = Label(new_win)
        lab_img3.config(image=new_win.mini3_1, background="azure")
        lab_img3.place(x=130,y=45)
        lab_img4 = Label(new_win)
        lab_img4.config(image=new_win.mini4_1, background="azure")
        lab_img4.place(x=190,y=45)
        lab_alarm = Label(new_win, font = ("맑은고딕", "15", "bold"), background= "azure")
        lab_alarm.place(x=70, y=8)
        def update_new_win():
            # 어깨 판단
            if config.outputList[0] == 1:
                lab_img1.config(image=new_win.mini1_2, background="azure")
            elif config.outputList[0] == 2:
                lab_img1.config(image=new_win.mini1_3, background="azure")
            else:
                lab_img1.config(image=new_win.mini1_1, background="azure")

            # 거북목 판단
            if config.outputList[1] == 1:
                lab_img2.config(image=new_win.mini2_2, background="azure")
            elif config.outputList[1] == 2:
                lab_img2.config(image=new_win.mini2_3, background="azure")
            else:
                lab_img2.config(image=new_win.mini2_1, background="azure")

            # 턱괴기 판단
            if config.outputList[2] == 1:
                lab_img3.config(image=new_win.mini3_2, background="azure")
            else:
                lab_img3.config(image=new_win.mini3_1, background="azure")

            # 환경 밝기 판단
            if config.outputList[3] == 1:
                lab_img4.config(image=new_win.mini4_2, background="azure")
            else:
                lab_img4.config(image=new_win.mini4_1, background="azure")
            
            # 자리비움 판단
            if config.disappear == 1:
                lab_alarm.config(text = "<자리 비움>", fg = "black")
            else:
                lab_alarm.config(text = "", fg = "black")


            # 500ms 후에 다시 업데이트
            new_win.after(50, update_new_win)

        # 창이 생성될 때 업데이트 시작
        update_new_win()

    # 등록된 자세 정보 조회
    list_from_DB = db.fetch_hpe_data()
    hpe_data_DB = list_from_DB[0]

    # 기본 창 설정
    main_win = Tk()
    main_win.geometry("1280x720+10+10")
    main_win.resizable(width=0, height=0)
    main_win.title("Duhoi And Jeungjae")
    main_win.iconbitmap("UI/img/logo.ico")
    # 메인 창에 들어갈 배경 이미지 설정
    image_path23 = resource_path("UI/img/main_bg.png")
    main_win.frame_photo = PhotoImage(file = image_path23,master=main_win)
    frame_label = Label(main_win, border = 0, image = main_win.frame_photo)
    frame_label.pack(fill = "both", expand = True)

    # 백그라운드 화면 조건
    main_win.bind("<Unmap>", lambda event: on_minimize() if main_win.state() == "iconic" else None)

    # 알림 메시지
    frame_alarm = Frame(main_win, bg = "white", width=750, height=50)
    frame_alarm.place(x=480, y=53)
    lbl_alarm = Label(frame_alarm, font = ("맑은고딕", "20", "bold"), background= "white")
    user_name = db.get_name()    # db에서 이름 가져오기
    lbl_alarm.config(text = (user_name+ "  |  최근 알림: 알림 없음"), fg = "black")
    lbl_alarm.place(x=10, y=7)


    # 카메라 프레임 설정
    frm = Frame(main_win, width = 650, height = 520)
    frm.place(x = 39, y = 145)
    lbl_video3 = Label(frm)
    lbl_video3.pack()
    # videocapture 객체를 통해 동영상 재생
    cap = cv2.VideoCapture(0)
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose
    
    #창닫기 함수 정의
    def on_close():
        if cap.isOpened():
            cap.release()  # 카메라 리소스 해제
        main_win.destroy()
        config.flag_win=0


    # 체크박스 변수와 버튼을 정의
    CheckVar1 = IntVar()
    c1 = Checkbutton(main_win, text="Visualization", variable=CheckVar1, bg="#C2D6E9", font=("Arial", "15", "bold"))
    c1.place(x=545, y=670)


    # 이후 판단을 위해 초깃값 생성
    Initial_cnt = 0
    Initial_last_time = time.time()

    # 알림 이미지 기본값
    # 어깨
    image_path24 = resource_path("UI/img/scoliosis_good.png")
    main_win.img1_1 = PhotoImage(file=image_path24, master=main_win)      # 0단계(good)
    image_path25 = resource_path("UI/img/scoliosis_caution.png")
    main_win.img1_2 = PhotoImage(file=image_path25, master=main_win)    # 1단계
    image_path26 = resource_path("UI/img/scoliosis_warning.png")
    main_win.img1_3 = PhotoImage(file=image_path26, master=main_win)    # 2단계(bad)
    main_win.img1_1 = main_win.img1_1.subsample(7)
    main_win.img1_2 = main_win.img1_2.subsample(7)
    main_win.img1_3 = main_win.img1_3.subsample(7)
    lbl_img1 = Label(main_win)
    lbl_img1.config(image=main_win.img1_1, background = "#CBDAEC", border=0)
    lbl_img1.place(x=750, y=170)

    # 거북목
    image_path27 = resource_path("UI/img/forward_head_good.png")
    main_win.img2_1 = PhotoImage(file=image_path27, master=main_win)
    image_path28 = resource_path("UI/img/forward_head_caution.png")
    main_win.img2_2 = PhotoImage(file=image_path28, master=main_win)
    image_path29 = resource_path("UI/img/forward_head_warning.png")
    main_win.img2_3 = PhotoImage(file=image_path29, master=main_win)
    main_win.img2_1 = main_win.img2_1.subsample(7)
    main_win.img2_2 = main_win.img2_2.subsample(7)
    main_win.img2_3 = main_win.img2_3.subsample(7)
    lbl_img2 = Label(main_win)
    lbl_img2.config(image=main_win.img2_1, background = "#CBDAEC", border=0)
    lbl_img2.place(x=1000, y=170)

    # 턱괴기
    image_path30 = resource_path("UI/img/chin_hold_good.png")
    main_win.img3_1 = PhotoImage(file=image_path30, master=main_win)
    
    image_path31 = resource_path("UI/img/chin_hold_warning.png")
    main_win.img3_2 = PhotoImage(file=image_path31, master=main_win)
    
    main_win.img3_1 = main_win.img3_1.subsample(7)
    main_win.img3_2 = main_win.img3_2.subsample(7)
    
    lbl_img3 = Label(main_win)
    lbl_img3.config(image=main_win.img3_1, background = "#B0C6E1", border=0)
    lbl_img3.place(x=750, y=420)

    # 환경 밝기
    image_path32 = resource_path("UI/img/brightness_good.png")
    main_win.img4_1 = PhotoImage(file=image_path32, master=main_win)
    image_path33 = resource_path("UI/img/brightness_warning.png")
    main_win.img4_2 = PhotoImage(file=image_path33, master=main_win)
    main_win.img4_1 = main_win.img4_1.subsample(7)
    main_win.img4_2 = main_win.img4_2.subsample(7)
    lbl_img4 = Label(main_win)
    lbl_img4.config(image=main_win.img4_1, background = "#B0C6E1", border=0)
    lbl_img4.place(x=1000, y=420)

    # 내부 함수 2. join: 가입 버튼을 누르면 회원가입 창으로 바꿈
    def logout():
        config.flag_win = 1
        config.count_time = 1
        config.disappear = 0
        config.last_time = 0
        config.cnt = 0
        config.complete = 0
        main_win.destroy()

    # 로그아웃 버튼
    image_path34 = resource_path("UI/img/logout_bt.png")
    main_win.logout_image = PhotoImage(file = image_path34,master=main_win)
    logout_button = Button(main_win, image = main_win.logout_image, border = 0, bg = "#C2D6E9")
    logout_button.config(command=logout)
    logout_button.place(x = 1240, y = 680)


    #내부 함수: 자세 및 손 재등록 하기 위한 함수
    def go_to_regi():
        # 전역함수 초기화
        config.flag_win = 3
        config.count_time = 1
        config.disappear = 0
        config.last_time = 0
        config.cnt = 0
        config.complete = 0
        config.cnt_start = 0
        # 기존 DB 정보들 지우기
        db.delete_hpe_data()
        main_win.destroy() 

    # 재등록 버튼
    image_path35 = resource_path("UI/img/go_to_regi.png")
    main_win.go_to_regi_image = PhotoImage(file = image_path35,master=main_win)
    go_to_regi_button = Button(main_win, image = main_win.go_to_regi_image, border = 0, bg = "#C2D6E9")
    go_to_regi_button.config(command=go_to_regi)
    go_to_regi_button.place(x = 1200, y = 680)


    # 자리비움 버튼
    image_path36 = resource_path("UI/img/disappear_bt.png")
    main_win.disappear_image = PhotoImage(file = image_path36,master=main_win)
    disappear_button = Button(main_win, image = main_win.disappear_image, border = 0, bg = "#C2D6E9")
    disappear_button.place(x = 1160, y = 680) 

    # 영상 재생 및 판단하여 알리는 함수
    def video_play():
        if config.count_time == 1:
            config.last_time = Initial_last_time
            config.cnt = Initial_cnt
            config.count_time += 1

        # 1초마다 좌표를 출력하기 위해 시간 저장 변수 설정
        success, image = cap.read()
        if not success:
            print("카메라 없음")
            return

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        image = cv2.resize(image, (650, 520))

        # 그레이스케일로 변환
        config.gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)        

        # 밝기 측정 (평균 계산)
        config.brightness.data = config.gray.mean()


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
        if current_time - config.last_time >= 1.0:
            # [[틀린 기준 판단]] HPE를 성공한다면 출력 - README 파일의 키포인트 넘버 확인
            if results.pose_landmarks:
                config.cnt = 0 # 사람이 자리에 있다는 것이므로 자리비움 카운트 초기화
                config.disappear = 0

                # DB에 등록된 자세 판단 기준
                center_mouth_dist_DB = hpe_data_DB[2]
                hand_distance_DB = min(hpe_data_DB[3], hpe_data_DB[4])

                # 단일 키 포인트
                left_shoulder = results.pose_landmarks.landmark[11]
                right_shoulder = results.pose_landmarks.landmark[12]
                left_mouth = results.pose_landmarks.landmark[9]
                right_mouth = results.pose_landmarks.landmark[10]
                left_ankle = results.pose_landmarks.landmark[28]
                right_ankle = results.pose_landmarks.landmark[29]

               # 합성 키 포인트
                angle_shoulder = abs(math.degrees(math.atan(right_shoulder.y - left_shoulder.y)/(right_shoulder.x - left_shoulder.x)))
                center_mouth_dist = (left_mouth.z + right_mouth.z)/2
                left_hand_distance = math.sqrt((left_mouth.x - left_ankle.x)**2 + (left_mouth.y - left_ankle.y)**2 + 10*(left_mouth.z - left_ankle.z)**2)
                right_hand_distance = math.sqrt(10*(right_mouth.x - right_ankle.x)**2 + (right_mouth.y - right_ankle.y)**2 ) #+ 10*(right_mouth.z - right_ankle.z)**2
                
                config.angle_waist.data = angle_shoulder
                config.turttle_neck.data = center_mouth_dist

                if 10000*left_ankle.visibility >= 0.1 and 10000*right_ankle.visibility >= 0.1:
                    config.hands.data = min(left_hand_distance, right_hand_distance)
                elif 10000*left_ankle.visibility >= 0.1 and 10000*right_ankle.visibility < 0.1:
                    config.hands.data = left_hand_distance
                elif 10000*left_ankle.visibility < 0.1 and 10000*right_ankle.visibility >= 0.1:
                    config.hands.data = right_hand_distance
                else:
                    config.hands.data = hand_distance_DB
                             
                
                config.outputList = config.result_pose(config.estimation_pose(center_mouth_dist_DB ,hand_distance_DB))   # 파라미터에 center_mouth_dist랑 hand_distance 보내야함!

                # 어깨 판단 
                if config.outputList[0] == 1:
                    lbl_img1.config(image=main_win.img1_2, background = "#CBDAEC", border=0)
                elif config.outputList[0] == 2:
                    lbl_img1.config(image=main_win.img1_3, background = "#CBDAEC", border=0)
                else:
                    lbl_img1.config(image=main_win.img1_1, background = "#CBDAEC", border=0)

                # 거북목 판단
                if config.outputList[1] == 1:
                    lbl_img2.config(image=main_win.img2_2, background = "#CBDAEC", border=0)
                elif config.outputList[1] == 2:
                    lbl_img2.config(image=main_win.img2_3, background = "#CBDAEC", border=0)
                else:
                    lbl_img2.config(image=main_win.img2_1, background = "#CBDAEC", border=0)

                # 턱괴기 판단
                if config.outputList[2] == 1:
                    lbl_img3.config(image=main_win.img3_2, background = "#B0C6E1", border=0)
                else:
                    lbl_img3.config(image=main_win.img3_1, background = "#B0C6E1", border=0)

                # 환경밝기 판단
                if config.outputList[3] == 1:
                    lbl_img4.config(image=main_win.img4_2, background = "#B0C6E1", border=0)
                else:
                    lbl_img4.config(image=main_win.img4_1, background = "#B0C6E1", border=0)

                # 메시지 변경
                if (config.outputList[0] != 0 or config.outputList[1] != 0 or config.outputList[2] != 0 or config.outputList[3] != 0): 
                    lbl_alarm.config(text = (user_name + "  |  최근 알림: 자세가 불량합니다. 고쳐주세요."), fg = "red")
                else:
                    lbl_alarm.config(text = (user_name + "  |  최근 알림: 자세 알림이 없습니다."), fg = "black")


                 # 디버깅용
                #print(10000*left_ankle.visibility)
                #print(10000*right_ankle.visibility)
                #print(config.hands.output)
                #print(config.estimation_pose())

                # for i in range(4):
                #     print(config.outputList[i])

                #print(f"cnt = {angle_waist.cnt:.4f}")
                #print(f"data = {angle_waist.data:.4f}")
                #print(f"output = {angle_waist.output:.4f}")    
            else: 
                config.cnt += 1
                if config.cnt > 10: # 확인 빠르게 하기 위해 10초로 설정, 추후에 1분으로 고치면 될 듯
                    config.disappear = 1
                else:
                    config.disappear = 0
                ####################################################
                
            print(config.cnt)
            if config.disappear == 1:
                lbl_alarm.config(text = (user_name + "  |  자리 비움"), fg = "black")


            # 마지막 출력 시간 갱신
            config.last_time = current_time
        disappear_button.config(command=on_minimize)

        #비디오 객체 저장 및 재생 
        img = Image.fromarray(image)
        imgtk = ImageTk.PhotoImage(image=img)   ##여기도 마찬가지
        video_frames[0]=imgtk
       
        lbl_video3.configure(image=imgtk)
        lbl_video3.imgtk = imgtk
        lbl_video3.after(10, video_play)

    video_play()


    # 종료 키 설정 및 창 루프 생성
    main_win.protocol("WM_DELETE_WINDOW", on_close)
    main_win.mainloop()

