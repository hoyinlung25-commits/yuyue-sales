#!/usr/bin/env python3
"""Generate 《絕處．重生》 demo track — Cantonese heavy metal instrumental + TTS vocals."""

import math
import subprocess
import wave
from pathlib import Path

import numpy as np
from scipy import signal

SR = 44100
OUT_DIR = Path(__file__).parent
WAV_PATH = OUT_DIR / "jue-chu-chong-sheng-instrumental.wav"
FINAL_PATH = OUT_DIR / "jue-chu-chong-sheng.mp3"

# Section boundaries (seconds)
S1_END = 32
S2_END = 78
S3_END = 118
S4_END = 165
TOTAL = S4_END


def t(length: float) -> np.ndarray:
    return np.linspace(0, length, int(SR * length), endpoint=False)


def env(adsr, n_samples: int) -> np.ndarray:
    a, d, s, r = adsr
    a_n = max(1, int(a * SR))
    d_n = max(1, int(d * SR))
    r_n = max(1, int(r * SR))
    sustain_n = max(0, n_samples - a_n - d_n - r_n)
    e = np.concatenate(
        [
            np.linspace(0, 1, a_n, endpoint=False),
            np.linspace(1, s, d_n, endpoint=False),
            np.full(sustain_n, s),
            np.linspace(s, 0, r_n, endpoint=False),
        ]
    )
    if len(e) < n_samples:
        e = np.pad(e, (0, n_samples - len(e)))
    return e[:n_samples]


def soft_clip(x: np.ndarray, drive: float = 2.5) -> np.ndarray:
    return np.tanh(drive * x)


def lowpass(x: np.ndarray, cutoff: float, order: int = 4) -> np.ndarray:
    nyq = SR / 2
    wn = min(0.99, cutoff / nyq)
    b, a = signal.butter(order, wn, btype="low")
    return signal.filtfilt(b, a, x)


def highpass(x: np.ndarray, cutoff: float, order: int = 2) -> np.ndarray:
    nyq = SR / 2
    wn = max(0.001, cutoff / nyq)
    b, a = signal.butter(order, wn, btype="high")
    return signal.filtfilt(b, a, x)


def reverb(x: np.ndarray, decay: float = 0.35, mix: float = 0.25) -> np.ndarray:
  delays = [0.029, 0.037, 0.053, 0.067]
  wet = np.zeros_like(x)
  for d in delays:
      n = int(d * SR)
      if n < len(x):
          shifted = np.pad(x[:-n], (n, 0))
          wet += shifted * decay
  wet = lowpass(wet, 4000)
  return (1 - mix) * x + mix * wet


def note_freq(midi: int) -> float:
    return 440.0 * (2 ** ((midi - 69) / 12))


def osc(freq: float, length: float, kind: str = "saw") -> np.ndarray:
    phase = 2 * np.pi * freq * t(length)
    if kind == "sine":
        return np.sin(phase)
    if kind == "square":
        return signal.square(phase)
    return signal.sawtooth(phase)


def kick(length: float = 0.18, amp: float = 0.9) -> np.ndarray:
    n = int(SR * length)
    tt = t(length)
    pitch = np.linspace(85, 42, n)
    body = np.sin(2 * np.pi * np.cumsum(pitch) / SR)
    click = highpass(np.random.randn(n) * np.exp(-tt * 90), 1200) * 0.25
    e = env((0.001, 0.04, 0.0, 0.08), n)
    return (body * 0.85 + click) * e * amp


def snare(length: float = 0.14, amp: float = 0.55) -> np.ndarray:
    n = int(SR * length)
    tt = t(length)
    noise = np.random.randn(n)
    tone = np.sin(2 * np.pi * 180 * tt) * np.exp(-tt * 35)
    e = env((0.001, 0.02, 0.0, 0.08), n)
    return (noise * 0.7 + tone * 0.4) * e * amp


def hihat(length: float = 0.05, amp: float = 0.18, open_hat: bool = False) -> np.ndarray:
    n = int(SR * length)
    tt = t(length)
    noise = highpass(np.random.randn(n), 7000)
    decay = 18 if open_hat else 55
    e = env((0.001, 0.005, 0.0, length * 0.8), n)
    return noise * np.exp(-tt * decay) * e * amp


def crash(length: float = 1.2, amp: float = 0.35) -> np.ndarray:
    n = int(SR * length)
    tt = t(length)
    noise = highpass(np.random.randn(n), 5000)
    e = np.exp(-tt * 2.2)
    return noise * e * amp


