"""
Generates Gumroad Cover (1280x720) and Thumbnail (600x600)
Run: python3 generate_images.py
"""

from PIL import Image, ImageDraw, ImageFont
import math

# ── Colours -----------------------------------------------------------------
NAVY        = (10,  30,  80)
NAVY_LIGHT  = (18,  48, 110)
BLUE        = (37,  99, 235)
BLUE_BRIGHT = (96, 165, 250)
BLUE_PALE   = (219, 234, 254)
WHITE       = (255, 255, 255)
OFF_WHITE   = (226, 232, 240)
MUTED       = (148, 163, 184)
ACCENT_GLOW = (37,  99, 235, 60)   # semi-transparent for glow layers

# ── Fonts -------------------------------------------------------------------
AVENIR      = "/System/Library/Fonts/Avenir Next.ttc"
AVENIR_COND = "/System/Library/Fonts/Avenir Next Condensed.ttc"
MONO        = "/System/Library/Fonts/SFNSMono.ttf"

def load(path, size, index=0):
    try:
        return ImageFont.truetype(path, size, index=index)
    except Exception:
        return ImageFont.load_default()

# ── Helpers -----------------------------------------------------------------
def draw_rounded_rect(draw, xy, radius, fill, outline=None, outline_width=2):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill,
                            outline=outline, width=outline_width)

def centered_text(draw, text, font, y, width, colour):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x  = (width - tw) // 2
    draw.text((x, y), text, font=font, fill=colour)
    return bbox[3] - bbox[1]   # return text height

def draw_code_snippet(draw, x, y, font, alpha=60):
    """Decorative background code lines."""
    lines = [
        "const launch = async () => {",
        "  await learnByBuilding();",
        "  return shipIt();",
        "};",
    ]
    col = (*BLUE_BRIGHT, alpha)
    for i, line in enumerate(lines):
        draw.text((x, y + i * 22), line, font=font, fill=col)

def gradient_bg(img, top_colour, bottom_colour):
    """Vertical gradient painted pixel-row by pixel-row."""
    draw = ImageDraw.Draw(img)
    w, h = img.size
    r1, g1, b1 = top_colour
    r2, g2, b2 = bottom_colour
    for row in range(h):
        t  = row / h
        r  = int(r1 + (r2 - r1) * t)
        g  = int(g1 + (g2 - g1) * t)
        b  = int(b1 + (b2 - b1) * t)
        draw.line([(0, row), (w, row)], fill=(r, g, b))


