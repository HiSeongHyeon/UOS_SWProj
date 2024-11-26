import cv2
import mediapipe as mp
import numpy as np
import time
import math

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# 판단할 자세별 클래스
class angle_waist:
    def __init__(self, cnt = 0, data = 0.0, output = 0.0):
        self.cnt = cnt 
        self.data = data 
        self.output = output 
    
    def average_output(self):
        if self.cnt == 1:
            self.output += self.data 
        else:
            self.output = (self.output + self.data) / 2

class monitor_near:
    def __init__(self, cnt = 0, data = 0.0, output = 0.0):
        self.cnt = cnt
        self.data = data
        self.output = output
    
    def average_output(self):
        if self.cnt == 1:
            self.output += self.data 
        else:
            self.output = (self.output + self.data) / 2

class monitor_far:
    def __init__(self, cnt = 0, data = 0.0, output = 0.0):
        self.cnt = cnt
        self.data = data
        self.output = output
    
    def average_output(self):
        if self.cnt == 1:
            self.output += self.data 
        else:
            self.output = (self.output + self.data) / 2  

class turttle_neck:
    def __init__(self, cnt = 0, data = 0.0, output = 0.0):
        self.cnt = cnt
        self.data = data
        self.output = output
    
    def average_output(self):
        if self.cnt == 1:
            self.output += self.data 
        else:
            self.output = (self.output + self.data) / 2  

class hands:
    def __init__(self, cnt = 0, data = 0.0, output = 0.0):
        self.cnt = cnt
        self.data = data
        self.output = output
    
    def average_output(self):
        if self.cnt == 1:
            self.output += self.data 
        else:
            self.output = (self.output + self.data) / 2  

cnt = 0

angle_waist = angle_waist(cnt = 0, data = 0.0, output = 0.0)
monitor_near = monitor_near(cnt = 0, data = 0.0, output =0.0)
monitor_far = monitor_far(cnt = 0, data = 0.0, output =0.0)
turttle_neck = turttle_neck(cnt = 0, data = 0.0, output =0.0)
hands = hands(cnt = 0, data = 0.0, output =0.0)

def estimation_pose():
    #기준에 따라 상태 출력
    list = [0, 0, 0, 0, 0]

    # 허리 기울임은 비율로 나타내기 어려움(애초에 0도를 정상으로 시작하기 때문 / 0도~4도 정상 / 4 ~ 7도 주의 / 7 ~ 10도 이상 경고 )
    if abs(angle_waist.data) > 4:
        angle_waist.cnt += 1
        angle_waist.average_output()
        if angle_waist.cnt > 10:
            list[0] = angle_waist.output # 허리 기울임 정도 list[0]에 저장
            angle_waist.cnt = 0
    else:
        if angle_waist.cnt > 0:
            list[0] = 0                  # 출력될 리스트의 경우 자세에 문제가 없다면 0 리턴
            angle_waist.cnt -= 1

    if monitor_near.data < center_shoulder_dist_cho:    # 비교문의 기준으로 들어갈 변수 >>> DB상의 개인별 바른 자세 정보로 바뀌면 됨 이 부분을 파라미터로 받아오면 될 듯!
        monitor_near.cnt += 1
        monitor_near.average_output()
        if monitor_near.cnt > 10:
            list[1] = (monitor_near.output/center_shoulder_dist_cho - 1.0)*100
            monitor_near.cnt = 0
        else:
            if monitor_near.cnt >= 1:
                list[1] = 0
                monitor_near.cnt -= 1

    elif monitor_far.data > center_shoulder_dist_cho:
        monitor_far.cnt += 1
        monitor_far.average_output()
        if monitor_far.cnt > 10:
            list[2] = (1.0 - monitor_far.output/center_shoulder_dist_cho)*100
            monitor_far.cnt = 0
        else:
            if monitor_far.cnt >= 1:
                list[2] = 0
                monitor_far.cnt -= 1    

    if turttle_neck.data < center_mouth_dist_cho:
        turttle_neck.cnt += 1
        turttle_neck.average_output()
        if turttle_neck.cnt > 10:
            list[3] = (turttle_neck.output/center_mouth_dist_cho - 1.0)*100
            turttle_neck.cnt = 0
    else:
        if turttle_neck.cnt >= 1:
            list[3] = 0
            turttle_neck.cnt -= 1 
            
    if hands.data < 1:
        hands.cnt += 1
        hands.average_output()
        if hands.cnt > 10:
            list[4] = hands.output
            hands.cnt = 0
    else:
        if hands.cnt >= 1:
            list[4] = 0
            hands.cnt -= 1

    return list


    
    

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
                angle_waist.data = abs(math.degrees(math.atan(right_shoulder.y - left_shoulder.y)/(right_shoulder.x - left_shoulder.x)))
                center_shoulder_dist = (left_shoulder.z + right_shoulder.z)/2
                center_mouth_dist = (left_mouth.z + right_mouth.z)/2
                left_hand_distance = math.sqrt((left_mouth.x - left_ankle.x)**2 + (left_mouth.y - left_ankle.y)**2)
                right_hand_distance = math.sqrt((right_mouth.x - right_ankle.x)**2 + (right_mouth.y - right_ankle.y)**2)

                monitor_near.data = center_shoulder_dist
                monitor_far.data = center_shoulder_dist
                turttle_neck.data = center_mouth_dist
                hands.data = min(left_hand_distance, right_hand_distance)
                
                # 개인 별 바른 자세 데이터(어디에 만들지 잘 모르겠어서 일단 여기에 만들었음)
                center_shoulder_dist_cho = -0.5
                center_mouth_dist_cho = -1.1

                # 확인용 코드(값 잘 받는지 확인)
                print(f"center of shoulder = {center_shoulder_dist:.4f}")
                print(f"center of shoulder = {monitor_near.output/center_shoulder_dist_cho:.4f}")

                outputList = estimation_pose()
                for i in range(5):
                    print(outputList[i])


                #print(f"cnt = {angle_waist.cnt:.4f}")
                #print(f"data = {angle_waist.data:.4f}")
                #print(f"output = {angle_waist.output:.4f}")    
            else: 
                cnt += 1
                if cnt > 10: # 확인 빠르게 하기 위해 10초로 설정, 추후에 1분으로 고치면 될 듯
                    print(1)
                    cnt = 0 # 이 부분 어떻게 처리할 것인지. 확인을 누르면 cnt를 0으로 돌릴지 논의
                else:
                    print(0)


            # 마지막 출력 시간 갱신
            last_time = current_time

        # ESC 키를 누르면 종료
        if cv2.waitKey(5) & 0xFF == 27:
            break

# 자원 해제
cap.release()
cv2.destroyAllWindows()