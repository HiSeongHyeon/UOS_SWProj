import cv2
import mediapipe as mp
import numpy as np
import time
import math

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# 자세 판단 카운트 변수
cnt_monitor_near = 0
cnt_monitor_far = 0
cnt_angle_waist = 0
cnt_angle_body = 0
cnt_turttle_neck = 0
cnt_hands = 0

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

                # 합성 키 포인트
                length_eye = math.sqrt((left_eye.x - right_eye.x)**2 + (left_eye.y - right_eye.y)**2)
                length_shoulder = math.sqrt((left_shoulder.x - right_shoulder.x)**2 + (left_shoulder.y - right_shoulder.y)**2)
                center_shoulder_dist = (left_shoulder.z + right_shoulder.z)/2
                center_mouth_dist = (left_mouth.z + right_mouth.z)/2
                angle_shoulder = math.degrees(math.atan(right_shoulder.y - left_shoulder.y)/(right_shoulder.x - left_shoulder.x))
                length_neck = math.sqrt(((right_mouth.x + left_mouth.x)/2 - (right_shoulder.x + left_shoulder.x)/2)**2 + ((right_mouth.y + left_mouth.y)/2 - (right_shoulder.y + left_shoulder.y)/2)**2)
                left_hand_distance = math.sqrt((left_mouth.x - left_ankle.x)**2 + (left_mouth.y - left_ankle.y)**2)
                right_hand_distance = math.sqrt((right_mouth.x - right_ankle.x)**2 + (right_mouth.y - right_ankle.y)**2)

                
                # 개인 별 바른 자세 데이터(어디에 만들지 잘 모르겠어서 일단 여기에 만들었음)
                center_shoulder_dist_cho = -0.5
                center_mouth_dist_cho = -1.1


                #기준에 따라 상태 출력

                if center_shoulder_dist < center_shoulder_dist_cho or left_shoulder.visibility < 0.9 or right_shoulder.visibility < 0.9:
                    cnt_monitor_near += 1
                    if cnt_monitor_near > 10:
                        print(f"모니터에서 떨어지세요.")
                        cnt_monitor_near = 0
                    else:
                        if cnt_monitor_near >= 1:
                            cnt_monitor_near -= 1

                elif center_shoulder_dist > -0.3:
                    cnt_monitor_far += 1
                    if cnt_monitor_far > 10:
                        print(f"모니터와 너무 떨어졌습니다.")
                        cnt_monitor_far = 0
                    else:
                        if cnt_monitor_far >= 1:
                            cnt_monitor_far -= 1

                if abs(angle_shoulder) > 4:
                    cnt_angle_waist += 1
                    if cnt_angle_waist > 10:
                        print(f"허리를 기울이지 마세요.")
                        cnt_angle_waist = 0
                else:
                    if cnt_angle_waist >= 1:
                        cnt_angle_waist -= 1
                    
                if center_mouth_dist > center_mouth_dist_cho + 0.2:
                    cnt_angle_body += 1
                    if cnt_angle_body > 10:
                        print(f"몸을 앞으로 기울이세요.")
                        cnt_angle_body = 0
                else:
                    if cnt_angle_body >= 1:
                        cnt_angle_body -= 1  

                if center_mouth_dist < center_mouth_dist_cho:
                    cnt_turttle_neck += 1
                    if cnt_turttle_neck > 10:
                        print(f"거북목입니다.")
                        cnt_turttle_neck = 0
                else:
                    if cnt_turttle_neck >= 1:
                        cnt_turttle_neck -= 1 

                if left_hand_distance < 1 or right_hand_distance < 1:
                    cnt_hands += 1
                    if cnt_hands > 10:
                        print(f"턱을 괴지 마세요.")
                        cnt_hands = 0
                else:
                    if cnt_hands >= 1:
                        cnt_hands -= 1
        
                

                print(f"cnt = {cnt_turttle_neck:.4f}")

           

            # 마지막 출력 시간 갱신
            last_time = current_time

        # ESC 키를 누르면 종료
        if cv2.waitKey(5) & 0xFF == 27:
            break

# 자원 해제
cap.release()
cv2.destroyAllWindows()