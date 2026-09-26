"""XForward reel soundtrack: 128 BPM, 20 s, D minor (the loop) -> F major (forward).

Reuses the showreel's pure-Python instruments (reel_synth.py) and places every
hit on the same beat grid as the picture: tense ticking loop, the counter,
a silent break, the drop when the engineer arrives, the build, the ROI climb,
four proof stabs and the logo lock.
"""
import math, os, random, subprocess, sys, wave
from array import array

HERE = os.path.dirname(os.path.abspath(__file__))
for d in (os.path.join(HERE, "..", "showreel"), os.path.join(HERE, "..", "reel")):
    if os.path.exists(os.path.join(d, "reel_synth.py")):
        sys.path.insert(0, os.path.abspath(d))
        break
from reel_synth import (SR, TAU, hz, Bus, svf, noise, sat, mk_kick, mk_clap, mk_hat, mk_snare, mk_crash,
                        mk_tom, supersaw, pluck, sine_sweep, bell, blip, riser, reverse_swell, whoosh,
                        impact, pop, crush)

BPM = 128
B = 60 / BPM
DUR = 20.0


def bt(n):
    return n * B


def square_blip(f, dur=0.12, dec=0.04):
    n = int(dur * SR)
    out = [0.0] * n
    for k in range(n):
        p = (f * k / SR) % 1.0
        out[k] = (0.6 if p < 0.5 else -0.6) * math.exp(-(k / SR) / dec) * min(1.0, k / 30)
    return svf(out, 3500, mode=0)


def tock(f=1250, dec=0.018):
    n = int(0.08 * SR)
    return [math.sin(TAU * f * k / SR) * math.exp(-(k / SR) / dec) * min(1.0, k / 12) for k in range(n)]


def click(seed=3):
    r = random.Random(seed)
    n = int(0.03 * SR)
    hp = svf([r.uniform(-1, 1) for _ in range(n)], 5000, mode=2)
    return [hp[k] * math.exp(-k / (0.004 * SR)) * 2.2 for k in range(n)]


def tape_stop(dur, f0=220, seed=5):
    """A chord-ish tone whose pitch collapses to nothing, like a tape stop."""
    n = int(dur * SR)
    out, ph1, ph2 = [0.0] * n, 0.0, 0.0
    for k in range(n):
        p = k / n
        f = f0 * (1 - p) ** 2 + 20 * p
        ph1 += TAU * f / SR
        ph2 += TAU * f * 1.5 / SR
        out[k] = (math.sin(ph1) + 0.5 * math.sin(ph2)) * (1 - p) * min(1.0, k / 200)
    return sat(out, 1.3)


class Mix:
    def __init__(self):
        self.b = {k: Bus(DUR) for k in ("kick", "perc", "hats", "bass", "chords", "plucks", "fx")}
        self.kicks = []

    def pan_sweep(self, bus, t, sig, p0, p1, gain=1.0):
        i0 = int(round(t * SR))
        L, R, n = self.b[bus].L, self.b[bus].R, len(sig)
        for k in range(n):
            i = i0 + k
            if 0 <= i < len(L):
                a = (p0 + (p1 - p0) * k / n + 1) * math.pi / 4
                L[i] += sig[k] * gain * math.cos(a) * 1.41421356
                R[i] += sig[k] * gain * math.sin(a) * 1.41421356


