import subprocess
import json
import re
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

class MCPClient:
    def __init__(self):
        # OpenAI LLM 모델 초기화
        self.chat_model = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.1
        )
        
    def call_mcp_tool(self, tool_name, arguments=None):
        """MCP 도구 호출 (로컬 함수 구현)"""
        try:
            if tool_name == "say_hello":
                name = arguments.get("name", "사용자") if arguments else "사용자"
                return f"안녕하세요, {name}님!"
            elif tool_name == "calculate_sum":
                if arguments and "a" in arguments and "b" in arguments:
                    result = arguments["a"] + arguments["b"]
                    return f"{arguments['a']} + {arguments['b']} = {result}"
                else:
                    return "계산에 필요한 인수가 부족합니다"
            else:
                return f"알 수 없는 도구: {tool_name}"
                
        except Exception as e:
            return f"도구 호출 중 오류 발생: {str(e)}"
    
    def parse_calculation(self, user_input):
        """사용자 입력에서 계산식 추출"""
        # 간단한 덧셈 패턴 매칭
        pattern = r'(\d+)\s*\+\s*(\d+)'
        match = re.search(pattern, user_input)
        
        if match:
            a, b = int(match.group(1)), int(match.group(2))
            return a, b
        
        return None, None
    
    def process_user_input(self, user_input):
        """사용자 입력 처리"""
        # LLM에게 질의
        messages = [
            SystemMessage(content="""당신은 MCP 도구를 사용할 수 있는 AI입니다.
사용자가 인사를 하면 'USE_TOOL:say_hello' 형식으로 응답하세요.
사용자가 계산을 묻으면 'USE_TOOL:calculate_sum' 형식으로 응답하세요.
도구를 사용하지 않아도 되는 질문은 직접 답변하세요."""),
            HumanMessage(content=user_input)
        ]
        
        # LLM 응답 받기
        result = self.chat_model.invoke(messages)
        print(f"사용자: {user_input}")
        print(f"LLM 분석: {result.content}")
        
        # 도구 사용이 필요한 경우 처리
        if "USE_TOOL:say_hello" in result.content:
            # 사용자 이름 추출 (간단한 방법)
            name = "사용자"  # 실제로는 더 정교한 이름 추출 로직 필요
            tool_result = self.call_mcp_tool("say_hello", {"name": name})
            print(f"MCP 도구 결과: {tool_result}")
            
        elif "USE_TOOL:calculate_sum" in result.content:
            # 계산식에서 숫자 추출
            a, b = self.parse_calculation(user_input)
            if a is not None and b is not None:
                tool_result = self.call_mcp_tool("calculate_sum", {"a": a, "b": b})
                print(f"MCP 도구 결과: {tool_result}")
            else:
                print("계산할 숫자를 찾을 수 없습니다.")
        elif any(op in user_input for op in ['+', '더하기', '계산']):
            # LLM이 직접 답변했지만 계산 관련 질문인 경우 도구 사용
            a, b = self.parse_calculation(user_input)
            if a is not None and b is not None:
                tool_result = self.call_mcp_tool("calculate_sum", {"a": a, "b": b})
                print(f"MCP 도구 결과: {tool_result}")
            else:
                print("LLM 직접 답변:", result.content)
        
        return result.content
    
    def close(self):
        """리소스 정리 (현재는 특별한 정리 작업 없음)"""
        pass

# 사용 예제
if __name__ == "__main__":
    client = MCPClient()
    
    try:
        # 테스트 케이스들
        test_cases = [
            "안녕하세요",
            "mcp를 이용하여 2+2를 계산해줘"
        ]
        
        for test_input in test_cases:
            print(f"\n{'='*50}")
            client.process_user_input(test_input)
            
    finally:
        client.close()