# 기상청 격자 좌표 변환 및 날씨 정보 조회

import requests
import math
import os
from dotenv import load_dotenv
from datetime import datetime
import json

# .env 파일에서 환경 변수 로드
load_dotenv()

def convert_to_grid(lat, lon):
    """위도/경도를 기상청 격자 좌표로 변환"""
    
    # 기상청 격자 좌표 변환 상수
    RE = 6371.00877    # 지구 반경 (km)
    GRID = 5.0         # 격자 간격 (km)
    SLAT1 = 30.0       # 투영 위도1 (degree)
    SLAT2 = 60.0       # 투영 위도2 (degree)
    OLON = 126.0       # 기준점 경도 (degree)
    OLAT = 38.0        # 기준점 위도 (degree)
    XO = 43            # 기준점 X좌표 (GRID)
    YO = 136           # 기준점 Y좌표 (GRID)
    
    # 도 → 라디안 변환
    DEGRAD = math.pi / 180.0
    
    slat1 = SLAT1 * DEGRAD
    slat2 = SLAT2 * DEGRAD
    olon = OLON * DEGRAD
    olat = OLAT * DEGRAD
    
    sn = math.tan(math.pi * 0.25 + slat2 * 0.5) / math.tan(math.pi * 0.25 + slat1 * 0.5)
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
    sf = math.tan(math.pi * 0.25 + slat1 * 0.5)
    sf = math.pow(sf, sn) * math.cos(slat1) / sn
    ro = math.tan(math.pi * 0.25 + olat * 0.5)
    ro = RE * sf / math.pow(ro, sn)
    
    ra = math.tan(math.pi * 0.25 + lat * DEGRAD * 0.5)
    ra = RE * sf / math.pow(ra, sn)
    theta = lon * DEGRAD - olon
    
    if theta > math.pi:
        theta -= 2.0 * math.pi
    if theta < -math.pi:
        theta += 2.0 * math.pi
    
    theta *= sn
    x = int(ra * math.sin(theta) + XO + 0.5)
    y = int(ro - ra * math.cos(theta) + YO + 0.5)
    
    return x, y

def get_weather_data(nx, ny):
    """격자 좌표로 날씨 정보 조회"""
    
    # 환경 변수에서 API 키 가져오기
    API_KEY = os.getenv("WEATHER_API_KEY")
    url = os.getenv("WEATHER_API_URL", "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst")
    
    if not API_KEY:
        print("❌ ERROR: WEATHER_API_KEY가 .env 파일에 설정되지 않았습니다!")
        return None
    
    # 현재 날짜와 시간 가져오기
    now = datetime.now()
    base_date = now.strftime("%Y%m%d")
    base_time = "0500"  # 05:00 발표 기준
    
    params = {
        "serviceKey": API_KEY,
        "pageNo": "1",
        "numOfRows": "10",
        "dataType": "JSON",
        "base_date": base_date,  # 현재 날짜 자동 설정
        "base_time": base_time,
        "nx": str(nx),
        "ny": str(ny)
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # HTTP 에러 체크
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ API 요청 실패: {e}")
        return None

def parse_weather_data(weather_data, city_name):
    """날씨 데이터를 사람이 읽기 쉽게 파싱"""
    if not weather_data or weather_data.get('response', {}).get('header', {}).get('resultCode') != '00':
        return None
    
    items = weather_data.get('response', {}).get('body', {}).get('items', {}).get('item', [])
    
    # 온도, 강수확률, 하늘상태 등 주요 정보 추출
    weather_info = {
        'city': city_name,
        'temperature': None,
        'precipitation_prob': None,
        'sky_condition': None,
        'wind_speed': None
    }
    
    for item in items:
        category = item.get('category')
        value = item.get('fcstValue')
        
        if category == 'TMP':  # 온도
            weather_info['temperature'] = f"{value}°C"
        elif category == 'POP':  # 강수확률
            weather_info['precipitation_prob'] = f"{value}%"
        elif category == 'SKY':  # 하늘상태
            sky_codes = {'1': '맑음', '3': '구름많음', '4': '흐림'}
            weather_info['sky_condition'] = sky_codes.get(value, value)
        elif category == 'WSD':  # 풍속
            weather_info['wind_speed'] = f"{value}m/s"
    
    return weather_info

# 주요 도시별 격자 좌표
cities = {
    "서울시청": {"lat": 37.5663, "lon": 126.9779, "nx": 60, "ny": 127},
    "부산시청": {"lat": 35.1796, "lon": 129.0756, "nx": 98, "ny": 76},
    "대구시청": {"lat": 35.8714, "lon": 128.6014, "nx": 89, "ny": 90},
    "인천시청": {"lat": 37.4563, "lon": 126.7052, "nx": 55, "ny": 124},
    "광주시청": {"lat": 35.1595, "lon": 126.8526, "nx": 58, "ny": 74},
    "대전시청": {"lat": 36.3504, "lon": 127.3845, "nx": 67, "ny": 100},
    "제주시청": {"lat": 33.4996, "lon": 126.5312, "nx": 52, "ny": 38}
}

def main():
    print("🗺️ === 기상청 격자 좌표 시스템 ===")
    print(f"📅 조회 날짜: {datetime.now().strftime('%Y-%m-%d')}")
    print("\n📍 주요 도시별 격자 좌표:")

    for city, info in cities.items():
        print(f"  {city}: nx={info['nx']}, ny={info['ny']} (위도: {info['lat']}, 경도: {info['lon']})")

    # 좌표 변환 테스트
    print("\n🔄 좌표 변환 테스트:")
    test_lat, test_lon = 37.5663, 126.9779  # 서울시청
    converted_x, converted_y = convert_to_grid(test_lat, test_lon)
    print(f"서울시청 (위도: {test_lat}, 경도: {test_lon})")
    print(f"  → 격자 좌표: nx={converted_x}, ny={converted_y}")

    # 주요 도시 날씨 정보 조회
    print(f"\n🌤️ 주요 도시 현재 날씨 정보:")
    print("=" * 60)
    
    for city_name, coords in list(cities.items())[:3]:  # 처음 3개 도시만
        print(f"\n📍 {city_name}")
        try:
            weather_data = get_weather_data(coords['nx'], coords['ny'])
            
            if weather_data:
                # 상세 JSON 출력 (선택적)
                # print(json.dumps(weather_data, indent=2, ensure_ascii=False))
                
                # 파싱된 날씨 정보 출력
                parsed_weather = parse_weather_data(weather_data, city_name)
                if parsed_weather:
                    print(f"  🌡️ 온도: {parsed_weather['temperature'] or 'N/A'}")
                    print(f"  🌧️ 강수확률: {parsed_weather['precipitation_prob'] or 'N/A'}")
                    print(f"  ☁️ 하늘상태: {parsed_weather['sky_condition'] or 'N/A'}")
                    print(f"  💨 풍속: {parsed_weather['wind_speed'] or 'N/A'}")
                else:
                    print("  ❌ 날씨 정보 파싱 실패")
            else:
                print("  ❌ 날씨 데이터 조회 실패")
                
        except Exception as e:
            print(f"  ❌ 오류 발생: {e}")

    print(f"\n💡 참고사항:")
    print("  - nx, ny는 기상청에서 한국을 격자로 나눈 좌표계")
    print("  - 각 격자는 약 5km × 5km 크기")
    print("  - 정확한 좌표는 기상청 홈페이지에서 확인 가능")
    print("  - API 키는 .env 파일에서 안전하게 관리됨")

if __name__ == "__main__":
    main() 