# fastmcp_server.py
from fastmcp import FastMCP

# 관리자권한으로 실행
# pip install fastmcp mcp

# MCP 이름 : fastmcp-hello

# MCP 서버 인스턴스 생성
mcp = FastMCP("Hello MCP Server")

@mcp.tool()
def say_hello(name: str = "사용자") -> str:
    """인사를 건네는 함수입니다."""
    return f"안녕하세요, {name}님!"

@mcp.tool()
def calculate_sum(a: int, b: int) -> int:
    """두 숫자의 합을 계산합니다."""
    return a + b

if __name__ == "__main__":
    mcp.run()