# 한국수출입은행 공공 API를 활용한 환율 정보 조회

import requests
import json
import csv
from datetime import datetime
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

def get_exchange_rate():
    """한국수출입은행 API로 환율 정보 조회"""
    
    # 환경 변수에서 API 키 가져오기
    API_KEY = os.getenv("EXIM_API_KEY")
    
    if not API_KEY:
        print("❌ ERROR: EXIM_API_KEY가 .env 파일에 설정되지 않았습니다!")
        print("📝 .env 파일에 다음 내용을 추가하세요:")
        print("EXIM_API_KEY=your_exim_api_key_here")
        return None
    
    # 한국수출입은행 환율 API
    url = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"
    
    # 오늘 날짜 자동 설정
    today = datetime.now().strftime("%Y%m%d")
    
    params = {
        "authkey": API_KEY,  # .env 파일에서 로드
        "searchdate": today,
        "data": "AP01"
    }
    
    try:
        print(f"💱 환율 정보 조회 중... (날짜: {today})")
        response = requests.get(url, params=params)
        response.raise_for_status()  # HTTP 에러 체크
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 환율 데이터 조회 성공! ({len(data)}개 통화)")
            return data
        else:
            print(f"❌ API 요청 실패: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API 요청 오류: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON 파싱 오류: {e}")
        return None
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        return None

