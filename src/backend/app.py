from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from typing import Optional
from pydantic import field_validator
import webbrowser
import threading
import time
import sys
import os
from services.shortener import generate_short_code, format_expiry, is_expired
from services import qr as qr_service
from services import analytics as analytics_service
from database import init_db, create_url, get_url_by_code, get_url_by_alias, get_stats
import uvicorn

app = FastAPI(title="QR ShortLink Generator")

# PyInstaller 번들 환경 감지
if getattr(sys, 'frozen', False):
    # PyInstaller로 번들된 EXE 실행 중
    # sys._MEIPASS: PyInstaller가 임시로 추출한 디렉토리
    BASE_DIR = Path(sys._MEIPASS)
    FRONTEND_DIR = BASE_DIR / "frontend"
else:
    # 일반 Python 개발 환경
    BACKEND_DIR = Path(__file__).resolve().parent  # src/backend
    SRC_DIR = BACKEND_DIR.parent  # src
    FRONTEND_DIR = SRC_DIR / "frontend"


class URLCreate(BaseModel):
    original_url: str
    custom_alias: Optional[str] = None
    expires_in_days: int = 30
    qr_size: int = 300

    @field_validator('custom_alias', mode='before')
    @classmethod
    def validate_custom_alias(cls, v):
        # 빈 문자열을 None으로 변환
        return v if v and isinstance(v, str) and v.strip() else None


@app.get("/", response_class=HTMLResponse)
def root():
    """메인 페이지 반환"""
    index_path = FRONTEND_DIR / "index.html"
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return "<h1>QR ShortLink Generator API</h1>"


@app.get("/api/styles.css")
def get_styles():
    """CSS 파일 반환"""
    css_path = FRONTEND_DIR / "styles.css"
    if css_path.exists():
        return FileResponse(css_path, media_type="text/css")
    return {"error": "CSS not found"}


@app.get("/api/app.js")
def get_script():
    """JavaScript 파일 반환"""
    js_path = FRONTEND_DIR / "app.js"
    if js_path.exists():
        return FileResponse(js_path, media_type="application/javascript")
    return {"error": "JS not found"}


@app.on_event("startup")
def startup():
    init_db()


@app.post("/create")
def create_shortlink(data: URLCreate):
    if not data.original_url.startswith(("http://", "https://")):
        data.original_url = "https://" + data.original_url

    if data.custom_alias:
        existing = get_url_by_alias(data.custom_alias)
        if existing:
            raise HTTPException(status_code=400, detail="Alias already in use")
        short_code = data.custom_alias
    else:
        short_code = generate_short_code()

    expires_at = format_expiry(data.expires_in_days) if data.expires_in_days else None

    create_url(data.original_url, short_code, data.custom_alias, expires_at)

    short_url = f"http://localhost:8000/{short_code}"
    qr_path = qr_service.save_qr_file(short_code, short_url, data.qr_size)

    return {
        "short_code": short_code,
        "short_url": short_url,
        "original_url": data.original_url,
        "qr_code_url": f"/qr/{short_code}",
        "expires_at": expires_at,
    }


@app.get("/qr/{short_code}")
def get_qr_image(short_code: str):
    qr_path = qr_service.get_qr_path(short_code)
    if not qr_path:
        raise HTTPException(status_code=404, detail="QR code not found")
    return FileResponse(qr_path, media_type="image/png")


@app.get("/{short_code}")
def redirect_to_original(short_code: str, request: Request):
    # 파일 확장자가 있으면 404 반환
    if "." in short_code or short_code in ("static", "api", "docs", "openapi.json"):
        raise HTTPException(status_code=404, detail="URL not found")
    url_data = get_url_by_code(short_code)

    if not url_data:
        raise HTTPException(status_code=404, detail="URL not found")

    if url_data.get("expires_at") and is_expired(url_data["expires_at"]):
        raise HTTPException(status_code=410, detail="URL expired")

    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    analytics_service.track_click(short_code, ip_address, user_agent)

    return RedirectResponse(url=url_data["original_url"], status_code=301)


@app.get("/stats/{short_code}")
def get_url_stats(short_code: str):
    stats = get_stats(short_code)
    if not stats:
        raise HTTPException(status_code=404, detail="URL not found")
    return stats


# 정적 파일 마운트
try:
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
except Exception as e:
    print(f"정적 파일 마운트 실패: {e}")


def open_browser_delayed():
    """3초 후 브라우저 열기"""
    try:
        time.sleep(3)  # 서버 완전 시작 대기
        webbrowser.open('http://localhost:8000')
        print("[INFO] Browser opened")
    except Exception as e:
        print(f"[WARN] Browser open failed: {e}")


if __name__ == "__main__":
    # 별도 스레드에서 브라우저 열기
    browser_thread = threading.Thread(target=open_browser_delayed, daemon=True)
    browser_thread.start()

    # 서버 실행
    uvicorn.run(app, host="0.0.0.0", port=8000)
