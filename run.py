"""
아침 브리핑 전체 파이프라인 실행
- 데이터 수집 → 메일 + 슬랙 전송
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from collectors import hackernews, naver_news
from delivery import email_sender, slack_sender


def main():
    print("=" * 50)
    print("📥 데이터 수집 시작")
    print("=" * 50)
    
    try:
        hackernews.collect()
    except Exception as e:
        print(f"❌ HN 수집 실패: {e}")
    
    try:
        naver_news.collect()
    except Exception as e:
        print(f"❌ 네이버 뉴스 수집 실패: {e}")
    
    print()
    print("=" * 50)
    print("📤 전송")
    print("=" * 50)
    
    # 메일 전송
    try:
        email_sender.send()
    except Exception as e:
        print(f"❌ 메일 전송 실패: {e}")
    
    # 슬랙 전송
    try:
        slack_sender.send()
    except Exception as e:
        print(f"❌ 슬랙 전송 실패: {e}")
    
    print()
    print("🎉 완료")


if __name__ == "__main__":
    main()
