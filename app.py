import streamlit as st
from analyzer import analyze_and_draw
from reporter import get_body_ratios
from PIL import Image
import cv2
import tempfile
import os
import numpy as np
from datetime import datetime

st.set_page_config(page_title="CheckBody", layout="centered")
st.title("📸 CheckBody - 신체 비율 분석기")
st.markdown("사진을 업로드하면 3D 와이어프레임과 신체 비율을 분석합니다.")

# 로고 로드 (경로 확인)
logo_path = "assets/lucy_logo.png"
logo = None
try:
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        st.success("✅ 로고 로드 성공")
    else:
        st.warning("⚠️ 로고 파일 없음: assets/lucy_logo.png")
except Exception as e:
    st.error(f"❌ 로고 로드 실패: {e}")

# 파일 업로드
uploaded = st.file_uploader("📷 사진을 선택하세요", type=["jpg", "jpeg", "png"])

if uploaded:
    # 임시 파일 생성
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
        tmp_file.write(uploaded.getvalue())
        temp_path = tmp_file.name

    with st.spinner("🔍 분석 중입니다..."):
        result_img, data = analyze_and_draw(temp_path)

        if result_img is None:
            st.error(data)
        else:
            # 로고 표시 여부
            st.subheader("🔧 설정")
            show_logo = st.checkbox("✅ 로고 표시", value=True)

            # 로고 삽입 함수
            def add_logo_to_image(img_array, logo_img, show):
                if not show or logo_img is None:
                    return img_array

                # OpenCV → PIL 변환
                pil_img = Image.fromarray(cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB))
                
                # 로고 크기 조정
                logo_resized = logo_img.resize((200, 100), Image.Resampling.LANCZOS)
                
                # 위치 (오른쪽 상단)
                img_width, img_height = pil_img.size
                position = (img_width - 210, 10)
                
                # 합성
                pil_img.paste(logo_resized, position, logo_resized)
                
                # PIL → OpenCV 변환
                result = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
                return result

            # 로고 삽입 전/후 비교
            st.subheader("🖼️ 이미지 비교")
            
            # 로고 없이
            st.image(result_img, caption="🔍 로고 없음", use_column_width=True)

            # 로고 적용
            final_image = add_logo_to_image(result_img, logo, show_logo)
            st.image(final_image, caption="✅ 로고 적용됨", use_column_width=True)

            # 분석 결과
            ratios = get_body_ratios(data)
            st.subheader("📊 분석 결과")
            st.json(ratios)

            # 다운로드 (타임스탬프 포함)
            now = datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")
            filename = f"checkbody_{timestamp}.png"

            rgb_image = cv2.cvtColor(final_image, cv2.COLOR_BGR2RGB)
            result_pil = Image.fromarray(rgb_image)

            st.download_button(
                label="💾 결과 다운로드 (이미지)",
                data=result_pil.tobytes(),
                file_name=filename,
                mime="image/png"
            )

    # 임시 파일 삭제
    os.unlink(temp_path)
