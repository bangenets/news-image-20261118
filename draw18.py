#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news summary image (1024x1024 PNG).

One-day newspaper front page: masthead with the date, one lead story and
four further stories, each with a simple code-drawn flat icon, plus an
"Also today" strip. All facts verified against wire reporting of the day.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 248, 241)
NAVY = (16, 38, 63)
NAVY2 = (24, 54, 86)
GOLD = (245, 197, 66)
RED = (178, 34, 34)
INK = (24, 24, 24)
GREY = (96, 96, 96)
CARD = (255, 255, 255)
BORDER = (210, 205, 192)

FB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
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


def text_block(draw, xy, text, fnt, max_w, fill, spacing=4, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    x, y = xy
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


# ---------------------------------------------------------------- icons
def icon_globe_flags(d, x, y, s):
    """Globe with three small flags (China, Russia, US) on poles."""
    cx, cy, r = x + s // 2, y + s // 2 + 8, s // 2 - 26
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(58, 130, 190),
              outline=(16, 38, 63), width=3)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=(255, 255, 255), width=2)
    for yy in (-0.55, 0, 0.55):
        d.arc([cx - r, cy + int(r * yy) - int(r * 0.45), cx + r, cy + int(r * yy) + int(r * 0.45)],
              200, 340, fill=(255, 255, 255), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=2)
    # three flag poles
    flags = [((214, 38, 38), None), (None, "ru"), (None, "us")]
    fx = [x + 8, x + s // 2 - 14, x + s - 46]
    for i, (col, kind) in enumerate(flags):
        px = fx[i]
        d.line([px + 12, y + 2, px + 12, y + 40], fill=(60, 60, 60), width=3)
        if kind is None:
            d.rectangle([px + 12, y + 2, px + 38, y + 20], fill=col)
            d.ellipse([px + 18, y + 7, px + 24, y + 13], fill=(245, 197, 66))
        elif kind == "ru":
            d.rectangle([px + 12, y + 2, px + 38, y + 20], fill=(255, 255, 255))
            d.rectangle([px + 12, y + 8, px + 38, y + 14], fill=(0, 57, 166))
            d.rectangle([px + 12, y + 14, px + 38, y + 20], fill=(214, 38, 38))
        else:
            d.rectangle([px + 12, y + 2, px + 38, y + 20], fill=(255, 255, 255))
            for k in range(3):
                d.rectangle([px + 12, y + 2 + k * 6, px + 38, y + 5 + k * 6], fill=(178, 34, 34))
            d.rectangle([px + 12, y + 2, px + 23, y + 11], fill=(0, 40, 104))


def icon_drone(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2 - 8
    arm = s // 3
    for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        d.line([cx, cy, cx + dx * arm, cy + dy * arm], fill=(60, 60, 60), width=5)
        d.ellipse([cx + dx * arm - 14, cy + dy * arm - 6, cx + dx * arm + 14, cy + dy * arm + 6],
                  fill=(120, 120, 120))
    d.ellipse([cx - 26, cy - 18, cx + 26, cy + 18], fill=(178, 34, 34), outline=(90, 10, 10), width=2)
    d.ellipse([cx - 8, cy - 6, cx + 8, cy + 6], fill=(245, 197, 66))
    for i, wy in enumerate((y + s - 34, y + s - 22)):
        d.arc([x + 10, wy - 8, x + s - 10, wy + 8], 0, 180, fill=(58, 130, 190), width=3)


def icon_bridge(d, x, y, s):
    deck_y = y + s // 2
    d.line([x + 8, deck_y, x + s // 2 - 26, deck_y], fill=(70, 70, 70), width=8)
    d.line([x + s // 2 + 26, deck_y, x + s - 8, deck_y], fill=(70, 70, 70), width=8)
    for tx in (x + 34, x + s - 52):
        d.rectangle([tx, deck_y - 52, tx + 14, deck_y], fill=(178, 34, 34))
        d.line([tx + 7, deck_y - 52, tx + 7, deck_y - 72], fill=(178, 34, 34), width=3)
    d.line([x + 41, deck_y - 66, x + s // 2 - 26, deck_y], fill=(150, 150, 150), width=2)
    d.line([x + s - 45, deck_y - 66, x + s // 2 + 26, deck_y], fill=(150, 150, 150), width=2)
    # broken middle: falling span + smoke
    d.line([x + s // 2 - 18, deck_y + 6, x + s // 2 + 4, deck_y + 30], fill=(70, 70, 70), width=6)
    for ox, oy, r in ((-14, -16, 9), (2, -26, 11), (16, -12, 8)):
        d.ellipse([x + s // 2 + ox - r, deck_y + oy - r, x + s // 2 + ox + r, deck_y + oy + r],
                  fill=(190, 190, 190))
    for wy in (deck_y + 44, deck_y + 58):
        d.arc([x + 16, wy - 8, x + s - 16, wy + 8], 0, 180, fill=(58, 130, 190), width=3)


def icon_capitol(d, x, y, s):
    cx = x + s // 2
    base_y = y + s - 26
    d.rectangle([x + 22, base_y - 12, x + s - 22, base_y], fill=(90, 90, 90))
    d.rectangle([x + 34, base_y - 46, x + s - 34, base_y - 12], fill=(120, 120, 120))
    for i in range(5):
        colx = x + 44 + i * ((s - 88) // 4)
        d.rectangle([colx, base_y - 42, colx + 8, base_y - 14], fill=(240, 240, 240))
    d.pieslice([cx - 34, base_y - 96, cx + 34, base_y - 28], 180, 360, fill=(178, 34, 34))
    d.rectangle([cx - 40, base_y - 50, cx + 40, base_y - 44], fill=(90, 90, 90))
    d.line([cx, base_y - 96, cx, base_y - 112], fill=(60, 60, 60), width=3)
    d.ellipse([cx - 4, base_y - 118, cx + 4, base_y - 110], fill=(245, 197, 66))


def icon_virus(d, x, y, s):
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 34
    for k in range(12):
        a = math.radians(k * 30)
        x1, y1 = cx + int(r * 0.8 * math.cos(a)), cy + int(r * 0.8 * math.sin(a))
        x2, y2 = cx + int((r + 16) * math.cos(a)), cy + int((r + 16) * math.sin(a))
        d.line([x1, y1, x2, y2], fill=(178, 34, 34), width=5)
        d.ellipse([x2 - 6, y2 - 6, x2 + 6, y2 + 6], fill=(178, 34, 34))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(214, 38, 38), outline=(120, 10, 10), width=3)
    for ox, oy, rr in ((-14, -10, 9), (12, 6, 11), (-2, 16, 7)):
        d.ellipse([cx + ox - rr, cy + oy - rr, cx + ox + rr, cy + oy + rr], fill=(245, 120, 120))


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24  # margin

    # masthead
    d.rectangle([M, M, W - M, 150], fill=NAVY)
    d.text((W // 2, 40), "THE WORLD IN ONE DAY", font=font(FB, 54),
           fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 106), "WEDNESDAY, 18 NOVEMBER 2026", font=font(FB, 36),
           fill=GOLD, anchor="ma")

    # ---- lead story
    ly0, ly1 = 166, 440
    d.rectangle([M, ly0, W - M, ly1], fill=CARD, outline=BORDER, width=2)
    d.rectangle([M, ly0, M + 10, ly1], fill=RED)
    # icon panel
    d.rectangle([M + 26, ly0 + 20, M + 26 + 250, ly1 - 20], fill=(226, 238, 247))
    icon_globe_flags(d, M + 26, ly0 + 20, 250)
    tx = M + 26 + 250 + 24
    tw = W - M - tx - 20
    d.text((tx, ly0 + 22), "LEAD  •  DIPLOMACY  •  SHENZHEN", font=font(FB, 20), fill=RED)
    y = text_block(d, (tx, ly0 + 52),
                   "XI AND PUTIN MEET IN SHENZHEN BEFORE TRUMP TRILATERAL",
                   font(FB, 33), tw, INK, spacing=2, max_lines=3)
    text_block(d, (tx, y + 8),
               "The Chinese and Russian leaders opened APEC talks a day before the "
               "first three-way summit with the US president. Ukraine and Iran top the agenda.",
               font(FR, 22), tw, (60, 60, 60), spacing=3, max_lines=3)

    # ---- 2x2 grid
    cards = [
        ("GULF CONFLICT", "US STRIKES IRAN SITE; IRAN HITS BACK",
         "US jets hit Qeshm; Iran fired drones at Kuwait and Bahrain.",
         icon_drone, (240, 214, 200)),
        ("UKRAINE WAR", "KERCH BRIDGE HIT AGAIN; SPAN FALLS",
         "Ukrainian strikes partly collapsed the bridge to Crimea.",
         icon_bridge, (226, 238, 247)),
        ("US SENATE", "PELTOLA WINS ALASKA; DEMOCRATS 56–44",
         "Peltola beat Sullivan — the ninth Senate flip of the midterms.",
         icon_capitol, (232, 228, 244)),
        ("HEALTH", "US LOSES MEASLES-FREE STATUS",
         "More than 5,400 cases in 2026, the most since 1991.",
         icon_virus, (247, 226, 226)),
    ]
    gx0, gy0 = M, 456
    cw, chh, gap = 476, 210, 16
    for i, (kicker, head, sub, icon, bg) in enumerate(cards):
        cx = gx0 + (i % 2) * (cw + gap)
        cy = gy0 + (i // 2) * (chh + gap)
        d.rectangle([cx, cy, cx + cw, cy + chh], fill=CARD, outline=BORDER, width=2)
        d.rectangle([cx + 12, cy + 12, cx + 12 + 150, cy + chh - 12], fill=bg)
        icon(d, cx + 12, cy + 12, 150)
        tx = cx + 12 + 150 + 16
        tw = cx + cw - tx - 14
        d.text((tx, cy + 16), kicker, font=font(FB, 18), fill=RED)
        y = text_block(d, (tx, cy + 42), head, font(FB, 25), tw, INK, spacing=2, max_lines=2)
        text_block(d, (tx, y + 6), sub, font(FR, 19), tw, (60, 60, 60), spacing=2, max_lines=2)

    # ---- also today strip
    ay0, ay1 = 908, 972
    d.rectangle([M, ay0, W - M, ay1], fill=(232, 238, 244), outline=BORDER, width=2)
    d.text((M + 18, ay0 + 10), "ALSO TODAY", font=font(FB, 20), fill=NAVY)
    text_block(d, (M + 18, ay0 + 34),
               "Ebola in DR Congo passes 11,000 cases  •  "
               "Voyager 1 reaches one light-day from Earth",
               font(FR, 19), W - 2 * M - 36, INK, spacing=2, max_lines=1)

    # ---- footer
    d.text((W // 2, 984), "Sources: Associated Press  •  Reuters  •  AFP  •  NASA JPL  •  "
           "Pan American Health Organization  •  United Nations",
           font=font(FR, 15), fill=GREY, anchor="ma")

    out = "/tmp/entry18.png"
    img.save(out, "PNG", optimize=True)
    import os
    print("saved", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
