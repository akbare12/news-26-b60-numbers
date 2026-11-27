#!/usr/bin/env python3
"""NEWS-26 b60 numbers — renders entry.png (1024x1024) for news-image-20261126.
Layout V58: masthead + DATE CHECK 2 lines, 3 hero HORIZONTAL BANDS stacked
full-width with ART RIGHT 25%, map strip, 2x5 numbered cards, ALSO 2 cols,
timeline, footer. All copy written fresh from KANON-20261126 + brief.
Every string is measured with PIL font metrics and asserted to fit; no
silent truncation anywhere."""
import hashlib
import os
import re
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 12
CW = W - 2 * M
FD = "/usr/share/fonts/truetype/dejavu/"
F = lambda n, s: ImageFont.truetype(FD + n, s)
FB28 = F("DejaVuSans-Bold.ttf", 28)
FB20 = F("DejaVuSans-Bold.ttf", 20)
FB15 = F("DejaVuSans-Bold.ttf", 15)
FB13 = F("DejaVuSans-Bold.ttf", 13)
FB11 = F("DejaVuSans-Bold.ttf", 11)
FB10 = F("DejaVuSans-Bold.ttf", 10)
FB9 = F("DejaVuSans-Bold.ttf", 9)
FR12 = F("DejaVuSans.ttf", 12)
FR11 = F("DejaVuSans.ttf", 11)
FR10 = F("DejaVuSans.ttf", 10)
FR9 = F("DejaVuSans.ttf", 9)
FR8 = F("DejaVuSans.ttf", 8)

PAPER = (247, 243, 232)
INK = (26, 26, 26)
NAVY = (20, 50, 79)
RED = (179, 38, 30)
GOLD = (176, 124, 0)
TEAL = (14, 107, 107)
GREY = (90, 88, 80)
LINE = (180, 172, 150)
CARD = (255, 255, 255)
OCEAN = (207, 227, 238)
LAND = (216, 205, 178)
LANDB = (150, 140, 115)

_tmp = Image.new("RGB", (8, 8))
_dm = ImageDraw.Draw(_tmp)


def tw(s, font):
    return _dm.textbbox((0, 0), s, font=font)[2]


def th(s, font):
    b = _dm.textbbox((0, 0), s, font=font)
    return b[3] - b[1]


def wrap(s, font, width):
    """Greedy wrap by measured width. Raises if any single word is too wide."""
    lines, cur = [], ""
    for w in s.split(" "):
        if tw(w, font) > width:
            raise AssertionError("word too wide: %r (%d > %d)" % (w, tw(w, font), width))
        t = (cur + " " + w).strip() if cur else w
        if tw(t, font) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(s, font, width, max_lines, tag):
    ls = wrap(s, font, width)
    assert len(ls) <= max_lines, "%s: %d lines > %d: %r" % (tag, len(ls), max_lines, s)
    return ls