def save_to_csv(data, filename=None):
    """환율 데이터를 CSV 파일로 저장"""
    
    if not data:
        print("❌ 저장할 데이터가 없습니다.")
        return False
    
    # 파일명 생성
    if not filename:
        today = datetime.now().strftime("%Y%m%d")
        filename = f"exchange_rate_{today}.csv"
    
    try:
        # CSV 파일로 저장
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = [
                '통화코드', '통화명', '기준환율', '현찰사실때', '현찰파실때', 
                '송금보내실때', '송금받으실때', '조회일자'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # 헤더 작성
            writer.writeheader()
            
            # 데이터 작성
            today_str = datetime.now().strftime("%Y-%m-%d")
            
            for item in data:
                # 데이터 정리
                row_data = {
                    '통화코드': item.get('cur_unit', ''),
                    '통화명': item.get('cur_nm', ''),
                    '기준환율': item.get('deal_bas_r', ''),
                    '현찰사실때': item.get('bkpr', ''),
                    '현찰파실때': item.get('yy_efee_r', ''),
                    '송금보내실때': item.get('ten_dd_efee_r', ''),
                    '송금받으실때': item.get('kftc_deal_bas_r', ''),
                    '조회일자': today_str
                }
                
                writer.writerow(row_data)
        
        print(f"📁 CSV 파일 저장 완료: {filename}")
        print(f"📊 총 {len(data)}개 통화 데이터 저장됨")
        return True
        
    except Exception as e:
        print(f"❌ CSV 저장 실패: {e}")
        return False

def save_major_currencies_csv(data, filename=None):
    """주요 통화만 따로 CSV로 저장"""
    
    if not data:
        return False
    
    # 파일명 생성
    if not filename:
        today = datetime.now().strftime("%Y%m%d")
        filename = f"major_exchange_rate_{today}.csv"
    
    # 주요 통화 필터링
    major_currencies = ["USD", "EUR", "JPY", "CNH", "GBP"]
    major_data = []
    
    for item in data:
        cur_unit = item.get("cur_unit", "")
        currency_code = cur_unit.split("(")[0] if "(" in cur_unit else cur_unit
        
        if currency_code in major_currencies:
            major_data.append(item)
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = [
                '통화코드', '통화명', '기준환율', '전일대비', '조회일시'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for item in major_data:
                # 기준환율에서 쉼표 제거 후 숫자로 변환
                rate = item.get('deal_bas_r', '0').replace(",", "")
                
                row_data = {
                    '통화코드': item.get('cur_unit', ''),
                    '통화명': item.get('cur_nm', ''),
                    '기준환율': f"{float(rate):,.2f}원" if rate != '0' else '정보없음',
                    '전일대비': '정보없음',  # API에서 제공하지 않는 경우
                    '조회일시': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                writer.writerow(row_data)
        
        print(f"📁 주요통화 CSV 파일 저장 완료: {filename}")
        print(f"📊 {len(major_data)}개 주요 통화 저장됨")
        return True
        
    except Exception as e:
        print(f"❌ 주요통화 CSV 저장 실패: {e}")
        return False

def display_exchange_rates(data):
    """환율 정보를 보기 좋게 출력"""
    
    if not data:
        print("❌ 환율 데이터가 없습니다.")
        return
    
    print(f"\n💰 === {datetime.now().strftime('%Y-%m-%d')} 환율 정보 ===")
    print("=" * 50)
    
    # 주요 통화만 필터링
    major_currencies = ["USD", "EUR", "JPY", "CNH", "GBP"]
    
    for item in data:
        cur_unit = item.get("cur_unit", "")
        cur_nm = item.get("cur_nm", "")
        deal_bas_r = item.get("deal_bas_r", "")
        
        # 주요 통화인지 확인
        currency_code = cur_unit.split("(")[0] if "(" in cur_unit else cur_unit
        
        if currency_code in major_currencies and deal_bas_r:
            # 쉼표 제거 후 숫자로 변환
            try:
                rate = float(deal_bas_r.replace(",", ""))
                print(f"🌍 {cur_nm:<15} ({currency_code})")
                print(f"   기준환율: {rate:>10,.2f} 원")
                print("-" * 30)
            except ValueError:
                print(f"🌍 {cur_nm:<15} ({currency_code})")
                print(f"   기준환율: 정보없음")
                print("-" * 30)

def get_specific_currency(data, currency_code):
    """특정 통화의 환율만 조회"""
    
    if not data:
        return None
    
    for item in data:
        cur_unit = item.get("cur_unit", "")
        if currency_code in cur_unit:
            return item
    
    return None

def calculate_exchange(amount, rate, from_currency, to_currency):
    """환전 계산"""
    
    try:
        if from_currency == "KRW":
            # 원화 → 외화
            result = amount / rate
            print(f"💰 {amount:,.0f} 원 → {result:,.2f} {to_currency}")
        else:
            # 외화 → 원화
            result = amount * rate
            print(f"💰 {amount:,.2f} {from_currency} → {result:,.0f} 원")
        
        return result
    except (ValueError, ZeroDivisionError) as e:
        print(f"❌ 환전 계산 오류: {e}")
        return None

def main():
    print("🚀 === 환율 정보 조회 프로그램 ===")
    print("📋 한국수출입은행 공공 API 활용")
    
    # 환율 데이터 조회
    exchange_data = get_exchange_rate()
    
    if exchange_data:
        # 전체 환율 정보 출력
        display_exchange_rates(exchange_data)
        
        # CSV 파일로 저장
        print(f"\n💾 === CSV 파일 저장 ===")
        
        # 전체 데이터 저장
        save_to_csv(exchange_data)
        
        # 주요 통화만 저장
        save_major_currencies_csv(exchange_data)
        
        # 달러 환율 상세 정보
        print(f"\n🇺🇸 === 달러(USD) 상세 정보 ===")
        usd_data = get_specific_currency(exchange_data, "USD")
        
        if usd_data:
            print(f"통화명: {usd_data.get('cur_nm')}")
            print(f"기준환율: {usd_data.get('deal_bas_r')} 원")
            print(f"현찰 사실때: {usd_data.get('bkpr')} 원")
            print(f"현찰 파실때: {usd_data.get('yy_efee_r')} 원")
            print(f"송금 보내실때: {usd_data.get('ten_dd_efee_r')} 원")
            print(f"송금 받으실때: {usd_data.get('kftc_deal_bas_r')} 원")
            
            # 환전 계산 예시
            print(f"\n💹 === 환전 계산 예시 ===")
            try:
                usd_rate = float(usd_data.get('deal_bas_r', '0').replace(",", ""))
                
                if usd_rate > 0:
                    calculate_exchange(100, usd_rate, "USD", "KRW")  # 100달러 → 원
                    calculate_exchange(1000000, usd_rate, "KRW", "USD")  # 100만원 → 달러
            except ValueError:
                print("❌ 달러 환율 정보를 숫자로 변환할 수 없습니다.")
        
        # 유로 환율 정보
        print(f"\n🇪🇺 === 유로(EUR) 정보 ===")
        eur_data = get_specific_currency(exchange_data, "EUR")
        
        if eur_data:
            try:
                eur_rate = float(eur_data.get('deal_bas_r', '0').replace(",", ""))
                print(f"기준환율: {eur_rate:,.2f} 원")
                
                if eur_rate > 0:
                    calculate_exchange(100, eur_rate, "EUR", "KRW")  # 100유로 → 원
            except ValueError:
                print("❌ 유로 환율 정보를 숫자로 변환할 수 없습니다.")
        
        print(f"\n📊 총 {len(exchange_data)}개 통화 정보 조회 완료!")
        
        # 저장된 파일 목록 확인
        today = datetime.now().strftime("%Y%m%d")
        files = [
            f"exchange_rate_{today}.csv",
            f"major_exchange_rate_{today}.csv"
        ]
        
        print(f"\n📁 === 저장된 파일 목록 ===")
        for file in files:
            if os.path.exists(file):
                file_size = os.path.getsize(file)
                print(f"  ✅ {file} ({file_size:,} bytes)")
            else:
                print(f"  ❌ {file} (파일 없음)")
        
        print(f"\n💡 참고사항:")
        print("  - API 키는 .env 파일에서 안전하게 관리됩니다")
        print("  - 환율 정보는 매일 갱신됩니다")
        print("  - CSV 파일은 Excel에서 바로 열어볼 수 있습니다")
        
    else:
        print("❌ 환율 정보를 가져올 수 없습니다.")
        print("💡 API 키를 확인하거나 네트워크 연결을 점검해보세요.")

if __name__ == "__main__":
    main()