def build(out_dir):
    M = Mix()
    kick_b, perc_b, hat_b, bass_b, chord_b, pl_b, fx_b = (M.b[k] for k in ("kick", "perc", "hats", "bass", "chords", "plucks", "fx"))
    KICK, KICKB = mk_kick(), mk_kick(f0=180, f1=42, adec=0.34, seed=2)
    CLAP, SN_S = mk_clap(), mk_snare(seed=13, dec=0.07, gain=0.7)
    CH = [mk_hat(0.028, 7 + i) for i in range(4)]
    OH = mk_hat(0.16, 19)
    CRASH = mk_crash()

    def K(beat, g=1.0, big=False):
        kick_b.add(bt(beat), KICKB if big else KICK, g)
        M.kicks.append(bt(beat))

    def groove(b0, b1, clap=True, hats16=True, open_hats=True, kick=True, hat_gain=1.0, kick_gain=1.0):
        for b in range(b0, b1):
            if kick:
                K(b, kick_gain)
            if clap and b % 2 == 1:
                perc_b.add(bt(b), CLAP, 0.75, 0.05)
            if open_hats:
                hat_b.add(bt(b + 0.5), OH, 0.4 * hat_gain, 0.25)
            if hats16:
                for s, g in ((0.25, 0.3), (0.75, 0.36)):
                    hat_b.add(bt(b + s), CH[(b * 2 + int(s * 4)) % 4], g * hat_gain, 0.35)

    V = {
        'Dm': ['D4', 'F4', 'A4'], 'F': ['F3', 'A3', 'C4', 'F4'], 'C': ['E3', 'G3', 'C4', 'E4'], 'Bb': ['D4', 'F4', 'A#3'],
        'Fadd9': ['F3', 'C4', 'F4', 'G4', 'A4'], 'Bbadd9': ['D4', 'F4', 'A#3', 'C5'], 'Dm7': ['D4', 'F4', 'A4', 'C5'],
    }
    fz = lambda ch: [hz(n) for n in V[ch]]

    def pad(ch, b0, beats, gain, cut=(900, 2600), q=0.9, seed=4, a=0.01):
        L, R = supersaw(fz(ch), bt(beats), a=a, d=9, s=1, rel=0.03, cut0=cut[1], cut1=cut[0], cdec=0.6, q=q, seed=seed)
        chord_b.add2(bt(b0), L, R, gain)

    def stab(ch, b0, gain=0.5, seed=30, dur=0.18):
        L, R = supersaw(fz(ch), dur, d=0.12, cut0=7000, cut1=900, cdec=0.07, seed=seed)
        chord_b.add2(bt(b0), L, R, gain)

    # ---------------------------------------------------------------- bar 1: the loop (D minor)
    sub = sine_sweep(hz('D2'), hz('D2'), bt(7.5), gain=1.0, attack=bt(3))
    bass_b.add(0, sub, 0.3)
    loop = ['D4', 'F4', 'A4', 'F4']
    for s in range(30):  # a 4-note loop that never resolves: going in circles
        pl_b.add(bt(s * 0.25), pluck(hz(loop[s % 4]) * (2 if s % 8 >= 4 else 1), 0.35, 0.55, seed=200 + s),
                 0.2 + 0.004 * s, (-0.5, 0.5)[s % 2])
    for i in range(16):
        hat_b.add(bt(i * 0.5), CH[i % 4], 0.14, 0.3)
        if i % 2 == 0:
            fx_b.add(bt(i * 0.5), tock(1250 if i % 4 == 0 else 950), 0.16, -0.3)
    for b in range(4):  # a thud under each word
        kick_b.add(bt(b), mk_kick(f0=130, f1=48, adec=0.22, seed=40 + b), 0.8)
        stab('Dm', b, 0.32, seed=60 + b, dur=0.12)

    # ---------------------------------------------------------------- bar 2: the cost
    fx_b.add(bt(3.4), reverse_swell(bt(0.6), seed=24, f=3500), 0.45)            # rings suck in
    K(4, 1.0, big=True)
    stab('Dm7', 4, 0.5, seed=70)
    for i in range(24):  # counter ticks, accelerating and rising
        tt = bt(4) + 0.9 * (i / 24) ** 1.35
        fx_b.add(tt, blip(900 + 1600 * i / 24, 0.05, 0.012), 0.1, (-0.4, 0.4)[i % 2])
    K(6, 0.8)
    stab('Dm', 6, 0.35, seed=72)
    fx_b.add(bt(5), riser(bt(2.4), 300, 6000, seed=31, q=2.5), 0.35)
    fx_b.add(bt(7.35), tape_stop(bt(0.55)), 0.3)                                # the break

    # ---------------------------------------------------------------- bar 3: the engineer (F major drop)
    fx_b.add(bt(8), impact(big=1.0), 0.95)
    perc_b.add(bt(8), CRASH, 0.5)
    M.pan_sweep("fx", bt(8) - 0.05, whoosh(0.45, seed=33, f0=500, f1=5000), -0.9, 0.3, 0.6)  # the arrow
    K(8, 1.0, big=True)
    for b in range(9, 12):
        K(b)
    groove(8, 12, kick=False)
    pad('F', 8, 4, 0.5, cut=(2400, 5000), seed=6)
    fx_b.add(bt(10) + 0.05, sine_sweep(900, 180, 0.2, dec=0.09), 0.3, 0.2)          # "not a slide deck" strike
    fx_b.add(bt(11), sine_sweep(1200, 1800, 0.06, dec=0.03), 0.12, 0.5)

    # ---------------------------------------------------------------- bar 4: the map (C major, lighter)
    groove(12, 16, clap=True, hats16=False, kick_gain=0.8, hat_gain=0.8)
    pad('C', 12, 4, 0.36, cut=(1600, 3200), seed=7)
    for i, (b, n) in enumerate(zip((12, 12.5, 13, 13.5, 14), ('C5', 'E5', 'G5', 'A5', 'C6'))):   # a node lands
        pl_b.add(bt(b), pluck(hz(n), 0.8, 0.7, seed=300 + i), 0.34, -0.5 + 0.25 * i)
        fx_b.add(bt(b), bell(hz(n) * 2, 0.5, 2.0, 1.2, 0.18), 0.05, -0.5 + 0.25 * i)
    for i, b in enumerate((12.6, 13.1, 13.6, 14.1)):  # connectors drawing
        fx_b.add(bt(b), sine_sweep(500, 1400, 0.22, dec=0.09), 0.06, 0.3 - 0.2 * i)

    # ---------------------------------------------------------------- bar 5: the agents (Dm -> Bb)
    fx_b.add(bt(16), impact(seed=35, sub=(80, 36), sdec=0.45, big=0.5), 0.55)
    for i in range(5):  # nodes extrude
        fx_b.add(bt(16) + 0.045 * i, mk_tom(170 - 12 * i, 90, 0.1), 0.35, -0.6 + 0.3 * i)
    K(16, 1.0, big=True)
    for b in range(17, 20):
        K(b)
    groove(16, 20, kick=False)
    pad('Dm', 16, 2, 0.42, cut=(2000, 4200), seed=8)
    pad('Bb', 18, 2, 0.42, cut=(2000, 4200), seed=9)
    arp = ['D5', 'F5', 'A5', 'D6', 'F5', 'A5', 'D6', 'F6']
    for s in range(14):  # agents spawn: digital arpeggio
        fx_b.add(bt(16.5 + s * 0.25), square_blip(hz(arp[s % 8]), 0.1, 0.035), 0.12, (-0.6, 0.6)[s % 2])

    # ---------------------------------------------------------------- bar 6: the work (Bb -> F)
    fx_b.add(bt(20), impact(seed=37, sub=(75, 35), sdec=0.4, big=0.45), 0.5)
    K(20, 1.0, big=True)
    for b in range(21, 24):
        K(b)
    groove(20, 24, kick=False)
    pad('Bb', 20, 2, 0.45, cut=(2400, 5200), seed=10)
    pad('F', 22, 2, 0.45, cut=(2400, 5200), seed=11)
    for i in range(6):  # streams rushing forward
        M.pan_sweep("fx", bt(20.2 + i * 0.55), whoosh(0.5, seed=50 + i, f0=300, f1=3200 + 300 * i), -0.9, 0.9, 0.22)
    r = random.Random(7)
    penta = ['F5', 'G5', 'A5', 'C6', 'D6', 'F6']
    for i in range(22):
        fx_b.add(bt(20) + r.random() * bt(3.8), blip(hz(penta[r.randrange(6)]), 0.08, 0.02), 0.05, r.uniform(-1, 1))

    # ---------------------------------------------------------------- bar 7: the ROI (C, build)
    for b in (24, 25, 26):
        K(b)
    for b in range(24, 27):
        hat_b.add(bt(b + 0.5), OH, 0.35, 0.25)
    pad('C', 24, 4, 0.5, cut=(1200, 1200), seed=12, a=0.3)
    climb = ['C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5', 'C6']
    for i, n in enumerate(climb):
        pl_b.add(bt(25 + i * 0.375), pluck(hz(n), 0.6, 0.65, seed=400 + i), 0.3, -0.6 + 0.17 * i)
    for i in range(4):
        perc_b.add(bt(24 + i * 0.5), SN_S, 0.3 + 0.05 * i)
    for i in range(4):
        perc_b.add(bt(26 + i * 0.25), SN_S, 0.45 + 0.04 * i)
    for i in range(7):
        perc_b.add(bt(27 + i * 0.125), SN_S, 0.6 + 0.04 * i)
    fx_b.add(bt(24), riser(bt(3.9), 250, 10000, seed=47, q=1.6, power=2.4, tone=(130, 520)), 0.5)
    fx_b.add(bt(27.2), bell(hz('C7'), 0.6, 2.0, 0.8, 0.25), 0.08, 0.4)            # the summit pin

    # ---------------------------------------------------------------- bar 8: the proof (4 stabs)
    fx_b.add(bt(28), impact(seed=39, sub=(80, 36), sdec=0.4, big=0.5), 0.55)
    K(28, 1.0, big=True)
    for b in range(29, 32):
        K(b)
    groove(28, 32, kick=False)
    for i, ch in enumerate(('F', 'C', 'Dm', 'Bb')):
        stab(ch, 28 + i, 0.55, seed=80 + i, dur=0.22)
        fx_b.add(bt(28 + i), bell(hz(('A6', 'G6', 'F6', 'D6')[i]), 0.7, 3.5, 1.6, 0.25), 0.07, (-0.3, 0.3)[i % 2])

    # ---------------------------------------------------------------- bar 9-10: the logo, the call
    M.pan_sweep("fx", bt(31.2), whoosh(bt(0.8), seed=61, f0=400, f1=4200), -0.95, -0.1, 0.5)   # ink chevron
    M.pan_sweep("fx", bt(31.2), whoosh(bt(0.8), seed=62, f0=450, f1=4600), 0.95, 0.1, 0.5)     # blue chevron
    fx_b.add(bt(32), click(), 0.9)                                                               # the lock
    fx_b.add(bt(32), impact(seed=41, big=1.1), 0.95)
    perc_b.add(bt(32), CRASH, 0.55)
    K(32, 1.0, big=True)
    L, R = supersaw(fz('Fadd9'), bt(4), a=0.01, d=9, s=1, rel=0.05, cut0=5200, cut1=1800, cdec=0.9, seed=13)
    chord_b.add2(bt(32), L, R, 0.5)
    for i, n in enumerate(['F4', 'A4', 'C5', 'F5', 'G5', 'A5', 'C6', 'F6']):                   # wordmark
        pl_b.add(bt(32.6) + i * 0.055, pluck(hz(n), 0.9, 0.7, seed=500 + i), 0.2, -0.7 + 0.2 * i)
    fx_b.add(bt(34), bell(hz('C6'), 1.0, 2.0, 1.0, 0.45), 0.1, 0.2)                              # tagline
    tail = DUR - bt(36)
    L, R = supersaw(fz('Bbadd9'), bt(2), a=0.02, d=9, s=1, rel=0.3, cut0=3600, cut1=2200, cdec=1.0, seed=14)
    chord_b.add2(bt(36), L, R, 0.42)
    L, R = supersaw(fz('Fadd9'), DUR - bt(38), a=0.2, d=9, s=1, rel=0.01, cut0=3200, cut1=1400, cdec=1.2, seed=15)
    fade = int(1.2 * SR)
    for k in range(len(L) - fade, len(L)):
        g = (len(L) - k) / fade
        L[k] *= g
        R[k] *= g
    chord_b.add2(bt(38), L, R, 0.42)
    fx_b.add(bt(36), pop(1200, 280, seed=45), 0.55)                                               # CTA pops
    pl_b.add(bt(36), pluck(hz('F5'), 0.9, 0.7, seed=600), 0.25)
    bass_b.add(bt(32), sine_sweep(hz('F1'), hz('F1'), bt(4) - 0.05, dec=1.2), 0.5)
    bass_b.add(bt(36), sine_sweep(hz('A#1'), hz('A#1'), bt(2) - 0.05, dec=0.8), 0.4)
    bass_b.add(bt(38), sine_sweep(hz('F1'), hz('F1'), DUR - bt(38) - 0.05, dec=1.2), 0.45)
    fx_b.add(bt(40), pop(900, 240, seed=47), 0.35)                                               # final pulse
    fx_b.add(bt(40), bell(hz('F6'), 1.2, 2.0, 0.8, 0.5), 0.08)

    # ---------------------------------------------------------------- bass line (8ths) for the groove bars
    roots = {3: 'F', 4: 'C', 5: ('D', 'A#'), 6: ('A#', 'F'), 7: 'C', 8: ('F', 'C', 'D', 'A#')}
    oct1 = {'F': 'F1', 'C': 'C2', 'D': 'D2', 'A#': 'A#1'}
    for bar in range(3, 9):
        for e in range(8):
            beat = (bar - 1) * 4 + e * 0.5
            if bar == 7 and beat >= 27.5:
                continue
            rv = roots[bar]
            if isinstance(rv, tuple):
                rv = rv[min(len(rv) - 1, e * len(rv) // 8)]
            f = hz(oct1[rv]) * (2 if e % 2 else 1)
            n = int(bt(0.45) * SR)
            ph1 = ph2 = 0.0
            raw = [0.0] * n
            for k in range(n):
                ph1 = (ph1 + f * 2 / SR) % 1.0
                ph2 += TAU * f / SR
                raw[k] = 0.55 * (2 * ph1 - 1) + 0.9 * math.sin(ph2)
            fl = svf(raw, 0, q=1.3, cut_fn=lambda i: 180 + 1400 * math.exp(-(i / SR) / 0.06))
            env = [min(1.0, k / 40) * (1.0 if k < n - 300 else (n - k) / 300) for k in range(n)]
            bass_b.add(bt(beat), [a * b for a, b in zip(fl, env)], 0.55 if bar != 4 else 0.45)

    # ---------------------------------------------------------------- sidechain + mixdown
    n = kick_b.n
    duck = [1.0] * n
    for tk in M.kicks:
        i0 = int(tk * SR)
        for k in range(int(0.34 * SR)):
            i = i0 + k
            if i >= n:
                break
            x = k / SR
            duck[i] = min(duck[i], 1 - 0.75 * (min(1.0, x / 0.004) * math.exp(-x / 0.1)))
    KG, PG, HG, BG, CG, LG, FG = 0.58, 0.9, 0.5, 0.46, 2.0, 1.45, 0.9
    dryL, dryR, sendL, sendR = [0.0] * n, [0.0] * n, [0.0] * n, [0.0] * n
    for i in range(n):
        d = duck[i]
        cL, cR = chord_b.L[i] * d, chord_b.R[i] * d
        dryL[i] = kick_b.L[i] * KG + perc_b.L[i] * PG + hat_b.L[i] * HG + bass_b.L[i] * d * BG + cL * CG + pl_b.L[i] * LG + fx_b.L[i] * FG
        dryR[i] = kick_b.R[i] * KG + perc_b.R[i] * PG + hat_b.R[i] * HG + bass_b.R[i] * d * BG + cR * CG + pl_b.R[i] * LG + fx_b.R[i] * FG
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
    nir = int(2.2 * SR)
    irs = []
    for seed in (101, 102):
        nz = noise(nir, seed)
        lp = svf(nz, 0, cut_fn=lambda i: 9000 * math.exp(-(i / SR) / 0.5) + 700)
        irs.append([0.0] * int(0.018 * SR) + [lp[k] * math.exp(-(k / SR) / 0.42) for k in range(nir)])
    pk = 0.9 / max(abs(v) for v in irs[0] + irs[1])
    wr(os.path.join(out_dir, 'ir.wav'), irs[0], irs[1], pk)
    return 1.0 / math.sqrt(sum(v * v for v in irs[0]) * pk * pk)


def master(out_dir, out_wav, irgain, wet=0.32):
    d = lambda f: os.path.join(out_dir, f)
    fc = (f"[1:a][2:a]afir=dry=0:wet=1:gtype=none:irgain={irgain:.5f}[wet];"
          f"[0:a][wet]amix=inputs=2:weights='1 {wet}':normalize=0,highpass=f=26,"
          "bass=g=-2:f=90,equalizer=f=1400:t=q:w=0.9:g=3,treble=g=-1.5:f=9000,"
          "acompressor=threshold=0.18:ratio=2.2:attack=8:release=140:makeup=1.6,"
          f"alimiter=limit=0.84:level_in=2.3:attack=4:release=60:level=false,"
          f"afade=t=out:st={DUR - 0.6}:d=0.6[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", d('dry.wav'), "-i", d('send.wav'), "-i", d('ir.wav'),
                    "-filter_complex", fc, "-map", "[out]", "-t", str(DUR), "-ar", str(SR), "-ac", "2", out_wav],
                   check=True)


if __name__ == "__main__":
    od = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "out")
    os.makedirs(od, exist_ok=True)
    ig = build(od)
    master(od, os.path.join(od, "music.wav"), ig)
    print("ok")
