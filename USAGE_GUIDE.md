# QR 코드 + 쇼트링크 생성기 — 사용 가이드

## 📖 목차

1. [빠른 시작](#빠른-시작)
2. [웹 인터페이스 사용법](#웹-인터페이스-사용법)
3. [API 사용법](#api-사용법)
4. [고급 기능](#고급-기능)
5. [FAQ](#faq)
6. [문제 해결](#문제-해결)

---

## 빠른 시작

### 3단계로 시작하기

```bash
# 1. 백엔드 의존성 설치
cd src/backend
pip install -r requirements.txt

# 2. 서버 실행
python app.py

# 3. 브라우저 열기
# http://localhost:8000
```

**완료!** 이제 URL을 단축하고 QR 코드를 생성할 수 있습니다.

---

## 웹 인터페이스 사용법

### 기본 사용 흐름

#### 1단계: URL 입력
```
📝 URL 주소 필드에 다음 중 하나를 입력:
   ✓ https://example.com
   ✓ www.example.com (자동으로 https:// 추가)
   ✓ example.com (자동으로 https:// 추가)
```

#### 2단계: 선택 옵션 설정

| 옵션 | 기본값 | 범위 | 설명 |
|------|--------|------|------|
| **커스텀 별칭** | (자동 생성) | 1-50자 | 원하는 짧은 주소 지정 (예: `my-link`) |
| **만료일** | 30일 | 1-365일 | URL 유효기간 설정 |
| **QR 크기** | 300px | 100-500px | QR 코드 크기 조정 |

#### 3단계: 생성 버튼 클릭

클릭하면 다음이 자동 생성됩니다:
- ✅ 짧은 URL (예: `http://localhost:8000/abc123`)
- ✅ QR 코드 이미지 (PNG, 300x300px)
- ✅ 다운로드 링크

---

### 실제 사용 예시

#### 예제 1: 블로그 포스트 공유

```
원본 URL:
https://myblog.com/2024/04/ultimate-guide-to-seo?utm_source=twitter

입력 정보:
- URL: https://myblog.com/2024/04/ultimate-guide-to-seo?utm_source=twitter
- 커스텀 별칭: seo-guide
- 만료일: 90 (3개월)
- QR 크기: 300

생성 결과:
- 짧은 URL: http://localhost:8000/seo-guide
- QR 코드: [다운로드 가능]
- 유효기간: 2024-07-06
```

**사용**: 트위터에 QR 코드를 포함한 이미지로 공유

#### 예제 2: 시간 한정 판매

```
원본 URL:
https://store.com/flash-sale-limited-time?code=SPRING2024

입력 정보:
- URL: https://store.com/flash-sale-limited-time?code=SPRING2024
- 커스텀 별칭: spring-sale
- 만료일: 1 (당일만 유효)
- QR 크기: 400

생성 결과:
- 짧은 URL: http://localhost:8000/spring-sale
- QR 코드: 판매 포스터에 인쇄
```

**사용**: 마케팅 포스터, 전단지, SNS에 배포

#### 예제 3: 이벤트 등록 링크

```
원본 URL:
https://events.company.com/register?event=webinar-2024-q2&ref=marketing

입력 정보:
- URL: https://events.company.com/register?event=webinar-2024-q2&ref=marketing
- 커스텀 별칭: webinar-q2
- 만료일: 7 (1주일)

생성 결과:
- 짧은 URL: http://localhost:8000/webinar-q2
- QR 코드: 이메일, 웹사이트에 배포
```

**사용**: 이메일 뉴스레터, 웹 배너

---

## API 사용법

### 프로그래밍 방식으로 사용

#### JavaScript/Node.js 예제

```javascript
// 쇼트링크 + QR 생성
async function createShortLink(originalUrl, customAlias = null) {
  const response = await fetch('http://localhost:8000/create', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      original_url: originalUrl,
      custom_alias: customAlias,
      expires_in_days: 30,
      qr_size: 300
    })
  });
  
  const data = await response.json();
  console.log('짧은 URL:', data.short_url);
  console.log('QR 코드:', data.qr_code_url);
  return data;
}

// 사용
createShortLink('https://example.com/long/url', 'my-link');
```

#### Python 예제

```python
import requests
import json

def create_short_link(original_url, custom_alias=None, expires_in_days=30):
    """쇼트링크 생성"""
    url = 'http://localhost:8000/create'
    payload = {
        'original_url': original_url,
        'custom_alias': custom_alias,
        'expires_in_days': expires_in_days,
        'qr_size': 300
    }
    
    response = requests.post(url, json=payload)
    return response.json()

# 사용
result = create_short_link('https://example.com/blog/post')
print(f"짧은 URL: {result['short_url']}")
print(f"QR 코드: {result['qr_code_url']}")
```

#### curl 예제

```bash
# 기본 생성
curl -X POST http://localhost:8000/create \
  -H "Content-Type: application/json" \
  -d '{
    "original_url": "https://example.com",
    "expires_in_days": 30
  }'

# 커스텀 alias 사용
curl -X POST http://localhost:8000/create \
  -H "Content-Type: application/json" \
  -d '{
    "original_url": "https://example.com",
    "custom_alias": "my-link",
    "expires_in_days": 60,
    "qr_size": 400
  }'

# 결과를 파일로 저장
curl -X POST http://localhost:8000/create \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://example.com"}' \
  > result.json
```

### API 응답 형식

#### 성공 응답 (200 OK)

```json
{
  "short_code": "abc123",
  "short_url": "http://localhost:8000/abc123",
  "original_url": "https://example.com",
  "qr_code_url": "/qr/abc123",
  "expires_at": "2024-05-07T20:38:12.345678"
}
```

#### 오류 응답 (400 Bad Request)

```json
{
  "detail": "Alias already in use"
}
```

#### 오류 응답 (404 Not Found)

```json
{
  "detail": "URL not found"
}
```

#### 오류 응답 (410 Gone)

```json
{
  "detail": "URL expired"
}
```

---

## 고급 기능

### 1. 클릭 분석 조회

```bash
# API 호출
curl http://localhost:8000/stats/abc123

# 응답
{
  "original_url": "https://example.com",
  "short_code": "abc123",
  "custom_alias": "my-link",
  "created_at": "2024-04-07T20:38:12.345678",
  "expires_at": "2024-05-07T20:38:12.345678",
  "click_count": 42,
  "clicks": [
    {
      "ip_address": "192.168.1.100",
      "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
      "clicked_at": "2024-04-07T21:15:30.123456"
    },
    {
      "ip_address": "10.0.0.50",
      "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4)...",
      "clicked_at": "2024-04-07T21:20:45.654321"
    }
  ]
}
```

**활용**:
- 캠페인 효과 측정
- 클릭 소스 분석 (IP 주소)
- 사용자 디바이스 추적 (User-Agent)
- 시간대별 클릭 분포 분석

### 2. QR 코드 다운로드

```bash
# PNG 이미지로 다운로드
curl http://localhost:8000/qr/abc123 -o qr_code.png

# 마크다운에 임베드
![QR Code](http://localhost:8000/qr/abc123)

# HTML에 임베드
<img src="http://localhost:8000/qr/abc123" alt="QR Code">
```

### 3. 만료일 관리

```
생성 시점: 2024-04-07 20:38:12
만료일: 2024-05-07 20:38:12 (30일 후)

만료 후:
- GET /{code} 접근 → 410 Gone (리디렉션 불가)
- GET /stats/{code} 접근 → 통계 조회 가능 (히스토리 유지)
- 데이터베이스 → URL 기록 유지 (삭제 안 됨)
```

### 4. 커스텀 alias 네이밍 규칙

**지원하는 형식**:
```
✅ my-link          (하이픈 허용)
✅ mylink123        (숫자 허용)
✅ MYLINK           (대문자 허용)
✅ my_link          (언더스코어 허용)
```

**주의사항**:
```
❌ my link          (공백 불가)
❌ my-link!         (특수문자 불가)
❌ /my/link         (슬래시 불가)
❌ 한글-링크        (한글은 권장하지 않음)
```

---

## FAQ

### Q1: 서버를 다른 포트에서 실행하려면?

```bash
# 기본 포트: 8000
python app.py

# 다른 포트 사용 (예: 3000)
uvicorn app:app --host 0.0.0.0 --port 3000
```

### Q2: 생성된 QR 코드를 SVG 형식으로 받을 수 있나요?

현재 API는 PNG만 지원합니다. SVG 지원이 필요하면:
1. `src/backend/services/qr.py`의 `generate_qr_svg()` 함수 활용
2. API 엔드포인트 추가 필요

### Q3: URL이 만료되면 데이터를 복구할 수 있나요?

만료된 URL도 다음이 가능합니다:
- ✅ `/stats/{code}`로 분석 데이터 조회
- ✅ 데이터베이스에 기록 유지
- ❌ `/`로 리디렉션은 불가 (410 Gone)

### Q4: 얼마나 많은 URL을 생성할 수 있나요?

이론적으로 무제한입니다:
- Base62 인코딩으로 6자리 = 약 5,689,009,063,875 가지 조합
- 저장소 제약: 디스크 용량에 따름
- 현재 환경: 제한 없음

### Q5: 데이터베이스는 어디에 저장되나요?

```
outputs/urls.db ← SQLite 데이터베이스
outputs/qr_codes/ ← 생성된 QR 코드 PNG
```

프로젝트 루트 기준 상대 경로입니다.

### Q6: HTTPS 환경에서는?

현재 localhost HTTP만 지원합니다. 프로덕션 배포 시:
1. `src/backend/app.py:45` 수정
   ```python
   # 변경 전
   short_url = f"http://localhost:8000/{short_code}"
   
   # 변경 후
   short_url = f"https://yourdomain.com/{short_code}"
   ```
2. HTTPS 인증서 설정
3. 리버스 프록시(Nginx/Apache) 구성

### Q7: 프론트엔드를 다른 도메인에서 호스팅할 수 있나요?

가능합니다. `src/frontend/app.js`에서 API 엔드포인트 수정:
```javascript
// 변경 전
const API_URL = 'http://localhost:8000';

// 변경 후
const API_URL = 'https://api.yourdomain.com';
```

---

## 문제 해결

### 문제 1: "127.0.0.1 refused connection"

**원인**: 서버가 실행되지 않음

**해결**:
```bash
# 1단계: 백엔드 디렉토리로 이동
cd src/backend

# 2단계: 서버 실행
python app.py

# 3단계: 로그 확인
# "Application startup complete" 메시지 확인
```

### 문제 2: "ModuleNotFoundError: No module named 'fastapi'"

**원인**: 의존성이 설치되지 않음

**해결**:
```bash
# 1단계: 백엔드 디렉토리로 이동
cd src/backend

# 2단계: 의존성 설치
pip install -r requirements.txt

# 3단계: 버전 확인
pip list | grep -E "fastapi|uvicorn|qrcode"
```

### 문제 3: "Alias already in use"

**원인**: 같은 이름의 alias가 이미 존재

**해결**:
- 다른 alias 이름 사용
- 또는 기본 자동 생성 사용 (alias 필드 비우기)

### 문제 4: QR 코드 이미지가 깨짐

**원인**: QR 파일이 생성되지 않음

**해결**:
```bash
# 1단계: outputs 디렉토리 확인
ls -la outputs/qr_codes/

# 2단계: 권한 확인
# Windows: 폴더 속성 → 보안
# Linux/Mac: chmod 755 outputs/qr_codes/

# 3단계: 디스크 공간 확인
df -h
```

### 문제 5: 포트 8000이 이미 사용 중

**원인**: 다른 프로세스가 포트 사용 중

**해결 방법 1**: 다른 포트 사용
```bash
uvicorn app:app --port 3000
```

**해결 방법 2**: 기존 프로세스 종료
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

---

## 📞 추가 지원

문제가 해결되지 않으면:

1. **로그 확인**: 서버 콘솔의 에러 메시지 확인
2. **README.md 참고**: `src/backend/CLAUDE.md` 개발 가이드 확인
3. **데이터베이스 상태**: `outputs/urls.db` SQLite 확인
   ```bash
   sqlite3 outputs/urls.db
   > .tables
   > SELECT COUNT(*) FROM urls;
   ```

---

**마지막 업데이트**: 2024년 4월 7일  
**버전**: 1.0.0
