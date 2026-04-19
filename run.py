"""
아침 브리핑 전체 파이프라인 실행
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from collectors import hackernews, naver_news
from delivery import email_sender

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
    print("📧 메일 전송")
    print("=" * 50)
    
    email_sender.send()
    
    print()
    print("🎉 완료")

if __name__ == "__main__":
    main()
