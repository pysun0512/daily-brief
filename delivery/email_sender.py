"""
Resend로 브리핑 이메일 전송
- data/ 폴더의 JSON 파일들을 읽어서
- HTML로 포맷팅해서 전송
"""
import os
import json
import resend
from datetime import datetime
from dotenv import load_dotenv

# .env 파일 로드
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, "..")
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

resend.api_key = os.getenv("RESEND_API_KEY")

DATA_DIR = os.path.join(PROJECT_ROOT, "data")

def load_json(filename):
    """data/ 폴더에서 JSON 파일 읽기, 없으면 빈 리스트"""
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"  ⚠️ {filename} 읽기 실패: {e}")
        return []

def build_hn_section(items):
    if not items:
        return ""
    rows = ""
    for item in items:
        rows += f"""
        <div class="item">
          <div class="title"><a href="{item['url']}">{item['title']}</a></div>
          <div class="meta">⬆ {item['score']} · 💬 {item['comments']} · @{item['author']}</div>
        </div>
        """
    return f"""
    <h2>💻 Hacker News Top</h2>
    {rows}
    """

def build_naver_section(items):
    if not items:
        return ""
    # 섹션별로 그룹핑
    by_section = {}
    for item in items:
        by_section.setdefault(item["section"], []).append(item)
    
    html = "<h2>📰 네이버 뉴스 랭킹</h2>"
    for section_name, section_items in by_section.items():
        html += f'<h3>{section_name}</h3>'
        for item in section_items:
            html += f"""
            <div class="item">
              <div class="title"><a href="{item['url']}">{item['title']}</a></div>
            </div>
            """
    return html

def build_html():
    today = datetime.now().strftime("%Y년 %m월 %d일")
    
    hn_items = load_json("hn.json")
    naver_items = load_json("naver.json")
    
    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{
      font-family: -apple-system, 'Apple SD Gothic Neo', sans-serif;
      max-width: 640px;
      margin: 0 auto;
      padding: 20px;
      color: #1a1a1a;
      line-height: 1.6;
    }}
    h1 {{
      font-size: 24px;
      border-bottom: 3px solid #0066ff;
      padding-bottom: 10px;
      margin-bottom: 24px;
    }}
    h2 {{
      font-size: 18px;
      color: #0066ff;
      margin-top: 32px;
      margin-bottom: 12px;
    }}
    h3 {{
      font-size: 14px;
      color: #666;
      margin-top: 20px;
      margin-bottom: 8px;
      font-weight: 600;
    }}
    .item {{
      padding: 10px 0;
      border-bottom: 1px solid #eee;
    }}
    .title {{
      font-size: 15px;
      margin-bottom: 4px;
    }}
    .title a {{
      color: #1a1a1a;
      text-decoration: none;
    }}
    .title a:hover {{
      color: #0066ff;
    }}
    .meta {{
      font-size: 12px;
      color: #888;
    }}
    .footer {{
      margin-top: 40px;
      padding-top: 16px;
      border-top: 1px solid #eee;
      font-size: 12px;
      color: #999;
      text-align: center;
    }}
  </style>
</head>
<body>
  <h1>☀️ {today} 아침 브리핑</h1>
  {build_hn_section(hn_items)}
  {build_naver_section(naver_items)}
  <div class="footer">
    daily-brief · 자동 생성됨
  </div>
</body>
</html>
"""
    return html

def send():
    html = build_html()
    today = datetime.now().strftime("%m월 %d일")
    
    response = resend.Emails.send({
        "from": os.getenv("FROM_EMAIL"),
        "to": os.getenv("TO_EMAIL"),
        "subject": f"☀️ {today} 아침 브리핑",
        "html": html,
    })
    
    print(f"✅ 메일 전송됨: {response}")
    return response

if __name__ == "__main__":
    send()
