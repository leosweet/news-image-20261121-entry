#!/usr/bin/env python3
"""Render the 21 November 2026 world-news infographic (1024x1024 PNG).

v2: full-day edition. Every story below was checked against live news
reporting for Saturday 21 November 2026 (UTC):

 1. Russia's largest strike package of the war on Ukraine (overnight
    19-20 Nov, reported 20-21 Nov): 400+ drones, 110+ missiles incl.
    27 ballistic; at least 8 killed, Kyiv's Dnipro bridges hit, power
    cut nationwide. Two missiles and a drone landed in Poland; PM Tusk
    called it a deliberate provocation. On 21 Nov a double-tap strike
    on Kryvyi Rih killed 2 and wounded 60 (officials).
 2. AI sell-off: S&P 500 -3.7% into correction, Nasdaq -5.3% (negative
    for 2026), Nikkei -5.1%; Nvidia -14% amid a leadership crisis.
 3. Magnitude 6.8 quake in the Banda Sea, 09:42 UTC, 226 km NE of Dili;
    felt in Dili and Darwin; no damage reported (GFZ/USGS).
 4. Geneva: 128 CCW states agree to elaborate rules on lethal
    autonomous weapons over two years -- but no binding commitment;
    campaigners call the mandate watered down.
 5. Mexico captures FBI Ten Most Wanted boss "El Chapo Isidro"
    (Fausto Isidro Meza Flores) in a Sinaloa raid with US intelligence
    help; $5m FBI reward; 11 killed in the fighting.
 6. BepiColombo enters orbit around Mercury (18:24 UTC) after an
    8-year, 10-billion-km journey; science begins April 2027.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 1024, 1024
INK = (10, 22, 38)            # page background
CARD = (22, 40, 62)           # card background
CARD_HI = (29, 51, 78)        # featured card background
PAPER = (244, 246, 249)       # near-white text
GOLD = (240, 180, 8)          # masthead accent
SOFT = (164, 181, 198)        # secondary text
RULE = (62, 78, 98)           # hairline
RED = (219, 57, 57)
AMBER = (233, 128, 34)
SKY = (88, 158, 216)
VIOLET = (152, 94, 190)
LEAF = (52, 168, 96)

DEJAVU = "/usr/share/fonts/truetype/dejavu"


def load(name, size):
    return ImageFont.truetype(os.path.join(DEJAVU, name), size)


F_DATE = load("DejaVuSans-Bold.ttf", 54)
F_TAG = load("DejaVuSans-Bold.ttf", 24)
F_LEAD = load("DejaVuSans-Bold.ttf", 35)
F_HEAD = load("DejaVuSans-Bold.ttf", 23)
F_BODY = load("DejaVuSans.ttf", 19)
F_KICK = load("DejaVuSans-Bold.ttf", 17)
F_FOOT = load("DejaVuSans.ttf", 15)


def fit_lines(draw, text, font, max_width, limit):
    """Greedy word wrap; returns at most `limit` lines."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines[:limit]


# ---------------------------------------------------------------- icons

def icon_burst(draw, x, y, s, color):
    """Explosion: 16-point star with a bright core."""
    cx, cy = x + s / 2, y + s / 2
    pts = []
    for i in range(32):
        ang = math.pi * 2 * i / 32 - math.pi / 2
        r = s * 0.48 if i % 2 == 0 else s * 0.22
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    draw.polygon(pts, fill=color)
    draw.ellipse([cx - s * 0.13, cy - s * 0.13, cx + s * 0.13, cy + s * 0.13],
                 fill=(255, 216, 70))


def icon_chart(draw, x, y, s, color):
    """Falling market chart with axes."""
    draw.line([(x + 4, y + s - 4), (x + s - 2, y + s - 4)],
              fill=(205, 214, 224), width=3)
    draw.line([(x + 4, y + 2), (x + 4, y + s - 4)],
              fill=(205, 214, 224), width=3)
    pts = [(x + 10, y + s * 0.18), (x + s * 0.34, y + s * 0.34),
           (x + s * 0.55, y + s * 0.26), (x + s * 0.76, y + s * 0.62),
           (x + s - 8, y + s * 0.86)]
    draw.line(pts, fill=color, width=5, joint="curve")
    for px, py in pts:
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=color)


