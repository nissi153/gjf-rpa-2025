import streamlit as st
import pandas as pd
import time
import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import urllib.parse

# Streamlit 페이지 설정
st.set_page_config(
    page_title="연합뉴스 기사 스크래퍼",
    page_icon="📰",
    layout="wide"
)

st.title("📰 연합뉴스 기사 스크래퍼")
st.markdown("AI, 환율, 나스닥 관련 뉴스를 자동으로 수집하고 요약합니다.")

class YonhapNewsScraper:
    def __init__(self):
        self.base_url = "https://www.yna.co.kr"
        self.search_url = "https://www.yna.co.kr/search"
        self.rss_url = "https://www.yna.co.kr/rss/all.xml"
        self.naver_api_url = "https://openapi.naver.com/v1/search/news.json"
    
    def search_news_from_rss(self, keyword, max_articles=10):
        """RSS 피드에서 키워드 관련 뉴스 검색"""
        articles = []
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(self.rss_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item')
            
            for item in items:
                try:
                    title = item.find('title').text.strip()
                    link = item.find('link').text.strip()
                    pub_date = item.find('pubDate').text.strip() if item.find('pubDate') else datetime.now().strftime('%Y-%m-%d')
                    description = item.find('description').text.strip() if item.find('description') else f"{keyword} 관련 뉴스"
                    
                    # 키워드가 제목이나 설명에 포함되어 있는지 확인
                    if keyword.lower() in title.lower() or keyword.lower() in description.lower():
                        articles.append({
                            'keyword': keyword,
                            'date': pub_date,
                            'title': title,
                            'url': link,
                            'summary': description[:200] + "..." if len(description) > 200 else description
                        })
                        
                        if len(articles) >= max_articles:
                            break
                            
                except Exception as e:
                    continue
                    
        except Exception as e:
            st.warning(f"RSS 피드에서 '{keyword}' 검색 중 오류: {e}")
            
        return articles
    
    def search_news_from_google(self, keyword, max_articles=10):
        """구글 뉴스에서 연합뉴스 기사 검색"""
        articles = []
        
        try:
            # 구글 뉴스 검색 URL (연합뉴스 사이트 한정)
            query = f"{keyword} site:yna.co.kr"
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&tbm=nws"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 구글 뉴스 결과 파싱
            news_results = soup.find_all('div', class_='SoaBEf')
            
            for result in news_results[:max_articles]:
                try:
                    title_element = result.find('div', class_='MBeuO')
                    if title_element:
                        title = title_element.get_text().strip()
                        
                        link_element = result.find('a')
                        link = link_element.get('href') if link_element else ""
                        
                        date_element = result.find('span', class_='r0bn4c')
                        date_text = date_element.get_text().strip() if date_element else datetime.now().strftime('%Y-%m-%d')
                        
                        summary_element = result.find('div', class_='GI74Re')
                        summary = summary_element.get_text().strip() if summary_element else f"{keyword} 관련 뉴스"
                        
                        if title and 'yna.co.kr' in link:
                            articles.append({
                                'keyword': keyword,
                                'date': date_text,
                                'title': title,
                                'url': link,
                                'summary': summary[:200] + "..." if len(summary) > 200 else summary
                            })
                            
                except Exception as e:
                    continue
                    
        except Exception as e:
            st.warning(f"구글 뉴스에서 '{keyword}' 검색 중 오류: {e}")
            
        return articles
    
    def search_news(self, keyword, max_articles=10):
        """키워드로 뉴스 검색 (여러 방법 시도)"""
        articles = []
        
        # 방법 1: RSS 피드에서 검색
        st.info(f"RSS 피드에서 '{keyword}' 검색 중...")
        rss_articles = self.search_news_from_rss(keyword, max_articles)
        articles.extend(rss_articles)
        
        # 방법 2: 구글 뉴스에서 검색 (RSS에서 충분하지 않은 경우)
        if len(articles) < max_articles:
            st.info(f"구글 뉴스에서 '{keyword}' 추가 검색 중...")
            remaining = max_articles - len(articles)
            google_articles = self.search_news_from_google(keyword, remaining)
            articles.extend(google_articles)
        
        # 방법 3: 직접 연합뉴스 사이트 검색 (마지막 시도)
        if len(articles) < max_articles:
            st.info(f"연합뉴스 사이트에서 '{keyword}' 직접 검색 중...")
            remaining = max_articles - len(articles)
            direct_articles = self.search_news_direct(keyword, remaining)
            articles.extend(direct_articles)
        
        return articles[:max_articles]
    
    def search_news_direct(self, keyword, max_articles=10):
        """연합뉴스 사이트에서 직접 검색"""
        articles = []
        
        try:
            # 검색 URL 구성
            search_url = f"{self.search_url}?query={urllib.parse.quote(keyword)}&sort=date"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            # 세션 사용으로 연결 유지
            session = requests.Session()
            session.headers.update(headers)
            
            response = session.get(search_url, timeout=20)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 다양한 선택자로 기사 찾기
            selectors_to_try = [
                'div.list-type038 li',
                'div.news-list li', 
                'ul.list-basic li',
                'div.search-result-item',
                'article',
                '.item'
            ]
            
            article_elements = []
            for selector in selectors_to_try:
                article_elements = soup.select(selector)
                if article_elements:
                    break
            
            # 기사가 없으면 모든 링크에서 찾기
            if not article_elements:
                all_links = soup.find_all('a', href=True)
                count = 0
                for link in all_links:
                    href = link.get('href', '')
                    text = link.get_text().strip()
                    
                    if ('/view/' in href or '/news/' in href) and len(text) > 15:
                        if keyword.lower() in text.lower():
                            full_url = href if href.startswith('http') else self.base_url + href
                            articles.append({
                                'keyword': keyword,
                                'date': datetime.now().strftime('%Y-%m-%d'),
                                'title': text,
                                'url': full_url,
                                'summary': f"{keyword} 관련 연합뉴스"
                            })
                            count += 1
                            if count >= max_articles:
                                break
                return articles
            
            # 기사 정보 추출
            for element in article_elements[:max_articles]:
                try:
                    # 제목과 링크
                    title_element = element.select_one('a[href*="/view/"], a[href*="/news/"], .tit-wrap a, a')
                    if not title_element:
                        continue
                        
                    title = title_element.get_text().strip()
                    link = title_element.get('href', '')
                    
                    if not title or len(title) < 10:
                        continue
                    
                    # URL 완성
                    if link and not link.startswith('http'):
                        link = self.base_url + link
                    
                    # 날짜
                    date_text = datetime.now().strftime('%Y-%m-%d')
                    date_selectors = ['.info-text01', '.date', '.time', 'time', '.news-date']
                    for selector in date_selectors:
                        date_element = element.select_one(selector)
                        if date_element:
                            date_text = date_element.get_text().strip()
                            break
                    
                    # 요약
                    summary = f"{keyword} 관련 연합뉴스"
                    summary_selectors = ['.lead', '.summary', '.desc', 'p', '.news-summary']
                    for selector in summary_selectors:
                        summary_element = element.select_one(selector)
                        if summary_element:
                            summary_text = summary_element.get_text().strip()
                            if summary_text and len(summary_text) > 10:
                                summary = summary_text[:200] + "..." if len(summary_text) > 200 else summary_text
                                break
                    
                    articles.append({
                        'keyword': keyword,
                        'date': date_text,
                        'title': title,
                        'url': link,
                        'summary': summary
                    })
                    
                except Exception as e:
                    continue
                    
        except requests.exceptions.Timeout:
            st.warning(f"'{keyword}' 검색 요청이 시간 초과되었습니다.")
        except requests.exceptions.RequestException as e:
            st.warning(f"'{keyword}' 검색 중 네트워크 오류가 발생했습니다.")
        except Exception as e:
            st.warning(f"'{keyword}' 검색 중 오류가 발생했습니다.")
            
        return articles
    
    def get_article_content(self, url):
        """기사 본문 내용 가져오기 (상세 요약용)"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 기사 본문 추출
            content_div = soup.find('div', class_='story-news-article')
            if content_div:
                paragraphs = content_div.find_all('p')
                content = ' '.join([p.get_text().strip() for p in paragraphs])
                return content[:500] + "..." if len(content) > 500 else content
            
            return "본문 내용을 가져올 수 없습니다."
            
        except Exception as e:
            return f"본문 로딩 실패: {str(e)}"

# 메인 앱
def main():
    scraper = YonhapNewsScraper()
    
    # 사이드바 설정
    st.sidebar.header("검색 설정")
    
    # 키워드 선택
    keywords = st.sidebar.multiselect(
        "검색할 키워드를 선택하세요:",
        ["AI", "환율", "나스닥"],
        default=["AI", "환율", "나스닥"]
    )
    
    # 기사 수 설정
    max_articles = st.sidebar.slider("키워드당 최대 기사 수", 5, 20, 10)
    
    # 검색 버튼
    if st.sidebar.button("🔍 뉴스 검색 시작", type="primary"):
        if not keywords:
            st.warning("최소 하나의 키워드를 선택해주세요.")
            return
        
        all_articles = []
        
        # 진행 상황 표시
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, keyword in enumerate(keywords):
            status_text.text(f"'{keyword}' 관련 뉴스를 검색 중...")
            
            articles = scraper.search_news(keyword, max_articles)
            all_articles.extend(articles)
            
            progress_bar.progress((i + 1) / len(keywords))
            time.sleep(1)  # 서버 부하 방지
        
        status_text.text("검색 완료!")
        
        if all_articles:
            # 결과를 DataFrame으로 변환
            df = pd.DataFrame(all_articles)
            
            # 결과 표시
            st.success(f"총 {len(all_articles)}개의 기사를 찾았습니다!")
            
            # 키워드별 통계
            st.subheader("📊 키워드별 기사 수")
            keyword_counts = df['keyword'].value_counts()
            st.bar_chart(keyword_counts)
            
            # 기사 목록 표시
            st.subheader("📰 검색된 기사 목록")
            
            for keyword in keywords:
                keyword_articles = df[df['keyword'] == keyword]
                if not keyword_articles.empty:
                    st.markdown(f"### 🔍 '{keyword}' 관련 기사 ({len(keyword_articles)}개)")
                    
                    for idx, article in keyword_articles.iterrows():
                        with st.expander(f"📄 {article['title'][:50]}..."):
                            col1, col2 = st.columns([1, 3])
                            
                            with col1:
                                st.write("**날짜:**", article['date'])
                                st.write("**키워드:**", article['keyword'])
                            
                            with col2:
                                st.write("**제목:**", article['title'])
                                st.write("**요약:**", article['summary'])
                                st.write("**링크:**", article['url'])
            
            # CSV 다운로드 기능
            st.subheader("💾 데이터 다운로드")
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 CSV 파일로 다운로드",
                data=csv,
                file_name=f"yonhap_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
        else:
            st.warning("검색된 기사가 없습니다. 다른 키워드를 시도해보세요.")

if __name__ == "__main__":
    main()