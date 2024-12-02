# DB 모듈에서 사용하는 클래스
from DB.db import Database

# UI와 HPE 모듈에서 사용하는 함수
from UI.interface import login_window
from UI.interface import join_window
from UI.interface import regi_pose_window
from UI.interface import regi_hand_window
from UI.interface import main_window

# 에러 제거 위한 모듈
import sys
import config

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    class NullOutput(object):
        def write(self, string):
            pass

        def isatty(self):
            return False


    sys.stdout = NullOutput()
    sys.stderr = NullOutput()


# Database 객체 생성
db = Database()


# 2가지 Table 생성 (1) Database_data (2) HPE
db.create_tables()


# UI 켜기 및 판단 실행
while config.flag_win != 0:
    if (config.flag_win == 1):
        login_window(db)
    elif (config.flag_win == 2):
        join_window(db)
    elif (config.flag_win == 3):
        regi_pose_window(db)
    elif (config.flag_win == 4):
        regi_hand_window(db)
    elif (config.flag_win == 5):
        main_window(db)
    else:
        print("비정상적으로 프로그램 작동함.\n")
        config.flag_win = 0
        quit()


# 마지막으로 프로그램 종료 시 DB 연결 해제
db.close_connection()