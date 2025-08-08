# fastmcp_client.py
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_mcp_server():
    # 서버 매개변수 설정
    server_params = StdioServerParameters(
        command="python",
        args=["./18-mcp/fastmcp_server.py"],  # 여러분의 서버 파일
        env={}
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 서버 초기화
            await session.initialize()
            
            # 사용 가능한 도구 목록 가져오기
            tools = await session.list_tools()
            print("사용 가능한 도구들:")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")
            
            # 도구 호출 예제 1: say_hello
            result = await session.call_tool("say_hello", {"name": "김철수"})
            print(f"\nsay_hello 결과: {result.content}")
            
            # 도구 호출 예제 2: calculate_sum
            result = await session.call_tool("calculate_sum", {"a": 10, "b": 20})
            print(f"calculate_sum 결과: {result.content}")

if __name__ == "__main__":
    asyncio.run(test_mcp_server())