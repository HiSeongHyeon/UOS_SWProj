import cv2
import mediapipe as mp
import numpy as np
import time
import math
from queue import Queue

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

q_angle_waist = Queue(maxsize=10)
q_tuttle_neck = Queue(maxsize=10)
q_hands       = Queue(maxsize=10)
q_brightness  = Queue(maxsize=10)

def initialize_queue(size, initial_value):
    q = Queue(maxsize=size)  # 최대 크기를 설정
    for _ in range(size):
        q.put(initial_value)  # 초기값 추가
    return q

q_angle_waist = initialize_queue(5, 0)
q_tuttle_neck = initialize_queue(5, 0)
q_hands = initialize_queue(5, 0)
q_brightness = initialize_queue(5, 0)

# 판단할 자세별 클래스
class angle_waist:
    def __init__(self, data, queue, output): 
        self.data = data 
        self.queue = queue
        self.output = output 
    
    def average_output(self):
        total = 0
        temp_list = []

        # 큐 순회하며 합산
        while not self.queue.empty():
            item = self.queue.get()
            total += item
            temp_list.append(item)

        # 원래 큐 상태로 복구
        for item in temp_list:
            self.queue.put(item)

        # 평균 계산
        self.output = total / len(temp_list)
        return self.output
    
    def Enqueue(self, data):
        self.queue.get()
        self.queue.put(data)

class turttle_neck:
    def __init__(self, data, queue, output):
        self.data = data
        self.queue = queue
        self.output = output
    
    def average_output(self):
        total = 0
        temp_list = []

        # 큐 순회하며 합산
        while not self.queue.empty():
            item = self.queue.get()
            total += item
            temp_list.append(item)

        # 원래 큐 상태로 복구
        for item in temp_list:
            self.queue.put(item)

        # 평균 계산
        self.output = total / len(temp_list)
        return self.output 
    
    def Enqueue(self, data):
        self.queue.get()
        self.queue.put(data)

class hands:
    def __init__(self, data, queue, output):
        self.data = data
        self.queue = queue
        self.output = output
    
    def average_output(self):
        total = 0
        temp_list = []

        # 큐 순회하며 합산
        while not self.queue.empty():
            item = self.queue.get()
            total += item
            temp_list.append(item)

        # 원래 큐 상태로 복구
        for item in temp_list:
            self.queue.put(item)

        # 평균 계산
        self.output = total / len(temp_list)
        return self.output  
    
    def Enqueue(self, data):
        self.queue.get()
        self.queue.put(data)

class brightness:
    def __init__(self, data, queue, output):
        self.data = data
        self.queue = queue
        self.output = output
    
    def average_output(self):
        total = 0
        temp_list = []

        # 큐 순회하며 합산
        while not self.queue.empty():
            item = self.queue.get()
            total += item
            temp_list.append(item)

        # 원래 큐 상태로 복구
        for item in temp_list:
            self.queue.put(item)

        # 평균 계산
        self.output = total / len(temp_list)
        return self.output
    
    def Enqueue(self, data):
        self.queue.get()
        self.queue.put(data)
     
cnt = 0

angle_waist = angle_waist(data = 0.0, queue = q_angle_waist, output = 0.0)
turttle_neck = turttle_neck(data = 0.0, queue = q_tuttle_neck, output = 0.0)
hands = hands(data = 0.0, queue = q_hands, output = 0.0)
brightness = brightness(data = 0.0, queue = q_brightness, output = 0.0)

