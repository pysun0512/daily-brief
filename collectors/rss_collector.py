"""
공통 RSS 수집기
- sources.yaml에서 정의된 모든 RSS 피드 수집
- 지난 24시간 항목만 필터
- 카테고리별로 그룹핑해서 저장
"""
import feedparser
import yaml
import json
import os
from datetime import datetime, timedelta, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, "..")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
SOURCES_FILE = os.path.join(PROJECT_ROOT, "sources.yaml")
os.makedirs(DATA_DIR, exist_ok=True)

# 24시간 전 시각 (UTC)
CUTOFF = datetime.now(timezone.utc) - timedelta(hours=24)


def parse_entry_date(entry):
    """피드 항목의 발행 시각을 datetime으로 변환"""
    for attr in ("published_parsed", "updated_parsed"):
        t = entry.get(attr)
        if t:
            try:
                return datetime(*t[:6], tzinfo=timezone.utc)
            except Exception:
                pass
    return None


def collect_feed(source):
    """단일 RSS 피드에서 지난 24시간 항목 가져오기"""
    items = []
    try:
        feed = feedparser.parse(source["url"])
        for entry in feed.entries[:30]:  # 각 피드 최대 30개만 검사
            pub = parse_entry_date(entry)
            if pub and pub < CUTOFF:
                continue  # 24시간 지난 거 스킵
            items.append({
                "source": source["name"],
                "category": source["category"],
                "title": entry.get("title", "").strip(),
                "url": entry.get("link", ""),
                "summary": entry.get("summary", "")[:300],  # 짧게
                "published": pub.isoformat() if pub else None,
            })
    except Exception as e:
        print(f"  ❌ {source['name']}: {e}")
    return items


def collect():
    """sources.yaml의 모든 활성 소스 수집"""
    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        sources_config = yaml.safe_load(f)
    
    # 카테고리별 결과 저장
    by_category = {}
    
    for group_name, sources in sources_config.items():
        for source in sources:
            if not source.get("enabled", True):
                continue
            items = collect_feed(source)
            if items:
                cat = source["category"]
                by_category.setdefault(cat, []).extend(items)
                print(f"  ✓ {source['name']}: {len(items)}개")
            else:
                print(f"  · {source['name']}: 0개 (24시간 내 없음)")
    
    # 카테고리별 JSON 파일로 저장
    for category, items in by_category.items():
        output = os.path.join(DATA_DIR, f"rss_{category}.json")
        with open(output, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        print(f"✅ {category}: 총 {len(items)}개 → rss_{category}.json")
    
    return by_category


if __name__ == "__main__":
    collect()
