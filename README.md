# 2024 소프트웨어 공학 설계(Human Pose Estimation)

<details>
<summary># 0. 준비사항 </summary>
# Medipipe, opencv-python 설치
- pip install mediapipe opencv-python
</details>

<details>
<summary> 1. HPE </summary>
mediapipe의 pose_landmarks에서 반환되는 각 키포인트(landmark)는 NormalizedLandmark 객체로, 이는 x, y, z, visibility의 속성을 가집니다.

따라서 left_shoulder (인덱스 11)의 속성들은 다음과 같습니다:

x: 이미지 너비를 기준으로 [0.0, 1.0] 범위 내의 좌표. 0은 이미지의 가장 왼쪽, 1은 가장 오른쪽.
y: 이미지 높이를 기준으로 [0.0, 1.0] 범위 내의 좌표. 0은 이미지의 가장 위쪽, 1은 가장 아래쪽.
z: 상대적인 깊이 좌표. 양수는 카메라에서 멀어지는 방향이고, 음수는 카메라에 가까워지는 방향입니다. 이 값은 이미지가 아닌 상대적인 거리 정보를 제공하며, x와 y처럼 정규화된 값이 아닙니다.
visibility: [0.0, 1.0] 범위의 신뢰도 값. 값이 1에 가까울수록 해당 관절이 명확하게 인식된 것이며, 0에 가까울수록 신뢰도가 낮습니다.

left_shoulder = results.pose_landmarks.landmark[11]
print(f"Left Shoulder - x: {left_shoulder.x}, y: {left_shoulder.y}, z: {left_shoulder.z}, visibility: {left_shoulder.visibility}")

About Key Points
0 - nose
1 - left eye (inner)
2 - left eye
3 - left eye (outer)
4 - right eye (inner)
5 - right eye
6 - right eye (outer)
7 - left ear
8 - right ear
9 - mouth (left)
10 - mouth (right)
11 - left shoulder
12 - right shoulder
13 - left elbow
14 - right elbow
15 - left wrist
16 - right wrist
17 - left pinky
18 - right pinky
19 - left index
20 - right index
21 - left thumb
22 - right thumb
23 - left hip
24 - right hip
25 - left knee
26 - right knee
27 - left ankle
28 - right ankle
29 - left heel
30 - right heel
31 - left foot index
32 - right foot index
</details>
