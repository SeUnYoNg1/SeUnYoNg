import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

st.title("📷 AI 정부 지원금 포토 스캐너")
st.write("서류나 화면 캡처 사진 1장을 올리면 AI가 지원금을 스캔해 드립니다.")

# API 키 설정
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("🔑 API 키가 설정되지 않았습니다. Streamlit Secrets를 확인해 주세요.")
    st.stop()

genai.configure(api_key=api_key)

# 모델 설정 (가장 안정적인 flash 모델 사용)
model = genai.GenerativeModel('gemini-1.5-flash')

uploaded_file = st.file_uploader("서류 사진 업로드", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드된 사진", use_container_width=True)

    if st.button("🚀 지원금 스캔 시작"):
        with st.spinner("AI가 분석 중입니다..."):
            try:
                response = model.generate_content([
                    image, 
                    "사진 속 서류를 분석하여 받을 수 있는 맞춤 정부지원금 3가지를 추천하고 이유를 설명해줘."
                ])
                st.markdown("### 📊 분석 결과")
                st.write(response.text)
            except Exception as e:
                st.error(f"분석 중 오류가 발생했습니다: {e}")
