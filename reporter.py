def get_body_ratios(landmarks):
    """
    포즈 데이터에서 신체 비율 계산
    """
    try:
        # 머리, 허리, 발
        head = landmarks[0]       # 코
        left_hip = landmarks[23]
        right_hip = landmarks[24]
        left_ankle = landmarks[27]
        right_ankle = landmarks[28]

        # 허리 중앙
        hip_y = (left_hip.y + right_hip.y) / 2
        ankle_y = (left_ankle.y + right_ankle.y) / 2

        # 비율 계산
        upper_length = abs(hip_y - head.y)
        lower_length = abs(ankle_y - hip_y)
        ratio = upper_length / lower_length if lower_length != 0 else 0

        return {
            "상체길이": round(upper_length, 3),
            "하체길이": round(lower_length, 3),
            "상하체비율": round(ratio, 2),
            "자세각도": "정면" if abs(head.x - 0.5) < 0.1 else "측면/기울어짐",
            "대칭성": "양호" if abs(left_hip.y - right_hip.y) < 0.05 else "주의"
        }
    except Exception as e:
        return {"에러": f"비율 계산 중 오류 발생: {str(e)}"}