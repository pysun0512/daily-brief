"""
Slack #daily-brief 채널로 브리핑 전송
- Block Kit 사용 (헤더, 섹션, 구분선)
- data/ 폴더의 JSON 파일 읽어서 메시지 생성
"""
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, "..")
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")


def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"  ⚠️ {filename} 읽기 실패: {e}")
        return []


def truncate(text, max_len=200):
    """슬랙은 섹션당 텍스트 제한이 있어서 너무 길면 잘라줌"""
    if len(text) > max_len:
        return text[:max_len - 3] + "..."
    return text


def build_blocks():
    today = datetime.now().strftime("%Y년 %m월 %d일 (%a)")
    
    hn_items = load_json("hn.json")
    naver_items = load_json("naver.json")
    
    blocks = []
    
    # 헤더
    blocks.append({
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": f"☀️ {today} 아침 브리핑",
            "emoji": True
        }
    })
    
    # Hacker News 섹션
    if hn_items:
        blocks.append({"type": "divider"})
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*💻 Hacker News Top*"
            }
        })
        for item in hn_items[:5]:  # 슬랙 알림은 짧게, 상위 5개만
            title = truncate(item.get("title", ""), 150)
            url = item.get("url", "")
            score = item.get("score", 0)
            comments = item.get("comments", 0)
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<{url}|*{title}*>\n⬆ {score} · 💬 {comments}"
                }
            })
    
    # 네이버 뉴스 섹션
    if naver_items:
        blocks.append({"type": "divider"})
        
        # 섹션별로 그룹핑
        by_section = {}
        for item in naver_items:
            by_section.setdefault(item["section"], []).append(item)
        
        for section_name, section_items in by_section.items():
            text_lines = [f"*📰 {section_name}*"]
            for item in section_items[:3]:  # 카테고리당 3개씩만
                title = truncate(item.get("title", ""), 100)
                url = item.get("url", "")
                text_lines.append(f"• <{url}|{title}>")
            
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "\n".join(text_lines)
                }
            })
    
    # 푸터
    blocks.append({"type": "divider"})
    blocks.append({
        "type": "context",
        "elements": [{
            "type": "mrkdwn",
            "text": f"_daily-brief · 자동 생성됨 · {datetime.now().strftime('%H:%M')}_"
        }]
    })
    
    return blocks


def send():
    if not WEBHOOK_URL:
        raise ValueError("SLACK_WEBHOOK_URL이 .env에 설정되지 않음")
    
    blocks = build_blocks()
    today = datetime.now().strftime("%m월 %d일")
    
    payload = {
        "text": f"☀️ {today} 아침 브리핑",  # 알림에 뜨는 fallback 텍스트
        "blocks": blocks,
    }
    
    r = requests.post(
        WEBHOOK_URL,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=10
    )
    r.raise_for_status()
    
    print(f"✅ 슬랙 전송됨 (응답: {r.text}, 블록 수: {len(blocks)})")
    return r.text


if __name__ == "__main__":
    send()
