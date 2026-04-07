---
name: track-analytics
description: 클릭 분석 데이터를 수집하고 저장합니다. IP, User-Agent, 타임스탬프를 기록합니다.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
---

# Track Analytics Skill

이 스킬은 URL 클릭 분석 데이터를 수집합니다.

## Instructions

1. short code를 기반으로 URL 조회
2. 클릭 수를 증가시킴
3. IP 주소와 User-Agent를 기록
4. 분석 데이터를 반환

## Usage

```python
from services import analytics

# 클릭 추적
result = analytics.track_click(
    short_code="abc123",
    ip_address="192.168.1.1",
    user_agent="Mozilla/5.0..."
)

# 분석 데이터 조회
stats = analytics.get_analytics_summary("abc123")
```

## 핵심 함수

- `track_click(short_code, ip_address, user_agent)` - 클릭 기록
- `get_analytics_summary(short_code)` - 분석 데이터 조회

## 저장 데이터

- `url_id`: URL ID
- `ip_address`: 방문자 IP
- `user_agent`: 브라우저 정보
- `clicked_at`: 클릭 시간

## 사용 시점

- 리디렉션 시 매번 호출
- URL 접근 로그 수집
- 클릭 통계 분석