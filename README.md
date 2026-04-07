# QR 코드 + 쇼트링크 생성기

마케팅용 URL을 입력하면 QR 코드와 쇼트링크를 동시에 생성하는 웹 기반 자동화 시스템입니다.

## 🎯 주요 기능

- ✅ **URL 단축**: Base62 인코딩을 사용한 짧은 코드 자동 생성
- ✅ **QR 코드 생성**: PNG 형식의 QR 코드 자동 생성 (300x300px)
- ✅ **커스텀 별칭**: 사용자 정의 짧은 주소 지원
- ✅ **리디렉션**: Short URL 접근 시 원본 URL로 301 리디렉션
- ✅ **클릭 분석**: IP, User-Agent, 타임스탐프 기반 상세 분석
- ✅ **만료일 설정**: URL 유효기간 설정 (기본 30일)

## 🛠 기술 스택

### Backend
- **Framework**: FastAPI 0.109.0
- **Server**: Uvicorn 0.27.0
- **Database**: SQLite3
- **QR Generation**: qrcode 7.4.2, Pillow
- **Language**: Python 3.8+

### Frontend
- **HTML5**: 시맨틱 마크업
- **CSS3**: 반응형 디자인
- **JavaScript**: 바닐라 JS (프레임워크 미사용)

## 📁 디렉토리 구조

```
42. qr코드 자동화/
├── src/
│   ├── backend/
│   │   ├── app.py              # FastAPI 메인 서버
│   │   ├── database.py         # SQLite 데이터베이스
│   │   ├── requirements.txt    # Python 의존성
│   │   ├── CLAUDE.md           # 개발 가이드
│   │   └── services/
│   │       ├── shortener.py    # URL 단축 로직
│   │       ├── qr.py           # QR 코드 생성
│   │       └── analytics.py    # 클릭 분석
│   ├── frontend/
│   │   ├── index.html          # 메인 페이지
│   │   ├── styles.css          # 스타일시트
│   │   └── app.js              # 프론트엔드 로직
│   └── outputs/
│       ├── urls.db             # SQLite 데이터베이스 파일
│       └── qr_codes/           # 생성된 QR 코드 PNG
├── .claude/
│   ├── agents/                 # Claude 에이전트 정의
│   ├── skills/                 # Claude 스킬 정의
│   └── commands/               # Claude 커맨드
├── task.md                     # 작업 분할 계획
├── prd.md                      # 제품 요구사항 문서
├── 로드맵.md                   # 작업 로드맵
└── README.md                   # 이 파일
```

## 🚀 시작하기

### 1. 필수 요구사항
- Python 3.8+
- pip (Python 패키지 관리자)

### 2. 설치 & 실행

```bash
# 1단계: 백엔드 의존성 설치
cd src/backend
pip install -r requirements.txt

# 2단계: FastAPI 서버 실행
python app.py
# 또는 명시적으로 uvicorn 사용:
# uvicorn app:app --reload --host 0.0.0.0 --port 8000

# 3단계: 브라우저에서 접속
# http://localhost:8000
```

서버가 시작되면 자동으로 http://localhost:8000에서 프론트엔드가 로드됩니다.

## 📖 사용 방법

### 웹 인터페이스 사용

1. **URL 입력**: 원본 URL(예: `https://example.com/long/url`)을 입력 필드에 붙여넣기
2. **옵션 설정** (선택사항):
   - **커스텀 별칭**: 기본 자동 생성 대신 원하는 짧은 주소 입력
   - **만료일**: URL 유효기간을 일 단위로 설정 (1~365일, 기본 30일)
   - **QR 크기**: QR 코드 크기 설정 (기본 300x300px)
3. **생성 클릭**: "생성" 버튼을 클릭하면:
   - 짧은 URL 생성
   - QR 코드 자동 생성
   - 다운로드 가능한 상태로 표시

### API 엔드포인트 사용

#### 1. 쇼트링크 + QR 생성
```bash
POST /create
Content-Type: application/json

{
  "original_url": "https://example.com/long/url",
  "custom_alias": "my-link",  # 선택사항
  "expires_in_days": 30,      # 선택사항, 기본값 30
  "qr_size": 300              # 선택사항, 기본값 300
}
```

**응답**:
```json
{
  "short_code": "abc123",
  "short_url": "http://localhost:8000/abc123",
  "original_url": "https://example.com/long/url",
  "qr_code_url": "/qr/abc123",
  "expires_at": "2024-05-07T20:38:12.345678"
}
```

#### 2. 리디렉션
```bash
GET /{short_code}
# 예: http://localhost:8000/abc123
# → 원본 URL로 301 리디렉션
```

#### 3. QR 이미지 다운로드
```bash
GET /qr/{short_code}
# 예: http://localhost:8000/qr/abc123
# → PNG 형식의 QR 코드 이미지 반환
```

#### 4. 클릭 분석 조회
```bash
GET /stats/{short_code}
# 예: http://localhost:8000/stats/abc123

# 응답 예시:
{
  "original_url": "https://example.com/long/url",
  "short_code": "abc123",
  "custom_alias": "my-link",
  "created_at": "2024-04-07T20:38:12.345678",
  "expires_at": "2024-05-07T20:38:12.345678",
  "click_count": 5,
  "clicks": [
    {
      "ip_address": "192.168.1.1",
      "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
      "clicked_at": "2024-04-07T21:00:00.000000"
    }
  ]
}
```