def icon_quake(draw, x, y, s, color):
    """Seismograph zigzag with a peak marker."""
    mid = y + s / 2
    pts = [(x + 2, mid), (x + s * 0.2, mid),
           (x + s * 0.32, mid - s * 0.3), (x + s * 0.44, mid + s * 0.28),
           (x + s * 0.56, mid - s * 0.38), (x + s * 0.68, mid + s * 0.26),
           (x + s * 0.8, mid), (x + s - 2, mid)]
    draw.line(pts, fill=color, width=5, joint="curve")
    draw.ellipse([x + s * 0.56 - 6, mid - s * 0.38 - 6,
                  x + s * 0.56 + 6, mid - s * 0.38 + 6], fill=(255, 216, 70))


def icon_robot(draw, x, y, s, color):
    """Robot head: antenna, square eyes, grille mouth."""
    draw.line([(x + s * 0.5, y + s * 0.2), (x + s * 0.5, y + 2)],
              fill=color, width=4)
    draw.ellipse([x + s * 0.43, y - 2, x + s * 0.57, y + 12], fill=GOLD)
    draw.rounded_rectangle([x + s * 0.12, y + s * 0.2,
                            x + s * 0.88, y + s * 0.92],
                           radius=10, fill=color)
    draw.rectangle([x + s * 0.28, y + s * 0.42, x + s * 0.42, y + s * 0.56],
                   fill=INK)
    draw.rectangle([x + s * 0.58, y + s * 0.42, x + s * 0.72, y + s * 0.56],
                   fill=INK)
    for i in range(3):
        xx = x + s * (0.34 + 0.11 * i)
        draw.line([(xx, y + s * 0.74), (xx, y + s * 0.82)],
                  fill=INK, width=4)


def icon_shield(draw, x, y, s, color):
    """Shield with a five-point star."""
    draw.polygon([(x + s * 0.5, y + 2), (x + s * 0.96, y + s * 0.2),
                  (x + s * 0.96, y + s * 0.56), (x + s * 0.5, y + s - 2),
                  (x + s * 0.04, y + s * 0.56), (x + s * 0.04, y + s * 0.2)],
                 fill=color)
    cx, cy, r = x + s * 0.5, y + s * 0.44, s * 0.24
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + math.pi * i / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=PAPER)


def icon_planet(draw, x, y, s, color):
    """Ringed planet with two craters."""
    draw.ellipse([x + s * 0.16, y + s * 0.12, x + s * 0.84, y + s * 0.88],
                 fill=color)
    draw.ellipse([x + s * 0.3, y + s * 0.26, x + s * 0.48, y + s * 0.44],
                 fill=(color[0] + 42, color[1] + 32, color[2] + 42))
    draw.ellipse([x + s * 0.56, y + s * 0.5, x + s * 0.68, y + s * 0.62],
                 fill=(color[0] + 42, color[1] + 32, color[2] + 42))
    draw.line([(x + 2, y + s * 0.64), (x + s - 2, y + s * 0.36)],
              fill=GOLD, width=6)


# ---------------------------------------------------------------- layout

def card(draw, x, y, w, h, kicker, accent, headline, body, icon):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD)
    draw.rounded_rectangle([x, y, x + w, y + 6], radius=3, fill=accent)
    icon(draw, x + w - 100, y + 30, 84, accent)
    tx = x + 16
    tw = w - 16 - 108
    draw.text((tx, y + 14), kicker, font=F_KICK, fill=accent)
    ly = y + 40
    for line in fit_lines(draw, headline, F_HEAD, tw, 2):
        draw.text((tx, ly), line, font=F_HEAD, fill=PAPER)
        ly += 29
    ly += 2
    for line in fit_lines(draw, body, F_BODY, tw, 3):
        draw.text((tx, ly), line, font=F_BODY, fill=SOFT)
        ly += 23


