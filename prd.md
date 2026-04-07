# PRD - QR 코드 + 쇼트링크 생성기

## 1. 개요

### 1.1 프로젝트 이름
QR 코드 + 쇼트링크 생성기 (QR ShortLink Generator)

### 1.2 프로젝트 유형
웹 기반 자동화 도구

### 1.3 핵심 기능 요약
마케팅용 URL을 입력하면 QR 코드와 쇼트링크를 동시에 생성하는 웹 기반 자동화 시스템

### 1.4 대상 사용자
- 마케팅 담당자
- 홍보물 제작자
- 웹사이트 운영자

---

## 2. 기술 스택

### 2.1 Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite
- **Key Libraries**: qrcode, pillow

### 2.2 Frontend
- **Type**: Static HTML + JavaScript
- **Design**: Responsive, Modern UI

---

## 3. 기능 요구사항

### 3.1 핵심 기능

#### F1: URL 단축
- 원본 URL을 짧은 코드로 변환
- Base62 인코딩 방식 사용
- 자동 생성 또는 커스텀 alias 지원

#### F2: QR 코드 생성
- PNG/SVG 형식 지원
- 해상도: 300x300 px (기본)
- 커스텀 색상 옵션 (선택)

#### F3: 리디렉션
- Short URL 접근 시 원본 URL로 301 리디렉션
- 클릭 추적 로깅

#### F4: 클릭 분석 (Analytics)
- 클릭 수 카운트
- IP 주소 기록
- User-Agent 기록
- 타임스탬프 기록

#### F5: 만료일 설정
- 날짜指定 가능
- 만료 후 접근 시 오류 메시지

### 3.2 API 엔드포인트

| 메서드 | 엔드포인트 | 설명 |
|--------|-----------|------|
| POST | /create | URL 단축 + QR 생성 |
| GET | /{code} | Short URL 리디렉션 |
| GET | /stats/{code} | 클릭 분석 데이터 |
| GET | /qr/{code} | QR 코드 이미지 반환 |

### 3.3 사용자 인터페이스

#### 입력 필드
- URL 입력 (필수)
- 커스텀 alias (선택)
- 만료일 (선택)
- QR 크기 (선택)

#### 출력
- Short URL 표시
- QR 코드プレビュー
- 다운로드 버튼

---

## 4. 데이터베이스 스키마

### 4.1 URLs 테이블
| 필드 | 타입 | 설명 |
|------|------|------|
| id | INTEGER | Primary Key |
| original_url | TEXT | 원본 URL |
| short_code | TEXT | 단축 코드 |
| custom_alias | TEXT | 커스텀 별칭 |
| created_at | DATETIME | 생성일 |
| expires_at | DATETIME | 만료일 |
| click_count | INTEGER | 클릭 수 |

### 4.2 Analytics 테이블
| 필드 | 타입 | 설명 |
|------|------|------|
| id | INTEGER | Primary Key |
| url_id | INTEGER | Foreign Key |
| ip_address | TEXT | IP 주소 |
| user_agent | TEXT | 사용자 에이전트 |
| clicked_at | DATETIME | 클릭 시간 |

---

## 5. 프로젝트 구조

```
qr-automation/
├── .claude/
│   ├── agents/
│   │   ├── orchestrator.md
│   │   ├── api-generator.md
│   │   ├── qr-generator.md
│   │   ├── redirect-handler.md
│   │   └── analytics-tracker.md
│   ├── skills/
│   │   ├── generate-shortlink/
│   │   │   └── SKILL.md
│   │   ├── generate-qr/
│   │   │   └── SKILL.md
│   │   └── track-analytics/
│   │       └── SKILL.md
│   └── commands/
│       └── create-shortlink.md
├── src/
│   ├── backend/
│   │   ├── app.py
│   │   ├── models.py
│   │   ├── database.py
│   │   └── services/
│   │       ├── shortener.py
│   │       ├── qr.py
│   │       └── analytics.py
│   └── frontend/
│       ├── index.html
│       ├── app.js
│       └── styles.css
└── outputs/
```

---

## 6.验收 기준

### 6.1 성공 조건
1. URL 입력 시 Short URL이 생성된다
2. QR 코드가 정확하게 생성된다
3. Short URL访问 시 원본 URL로 리디렉션된다
4. 클릭 분석 데이터가 정확히 수집된다

### 6.2 테스트 시나리오
1. 유효한 URL 입력 → Short Link + QR 생성
2. 커스텀 alias 사용 → 사용자 정의 Short Link
3. 만료일 설정 → 만료 후 접근 시 오류
4. 분석 데이터 확인 → 클릭 수 정확히 카운트

---

## 7. 비기능적 요구사항

### 7.1 성능
- QR 생성 시간: 1초 이내
- 리디렉션 시간: 100ms 이내

### 7.2 보안
- 입력값 검증
- SQL 인젝션 방지
-恶意 URL 차단

### 7.3 사용성
- 직관적인 UI
- 모바일 반응형 지원
- 빠른 응답 시간