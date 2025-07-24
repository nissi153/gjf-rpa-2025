import requests
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 기상청_단기예보 조회서비스
# https://www.data.go.kr/iim/api/selectAPIAcountView.do

# 환경 변수에서 API 키 가져오기
API_KEY = os.getenv("WEATHER_API_KEY")
url = os.getenv("WEATHER_API_URL", "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst")

if not API_KEY:
    print("❌ ERROR: WEATHER_API_KEY가 .env 파일에 설정되지 않았습니다!")
    exit(1)

params = {
    "serviceKey": API_KEY,
    "pageNo": "1",
    "numOfRows": "10",
    "dataType": "JSON",
    "base_date": "20250725",
    "base_time": "0500",
    "nx": "55",
    "ny": "127"
}

print("🌤️ 기상청 API 호출 중...")
response = requests.get(url, params=params)
print("✅ API 응답:")
print(response.json())
