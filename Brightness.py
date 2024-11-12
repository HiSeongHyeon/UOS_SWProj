import cv2
import time

# 카메라 초기화
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

# 마지막 밝기 정보 출력 시간 저장
last_time = time.time()

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다.")
        break

    # 그레이스케일로 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 밝기 측정 (평균 계산)
    brightness = gray.mean()

    # 1초마다 밝기 정보 출력
    current_time = time.time()
    if current_time - last_time >= 1:
        print(f"현재 밝기: {brightness:.2f}")
        last_time = current_time  # 마지막 출력 시간을 갱신

    # 프레임 보여주기
    cv2.imshow('Camera', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 종료 작업
cap.release()
cv2.destroyAllWindows()
