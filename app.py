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

# 로고 로드
logo = None
try:
    logo = Image.open("assets/lucy_logo.png").convert("RGBA")
except:
    st.warning("로고 파일을 찾을 수 없습니다. (assets/lucy_logo.png)")

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
            def add_logo_to_image(img_array, logo_img, show_logo):
                if not show_logo or logo_img is None:
                    return img_array

                pil_img = Image.fromarray(cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB))
                logo_resized = logo_img.resize((200, 100), Image.Resampling.LANCZOS)
                
                img_width, img_height = pil_img.size
                position = (img_width - 200 - 10, 10)
                
                pil_img.paste(logo_resized, position, logo_resized)
                result = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
                return result

            # 로고 적용 여부에 따라 이미지 처리
            final_image = add_logo_to_image(result_img, logo, show_logo)

            # 결과 표시
            st.image(final_image, caption="✅ 분석된 와이어프레임", use_column_width=True)

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
