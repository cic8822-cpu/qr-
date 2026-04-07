---
name: generate-shortlink
description: URL을 단축 코드로 변환할 때 사용합니다. Base62 인코딩과 타임스탬프 기반으로 고유한 short code를 생성합니다.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
---

# Generate ShortLink Skill

이 스킬은 URL을 단축 링크로 변환하는 기능を提供します.

## Instructions

1. URL을 입력으로 받는다
2. Base62 인코딩을 사용하여 고유한 short code를 생성한다
3. 커스텀 alias가 제공된 경우 해당 alias를 우선 사용한다
4. 데이터베이스에 short code와 원본 URL을 저장한다

## Usage

```python
from services.shortener import generate_short_code, format_expiry

# 자동 생성
short_code = generate_short_code(length=6)

# 커스텀 alias 사용
short_code = custom_alias  # 검증 후 사용

# 만료일 설정
expires_at = format_expiry(days=30)
```

## 핵심 함수

- `generate_short_code(length: int = 6)` - 랜덤 short code 생성
- `encode_base62(num: int)` - 숫자를 Base62로 인코딩
- `decode_base62(code: str)` - Base62를 숫자로 디코딩
- `generate_from_timestamp()` - 타임스탬프 기반 code 생성
- `format_expiry(days: int)` - 만료일 계산
- `is_expired(expires_at: str)` - 만료 여부 확인