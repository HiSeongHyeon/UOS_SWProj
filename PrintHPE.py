import cv2
import mediapipe as mp
import numpy as np
import time
import math
from DB.db import Database  # Database 클래스를 import

# Mediapipe 초기화
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# Database 초기화
db = Database()
db.create_tables()

# 사용자 SIGN UP 과정
user_id = "user1"
user_pw = "password123"
user_name = "Test User"
sign_up_success = db.sign_up(user_id, user_pw, user_name)  # 사용자 추가

if sign_up_success:
    print(f"Sign up successful for user: {user_id}")
else:
    print(f"User already exists: {user_id}")

# 로그인된 사용자 정보 설정
login_success = db.log_in(user_id, user_pw)
if login_success:
    print(f"Log in successful for user: {user_id}")
else:
    print(f"Log in failed for user: {user_id}")

# 자세 데이터 계산 함수
def average_pose(cnt, data, listData, i):
    if listData[i] is None:
        listData[i] = 0.0
        
    if cnt < 10:
        listData[i] = listData[i] + data
        return listData[i]
        
    else:
        average = listData[i] / 10
        listData[i] = 0.0    
        return average 

def save_pose(cnt, keyPoint_list, pose_list, i):
    if pose_list[i] is None:
        pose_list[i] = 0.0

    for i in range(5):
        pose_list[i] = average_pose(cnt, keyPoint_list[i], pose_list, i)
        
    return pose_list

# DB에 저장된 데이터 출력 함수
def print_saved_hpe_data():
    """
    데이터베이스에 저장된 HPE 데이터를 출력합니다.
    """
    print("\n=== Saved HPE Data in Database ===")
    saved_data = db.fetch_hpe_data()
    if saved_data:
        for index, data in enumerate(saved_data):
            print(f"Record {index + 1}: angle_shoulder={data[0]}, center_shoulder_dist={data[1]}, "
                  f"center_mouth_dist={data[2]}, left_hand_distance={data[3]}, right_hand_distance={data[4]}")
    else:
        print("No data found in the HPE table.")

# 초기 변수 설정
keyPoint_list = [0.0, 0.0, 0.0, 0.0, 0.0]   # 실시간 자세 정보
pose_list = [0.0, 0.0, 0.0, 0.0, 0.0]       # DB에 저장할 최종 자세 정보
cnt = 0

# 카메라 캡처 시작
cap = cv2.VideoCapture(0)

# 1초마다 좌표를 출력하기 위해 시간 저장 변수 설정
last_time = time.time()

with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("카메라를 찾을 수 없습니다.")
            continue

        # 성능 향상을 위해 이미지 작성 불가능 설정
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        # 포즈 주석을 이미지 위에 그리기
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        # 좌우 반전된 이미지 출력
        cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))

        # [[판단 시간 설정]] 1초마다 좌표 추출 및 출력
        current_time = time.time()
        if current_time - last_time >= 1.0:

            # [[틀린 기준 판단]] HPE를 성공한다면 출력 - README 파일의 키포인트 넘버 확인
            if results.pose_landmarks:
                # 주요 키포인트
                left_shoulder = results.pose_landmarks.landmark[11]
                right_shoulder = results.pose_landmarks.landmark[12]
                left_mouth = results.pose_landmarks.landmark[9]
                right_mouth = results.pose_landmarks.landmark[10]
                left_ankle = results.pose_landmarks.landmark[28]
                right_ankle = results.pose_landmarks.landmark[29]

                # keyPoint_list 업데이트
                keyPoint_list[0] = abs(math.degrees(math.atan(right_shoulder.y - left_shoulder.y) / (right_shoulder.x - left_shoulder.x)))
                keyPoint_list[1] = (left_shoulder.z + right_shoulder.z) / 2
                keyPoint_list[2] = (left_mouth.z + right_mouth.z) / 2
                keyPoint_list[3] = math.sqrt((left_mouth.x - left_ankle.x) ** 2 + (left_mouth.y - left_ankle.y) ** 2)
                keyPoint_list[4] = math.sqrt((right_mouth.x - right_ankle.x) ** 2 + (right_mouth.y - right_ankle.y) ** 2)

                # 자세 등록
                pose_list = save_pose(cnt, keyPoint_list, pose_list, 0)
                
                # 매 초마다 저장된 자세를 평균낸 후 DB에 삽입
                if cnt == 9: 
                    for j in range(5):
                        print(f"Pose {j + 1}: {pose_list[j]}")

                    # DB에 데이터 삽입
                    success = db.insert_hpe_data(
                        angle_shoulder=pose_list[0],
                        center_shoulder_dist=pose_list[1],
                        center_mouth_dist=pose_list[2],
                        left_hand_distance=pose_list[3],
                        right_hand_distance=pose_list[4]
                    )
                    
                    if success:
                        print("Pose data successfully inserted into the database!")
                    else:
                        print("Failed to insert pose data into the database.")

                    # 저장된 데이터 출력
                    print_saved_hpe_data()

                    cnt = 0  # 카운터 초기화

                cnt += 1
            else:
                # 화면에 keyPoint가 생성되지 않을 경우
                print("화면에 자세가 보이도록 앉아주세요.")

            # 마지막 출력 시간 갱신
            last_time = current_time

        # ESC 키를 누르면 종료
        if cv2.waitKey(5) & 0xFF == 27:
            break

# 자원 해제
cap.release()
cv2.destroyAllWindows()

# DB 연결 닫기
db.close_connection()
