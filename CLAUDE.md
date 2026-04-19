# Daily Brief Routine

매일 아침 7시(KST)에 실행되는 자동 브리핑 시스템.

## 목적
주요 뉴스 소스에서 당일 인기 콘텐츠를 수집해 HTML 이메일로 전송.

## 실행 방법

하나의 명령어로 전체 파이프라인이 돌아간다:
```bash
cd ~/daily-brief
source venv/bin/activate
python3 run.py
```

이 명령어가 하는 일:
1. `collectors/hackernews.py` 실행 → `data/hn.json` 저장
2. `collectors/naver_news.py` 실행 → `data/naver.json` 저장
3. `delivery/email_sender.py` 실행 → HTML 이메일로 `TO_EMAIL` 주소에 전송

## 환경 변수
`.env` 파일에 다음 값들이 있어야 함:
- `RESEND_API_KEY` — Resend API 키
- `TO_EMAIL` — 수신자 이메일
- `FROM_EMAIL` — 발신자 이메일 (현재: `onboarding@resend.dev`)

## 성공 기준
- 출력 마지막에 `🎉 완료` 메시지
- `✅ 메일 전송됨: {'id': ...}` 응답 확인
- 수집 건수가 0이 아닐 것 (HN 최소 5개, 네이버 최소 10개 권장)

## 실패 시 대응

### 수집 실패
- 특정 collector가 실패해도 나머지는 계속 진행됨 (run.py에서 try/except 처리됨)
- 모든 collector 실패 시에도 빈 템플릿으로 이메일은 전송됨 (상태 확인용)

### 네이버 뉴스 0개 수집
- 네이버가 HTML 구조를 변경했을 가능성
- `collectors/naver_news.py`의 CSS 선택자 `a.sa_text_title` 확인
- 필요 시 선택자 수정 후 재실행

### 메일 전송 실패
- Resend API 키 만료/무효 가능성
- 일일 전송 한도(100통) 초과 확인
- 상세 에러 메시지를 로그에 남김

## 하지 말 것
- git commit, PR 생성 금지 — 이 루틴은 전송만 수행
- `.env` 파일 수정 금지
- 새로운 라이브러리 자동 설치 금지 (venv 내 기존 라이브러리만 사용)

## 출력 형식
루틴 실행 후 아래 항목을 짧게 보고:
- 각 collector 수집 건수
- 메일 전송 ID
- 전체 소요 시간
