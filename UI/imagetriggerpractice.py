import time
from tkinter import Tk, PhotoImage, Label

def temp_Window():
    # Tkinter 창 생성
    main_win = Tk()
    main_win.geometry("640x480+200+100")
    main_win.minsize(640, 480)
    main_win.resizable(width=0, height=0)
    main_win.title("temp_window_for_trigger")
    main_win.configure(bg='gray')
    main_win.option_add("*Font", "맑은고딕 20")

    # 이미지 로드 및 크기 조정
    img1 = PhotoImage(file="C:/Users/jihwa/Desktop/worksp/program/picture1.png", master=main_win)
    img1 = img1.subsample(5)
    img2 = PhotoImage(file="C:/Users/jihwa/Desktop/worksp/program/picture4.png", master=main_win)
    img2 = img2.subsample(5)

    # 이미지 라벨 설정
    lab_img = Label(main_win, background="gray")
    lab_img.pack()

    # 이미지 교체 함수 정의
    def switch_image():
        current_image = img1 if lab_img.cget("image") == str(img2) else img2
        lab_img.config(image=current_image)
        main_win.after(10000, switch_image)  # 10초 후 이미지 전환

    # 첫 이미지 설정 및 이미지 전환 시작
    lab_img.config(image=img1)
    main_win.after(10000, switch_image)

    # 창 닫기 버튼 설정
    main_win.protocol('WM_DELETE_WINDOW', quit)

    # Tkinter 메인 루프 시작
    main_win.mainloop()
    main_win.destroy()  # 창을 닫고 리소스를 해제

# 10초 간격으로 temp_Window() 실행
while True:
    temp_Window()
    time.sleep(10)
