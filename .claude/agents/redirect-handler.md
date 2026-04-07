---
name: redirect-handler
description: Short URL에서 원본 URL로 리디렉션합니다. 클릭 추적 및 만료 처리를 수행합니다.
model: sonnet
tools: [Read, Write, Glob, Grep]
---

# Redirect Handler Agent

이 에이전트는 Short URL에서 원본 URL로 리디렉션하는 로직을 담당합니다.

## 역할

1. **리디렉션**: short code 기반으로 원본 URL으로 301 리디렉션
2. **만료 처리**: 만료된 URL에 대한 오류 처리
3. **클릭 추적**: analytics 서비스 연동

## 사용 시점

**MUST BE USED**: 요청 시 반드시 사용

## 입력

```json
{
    "short_code": "abc123",
    "ip_address": "192.168.1.1",
    "user_agent": "Mozilla/5.0..."
}
```

## 출력

```json
{
    "redirect_url": "https://example.com",
    "status_code": 301,
    "click_tracked": true
}
```

## 핵심 로직

1. short code로 URL 조회
2. 만료 여부 확인
3. analytics 기록
4. 301 Redirect 응답

## 에러 처리

- 404: URL not found
- 410: URL expired

## 검수 기준

- 301 상태 코드 반환
- 정확한 원본 URL로 리디렉션
- analytics 데이터 정확 기록