def build():
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), INK)
    d = ImageDraw.Draw(img)

    # Masthead
    d.text((CANVAS_W // 2, 30), "SATURDAY 21 NOVEMBER 2026",
           font=F_DATE, fill=PAPER, anchor="mt")
    d.text((CANVAS_W // 2, 102), "THE WORLD IN ONE PICTURE",
           font=F_TAG, fill=GOLD, anchor="mt")
    d.line([(28, 146), (CANVAS_W - 28, 146)], fill=GOLD, width=3)

    # Lead story: Russia's strike on Ukraine, spilling into Poland
    lx, ly, lw, lh = 28, 162, CANVAS_W - 56, 210
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=10, fill=CARD_HI)
    d.rectangle([lx, ly + 8, lx + 10, ly + lh - 8], fill=RED)
    icon_burst(d, lx + lw - 108, ly + 56, 104, RED)
    d.text((lx + 26, ly + 14), "WAR  |  UKRAINE AND POLAND",
           font=F_KICK, fill=(255, 122, 122))
    hy = ly + 40
    for line in fit_lines(d, "RUSSIA'S BIGGEST STRIKE YET HITS UKRAINE - AND POLAND",
                          F_LEAD, lw - 240, 2):
        d.text((lx + 26, hy), line, font=F_LEAD, fill=PAPER)
        hy += 41
    by = hy + 4
    lead_body = ("400+ drones and 110 missiles rain down: 8 killed, Kyiv's "
                 "bridges hit, power cut nationwide. Two missiles and a "
                 "drone land in Poland; Tusk calls it a deliberate "
                 "provocation. Kryvyi Rih double-tap kills 2, wounds 60.")
    for line in fit_lines(d, lead_body, F_BODY, lw - 160, 3):
        d.text((lx + 26, by), line, font=F_BODY, fill=SOFT)
        by += 23

    # 2 x 2 grid
    gx, gy = 28, 388
    cw, ch, gap = 472, 186, 12
    card(d, gx, gy, cw, ch, "ECONOMY  |  GLOBAL", RED,
         "MARKETS PLUNGE INTO CORRECTION",
         "S&P 500 -3.7% into correction; Nasdaq -5.3%, Nikkei -5.1%. "
         "Nvidia -14% amid a leadership crisis.", icon_chart)
    card(d, gx + cw + gap, gy, cw, ch, "DISASTER  |  ASIA", AMBER,
         "6.8 QUAKE STRIKES OFF TIMOR-LESTE",
         "Banda Sea tremor at 09:42 UTC, 226 km NE of Dili. Felt in Dili "
         "and Darwin; no damage reported.", icon_quake)
    card(d, gx, gy + ch + gap, cw, ch, "DIPLOMACY  |  GENEVA", SKY,
         "128 NATIONS OPEN PATH ON 'KILLER ROBOTS'",
         "UN talks agree to draft rules on autonomous weapons over two "
         "years - but no binding commitment.", icon_robot)
    card(d, gx + cw + gap, gy + ch + gap, cw, ch, "CRIME  |  MEXICO", GOLD,
         "MEXICO CAPTURES FBI MOST-WANTED BOSS",
         "'El Chapo Isidro' seized in a Sinaloa raid with US help. $5m "
         "FBI reward; 11 killed in the fighting.", icon_shield)

    # Bottom strip: BepiColombo at Mercury
    sx, sy, sw, sh = 28, 786, CANVAS_W - 56, 170
    d.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=10, fill=CARD_HI)
    d.rounded_rectangle([sx, sy, sx + sw, sy + 6], radius=3, fill=VIOLET)
    icon_planet(d, sx + 26, sy + 28, 114, VIOLET)
    tx = sx + 164
    d.text((tx, sy + 16), "SPACE  |  MERCURY", font=F_KICK,
           fill=(201, 146, 228))
    d.text((tx, sy + 42), "BEPICOLOMBO REACHES MERCURY",
           font=F_LEAD, fill=PAPER)
    by = sy + 90
    for line in fit_lines(d, "ESA and JAXA orbiters enter orbit around the "
                             "innermost planet - after 8 years and 10 "
                             "billion km. Science begins in April 2027.",
                          F_BODY, sw - 190, 2):
        d.text((tx, by), line, font=F_BODY, fill=SOFT)
        by += 23

    # Footer
    d.line([(28, 970), (CANVAS_W - 28, 970)], fill=RULE, width=2)
    d.text((CANVAS_W // 2, 980),
           "Sources: Reuters, AP, BBC, The Guardian, ESA, USGS  -  "
           "All stories reported on 21 November 2026",
           font=F_FOOT, fill=SOFT, anchor="mt")
    return img


def main():
    img = build()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    img.save(path)
    print("wrote", path, img.size, os.path.getsize(path))


if __name__ == "__main__":
    main()