def draw_lines(d, lines, x, y, font, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


# ---------------- content (fresh from kanon + brief) ----------------
HEROES = [
    dict(tag="[C]", kicker="NEW YORK  |  THANKSGIVING DAY",
         title="MACY'S 100TH PARADE POSTPONED \u2014 FIRST TIME FOR WEATHER",
         deck=("Thanksgiving parade in New York delayed by a huge East Coast storm; "
               "high wind warning from 10:00, gusts to 60 mph. Balloons grounded "
               "under the safety rules."),
         why=("WHY IT MATTERS: A century-old Thanksgiving ritual bows to the "
              "weather on its 100th birthday."),
         stat="100TH PARADE  \u2022  GUSTS 60 MPH  \u2022  BACK SAT 28 NOV 08:30 ET",
         art="balloon"),
    dict(tag="[CL]", kicker="STRAIT OF HORMUZ  |  IRAN WAR WIDENS",
         title="IRGC CLAIMS MINES HIT 2 TANKERS IN HORMUZ",
         deck=("Tehran claims two tankers exploded and burned north of Khasab, one a "
               "supertanker carrying over 2 million barrels of crude. Claim "
               "unverified; a separate projectile blast was logged near a "
               "tanker west of Dubai."),
         why=("WHY IT MATTERS: The Iran war widens to the world's busiest oil "
              "chokepoint, lifting Brent."),
         stat="2 TANKERS  \u2022  2M BARRELS  \u2022  BRENT $93.8",
         art="tanker"),
    dict(tag="[C]", kicker="GLOBAL MARKETS  |  TRADE",
         title="TRUMP TARIFFS: MARKETS REBOUND AS SALVO LANDS SOFT",
         deck=("European and Asian markets rebound as the new US tariff salvo lands "
               "softer than feared: the levies will not stack on July duties, and "
               "no nasty surprise emerged."),
         why=("WHY IT MATTERS: Traders read the tariff salvo as manageable, not a "
              "trade-war shock."),
         stat="14 PARTNERS  \u2022  20% CHINA  \u2022  STOXX +1.6%",
         art="chart"),
]

CARDS = [
    dict(n="01", region="GAZA", tag="[C]",
         head="Israel strike kills Hamas education deputy",
         deck=("Khaled Abu Nada and wife killed in Deir al-Balah flat; 9 dead "
               "overnight, third night of strikes."),
         stat="9 KILLED \u2022 DEIR AL-BALAH"),
    dict(n="02", region="KYIV", tag="[C]",
         head="Russian ballistic missiles hit Kyiv mall",
         deck="Desnianskyi mall struck amid 113 drones; 7 hurt overnight.",
         stat="7 HURT \u2022 113 DRONES"),
    dict(n="03", region="BOGOR", tag="[C]",
         head="Flooded illegal gold mine: 13 dead",
         deck=("Bogor mine flood toll rises to 13 dead, 13 missing, 100m "
               "underground after heavy rain."),
         stat="13 DEAD \u2022 13 MISSING"),
    dict(n="04", region="ISRAEL", tag="[C]",
         head="Judge urges dropping Netanyahu bribe case",
         deck=("Judge in PM's corruption trial recommends prosecutors drop Case "
               "4000, the sole bribery charge."),
         stat="CASE 4000 \u2022 BRIBERY CHARGE"),
    dict(n="05", region="N. KOREA", tag="[C]",
         head="Kim tours nuclear plant, urges tactical nukes",
         deck=("Kim Jong Un visits nuclear-material plant and calls for wider use "
               "of tactical nuclear arms."),
         stat="TACTICAL NUCLEAR PUSH"),
    dict(n="06", region="SPACE", tag="[CL]",
         head="FCC clears 1M SpaceX orbital data satellites",
         deck=("SpaceX Starmind approved 25 Nov: first US nod for AI data centres "
               "in orbit."),
         stat="1M SATELLITES \u2022 25 NOV"),
    dict(n="07", region="BRITAIN", tag="[C]",
         head="UK net migration falls to 77,000",
         deck=("Net migration in year to June 2026 is lowest since 1997 outside "
               "the pandemic."),
         stat="77,000 \u2022 LOWEST SINCE 1997"),
    dict(n="08", region="RUSSIA", tag="[C]",
         head="Russia approves record post-Soviet military budget",
         deck="Moscow signs off its biggest defence budget since the Soviet era.",
         stat="RECORD MILITARY BUDGET"),
    dict(n="09", region="THAILAND", tag="[C]",
         head="Bangkok oil depot blast hurts 7",
         deck=("Explosion at Bangkok oil depot injures 7 and triggers evacuation "
               "alert; fire out in 30 minutes."),
         stat="7 HURT \u2022 FIRE OUT IN 30 MIN"),
    dict(n="10", region="GERMANY", tag="[C]",
         head="Germany arrests 2 over synagogue plot",
         deck=("Two Iraqi suspects held in Cologne and Heidelberg over a planned "
               "synagogue attack in late March."),
         stat="2 HELD \u2022 COLOGNE + HEIDELBERG"),
]

ALSO = [
    "Ukrainian drones damage 5 jets at Savasleyka base [R]",
    "Kharkiv couple, 37 and 38, die in flat strike [C]",
    "18 hurt in Kryvyi Rih strike [C]",
    "Subkhankulovo pump station burns in drone hit [R]",
    "UKMTO: explosion by vessel 18nm east of Khasab, 25 Nov [CL]",
    "Saudi defences down 2 missiles bound for Riyadh, 25 Nov [CL]",
    "Houthi claim strike on Ras Tanura refinery, 25 Nov [CL]",
    "OPEC+ meets 29 Nov on 2027 output [C]",
    "Nvidia shares -3.91% to $149.30 [C]",
    "Gold $3,572/oz, down 8% in a month [C]",
    "Philadelphia parade cancelled in the storm [C]",
    "Eisenkot seals first Israel coalition deal [C]",
    "Merz warns Russia's aims go beyond Ukraine [C]",
    "Britain on drone-threat alert at air bases [R]",
    "Norse Atlantic suspends all flights [C]",
    "Poundland in administration, 11,000 jobs at risk [C]",
    "Malaysia sues Google for $146M [C]",
    "Kenya court halts US-backed Ebola facility [C]",
    "Belarus offers to fly Zelensky to Moscow [R]",
    'Kushner calls Putin a "grandmaster of politics" [C]',
    "Estonia to close its border [C]",
    "Copernicus: longest stretch above 2C warming [C]",
    "Nvidia halts AI server shipments to 4 nations [R]",
    "US Bitcoin funds hit record $4.94B [C]",
    "Jazan port hit by Houthi projectile, minor damage \u2014 25 Nov [CL]",
    "Two Italian technicians killed in Iran drone hit in Kuwait [R]",
    "Zelenskiy warns Russia readying new mass strike [C]",
    "Russian refinery in Krasnodar ablaze after drone hit [R]",
    "Settlers smash foundations of Palestinian family homes [C]",
    "North Korea halts missile shipments to Russia [R]",
    "Guinea-Bissau delays elections by two years [C]",
    "Kenya cult leader Mackenzie convicted on terror charges [C]",
    "Romania charges hard-right leader Simion over poll violence [C]",
    "US Army blows up unstable lead azide stockpile in Iowa, 25 Nov [CL]",
    "UKMTO Dubai blast: crew safe, no damage [C]",
    "Russia claims it hit drone-linked sites [CL]",
    "Mamdani to miss Saturday parade for foot surgery [C]",
]

TIMELINE = [
    "UN rights chief Turk warns of atrocity-crime risk [C]",
    "Cargo ship near Odesa claimed hit [CL]",
    "Dollar flat at 103.71 [C]",
    "NBC to air 2025 parade on Thursday [C]",
    "S&P 500 futures +0.5% as Wall Street shuts [C]",
    "Dow +0.33% on Wednesday [C]",
    "WTI +0.2% to $83.32 [C]",
    "MSCI world index +0.4% [C]",
    "Balloon inflation halted on Wednesday night [C]",
]

DATE_L1 = ("DATE CHECK \u2014 THURSDAY 26 NOVEMBER 2026 \u2022 Every story happened or "
           "moved on 26 Nov unless marked 25 Nov.")
DATE_L2 = ("LEFT OUT \u2014 COP31 fail (22 Nov) \u2022 Shenzhou-24 (25 Nov) \u2022 "
           "Cairo tanker 31 dead (25 Nov) \u2022 Cartagena hostages (25 Nov) \u2022 "
           "Australia\u2013Solomon pact (25 Nov) \u2022 UK energy +26% (25 Nov) \u2022 "
           "Huawei verdict (24 Nov)")

# (lon, lat, label) — each pin maps to a story drawn in this image.
PINS = [
    (-74.0, 40.7, "NEW YORK"), (56.2, 26.2, "KHASAB"), (116.4, 39.9, "BEIJING"),
    (30.5, 50.45, "KYIV"), (34.45, 31.5, "GAZA"), (106.8, -6.6, "BOGOR"),
    (-0.1, 51.5, "LONDON"), (100.5, 13.75, "BANGKOK"), (46.7, 24.6, "RIYADH"),
    (37.6, 55.75, "MOSCOW"), (125.75, 39.0, "PYONGYANG"), (7.0, 50.9, "COLOGNE"),
]

LAND_POLYS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-75, 62), (-60, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21),
     (-97, 16), (-105, 20), (-115, 28), (-125, 40), (-145, 60), (-165, 60)],
    [(-80, 10), (-60, 5), (-50, 0), (-35, -8), (-40, -20), (-48, -28),
     (-58, -35), (-65, -45), (-70, -55), (-73, -40), (-72, -20), (-80, -5)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 10), (48, 0), (40, -15), (35, -28), (28, -33), (18, -35),
     (12, -18), (8, 4), (-8, 5)],
    [(-10, 36), (-2, 48), (5, 58), (10, 57), (18, 56), (21, 55), (28, 60),
     (30, 70), (40, 68), (55, 69), (70, 72), (90, 75), (110, 76), (130, 72),
     (150, 70), (170, 66), (178, 65), (162, 58), (158, 52), (142, 45),
     (140, 40), (135, 35), (127, 35), (122, 30), (120, 22), (110, 10),
     (105, 2), (100, 8), (95, 15), (90, 22), (80, 8), (77, 20), (72, 20),
     (66, 25), (60, 25), (57, 26), (52, 28), (48, 30), (44, 29), (40, 36),
     (36, 36), (30, 36), (26, 38), (22, 37), (18, 40), (12, 44), (8, 44),
     (3, 43), (-2, 37), (-9, 37), (-10, 43)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35),
     (140, -38), (147, -39), (150, -37), (153, -27), (146, -19), (142, -11),
     (136, -12), (132, -11), (126, -14), (122, -17), (118, -20)],
    [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 53), (1, 51)],
    [(130, 31), (132, 33), (135, 34), (138, 35), (140, 38), (141, 42),
     (143, 44), (145, 44), (141, 40)],
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10),
     (125, -9), (130, -4), (135, -3), (140, -8), (138, -2)],
    [(-55, 60), (-45, 60), (-40, 64), (-30, 68), (-22, 70), (-30, 76),
     (-50, 76), (-58, 70)],
]

