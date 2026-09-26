"""Showreel soundtrack: 128 BPM, A minor, 15 s, stereo.

Pure-Python synthesis of dry stems (drums, bass, chords, plucks, FX) with
sidechain pumping. ffmpeg then adds a convolution reverb and the master
compressor/limiter. Every sound is placed on the same beat grid the
composition uses, so hits land on cuts.
"""
import math, os, random, subprocess, sys, wave
from array import array

SR = 44100
BPM = 128
B = 60 / BPM            # one beat = 0.46875 s
DUR = 15.0
TAU = 2 * math.pi

NOTE = {'C': -9, 'C#': -8, 'D': -7, 'D#': -6, 'E': -5, 'F': -4, 'F#': -3,
        'G': -2, 'G#': -1, 'A': 0, 'A#': 1, 'B': 2}


def hz(n):
    return 440.0 * 2 ** ((NOTE[n[:-1]] + (int(n[-1]) - 4) * 12) / 12)


def bt(n):
    return n * B


# ---------------------------------------------------------------- buses
class Bus:
    def __init__(self, dur=DUR):
        self.n = int(dur * SR)
        self.L = [0.0] * self.n
        self.R = [0.0] * self.n

    def add(self, t, sig, gain=1.0, pan=0.0):
        a = (pan + 1) * math.pi / 4
        gl, gr = gain * math.cos(a) * 1.41421356, gain * math.sin(a) * 1.41421356
        i0 = int(round(t * SR))
        L, R = self.L, self.R
        k0, k1 = max(0, -i0), min(len(sig), self.n - i0)
        for k in range(k0, k1):
            v = sig[k]
            L[i0 + k] += v * gl
            R[i0 + k] += v * gr

    def add2(self, t, sl, sr, gain=1.0):
        i0 = int(round(t * SR))
        L, R = self.L, self.R
        k1 = min(len(sl), self.n - i0)
        for k in range(max(0, -i0), k1):
            L[i0 + k] += sl[k] * gain
            R[i0 + k] += sr[k] * gain


# ---------------------------------------------------------------- dsp helpers
def svf(sig, cutoff, q=0.707, mode=0, cut_fn=None):
    """Simper TPT state-variable filter. mode 0 low, 1 band, 2 high."""
    k_ = 1.0 / q
    out = [0.0] * len(sig)
    ic1 = ic2 = 0.0

    def co(fc):
        fc = min(max(fc, 18.0), SR * 0.45)
        g = math.tan(math.pi * fc / SR)
        a1 = 1 / (1 + g * (g + k_))
        return a1, g * a1, g * g * a1

    a1, a2, a3 = co(cut_fn(0) if cut_fn else cutoff)
    for i, v0 in enumerate(sig):
        if cut_fn and not (i & 31):
            a1, a2, a3 = co(cut_fn(i))
        v3 = v0 - ic2
        v1 = a1 * ic1 + a2 * v3
        v2 = ic2 + a2 * ic1 + a3 * v3
        ic1 = 2 * v1 - ic1
        ic2 = 2 * v2 - ic2
        out[i] = v2 if mode == 0 else (v1 if mode == 1 else v0 - k_ * v1 - v2)
    return out


def noise(n, seed):
    r = random.Random(seed)
    u = r.uniform
    return [u(-1, 1) for _ in range(n)]


def env_ad(n, a, d, curve=1.0):
    """Linear attack (s), exponential decay time-constant d (s)."""
    na = max(1, int(a * SR))
    out = [0.0] * n
    for k in range(n):
        out[k] = (k / na) if k < na else math.exp(-(k - na) / (d * SR)) ** curve
    return out


def mul(a, b):
    return [x * y for x, y in zip(a, b)]


def sat(sig, drive=1.5):
    t = math.tanh(drive)
    return [math.tanh(drive * v) / t for v in sig]


# ---------------------------------------------------------------- drums
def mk_kick(f0=165, f1=45, pdec=0.032, adec=0.27, dur=0.5, drive=1.8, seed=1):
    n = int(dur * SR)
    r = random.Random(seed)
    out, ph = [0.0] * n, 0.0
    for k in range(n):
        x = k / SR
        ph += TAU * (f1 + (f0 - f1) * math.exp(-x / pdec)) / SR
        v = math.sin(ph) * math.exp(-x / adec)
        if k < 110:
            v += 0.35 * r.uniform(-1, 1) * (1 - k / 110)
        out[k] = v
    return sat(out, drive)


