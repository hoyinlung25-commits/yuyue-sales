"""Shared CJK fonts for marketing posters."""

from pathlib import Path

from PIL import ImageFont

FONTS_DIR = Path(__file__).parent / "fonts"

CANDIDATES = [
    FONTS_DIR / "WenQuanYiMicroHei.ttc",
    FONTS_DIR / "NotoSansTC-Bold.otf",
    FONTS_DIR / "NotoSansTC-Regular.otf",
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
]


def poster_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    del bold  # same file; weight via size in layout
    for path in CANDIDATES:
        p = Path(path)
        if p.is_file():
            return ImageFont.truetype(str(p), size)
    raise RuntimeError("No CJK font found in marketing/fonts/ or system.")

