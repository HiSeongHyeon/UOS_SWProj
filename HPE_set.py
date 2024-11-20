import cv2
import mediapipe as mp
import numpy as np
import time
import math

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def average_pose(cnt, data, listData, i, j):
    if listData[i][j] is None:
        listData[i][j] = 0.0
        
    if cnt < 10:
        listData[i][j] = listData[i][j] + data
        return listData[i][j]
        
    else:
        return listData[i][j]/cnt 

pose_list = [[0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0]
             , [0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0]]
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


                # 자세 등록
                pose_list[0][0] = 2
                pose_list[0][1] = average_pose(cnt, left_eye.x, pose_list, 0, 1)
                pose_list[0][2] = average_pose(cnt, left_eye.y, pose_list, 0, 2)
                pose_list[0][3] = average_pose(cnt, left_eye.z, pose_list, 0, 3)
                pose_list[0][4] = average_pose(cnt, left_eye.visibility, pose_list, 0, 4)

                pose_list[1][0] = 6
                pose_list[1][1] = average_pose(cnt, right_eye.x, pose_list, 1, 1)
                pose_list[1][2] = average_pose(cnt, right_eye.y, pose_list, 1, 2)            
                pose_list[1][3] = average_pose(cnt, right_eye.z, pose_list, 1, 3)
                pose_list[1][4] = average_pose(cnt, right_eye.visibility, pose_list, 1, 4)

                pose_list[2][0] = 11
                pose_list[2][1] = average_pose(cnt, left_shoulder.x, pose_list, 2, 1)
                pose_list[2][2] = average_pose(cnt, left_shoulder.y, pose_list, 2, 2)            
                pose_list[2][3] = average_pose(cnt, left_shoulder.z, pose_list, 2, 3)
                pose_list[2][4] = average_pose(cnt, left_shoulder.visibility, pose_list, 2, 3)

                pose_list[3][0] = 12
                pose_list[3][1] = average_pose(cnt, right_shoulder.x, pose_list, 3, 1)
                pose_list[3][2] = average_pose(cnt, right_shoulder.y, pose_list, 3, 2)            
                pose_list[3][3] = average_pose(cnt, right_shoulder.z, pose_list, 3, 3)
                pose_list[3][4] = average_pose(cnt, right_shoulder.visibility, pose_list, 3, 4)

                pose_list[4][0] = 9
                pose_list[4][1] = average_pose(cnt, left_mouth.x, pose_list, 4, 1)
                pose_list[4][2] = average_pose(cnt, left_mouth.y, pose_list, 4, 2)            
                pose_list[4][3] = average_pose(cnt, left_mouth.z, pose_list, 4, 3)
                pose_list[4][4] = average_pose(cnt, left_mouth.visibility, pose_list, 4, 4)

                pose_list[5][0] = 10
                pose_list[5][1] = average_pose(cnt, right_mouth.x, pose_list, 5, 1)
                pose_list[5][2] = average_pose(cnt, right_mouth.y, pose_list, 5, 2)            
                pose_list[5][3] = average_pose(cnt, right_mouth.z, pose_list, 5, 3)
                pose_list[5][4] = average_pose(cnt, right_mouth.visibility, pose_list, 5, 4)

                pose_list[6][0] = 28
                pose_list[6][1] = average_pose(cnt, left_ankle.x, pose_list, 6, 1)
                pose_list[6][2] = average_pose(cnt, left_ankle.y, pose_list, 6, 2)            
                pose_list[6][3] = average_pose(cnt, left_ankle.z, pose_list, 6, 3)
                pose_list[6][4] = average_pose(cnt, left_ankle.visibility, pose_list, 6, 4)

                pose_list[7][0] = 29
                pose_list[7][1] = average_pose(cnt, right_ankle.x, pose_list, 7, 1)
                pose_list[7][2] = average_pose(cnt, right_ankle.y, pose_list, 7, 2)            
                pose_list[7][3] = average_pose(cnt, right_ankle.z, pose_list, 7, 3)
                pose_list[7][4] = average_pose(cnt, right_ankle.visibility, pose_list, 7, 4)

                cnt += 1
        

            if cnt > 9: 
                for i in range(8):
                    for j in range(5):
                        print(pose_list[i][j])
                cnt = 0
            else:
               print("화면에 자세가 보이도록 앉아주세요.")

            # 마지막 출력 시간 갱신
            last_time = current_time

        # ESC 키를 누르면 종료
        if cv2.waitKey(5) & 0xFF == 27:
            break

# 자원 해제
cap.release()
cv2.destroyAllWindows()