def mk_clap(seed=5):
    n = int(0.42 * SR)
    bp = svf(noise(n, seed), 1250, q=1.1, mode=1)
    hp = svf(bp, 600, mode=2)
    out = [0.0] * n
    for k in range(n):
        x = k / SR
        e = 0.0
        for off in (0.0, 0.0105, 0.021):
            if x >= off:
                e = max(e, math.exp(-(x - off) / 0.0065))
        if x > 0.026:
            e = max(e, 0.62 * math.exp(-(x - 0.026) / 0.085))
        out[k] = hp[k] * e * 2.2
    return out


_HATF = (205.3, 304.4, 369.6, 522.7, 540.0, 800.0)


def mk_hat(dec=0.035, seed=7, tone=1.0):
    n = int(dec * 7 * SR)
    r = random.Random(seed)
    raw = [0.0] * n
    phs = [r.random() for _ in _HATF]
    for k in range(n):
        s = 0.0
        for j, f in enumerate(_HATF):
            p = (phs[j] + f * tone * 7.3 * k / SR) % 1.0
            s += 1.0 if p < 0.5 else -1.0
        raw[k] = s / 6 * 0.6 + r.uniform(-1, 1) * 0.55
    hp = svf(svf(raw, 7200, mode=2), 11000, q=0.9, mode=1)
    return [hp[k] * math.exp(-k / (dec * SR)) * 2.6 for k in range(n)]


def mk_snare(seed=9, dec=0.15, body=188, gain=1.0):
    n = int(dec * 5 * SR)
    nz = svf(svf(noise(n, seed), 1800, mode=2), 5200, q=0.8, mode=1)
    out, ph = [0.0] * n, 0.0
    for k in range(n):
        x = k / SR
        ph += TAU * (body * (1 + 0.35 * math.exp(-x / 0.012))) / SR
        out[k] = gain * (1.5 * nz[k] * math.exp(-x / dec) + 0.55 * math.sin(ph) * math.exp(-x / 0.06))
    return out


def mk_crash(dur=2.2, seed=11, dec=0.75):
    n = int(dur * SR)
    r = random.Random(seed)
    raw = [0.0] * n
    phs = [r.random() for _ in _HATF]
    for k in range(n):
        s = 0.0
        for j, f in enumerate(_HATF):
            p = (phs[j] + f * 3.1 * k / SR) % 1.0
            s += 1.0 if p < 0.5 else -1.0
        raw[k] = s / 6 * 0.35 + r.uniform(-1, 1)
    hp = svf(raw, 4200, mode=2)
    return [hp[k] * math.exp(-k / (dec * SR)) * 0.9 for k in range(n)]


def mk_tom(f0=150, f1=90, dec=0.22):
    n = int(dec * 4 * SR)
    out, ph = [0.0] * n, 0.0
    for k in range(n):
        x = k / SR
        ph += TAU * (f1 + (f0 - f1) * math.exp(-x / 0.05)) / SR
        out[k] = math.sin(ph) * math.exp(-x / dec)
    return sat(out, 1.4)


# ---------------------------------------------------------------- tonal
def saw_voices(freqs, n, voices=5, detune=0.014, seed=3):
    """Detuned saw stack, voices spread across the stereo field."""
    r = random.Random(seed)
    L, R = [0.0] * n, [0.0] * n
    for f in freqs:
        for v in range(voices):
            d = detune * ((v / (voices - 1)) * 2 - 1) if voices > 1 else 0.0
            inc = f * (1 + d) / SR
            p = r.random()
            pan = ((v / (voices - 1)) * 2 - 1) * 0.8 if voices > 1 else 0.0
            gl, gr = math.cos((pan + 1) * math.pi / 4), math.sin((pan + 1) * math.pi / 4)
            for k in range(n):
                p += inc
                if p >= 1.0:
                    p -= 1.0
                s = 2 * p - 1
                L[k] += s * gl
                R[k] += s * gr
    g = 1.0 / (len(freqs) * voices ** 0.5 * 1.4)
    return [x * g for x in L], [x * g for x in R]


