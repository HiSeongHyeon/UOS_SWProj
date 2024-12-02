from HPE.class_mod import *
from queue import Queue


global flag_win, count_time, disappear, last_time
flag_win = 1
count_time = 1
disappear = 0
last_time = 0
cnt = 0
gray = 0
complete = 0
cnt_start = 0
outputList = []

###########################################################################
#                   자세             등록                                  #
###########################################################################

def average_pose(cnt, data, listData, i):

    # 실시간 자세 정보 저장
    if cnt < 10:
        listData[i] = listData[i] + data
        return listData[i]
        
    # 10초 동안의 자세 정보에 대한 평균을 저장하고 반환한다.    
    else:  
        if cnt == 10:
            average = listData[i]/10
        else:
            average = listData[i]

        return average 


def save_pose(cnt, keyPoint_list, pose_list, i):
    for i in range(5):
        pose_list[i] = average_pose(cnt, keyPoint_list[i], pose_list, i)
        
    return pose_list

keyPoint_list = [0.0, 0.0, 0.0, 0.0, 0.0]   # 실시간 자세 정보
pose_list = [0.0, 0.0, 0.0, 0.0, 0.0]       # DB에 저장할 최종 자세 정보

###########################################################################
#                   자세             판단                                  #
###########################################################################

q_angle_waist = Queue(maxsize=10)
q_tuttle_neck = Queue(maxsize=10)
q_hands       = Queue(maxsize=10)
q_brightness  = Queue(maxsize=10)

def initialize_queue(size, initial_value):
    q = Queue(maxsize=size)  # 최대 크기를 설정
    for _ in range(size):
        q.put(initial_value)  # 초깃값 추가
    return q

q_angle_waist = initialize_queue(5, 0)
q_tuttle_neck = initialize_queue(5, 0)
q_hands = initialize_queue(5, 0)
q_brightness = initialize_queue(5, 0)

outputlist = [0, 0, 0, 0]

angle_waist = angle_waist(data = 0.0, queue = q_angle_waist, output = 0.0)
turttle_neck = turttle_neck(data = 0.0, queue = q_tuttle_neck, output = 0.0)
hands = hands(data = 0.0, queue = q_hands, output = 0.0)
brightness = brightness(data = 0.0, queue = q_brightness, output = 0.0)


def estimation_pose(center_mouth_dist_DB,hands_distance_DB):
    #기준에 따라 상태를 반환할 리스트
    list = [0, 0, 0, 0]

    # 허리 기울임(기울어진 각도 반환)
    angle_waist.enqueue(abs(angle_waist.data))                  
    angle_waist.average_output()
    list[0] = angle_waist.output
    

    # 거북목(DB에 저장된 사용자별 바른 자세 정보와의 상대 오차 반환)
    turttle_neck.enqueue(turttle_neck.data)
    turttle_neck.average_output()
    list[1] = (turttle_neck.output/center_mouth_dist_DB - 1.0)*100

    # 턱괴기(DB에 저장된 사용자별 바른 자세 정보와의 비교를 통한 판단 결과 반환)
    hands.enqueue(hands.data)
    hands.average_output()
    if hands.output >= hands_distance_DB:
        list[2] = 0
    else:
        list[2] = 1
        
    
    # 밝기(절대적인 밝기 기준과의 비교를 통한 판단 결과 반환)
    brightness.enqueue(brightness.data)
    brightness.average_output()
    if brightness.output > 60:
        list[3] = 0
    else:
        list[3] = 1
    
    return list

def result_pose(list):
    
    # 허리 각도 (단계 1: 5도 이하 / 단계 2: 5~15도 / 단계 3: 15도 이상)
    if list[0] < 5:                     
        list[0] = 0
    elif list[0] >= 5 and list[0] < 15:
        list[0] = 1
    else:
        list[0] = 2

    # 거북목 (단계 1: 15% 이하 / 단계 2: 15~40% / 단계 3: 40% 이상)       
    if list[1] < 15:
        list[1] = 0
    elif list[1] >= 15 and list[1] < 40:
        list[1] = 1
    else:
        list[1] = 2

    # 턱괴기(턱을 괴고 있음(1) / 괴고 있지 않음(0))
    if list[2]:
        list[2] = 1
    else:
        list[2] = 0

    # 밝기(밝기가 어두움(1) / 어둡지 않음(0))
    if list[3]:
        list[3] = 1
    else:
        list[3] = 0

    return list

