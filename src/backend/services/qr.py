import qrcode
import io
import base64
from pathlib import Path
from PIL import Image
import os

# 사용자 홈 디렉토리에 표준화된 경로로 저장
OUTPUT_DIR = Path(os.path.expanduser("~")) / ".qr_generator" / "qr_codes"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_qr_image(
    url: str, size: int = 300, fill_color: str = "black", back_color: str = "white"
) -> Image.Image:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")

    img = img.resize((size, size), Image.LANCZOS)
    return img


def generate_qr_base64(
    url: str, size: int = 300, fill_color: str = "black", back_color: str = "white"
) -> str:
    img = generate_qr_image(url, size, fill_color, back_color)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()


def save_qr_file(short_code: str, url: str, size: int = 300) -> Path:
    img = generate_qr_image(url, size)
    file_path = OUTPUT_DIR / f"{short_code}.png"
    img.save(file_path, format="PNG")
    return file_path


def get_qr_path(short_code: str) -> Path | None:
    file_path = OUTPUT_DIR / f"{short_code}.png"
    return file_path if file_path.exists() else None


def generate_qr_svg(url: str, size: int = 300) -> str:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    matrix = qr.get_matrix()
    cell_size = size // len(matrix)
    border_size = 4 * cell_size

    svg_parts = []
    svg_parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
    )
    svg_parts.append(f'<rect width="{size}" height="{size}" fill="white"/>')

    for row_idx, row in enumerate(matrix):
        for col_idx, cell in enumerate(row):
            if cell:
                x = border_size + col_idx * cell_size
                y = border_size + row_idx * cell_size
                svg_parts.append(
                    f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="black"/>'
                )

    svg_parts.append("</svg>")
    return "".join(svg_parts)
