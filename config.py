from HPE.class_mod import *


global flag_win, count_time
flag_win = 1
count_time = 1

angle_waist = angle_waist(cnt = 0, data = 0.0, output = 0.0)
monitor_near = monitor_near(cnt = 0, data = 0.0, output =0.0)
monitor_far = monitor_far(cnt = 0, data = 0.0, output =0.0)
turttle_neck = turttle_neck(cnt = 0, data = 0.0, output =0.0)
hands = hands(cnt = 0, data = 0.0, output =0.0)

def estimation_pose(center_shoulder_dist_cho, center_mouth_dist_cho):
        #기준에 따라 상태 출력
        list = [0, 0, 0, 0, 0]
        cnt_num = 100
        # 허리 기울임은 비율로 나타내기 어려움(애초에 0도를 정상으로 시작하기 때문 / 0도~4도 정상 / 4 ~ 7도 주의 / 7 ~ 10도 이상 경고 )
        if abs(angle_waist.data) > 4:
            angle_waist.cnt += 1
            angle_waist.average_output()
            if angle_waist.cnt > cnt_num:
                list[0] = angle_waist.output # 허리 기울임 정도 list[0]에 저장
                angle_waist.cnt = 0
        else:
            if angle_waist.cnt > 0:
                list[0] = 0                  # 출력될 리스트의 경우 자세에 문제가 없다면 0 리턴
                angle_waist.cnt -= 1

        if monitor_near.data < center_shoulder_dist_cho:    # 비교문의 기준으로 들어갈 변수 >>> DB상의 개인별 바른 자세 정보로 바뀌면 됨 이 부분을 파라미터로 받아오면 될 듯!
            monitor_near.cnt += 1
            monitor_near.average_output()
            if monitor_near.cnt > cnt_num:
                list[1] = (monitor_near.output/center_shoulder_dist_cho - 1.0)*100
                monitor_near.cnt = 0
            else:
                if monitor_near.cnt >= 1:
                    list[1] = 0
                    monitor_near.cnt -= 1

        elif monitor_far.data > center_shoulder_dist_cho:
            monitor_far.cnt += 1
            monitor_far.average_output()
            if monitor_far.cnt > cnt_num:
                list[2] = (1.0 - monitor_far.output/center_shoulder_dist_cho)*100
                monitor_far.cnt = 0
            else:
                if monitor_far.cnt >= 1:
                    list[2] = 0
                    monitor_far.cnt -= 1    

        if turttle_neck.data < center_mouth_dist_cho:
            turttle_neck.cnt += 1
            turttle_neck.average_output()
            if turttle_neck.cnt > cnt_num:
                list[3] = (turttle_neck.output/center_mouth_dist_cho - 1.0)*100
                turttle_neck.cnt = 0
        else:
            if turttle_neck.cnt >= 1:
                list[3] = 0
                turttle_neck.cnt -= 1 
                
        if hands.data < 1:
            hands.cnt += 1
            hands.average_output()
            if hands.cnt > cnt_num:
                list[4] = hands.output
                hands.cnt = 0
        else:
            if hands.cnt >= 1:
                list[4] = 0
                hands.cnt -= 1

        return list

def result_pose(list):
        i = 1

        # 어깨. 0이 good, 2가 bad
        if list[0] < 5:
            list[0] = 0
        elif list[0] >= 5 and list[0] < 15:
            list[0] = 1
        else:
            list[0] = 2

        # 1번이 가까워지는거, 2번이 멀어지는거, 3번이 거북목
        for i in range(1, len(list)-1):
            if list[i] < 10:
                list[i] = 0
            elif list[i] >= 10 and list[i] < 30:
                list[i] = 1
            else:
                list[i] = 2

        # 4번이 턱괴기
        if list[4]:
            list[4] = 1
        else:
            list[4] = 0

        return list