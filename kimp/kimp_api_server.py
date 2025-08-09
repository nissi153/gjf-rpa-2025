# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
import json
import os
from typing import Optional, List
from datetime import datetime

# KimchiPremiumCalculator 클래스를 직접 포함
class KimchiPremiumCalculator:
    def __init__(self):
        self.usd_krw_rate = None
        self.data = []
        
    def get_exchange_rate(self):
        """USD/KRW 환율 가져오기"""
        try:
            url = "https://api.exchangerate-api.com/v4/latest/USD"
            response = requests.get(url, timeout=10)
            data = response.json()
            self.usd_krw_rate = data['rates']['KRW']
            return self.usd_krw_rate
        except Exception as e:
            print(f"환율 조회 오류: {e}")
            self.usd_krw_rate = 1300
            return self.usd_krw_rate
    
    def get_binance_prices(self, symbols):
        """바이낸스 가격 가져오기"""
        try:
            url = "https://api.binance.com/api/v3/ticker/24hr"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            binance_prices = {}
            for item in data:
                symbol = item['symbol']
                if symbol in symbols:
                    binance_prices[symbol] = {
                        'price': float(item['lastPrice']),
                        'change_24h': float(item['priceChangePercent'])
                    }
            
            return binance_prices
        except Exception as e:
            print(f"바이낸스 가격 조회 오류: {e}")
            return {}
    
    def get_upbit_markets(self):
        """업비트 마켓 정보 가져오기"""
        try:
            url = "https://api.upbit.com/v1/market/all"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                markets = response.json()
                krw_markets = [m['market'] for m in markets if m['market'].startswith('KRW-')]
                return krw_markets
            return []
        except Exception as e:
            print(f"업비트 마켓 조회 오류: {e}")
            return []

    def get_upbit_prices(self, markets):
        """업비트 가격 가져오기"""
        try:
            markets_str = ','.join(markets)
            url = f"https://api.upbit.com/v1/ticker?markets={markets_str}"
            
            headers = {'Accept': 'application/json'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                return {}
            
            data = response.json()
            
            if not isinstance(data, list):
                return {}
            
            upbit_prices = {}
            for item in data:
                if isinstance(item, dict) and 'market' in item and 'trade_price' in item:
                    market = item['market']
                    upbit_prices[market] = {
                        'price': float(item['trade_price']),
                        'change_24h': float(item.get('signed_change_rate', 0)) * 100
                    }
            
            return upbit_prices
        except Exception as e:
            print(f"업비트 가격 조회 오류: {e}")
            return {}
    
    def calculate_kimchi_premium(self):
        """김치 프리미엄 계산"""
        crypto_pairs = {
            'BTCUSDT': 'KRW-BTC',
            'ETHUSDT': 'KRW-ETH',
            'XRPUSDT': 'KRW-XRP',
            'ADAUSDT': 'KRW-ADA',
            'SOLUSDT': 'KRW-SOL',
            'AVAXUSDT': 'KRW-AVAX',
            'MATICUSDT': 'KRW-MATIC',
            'LINKUSDT': 'KRW-LINK',
            'DOTUSDT': 'KRW-DOT',
            'ATOMUSDT': 'KRW-ATOM'
        }
        
        # 환율 가져오기
        self.get_exchange_rate()
        
        # 업비트 마켓 확인
        available_markets = self.get_upbit_markets()
        
        # 실제 존재하는 마켓만 필터링
        filtered_pairs = {}
        for binance_symbol, upbit_market in crypto_pairs.items():
            if upbit_market in available_markets:
                filtered_pairs[binance_symbol] = upbit_market
        
        # 바이낸스 가격 가져오기
        binance_symbols = list(filtered_pairs.keys())
        binance_prices = self.get_binance_prices(binance_symbols)
        
        # 업비트 가격 가져오기
        upbit_markets = list(filtered_pairs.values())
        upbit_prices = self.get_upbit_prices(upbit_markets)
        
        # 김치 프리미엄 계산
        self.data = []
        
        for binance_symbol, upbit_market in filtered_pairs.items():
            if binance_symbol in binance_prices and upbit_market in upbit_prices:
                # 바이낸스 USD 가격을 KRW로 변환
                binance_usd = binance_prices[binance_symbol]['price']
                binance_krw = binance_usd * self.usd_krw_rate
                
                # 업비트 KRW 가격
                upbit_krw = upbit_prices[upbit_market]['price']
                
                # 김치 프리미엄 계산
                kimp_rate = ((upbit_krw - binance_krw) / binance_krw) * 100
                
                # 코인 이름 추출
                crypto_name = binance_symbol.replace('USDT', '')
                
                crypto_data = {
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'crypto_name': crypto_name,
                    'binance_usd': binance_usd,
                    'binance_krw': binance_krw,
                    'upbit_krw': upbit_krw,
                    'kimp_rate': round(kimp_rate, 2),
                    'binance_change_24h': binance_prices[binance_symbol]['change_24h'],
                    'upbit_change_24h': upbit_prices[upbit_market]['change_24h'],
                    'usd_krw_rate': self.usd_krw_rate
                }
                
                self.data.append(crypto_data)
        
        # 김치 프리미엄 기준으로 정렬 (높은 순)
        self.data.sort(key=lambda x: x['kimp_rate'], reverse=True)
        
        return self.data

# Pydantic 모델
class CryptoData(BaseModel):
    timestamp: str
    crypto_name: str
    binance_usd: float
    binance_krw: float
    upbit_krw: float
    kimp_rate: float
    binance_change_24h: float
    upbit_change_24h: float
    usd_krw_rate: float

class KimpResponse(BaseModel):
    count: int
    exchange_rate: float
    timestamp: str
    data: List[CryptoData]

# FastAPI 앱 초기화
app = FastAPI(
    title="Kimchi Premium API Server",
    description="실시간 바이낸스-업비트 김치 프리미엄 계산 API",
    version="2.0.0"
)

# 전역 calculator 인스턴스
calculator = KimchiPremiumCalculator()

@app.get("/")
async def root():
    """루트 엔드포인트 - API 정보"""
    return {
        "message": "Kimchi Premium API Server",
        "version": "2.0.0",
        "description": "바이낸스-업비트 실시간 김치 프리미엄 계산",
        "endpoints": {
            "/kimp": "전체 김치 프리미엄 데이터",
            "/kimp/{symbol}": "특정 코인 김치 프리미엄",
            "/kimp/top/{n}": "상위 N개 김치 프리미엄",
            "/kimp/negative": "음수 김치 프리미엄 코인들",
            "/exchange-rate": "현재 USD/KRW 환율"
        }
    }

@app.get("/kimp", response_model=KimpResponse)
async def get_all_kimp():
    """전체 김치 프리미엄 데이터 조회"""
    try:
        data = calculator.calculate_kimchi_premium()
        
        if not data:
            raise HTTPException(status_code=500, detail="데이터를 가져올 수 없습니다")
        
        return KimpResponse(
            count=len(data),
            exchange_rate=calculator.usd_krw_rate,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            data=data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")

@app.get("/kimp/{symbol}")
async def get_kimp_by_symbol(symbol: str):
    """특정 코인의 김치 프리미엄 조회"""
    try:
        symbol = symbol.upper()
        data = calculator.calculate_kimchi_premium()
        
        if not data:
            raise HTTPException(status_code=500, detail="데이터를 가져올 수 없습니다")
        
        for crypto in data:
            if crypto['crypto_name'].upper() == symbol:
                return {
                    "symbol": symbol,
                    "exchange_rate": calculator.usd_krw_rate,
                    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "data": crypto
                }
        
        available_symbols = [crypto['crypto_name'] for crypto in data]
        raise HTTPException(
            status_code=404,
            detail=f"코인 '{symbol}'을 찾을 수 없습니다. 사용 가능한 코인: {available_symbols}"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")

@app.get("/kimp/top/{n}")
async def get_top_kimp(n: int = 5):
    """상위 N개 김치 프리미엄 조회"""
    try:
        if n <= 0 or n > 50:
            raise HTTPException(status_code=400, detail="n은 1-50 사이의 값이어야 합니다")
        
        data = calculator.calculate_kimchi_premium()
        
        if not data:
            raise HTTPException(status_code=500, detail="데이터를 가져올 수 없습니다")
        
        top_data = data[:n]
        
        return {
            "count": len(top_data),
            "top_n": n,
            "exchange_rate": calculator.usd_krw_rate,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "data": top_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")

@app.get("/kimp/negative")
async def get_negative_kimp():
    """음수 김치 프리미엄 코인들 조회"""
    try:
        data = calculator.calculate_kimchi_premium()
        
        if not data:
            raise HTTPException(status_code=500, detail="데이터를 가져올 수 없습니다")
        
        negative_data = [item for item in data if item['kimp_rate'] < 0]
        
        return {
            "count": len(negative_data),
            "exchange_rate": calculator.usd_krw_rate,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "data": negative_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")

@app.get("/exchange-rate")
async def get_exchange_rate():
    """현재 USD/KRW 환율 조회"""
    try:
        rate = calculator.get_exchange_rate()
        return {
            "usd_krw": rate,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"환율 조회 오류: {str(e)}")

@app.get("/symbols")
async def get_available_symbols():
    """사용 가능한 코인 심볼 목록"""
    try:
        data = calculator.calculate_kimchi_premium()
        
        if not data:
            raise HTTPException(status_code=500, detail="데이터를 가져올 수 없습니다")
        
        symbols = [crypto['crypto_name'] for crypto in data]
        
        return {
            "count": len(symbols),
            "symbols": symbols,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)