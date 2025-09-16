import cv2
import mediapipe as mp
import numpy as np

def analyze_and_draw(image_path):
    """
    사진에서 포즈를 추출하고, 와이어프레임을 그려 반환
    """
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True, model_complexity=2, enable_segmentation=False)

    # 이미지 읽기
    image = cv2.imread(image_path)
    if image is None:
        return None, "이미지를 불러올 수 없습니다."

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    if not results.pose_landmarks:
        return None, "사진에서 포즈를 감지하지 못했습니다. 정면 사진을 사용해보세요."

    h, w, _ = image.shape
    landmarks = results.pose_landmarks.landmark

    # 와이어프레임 그리기
    connections = mp_pose.POSE_CONNECTIONS
    for start, end in connections:
        x1 = int(landmarks[start].x * w)
        y1 = int(landmarks[start].y * h)
        x2 = int(landmarks[end].x * w)
        y2 = int(landmarks[end].y * h)
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # 점도 찍기
    for lm in landmarks:
        x = int(lm.x * w)
        y = int(lm.y * h)
        cv2.circle(image, (x, y), 3, (0, 0, 255), -1)

    return image, landmarks