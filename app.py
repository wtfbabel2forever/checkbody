import streamlit as st
from analyzer import analyze_and_draw
from reporter import get_body_ratios
from PIL import Image
import cv2

st.set_page_config(page_title="CheckBody", layout="centered")
st.title("📸 CheckBody - 신체 비율 분석기")
st.markdown("사진을 업로드하면 3D 와이어프레임과 신체 비율을 분석합니다.")

uploaded = st.file_uploader("📷 사진을 선택하세요", type=["jpg", "jpeg", "png"])

if uploaded:
    with open("temp.jpg", "wb") as f:
        f.write(uploaded.getbuffer())

    with st.spinner("🔍 분석 중입니다..."):
        result_img, data = analyze_and_draw("temp.jpg")

        if result_img is None:
            st.error(data)
        else:
            st.image(result_img, caption="✅ 분석된 와이어프레임", use_column_width=True)

            ratios = get_body_ratios(data)
            st.subheader("📊 분석 결과")
            st.json(ratios)

            # 다운로드
            result_pil = Image.fromarray(cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB))
            st.download_button(
                label="💾 결과 다운로드 (이미지)",
                data=result_pil.tobytes(),
                file_name="checkbody_result.png",
                mime="image/png"
            )