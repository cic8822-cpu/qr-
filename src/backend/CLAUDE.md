# CLAUDE.md

이 파일은 Claude Code(claude.ai/code)가 이 저장소에서 작업할 때 참고할 지침을 제공합니다.

## 프로젝트 개요

**QR ShortLink Generator** — URL을 단축하고 QR 코드를 생성하는 FastAPI 기반 백엔드입니다. 원본 URL을 입력하면 base62 인코딩된 짧은 코드를 생성하거나 커스텀 alias를 받아들이고, QR 코드를 생성한 후 클릭을 IP와 User-Agent로 추적합니다.

## 개발 워크플로우

### 설정 & 의존성

```bash
# 의존성 설치 (requirements.txt: fastapi, uvicorn, qrcode, python-multipart)
pip install -r requirements.txt

# 개발 서버 실행
python app.py
# 또는 uvicorn으로 실행:
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# 타입 체크 (타입 힌트 추가 시)
python -m py_compile app.py database.py services/*.py
```

### 테스트 & 디버깅

현재 프로젝트에는 테스트 프레임워크가 없습니다. 엔드포인트를 수동으로 테스트하려면:

```bash
# 쇼트링크 생성
curl -X POST http://localhost:8000/create \
  -H "Content-Type: application/json" \
  -d '{"original_url":"https://example.com/long/path","expires_in_days":30,"qr_size":300}'

# 짧은 코드로 리디렉션
curl -L http://localhost:8000/shortcode

# QR 이미지 가져오기
curl http://localhost:8000/qr/shortcode -o qr.png

# 통계 조회
curl http://localhost:8000/stats/shortcode
```

## 아키텍처 & 주요 컴포넌트

### 데이터베이스 계층 (`database.py`)
- **위치**: SQLite 저장소 `../outputs/urls.db`
- **테이블**:
  - `urls`: 원본 URL, 짧은 코드, 커스텀 alias, 생성일, 만료일, 클릭 수 추적
  - `analytics`: 개별 클릭 기록 (IP, User-Agent, 타임스탐프 포함, urls로의 외래키)
- **주요 함수**: `get_db()`, `init_db()`, `create_url()`, `get_url_by_code()`, `get_stats()`
- **초기화**: 앱 시작 시 `@app.on_event("startup")`을 통해 테이블 자동 생성

### API 계층 (`app.py`)
FastAPI 애플리케이션의 4개 엔드포인트:

1. **POST /create** — 쇼트링크 생성 (선택적 커스텀 alias 및 QR 코드)
   - 원본 URL 검증 (없으면 https:// 추가)
   - alias 중복 확인
   - QR 코드를 디스크에 생성
   - 짧은 코드, 짧은 URL, QR 엔드포인트 반환

2. **GET /qr/{short_code}** — QR 이미지 PNG로 제공
   - QR 파일이 없으면 404 반환

3. **GET /{short_code}** — 리디렉션 & 추적
   - 리디렉션 전 만료 여부 확인
   - analytics에 기록 (IP, User-Agent)
   - 원본 URL로 301 리디렉션
   - 만료된 링크는 410 Gone 반환

4. **GET /stats/{short_code}** — URL 통계 조회
   - 원본 URL, 생성일, 클릭 수, 상세 클릭 히스토리 반환

### 서비스 모듈

#### `services/shortener.py`
- **Base62 인코딩/디코딩** — URL 단축 처리
- **`generate_short_code()`** — 무작위 6자 base62 문자열 생성 (타임스탬프 기반 `generate_from_timestamp()` 대체 가능)
- **`format_expiry()`** — 일수를 ISO 8601 형식으로 변환
- **`is_expired()`** — URL 만료 여부 확인

#### `services/qr.py`
- **`generate_qr_image()`** — URL에서 PIL 이미지 생성 (높은 오류 정정, 10x10 박스 크기, 4px 테두리)
- **`save_qr_file()`** — QR을 PNG로 `../outputs/qr_codes/{short_code}.png`에 저장
- **`generate_qr_base64()`** — base64 인코딩된 PNG 반환 (현재 API에서 미사용, 하지만 가능)
- **`generate_qr_svg()`** — SVG QR 코드를 문자열로 생성 (현재 API에서 미사용)
- **QR 파일은 영구 저장** — 누락되면 다시 생성

#### `services/analytics.py`
- **`track_click()`** — analytics 테이블에 클릭 기록하고 URL 클릭 수 증가
- **`get_analytics_summary()`** — `database.get_stats()` 래퍼
- 기록 전 만료 여부 확인

## 주요 패턴 & 설계 결정

### URL 검증
- URL에 `http://` 또는 `https://`가 없으면 프론트엔드에서 `https://`를 추가해야 함
- 프로토콜 확인 이외의 URL 구조 검증 없음

### 만료 시스템
- 만료일은 ISO 8601 문자열로 데이터베이스에 저장
- 리디렉션 시점에 만료 확인 (예약된 정리 없음)
- 만료된 URL은 삭제하지 않고 HTTP 410 Gone 반환

### QR 코드 저장
- PNG 파일은 `outputs/qr_codes/`에 영구 저장
- 필요 시 생성하고 디스크에 캐싱
- `FileResponse`로 `image/png` 미디어 타입으로 제공

### 분석 데이터
- 클릭별로 저장 (집계 없음)
- `request.client.host`에서 IP 주소 캡처
- 요청 헤더에서 User-Agent 추출
- 예약된 데이터 정리 없음

### 커스텀 Alias
- 사용자가 자동 생성 코드 대신 `custom_alias` 제공 가능
- 데이터베이스 수준에서 고유성 제약 시행
- alias가 이미 존재하면 400 Bad Request 반환

## 일반적인 수정사항

### 검증 규칙 추가
`app.py`의 **POST /create** 엔드포인트에서 `create_url()` 호출 전에 수정합니다.

### 짧은 코드 생성 방식 변경
`app.py:39`의 `generate_short_code()` 호출을 `services/shortener.py`의 대안으로 교체합니다 (예: 타임스탬프 기반 `generate_from_timestamp()`).

### 새로운 분석 지표 추가
1. `database.py:init_db()`의 `analytics` 테이블에 컬럼 추가
2. `services/analytics.py`의 `track_click()`을 수정하여 지표 기록
3. `database.py`의 `get_stats()`를 수정하여 지표 반환

### QR 커스터마이제이션 확장
`services/qr.py:generate_qr_image()`에 파라미터 추가 (예: 색상, 테두리 크기), `URLCreate` 모델에서 노출, `save_qr_file()`로 전달합니다.

## 알려진 제한사항 & 기술 부채

- 테스트 커버리지 없음
- 로깅 프레임워크 미사용 (프로덕션 배포 시 `logging` 모듈 추가 필요)
- analytics 테이블에 보관 정책 없음 (무한 증가)
- URL 삭제 시 QR 파일 정리 안 함 (고아 파일 누적 가능)
- `/create` 엔드포인트에 rate limiting 없음
- 인증/권한 부여 없음 (모든 사용자가 모든 URL 생성/조회 가능)
- 응답에 localhost URL 하드코딩 (배포 호스트에 따라 파라미터화 필요)
- ISO 문자열 파싱으로 만료 확인 (데이터베이스 수준 날짜 비교가 더 효율적)

## 출력 디렉토리 구조

```
outputs/
├── urls.db           — SQLite 데이터베이스
└── qr_codes/         — QR 코드 PNG 파일 (짧은 코드당 하나)
```

모든 파일은 프로젝트 루트에 상대적으로 저장됩니다 (`src/backend`에서 `../../`).