def estimation_pose():
    #기준에 따라 상태 출력
    list = [0, 0, 0, 0]

    # 허리 기울임은 비율로 나타내기 어려움(애초에 0도를 정상으로 시작하기 때문 / 0도~4도 정상 / 4 ~ 7도 주의 / 7 ~ 10도 이상 경고 )
    angle_waist.Enqueue(abs(angle_waist.data))
    angle_waist.average_output()
    list[0] = angle_waist.output
    

    # 거북목
    turttle_neck.Enqueue(turttle_neck.data)
    turttle_neck.average_output()
    list[1] = (turttle_neck.output/center_mouth_dist_cho - 1.0)*100

    # 턱괴기
    hands.Enqueue(hands.data)
    hands.average_output()
    if hands.output > 5:
        list[2] = 0
    else:
        list[2] = 1
        
    
    # 밝기
    brightness.Enqueue(brightness.data)
    brightness.average_output()
    if brightness.output > 60:
        list[3] = 0
    else:
        list[3] = 1
    
    return list

def result_pose(list):
    # 허리 각도
    if list[0] < 5:
        list[0] = 0
    elif list[0] >= 5 and list[0] < 15:
        list[0] = 1
    else:
        list[0] = 2

    # 거북목
    if list[1] < 10:
        list[1] = 0
    elif list[1] >= 10 and list[1] < 30:
        list[1] = 1
    else:
        list[1] = 2

    # 턱괴기

    # 밝기
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
                # left_eye = results.pose_landmarks.landmark[2]
                # right_eye = results.pose_landmarks.landmark[6]
                left_shoulder = results.pose_landmarks.landmark[11]
                right_shoulder = results.pose_landmarks.landmark[12]
                left_mouth = results.pose_landmarks.landmark[9]
                right_mouth = results.pose_landmarks.landmark[10]
                left_ankle = results.pose_landmarks.landmark[28]
                right_ankle = results.pose_landmarks.landmark[29]

                # 합성 키 포인트
                angle_shoulder = abs(math.degrees(math.atan(right_shoulder.y - left_shoulder.y)/(right_shoulder.x - left_shoulder.x)))
                center_mouth_dist = (left_mouth.z + right_mouth.z)/2
                left_hand_distance = math.sqrt((left_mouth.x - left_ankle.x)**2 + (left_mouth.y - left_ankle.y)**2 + 10*(left_mouth.z - left_ankle.z)**2)
                right_hand_distance = math.sqrt(10*(right_mouth.x - right_ankle.x)**2 + (right_mouth.y - right_ankle.y)**2 + 10*(right_mouth.z - right_ankle.z)**2)
                
                print(f"Right hand: (x={right_ankle.x:.4f}, y={right_ankle.y:.4f},  z= {right_ankle.z:.4f}, visibility = {right_ankle.visibility}")

                angle_waist.data = angle_shoulder
                turttle_neck.data = center_mouth_dist
                hands.data = min(left_hand_distance, right_hand_distance)
                
                ret, frame = cap.read()
                if not ret:
                    ret = 1

                # 그레이스케일로 변환
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # 밝기 측정 (평균 계산)
                brightness.data = gray.mean()

                # 개인 별 바른 자세 데이터(어디에 만들지 잘 모르겠어서 일단 여기에 만들었음)
                center_mouth_dist_cho = -1.1

                # 확인용 코드(값 잘 받는지 확인)
                print(f"hand dist = {hands.data}")
                
                outputList = result_pose(estimation_pose())

                for i in range(4):
                    print(outputList[i])


                # print(f"cnt = {angle_waist.cnt:.4f}")
                # print(f"data = {monitor_far.data:.4f}")
                # print(f"output = {monitor_far.output:.4f}")    
            else: 
                cnt += 1
                if cnt > 10: # 확인 빠르게 하기 위해 10초로 설정, 추후에 1분으로 고치면 될 듯
                    disappear = 1
                    cnt = 0 # 이 부분 어떻게 처리할 것인지. 확인을 누르면 cnt를 0으로 돌릴지 논의
                else:
                    disappear = 0


            # 마지막 출력 시간 갱신
            last_time = current_time

        # ESC 키를 누르면 종료
        if cv2.waitKey(5) & 0xFF == 27:
            break

# 자원 해제
cap.release()
cv2.destroyAllWindows()
