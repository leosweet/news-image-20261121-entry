#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news infographic (1024x1024 PNG).

Stories (all reported on Saturday 21 November 2026):
 1. Russia's massive overnight strike on Ukraine; missiles land in Poland
 2. Global markets plunge into correction on an AI sell-off
 3. Magnitude 6.8 earthquake off Timor-Leste
 4. 128 nations agree to draft rules on autonomous weapons in Geneva
 5. Mexico captures FBI most-wanted cartel boss "El Chapo Isidro"
 6. BepiColombo enters orbit around Mercury after 8 years
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (13, 27, 42)          # deep navy
PANEL = (24, 43, 66)       # panel navy
PANEL2 = (30, 52, 78)      # lighter panel
WHITE = (245, 247, 250)
GOLD = (242, 183, 5)
MUTED = (168, 184, 200)
RED = (214, 48, 49)
GREEN = (46, 160, 90)
ORANGE = (232, 126, 36)
STEEL = (84, 153, 199)
PURPLE = (155, 89, 182)
TEAL = (26, 188, 156)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_DATE = font("DejaVuSans-Bold.ttf", 58)
F_SUB = font("DejaVuSans-Bold.ttf", 26)
F_LEAD = font("DejaVuSans-Bold.ttf", 36)
F_HEAD = font("DejaVuSans-Bold.ttf", 26)
F_BODY = font("DejaVuSans.ttf", 20)
F_KICK = font("DejaVuSans-Bold.ttf", 18)
F_FOOT = font("DejaVuSans.ttf", 16)