def guitar_power(midi_root: int, length: float, palm_mute: bool = False, amp: float = 0.35) -> np.ndarray:
    freqs = [note_freq(midi_root), note_freq(midi_root + 7)]
    n = int(SR * length)
    raw = np.zeros(n)
    for f in freqs:
        raw += osc(f, length, "saw") * 0.5
    raw += osc(note_freq(midi_root - 12), length, "sine") * 0.25
    if palm_mute:
        raw = lowpass(raw, 900)
        raw *= env((0.002, 0.01, 0.6, 0.03), n)
    else:
        raw = lowpass(raw, 3200)
        raw *= env((0.005, 0.05, 0.7, 0.12), n)
    return soft_clip(raw, 3.5 if palm_mute else 2.2) * amp


def lead_note(midi: int, length: float, amp: float = 0.22) -> np.ndarray:
    f = note_freq(midi)
    n = int(SR * length)
    vibrato = 1 + 0.004 * np.sin(2 * np.pi * 5.5 * t(length))
    phase = np.cumsum(vibrato) / len(vibrato)
    mod = np.sin(2 * np.pi * f * t(length) * phase)
    raw = mod + osc(f * 2, length, "sine") * 0.08
    raw *= env((0.02, 0.08, 0.75, 0.15), n)
    return raw * amp


def pad_chord(midis, length: float, amp: float = 0.12) -> np.ndarray:
    n = int(SR * length)
    raw = np.zeros(n)
    for m in midis:
        raw += osc(note_freq(m), length, "sine") * 0.35
        raw += osc(note_freq(m), length, "saw") * 0.08
    raw = lowpass(raw, 1800)
    raw *= env((0.4, 0.5, 0.8, 0.6), n)
    return raw * amp


def place(buf: np.ndarray, start: float, clip: np.ndarray) -> None:
    i = int(start * SR)
    end = i + len(clip)
    if i < 0:
        clip = clip[-i:]
        i = 0
    if end > len(buf):
        clip = clip[: len(buf) - i]
        end = len(buf)
    buf[i:end] += clip


def section1_desair(buf: np.ndarray) -> None:
    bpm = 72
    beat = 60 / bpm
    progression = [50, 57, 53, 55]  # Dm Am F G-ish (midi)
    for bar in range(8):
        root = progression[bar % 4]
        start = bar * 4 * beat
        place(buf, start, pad_chord([root, root + 4, root + 7], 4 * beat, 0.14))
        for b in range(4):
            bs = start + b * beat
            place(buf, bs, kick(0.2, 0.45))
            place(buf, bs + beat * 0.5, hihat(0.04, 0.08))
        if bar % 2 == 1:
            place(buf, start + beat * 2.5, guitar_power(root, beat * 1.2, palm_mute=False, amp=0.12))


def section2_hell(buf: np.ndarray) -> None:
    bpm = 148
    beat = 60 / bpm
    bars = 12
    roots = [38, 38, 41, 36, 38, 34, 36, 38, 41, 36, 34, 31]
    for bar in range(bars):
        root = roots[bar]
        start = S1_END + bar * 4 * beat
        if bar == 0:
            place(buf, start, crash(1.0, 0.45))
        for eighth in range(8):
            t0 = start + eighth * beat / 2
            if eighth % 2 == 0:
                place(buf, t0, kick(0.16, 0.95))
            else:
                place(buf, t0, kick(0.12, 0.55))
            if eighth % 4 == 2:
                place(buf, t0, snare(0.12, 0.7))
            place(buf, t0, hihat(0.035, 0.14 if eighth % 2 == 0 else 0.1))
        for chug in range(8):
            t0 = start + chug * beat / 2
            place(buf, t0, guitar_power(root, beat / 2 * 0.9, palm_mute=True, amp=0.42))
        if bar in (3, 7):
            # breakdown half-time
            place(buf, start + beat * 2, guitar_power(root - 12, beat * 1.8, palm_mute=False, amp=0.55))
        if bar == 11:
            place(buf, start + beat * 2, crash(1.4, 0.5))


def section3_fly(buf: np.ndarray) -> None:
    bpm_start, bpm_end = 88, 118
    beats = 16
    melody = [62, 64, 67, 69, 71, 74, 76, 78, 76, 74, 71, 69, 67, 64, 62, 59]
    for i in range(beats):
        frac = i / max(1, beats - 1)
        bpm = bpm_start + (bpm_end - bpm_start) * frac
        beat = 60 / bpm
        start = S2_END + i * beat
        place(buf, start, lead_note(melody[i], beat * 0.85, 0.28))
        place(buf, start, pad_chord([melody[i] - 12, melody[i] - 7, melody[i] - 3], beat, 0.08 + 0.06 * frac))
        if i % 2 == 0:
            place(buf, start, kick(0.15, 0.35 + 0.2 * frac))
        place(buf, start + beat * 0.5, hihat(0.04, 0.06))