def supersaw(freqs, dur, a=0.004, d=0.2, s=0.0, rel=0.05, cut0=5000, cut1=900, cdec=0.12,
             q=0.9, voices=5, detune=0.014, seed=3, cut_fn=None):
    n = int((dur + rel) * SR)
    L, R = saw_voices(freqs, n, voices, detune, seed)
    fn = cut_fn or (lambda i: cut1 + (cut0 - cut1) * math.exp(-(i / SR) / cdec))
    L = svf(L, 0, q=q, cut_fn=fn)
    R = svf(R, 0, q=q, cut_fn=fn)
    na, nd = max(1, int(a * SR)), int(dur * SR)
    for k in range(n):
        if k < na:
            e = k / na
        elif k < nd:
            e = s + (1 - s) * math.exp(-(k - na) / (d * SR))
        else:
            e = (s + (1 - s) * math.exp(-(nd - na) / (d * SR))) * math.exp(-(k - nd) / (rel * SR))
        L[k] *= e
        R[k] *= e
    return L, R


def pluck(f, dur=0.7, bright=0.55, decay=0.9965, seed=17):
    """Karplus-Strong string."""
    r = random.Random(seed)
    N = max(2, int(round(SR / f)))
    buf = [r.uniform(-1, 1) for _ in range(N)]
    for _ in range(2):  # soften the excitation
        buf = [bright * buf[i] + (1 - bright) * buf[i - 1] for i in range(N)]
    n = int(dur * SR)
    out = [0.0] * n
    i = 0
    for k in range(n):
        v = buf[i]
        j = i + 1 if i + 1 < N else 0
        buf[i] = decay * 0.5 * (v + buf[j])
        out[k] = v
        i = j
    fade = int(0.03 * SR)
    for k in range(max(0, n - fade), n):
        out[k] *= (n - k) / fade
    return out


def sine_sweep(f0, f1, dur, dec=None, curve='exp', gain=1.0, attack=0.002):
    n = int(dur * SR)
    out, ph = [0.0] * n, 0.0
    na = max(1, int(attack * SR))
    for k in range(n):
        p = k / n
        f = f0 * (f1 / f0) ** p if curve == 'exp' else f0 + (f1 - f0) * p
        ph += TAU * f / SR
        e = min(1.0, k / na) * (math.exp(-(k / SR) / dec) if dec else math.sin(math.pi * p) ** 0.5)
        out[k] = gain * math.sin(ph) * e
    return out


def bell(f, dur=1.2, ratio=3.5, index=3.2, dec=0.5, idec=0.18):
    n = int(dur * SR)
    out = [0.0] * n
    for k in range(n):
        x = k / SR
        m = index * math.exp(-x / idec) * math.sin(TAU * f * ratio * x)
        out[k] = math.sin(TAU * f * x + m) * math.exp(-x / dec) * min(1.0, k / 60)
    return out


def blip(f, dur=0.09, dec=0.025):
    n = int(dur * SR)
    return [math.sin(TAU * f * k / SR) * math.exp(-(k / SR) / dec) * min(1.0, k / 20) for k in range(n)]


def droplet(f0=520, f1=1500, dur=0.16):
    n = int(dur * SR)
    out, ph = [0.0] * n, 0.0
    for k in range(n):
        x = k / SR
        f = f0 + (f1 - f0) * (1 - math.exp(-x / 0.018))
        ph += TAU * f / SR
        out[k] = math.sin(ph) * math.exp(-x / 0.045) * min(1.0, k / 30)
    return out


def riser(dur, f0=300, f1=7000, seed=21, q=2.0, power=2.2, tone=None):
    n = int(dur * SR)
    fn = lambda i: f0 * (f1 / f0) ** (i / n)
    bp = svf(noise(n, seed), 0, q=q, mode=1, cut_fn=fn)
    out = [0.0] * n
    ph = 0.0
    for k in range(n):
        p = k / n
        v = bp[k] * 1.6
        if tone:
            ph += TAU * (tone[0] * (tone[1] / tone[0]) ** p) / SR
            v += 0.35 * math.sin(ph)
        out[k] = v * p ** power
    return out


def reverse_swell(dur, seed=23, f=2500):
    """A crash played backwards: rises and stops dead on the downbeat."""
    n = int(dur * SR)
    lp = svf(noise(n, seed), f, mode=0)
    return [lp[n - 1 - k] * math.exp(-(n - 1 - k) / (0.33 * SR)) * 1.4 for k in range(n)]


def whoosh(dur, seed=29, f0=400, f1=3000):
    n = int(dur * SR)
    fn = lambda i: f0 + (f1 - f0) * math.sin(math.pi * i / n)
    bp = svf(noise(n, seed), 0, q=1.4, mode=1, cut_fn=fn)
    return [bp[k] * math.sin(math.pi * k / n) ** 1.5 * 1.8 for k in range(n)]