STOP = set("""the a an to of in on at for and or after over near its it is are was
by with from as up hit hits more than into first new us uk will not stack
""".split())
STOP |= set(["nov", "25", "26"])


def tokens(s):
    out = set()
    for t in re.findall(r"[A-Za-z][A-Za-z\-']*", s.lower()):
        t = t.rstrip("s") if len(t) > 4 and t.endswith("s") else t
        if len(t) >= 4 and t not in STOP:
            out.add(t)
    return out


def norm_num(s):
    """Normalise a numeric token so 93.8 == 93.80 == 93.800 (and 08 == 8)."""
    try:
        v = float(s)
    except ValueError:
        return s
    if v == int(v):
        return str(int(v))
    return ("%f" % v).rstrip("0").rstrip(".")


def check_content():
    # TIMELINE is a chronology recap, NOT stories: total counts heroes +
    # cards + ALSO only.
    total = len(HEROES) + len(CARDS) + len(ALSO)
    assert total == 50, "story count %d != 50" % total
    assert len(ALSO) == 37 and len(TIMELINE) == 9, "also/timeline counts"
    all_text = []
    for h in HEROES:
        all_text.append(("hero", h["title"] + " " + h["deck"] + " " + h["why"] + " " + h["stat"]))
        assert h["why"].endswith("."), "WHY must end with period: %r" % h["why"]
        assert h["why"].startswith("WHY IT MATTERS:"), "WHY label missing"
        assert h["tag"] in ("[C]", "[R]", "[CL]"), "hero tag"
        assert "25 Nov" not in h["title"] + " " + h["deck"] or h["tag"] == "[CL]", \
            "25-Nov hero must be [CL]: %s" % h["title"]
    for c in CARDS:
        all_text.append(("card" + c["n"], c["head"] + " " + c["deck"] + " " + c["stat"]))
        assert c["tag"] in ("[C]", "[R]", "[CL]"), "card tag"
        if "25 Nov" in c["deck"] + c["stat"]:
            assert c["tag"] == "[CL]", "25-Nov card must be [CL]: %s" % c["head"]
    for i, a in enumerate(ALSO):
        all_text.append(("also%d" % i, a))
        assert re.search(r"\[(C|R|CL)\]", a), "ALSO item missing tag: %r" % a
        if "25 Nov" in a:
            assert "[CL]" in a, "25-Nov ALSO must be [CL]: %r" % a
    for i, t in enumerate(TIMELINE):
        all_text.append(("tl%d" % i, t))
        assert re.search(r"\[(C|R|CL)\]", t), "timeline item missing tag: %r" % t
    # no story may repeat another: <3 shared distinctive words per pair
    for i in range(len(all_text)):
        for j in range(i + 1, len(all_text)):
            sh = tokens(all_text[i][1]) & tokens(all_text[j][1])
            assert len(sh) < 3, "dup pair %s vs %s shares %s" % (
                all_text[i][0], all_text[j][0], sorted(sh))
    # hero stat figures (2+ digit numbers, NORMALISED) must not reappear
    # in ALSO: "93.8" and "93.80" are the same number.
    for h in HEROES:
        for num in re.findall(r"\d+(?:\.\d+)?", h["stat"]):
            nnum = norm_num(num)
            if len(nnum.replace(".", "")) < 2:
                continue
            for a in ALSO:
                for anum in re.findall(r"\d+(?:\.\d+)?", a):
                    assert norm_num(anum) != nnum, \
                        "hero stat %s repeated in ALSO: %r" % (num, a)
    # banned / left-out words must not appear as stories; Bangchak never
    joined = " ".join(t for _, t in all_text).lower()
    for bad in ["bangchak", "cop31", "shenzhou", "cairo", "cartagena",
                "solomon", "huawei", "energy"]:
        assert bad not in joined, "banned word in stories: %s" % bad
    # DATE CHECK left-out list must not name a story drawn in the image
    for bad in ["cop31", "shenzhou", "cairo", "cartagena", "solomon", "huawei"]:
        assert bad in DATE_L2.lower(), "date-check missing: %s" % bad
    # Kyiv card must be pure Kyiv
    ky = CARDS[1]
    assert ky["deck"] == "Desnianskyi mall struck amid 113 drones; 7 hurt overnight."
    assert ky["stat"] == "7 HURT \u2022 113 DRONES"
    assert "savasleyka" not in ky["deck"].lower() + ky["head"].lower()
    print("content checks OK: %d stories" % total)

