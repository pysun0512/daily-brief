"""
네이버 뉴스 섹션별 랭킹 수집
- 경제, 정치, IT/과학 섹션
- 각 섹션별 Top 5
"""
import requests
from bs4 import BeautifulSoup
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

# 네이버 뉴스 섹션 ID
SECTIONS = {
    "경제": "101",
    "정치": "100",
    "IT/과학": "105",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

def collect_section(name, section_id, top_n=5):
    """한 섹션의 많이 본 뉴스 수집"""
    url = f"https://news.naver.com/section/{section_id}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        
        items = []
        # 섹션 상단 headline 뉴스 수집
        articles = soup.select("a.sa_text_title")[:top_n]
        
        for a in articles:
            title = a.get_text(strip=True)
            link = a.get("href", "")
            if title and link:
                items.append({
                    "section": name,
                    "title": title,
                    "url": link,
                })
        
        return items
    except Exception as e:
        print(f"  ❌ {name} 실패: {e}")
        return []

def collect():
    all_items = []
    for name, sid in SECTIONS.items():
        items = collect_section(name, sid)
        all_items.extend(items)
        print(f"  {name}: {len(items)}개")
    
    output_path = os.path.join(DATA_DIR, "naver.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 네이버 뉴스: 총 {len(all_items)}개 수집 → {output_path}")
    return all_items

if __name__ == "__main__":
    collect()
