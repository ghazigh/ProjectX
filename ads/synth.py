"""Tiny deterministic music synth (pure Python, no deps) for ad drafts.

Builds a beat-grid track per concept: kick, hats, snare, sub drone, pad,
risers and impacts, then writes 16-bit mono WAV.
"""
import math, random, struct, wave

SR = 44100


class Track:
    def __init__(self, seconds, seed=7):
        self.n = int(seconds * SR)
        self.buf = [0.0] * self.n
        self.rng = random.Random(seed)

    def _add(self, start, samples):
        i0 = int(start * SR)
        for k, v in enumerate(samples):
            i = i0 + k
            if 0 <= i < self.n:
                self.buf[i] += v

    def kick(self, t, gain=0.9, f0=120, f1=42, dec=0.32):
        out, ph = [], 0.0
        for k in range(int(dec * SR * 1.6)):
            x = k / SR
            f = f1 + (f0 - f1) * math.exp(-x * 28)
            ph += 2 * math.pi * f / SR
            out.append(gain * math.sin(ph) * math.exp(-x / dec * 2.6))
        self._add(t, out)

    def hat(self, t, gain=0.12, dec=0.045):
        r = self.rng
        prev, out = 0.0, []
        for k in range(int(dec * SR * 3)):
            w = r.uniform(-1, 1)
            hp = w - prev  # crude high-pass
            prev = w
            out.append(gain * hp * math.exp(-(k / SR) / dec))
        self._add(t, out)

    def snare(self, t, gain=0.45, dec=0.14):
        r = self.rng
        out, ph = [], 0.0
        for k in range(int(dec * SR * 3)):
            x = k / SR
            ph += 2 * math.pi * 190 / SR
            out.append(gain * (0.55 * r.uniform(-1, 1) + 0.45 * math.sin(ph)) * math.exp(-x / dec))
        self._add(t, out)

    def riser(self, t0, t1, gain=0.35):
        r = self.rng
        n, out, lp = int((t1 - t0) * SR), [], 0.0
        for k in range(n):
            p = k / n
            a = 0.02 + 0.6 * p  # filter opens as it rises
            lp += a * (r.uniform(-1, 1) - lp)
            out.append(gain * lp * (p ** 2.2))
        self._add(t0, out)

    def impact(self, t, gain=1.0):
        self.kick(t, gain=gain, f0=160, f1=35, dec=0.9)
        r = self.rng
        out, lp = [], 0.0
        for k in range(int(1.6 * SR)):
            x = k / SR
            lp += 0.08 * (r.uniform(-1, 1) - lp)
            out.append(0.5 * gain * lp * math.exp(-x / 0.35))
        self._add(t, out)

    def tone(self, t0, t1, freqs, gain=0.08, attack=0.8, release=1.2, detune=0.003):
        n = int((t1 - t0) * SR)
        out = [0.0] * n
        for f in freqs:
            for d in (-detune, detune):
                ff, ph = f * (1 + d), 0.0
                inc = 2 * math.pi * ff / SR
                for k in range(n):
                    ph += inc
                    out[k] += math.sin(ph)
        norm = gain / (2 * len(freqs))
        for k in range(n):
            x = k / SR
            env = min(1.0, x / attack) * min(1.0, (t1 - t0 - x) / release if release else 1.0)
            out[k] *= norm * max(0.0, env)
        self._add(t0, out)

    def write(self, path, peak=0.89):
        m = max(1e-9, max(abs(v) for v in self.buf))
        g = peak / m
        with wave.open(path, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, v * g)) * 32767)) for v in self.buf))


def chrome_x(path):  # 120 BPM, 15 s
    T, b = Track(15, 11), 0.5
    T.tone(0, 15, [41.2, 61.7], gain=0.16, attack=2.5, release=2)          # sub drone (E1/B1)
    T.tone(0.5, 4.5, [164.8, 246.9, 329.6], gain=0.05, attack=2.5, release=0.3)
    T.riser(2.2, 4.5, 0.4)
    T.impact(4.5)
    for i in range(12):  # 4.5 .. 10.5
        t = 4.5 + i * b
        if i: T.kick(t, 0.7)
        T.hat(t + b / 2, 0.1)
    for t in (5.0, 6.5, 8.0, 9.5):
        T.snare(t, 0.3)
    T.tone(4.5, 11, [82.4, 123.5, 164.8, 207.7], gain=0.06, attack=0.4, release=0.8)
    T.riser(9.6, 11, 0.3)
    T.impact(11, 0.9)
    T.tone(11, 15, [164.8, 246.9, 329.6, 415.3], gain=0.07, attack=0.2, release=3)
    T.write(path)


def tunnel(path):  # 128 BPM, 14 s
    T, b = Track(14, 23), 60 / 128
    t = 0.0
    while t < 7.0:  # four-on-the-floor build
        T.kick(t, 0.8)
        T.hat(t + b / 2, 0.06 + 0.1 * t / 7)
        if t > 3.2:
            T.hat(t + b / 4, 0.05); T.hat(t + 3 * b / 4, 0.05)
        t += b
    T.tone(0, 7, [55, 82.4], gain=0.14, attack=1.5, release=0.1)
    for k in range(8):  # word cuts: snare stabs
        T.snare(3.3 + k * b, 0.5)
    T.riser(7.2, 9.9, 0.45)
    T.tone(7.2, 9.9, [110, 164.8, 220], gain=0.06, attack=1.5, release=0.2)
    T.impact(9.9, 1.0)
    T.tone(9.9, 14, [110, 164.8, 220, 277.2], gain=0.07, attack=0.1, release=3)
    T.write(path)


def hours(path):  # 100 BPM, 15 s, ambient
    T, b = Track(15, 5), 0.6
    T.tone(0, 15, [73.4, 110], gain=0.13, attack=3, release=2)
    T.tone(0, 7, [293.7, 440, 587.3], gain=0.035, attack=3, release=1.5)
    t = 3.0
    while t < 7.0:  # soft heartbeat while the loops circle
        T.kick(t, 0.35, f0=90, f1=40, dec=0.25); t += b
    T.riser(5.6, 7.0, 0.3)
    T.impact(7.0, 0.6)
    t = 7.0
    while t < 10.2:
        T.kick(t, 0.6); T.hat(t + b / 2, 0.09); t += b
    T.tone(7, 10.4, [146.8, 220, 293.7, 370], gain=0.05, attack=0.3, release=0.5)
    T.riser(9.2, 10.4, 0.35)
    T.impact(10.4, 1.0)
    T.tone(10.4, 15, [146.8, 220, 293.7, 440], gain=0.07, attack=0.1, release=3)
    T.write(path)
