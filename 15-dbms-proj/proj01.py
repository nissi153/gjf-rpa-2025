from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
import time
import re
import logging
from datetime import datetime

# 김홍은 수강생 결과물 

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DaumNewsCrawlerVisual:
    def __init__(self):
        self.base_url = "https://news.daum.net"
        self.driver = None
        self.setup_driver()
        
    def setup_driver(self):
        """크롬 드라이버 설정"""
        chrome_options = Options()
        # 브라우저를 시각적으로 보여주기 위해 headless 모드 비활성화
        # chrome_options.add_argument("--headless")  # 주석 처리하여 브라우저 표시
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("크롬 브라우저가 성공적으로 시작되었습니다.")
        except Exception as e:
            logger.error(f"크롬 드라이버 설정 실패: {e}")
            logger.info("ChromeDriver가 설치되어 있는지 확인해주세요.")
            raise
        
    def search_ai_news_visual(self, max_articles=15):
        """시각적으로 AI 키워드 뉴스 검색"""
        news_list = []
        
        try:
            # 1. 다음 뉴스 사이트 접속
            logger.info("🌐 다음 뉴스 사이트에 접속 중...")
            self.driver.get(self.base_url)
            time.sleep(3)
            
            # 2. 검색 버튼 찾기 및 클릭
            logger.info("🔍 검색 버튼을 찾는 중...")
            try:
                # 다양한 검색 버튼 선택자 시도
                search_selectors = [
                    "a[href*='search']",
                    ".link_search",
                    ".btn_search",
                    "button[type='submit']"
                ]
                
                search_element = None
                for selector in search_selectors:
                    try:
                        search_element = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                        break
                    except:
                        continue
                
                if not search_element:
                    # 직접 검색 페이지로 이동
                    logger.info("🔍 검색 페이지로 직접 이동...")
                    search_url = "https://search.daum.net/search?w=news&q=AI"
                    self.driver.get(search_url)
                else:
                    search_element.click()
                    time.sleep(2)
                    
                    # 검색어 입력
                    logger.info("⌨️ 'AI' 키워드 입력 중...")
                    search_input = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='q'], input[type='search'], .tf_keyword"))
                    )
                    search_input.clear()
                    search_input.send_keys("AI")
                    search_input.send_keys(Keys.RETURN)
                    
            except Exception as e:
                logger.info("🔍 검색 페이지로 직접 이동...")
                search_url = "https://search.daum.net/search?w=news&q=AI"
                self.driver.get(search_url)
            
            time.sleep(3)
            
            # 3. 뉴스 탭 클릭 (필요한 경우)
            try:
                news_tab = self.driver.find_element(By.CSS_SELECTOR, "a[href*='w=news'], .tab_news")
                if news_tab:
                    logger.info("📰 뉴스 탭 클릭...")
                    news_tab.click()
                    time.sleep(2)
            except:
                pass
            
            # 4. 뉴스 기사 목록 추출
            logger.info("📋 뉴스 기사 목록 추출 중...")
            
            # 페이지 스크롤하여 더 많은 결과 로드
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # BeautifulSoup으로 파싱
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # 다양한 뉴스 아이템 선택자 시도
            news_selectors = [
                '.c-item-doc',
                '.item-title',
                '.news-item',
                '.c-doc',
                'div[data-tiara-layer="news"]'
            ]
            
            news_items = []
            for selector in news_selectors:
                items = soup.select(selector)
                if items:
                    news_items = items
                    logger.info(f"✅ {len(items)}개의 뉴스 아이템을 '{selector}' 선택자로 찾았습니다.")
                    break
            
            if not news_items:
                # 모든 링크에서 뉴스 관련 항목 찾기
                all_links = soup.find_all('a', href=True)
                for link in all_links:
                    title = link.get_text(strip=True)
                    url = link.get('href')
                    if title and url and 'AI' in title.upper() and len(title) > 10:
                        if not url.startswith('http'):
                            url = f"https:{url}" if url.startswith('//') else f"https://search.daum.net{url}"
                        news_items.append(link)
            
            # 5. 각 뉴스 아이템에서 정보 추출
            for i, item in enumerate(news_items[:max_articles]):
                try:
                    # 제목과 링크 추출
                    title_element = item.find('a') if item.name != 'a' else item
                    if not title_element:
                        continue
                    
                    title = title_element.get_text(strip=True)
                    url = title_element.get('href')
                    
                    if not title or not url or len(title) < 5:
                        continue
                    
                    # URL 정리
                    if not url.startswith('http'):
                        if url.startswith('//'):
                            url = f"https:{url}"
                        elif url.startswith('/'):
                            url = f"https://search.daum.net{url}"
                        else:
                            continue
                    
                    # AI 키워드 포함 확인
                    if 'AI' in title.upper() or '인공지능' in title:
                        news_list.append({
                            'title': title,
                            'url': url
                        })
                        logger.info(f"📄 {len(news_list)}. {title[:50]}...")
                        
                        # 시각적 효과를 위한 딜레이
                        time.sleep(0.5)
                        
                except Exception as e:
                    logger.warning(f"뉴스 아이템 처리 중 오류: {e}")
                    continue
            
            logger.info(f"✅ 총 {len(news_list)}개의 AI 관련 뉴스를 찾았습니다.")
            
        except Exception as e:
            logger.error(f"뉴스 검색 중 오류 발생: {e}")
        
        return news_list
    
    def get_article_content_and_date_visual(self, url):
        """시각적으로 개별 기사 내용과 날짜 추출"""
        try:
            logger.info(f"📖 기사 내용 추출 중: {url[:50]}...")
            
            # 새 탭에서 기사 열기
            self.driver.execute_script(f"window.open('{url}', '_blank');")
            self.driver.switch_to.window(self.driver.window_handles[-1])
            
            time.sleep(2)
            
            # 페이지 소스 가져오기
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # 기사 날짜 추출
            date_selectors = [
                'span.num_date',
                'span.date',
                'time',
                'span.txt_date',
                'div.date_area span',
                'span.info_date',
                '.date',
                '.txt_info'
            ]
            
            article_date = ""
            for selector in date_selectors:
                date_element = soup.select_one(selector)
                if date_element:
                    date_text = date_element.get_text(strip=True)
                    date_match = re.search(r'(\d{4}[.\-/]\d{1,2}[.\-/]\d{1,2})', date_text)
                    if date_match:
                        article_date = date_match.group(1).replace('-', '.').replace('/', '.')
                        break
            
            if not article_date:
                article_date = datetime.now().strftime("%Y.%m.%d")
            
            # 기사 본문 추출
            content_selectors = [
                'div.article_view',
                'div.news_view',
                'div.view_content',
                'div#harmonyContainer',
                'div.news_body',
                'div.article-body',
                '.article_txt',
                '.news_txt'
            ]
            
            content = ""
            for selector in content_selectors:
                content_div = soup.select_one(selector)
                if content_div:
                    for tag in content_div.find_all(['script', 'style', 'iframe', 'ins']):
                        tag.decompose()
                    content = content_div.get_text(strip=True)
                    break
            
            if not content:
                content = soup.get_text()
                content = re.sub(r'\s+', ' ', content).strip()
            
            # 탭 닫기
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            
            return content[:1000] if content else "내용을 가져올 수 없습니다.", article_date
            
        except Exception as e:
            logger.warning(f"기사 내용 추출 실패: {e}")
            try:
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
            except:
                pass
            return "내용을 가져올 수 없습니다.", datetime.now().strftime("%Y.%m.%d")
    
    def extract_summary_and_keywords(self, title, content):
        """간단한 요약과 키워드 추출"""
        # 간단한 요약 (첫 200자)
        summary = content[:200] + "..." if len(content) > 200 else content
        
        # 키워드 추출 (AI 관련 키워드 찾기)
        ai_keywords = ['AI', '인공지능', '머신러닝', '딥러닝', '챗GPT', 'ChatGPT', 
                      '로봇', '자동화', '빅데이터', '알고리즘', '신경망']
        
        found_keywords = []
        text_upper = (title + " " + content).upper()
        
        for keyword in ai_keywords:
            if keyword.upper() in text_upper:
                found_keywords.append(keyword)
        
        return summary, ", ".join(found_keywords) if found_keywords else "AI"
    
    def crawl_and_save_visual(self, filename="ai_news_visual.csv", max_articles=15):
        """시각적 뉴스 크롤링 및 CSV 저장"""
        logger.info("🚀 시각적 AI 뉴스 크롤링 시작...")
        
        try:
            # 뉴스 검색
            news_list = self.search_ai_news_visual(max_articles)
            
            if not news_list:
                logger.warning("❌ 검색된 뉴스가 없습니다.")
                return
            
            # 중복 제거
            unique_news = []
            seen_urls = set()
            
            for news in news_list:
                if news['url'] not in seen_urls:
                    unique_news.append(news)
                    seen_urls.add(news['url'])
            
            logger.info(f"✅ 총 {len(unique_news)}개의 고유한 뉴스를 찾았습니다.")
            
            # CSV 파일 생성
            logger.info("📊 CSV 파일 생성 중...")
            with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ['번호', '제목', 'URL', '날짜', '요약', '키워드']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for i, news in enumerate(unique_news, 1):
                    logger.info(f"📝 기사 {i}/{len(unique_news)} 처리 중...")
                    
                    # 기사 내용과 날짜 가져오기
                    content, article_date = self.get_article_content_and_date_visual(news['url'])
                    
                    # 요약과 키워드 추출
                    summary, keywords = self.extract_summary_and_keywords(news['title'], content)
                    
                    # CSV에 쓰기
                    writer.writerow({
                        '번호': i,
                        '제목': news['title'],
                        'URL': news['url'],
                        '날짜': article_date,
                        '요약': summary,
                        '키워드': keywords
                    })
                    
                    logger.info(f"✅ 완료: {news['title'][:30]}...")
                    time.sleep(1)  # 시각적 효과를 위한 딜레이
            
            logger.info(f"🎉 크롤링 완료! {filename} 파일이 생성되었습니다.")
            
        finally:
            self.close_driver()
    
    def close_driver(self):
        """브라우저 드라이버 종료"""
        if self.driver:
            logger.info("🔚 브라우저를 종료합니다...")
            time.sleep(2)  # 사용자가 결과를 볼 수 있도록 잠시 대기
            self.driver.quit()
            logger.info("✅ 브라우저가 종료되었습니다.")

def main():
    print("🤖 AI 뉴스 크롤러 - 시각적 버전")
    print("=" * 50)
    
    crawler = DaumNewsCrawlerVisual()
    try:
        crawler.crawl_and_save_visual("ai_news_visual.csv", max_articles=10)
    except Exception as e:
        logger.error(f"크롤링 중 오류 발생: {e}")
        crawler.close_driver()

if __name__ == "__main__":
    main()