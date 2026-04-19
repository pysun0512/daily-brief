"""
Hacker News Top 스토리 수집
- 공식 API 사용 (무료, 인증 불필요)
- 지난 24시간 내 작성된 Top 10 저장
"""
import requests
import json
import os
from datetime import datetime, timedelta

# 파일이 어디서 실행되든 data/ 폴더 제대로 찾게 하기
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

def collect():
    # Top 30 스토리 ID 가져오기
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    top_ids = requests.get(url, timeout=10).json()[:30]
    
    cutoff = (datetime.now() - timedelta(hours=24)).timestamp()
    items = []
    
    for story_id in top_ids:
        try:
            r = requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                timeout=5
            )
            item = r.json()
            if item and item.get("time", 0) >= cutoff:
                items.append({
                    "title": item.get("title", ""),
                    "url": item.get("url") or f"https://news.ycombinator.com/item?id={story_id}",
                    "score": item.get("score", 0),
                    "comments": item.get("descendants", 0),
                    "author": item.get("by", ""),
                })
        except Exception as e:
            print(f"  스킵 (id={story_id}): {e}")
    
    # 점수 높은 순으로 정렬 후 상위 10개
    items.sort(key=lambda x: x["score"], reverse=True)
    items = items[:10]
    
    output_path = os.path.join(DATA_DIR, "hn.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Hacker News: {len(items)}개 수집 → {output_path}")
    return items

if __name__ == "__main__":
    collect()