def section4_rebirth(buf: np.ndarray) -> None:
    bpm = 108
    beat = 60 / bpm
    progression = [55, 62, 60, 57, 55, 62, 64, 67]
    melody = [67, 69, 71, 69, 67, 64, 62, 67, 69, 71, 74, 71, 69, 67, 64, 62]
    bars = 10
    for bar in range(bars):
        root = progression[bar % len(progression)]
        start = S3_END + bar * 4 * beat
        place(buf, start, pad_chord([root, root + 4, root + 7], 4 * beat, 0.1))
        for b in range(4):
            bs = start + b * beat
            place(buf, bs, kick(0.18, 0.65))
            place(buf, bs + beat * 0.5, snare(0.1, 0.45))
            place(buf, bs + beat * 0.25, hihat(0.03, 0.1))
            place(buf, bs + beat * 0.75, hihat(0.03, 0.1))
        for q in range(4):
            qs = start + q * beat
            place(buf, qs, guitar_power(root, beat * 0.95, palm_mute=(q % 2 == 0), amp=0.28))
            if bar < 8:
                place(buf, qs + beat * 0.5, lead_note(melody[bar * 2 + (q // 2)] if bar * 4 + q < len(melody) else root + 12, beat * 0.45, 0.2))


def build_instrumental() -> np.ndarray:
    n = int(TOTAL * SR)
    buf = np.zeros(n)
    # rain / room tone
    rain = lowpass(np.random.randn(n) * 0.015, 1200)
    buf += rain
    section1_desair(buf)
    section2_hell(buf)
    section3_fly(buf)
    section4_rebirth(buf)
    buf = reverb(buf, 0.3, 0.22)
    # fade in/out
    fade = int(2 * SR)
    ramp = np.linspace(0, 1, fade)
    buf[:fade] *= ramp
    buf[-fade:] *= ramp[::-1]
    peak = np.max(np.abs(buf)) or 1
    return np.clip(buf / peak * 0.92, -1, 1)


def write_wav(path: Path, audio: np.ndarray) -> None:
    pcm = (audio * 32767).astype(np.int16)
    with wave.open(str(path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(pcm.tobytes())


VOCAL_CUES = [
    (2.0, "白紙寫滿，醫生唔再講嘅字。我仲未活夠，點解先要知死期。"),
    (10.0, "病房燈光，照唔透我嘅明天。藥丸一粒粒，數住剩低幾天。"),
    (22.0, "天台上，風扯開我件衫。閉眼一刻，以為終於可以安靜。"),
    (36.0, "火！火燒穿個天靈蓋！煉獄門，關唔埋！"),
    (52.0, "地獄唔係懲罰，係逼你面對，你仲未做完嘅事！"),
    (82.0, "忽然輕了。魂被拋出去，拋過烈火，拋過叫喊。"),
    (98.0, "雲裂開，光唔刺眼。諸神靜靜坐，唔審判，唔責罵。"),
    (112.0, "絕症係身體，唔係你條命。絕處未必係絕路。"),
    (130.0, "我從地獄飛過天，先學會點樣落地。每一日，都係我揀嘅。"),
    (150.0, "絕處重生。唔係神蹟，係一個少年，終於肯為自己活一次。我，仲在。"),
]


def generate_vocals() -> Path:
    vocal_dir = OUT_DIR / "vocal_parts"
    vocal_dir.mkdir(exist_ok=True)
    parts = []
    for idx, (start, text) in enumerate(VOCAL_CUES):
        part = vocal_dir / f"vocal_{idx:02d}.mp3"
        rate = "-8%" if idx < 3 else ("+5%" if 3 <= idx <= 5 else "-5%")
        pitch = "-4Hz" if idx < 3 else ("+2Hz" if 3 <= idx <= 5 else "+0Hz")
        subprocess.run(
            [
                "edge-tts",
                "--voice",
                "zh-HK-WanLungNeural",
                f"--rate={rate}",
                f"--pitch={pitch}",
                "--text",
                text,
                "--write-media",
                str(part),
            ],
            check=True,
        )
        parts.append((start, part))
    return parts


def mix_final(instrumental: Path, vocal_parts: list) -> None:
    from pydub import AudioSegment

    mix = AudioSegment.from_wav(str(instrumental)) - 2
    for start, part in vocal_parts:
        v = AudioSegment.from_file(str(part)) - 4
        if start < S1_END + 5:
            v = v - 2
        elif S1_END <= start < S2_END:
            v = v + 4  # louder in hell
        else:
            v = v + 1
        mix = mix.overlay(v, position=int(start * 1000))
    mix.export(str(FINAL_PATH), format="mp3", bitrate="192k")


def main() -> None:
    print("Generating instrumental...")
    audio = build_instrumental()
    write_wav(WAV_PATH, audio)
    print(f"Wrote {WAV_PATH}")

    print("Generating Cantonese vocals (zh-HK-WanLungNeural)...")
    vocal_parts = generate_vocals()

    print("Mixing final track...")
    mix_final(WAV_PATH, vocal_parts)
    print(f"Done: {FINAL_PATH}")


if __name__ == "__main__":
    main()
