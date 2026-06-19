"""
Generates: kdp_cover.png
Amazon KDP book cover - 1600 x 2560px (ideal 1:1.6 ratio)
Run: python3 generate_kdp_cover.py
"""

from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1600, 2560

NAVY        = (10,  30,  80)
NAVY_LIGHT  = (18,  48, 110)
BLUE        = (37,  99, 235)
BLUE_BRIGHT = (96, 165, 250)
BLUE_PALE   = (219, 234, 254)
BLUE_DARK   = (29,  78, 216)
WHITE       = (255, 255, 255)
MUTED       = (148, 163, 184)

AVENIR      = "/System/Library/Fonts/Avenir Next.ttc"
AVENIR_COND = "/System/Library/Fonts/Avenir Next Condensed.ttc"
MONO        = "/System/Library/Fonts/SFNSMono.ttf"

def load(path, size, index=0):
    try:
        return ImageFont.truetype(path, size, index=index)
    except Exception:
        return ImageFont.load_default()

def gradient_bg(img, top, bottom):
    draw = ImageDraw.Draw(img)
    r1,g1,b1 = top
    r2,g2,b2 = bottom
    for row in range(H):
        t = row / H
        draw.line([(0,row),(W,row)],
            fill=(int(r1+(r2-r1)*t), int(g1+(g2-g1)*t), int(b1+(b2-b1)*t)))

def centered(draw, text, font, y, colour):
    bbox = draw.textbbox((0,0), text, font=font)
    x = (W - (bbox[2]-bbox[0])) // 2
    draw.text((x, y), text, font=font, fill=colour)
    return bbox[3] - bbox[1]

img = Image.new("RGB", (W, H))
gradient_bg(img, NAVY, (4, 12, 48))
d = ImageDraw.Draw(img, "RGBA")

# ── glow circles ────────────────────────────────────────────────────────────
for cx, cy, radius, alpha in [
    (W//2, 480,  700, 18),
    (200,  2200, 500, 12),
    (1400, 1800, 400, 10),
]:
    for step in range(60, 0, -8):
        op = int(alpha * (step/60))
        r = step * radius // 60
        d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(*BLUE, op))

# ── left accent bar ──────────────────────────────────────────────────────────
d.rectangle([0, 0, 12, H], fill=BLUE)

# ── top badge ────────────────────────────────────────────────────────────────
badge_font = load(AVENIR, 36, index=7)
badge_text = "BUILD-FIRST  |  2026"
bbox = d.textbbox((0,0), badge_text, font=badge_font)
bw = bbox[2]-bbox[0]+48
bx = (W-bw)//2
d.rounded_rectangle([bx, 80, bx+bw, 80+62], radius=10, fill=BLUE)
d.text((bx+24, 94), badge_text, font=badge_font, fill=WHITE)

# ── "THE" ─────────────────────────────────────────────────────────────────
the_font = load(AVENIR_COND, 88, index=7)
centered(d, "THE", the_font, 190, BLUE_PALE)

# ── "6-MONTH" ────────────────────────────────────────────────────────────────
big_font = load(AVENIR_COND, 200, index=7)
centered(d, "6-MONTH", big_font, 280, WHITE)

# ── "BUILD-FIRST" ─────────────────────────────────────────────────────────
bf_font = load(AVENIR_COND, 158, index=7)
centered(d, "BUILD-FIRST", bf_font, 490, BLUE_BRIGHT)

# ── "DEVELOPER" ──────────────────────────────────────────────────────────────
dev_font = load(AVENIR_COND, 138, index=7)
centered(d, "DEVELOPER", dev_font, 650, WHITE)

# ── "BLUEPRINT" on filled bar ────────────────────────────────────────────────
bp_font = load(AVENIR_COND, 190, index=7)
bp_text = "BLUEPRINT"
bb = d.textbbox((0,0), bp_text, font=bp_font)
bpw = bb[2]-bb[0]
bph = bb[3]-bb[1]
bpx = (W-bpw)//2
bpy = 810
pad = 28
d.rectangle([bpx-pad, bpy-16, bpx+bpw+pad, bpy+bph+16], fill=BLUE)
d.text((bpx, bpy), bp_text, font=bp_font, fill=WHITE)

# ── divider line ─────────────────────────────────────────────────────────────
d.rectangle([(W//2)-200, 1090, (W//2)+200, 1098], fill=BLUE_BRIGHT)

# ── subtitle ─────────────────────────────────────────────────────────────────
sub_font = load(AVENIR, 52, index=3)
centered(d, "How to Escape Tutorial Hell", sub_font, 1118, BLUE_PALE)
centered(d, "and Start Shipping Real-World Apps", sub_font, 1182, BLUE_PALE)

# ── what's inside panel ──────────────────────────────────────────────────────
px, py, pw, ph = 80, 1300, W-160, 720
d.rounded_rectangle([px, py, px+pw, py+ph], radius=18,
                    fill=NAVY_LIGHT, outline=BLUE, width=3)
d.rectangle([px, py, px+pw, py+72], fill=BLUE)
d.rounded_rectangle([px, py, px+pw, py+72], radius=18,
                    fill=BLUE, outline=BLUE, width=0)
d.rectangle([px, py+36, px+pw, py+72], fill=BLUE)

inside_title_font = load(AVENIR, 40, index=7)
d.text((px+24, py+18), "WHAT'S INSIDE", font=inside_title_font, fill=WHITE)

items = [
    (">>", "The 6-Month Build-First Roadmap"),
    (">>", "React, Firebase & Git Cheat Sheets"),
    (">>", "The Master Debugging Flowchart"),
    (">>", "The AI Co-Pilot Strategy"),
    (">>", "The Developer's Toolbelt"),
    (">>", "The Ship-It Philosophy"),
]
item_font  = load(AVENIR, 38, index=3)
arrow_font = load(AVENIR, 38, index=7)
iy = py + 88
for arrow, text in items:
    d.text((px+28, iy), arrow, font=arrow_font, fill=BLUE_BRIGHT)
    d.text((px+90, iy), text,  font=item_font,  fill=WHITE)
    iy += 96

# ── pill tags ────────────────────────────────────────────────────────────────
tag_font = load(AVENIR, 40, index=7)
tags = ["HTML/CSS", "JavaScript", "React", "Firebase", "Git", "AI"]
tx = 80
ty = 2100
for tag in tags:
    tb = d.textbbox((0,0), tag, font=tag_font)
    tw = tb[2]-tb[0]+40
    d.rounded_rectangle([tx, ty, tx+tw, ty+60], radius=30,
                        fill=NAVY_LIGHT, outline=BLUE, width=2)
    d.text((tx+20, ty+10), tag, font=tag_font, fill=BLUE_PALE)
    tx += tw + 18
    if tx > W - 200:
        tx = 80
        ty += 80

# ── bottom rule + author ──────────────────────────────────────────────────────
d.rectangle([0, H-100, W, H-96], fill=BLUE)
d.rectangle([0, H-95, W, H],     fill=(4, 12, 40))
author_font = load(AVENIR, 36, index=3)
centered(d, "DEAN BURT  |  buildwithcode.dev  |  Self-Taught Developer Series",
         author_font, H-72, MUTED)

img.save("kdp_cover.png", "PNG", dpi=(300, 300))
print("  KDP cover saved: kdp_cover.png  (1600 x 2560px)")
