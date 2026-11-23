#!/usr/bin/env python3
"""Build the v3 front page for make.fun news-image-20261122.

A newspaper front page summing up Sunday 22 November 2026 in one image:
36 stories, a stat strip, three flat-illustration lead panels, a diplomacy
band, a numbered story grid, a world map with pins, and an ALSO ON list.

All stories were verified against news search results (Reuters, AP, CNN,
Al Jazeera, Le Monde, Al Jazeera, Dawn, Formula1.com, Cricbuzz, ESPN, SCMP,
Hong Kong government releases). Every headline is written in my own words.
Only PIL and the Python standard library are used.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

PAPER = (246, 241, 231)
INK = (26, 26, 26)
NAVY = (29, 43, 58)
RED = (179, 39, 30)
GREY = (107, 107, 102)
LIGHT_GREY = (140, 140, 134)
BAND = (233, 238, 243)
MAP_NAVY = (22, 40, 58)
LAND = (125, 155, 138)
MAP_GRID = (42, 66, 88)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = font("DejaVuSerif-Bold.ttf", 46)
SANS_B = font("DejaVuSans-Bold.ttf", 16)
SANS = font("DejaVuSans.ttf", 14)
SANS_S = font("DejaVuSans.ttf", 13)
SANS_XS = font("DejaVuSans.ttf", 11)
SANS_XXS = font("DejaVuSans.ttf", 10)
SANS_BIG = font("DejaVuSans-Bold.ttf", 30)
SANS_MD = font("DejaVuSans-Bold.ttf", 20)
SANS_SM_B = font("DejaVuSans-Bold.ttf", 14)
SANS_NUM = font("DejaVuSans-Bold.ttf", 15)
SANS_TINY_B = font("DejaVuSans-Bold.ttf", 10)
SANS_TINY = font("DejaVuSans.ttf", 10)

MX = 28                      # page margin
CW = 968                     # content width


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_stat_strip(draw, y0, y1):
    stats = [
        ("186", "DRONES FIRED AT UKRAINE"),
        ("161", "DRONES DOWNED"),
        ("194", "NATIONS AT COP31, NO DEAL"),
        ("720/9", "INDIA'S TEST RECORD"),
        ("50", "WEMBANYAMA POINTS"),
        ("98.8%", "HONG KONG TURNOUT RECORD"),
    ]
    cell_w = CW / 6
    for i, (num, label) in enumerate(stats):
        cx = MX + cell_w * i + cell_w / 2
        nw = draw.textlength(num, font=SANS_BIG)
        draw.text((cx - nw / 2, y0 + 4), num, font=SANS_BIG, fill=RED)
        lw = draw.textlength(label, font=SANS_XXS)
        draw.text((cx - lw / 2, y0 + 42), label, font=SANS_XXS, fill=GREY)
        if i:
            x = MX + cell_w * i
            draw.line([(x, y0 + 8), (x, y1 - 8)], fill=(200, 192, 176), width=1)


def burst(draw, cx, cy, r_out, r_in, n, fill):
    """Star-burst polygon."""
    import math
    pts = []
    for i in range(n * 2):
        ang = math.pi * i / n - math.pi / 2
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def panel_cop31(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(15, 76, 76))
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(11, 58, 58))
    # globe
    gx, gy, gr = x + w // 2 - 30, y + 62, 42
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(61, 155, 109))
    draw.ellipse([gx - 26, gy - 30, gx + 2, gy - 4], fill=(46, 125, 84))
    draw.ellipse([gx + 4, gy + 6, gx + 30, gy + 30], fill=(46, 125, 84))
    # crack
    draw.line([(gx - 8, gy - gr), (gx + 6, gy - 12), (gx - 4, gy + 8),
               (gx + 10, gy + gr - 4)], fill=(179, 39, 30), width=4)
    # sun
    draw.ellipse([x + w - 52, y + 14, x + w - 26, y + 40], fill=(232, 180, 74))
    # NO DEAL tag
    tag = "NO DEAL"
    tw = draw.textlength(tag, font=SANS_TINY_B)
    tx = gx - tw / 2 - 6
    draw.rectangle([tx, y + h - 46, tx + tw + 12, y + h - 26], fill=RED)
    draw.text((tx + 6, y + h - 44), tag, font=SANS_TINY_B, fill=(255, 255, 255))
    draw.rectangle([x + w - 78, y + h - 20, x + w, y + h], fill=(0, 0, 0))
    draw.text((x + w - 72, y + h - 19), "ILLUSTRATION", font=SANS_TINY,
              fill=(255, 255, 255))


def panel_drones(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(16, 28, 46))
    # moon
    draw.ellipse([x + w - 56, y + 12, x + w - 28, y + 40], fill=(232, 228, 208))
    # stars
    for sx, sy in [(30, 18), (90, 30), (150, 14), (210, 26), (60, 46), (250, 48)]:
        draw.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2],
                     fill=(200, 205, 215))
    # searchlight beams
    draw.polygon([(x + 60, y + h), (x + 120, y + h), (x + 200, y + 30)],
                 fill=(58, 76, 102))
    draw.polygon([(x + 220, y + h), (x + 260, y + h), (x + 150, y + 34)],
                 fill=(48, 64, 88))
    # drones: small diamonds
    for dx, dy in [(70, 34), (150, 22), (215, 40), (110, 52)]:
        draw.polygon([(x + dx, y + dy - 7), (x + dx + 8, y + dy),
                      (x + dx, y + dy + 7), (x + dx - 8, y + dy)],
                     fill=(154, 165, 177))
        draw.ellipse([x + dx - 2, y + dy - 2, x + dx + 2, y + dy + 2],
                     fill=RED)
    # buildings
    draw.rectangle([x + 10, y + h - 52, x + 70, y + h], fill=(8, 16, 28))
    draw.rectangle([x + 80, y + h - 38, x + 130, y + h], fill=(8, 16, 28))
    draw.rectangle([x + 230, y + h - 46, x + 300, y + h], fill=(8, 16, 28))
    # explosion burst
    burst(draw, x + w // 2 + 20, y + h - 30, 26, 12, 8, (232, 120, 40))
    burst(draw, x + w // 2 + 20, y + h - 30, 14, 6, 8, (245, 200, 80))
    draw.rectangle([x + w - 78, y + h - 20, x + w, y + h], fill=(0, 0, 0))
    draw.text((x + w - 72, y + h - 19), "ILLUSTRATION", font=SANS_TINY,
              fill=(255, 255, 255))


def panel_bahrain(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(47, 93, 122))
    draw.rectangle([x, y + 66, x + w, y + h], fill=(24, 62, 84))
    # sun
    draw.ellipse([x + 18, y + 12, x + 44, y + 38], fill=(232, 180, 74))
    # tanker
    draw.rectangle([x + 16, y + 78, x + 190, y + 104], fill=(12, 14, 16))
    draw.rectangle([x + 16, y + 98, x + 190, y + 104], fill=(140, 30, 24))
    for i, col in enumerate([(179, 39, 30), (232, 180, 74), (61, 155, 109),
                             (232, 228, 208)]):
        cx0 = x + 26 + i * 42
        draw.rectangle([cx0, y + 58, cx0 + 36, y + 78], fill=col)
    # radar dish
    rx = x + 250
    draw.line([(rx, y + 104), (rx, y + 56)], fill=(232, 228, 208), width=4)
    draw.arc([rx - 26, y + 30, rx + 26, y + 82], start=200, end=340,
             fill=(232, 228, 208), width=4)
    draw.line([(rx, y + 56), (rx + 22, y + 38)], fill=(232, 228, 208), width=3)
    # blast
    burst(draw, x + 215, y + 44, 18, 8, 8, (245, 180, 60))
    # waves
    for wx in range(0, w - 30, 44):
        draw.arc([x + wx, y + h - 14, x + wx + 30, y + h + 2], start=180,
                 end=360, fill=(120, 160, 185), width=2)
    draw.rectangle([x + w - 78, y + h - 20, x + w, y + h], fill=(0, 0, 0))
    draw.text((x + w - 72, y + h - 19), "ILLUSTRATION", font=SANS_TINY,
              fill=(255, 255, 255))


# Simplified continent outlines as (lon, lat) points.
CONTINENTS = {
    "na": [(-168, 66), (-140, 70), (-120, 71), (-100, 73), (-85, 72), (-75, 70),
           (-65, 60), (-55, 52), (-60, 45), (-70, 42), (-76, 35), (-81, 26),
           (-87, 21), (-95, 18), (-97, 15), (-90, 13), (-83, 9), (-80, 9),
           (-85, 12), (-92, 15), (-100, 18), (-105, 21), (-112, 25),
           (-118, 32), (-124, 40), (-124, 48), (-130, 54), (-140, 60),
           (-152, 58), (-162, 58), (-168, 66)],
    "sa": [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
           (-70, -25), (-71, -32), (-73, -40), (-74, -48), (-70, -54),
           (-66, -55), (-68, -50), (-64, -42), (-58, -35), (-52, -32),
           (-47, -26), (-40, -22), (-38, -15), (-35, -8), (-38, -4),
           (-43, -2), (-50, 0), (-54, 2), (-60, 6), (-66, 9), (-72, 11),
           (-77, 8)],
    "af": [(-6, 35), (-10, 31), (-16, 25), (-17, 20), (-17, 15), (-16, 11),
           (-13, 8), (-8, 5), (-4, 5), (2, 6), (6, 4), (9, 4), (13, 0),
           (12, -6), (13, -12), (12, -18), (14, -24), (16, -29), (20, -35),
           (26, -34), (32, -29), (36, -24), (40, -16), (40, -10), (43, -4),
           (48, -1), (51, 2), (51, 11), (45, 11), (41, 14), (38, 18),
           (35, 23), (33, 28), (32, 31), (28, 32), (22, 33), (15, 33),
           (10, 37), (0, 36), (-6, 35)],
    "eu": [(-10, 37), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-1, 49),
           (2, 51), (5, 53), (8, 55), (8, 57), (11, 59), (6, 60), (6, 62),
           (12, 64), (15, 67), (20, 69), (26, 71), (31, 70), (35, 68),
           (40, 68), (45, 68), (50, 69), (55, 69), (60, 69), (66, 69),
           (72, 72), (78, 72), (84, 73), (90, 75), (96, 76), (102, 77),
           (108, 76), (114, 75), (120, 74), (126, 72), (132, 71), (138, 72),
           (144, 71), (150, 70), (156, 69), (160, 68), (162, 66), (166, 66),
           (170, 66), (178, 65), (178, 62), (172, 60), (166, 60), (160, 56),
           (156, 51), (150, 48), (144, 44), (141, 40), (138, 36), (135, 34),
           (132, 33), (129, 31), (127, 35), (126, 38), (122, 39), (120, 36),
           (121, 31), (118, 25), (114, 22), (110, 20), (108, 17), (105, 9),
           (103, 7), (100, 8), (98, 10), (97, 16), (94, 17), (92, 21),
           (90, 22), (88, 22), (86, 20), (82, 17), (80, 13), (77, 8),
           (75, 11), (72, 20), (68, 23), (66, 25), (62, 25), (58, 25),
           (56, 27), (54, 26), (52, 25), (50, 29), (48, 30), (46, 30),
           (43, 28), (41, 27), (39, 23), (37, 19), (35, 15), (34, 12),
           (36, 11), (39, 12), (43, 12), (44, 15), (42, 18), (39, 21),
           (36, 25), (34, 28), (32, 31), (30, 32), (26, 33), (22, 34),
           (18, 35), (14, 36), (10, 37), (5, 37), (0, 36), (-5, 35),
           (-10, 37)],
    "au": [(113, -22), (114, -30), (115, -35), (118, -35), (124, -33),
           (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
           (145, -38), (150, -37), (153, -32), (153, -27), (150, -23),
           (146, -19), (142, -15), (142, -11), (140, -17), (136, -15),
           (135, -12), (132, -11), (130, -13), (126, -14), (122, -17),
           (118, -20), (113, -22)],
    "jp": [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 36),
           (141, 39), (141, 41), (142, 43), (144, 44), (143, 42), (141, 39),
           (139, 37), (137, 36), (135, 34), (133, 34), (131, 32), (130, 31)],
    "nz": [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38),
           (178, -37), (175, -40), (173, -42), (170, -44), (167, -45)],
}

# Pins: (story number, lon, lat, dx, dy) — dx/dy shift the badge off the point.
PINS = [
    (1, 30.7, 36.9, -16, 12),
    (2, 30.5, 50.5, -16, -14),
    (3, 50.6, 26.2, 12, 10),
    (4, 114.1, 22.5, 16, 14),
    (5, 56.5, 26.6, 0, 12),
    (6, 34.5, 31.5, 12, 14),
    (8, 33.4, 47.9, 14, 10),
    (9, 22.0, 50.0, -16, -4),
    (10, 20.1, 32.1, -14, -12),
    (11, 92.0, 21.4, 12, -10),
    (12, 6.3, 4.8, -12, 10),
    (15, 106.1, -6.1, 12, 10),
    (16, 127.8, 26.2, 16, -12),
    (17, -108.5, 25.6, -12, 12),
    (18, -75.9, -11.2, -12, -10),
    (22, 174.8, -41.3, -14, 0),
    (24, -115.1, 36.2, 12, -12),
    (25, 114.2, 22.3, -16, -14),
]


def draw_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=MAP_NAVY)
    # Crop to lon -170..180, lat -60..85 so the aspect stays near true.
    lon0, lon1, lat1, lat0 = -170, 180, 85, -60
    sx = w / (lon1 - lon0)
    sy = h / (lat1 - lat0)

    def proj(lon, lat):
        px = x + (lon - lon0) * sx
        py = y + (lat1 - lat) * sy
        return px, py

    for gx in range(-150, 181, 30):
        px, _ = proj(gx, 0)
        draw.line([(px, y), (px, y + h)], fill=MAP_GRID, width=1)
    for gy in range(-60, 91, 30):
        _, py = proj(0, gy)
        draw.line([(x, py), (x + w, py)], fill=MAP_GRID, width=1)
    for pts in CONTINENTS.values():
        draw.polygon([proj(lon, lat) for lon, lat in pts], fill=LAND)
    for num, lon, lat, dx, dy in PINS:
        px, py = proj(lon, lat)
        bx, by = px + dx, py + dy
        draw.line([(px, py), (bx, by)], fill=(255, 255, 255), width=1)
        draw.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=RED,
                     outline=(255, 255, 255), width=1)
        label = str(num)
        tw = draw.textlength(label, font=SANS_TINY_B)
        draw.text((bx - tw / 2, by - 6), label, font=SANS_TINY_B,
                  fill=(255, 255, 255))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 74], fill=NAVY)
    d.text((MX, 12), "WORLD NEWS", font=SERIF_B, fill=(255, 255, 255))
    date_txt = "SUNDAY, 22 NOVEMBER 2026"
    dw = d.textlength(date_txt, font=SANS_MD)
    d.text((W - MX - dw, 26), date_txt, font=SANS_MD, fill=(255, 255, 255))
    d.rectangle([0, 74, W, 78], fill=RED)

    # Subline
    d.text((MX, 88), "36 STORIES  ·  SEVEN REGIONS  ·  ONE DAY",
           font=SANS_SM_B, fill=INK)
    src = "SOURCES: AP · REUTERS · AFP · CNN · AL JAZEERA"
    sw = d.textlength(src, font=SANS_XS)
    d.text((W - MX - sw, 90), src, font=SANS_XS, fill=GREY)

    # Stat strip
    draw_stat_strip(d, 112, 164)
    d.line([(MX, 166), (MX + CW, 166)], fill=(200, 192, 176), width=1)

    # Lead panels
    panels = [
        ("1  ·  ANTALYA, TURKEY — CLIMATE", (32, 96, 63),
         "Climate talks collapse with no deal", panel_cop31),
        ("2  ·  KYIV REGION, UKRAINE — WAR", (138, 59, 31),
         "186 drones fired at Ukraine overnight", panel_drones),
        ("3  ·  MANAMA, BAHRAIN — CLAIM", (47, 93, 122),
         "Iran claims two US radars hit; Bahrain denies it", panel_bahrain),
    ]
    panel_w = 312
    panel_gap = 16
    py0, ph = 178, 122
    for i, (head, hcol, headline, painter) in enumerate(panels):
        px = MX + i * (panel_w + panel_gap)
        d.rectangle([px, py0, px + panel_w, py0 + 20], fill=hcol)
        d.text((px + 8, py0 + 3), head, font=SANS_TINY_B, fill=(255, 255, 255))
        painter(d, px, py0 + 20, panel_w, ph)
        lines = wrap(d, headline, SANS_B, panel_w)
        ly = py0 + 20 + ph + 6
        for line in lines[:2]:
            d.text((px, ly), line, font=SANS_B, fill=INK)
            ly += 19

    # Diplomacy band
    by0, by1 = 372, 414
    d.rectangle([MX, by0, MX + CW, by1], fill=BAND)
    d.rectangle([MX, by0, MX + 6, by1], fill=RED)
    d.text((MX + 16, by0 + 6), "DIPLOMACY", font=SANS_SM_B, fill=RED)
    d.text((MX + 16, by0 + 22), "4  ·  SHENZHEN, CHINA", font=SANS_XS,
           fill=GREY)
    d.text((MX + 150, by0 + 10),
           "Trump and Putin hold separate talks after Shenzhen summit",
           font=SANS_B, fill=INK)

    # Numbered grid: stories 5-27
    grid = [
        "Tankers hit near Strait of Hormuz",
        "Hamas seeks talks after Gaza aid-van deaths",
        "Settlers torch cars and homes in West Bank",
        "Russian strike on Zelenskyy's hometown kills two, wounds 60",
        "Poland: three Russian missiles entered our airspace",
        "Blast hits Russian warship docked in Libya",
        "Rohingya hail court genocide verdict",
        "Nigeria boat toll rises to at least 24",
        "US seeks answers from Nvidia on China chip sales",
        "US-China power gap at record low, index finds",
        "Indonesia factory fire: 3 dead, 36 missing",
        "Shuri Castle hall reborn in ceremony",
        "Mexico cartel boss seized; 11 killed in raid",
        "Peru quake toll: one dead, 853 homeless",
        "EU and Indonesia sign landmark trade deal",
        "US stocks slide into correction",
        "Russian cargo ship hit in Baltic Sea",
        "India declare record 720/9 in Wellington Test",
        "Wembanyama drops 50 in Spurs' 114-91 win",
        "Verstappen wins wild Las Vegas Grand Prix",
        "Hong Kong vote sets record 98.8% turnout",
        "Anthropic shares slide after record debut",
        "AI rout hits Japan and Korea",
    ]
    gy0 = 428
    row_h = 40
    col_w = (CW - 2 * 16) // 3
    for idx, text in enumerate(grid):
        num = 5 + idx
        col = idx % 3
        row = idx // 3
        cx = MX + col * (col_w + 16)
        cy = gy0 + row * row_h
        d.text((cx, cy), str(num), font=SANS_NUM, fill=RED)
        nw = d.textlength(str(num), font=SANS_NUM)
        lines = wrap(d, text, SANS, col_w - nw - 10)
        ly = cy + 1
        for line in lines[:2]:
            d.text((cx + nw + 8, ly), line, font=SANS, fill=INK)
            ly += 17

    # Bottom: map + ALSO ON
    bot_y = 756
    map_w, map_h = 560, 210
    d.text((MX, bot_y), "WHERE IT HAPPENED", font=SANS_SM_B, fill=RED)
    d.text((MX + 168, bot_y + 2), "PINS MATCH STORY NUMBERS", font=SANS_XS,
           fill=GREY)
    draw_map(d, MX, bot_y + 22, map_w, map_h)

    ax = MX + map_w + 24
    aw = W - MX - ax
    d.text((ax, bot_y), "ALSO ON", font=SANS_SM_B, fill=RED)
    also = [
        "COP31 draft dropped $120bn aid target",
        "NATO to meet Monday on Poland breach",
        "Russia fired 111 missiles in Friday barrage",
        "Nvidia falls 14% as SEC probes its books",
        "India close in on first Test win in NZ since 2009",
        "90 nations sign COP31 electrification pledge",
        "EU rejects COP31 text over fossil fuels",
        "Iran says it downed US drone over Qeshm",
        "NATO: we will defend every inch of Poland",
    ]
    ay = bot_y + 20
    for i, text in enumerate(also):
        num = 28 + i
        d.text((ax, ay), str(num), font=SANS_NUM, fill=RED)
        nw = d.textlength(str(num), font=SANS_NUM)
        lines = wrap(d, text, SANS_S, aw - nw - 10)
        ly = ay + 1
        for line in lines[:2]:
            d.text((ax + nw + 8, ly), line, font=SANS_S, fill=INK)
            ly += 16
        ay += 24

    # Footer
    d.line([(MX, 994), (MX + CW, 994)], fill=(200, 192, 176), width=1)
    d.text((MX, 1002),
           "ALL STORIES REPORTED ON 22 NOVEMBER 2026  ·  PANELS ARE FLAT "
           "DRAWINGS, NOT PHOTOS", font=SANS_XS, fill=GREY)
    tail = "ONE IMAGE  ·  ONE DAY"
    tw = d.textlength(tail, font=SANS_XS)
    d.text((W - MX - tw, 1002), tail, font=SANS_XS, fill=GREY)

    img.save(OUT, "PNG")
    print("saved", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()
