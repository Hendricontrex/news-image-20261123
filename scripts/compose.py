#!/usr/bin/env python3
"""Render the 23 November 2026 front page as a 1024x1024 PNG.

Own layout: a dark dotted-map backdrop, a masthead band, five numbered
story rows, and a footer line. All text is drawn with PIL; nothing is
fetched from the network.
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent.parent
SIZE = 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PLAIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

GOLD = (232, 176, 74)
WHITE = (245, 245, 240)
FAINT = (205, 208, 210)
CARD = (13, 32, 48, 178)
ACCENTS = [(232, 176, 74), (224, 84, 72), (96, 196, 168), (232, 122, 54), (140, 178, 232)]

STORIES = [
    ("01", "COP31 COLLAPSES",
     "Climate talks in Antalya end with no deal as the EU rejects a text "
     "with no fossil-fuel phase-out — ANTALYA"),
    ("02", "DRONES HIT RUSSIAN WARSHIP",
     "Suspected Ukrainian sea drones hit the corvette Merkury at Benghazi; "
     "it capsizes, 10 hurt — BENGHAZI"),
    ("03", "TANKERS STRUCK IN HORMUZ",
     "Three tankers hit in the strait; two more catch fire after striking "
     "mines, Iran's navy says — STRAIT OF HORMUZ"),
    ("04", "US CURBS CANADA DEFENCE TIES",
     "Hegseth's memo curbs military contact with Canada; it spares NORAD "
     "and NATO, senators say — WASHINGTON"),
    ("05", "LIVERPOOL ROUT UNITED 4–0",
     "Pochettino's Man United debut ends in a 4–0 rout at Anfield; Yoro "
     "sent off after eight minutes — LIVERPOOL"),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def shrink_to_fit(draw, text, path, start, limit):
    """Largest font size at which text fits inside limit pixels."""
    size = start
    while size > 12:
        f = font(path, size)
        if draw.textlength(text, font=f) <= limit:
            return f
        size -= 2
    return font(path, size)


def wrap(draw, text, f, limit):
    """Greedy word wrap into lines no wider than limit."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=f) <= limit:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def squared_backdrop():
    """Centre-crop the dotted map to a square and darken it."""
    img = Image.open(HERE / "news-bg.png").convert("RGB")
    w, h = img.size
    side = min(w, h)
    img = img.crop(((w - side) // 2, (h - side) // 2,
                    (w + side) // 2, (h + side) // 2))
    img = img.resize((SIZE, SIZE), Image.LANCZOS)
    veil = Image.new("RGB", (SIZE, SIZE), (6, 18, 30))
    return Image.blend(img, veil, 0.62)


def draw_page():
    page = squared_backdrop()
    draw = ImageDraw.Draw(page, "RGBA")

    # --- masthead ---
    title_f = shrink_to_fit(draw, "WORLD NEWS", BOLD, 118, 940)
    draw.text((SIZE // 2, 30), "WORLD NEWS", font=title_f, fill=WHITE,
              anchor="ma")
    draw.rectangle([48, 168, SIZE - 48, 172], fill=GOLD)
    date_f = font(BOLD, 44)
    draw.text((SIZE // 2, 186), "MONDAY • 23 NOVEMBER 2026", font=date_f,
              fill=GOLD, anchor="ma")
    draw.rectangle([48, 246, SIZE - 48, 249], fill=(150, 158, 165))

    # --- story rows ---
    top, row_h, gap = 260, 132, 8
    body_f = font(PLAIN, 27)
    for i, (num, head, body) in enumerate(STORIES):
        y = top + i * (row_h + gap)
        draw.rectangle([40, y, SIZE - 40, y + row_h], fill=CARD)
        draw.rectangle([40, y, 52, y + row_h], fill=ACCENTS[i])
        num_f = font(BOLD, 58)
        draw.text((88, y + 34), num, font=num_f, fill=ACCENTS[i], anchor="la")
        head_f = shrink_to_fit(draw, head, BOLD, 46, 800)
        draw.text((190, y + 12), head, font=head_f, fill=WHITE, anchor="la")
        lines = wrap(draw, body, body_f, 800)[:2]
        ly = y + 62
        for line in lines:
            draw.text((190, ly), line, font=body_f, fill=FAINT, anchor="la")
            ly += 32

    # --- footer ---
    foot_f = font(PLAIN, 30)
    draw.text((SIZE // 2, 968), "THE DAY IN FIVE STORIES • 23 NOVEMBER 2026",
              font=foot_f, fill=FAINT, anchor="ma")
    return page


def main():
    # Every story body must wrap to at most two lines, or its dateline
    # would be cut off at the card's edge.
    probe = Image.new("RGB", (SIZE, SIZE))
    check = ImageDraw.Draw(probe)
    body_f = font(PLAIN, 27)
    for num, head, body in STORIES:
        lines = wrap(check, body, body_f, 800)
        assert len(lines) <= 2, f"story {num} wraps to {len(lines)} lines: {lines}"
        head_f = shrink_to_fit(check, head, BOLD, 46, 800)
        assert head_f.size >= 34, f"headline {num} shrinks below 34pt"
    out = HERE / "entry.png"
    draw_page().save(out, "PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
