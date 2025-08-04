from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

chat_model = ChatOpenAI(model="gpt-4o-mini")

st.title('🎭 인공지능 시인')

content = st.text_input('시의 주제를 제시해주세요.')

if st.button('시 작성 요청하기'):
    if content:
        with st.spinner('시 작성 중...'):
            try:
                # 최신 invoke 방식 사용
                result = chat_model.invoke([HumanMessage(content=content + "에 대한 시를 써줘")])
                
                st.markdown("### 🎨 생성된 시:")
                st.markdown(f"```\n{result.content}\n```")
                
                # 추가 정보 표시
                with st.expander("📊 생성 정보"):
                    st.write(f"모델: {result.response_metadata.get('model_name', 'gpt-4o-mini')}")
                    if 'token_usage' in result.response_metadata:
                        token_info = result.response_metadata['token_usage']
                        st.write(f"사용된 토큰: {token_info.get('total_tokens', '정보 없음')}")
                        
            except Exception as e:
                st.error(f"❌ 오류 발생: {str(e)}")
    else:
        st.warning("⚠️ 시의 주제를 입력해주세요!")