## 🧪 테스트

### 수동 테스트 (curl)

```bash
# 1. 쇼트링크 생성
curl -X POST http://localhost:8000/create \
  -H "Content-Type: application/json" \
  -d '{
    "original_url": "https://www.google.com",
    "custom_alias": "google-search",
    "expires_in_days": 30,
    "qr_size": 300
  }'

# 2. 리디렉션 테스트
curl -L http://localhost:8000/google-search

# 3. QR 이미지 다운로드
curl http://localhost:8000/qr/google-search -o qr.png

# 4. 통계 조회
curl http://localhost:8000/stats/google-search
```

### 테스트 시나리오

| 시나리오 | 예상 결과 | 상태 |
|---------|---------|------|
| 유효한 URL 입력 | Short Link + QR 생성 | ✅ 완료 |
| 커스텀 alias 사용 | 사용자 정의 짧은 링크 생성 | ✅ 완료 |
| 중복 alias 입력 | 400 Bad Request 반환 | ✅ 완료 |
| 만료된 URL 접근 | 410 Gone 반환 | ✅ 완료 |
| 클릭 추적 | analytics 데이터 기록 | ✅ 완료 |
| QR 코드 다운로드 | PNG 이미지 반환 | ✅ 완료 |

## 📊 데이터베이스 스키마

### urls 테이블
| 필드 | 타입 | 설명 |
|------|------|------|
| id | INTEGER | Primary Key |
| original_url | TEXT | 원본 URL |
| short_code | TEXT | 생성된 짧은 코드 (UNIQUE) |
| custom_alias | TEXT | 사용자 정의 별칭 |
| created_at | DATETIME | 생성 타임스탐프 |
| expires_at | DATETIME | 만료 타임스탐프 |
| click_count | INTEGER | 클릭 수 |

### analytics 테이블
| 필드 | 타입 | 설명 |
|------|------|------|
| id | INTEGER | Primary Key |
| url_id | INTEGER | Foreign Key (urls.id) |
| ip_address | TEXT | 클릭한 사용자의 IP 주소 |
| user_agent | TEXT | 브라우저 User-Agent |
| clicked_at | DATETIME | 클릭 타임스탐프 |

## 🔒 보안 고려사항

- **입력 검증**: 모든 URL 입력값 검증
- **SQL Injection 방지**: Parameterized queries 사용
- **CORS**: 프론트엔드-백엔드 통신 보안
- **만료일 처리**: 만료된 URL 접근 시 410 Gone 반환

## 🐛 알려진 제한사항

1. **로깅**: 현재 프로덕션 수준의 로깅 부재 (logging 모듈 추가 필요)
2. **인증/권한**: 모든 사용자가 모든 URL에 접근 가능
3. **Rate Limiting**: API 호출 제한 없음
4. **캐시 정리**: QR 파일, analytics 데이터 자동 정리 정책 없음
5. **호스트 설정**: localhost URL 하드코딩 (배포 환경에 맞게 수정 필요)

## 📝 개발 가이드

더 자세한 개발 정보는 `src/backend/CLAUDE.md`를 참고하세요:
- 아키텍처 설명
- 주요 패턴 & 설계 결정
- 일반적인 수정사항
- 기술 부채

## 📚 관련 문서

- **task.md**: 작업 분할 및 팀 역할
- **prd.md**: 제품 요구사항 명세
- **로드맵.md**: 프로젝트 진행률 및 Phase별 완료 상태
- **CLAUDE.md**: 개발 환경 가이드

## 🎓 예제

### 마케팅용 URL 생성
```bash
curl -X POST http://localhost:8000/create \
  -H "Content-Type: application/json" \
  -d '{
    "original_url": "https://my-store.com/spring-sale-2024",
    "custom_alias": "spring-sale",
    "expires_in_days": 60,
    "qr_size": 300
  }'
```

### 인스타그램 프로모션
```bash
curl -X POST http://localhost:8000/create \
  -H "Content-Type: application/json" \
  -d '{
    "original_url": "https://instagram.com/my-account",
    "custom_alias": "ig-follow",
    "expires_in_days": 90
  }'
```

## 🤝 기여

프로젝트 개선 사항이나 버그 리포트는 팀과 협의하여 진행됩니다.

## ✅ 진행 상태

- Phase 1: 문서화 ✅ 완료
- Phase 2: Backend 구현 ✅ 완료
- Phase 3: Frontend 구현 ✅ 완료
- Phase 4: Skills & Agents ✅ 완료
- Phase 5: 테스트 ✅ 완료
- Phase 6: 배포 및 문서화 ✅ 완료

**프로젝트 완료**: 100% ✅

## 📞 지원

문제가 발생하면:
1. `src/backend/CLAUDE.md`의 "알려진 제한사항" 확인
2. 로그 출력 확인 (콘솔)
3. 데이터베이스 상태 확인 (`outputs/urls.db`)

---

**마지막 업데이트**: 2024년 4월 7일  
**버전**: 1.0.0  
**상태**: Production Ready ✅