# ════════════════════════════════════════════════════════════════════════════
# COVER  1280 x 720
# ════════════════════════════════════════════════════════════════════════════
def make_cover(path="gumroad_cover.png"):
    W, H = 1280, 720
    img  = Image.new("RGB", (W, H))
    gradient_bg(img, NAVY, (6, 18, 55))
    d    = ImageDraw.Draw(img, "RGBA")

    # ── decorative glow circles ------------------------------------------
    for cx, cy, r, a in [(960, 120, 320, 25), (320, 600, 260, 18)]:
        for step in range(80, 0, -10):
            opacity = int(a * (step / 80))
            d.ellipse([cx - step*r//80, cy - step*r//80,
                       cx + step*r//80, cy + step*r//80],
                      fill=(*BLUE, opacity))

    # ── left accent stripe ------------------------------------------------
    d.rectangle([0, 0, 6, H], fill=BLUE)

    # ── top badge --------------------------------------------------------
    draw_rounded_rect(d, [60, 44, 330, 82], radius=6,
                      fill=BLUE, outline=None)
    badge_font = load(AVENIR, 22, index=7)
    d.text((76, 52), "BUILD-FIRST  |  2026", font=badge_font, fill=WHITE)

    # ── main title -------------------------------------------------------
    title_font  = load(AVENIR_COND, 92, index=7)   # heavy condensed
    title2_font = load(AVENIR_COND, 86, index=7)
    title3_font = load(AVENIR_COND, 74, index=7)

    d.text((60, 110), "THE 6-MONTH",    font=title_font,  fill=WHITE)
    d.text((60, 202), "BUILD-FIRST",    font=title2_font, fill=BLUE_BRIGHT)
    d.text((60, 288), "DEVELOPER",      font=title3_font, fill=WHITE)

    # ── "BLUEPRINT" on a filled bar -------------------------------------
    blueprint_font = load(AVENIR_COND, 100, index=7)
    bbox = d.textbbox((60, 370), "BLUEPRINT", font=blueprint_font)
    pad  = 14
    d.rectangle([60 - pad, 370 - 8,
                 bbox[2] + pad, bbox[3] + 8], fill=BLUE)
    d.text((60, 370), "BLUEPRINT", font=blueprint_font, fill=WHITE)

    # ── sub-line ---------------------------------------------------------
    sub_font = load(AVENIR, 28, index=3)
    d.text((62, 492),
           "Escape tutorial hell. Ship real apps.",
           font=sub_font, fill=BLUE_PALE)

    # ── pill tags --------------------------------------------------------
    tag_font = load(AVENIR, 20, index=7)
    tags = ["HTML/CSS", "JavaScript", "React", "Firebase", "Deploy"]
    tx = 62
    ty = 568
    for tag in tags:
        tb   = d.textbbox((0, 0), tag, font=tag_font)
        tw   = tb[2] - tb[0] + 24
        draw_rounded_rect(d, [tx, ty, tx + tw, ty + 34],
                          radius=17, fill=NAVY_LIGHT, outline=BLUE, outline_width=1)
        d.text((tx + 12, ty + 7), tag, font=tag_font, fill=BLUE_PALE)
        tx += tw + 12

    # ── decorative code lines (bottom-right) ----------------------------
    code_font = load(MONO, 16)
    draw_code_snippet(d, 820, 560, code_font, alpha=55)

    # ── right-side decorative PDF icon ----------------------------------
    px, py = 930, 120
    # outer card
    draw_rounded_rect(d, [px, py, px + 260, py + 340],
                      radius=12, fill=NAVY_LIGHT, outline=BLUE, outline_width=2)
    # folded corner
    d.polygon([(px + 200, py), (px + 260, py + 60),
               (px + 200, py + 60)], fill=NAVY)
    d.line([(px + 200, py), (px + 260, py + 60)], fill=BLUE, width=2)
    # mock content lines on the card
    line_font = load(AVENIR, 14, index=3)
    for i, (lw, lc) in enumerate([
        (160, BLUE_BRIGHT), (120, MUTED), (140, MUTED),
        (100, MUTED),       (130, MUTED), (110, MUTED),
    ]):
        ly = py + 90 + i * 28
        draw_rounded_rect(d, [px + 20, ly, px + 20 + lw, ly + 10],
                          radius=5, fill=lc if i == 0 else (*MUTED, 80))
    # PDF label on card
    pdf_font = load(AVENIR, 30, index=7)
    d.text((px + 72, py + 268), "PDF", font=pdf_font, fill=BLUE_BRIGHT)

    # ── bottom rule + author line ----------------------------------------
    d.rectangle([0, H - 54, W, H - 53], fill=BLUE)
    d.rectangle([0, H - 52, W, H],      fill=(6, 15, 45))
    author_font = load(AVENIR, 20, index=3)
    d.text((60, H - 38),
           "buildwithcode.dev  |  Self-Taught Developer Series",
           font=author_font, fill=MUTED)

    img.save(path, "PNG", dpi=(144, 144))
    print(f"  Cover saved:     {path}")


# ════════════════════════════════════════════════════════════════════════════
# THUMBNAIL  600 x 600
# ════════════════════════════════════════════════════════════════════════════
def make_thumbnail(path="gumroad_thumbnail.png"):
    W, H = 600, 600
    img  = Image.new("RGB", (W, H))
    gradient_bg(img, NAVY, (6, 18, 55))
    d    = ImageDraw.Draw(img, "RGBA")

    # ── glow ---------------------------------------------------------------
    for step in range(80, 0, -8):
        opacity = int(30 * (step / 80))
        d.ellipse([W//2 - step*3, H//2 - step*3,
                   W//2 + step*3, H//2 + step*3],
                  fill=(*BLUE, opacity))

    # ── left + top accent bars -------------------------------------------
    d.rectangle([0, 0, 5, H], fill=BLUE)
    d.rectangle([0, 0, W, 5], fill=BLUE)

    # ── top badge --------------------------------------------------------
    draw_rounded_rect(d, [24, 22, 242, 54],
                      radius=6, fill=BLUE)
    b_font = load(AVENIR, 17, index=7)
    d.text((36, 30), "BUILD-FIRST  2026", font=b_font, fill=WHITE)

    # ── "6-MONTH" label --------------------------------------------------
    mo_font = load(AVENIR_COND, 52, index=7)
    centered_text(d, "THE 6-MONTH", mo_font, 82, W, MUTED)

    # ── big title line ---------------------------------------------------
    big_font = load(AVENIR_COND, 72, index=7)
    centered_text(d, "BUILD-FIRST", big_font, 138, W, BLUE_BRIGHT)

    # ── "DEVELOPER" -------------------------------------------------------
    dev_font = load(AVENIR_COND, 58, index=7)
    centered_text(d, "DEVELOPER", dev_font, 218, W, WHITE)

    # ── "BLUEPRINT" highlight bar ----------------------------------------
    bp_font  = load(AVENIR_COND, 78, index=7)
    bp_text  = "BLUEPRINT"
    bp_bbox  = d.textbbox((0, 0), bp_text, font=bp_font)
    bp_w     = bp_bbox[2] - bp_bbox[0]
    bx       = (W - bp_w) // 2
    by       = 298
    pad      = 12
    d.rectangle([bx - pad, by - 6, bx + bp_w + pad, by + 72], fill=BLUE)
    d.text((bx, by), bp_text, font=bp_font, fill=WHITE)

    # ── sub-line --------------------------------------------------------
    sub_font = load(AVENIR, 20, index=3)
    centered_text(d, "Escape tutorial hell.", sub_font, 396, W, BLUE_PALE)
    centered_text(d, "Ship real apps.", sub_font, 422, W, BLUE_PALE)

    # ── divider ---------------------------------------------------------
    d.rectangle([W//2 - 80, 458, W//2 + 80, 460], fill=BLUE)

    # ── tag pills --------------------------------------------------------
    tag_font = load(AVENIR, 15, index=7)
    tags = ["JS", "React", "Firebase"]
    total_w  = sum(d.textbbox((0,0), t, font=tag_font)[2] + 28 for t in tags) + 12
    tx = (W - total_w) // 2
    ty = 472
    for tag in tags:
        tb = d.textbbox((0, 0), tag, font=tag_font)
        tw = tb[2] - tb[0] + 28
        draw_rounded_rect(d, [tx, ty, tx + tw, ty + 30],
                          radius=15, fill=NAVY_LIGHT, outline=BLUE, outline_width=1)
        d.text((tx + 14, ty + 6), tag, font=tag_font, fill=BLUE_PALE)
        tx += tw + 12

    # ── bottom bar -------------------------------------------------------
    d.rectangle([0, H - 44, W, H - 43], fill=BLUE)
    d.rectangle([0, H - 42, W, H],      fill=(6, 15, 45))
    ft_font = load(AVENIR, 16, index=3)
    centered_text(d, "buildwithcode.dev", ft_font, H - 30, W, MUTED)

    img.save(path, "PNG", dpi=(144, 144))
    print(f"  Thumbnail saved: {path}")


# ── Run ---------------------------------------------------------------------
if __name__ == "__main__":
    base = "/Users/deantyroneburtburt/Downloads/coding blog/"
    make_cover(base + "gumroad_cover.png")
    make_thumbnail(base + "gumroad_thumbnail.png")
    print("\n  Both images ready. Upload them to Gumroad.\n")
