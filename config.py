from HPE.class_mod import *
from queue import Queue


global flag_win, count_time, disappear, last_time
flag_win = 1
count_time = 1
disappear = 0
last_time = 0
cnt = 0


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


angle_waist = angle_waist(data = 0.0, queue = q_angle_waist, output = 0.0)
turttle_neck = turttle_neck(data = 0.0, queue = q_tuttle_neck, output = 0.0)
hands = hands(data = 0.0, queue = q_hands, output = 0.0)
brightness = brightness(data = 0.0, queue = q_brightness, output = 0.0)


def estimation_pose(center_mouth_dist_cho):
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
    if list[2]:
        list[2] = 1
    else:
        list[2] = 0

    # 밝기
    if list[3]:
        list[3] = 1
    else:
        list[3] = 0

    return list