---
name: create-shortlink
description: URL을 입력하여 QR 코드와 쇼트링크를 생성합니다.
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
---

# Create ShortLink Command

이 커맨드는 URL을 입력받아 QR 코드와 쇼트링크를 생성합니다.

## 사용법

```
/create-shortlink [URL]
```

## 예시

```
/create-shortlink https://example.com
/create-shortlink https://example.com --alias mylink --days 30
```

## 옵션

- `URL` (필수): 단축할 원본 URL
- `--alias` (선택): 커스텀 별칭
- `--days` (선택): 만료일 (기본: 30일)

## 동작

1. URL 유효성 검사
2. short code 생성 (또는 alias 사용)
3. QR 코드 생성 (PNG)
4. 데이터베이스 저장
5. 결과 반환 (short URL, QR 코드)

## 반환값

```json
{
    "short_code": "abc123",
    "short_url": "http://localhost:8000/abc123",
    "qr_code_url": "/qr/abc123",
    "original_url": "https://example.com"
}
```