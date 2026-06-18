#!/usr/bin/env bash
# Build seamless 15s / 30s loop videos from the-moon-main-scene.png
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCENE="$ROOT/assets/the-moon/the-moon-main-scene.png"
OUT_DIR="$ROOT/assets/the-moon"
SMOKE_DIR="/tmp/smoke_frames_the_moon"

mkdir -p "$SMOKE_DIR"

echo ">> Generating smoke overlay frames..."
python3 << PY
import math
from PIL import Image, ImageDraw, ImageFilter
import os

w, h = 1920, 1080
frames = 150
out = "$SMOKE_DIR"
for f in range(frames):
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    t = f / frames
    for i in range(15):
        x = int((w * 0.25 + i * 130 + 50 * math.sin(t * 2 * math.pi + i * 0.7)) % w)
        y = int((h * 0.5 + 40 * math.sin(t * 2 * math.pi * 0.5 + i)) - f * 1.8) % h
        r = 70 + int(25 * math.sin(t * 2 * math.pi + i))
        alpha = int(14 + 8 * math.sin(t * 2 * math.pi + i * 0.6))
        draw.ellipse((x-r, y-r, x+r, y+r), fill=(190, 175, 230, alpha))
    img = img.filter(ImageFilter.GaussianBlur(30))
    img.save(f'{out}/smoke_{f:04d}.png')
print(f'Smoke frames: {frames}')
PY

ffmpeg -y -framerate 30 -i "$SMOKE_DIR/smoke_%04d.png" -c:v libx264 -pix_fmt yuv420p -t 5 /tmp/smoke_overlay_5s.mp4

echo ">> Rendering 30s seamless loop..."
ffmpeg -y -loop 1 -i "$SCENE" \
  -stream_loop -1 -i /tmp/smoke_overlay_5s.mp4 \
  -filter_complex "[0:v]scale=2560:1440:force_original_aspect_ratio=increase,crop=2560:1440,zoompan=z='1.035+0.018*sin(2*PI*on/900)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=900:s=1920x1080:fps=30,eq=brightness='0.035*sin(2*PI*t/3)+0.015*sin(2*PI*t/1.77)':contrast=1.03:saturation='1.04+0.03*sin(2*PI*t/15)',noise=alls=5:allf=t+u[base];[1:v]scale=1920:1080,format=yuva420p,colorchannelmixer=aa=0.35[smoke];[base][smoke]overlay=0:0:format=auto,format=yuv420p" \
  -t 30 -c:v libx264 -preset medium -crf 17 -movflags +faststart \
  "$OUT_DIR/the-moon-loop-30s.mp4"

echo ">> Cutting 15s version..."
ffmpeg -y -i "$OUT_DIR/the-moon-loop-30s.mp4" -t 15 -c:v libx264 -preset medium -crf 17 -movflags +faststart \
  "$OUT_DIR/the-moon-loop-15s.mp4"

echo ">> Done:"
ls -lh "$OUT_DIR"/the-moon-loop-*.mp4
