import streamlit as st
from langchain_community.llms import CTransformers

# pip install langchain-community ctransformers
# https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML

llm = CTransformers(
    model="TheBloke/Llama-2-7B-Chat-GGML",
    model_file="llama-2-7b-chat.ggmlv3.q2_K.bin",
    model_type="llama"
)

st.title('인공지능 시인')

content = st.text_input('시의 주제를 제시해주세요.')

if st.button('시 작성 요청하기'):
    with st.spinner('시 작성 중...'):
        result = llm.predict("write a poem about " + content + ": ")
        st.write(result)