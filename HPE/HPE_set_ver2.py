import cv2
import mediapipe as mp
import numpy as np
import time
import math

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def average_pose(cnt, data, listData, i):
    if listData[i] is None:
        listData[i] = 0.0
        
    if cnt < 10:
        listData[i] = listData[i] + data
        return listData[i]
        
    else:
        average = listData[i]/10
        listData[i] = 0.0    
        return average 

def save_pose(cnt, keyPoint_list, pose_list, i):
    if pose_list[i] is None:
        pose_list[i] = 0.0

    for i in range(5):
        pose_list[i] = average_pose(cnt, keyPoint_list[i], pose_list, i)
        
    return pose_list
    
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
                # left shoulder (index 11), right shoulder (index 12)
                # 단일 키 포인트
                left_eye = results.pose_landmarks.landmark[2]
                right_eye = results.pose_landmarks.landmark[6]
                left_shoulder = results.pose_landmarks.landmark[11]
                right_shoulder = results.pose_landmarks.landmark[12]
                left_mouth = results.pose_landmarks.landmark[9]
                right_mouth = results.pose_landmarks.landmark[10]
                left_ankle = results.pose_landmarks.landmark[28]
                right_ankle = results.pose_landmarks.landmark[29]

                # angle_shoulder 
                keyPoint_list[0] = abs(math.degrees(math.atan(right_shoulder.y - left_shoulder.y)/(right_shoulder.x - left_shoulder.x)))
                
                # center_shoulder_dist 
                keyPoint_list[1] = (left_shoulder.z + right_shoulder.z)/2
                
                # center_mouth_dist 
                keyPoint_list[2] = (left_mouth.z + right_mouth.z)/2
                
                # left_hand_distance 
                keyPoint_list[3] = math.sqrt((left_mouth.x - left_ankle.x)**2 + (left_mouth.y - left_ankle.y)**2)
                
                # right_hand_distance 
                keyPoint_list[4] = math.sqrt((right_mouth.x - right_ankle.x)**2 + (right_mouth.y - right_ankle.y)**2)
                
                i=0

                # 자세 등록
                # 매 초마다 keyPoint_list를 pose_list에 저장(~cnt 9까지), cnt가 10이 되면 기존에 저장해온 값을 평균내서 출력  
                pose_list = save_pose(cnt, keyPoint_list, pose_list, i)
                
                # 확인용 출력 코드(이후 삭제 필요)                
                if cnt > 9: 
                    for j in range(5):
                        print(pose_list[j])

                    cnt = 0

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