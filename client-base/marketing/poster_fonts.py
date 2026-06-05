"""Shared CJK fonts for marketing posters (bundled + system fallbacks)."""

from pathlib import Path

from PIL import ImageFont

FONTS_DIR = Path(__file__).parent / "fonts"

BUNDLED = [
    FONTS_DIR / "NotoSansTC-Regular.otf",
    FONTS_DIR / "NotoSansTC-Bold.otf",
    FONTS_DIR / "WenQuanYiMicroHei.ttc",
]

SYSTEM = [
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
]


def poster_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    for bundled in BUNDLED:
        if bundled.is_file():
            return ImageFont.truetype(str(bundled), size)

    for path in SYSTEM:
        p = Path(path)
        if p.is_file():
            try:
                return ImageFont.truetype(str(p), size)
            except OSError:
                continue

    raise RuntimeError(
        "No CJK font found. Run compose script after fonts are in marketing/fonts/, "
        "or install fonts-noto-cjk / fonts-wqy-microhei."
    )
