---
name: generate-qr
description: QR 코드를 생성합니다. PNG와 SVG 형식을 지원하며 커스텀 색상과 크기 설정이 가능합니다.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
---

# Generate QR Code Skill

이 스킬은 QR 코드 생성 기능을 제공합니다.

## Instructions

1. URL을 입력으로 받는다
2. qrcode 라이브러리를 사용하여 QR 코드를 생성한다
3. PNG 또는 SVG 형식으로 저장한다
4. Base64 인코딩으로 웹에서 바로 표시 가능하다

## Usage

```python
from services import qr

# PNG 이미지 생성
img = qr.generate_qr_image(url, size=300)

# Base64 문자열 생성
base64_qr = qr.generate_qr_base64(url, size=300)

# 파일로 저장
qr_path = qr.save_qr_file(short_code, url, size=300)

# SVG 생성
svg_content = qr.generate_qr_svg(url, size=300)
```

## 핵심 함수

- `generate_qr_image(url, size, fill_color, back_color)` - PIL Image 객체 생성
- `generate_qr_base64(url, size, fill_color, back_color)` - Base64 문자열 반환
- `save_qr_file(short_code, url, size)` - 파일로 저장하고 경로 반환
- `get_qr_path(short_code)` - 저장된 QR 파일 경로 조회
- `generate_qr_svg(url, size)` - SVG 형식 문자열 생성

## 설정 옵션

- `size`: QR 코드 크기 (픽셀)
- `fill_color`:的前景색 (기본: "black")
- `back_color`: 배경색 (기본: "white")
- `error_correction`: 오류 수정 수준 (L, M, Q, H)