def wrap(draw, text, fnt, max_w):
    """Wrap text to fit max_w; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_burst(d, cx, cy, r, color):
    """Starburst / explosion pictogram."""
    import math
    pts = []
    for i in range(24):
        ang = math.pi * 2 * i / 24
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color)
    d.ellipse([cx - r * 0.28, cy - r * 0.28, cx + r * 0.28, cy + r * 0.28],
              fill=(255, 214, 64))


def draw_chart(d, x, y, w, h, color):
    """Falling line-chart pictogram with axes."""
    d.line([(x, y + h), (x + w, y + h)], fill=(200, 210, 220), width=3)
    d.line([(x, y), (x, y + h)], fill=(200, 210, 220), width=3)
    pts = [(x + 6, y + 14), (x + w * 0.3, y + 26), (x + w * 0.5, y + 20),
           (x + w * 0.7, y + 52), (x + w - 6, y + h - 8)]
    d.line(pts, fill=color, width=5, joint="curve")
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=color)


def draw_quake(d, x, y, w, h, color):
    """Seismic zigzag pictogram."""
    mid = y + h // 2
    pts = [(x, mid), (x + w * 0.18, mid), (x + w * 0.3, mid - h * 0.32),
           (x + w * 0.42, mid + h * 0.3), (x + w * 0.55, mid - h * 0.42),
           (x + w * 0.68, mid + h * 0.28), (x + w * 0.8, mid),
           (x + w, mid)]
    d.line(pts, fill=color, width=5, joint="curve")
    d.ellipse([x + w * 0.55 - 6, mid - h * 0.42 - 6,
               x + w * 0.55 + 6, mid - h * 0.42 + 6], fill=color)


def draw_robot(d, x, y, w, h, color):
    """Simple robot-head pictogram."""
    d.rounded_rectangle([x + w * 0.14, y + h * 0.22, x + w * 0.86, y + h * 0.9],
                        radius=12, fill=color)
    d.line([(x + w * 0.5, y + h * 0.22), (x + w * 0.5, y + 2)],
           fill=color, width=4)
    d.ellipse([x + w * 0.44, y - 2, x + w * 0.56, y + 10], fill=GOLD)
    d.ellipse([x + w * 0.3, y + h * 0.42, x + w * 0.44, y + h * 0.56],
              fill=BG)
    d.ellipse([x + w * 0.56, y + h * 0.42, x + w * 0.7, y + h * 0.56],
              fill=BG)
    d.line([(x + w * 0.32, y + h * 0.74), (x + w * 0.68, y + h * 0.74)],
           fill=BG, width=4)


def draw_badge(d, x, y, w, h, color):
    """Shield/badge pictogram with a star."""
    import math
    d.polygon([(x + w * 0.5, y), (x + w * 0.95, y + h * 0.18),
               (x + w * 0.95, y + h * 0.55), (x + w * 0.5, y + h),
               (x + w * 0.05, y + h * 0.55), (x + w * 0.05, y + h * 0.18)],
              fill=color)
    cx, cy, r = x + w * 0.5, y + h * 0.44, w * 0.26
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + math.pi * i / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=WHITE)


def draw_planet(d, x, y, w, h, color):
    """Planet with ring pictogram."""
    d.ellipse([x + w * 0.18, y + h * 0.14, x + w * 0.82, y + h * 0.86],
              fill=color)
    d.ellipse([x + w * 0.3, y + h * 0.28, x + w * 0.52, y + h * 0.5],
              fill=(color[0] + 40, color[1] + 30, color[2] + 40))
    d.line([(x, y + h * 0.62), (x + w, y + h * 0.38)], fill=GOLD, width=6)


def story_cell(d, x, y, w, h, kicker, kick_color, headline, body, pict):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=PANEL)
    d.rounded_rectangle([x, y, x + w, y + 6], radius=3, fill=kick_color)
    px, py, pw, ph = x + w - 108, y + 34, 92, 92
    pict(d, px, py, pw, ph, kick_color)
    tx = x + 16
    tw = w - 16 - 116
    d.text((tx, y + 16), kicker, font=F_KICK, fill=kick_color)
    lines = wrap(d, headline, F_HEAD, tw)[:2]
    ly = y + 44
    for ln in lines:
        d.text((tx, ly), ln, font=F_HEAD, fill=WHITE)
        ly += 30
    blines = wrap(d, body, F_BODY, tw)[:3]
    for ln in blines:
        d.text((tx, ly + 4), ln, font=F_BODY, fill=MUTED)
        ly += 24


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.text((W // 2, 34), "SATURDAY 21 NOVEMBER 2026", font=F_DATE,
           fill=WHITE, anchor="mt")
    d.text((W // 2, 104), "THE WORLD IN ONE PICTURE", font=F_SUB,
           fill=GOLD, anchor="mt")
    d.line([(28, 148), (W - 28, 148)], fill=GOLD, width=3)

    # ---- Lead story: Russia strike ----
    lx, ly, lw, lh = 28, 166, W - 56, 196
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=10, fill=PANEL2)
    d.rectangle([lx, ly + 8, lx + 10, ly + lh - 8], fill=RED)
    draw_burst(d, lx + lw - 84, ly + 62, 52, RED)
    d.text((lx + 26, ly + 14), "WAR  |  UKRAINE AND POLAND", font=F_KICK,
           fill=(255, 120, 120))
    head = wrap(d, "RUSSIA'S BIGGEST STRIKE HITS UKRAINE - AND POLAND",
                F_LEAD, lw - 220)
    hy = ly + 42
    for ln in head[:2]:
        d.text((lx + 26, hy), ln, font=F_LEAD, fill=WHITE)
        hy += 42
    body = wrap(d, "400+ drones and 110 missiles rain on Kyiv: 8 killed, "
                   "power cut in 10 regions. Two missiles and a drone land "
                   "in Poland; NATO calls it a grave violation.",
                F_BODY, lw - 52)
    by = hy + 6
    for ln in body[:2]:
        d.text((lx + 26, by), ln, font=F_BODY, fill=MUTED)
        by += 27

    # ---- 2x2 grid ----
    gx, gy = 28, 380
    cw, chh, gap = 472, 184, 12
    story_cell(d, gx, gy, cw, chh, "ECONOMY  |  GLOBAL", RED,
               "MARKETS PLUNGE INTO CORRECTION",
               "AI sell-off: S&P 500 -3.7%, Nikkei -5.1%. Nvidia -14% as "
               "the SEC probes its accounting.", draw_chart)
    story_cell(d, gx + cw + gap, gy, cw, chh, "DISASTER  |  ASIA", ORANGE,
               "6.8 QUAKE STRIKES OFF TIMOR-LESTE",
               "Tremor strikes 103 km off Lospalos at 09:42 UTC. No "
               "tsunami threat.", draw_quake)
    story_cell(d, gx, gy + chh + gap, cw, chh, "DIPLOMACY  |  GENEVA",
               STEEL, "128 NATIONS AGREE 'KILLER ROBOT' RULES",
               "UN talks to draft rules on autonomous weapons, aiming for "
               "an accord by 2028.", draw_robot)
    story_cell(d, gx + cw + gap, gy + chh + gap, cw, chh,
               "CRIME  |  MEXICO", GOLD,
               "MEXICO CAPTURES FBI MOST-WANTED BOSS",
               "'El Chapo Isidro' seized in a Sinaloa raid, announced "
               "Saturday. $5m FBI bounty.", draw_badge)

    # ---- Bottom strip: BepiColombo ----
    sx, sy, sw, sh = 28, 780, W - 56, 176
    d.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=10, fill=PANEL2)
    d.rounded_rectangle([sx, sy, sx + sw, sy + 6], radius=3, fill=PURPLE)
    draw_planet(d, sx + 24, sy + 30, 116, 116, PURPLE)
    tx = sx + 164
    d.text((tx, sy + 16), "SPACE  |  MERCURY", font=F_KICK, fill=(198, 142, 226))
    d.text((tx, sy + 44), "BEPICOLOMBO REACHES MERCURY", font=F_LEAD,
           fill=WHITE)
    blines = wrap(d, "ESA and JAXA orbiters enter orbit around the innermost "
                      "planet today - after 8 years and 10 billion km.",
                  F_BODY, sw - 190)
    by = sy + 92
    for ln in blines[:2]:
        d.text((tx, by), ln, font=F_BODY, fill=MUTED)
        by += 27

    # ---- Footer ----
    d.line([(28, 972), (W - 28, 972)], fill=(60, 76, 96), width=2)
    d.text((W // 2, 982), "Sources: Reuters, AP, BBC, The Guardian, ESA, "
           "USGS  -  All stories reported on 21 November 2026",
           font=F_FOOT, fill=MUTED, anchor="mt")

    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out, exist_ok=True)
    img.save(os.path.join(out, "entry.png"))
    print("wrote", os.path.join(out, "entry.png"),
          img.size, os.path.getsize(os.path.join(out, "entry.png")))


if __name__ == "__main__":
    main()