# ---------------- drawing ----------------
def rect_dist(px, py, box):
    x0, y0, x1, y1 = box
    dx = max(x0 - px, 0, px - x1)
    dy = max(y0 - py, 0, py - y1)
    return (dx * dx + dy * dy) ** 0.5


def draw_art(d, kind, x0, y0, x1, y1):
    if kind == "balloon":
        d.rectangle([x0, y0, x1, y1], fill=(191, 217, 234))
        d.ellipse([x1 - 52, y0 + 6, x1 - 12, y0 + 46], fill=(255, 214, 90))
        for bx in range(x0 + 8, x1 - 8, 26):
            d.rectangle([bx, y1 - 26, bx + 18, y1], fill=(90, 96, 104))
        d.ellipse([x0 + 30, y0 + 6, x0 + 150, y0 + 62], fill=RED)
        d.ellipse([x0 + 55, y0 + 6, x0 + 125, y0 + 62], fill=(255, 214, 90))
        d.ellipse([x0 + 78, y0 + 6, x0 + 102, y0 + 62], fill=RED)
        d.line([x0 + 70, y0 + 62, x0 + 62, y0 + 78], fill=INK, width=2)
        d.line([x0 + 110, y0 + 62, x0 + 118, y0 + 78], fill=INK, width=2)
        d.rectangle([x0 + 62, y0 + 78, x0 + 118, y1 - 2], fill=(120, 72, 20))
        d.text((x0 + 158, y0 + 10), "100TH", font=FB13, fill=NAVY)
        d.text((x0 + 158, y0 + 30), "PARADE", font=FB10, fill=NAVY)
    elif kind == "tanker":
        d.rectangle([x0, y0, x1, y1], fill=(22, 50, 74))
        d.rectangle([x0, y0 + 62, x1, y1], fill=(16, 42, 64))
        for wx in range(x0 + 10, x1 - 10, 34):
            d.arc([wx, y0 + 70, wx + 26, y0 + 82], 0, 180, fill=(120, 180, 210))
        d.rectangle([x0 + 18, y0 + 48, x1 - 18, y0 + 66], fill=(40, 40, 44))
        d.rectangle([x0 + 18, y0 + 62, x1 - 18, y0 + 66], fill=RED)
        d.rectangle([x0 + 30, y0 + 30, x0 + 90, y0 + 48], fill=(90, 96, 104))
        d.rectangle([x0 + 96, y0 + 36, x0 + 150, y0 + 48], fill=(120, 128, 136))
        d.polygon([(x0 + 165, y0 + 48), (x0 + 180, y0 + 12), (x0 + 195, y0 + 48)],
                  fill=(255, 140, 0))
        d.polygon([(x0 + 185, y0 + 48), (x0 + 198, y0 + 20), (x0 + 212, y0 + 48)],
                  fill=(255, 214, 90))
        d.ellipse([x0 + 205, y0 + 6, x0 + 225, y0 + 22], fill=(200, 200, 200))
        d.ellipse([x0 + 220, y0 + 14, x0 + 236, y0 + 28], fill=(170, 170, 170))
        d.text((x0 + 18, y0 + 6), "2M BARRELS", font=FB13, fill=(255, 255, 255))
    else:  # chart
        d.rectangle([x0, y0, x1, y1], fill=(232, 240, 228))
        d.line([x0 + 10, y0 + 14, x0 + 10, y1 - 12], fill=NAVY, width=2)
        d.line([x0 + 10, y1 - 12, x1 - 8, y1 - 12], fill=NAVY, width=2)
        bars = [18, 26, 22, 36, 46, 58]
        bw = 28
        for i, bh in enumerate(bars):
            bx = x0 + 22 + i * (bw + 6)
            d.rectangle([bx, y1 - 12 - bh, bx + bw, y1 - 12], fill=TEAL)
        pts = [(x0 + 22 + i * 34 + 14, y1 - 12 - bars[i] - 8) for i in range(6)]
        d.line(pts, fill=RED, width=3)
        d.polygon([(pts[-1][0], pts[-1][1] - 12), (pts[-1][0] + 14, pts[-1][1] + 2),
                   (pts[-1][0] - 2, pts[-1][1] + 6)], fill=RED)
        d.text((x0 + 130, y0 + 6), "+1.6%", font=FB13, fill=RED)


