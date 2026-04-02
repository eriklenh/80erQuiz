"""Generate og-image.png for 80erquiz.netlify.app (1200x630px)"""
from PIL import Image, ImageDraw, ImageFont
import math, os

W, H = 1200, 630

# --- Colors ---
DARK   = (7,   7,  13)
DARK2  = (15,  15, 26)
PINK   = (255, 45, 120)
CYAN   = (0,  229, 255)
YELLOW = (255, 230, 0)
MUTED  = (96,  96, 160)
WHITE  = (255, 255, 255)
TEXT   = (232, 232, 240)

img = Image.new("RGB", (W, H), DARK)
draw = ImageDraw.Draw(img)

# --- Grid overlay (subtle cyan lines) ---
for x in range(0, W, 44):
    draw.line([(x, 0), (x, H)], fill=(0, 229, 255, 10), width=1)
for y in range(0, H, 44):
    draw.line([(0, y), (W, y)], fill=(0, 229, 255, 10), width=1)

# --- Scanlines ---
for y in range(0, H, 4):
    draw.line([(0, y), (W, y)], fill=(0, 0, 0, 40), width=2)

# --- Corner accents ---
cs = 36  # corner size
lw = 3
draw.line([(20, 20), (20+cs, 20)], fill=PINK, width=lw)
draw.line([(20, 20), (20, 20+cs)], fill=PINK, width=lw)
draw.line([(W-20, 20), (W-20-cs, 20)], fill=CYAN, width=lw)
draw.line([(W-20, 20), (W-20, 20+cs)], fill=CYAN, width=lw)
draw.line([(20, H-20), (20+cs, H-20)], fill=CYAN, width=lw)
draw.line([(20, H-20), (20, H-20-cs)], fill=CYAN, width=lw)
draw.line([(W-20, H-20), (W-20-cs, H-20)], fill=PINK, width=lw)
draw.line([(W-20, H-20), (W-20, H-20-cs)], fill=PINK, width=lw)

# --- Load fonts (fallback to default if not found) ---
def font(size):
    try:
        return ImageFont.truetype("C:/Windows/Fonts/cour.ttf", size)
    except:
        return ImageFont.load_default()

def font_bold(size):
    try:
        return ImageFont.truetype("C:/Windows/Fonts/courbd.ttf", size)
    except:
        return font(size)

# --- Eyebrow ---
ey_font = font(18)
eyebrow = "NOSTALGIE-QUIZ"
ew = draw.textlength(eyebrow, font=ey_font)
draw.text(((W-ew)/2, 80), eyebrow, fill=CYAN, font=ey_font)

# --- Main title ---
t1_font = font_bold(68)
t1 = "Welcher"
t1w = draw.textlength(t1, font=t1_font)
draw.text(((W-t1w)/2, 135), t1, fill=WHITE, font=t1_font)

t2_font = font_bold(76)
t2 = "80er-Typ"
t2w = draw.textlength(t2, font=t2_font)
# Pink glow simulation: draw slightly offset layers
for dx, dy, alpha in [(-2,-2,80),(-1,-1,120),(2,2,80),(1,1,120)]:
    overlay = Image.new("RGB", (W, H), DARK)
    d2 = ImageDraw.Draw(overlay)
    d2.text(((W-t2w)/2+dx, 225+dy), t2, fill=PINK, font=t2_font)
    img = Image.blend(img, overlay, alpha/255)
    draw = ImageDraw.Draw(img)
draw.text(((W-t2w)/2, 225), t2, fill=PINK, font=t2_font)

t3_font = font_bold(68)
t3 = "bist du?"
t3w = draw.textlength(t3, font=t3_font)
draw.text(((W-t3w)/2, 320), t3, fill=WHITE, font=t3_font)

# --- Subtitle ---
sub_font = font(22)
sub = "7 Fragen.  Eine Wahrheit.  2 Minuten."
subw = draw.textlength(sub, font=sub_font)
draw.text(((W-subw)/2, 420), sub, fill=MUTED, font=sub_font)

# --- Type tags ---
tag_font = font(16)
tags = [
    ("Die Strassengang", PINK),
    ("Mixtape-Architekt", CYAN),
    ("Der Pixel-Pionier", YELLOW),
    ("Zeichentrick-Fan", PINK),
    ("Der Nachtleser", CYAN),
    ("Pausenhof-Netzwerker", YELLOW),
]

# Calculate positions (two rows of 3)
tag_y_start = 465
row_tags = [tags[:3], tags[3:]]
for row_i, row in enumerate(row_tags):
    widths = [draw.textlength(t, font=tag_font) + 28 for t, _ in row]
    total_w = sum(widths) + 16 * (len(row)-1)
    x = (W - total_w) / 2
    y = tag_y_start + row_i * 38
    for (label, color), tw in zip(row, widths):
        # Dark fill + colored border + colored text
        draw.rectangle([x, y, x+tw, y+25], fill=DARK2, outline=color)
        draw.text((x+14, y+4), label, fill=color, font=tag_font)
        x += tw + 16

# --- URL ---
url_font = font(18)
url = "80erquiz.netlify.app"
urlw = draw.textlength(url, font=url_font)
draw.text(((W-urlw)/2, H-50), url, fill=MUTED, font=url_font)

# --- Top accent line ---
draw.rectangle([0, 0, W, 4], fill=PINK)
draw.rectangle([W//2, 0, W, 4], fill=CYAN)

# Save
out = os.path.join(os.path.dirname(__file__), "og-image.png")
img.save(out, "PNG", optimize=True)
print(f"Saved: {out}  ({W}x{H}px)")