def impact(seed=31, sub=(70, 30), sdec=0.9, big=1.0):
    n = int(2.6 * SR)
    out, ph = [0.0] * n, 0.0
    nz = svf(noise(n, seed), 900, mode=0)
    for k in range(n):
        x = k / SR
        ph += TAU * (sub[1] + (sub[0] - sub[1]) * math.exp(-x / 0.12)) / SR
        out[k] = 0.7 * math.sin(ph) * math.exp(-x / sdec) + 0.9 * nz[k] * math.exp(-x / 0.18) * big
    return sat(out, 1.6)


def splat(seed=37):
    n = int(0.4 * SR)
    fn = lambda i: 6000 * math.exp(-(i / SR) / 0.05) + 350
    lp = svf(noise(n, seed), 0, q=1.2, cut_fn=fn)
    th = mk_tom(110, 55, 0.12)
    return [lp[k] * math.exp(-(k / SR) / 0.09) * 1.5 + (th[k] if k < len(th) else 0) * 0.8 for k in range(n)]


def pop(f0=1100, f1=260, seed=41):
    n = int(0.22 * SR)
    r = random.Random(seed)
    out, ph = [0.0] * n, 0.0
    for k in range(n):
        x = k / SR
        ph += TAU * (f1 + (f0 - f1) * math.exp(-x / 0.012)) / SR
        v = math.sin(ph) * math.exp(-x / 0.055)
        if k < 40:
            v += 0.5 * r.uniform(-1, 1) * (1 - k / 40)
        out[k] = v
    return out


def crush(sig, bits=5, hold=4):
    q = 2 ** (bits - 1)
    out, last = [0.0] * len(sig), 0.0
    for k, v in enumerate(sig):
        if k % hold == 0:
            last = round(v * q) / q
        out[k] = last
    return out


# ---------------------------------------------------------------- arrangement
MIX = (0.58, 0.95, 0.5, 0.46, 2.1, 1.5, 0.9)  # kick perc hats bass chords plucks fx


