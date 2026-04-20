"""
아침 브리핑 데이터 수집 (Routine용)
- HN, 네이버 데이터를 data/*.json에 저장
- 슬랙 전송은 Claude Routine이 직접 수행
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from collectors import hackernews, naver_news


def main():
    print("=" * 50)
    print("📥 데이터 수집")
    print("=" * 50)
    
    try:
        hackernews.collect()
    except Exception as e:
        print(f"❌ HN 수집 실패: {e}")
    
    try:
        naver_news.collect()
    except Exception as e:
        print(f"❌ 네이버 수집 실패: {e}")
    
    print()
    print("✅ 수집 완료. data/hn.json, data/naver.json 확인")


if __name__ == "__main__":
    main()
