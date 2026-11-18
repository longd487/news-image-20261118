# Render the 18 Nov 2026 world-news summary image (1024x1024 PNG).
# News researched 2026-11-18 from Reuters/AP/Bloomberg/company releases (see README).
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (11, 34, 57)
INK = (18, 28, 40)
GREY = (58, 68, 80)
LIGHT = (244, 246, 248)
WHITE = (255, 255, 255)
FOOT = (122, 135, 148)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)

F_TITLE = font("DejaVuSans-Bold.ttf", 52)
F_DATE = font("DejaVuSans.ttf", 28)
F_KICK = font("DejaVuSans-Bold.ttf", 22)
F_HEAD = font("DejaVuSans-Bold.ttf", 34)
F_BODY = font("DejaVuSans.ttf", 25)
F_NUM = font("DejaVuSans-Bold.ttf", 44)
F_FOOT = font("DejaVuSans.ttf", 20)

STORIES = [
    {
        "color": (192, 57, 43),
        "kicker": "TECH  ·  EARNINGS",
        "head": "Nvidia posts a record $115.8B quarter",
        "body": "Revenue doubled (+103%) and beat forecasts; data centre $107.6B. First results since Huang resigned; shares rose.",
    },
    {
        "color": (142, 68, 173),
        "kicker": "MIDDLE EAST",
        "head": "US hits Iran missile base in the Gulf",
        "body": "US hit an IRGC missile site on Qeshm Island in self-defence, after drone attacks on a US radar base in Bahrain.",
    },
    {
        "color": (36, 113, 163),
        "kicker": "DIPLOMACY",
        "head": "Trump, Xi, Putin summit set for tomorrow",
        "body": "First-ever trilateral summit on the APEC sidelines; arms control and Iran on the agenda. Trump is in Manila for Quad talks.",
    },
    {
        "color": (185, 119, 14),
        "kicker": "UKRAINE WAR",
        "head": "Crimean Bridge road span brought down",
        "body": "Ukraine's strikes collapsed a road section of the bridge to Crimea; Russia hit bridges in Kyiv in reply. Two people were killed.",
    },
    {
        "color": (17, 122, 101),
        "kicker": "ASIA-PACIFIC",
        "head": "North Korea fires ballistic missile",
        "body": "Pyongyang launched a ballistic missile into the Sea of Japan, South Korea's military said, amid heightened tensions on the peninsula.",
    },
]

def wrap(draw, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)

# ---- header ----
d.rectangle([0, 0, W, 148], fill=NAVY)
d.text((48, 26), "THE WORLD TODAY", font=F_TITLE, fill=WHITE)
d.text((48, 96), "Wednesday, 18 November 2026  ·  Five stories that defined the day",
       font=F_DATE, fill=(196, 210, 224))

# ---- story bands ----
y = 148
band_h = (H - 148 - 36) // 5  # 36px footer
for i, s in enumerate(STORIES):
    y0 = y + i * band_h
    y1 = y0 + band_h
    bg = WHITE if i % 2 == 0 else LIGHT
    d.rectangle([0, y0, W, y1], fill=bg)
    # left number column
    d.rectangle([0, y0, 84, y1], fill=s["color"])
    num = str(i + 1)
    nw = d.textlength(num, font=F_NUM)
    d.text((42 - nw / 2, y0 + band_h / 2 - 30), num, font=F_NUM, fill=WHITE)
    # text
    tx = 112
    d.text((tx, y0 + 14), s["kicker"], font=F_KICK, fill=s["color"])
    d.text((tx, y0 + 44), s["head"], font=F_HEAD, fill=INK)
    lines = wrap(d, s["body"], F_BODY, W - tx - 48)
    ly = y0 + 92
    for ln in lines[:2]:
        d.text((tx, ly), ln, font=F_BODY, fill=GREY)
        ly += 31
    # divider
    if i < 4:
        d.line([0, y1, W, y1], fill=(214, 220, 226), width=1)

# ---- footer ----
fy = H - 36
d.rectangle([0, fy, W, H], fill=NAVY)
d.text((48, fy + 7),
       "Sources: Reuters, AP, Bloomberg, company releases  ·  Image: make.fun news-image-20261118",
       font=F_FOOT, fill=(196, 210, 224))

# ---- fit checks (fail loudly instead of silently truncating) ----
for s in STORIES:
    hw = d.textlength(s["head"], font=F_HEAD)
    assert hw <= W - 112 - 48, f"headline too long ({hw:.0f}px): {s['head']}"
    bl = wrap(d, s["body"], F_BODY, W - 112 - 48)
    assert len(bl) <= 2, f"body wraps to {len(bl)} lines: {s['body']}"
print("fit checks passed")

img.save("/home/hatch/workspace/makefun-token-radar/news-image-20261118/entry.png", "PNG", optimize=True)
import os
print("saved", os.path.getsize("/home/hatch/workspace/makefun-token-radar/news-image-20261118/entry.png"), "bytes")
print("size:", img.size)
