# ex08.py
# https://www.hankyung.com/globalmarket/news-globalmarket
# 한경글로벌 마켓의 뉴스 기사 타이틀 10개 / image url을 출력하시오.

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def crawl_hankyung_news():
    """한국경제 글로벌마켓 뉴스 크롤링 - XPath 사용"""
    
    # Chrome 설정 (Selenium Manager 사용 - 자동으로 chromedriver 관리)
    options = Options()
    options.add_argument('--headless')  # 브라우저 창 없이 실행
    options.add_argument('--disable-gpu')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # 드라이버 실행 (경로 지정 없이 자동 관리)
    driver = webdriver.Chrome(options=options)

    try:
        print("🚀 한국경제 글로벌마켓 뉴스 크롤링 시작... (XPath 사용)")
        
        # 타겟 URL 접속
        url = 'https://www.hankyung.com/globalmarket/news-globalmarket'
        print(f"📰 접속 중: {url}")
        driver.get(url)
        time.sleep(3)  # 로딩 대기 시간 증가
        
        print(f"✅ 페이지 로딩 완료: {driver.title}")
        
        # 다양한 뉴스 XPath 선택자들 시도
        xpath_selectors = [
            # 기본 뉴스 링크들
            "//ul[@class='list_basic']//li//a",                    # 기존 선택자의 XPath 버전
            "//div[contains(@class, 'news-list')]//a",             # 뉴스 리스트 링크
            "//article//a",                                        # 기사 내 모든 링크
            
            # 제목 기반 선택자들
            "//h3//a",                                             # h3 태그 내 링크
            "//h4//a",                                             # h4 태그 내 링크
            "//h5//a",                                             # h5 태그 내 링크
            
            # 클래스 기반 선택자들
            "//div[contains(@class, 'headline')]//a",              # 헤드라인 클래스
            "//div[contains(@class, 'title')]//a",                 # 제목 클래스
            "//span[contains(@class, 'title')]//a",                # span 제목 클래스
            "//p[contains(@class, 'title')]//a",                   # p 제목 클래스
            
            # href 속성 기반 선택자들 (더 정확한 뉴스 링크)
            "//a[contains(@href, '/article/')]",                   # article 포함 링크
            "//a[contains(@href, '/news/')]",                      # news 포함 링크
            "//a[contains(@href, 'hankyung.com')]",               # 한경 도메인 링크
            
            # 텍스트 길이 기반 선택자들
            "//a[string-length(text()) > 10]",                    # 10자 이상 텍스트 링크
            "//a[string-length(normalize-space(text())) > 5]",    # 5자 이상 정규화된 텍스트
            
            # 복합 조건 선택자들
            "//a[contains(@href, 'article') and string-length(text()) > 5]",  # article URL + 긴 텍스트
            "//div[contains(@class, 'news') or contains(@class, 'article')]//a",  # 뉴스/기사 클래스 하위
            
            # 상위 요소 기반 선택자들
            "//li//a[contains(@href, 'article')]",                # li 하위의 article 링크
            "//section//a[contains(@href, 'article')]",           # section 하위의 article 링크
            "//main//a[contains(@href, 'article')]",              # main 하위의 article 링크
        ]
        
        news_found = False
        all_links = []
        
        for i, xpath in enumerate(xpath_selectors):
            try:
                print(f"🔍 XPath {i+1} 시도: {xpath}")
                news_items = driver.find_elements(By.XPATH, xpath)
                print(f"   → {len(news_items)}개 요소 발견")
                
                if news_items:
                    all_links.extend(news_items)
                    
                    # 처음 몇 개 링크 정보 미리보기
                    if i < 3 and len(news_items) > 0:
                        print(f"   📝 샘플: {news_items[0].text[:30]}...")
                    
            except Exception as e:
                print(f"   ❌ XPath 실패: {str(e)[:50]}...")
                
        # 중복 제거 및 유효성 검증
        seen_urls = set()
        unique_links = []
        
        print(f"🔄 중복 제거 및 유효성 검증 중...")
        
        for link in all_links:
            try:
                href = link.get_attribute('href')
                text = link.text.strip()
                
                # 더 엄격한 유효성 검사
                if (href and 
                    href not in seen_urls and 
                    text and 
                    len(text) > 3 and
                    ('hankyung.com' in href or 'article' in href)):
                    
                    seen_urls.add(href)
                    unique_links.append(link)
                    
            except Exception as e:
                continue
                
        print(f"📊 총 {len(unique_links)}개 고유 유효 링크 발견")
        
        # 뉴스 정보 추출 및 출력
        news_count = 0
        print(f"\n{'='*80}")
        print(f"🗞️  수집된 뉴스 목록 (XPath 사용)")
        print(f"{'='*80}")
        
        for i, item in enumerate(unique_links[:15]):  # 상위 15개
            try:
                title = item.text.strip()
                link = item.get_attribute('href')
                
                # 최종 뉴스 필터링
                if (title and link and 
                    len(title) > 5 and 
                    any(keyword in link for keyword in ['article', 'news', 'hankyung'])):
                    
                    news_count += 1
                    
                    # 제목 정리 (불필요한 공백 제거)
                    cleaned_title = ' '.join(title.split())
                    
                    print(f"\n📰 [{news_count:2d}] {cleaned_title}")
                    print(f"🔗 {link}")
                    print(f"📏 제목 길이: {len(cleaned_title)}자")
                    print("-" * 80)
                    
                    news_found = True
                    
                    if news_count >= 12:  # 최대 12개까지
                        break
                        
            except Exception as e:
                print(f"⚠️ 링크 처리 실패 [{i+1}]: {str(e)[:50]}...")
                continue
        
        if not news_found:
            print("❌ XPath로 뉴스를 찾을 수 없습니다.")
            print("🔍 페이지 구조 분석을 위한 정보:")
            
            # 페이지의 모든 링크 개수 확인
            all_a_tags = driver.find_elements(By.XPATH, "//a")
            print(f"   📊 페이지 내 전체 <a> 태그: {len(all_a_tags)}개")
            
            # href 속성이 있는 링크 개수
            links_with_href = driver.find_elements(By.XPATH, "//a[@href]")
            print(f"   🔗 href 속성이 있는 링크: {len(links_with_href)}개")
            
            # 텍스트가 있는 링크 개수  
            links_with_text = driver.find_elements(By.XPATH, "//a[text()]")
            print(f"   📝 텍스트가 있는 링크: {len(links_with_text)}개")
            
        return news_count
        
    except Exception as e:
        print(f"❌ 크롤링 중 심각한 오류 발생: {e}")
        return 0
        
    finally:
        # 드라이버 종료
        driver.quit()
        print(f"\n✅ 드라이버 종료 완료")

if __name__ == "__main__":
    print("🎯 XPath를 활용한 한국경제 뉴스 크롤링 시작!")
    print("="*80)
    
    count = crawl_hankyung_news()
    
    print("="*80)
    print(f"🎉 크롤링 완료! 총 {count}개의 뉴스를 성공적으로 수집했습니다!")
    
    if count > 0:
        print("💡 XPath 선택자가 성공적으로 작동했습니다!")
    else:
        print("⚠️ 뉴스 수집에 실패했습니다. 페이지 구조를 다시 확인해보세요.")