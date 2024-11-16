import cv2
import mediapipe as mp
import numpy as np
import time
import math

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# 자세 판단 카운트 변수

class angle_waist:
    def __init__(self, cnt = 0, data = 0.0, output = 0.0):
        self.cnt = cnt 
        self.data = data 
        self.output = output 
    
    def reset_cnt(self):
        self.cnt = 0
    
    def increment_cnt(self):
        self.cnt += 1

    def decrement_cnt(self):
        self.cnt -= 1
    
    def averge_output(self):
        if self.cnt == 1:
            self.output += self.data 
        else:
            self.output = (self.output + self.data) / 2

angle_waist = angle_waist(cnt=0, data=0.0, output=0.0)


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
                angle_waist.data = abs(math.degrees(math.atan(right_shoulder.y - left_shoulder.y)/(right_shoulder.x - left_shoulder.x)))
                length_neck = math.sqrt(((right_mouth.x + left_mouth.x)/2 - (right_shoulder.x + left_shoulder.x)/2)**2 + ((right_mouth.y + left_mouth.y)/2 - (right_shoulder.y + left_shoulder.y)/2)**2)
                left_hand_distance = math.sqrt((left_mouth.x - left_ankle.x)**2 + (left_mouth.y - left_ankle.y)**2)
                right_hand_distance = math.sqrt((right_mouth.x - right_ankle.x)**2 + (right_mouth.y - right_ankle.y)**2)

                
                # 개인 별 바른 자세 데이터(어디에 만들지 잘 모르겠어서 일단 여기에 만들었음)
                center_shoulder_dist_cho = -0.5
                center_mouth_dist_cho = -1.1


                #기준에 따라 상태 출력

                # 허리 기울임은 비율로 나타내기 어려움(애초에 0도를 정상으로 시작하기 때문 / 0도~4도 정상 / 4 ~ 7도 주의 / 7 ~ 10도 이상 경고 )
                if abs(angle_waist.data) > 4:
                    angle_waist.increment_cnt()
                    angle_waist.averge_output()
                    if angle_waist.cnt > 10:
                        # print(f"허리를 기울이지 마세요.")
                        print(f"output = {angle_waist.output:.4f}") # 이 자리에 리턴문이 오면 될 듯
                        angle_waist.reset_cnt()
                else:
                    if angle_waist.cnt > 0:
                        angle_waist.decrement_cnt()
                    

                print(f"cnt = {angle_waist.cnt:.4f}")
                #print(f"data = {angle_waist.data:.4f}")
                #print(f"output = {angle_waist.output:.4f}")    
           

            # 마지막 출력 시간 갱신
            last_time = current_time

        # ESC 키를 누르면 종료
        if cv2.waitKey(5) & 0xFF == 27:
            break

# 자원 해제
cap.release()
cv2.destroyAllWindows()