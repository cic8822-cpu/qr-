const API_BASE = 'http://localhost:8000';

let currentShortCode = '';
let currentQRUrl = '';

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('urlForm');
    form.addEventListener('submit', handleSubmit);
});

async function handleSubmit(e) {
    e.preventDefault();
    
    const originalUrl = document.getElementById('originalUrl').value.trim();
    const customAlias = document.getElementById('customAlias').value.trim();
    const expiresInDays = parseInt(document.getElementById('expiresInDays').value) || 30;
    const qrSize = parseInt(document.getElementById('qrSize').value) || 300;
    
    if (!originalUrl) {
        showError('URL을 입력해주세요.');
        return;
    }
    
    hideError();
    setLoading(true);
    
    try {
        const response = await fetch(`${API_BASE}/create`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                original_url: originalUrl,
                custom_alias: customAlias || "",
                expires_in_days: expiresInDays,
                qr_size: qrSize
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '생성 실패');
        }
        
        const data = await response.json();
        displayResult(data);
        
    } catch (error) {
        showError(error.message);
    } finally {
        setLoading(false);
    }
}

function displayResult(data) {
    currentShortCode = data.short_code;
    
    const shortUrlInput = document.getElementById('shortUrl');
    const originalUrlInput = document.getElementById('originalUrlResult');
    const qrImage = document.getElementById('qrImage');
    const clickCount = document.getElementById('clickCount');
    
    shortUrlInput.value = data.short_url;
    originalUrlInput.value = data.original_url;
    
    currentQRUrl = `${API_BASE}/qr/${data.short_code}`;
    qrImage.src = currentQRUrl;
    
    clickCount.textContent = '0';
    
    document.getElementById('resultSection').classList.remove('hidden');
    
    setTimeout(refreshStats, 1000);
}

async function refreshStats() {
    if (!currentShortCode) return;
    
    try {
        const response = await fetch(`${API_BASE}/stats/${currentShortCode}`);
        
        if (response.ok) {
            const data = await response.json();
            document.getElementById('clickCount').textContent = data.click_count || 0;
        }
    } catch (error) {
        console.error('Stats refresh failed:', error);
    }
}

function copyToClipboard(inputId) {
    const input = document.getElementById(inputId);
    input.select();
    input.setSelectionRange(0, 99999);
    
    navigator.clipboard.writeText(input.value).then(() => {
        alert('클립보드에 복사되었습니다.');
    }).catch(err => {
        console.error('Copy failed:', err);
    });
}

function downloadQR(format) {
    if (!currentQRUrl) return;
    
    if (format === 'png') {
        const link = document.createElement('a');
        link.href = currentQRUrl;
        link.download = `qr-${currentShortCode}.png`;
        link.click();
    } else if (format === 'svg') {
        fetch(`${API_BASE}/qr/${currentShortCode}?svg=true`)
            .then(response => response.text())
            .then(svgContent => {
                const blob = new Blob([svgContent], { type: 'image/svg+xml' });
                const url = URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.download = `qr-${currentShortCode}.svg`;
                link.click();
                URL.revokeObjectURL(url);
            })
            .catch(err => {
                console.error('SVG download failed:', err);
            });
    }
}

function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}

function hideError() {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.classList.add('hidden');
}

function setLoading(loading) {
    const submitBtn = document.querySelector('#urlForm button[type="submit"]');
    if (loading) {
        submitBtn.disabled = true;
        submitBtn.textContent = '생성 중...';
    } else {
        submitBtn.disabled = false;
        submitBtn.textContent = '생성하기';
    }
}

setInterval(refreshStats, 10000);