def build(out_dir):
    kick_b, perc_b, hat_b, bass_b, chord_b, pl_b, fx_b = (Bus() for _ in range(7))
    KICK, KICK2 = mk_kick(), mk_kick(f0=180, f1=42, adec=0.34, seed=2)
    CLAP, SN, SN_S = mk_clap(), mk_snare(), mk_snare(seed=13, dec=0.07, gain=0.7)
    CH = [mk_hat(0.028, 7 + i) for i in range(4)]
    OH = mk_hat(0.16, 19)
    CRASH = mk_crash()
    kicks = []

    def K(beat, g=1.0, big=False):
        kick_b.add(bt(beat), KICK2 if big else KICK, g)
        kicks.append(bt(beat))

    def groove(b0, b1, clap=True, hats16=True, open_hats=True, kick=True, hat_gain=1.0):
        for b in range(b0, b1):
            if kick:
                K(b)
            if clap and b % 2 == 1:
                perc_b.add(bt(b), CLAP, 0.8, 0.05)
            if open_hats:
                hat_b.add(bt(b + 0.5), OH, 0.42 * hat_gain, 0.25)
            if hats16:
                for s, g in ((0.25, 0.32), (0.75, 0.38)):
                    hat_b.add(bt(b + s), CH[(b * 2 + int(s * 4)) % 4], g * hat_gain, 0.35)

    # chord roots per bar (Am | F | G | Am | F | C | G E | Am)
    V = {
        'Am': ['A3', 'C4', 'E4', 'A4'], 'F': ['A3', 'C4', 'F4'], 'G': ['B3', 'D4', 'G4'],
        'C': ['G3', 'C4', 'E4'], 'E': ['G#3', 'B3', 'E4'], 'Am9': ['A3', 'E4', 'A4', 'B4', 'C5'],
    }
    fz = lambda ch: [hz(n) for n in V[ch]]

    # ---- bar 1 (beats 0-3): the dot / principles
    fx_b.add(bt(0), pop(), 0.9)
    fx_b.add(bt(0.01), blip(hz('A5'), 0.5, 0.12), 0.25, 0.2)
    fx_b.add(bt(0.25), sine_sweep(160, 330, bt(0.75), gain=1.0), 0.18)          # wind-up
    fx_b.add(bt(1), sine_sweep(260, 1400, 0.16, dec=0.07), 0.45, -0.1)             # launch
    fx_b.add(bt(1), whoosh(0.4, f0=500, f1=2600), 0.2, -0.3)
    for b_, n_ in ((2, 'A3'), ):
        fx_b.add(bt(b_), mk_tom(210, 120, 0.14), 0.6, 0.0)                         # contact
        pl_b.add(bt(b_), pluck(hz(n_), 0.9, 0.7), 0.55, 0.0)
    fx_b.add(bt(3), splat(), 0.85, 0.2)
    pl_b.add(bt(3), pluck(hz('E4'), 0.9, 0.7, seed=19), 0.45, 0.2)
    fx_b.add(bt(3.02), reverse_swell(bt(0.98)), 0.55)
    for i in range(8):  # ticking 8ths building into bar 2
        hat_b.add(bt(2 + i * 0.25), CH[i % 4], 0.12 + 0.05 * i, 0.3)
    L, R = supersaw(fz('Am'), bt(4), a=bt(3), d=9, s=1, rel=0.02, cut0=500, cut1=1400, cdec=1e9,
                    cut_fn=lambda i: 400 + 1800 * (i / SR / bt(4)) ** 2, voices=5, seed=4)
    chord_b.add2(0, L, R, 0.35)
    subA = sine_sweep(hz('A1'), hz('A1'), bt(4), gain=1.0, attack=bt(2))
    bass_b.add(0, subA, 0.25)

    # ---- bar 2 (beats 4-7): type. Stabs climb with each word.
    groove(4, 8)
    stab_v = [['F3', 'A3', 'C4'], ['A3', 'C4', 'F4'], ['C4', 'F4', 'A4'], ['F4', 'A4', 'C5']]
    for i, notes in enumerate(stab_v):
        L, R = supersaw([hz(n) for n in notes], 0.2, d=0.12, cut0=7000, cut1=900, cdec=0.07, seed=30 + i)
        chord_b.add2(bt(4 + i), L, R, 0.55)
    fx_b.add(bt(7.2), reverse_swell(bt(0.8), seed=24, f=4000), 0.6)          # zoom through the O
    fx_b.add(bt(7.35), whoosh(bt(0.65), f0=300, f1=5000, seed=31), 0.5, 0.0)

    # ---- bar 3 (beats 8-11): shapes. Plucked arp, morph bloops, then the break.
    groove(8, 11)
    K(11)
    perc_b.add(bt(11), CLAP, 0.8)
    arpG = ['G4', 'B4', 'D5', 'G5', 'D5', 'B4', 'D5', 'G5']
    for s in range(10):
        f = hz(arpG[s % 8])
        pl_b.add(bt(8 + s * 0.25), pluck(f, 0.5, 0.6, seed=50 + s), 0.32, (-0.5, 0.5)[s % 2])
    for b in (8, 9, 10, 11):
        fx_b.add(bt(b), sine_sweep(380, 1300, 0.14, dec=0.05), 0.22, 0.1 * (b - 9.5))
    L, R = supersaw(fz('G'), bt(3.5), a=0.01, d=9, s=1, rel=0.01, cut0=900, cut1=900, cdec=1e9,
                    cut_fn=lambda i: 700 + 2600 * (i / SR / bt(3.5)), seed=5)
    chord_b.add2(bt(8), L, R, 0.3)
    fx_b.add(bt(10.9), riser(bt(0.6), 600, 9000, q=3), 0.5)
    fx_b.add(bt(11.5), reverse_swell(bt(0.5), seed=26, f=6000), 0.7)           # the inhale

    # ---- bar 4 (beats 12-15): DROP / 3D
    fx_b.add(bt(12), impact(big=1.0), 0.95)
    perc_b.add(bt(12), CRASH, 0.5, 0.0)
    K(12, 1.0, big=True)
    for b in range(13, 16):
        K(b)
    groove(12, 16, kick=False)
    L, R = supersaw(fz('Am'), bt(4), a=0.01, d=9, s=1, rel=0.03, cut0=5000, cut1=2600, cdec=0.5, seed=6)
    chord_b.add2(bt(12), L, R, 0.5)
    fx_b.add(bt(13), bell(hz('E6'), 1.4, ratio=3.5, index=2.5, dec=0.45), 0.2, 0.3)     # chrome
    fx_b.add(bt(13), bell(hz('A6'), 1.4, ratio=2.01, index=1.2, dec=0.4), 0.14, -0.3)
    shat = [v * math.exp(-(k / SR) / 0.12) for k, v in enumerate(svf(noise(int(0.6 * SR), 57), 2500, mode=2))]
    fx_b.add(bt(14), shat, 0.45, 0.1)                                                  # burst
    r = random.Random(77)
    penta = ['A5', 'C6', 'D6', 'E6', 'G6', 'A6', 'C7']
    for i in range(14):
        tt = bt(14) + (r.random() ** 2) * 0.45
        fx_b.add(tt, blip(hz(penta[r.randrange(len(penta))]), 0.1, 0.02), 0.09, r.uniform(-0.9, 0.9))
    for s, nn in enumerate(['A4', 'C5', 'E5', 'A5']):                                   # helix
        pl_b.add(bt(15 + s * 0.25), pluck(hz(nn), 0.5, 0.65, seed=90 + s), 0.33, (-0.5, 0.5)[s % 2])
    fx_b.add(bt(15.35), reverse_swell(bt(0.65), seed=28, f=5000), 0.6)

    # ---- bar 5 (beats 16-19): particles
    fx_b.add(bt(16), impact(seed=33, sub=(80, 36), sdec=0.5, big=0.6), 0.6)
    K(16, 1.0, big=True)
    for b in range(17, 20):
        K(b)
    groove(16, 20, kick=False)
    r = random.Random(79)
    for i in range(46):  # sparkle cloud from the explosion
        tt = bt(16) + (r.random() ** 1.7) * bt(2.6)
        fx_b.add(tt, blip(hz(penta[r.randrange(len(penta))]) * (1 + r.uniform(-0.004, 0.004)), 0.12, 0.03),
                 0.05 + 0.05 * r.random(), r.uniform(-1, 1))
    L, R = supersaw(fz('F'), bt(4), a=0.01, d=9, s=1, rel=0.03, cut0=4200, cut1=2400, cdec=0.5, seed=7)
    chord_b.add2(bt(16), L, R, 0.45)
    arpF = ['F4', 'A4', 'C5', 'F5', 'C5', 'A4', 'C5', 'A5']
    for s in range(16):
        pl_b.add(bt(16 + s * 0.25), pluck(hz(arpF[s % 8]), 0.45, 0.6, seed=110 + s), 0.24, (-0.6, 0.6)[s % 2])
    fx_b.add(bt(18.2), reverse_swell(bt(0.95), seed=35, f=7000), 0.4)                    # text forms
    fx_b.add(bt(19.1), whoosh(bt(0.9), f0=250, f1=2200, seed=39), 0.4, 0.4)             # blown away

    # ---- bar 6 (beats 20-23): shaders, liquid wah on the pad, droplets on beats
    groove(20, 24)
    L, R = supersaw(fz('C'), bt(4), a=0.02, d=9, s=1, rel=0.03, cut0=0, cut1=0, cdec=1,
                    cut_fn=lambda i: 900 + 2600 * (0.5 + 0.5 * math.sin(TAU * (i / SR) / bt(2) - 1.2)),
                    q=2.2, seed=8)
    chord_b.add2(bt(20), L, R, 0.45)
    drop_notes = ['E6', 'G5', 'C6', 'A5']
    for i, b in enumerate((20, 21, 22, 23)):
        fx_b.add(bt(b), droplet(hz(drop_notes[i]) * 0.5, hz(drop_notes[i]), 0.18), 0.3, (-0.3, 0.3)[i % 2])
    r = random.Random(81)
    for i in range(6):
        fx_b.add(bt(20.5 + i * 0.5 + 0.25 * r.random()), droplet(700 + 600 * r.random(), 1600 + 800 * r.random(), 0.14),
                 0.12, r.uniform(-0.8, 0.8))
    fx_b.add(bt(22.6), riser(bt(1.4), 400, 7000, seed=43, q=2.5, tone=(220, 880)), 0.45)

    # ---- bar 7 (beats 24-27): the edit. Hit per micro-cut, snare roll, riser, V chord.
    for b in (24, 25, 26):
        K(b)
    for b in range(24, 27):
        hat_b.add(bt(b + 0.5), OH, 0.35, 0.25)
    hits = [
        lambda: mk_tom(260, 140, 0.1),
        lambda: crush(bell(hz('A5'), 0.25, 1.5, 4, 0.08), 4, 6),
        lambda: [v * 0.8 for v in blip(hz('E6'), 0.1, 0.03)],
        lambda: crush(svf(noise(int(0.16 * SR), 61), 1200, mode=1, q=3), 3, 9),
        lambda: sine_sweep(2400, 120, 0.1, dec=0.04),
        lambda: mk_tom(180, 95, 0.12),
    ]
    for i, h in enumerate(hits):
        fx_b.add(bt(24 + i * 0.5), h(), 0.5, (-0.4, 0.4)[i % 2])
    for i in range(4):
        perc_b.add(bt(24 + i * 0.5), SN_S, 0.35 + 0.05 * i, 0.0)
    for i in range(8):
        perc_b.add(bt(26 + i * 0.25), SN_S, 0.45 + 0.04 * i, 0.0)
    for i in range(7):
        perc_b.add(bt(27 + i * 0.125), SN_S, 0.6 + 0.04 * i, 0.0)
    L, R = supersaw(fz('G'), 0.14, d=0.09, cut0=6000, cut1=900, cdec=0.05, seed=12)
    chord_b.add2(bt(24), L, R, 0.5)
    L, R = supersaw(fz('E'), 0.14, d=0.09, cut0=6000, cut1=900, cdec=0.05, seed=13)
    chord_b.add2(bt(26), L, R, 0.5)
    for i in range(3):  # glitch stutter of the E stab
        L, R = supersaw(fz('E'), 0.05, d=0.03, cut0=8000, cut1=2000, cdec=0.03, seed=14 + i)
        chord_b.add2(bt(26.5 + i * 0.125), crush(L, 5, 3), crush(R, 5, 3), 0.35)
    fx_b.add(bt(24), riser(bt(3.85), 250, 11000, seed=47, q=1.6, power=2.6, tone=(110, 880)), 0.55)

    # ---- bar 8 (beats 28-31): title. Big hit, Am(add9) bloom, glissando, final pop.
    fx_b.add(bt(28), impact(seed=49, big=1.2), 1.0)
    perc_b.add(bt(28), CRASH, 0.6)
    K(28, 1.0, big=True)
    fx_b.add(bt(28), pop(1300, 300, seed=43), 0.7)
    L, R = supersaw(fz('Am9'), 15.0 - bt(28), a=0.01, d=9, s=1, rel=0.01, cut0=5200, cut1=1500, cdec=0.9, seed=9)
    fade = int(0.9 * SR)
    for k in range(len(L) - fade, len(L)):
        g = (len(L) - k) / fade
        L[k] *= g
        R[k] *= g
    chord_b.add2(bt(28), L, R, 0.5)
    bl = sine_sweep(hz('A1'), hz('A1'), 15.0 - bt(28) - 0.05, dec=0.9)
    bass_b.add(bt(28), bl, 0.55)
    gl = ['A4', 'C5', 'E5', 'A5', 'B5', 'C6', 'E6', 'A6']
    for i, nn in enumerate(gl):
        pl_b.add(bt(28.4) + i * 0.06, pluck(hz(nn), 0.9, 0.7, seed=140 + i), 0.2, -0.7 + 0.2 * i)
    fx_b.add(bt(30), bell(hz('E6'), 1.2, 2.0, 1.0, 0.5), 0.12, 0.2)
    fx_b.add(bt(31), pop(900, 240, seed=47), 0.45)
    pl_b.add(bt(31), pluck(hz('A5'), 0.9, 0.7, seed=160), 0.22, 0.0)

    # ---- bass line: 8ths on the chord roots, filtered saw + sub sine
    roots = {2: 'F', 3: 'G', 4: 'A', 5: 'F', 6: 'C', 7: 'G'}
    rootf = {'A': 'A1', 'F': 'F1', 'G': 'G1', 'C': 'C2', 'E': 'E1'}
    for bar in range(2, 8):
        for e in range(8):
            beat = (bar - 1) * 4 + e * 0.5
            if bar == 3 and beat >= 11.5:
                continue  # the break
            if bar == 7 and beat >= 27.5:
                continue
            ch = roots[bar] if not (bar == 7 and e >= 4) else 'E'
            f = hz(rootf[ch]) * (2 if e % 2 else 1)
            dur = bt(0.45)
            n = int(dur * SR)
            ph1 = ph2 = 0.0
            raw = [0.0] * n
            for k in range(n):
                ph1 = (ph1 + f * 2 / SR) % 1.0
                ph2 += TAU * f / SR
                raw[k] = 0.55 * (2 * ph1 - 1) + 0.9 * math.sin(ph2)
            cut = lambda i, n=n: 180 + 1400 * math.exp(-(i / SR) / 0.06)
            fl = svf(raw, 0, q=1.3, cut_fn=cut)
            envb = [min(1.0, k / 40) * (1.0 if k < n - 300 else (n - k) / 300) for k in range(n)]
            bass_b.add(bt(beat), mul(fl, envb), 0.62 if bar >= 4 else 0.5)

    # ---- sidechain: duck bass + chords under every kick
    duck = [1.0] * kick_b.n
    for tk in kicks:
        i0 = int(tk * SR)
        for k in range(int(0.34 * SR)):
            i = i0 + k
            if i >= len(duck):
                break
            x = k / SR
            g = 1 - 0.78 * (min(1.0, x / 0.004) * math.exp(-x / 0.1))
            duck[i] = min(duck[i], g)

    KG, PG, HG, BG, CG, LG, FG = MIX
    n = kick_b.n
    dryL, dryR, sendL, sendR = [0.0] * n, [0.0] * n, [0.0] * n, [0.0] * n
    for i in range(n):
        d = duck[i]
        bL, bR = bass_b.L[i] * d, bass_b.R[i] * d
        cL, cR = chord_b.L[i] * d, chord_b.R[i] * d
        dryL[i] = kick_b.L[i] * KG + perc_b.L[i] * PG + hat_b.L[i] * HG + bL * BG + cL * CG + pl_b.L[i] * LG + fx_b.L[i] * FG
        dryR[i] = kick_b.R[i] * KG + perc_b.R[i] * PG + hat_b.R[i] * HG + bR * BG + cR * CG + pl_b.R[i] * LG + fx_b.R[i] * FG
        sendL[i] = perc_b.L[i] * 0.3 + cL * 0.3 + pl_b.L[i] * 0.55 + fx_b.L[i] * 0.4
        sendR[i] = perc_b.R[i] * 0.3 + cR * 0.3 + pl_b.R[i] * 0.55 + fx_b.R[i] * 0.4

    peak = max(max(abs(v) for v in dryL), max(abs(v) for v in dryR), 1e-9)
    g = 0.5 / peak

    def wr(path, L, R, gain):
        a = array('h')
        for l, r_ in zip(L, R):
            a.append(int(max(-1.0, min(1.0, l * gain)) * 32767))
            a.append(int(max(-1.0, min(1.0, r_ * gain)) * 32767))
        with wave.open(path, 'wb') as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(a.tobytes())

    wr(os.path.join(out_dir, 'dry.wav'), dryL, dryR, g)
    wr(os.path.join(out_dir, 'send.wav'), sendL, sendR, g)
    # stereo impulse response: pre-delay, dense early part, darkening tail
    nir = int(2.2 * SR)
    irs = []
    for seed in (101, 102):
        nz = noise(nir, seed)
        lp = svf(nz, 0, cut_fn=lambda i: 9000 * math.exp(-(i / SR) / 0.5) + 700)
        irs.append([0.0] * int(0.018 * SR) + [lp[k] * math.exp(-(k / SR) / 0.42) for k in range(nir)])
    pk = 0.9 / max(abs(v) for v in irs[0] + irs[1])
    wr(os.path.join(out_dir, 'ir.wav'), irs[0], irs[1], pk)
    energy = sum(v * v for v in irs[0]) * pk * pk
    return 1.0 / math.sqrt(energy)


def master(out_dir, out_wav, irgain, wet=0.32):
    d = lambda f: os.path.join(out_dir, f)
    fc = (f"[1:a][2:a]afir=dry=0:wet=1:gtype=none:irgain={irgain:.5f}[wet];"
          f"[0:a][wet]amix=inputs=2:weights='1 {wet}':normalize=0,highpass=f=26,"
          "bass=g=-2:f=90,equalizer=f=1400:t=q:w=0.9:g=3,treble=g=-1.5:f=9000,"
          "acompressor=threshold=0.18:ratio=2.2:attack=8:release=140:makeup=1.6,"
          "alimiter=limit=0.84:level_in=1.9:attack=4:release=60:level=false,"
          "afade=t=out:st=14.75:d=0.25[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", d('dry.wav'), "-i", d('send.wav'), "-i", d('ir.wav'),
                    "-filter_complex", fc, "-map", "[out]", "-t", str(DUR), "-ar", str(SR), "-ac", "2", out_wav],
                   check=True)


if __name__ == "__main__":
    od = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(od, exist_ok=True)
    ig = build(od)
    master(od, os.path.join(od, "music.wav"), ig)
    print("ok")
