# QR 코드 + 쇼트링크 생성기 - 작업 분할 계획

## 프로젝트 개요
마케팅용 URL을 입력하면 QR 코드와 쇼트링크를 동시에 생성하는 웹 기반 자동화 시스템

## 작업 분할 (3인 팀 - 병렬 작업)

### Step 1 - 프로젝트 구조 및 문서화 (Architect)
- [ ] 1.1 task.md 생성 - 작업 세분화
- [ ] 1.2 prd.md 생성 - 제품 요구사항 문서
- [ ] 1.3 로드맵.md 생성 - 작업 로드맵

### Step 2 - Backend 구현 (Builder 1)
- [ ] 2.1 FastAPI 서버 구현 (app.py)
  - POST /create - URL 단축 및 QR 생성
  - GET /{code} - 리디렉션
  - GET /stats/{code} - 분석 데이터
- [ ] 2.2 데이터베이스 (SQLite)
  - URL 모델
  -Analytics 모델
- [ ] 2.3 QR 생성 서비스 (qrcode 라이브러리)
- [ ] 2.4 단축 URL 서비스 (Base62 인코딩)

### Step 3 - Frontend 구현 (Builder 2)
- [ ] 3.1 index.html - 메인 페이지
- [ ] 3.2 styles.css - 스타일시트
- [ ] 3.3 app.js - 프론트엔드 로직

### Step 4 - Skills 및 Agents (Builder 3)
- [ ] 4.1 generate-shortlink 스킬 생성
- [ ] 4.2 generate-qr 스킬 생성
- [ ] 4.3 track-analytics 스킬 생성
- [ ] 4.4 Orchestrator 에이전트 생성
- [ ] 4.5 API Generator 에이전트 생성
- [ ] 4.6 QR Generator 에이전트 생성
- [ ] 4.7 Redirect Handler 에이전트 생성
- [ ] 4.8 Analytics Tracker 에이전트 생성

### Step 5 - 테스트 및 검증 (Reviewer)
- [ ] 5.1 URL 입력 → Short Link 생성 확인
- [ ] 5.2 QR 코드 생성 확인
- [ ] 5.3 리디렉션 동작 확인
- [ ] 5.4 Analytics 데이터 수집 확인
- [ ] 5.5 커스텀 alias 기능 확인
- [ ] 5.6 만료일 기능 확인

### Step 6 - 배포 및 문서화 (Architect)
- [ ] 6.1 README.md 작성
- [ ] 6.2 사용 가이드 작성
- [ ] 6.3 최종 테스트 완료

---

## 병렬 작업 가능 항목
- Step 2 (Backend) + Step 3 (Frontend) 병렬 실행
- Step 4 (Skills/Agents) 와 별개로 진행 가능
- Step 5 (테스트) 는 Step 2, 3, 4 완료 후 진행