def main():
    check_content()
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # masthead
    d.text((M, 6), "THE WORLD IN ONE PAGE", font=FB28, fill=INK)
    rt = "50 STORIES"
    d.text((W - M - tw(rt, FB13), 14), rt, font=FB13, fill=RED)
    d.rectangle([M, 46, W - M, 48], fill=RED)
    # DATE CHECK band (2 lines, measured + asserted)
    assert tw(DATE_L1, FB10) <= CW, "DATE L1 too wide: %d" % tw(DATE_L1, FB10)
    assert tw(DATE_L2, FR9) <= CW, "DATE L2 too wide: %d" % tw(DATE_L2, FR9)
    d.rectangle([M, 50, W - M, 92], fill=(255, 248, 225))
    d.rectangle([M, 50, W - M, 92], outline=NAVY, width=1)
    d.text((M + 6, 54), DATE_L1, font=FB10, fill=NAVY)
    d.text((M + 6, 71), DATE_L2, font=FR9, fill=INK)
    # heroes: 3 horizontal bands, art RIGHT 25%
    y = 92
    for h in HEROES:
        top = y
        stat_top = top + 88
        art_x0, art_x1 = 762, W - M
        d.rectangle([M, top, W - M, top + 112], fill=CARD)
        d.rectangle([M, top, M + 6, top + 112], fill=RED if h["art"] != "chart" else TEAL)
        d.text((M + 16, top + 5), h["kicker"] + "  " + h["tag"], font=FB9, fill=RED)
        assert tw(h["title"], FB15) <= 742, "hero title too wide: %s" % h["title"]
        d.text((M + 16, top + 17), h["title"], font=FB15, fill=INK)
        dl = fit_lines(h["deck"], FR11, 734, 2, "hero deck")
        yb = draw_lines(d, dl, M + 16, top + 36, FR11, INK, 13)
        assert tw(h["why"], FB10) <= 734, "WHY too wide: %s" % h["why"]
        d.text((M + 16, top + 64), h["why"], font=FB10, fill=NAVY)
        why_bottom = top + 64 + th(h["why"], FB10)
        assert stat_top - why_bottom >= 6, "WHY/stat gap %d" % (stat_top - why_bottom)
        assert yb <= top + 62, "hero deck overlaps WHY"
        draw_art(d, h["art"], art_x0, top + 4, art_x1, stat_top - 4)
        d.rectangle([M, stat_top, W - M, top + 112], fill=NAVY)
        assert tw(h["stat"], FB11) <= CW - 12, "hero stat too wide"
        d.text((M + 16, stat_top + 5), h["stat"], font=FB11, fill=(255, 255, 255))
        d.text((W - M - tw(h["tag"], FB11), stat_top + 5), h["tag"], font=FB11,
               fill=(255, 214, 90))
        y = top + 112
    assert y == 428, "hero block end %d" % y
    # map strip: solid header band above map area
    d.rectangle([M, 428, W - M, 448], fill=NAVY)
    d.text((M + 8, 432), "WORLD MAP \u2014 12 PLACES IN TODAY'S NEWS",
           font=FB10, fill=(255, 255, 255))
    map_top, map_bot = 448, 548
    d.rectangle([M, map_top, W - M, map_bot], fill=OCEAN)
    px = lambda lon: M + (lon + 180.0) / 360.0 * CW
    py = lambda lat: map_top + (75.0 - lat) / 130.0 * (map_bot - map_top)
    for poly in LAND_POLYS:
        d.polygon([(px(lo), py(la)) for lo, la in poly], fill=LAND, outline=LANDB)
    dots = [(px(lo), py(la)) for lo, la, _ in PINS]
    for i in range(len(dots)):
        for j in range(i + 1, len(dots)):
            dd = ((dots[i][0] - dots[j][0]) ** 2 + (dots[i][1] - dots[j][1]) ** 2) ** 0.5
            assert dd >= 18, "pins %d-%d only %.1f apart" % (i, j, dd)
    placed = []
    for (lo, la, label), (dx0, dy0) in zip(PINS, dots):
        lw = tw(label, FB9) + 8
        lh = 13
        cands = [(18, 18), (18, -lh - 18), (-lw - 18, 18), (-lw - 18, -lh - 18),
                 (-lw // 2, 18), (-lw // 2, -lh - 18), (18, -7), (-lw - 18, -7),
                 (60, -7), (-lw - 60, -7), (60, 18), (-lw - 60, 18),
                 (18, 40), (-lw - 18, 40), (18, -lh - 40), (-lw - 18, -lh - 40),
                 (60, -lh - 18), (-lw - 60, -lh - 18), (60, 40), (-lw - 60, 40),
                 (-lw // 2, 40), (-lw // 2, -lh - 40), (100, -7), (-lw - 100, -7),
                 (18, -lh - 62), (-lw - 18, -lh - 62), (100, 18), (-lw - 100, 18)]
        got = None
        for ox, oy in cands:
            bx, by = dx0 + ox, dy0 + oy
            box = (bx, by, bx + lw, by + lh)
            if bx < M + 2 or by < map_top + 2 or box[2] > W - M - 2 or box[3] > map_bot - 2:
                continue
            if any(rect_dist(p[0], p[1], box) < 17 for p in dots):
                continue
            if any(not (box[2] + 2 < b[0] or b[2] + 2 < box[0] or box[3] + 2 < b[1]
                       or b[3] + 2 < box[1]) for b in placed):
                continue
            got = box
            break
        assert got is not None, "no label spot for %s" % label
        placed.append(got)
        d.rectangle(got, fill=(255, 255, 255), outline=GREY)
        d.text((got[0] + 4, got[1] + 1), label, font=FB9, fill=INK)
    for (dx0, dy0) in dots:
        d.ellipse([dx0 - 8, dy0 - 8, dx0 + 8, dy0 + 8], fill=(255, 255, 255))
        d.ellipse([dx0 - 5, dy0 - 5, dx0 + 5, dy0 + 5], fill=RED)
    # cards 2x5
    col_w, gap = 193, 8
    for r in range(2):
        for c in range(5):
            card = CARDS[r * 5 + c]
            x0 = M + 1 + c * (col_w + gap)
            y0 = 548 + r * (100 + 5)
            y1 = y0 + 100
            d.rectangle([x0, y0, x0 + col_w, y1], fill=CARD, outline=LINE)
            d.rectangle([x0, y0, x0 + col_w, y0 + 3], fill=NAVY)
            d.text((x0 + 8, y0 + 6), card["n"], font=FB13, fill=RED)
            d.text((x0 + 34, y0 + 8), card["region"], font=FB10, fill=NAVY)
            d.text((x0 + col_w - 8 - tw(card["tag"], FB9), y0 + 8),
                   card["tag"], font=FB9, fill=RED)
            hl = fit_lines(card["head"], FB10, col_w - 16, 2, "card head " + card["n"])
            hy = draw_lines(d, hl, x0 + 8, y0 + 24, FB10, INK, 12)
            assert hy <= y0 + 48, "card head too low " + card["n"]
            dl = fit_lines(card["deck"], FR9, col_w - 16, 3, "card deck " + card["n"])
            dy = draw_lines(d, dl, x0 + 8, y0 + 48, FR9, INK, 10)
            assert dy <= y0 + 79, "card deck hits divider " + card["n"]
            d.line([x0 + 8, y0 + 81, x0 + col_w - 8, y0 + 81], fill=LINE)
            assert tw(card["stat"], FB9) <= col_w - 16, "card stat too wide " + card["n"]
            d.text((x0 + 8, y0 + 85), card["stat"], font=FB9, fill=RED)
    # ALSO 2 columns x 19/18 (37 items)
    d.text((M, 757), "ALSO IN THE NEWS \u2014 37 MORE STORIES", font=FB11, fill=NAVY)
    d.line([M, 772, W - M, 772], fill=RED, width=2)
    half = (len(ALSO) + 1) // 2
    for ci in range(2):
        x = M if ci == 0 else M + 512
        for ri in range(half):
            idx = ci * half + ri
            if idx >= len(ALSO):
                continue
            item = ALSO[idx]
            assert tw("\u2022 " + item, FR9) <= 488, "ALSO too wide: %r" % item
            d.text((x, 775 + ri * 10.0), "\u2022 " + item, font=FR9, fill=INK)
    # timeline: 2 rows
    row1 = "  \u2022  ".join(TIMELINE[:5])
    row2 = "  \u2022  ".join(TIMELINE[5:])
    assert tw(row1, FR9) <= CW and tw(row2, FR9) <= CW, "timeline too wide"
    d.text((M, 973), row1, font=FR9, fill=GREY)
    d.text((M, 985), row2, font=FR9, fill=GREY)
    # footer: legend + sources
    leg = ("[C] CONFIRMED  \u2022  [R] REPORTED  \u2022  [CL] CLAIM  \u2022  "
           "25 NOV = EVENT OF 25 NOV, REPORTED 26 NOV")
    src = ("SOURCES: REUTERS \u2022 AP \u2022 BBC \u2022 CNN \u2022 UKMTO \u2022 FCC \u2022 "
           "ONS \u2022 KCNA  \u2014  50 STORIES \u2022 THURSDAY 26 NOVEMBER 2026")
    assert tw(leg, FR9) <= CW and tw(src, FR8) <= CW, "footer too wide"
    d.text((M, 998), leg, font=FR9, fill=INK)
    d.text((M, 1011), src, font=FR8, fill=GREY)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    data = open(out, "rb").read()
    print("saved", out, len(data), "bytes",
          hashlib.sha256(data).hexdigest())
    assert len(data) <= 1048576, "entry.png over 1 MiB"
    assert img.size == (1024, 1024)
    print("ALL ASSERTS PASSED")


if __name__ == "__main__":
    main()
