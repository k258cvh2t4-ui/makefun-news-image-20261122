#!/usr/bin/env python3
"""Build the Nov 22 2026 world-news front page (1024x1024) for make.fun news-image-20261122.
Pure PIL, deterministic output, accurate text only.
"""
import glob
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 236)
NAVY = (22, 35, 58)
RED = (179, 38, 30)
INK = (28, 28, 28)
GREY = (90, 90, 90)
BAND = (233, 237, 242)
RULE = (200, 192, 176)

def font(path_glob, size):
    hits = sorted(glob.glob(path_glob))
    if not hits:
        raise FileNotFoundError(path_glob)
    return ImageFont.truetype(hits[0], size)

F_SERIF_B = lambda s: font('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', s)
F_B = lambda s: font('/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf', s)
F_R = lambda s: font('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf', s)

def wrap(draw, text, fnt, max_w):
    """Greedy wrap to pixel width; returns list of lines."""
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def trunc(draw, text, fnt, max_w):
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    while text and draw.textlength(text + '...', font=fnt) > max_w:
        text = text[:-1]
    return text + '...'

img = Image.new('RGB', (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- masthead ----------
d.rectangle([0, 0, W, 86], fill=NAVY)
d.text((32, 16), 'WORLD NEWS', font=F_SERIF_B(46), fill=(255, 255, 255))
d.text((992, 30), 'SUNDAY, 22 NOVEMBER 2026', font=F_B(19), fill=(255, 255, 255), anchor='ra')
d.rectangle([0, 86, W, 90], fill=RED)

# ---------- subline ----------
y = 100
d.text((32, y), '31 STORIES  ·  SIX CONTINENTS  ·  ONE DAY', font=F_B(15), fill=INK)
d.text((992, y), 'SOURCES: AP · REUTERS · AFP · AL JAZEERA', font=F_R(13), fill=GREY, anchor='ra')
d.line([32, 126, 992, 126], fill=RULE, width=1)

# ---------- lead story ----------
y = 138
d.text((32, y), 'CLIMATE  —  ANTALYA, TURKEY', font=F_B(15), fill=RED)
y += 26
d.text((32, y), 'Climate talks collapse with no deal', font=F_B(40), fill=INK)
y += 52
lead = ('The COP31 summit ends with no agreement after governments fail to bridge divides '
        'over fossil fuels and climate finance. The EU formally objects to a final text '
        'that never mentions them.')
for line in wrap(d, lead, F_R(16), 960):
    d.text((32, y), line, font=F_R(16), fill=(60, 60, 60))
    y += 22

# ---------- diplomacy band ----------
y += 10
band_y0 = y
d.rectangle([32, y, 992, y + 54], fill=BAND)
d.rectangle([32, y, 38, y + 54], fill=RED)
d.text((52, y + 7), 'DIPLOMACY', font=F_B(14), fill=RED)
# single-line diplomacy text (fits at 15px across 830px after the label)
dip = ('Trump, Xi and Putin meet in Shenzhen — first trilateral summit; nuclear vow, '
       'no Ukraine breakthrough.')
dip_line = trunc(d, dip, F_B(15), 830)
d.text((150, y + 7), dip_line, font=F_B(15), fill=INK)
y = band_y0 + 54

# ---------- sections ----------
SECTIONS_LEFT = [
    ('MIDDLE EAST', (156, 61, 30), [
        ('Iran strikes three tankers near Strait of Hormuz',
         'Tehran hits tankers as the US–Iran standoff over a naval blockade deepens.'),
        ('Iran hits US bases in Bahrain',
         'Missiles and drones strike bases; a civilian site is damaged, two people hurt.'),
        ('Gaza strike kills three in food van',
         'Hamas calls an urgent meeting of ceasefire mediators.'),
        ('Settlers torch cars and homes in West Bank',
         'Raids hit villages near Ramallah; 12 vehicles and several homes burned.'),
    ]),
    ('EUROPE & UKRAINE', (46, 90, 136), [
        ('Zelenskyy: Ukraine sank Russian warship off Libya',
         'Kyiv confirms it was behind the drone attack on the vessel at Benghazi.'),
        ('Russian missile hits Kryvyi Rih',
         'Two killed, a seven-year-old boy among them; 60 wounded.'),
        ('Russian missiles land in Poland',
         'NATO calls it a violation as Europe held military drills nearby.'),
        ('UK and EU agree post-Brexit reset',
         'London and Brussels strike a deal for closer ties in a major reset.'),
        ('Denmark expels Russian defence attaché',
         'Copenhagen says Russian intelligence plotted to kill a Ukrainian rapper.'),
    ]),
    ('WORLD COURT & AFRICA', (51, 102, 102), [
        ('World Court: Myanmar committed genocide',
         'ICJ finds Myanmar responsible for genocide against the Rohingya in 2017.'),
        ('Nigeria boat capsizes on way to funeral',
         'At least 24 dead as a boat carrying mourners capsizes in Bayelsa State.'),
        ('Rohingya welcome genocide verdict',
         'Refugees in Bangladesh welcome it but want to return home.'),
    ]),
]
SECTIONS_RIGHT = [
    ('ASIA-PACIFIC', (47, 107, 82), [
        ('US lead over China in Asia narrows to record low',
         'Lowy index: US 78.9, China 73.6 — the tightest gap since 2018.'),
        ('China’s chipmakers gain ground despite US curbs',
         'CXMT and YMTC drive Beijing’s push for memory-chip self-sufficiency.'),
        ('US probes Nvidia chip flows to China',
         'Officials examine how AI chips reached China despite export controls.'),
        ('Thai court upholds royal-defamation verdict',
         'Opposition lawmaker’s sentence is cut to three years.'),
        ('Indonesia factory fire: three dead, dozens missing',
         'Rescuers search the ruins of a candy factory in Cikande.'),
        ('Shuri Castle hall reopens in Okinawa',
         'The restored hall opens seven years after the castle fire.'),
    ]),
    ('AMERICAS', (138, 109, 27), [
        ('Mexico captures cartel boss ‘El Chapo Isidro’',
         'Eleven killed in the Sinaloa raid, including four soldiers.'),
        ('US stocks slide into correction',
         'S&P 500 falls 3.7% and Nasdaq 5.3% as the AI sell-off spreads to Asia.'),
        ('Peru quake, magnitude 6.7',
         'One dead, 16 injured and 853 displaced near Junín in the Andes.'),
    ]),
    ('MARKETS & TRADE', (91, 74, 138), [
        ('EU and Indonesia sign landmark trade deal',
         'After almost ten years of talks, tariffs fall on up to 98.5% of goods.'),
        ('China eases margin-trading rules',
         'Minimum margin ratio drops to 80% from 100% on 30 November.'),
        ('AI sell-off spreads to Japan and Korea',
         'Asian tech shares slide as the US rout spills across the Pacific.'),
    ]),
]

COL_W = 465
def draw_column(x0, y0, sections):
    y = y0
    for title, color, items in sections:
        d.rectangle([x0, y, x0 + COL_W, y + 26], fill=color)
        d.text((x0 + 10, y + 4), title, font=F_B(14), fill=(255, 255, 255))
        y += 26 + 8
        for t, s in items:
            d.text((x0, y), trunc(d, t, F_B(15), COL_W), font=F_B(15), fill=INK)
            y += 18
            d.text((x0, y), trunc(d, s, F_R(13), COL_W), font=F_R(13), fill=(70, 70, 70))
            y += 15 + 7
    return y

col_top = y + 12
end_l = draw_column(32, col_top, SECTIONS_LEFT)
end_r = draw_column(527, col_top, SECTIONS_RIGHT)
y = max(end_l, end_r) + 4
print('columns end y =', y)

# ---------- also on ----------
d.line([32, y, 992, y], fill=RULE, width=1)
y += 10
d.text((32, y), 'ALSO ON', font=F_B(14), fill=RED)
y += 22
also = ('India youth wing protests at Meta offices  ·  Lewis Pugh swims the war-hit Strait of Hormuz  ·  '
        'Jeweller Paolo Bulgari dies at 89  ·  US Navy may run with nine carriers for five years  ·  '
        'China–Japan ties fray over Taiwan and minerals')
for line in wrap(d, also, F_R(13), 960):
    d.text((32, y), line, font=F_R(13), fill=(70, 70, 70))
    y += 18
y += 6
d.line([32, y, 992, y], fill=RULE, width=1)
y += 8
d.text((32, y), 'ALL STORIES REPORTED ON 22 NOVEMBER 2026', font=F_B(12), fill=GREY)
d.text((992, y), 'ONE IMAGE · ONE DAY', font=F_B(12), fill=GREY, anchor='ra')
print('final y =', y)

out = '/home/hatch/workspace/makefun-news-image-20261122/entry.png'
img.save(out, 'PNG', optimize=True)
import os
print('saved', out, os.path.getsize(out), 'bytes')
