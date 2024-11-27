from DB.Database import Database

# UI 모듈에서 사용하는 함수
from UI.interface import Login_Window
from UI.interface import Join_Window
from UI.interface import RegiPose_Window
from UI.interface import Main_Window

import config

# HPE 모듈에서 사용하는 함수
# from HPE import HPE_test_ver2

# Database 객체 생성
db = Database()

# 2가지 Table 생성 (1) Database_data (2) HPE
db.create_tables()


while True:
    if (config.flag_win == 1):
        Login_Window(db)
    elif (config.flag_win == 2):
        Join_Window(db)
    elif (config.flag_win == 3):
        RegiPose_Window(db)
    elif (config.flag_win == 4):
        Main_Window(db)
    else:
        print("비정상적으로 프로그램 작동함.\n")
        quit()



# UI 함수 호출 시 Database 객체 전달
# Login_Window(db)

# HPE 함수 호출 시 Database 객체 전달
# estimate_pose(db)

# 마지막으로 프로그램 종료 시 DB 연결 해제
db.close_connection()


"""
from DB.Database import Database

# Database 객체 생성
db = Database()

# 1. 테이블 생성
db.create_table()

# 2. 데이터 삽입
friend_data = [
    ('김상욱', 22, '010-4545-6767', '서울특별시 종로구 세종대로 종로 1가'),
    ('최지훈', 20, '010-7896-1234', '전라북도 전주시 덕진구 석소로 77, 101동 101호(인후동1가, 대우아파트)'),
    ('Dr.Bae', 67, '010-8452-5678', '전라북도 전주시 덕진구 석소2길 21-1(우아동2가)'),
    ('강서혁', 27, '010-1414-6767', '경상남도 의령군 화정면 화정로 41-6'),
    ('유민규', 21, '010-6497-6497', '서울특별시 동작구 흑석한강로 2(흑석동)')
]
db.insert_data(friend_data)

# 3. 데이터 조회
print("=== 모든 데이터 조회 ===")
all_friends = db.fetch_all_data()
for friend in all_friends:
    print(friend)

# 4. 데이터 수정
print("\n=== 데이터 수정: 최지훈 번호 변경 ===")
db.update_data('최지훈', '010-1234-5678')
updated_friend = db.fetch_all_data()
for friend in updated_friend:
    print(friend)

# 5. 데이터 삭제
print("\n=== 데이터 삭제: Dr.Bae 삭제 ===")
db.delete_data('Dr.Bae')
remaining_friends = db.fetch_all_data()
for friend in remaining_friends:
    print(friend)

# 6. 연결 닫기
db.close_connection()

"""