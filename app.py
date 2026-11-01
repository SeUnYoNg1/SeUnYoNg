import streamlit as st
from google import genai
import os
import cv2
import numpy as np
from PIL import Image

st.title("📸 AI 정부 지원금 포토 스캐너")
st.write("서류나 화면 캡처 사진 1장을 올리면 AI가 지원금을 스캔해 드립니다.")

# Streamlit 비밀변수(Secrets) 또는 환경변수에서 안전하게 API 키 불러오기
API_KEY = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("🔑 API 키가 설정되지 않았습니다. Streamlit 설정에서 GEMINI_API_KEY를 등록해 주세요.")
    st.stop()

client = genai.Client(api_key=API_KEY)

uploaded_file = st.file_uploader("서류 사진 업로드", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드된 사진", use_container_width=True)
    
    if st.button("🚀 지원금 스캔 시작"):
        with st.spinner("AI가 분석 중입니다..."):
            prompt = "당신은 정부 지원금 스캐너입니다. 사진을 분석하여 알맞은 지원금 3가지를 추천해주세요."
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[image, prompt]
            )
            st.markdown("### 📊 분석 결과")
            st.write(response.text)
