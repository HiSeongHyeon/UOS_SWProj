import sys,os

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
     os.chdir(sys._MEIPASS)
     
#version 1 : image moving
# from tkinter import Tk, Label, PhotoImage

# def fade_in(new_img):
#     global alpha, lbl
#     alpha += 0.1
#     if alpha > 1:
#         alpha = 1
#         lbl.config(image=new_img)
#         return
#     # alpha를 적용한 이미지 설정
#     lbl.config(image=placeholder)  # 알파 블렌딩을 흉내냄
#     lbl.after(50, lambda: fade_in(new_img))  # 50ms 간격으로 업데이트

# # 초기 설정
# win = Tk()
# win.geometry("400x300")
# win.title("이미지 교체 애니메이션")

# # 이미지 로드
# img1 = PhotoImage(file="C:/Users/User/Desktop/김민섭 3학년/소공/GUI/kim.png")
# img2 = PhotoImage(file="C:/Users/User/Desktop/김민섭 3학년/소공/GUI/kim1.png")

# # 초기 이미지 설정
# lbl = Label(win, image=img1)
# lbl.pack()

# # 애니메이션 설정
# alpha = 0  # 투명도
# placeholder = img2  # 변경될 이미지

# # 버튼을 눌러 이미지 교체
# win.after(1000, lambda: fade_in(img2))  # 1초 후 이미지 전환
# win.mainloop()

#version 2 image fadeout
from tkinter import Tk, Label, Canvas
from PIL import Image, ImageTk

# Tkinter 윈도우 생성
win = Tk()
win.title("Image Fade Animation")
win.geometry("400x400")

# 캔버스 생성
canvas = Canvas(win, width=400, height=400)
canvas.pack()

# 이미지 로드 (Pillow 사용)
image1 = Image.open("kim.png").resize((400, 400))  # 첫 번째 이미지
image2 = Image.open("kim1.png").resize((400, 400))  # 두 번째 이미지

# 이미지 전환 함수
def fade_images(alpha=0):
    """alpha 값을 조정하여 이미지 페이드 효과를 만듭니다."""
    if alpha > 1:  # 애니메이션 종료 조건
        return
    
    # 첫 번째와 두 번째 이미지를 섞음
    blended = Image.blend(image1, image2, alpha)
    tk_image = ImageTk.PhotoImage(blended)
    canvas.create_image(200, 200, image=tk_image)
    canvas.image = tk_image  # 참조 유지
    
    # alpha 값을 점진적으로 증가시킴
    win.after(50, fade_images, alpha + 0.05)

# 버튼 클릭 시 애니메이션 시작
win.after(1000, fade_images)  # 1초 후 애니메이션 시작

win.mainloop()
