from DB.db import Database

# UI 모듈에서 사용하는 함수
from UI.interface import Login_Window
from UI.interface import Join_Window
from UI.interface import RegiPose_Window
from UI.interface import RegiHand_Window
from UI.interface import Main_Window


######## 에러 제거 위한 모듈###############
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

##################################

# HPE 모듈에서 사용하는 함수
# from HPE import HPE_test_ver2

# Database 객체 생성
db = Database()

# 2가지 Table 생성 (1) Database_data (2) HPE
db.create_tables()


while config.flag_win != 0:
    if (config.flag_win == 1):
        Login_Window(db)
    elif (config.flag_win == 2):
        Join_Window(db)
    elif (config.flag_win == 3):
        RegiPose_Window(db)
    elif (config.flag_win == 4):
        RegiHand_Window(db)
    elif (config.flag_win == 5):
        Main_Window(db)
    else:
        print("비정상적으로 프로그램 작동함.\n")
        config.flag_win = 0
        quit()



# UI 함수 호출 시 Database 객체 전달
# Login_Window(db)

# HPE 함수 호출 시 Database 객체 전달
# estimate_pose(db)

# 마지막으로 프로그램 종료 시 DB 연결 해제
db.close_connection()
