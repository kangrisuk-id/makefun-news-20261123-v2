#!/usr/bin/env python3
"""Draw 'The World Today' front page for Monday 23 November 2026, v2 visual.

A living picture newspaper: 28 verified stories with drawn scenes in the
lead panels (Antalya skyline + thermometer, night strike over Dymer,
burning factory in Banten), a real line chart for the markets panel,
mini icons in the small panels, and a recognisable world map drawn from
coarse continent polygons. All rendered with Pillow. Deterministic.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (247, 243, 232)
INK = (17, 17, 17)
RED = (185, 28, 28)
TEAL = (15, 118, 110)
NAVY = (30, 58, 95)
GOLD = (180, 83, 9)
LIGHT = (238, 232, 214)
GREY = (90, 90, 90)
SKY_D = (23, 32, 56)
SKY_C = (186, 224, 235)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, maxw, fill=INK, leading=3, max_lines=99):
    for line in wrap(draw, text, fnt, maxw)[:max_lines]:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


# ---------- lead scenes (band is 64 px tall: keep every mark inside) ----------
def scene_cop(d, x0, y0, x1, y1):
    d.rectangle((x0, y0, x1, y1), fill=SKY_C)
    d.ellipse((x1 - 52, y0 + 6, x1 - 14, y0 + 44), fill=(250, 204, 21))  # sun
    for bx, bw, bh in [(6, 34, 30), (46, 26, 44), (78, 40, 24), (124, 28, 52),
                       (158, 36, 34), (200, 26, 46), (232, 40, 28)]:
        d.rectangle((x0 + bx, y1 - bh, x0 + bx + bw, y1), fill=NAVY)
    d.rectangle((x0, y1 - 4, x1, y1), fill=TEAL)
    tx = x0 + 12
    d.rounded_rectangle((tx, y0 + 8, tx + 10, y1 - 16), 5, fill=(255, 255, 255), outline=RED, width=2)
    d.rectangle((tx + 3, y0 + 24, tx + 7, y1 - 18), fill=RED)
    d.ellipse((tx - 3, y1 - 24, tx + 13, y1 - 8), fill=RED)
    d.rounded_rectangle((tx + 18, y0 + 6, tx + 128, y0 + 22), 3, fill=(255, 255, 255))
    d.text((tx + 22, y0 + 9), "+1.5C OVERSHOOT", font=font(FB, 10), fill=RED)


def scene_dymer(d, x0, y0, x1, y1):
    d.rectangle((x0, y0, x1, y1), fill=SKY_D)
    for sx, sy in [(30, 14), (90, 8), (150, 20), (230, 10), (300, 16), (60, 30), (200, 30)]:
        d.ellipse((x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3), fill=(255, 255, 255))
    dx, dy = x0 + 210, y0 + 18
    d.line((dx - 22, dy, dx + 22, dy), fill=(248, 113, 113), width=3)
    d.line((dx, dy - 8, dx, dy + 8), fill=(248, 113, 113), width=3)
    d.ellipse((dx - 5, dy - 5, dx + 5, dy + 5), fill=(248, 113, 113))
    ex, ey = x0 + 88, y1 - 30
    for r, c in [(24, (249, 115, 22)), (15, (250, 204, 21)), (8, (254, 240, 138))]:
        d.ellipse((ex - r, ey - r, ex + r, ey + r), fill=c)
    d.rectangle((x0 + 8, y1 - 38, x0 + 52, y1), fill=(71, 85, 105))
    d.polygon([(x0 + 130, y1), (x0 + 176, y1 - 28), (x0 + 222, y1)], fill=(71, 85, 105))
    d.polygon([(x0 + 216, y1), (x0 + 262, y1 - 16), (x0 + 300, y1)], fill=(100, 116, 139))
    d.line((x0, y1 - 1, x1, y1 - 1), fill=(15, 23, 42), width=2)


def scene_banten(d, x0, y0, x1, y1):
    d.rectangle((x0, y0, x1, y1), fill=(254, 243, 199))
    d.rectangle((x0 + 20, y1 - 36, x1 - 60, y1), fill=(68, 64, 60))
    d.polygon([(x0 + 20, y1 - 36), (x0 + 70, y1 - 50), (x1 - 110, y1 - 50), (x1 - 60, y1 - 36)],
              fill=(68, 64, 60))
    d.rectangle((x1 - 96, y1 - 60, x1 - 80, y1 - 32), fill=(68, 64, 60))  # chimney
    for fx in range(x0 + 40, x1 - 84, 26):
        hgt = 12 + (fx * 7) % 9
        d.polygon([(fx, y1 - 34), (fx + 9, y1 - 34 - hgt), (fx + 18, y1 - 34)], fill=(234, 88, 12))
        d.polygon([(fx + 5, y1 - 34), (fx + 9, y1 - 34 - hgt + 6), (fx + 13, y1 - 34)],
                  fill=(250, 204, 21))
    for cx, cy, r in [(x1 - 88, y0 + 12, 7), (x1 - 72, y0 + 8, 9), (x1 - 54, y0 + 11, 6)]:
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(168, 162, 158))
    d.rounded_rectangle((x0 + 8, y0 + 5, x0 + 128, y0 + 21), 3, fill=(254, 243, 199))
    d.text((x0 + 12, y0 + 8), "FACTORY ABLAZE", font=font(FB, 10), fill=(154, 52, 18))


# ---------- small icons (26x26 at given origin) ----------
def icon(d, kind, x, y, col):
    if kind == "ship":
        d.polygon([(x, y + 16), (x + 26, y + 16), (x + 21, y + 24), (x + 5, y + 24)], fill=col)
        d.line((x + 13, y + 3, x + 13, y + 16), fill=col, width=2)
        d.polygon([(x + 13, y + 3), (x + 22, y + 12), (x + 13, y + 12)], outline=col)
    elif kind == "vote":
        d.rectangle((x + 3, y + 12, x + 23, y + 25), outline=col, width=2)
        d.line((x + 8, y + 12, x + 18, y + 12), fill=col, width=3)
        d.line((x + 7, y + 5, x + 11, y + 9), fill=col, width=2)
        d.line((x + 11, y + 9, x + 20, y + 1), fill=col, width=2)
    elif kind == "cross":
        d.rectangle((x + 9, y + 2, x + 17, y + 24), fill=col)
        d.rectangle((x + 2, y + 9, x + 24, y + 17), fill=col)
    elif kind == "badge":
        d.ellipse((x + 3, y + 3, x + 23, y + 23), outline=col, width=2)
        d.polygon([(x + 13, y + 7), (x + 15, y + 12), (x + 20, y + 12), (x + 16, y + 15),
                   (x + 17, y + 20), (x + 13, y + 17), (x + 9, y + 20), (x + 10, y + 15),
                   (x + 6, y + 12), (x + 11, y + 12)], fill=col)
    elif kind == "arena":
        d.arc((x + 1, y + 4, x + 25, y + 28), 180, 360, fill=col, width=2)
        d.line((x + 1, y + 16, x + 25, y + 16), fill=col, width=2)
        d.ellipse((x + 10, y + 8, x + 16, y + 14), fill=col)
    elif kind == "chip":
        d.rectangle((x + 6, y + 6, x + 20, y + 20), outline=col, width=2)
        for i in range(3):
            d.line((x + 2, y + 9 + i * 4, x + 6, y + 9 + i * 4), fill=col, width=2)
            d.line((x + 20, y + 9 + i * 4, x + 24, y + 9 + i * 4), fill=col, width=2)
    elif kind == "down":
        d.line((x + 3, y + 6, x + 10, y + 12), fill=col, width=2)
        d.line((x + 10, y + 12, x + 15, y + 8), fill=col, width=2)
        d.line((x + 15, y + 8, x + 23, y + 19), fill=col, width=2)
        d.polygon([(x + 18, y + 19), (x + 24, y + 20), (x + 22, y + 14)], fill=col)
    elif kind == "plane":
        d.line((x + 2, y + 15, x + 24, y + 15), fill=col, width=3)
        d.polygon([(x + 20, y + 15), (x + 26, y + 11), (x + 26, y + 19)], fill=col)
        d.polygon([(x + 10, y + 14), (x + 16, y + 5), (x + 19, y + 5), (x + 16, y + 14)], fill=col)
        d.polygon([(x + 10, y + 16), (x + 16, y + 24), (x + 19, y + 24), (x + 16, y + 16)], fill=col)


def lead(d, box, kicker, head, body, accent, scene):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(255, 255, 255), outline=INK, width=1)
    d.rectangle((x0, y0, x1, y0 + 4), fill=accent)
    d.text((x0 + 8, y0 + 9), kicker, font=font(FB, 9), fill=accent)
    y = text_block(d, x0 + 8, y0 + 24, head, font(FB, 19), x1 - x0 - 16, leading=2, max_lines=3)
    scene(d, x0 + 8, y + 4, x1 - 8, y + 68)
    text_block(d, x0 + 8, y + 76, body, font(FR, 11), x1 - x0 - 16, leading=2, max_lines=4)


def small(d, box, kicker, head, body, accent, ic):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(255, 255, 255), outline=INK, width=1)
    d.rectangle((x0, y0, x1, y0 + 4), fill=accent)
    d.text((x0 + 8, y0 + 9), kicker, font=font(FB, 9), fill=accent)
    if ic:
        icon(d, ic, x1 - 36, y0 + 10, accent)
    hw = x1 - x0 - 52 if ic else x1 - x0 - 16
    y = text_block(d, x0 + 8, y0 + 24, head, font(FB, 13), hw, leading=2, max_lines=3)
    text_block(d, x0 + 8, y + 3, body, font(FR, 10), x1 - x0 - 16, leading=2, max_lines=5)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.text((512, 6), "THE WORLD TODAY", font=font(FS, 54), fill=INK, anchor="ma")
    d.line((8, 68, 1016, 68), fill=INK, width=3)
    d.text((8, 73), "MONDAY 23 NOVEMBER 2026", font=font(FB, 17), fill=RED)
    d.text((1016, 73), "28 STORIES  -  7 REGIONS  -  ONE PAGE",
           font=font(FB, 13), fill=INK, anchor="ra")
    d.line((8, 96, 1016, 96), fill=INK, width=1)

    # ---- Stat strip ----
    stats = [("190+", "COP31 countries, no deal"), ("11", "killed in Dymer strike"),
             ("24", "dead in Banten fire"), ("-5.06%", "Nikkei in AI sell-off"),
             ("258", "US House seats, Democrats"), ("$90", "Brent crude, Hormuz risk")]
    sw = (1016 - 8) // 6
    for i, (big, small_) in enumerate(stats):
        x = 8 + i * sw
        d.rectangle((x, 101, x + sw - 4, 143), fill=LIGHT, outline=INK, width=1)
        d.text((x + sw // 2 - 2, 104), big, font=font(FB, 21), fill=NAVY, anchor="ma")
        d.text((x + sw // 2 - 2, 130), small_, font=font(FR, 8), fill=GREY, anchor="ma")

    # ---- Leads with scenes ----
    lead(d, (8, 148, 408, 356), "CLIMATE  -  ANTALYA, TURKIYE",
         "COP31 COLLAPSES: NO DEAL ON FOSSIL FUELS",
         "The longest COP in history ended with no pact. The EU and some 130 "
         "parties rejected a draft that dropped every mention of fossil fuels. "
         "First breakdown since Copenhagen 2009. Reuters, CNN.", RED, scene_cop)
    lead(d, (416, 148, 708, 356), "WAR  -  DYMER, UKRAINE",
         "RUSSIAN STRIKE ON DYMER KILLS 11",
         "Rescuers pulled another body from rubble in Dymer, Kyiv region, "
         "raising the toll to 11, Governor Tkachenko said. A boy aged 7 was "
         "recovered alive. Reuters, 23 Nov.", NAVY, scene_dymer)
    lead(d, (716, 148, 1016, 356), "DISASTER  -  BANTEN, INDONESIA",
         "FACTORY FIRE KILLS 24, 30 MISSING",
         "Fire tore through a candy factory in Banten: 24 dead, about 30 "
         "still unaccounted for. In Jakarta, Prabowo will name two VP "
         "candidates; parliament votes 11 Dec. Reuters.", GOLD, scene_banten)

    # ---- Small grid ----
    gx, gy, gw, gh = 8, 364, 246, 122
    cells = [
        ("MIDDLE EAST", "IRAN VOWS TO FIGHT US BLOCKADE",
         "Tehran says it will use all tools against the US naval blockade of "
         "Hormuz. Oil flows slowed to 9.5m bpd. Reuters.", RED, "ship"),
        ("UNITED STATES", "DEMOCRATS LOCK 258 HOUSE SEATS",
         "At least 258 seats: the party's biggest House majority since 1992 "
         "after this month's midterms. Roundup, 23 Nov.", NAVY, "vote"),
        ("HEALTH  -  DR CONGO", "EBOLA DEATHS HIDDEN IN GRAVES",
         "Reuters counted far more new graves in Bunia than official tallies: "
         "11,500+ infected, 5,500+ dead. Investigation.", TEAL, "cross"),
        ("MEXICO", "'EL CHAPO ISIDRO' CAPTURED",
         "The cartel figure was seized in Sinaloa in a federal operation, "
         "ending a long manhunt. Reports, 23 Nov.", GOLD, "badge"),
        ("UNITED KINGDOM", "MANCHESTER ARENA EVACUATED",
         "Co-op Live arena was cleared over an unknown substance; more than "
         "50 people were treated. Reports, 23 Nov.", NAVY, "arena"),
        ("TECHNOLOGY", "CALIFORNIA SUES OPENAI",
         "Attorney General Bonta filed suit against OpenAI over model "
         "security and public safety. Reuters, 23 Nov.", RED, "chip"),
        ("ECONOMY  -  FRANCE", "FRENCH DOWNTURN DEEPENS",
         "Private sector shrank to a six-month low, PMI 46.2; factory output "
         "fell steepest since Feb 2025. Flash PMI, Reuters.", TEAL, "down"),
        ("US AVIATION", "1,000+ DELTA FLIGHTS DELAYED",
         "An automated systems failure delayed more than 1,000 Delta flights "
         "across the United States on Monday. Roundup, 23 Nov.", NAVY, "plane"),
    ]
    for i, (k, h, b, a, ic) in enumerate(cells):
        x = gx + (i % 4) * (gw + 8)
        y = gy + (i // 4) * (gh + 8)
        small(d, (x, y, x + gw, y + gh), k, h, b, a, ic)

    # ---- Markets chart panel (left, upper bottom) ----
    my = 622
    d.rectangle((8, my, 500, 792), fill=(255, 255, 255), outline=INK, width=1)
    d.rectangle((8, my, 500, my + 4), fill=TEAL)
    d.text((16, my + 9), "MARKETS  -  THE AI SELL-OFF IN ONE CHART", font=font(FB, 12), fill=TEAL)
    d.text((16, my + 30), "Index moves reported Monday 23 Nov (session path, schematic)",
           font=font(FR, 9), fill=GREY)
    cx0, cy0, cx1, cy1 = 30, my + 52, 478, my + 128
    d.rectangle((cx0, cy0, cx1, cy1), outline=GREY, width=1)
    for f in (0.25, 0.5, 0.75):
        yy = cy0 + (cy1 - cy0) * f
        d.line((cx0, yy, cx1, yy), fill=(210, 210, 210), width=1)
    zero = cy0 + 34
    d.line((cx0, zero, cx1, zero), fill=INK, width=1)
    series = [
        ("NIKKEI -5.06%", RED, [0, -1.2, -0.8, -2.4, -3.1, -2.6, -4.2, -5.06], 6),
        ("S&P 500 -3.7%", NAVY, [0, -0.7, -1.4, -1.1, -2.2, -2.9, -2.5, -3.7], -17),
        ("GOLD +2.72%", GOLD, [0, 0.5, 0.3, 1.1, 0.9, 1.8, 2.2, 2.72], -16),
    ]
    for name, col, vals, loff in series:
        pts = []
        for i, v in enumerate(vals):
            px = cx0 + 14 + i * (cx1 - cx0 - 28) / (len(vals) - 1)
            py = zero - v * 7
            pts.append((px, py))
        d.line(pts, fill=col, width=3)
        d.text((pts[-1][0] - 4, pts[-1][1] + loff), name, font=font(FB, 10), fill=col, anchor="ra")
    d.text((16, cy1 + 10), "Tech rout from Tokyo to Wall Street as the AI trade wobbles;",
           font=font(FR, 10), fill=INK)
    d.text((16, cy1 + 26), "gold climbs as investors run for safety. PCE data due Wed.",
           font=font(FR, 10), fill=INK)

    # ---- World map panel (left, lower bottom) ----
    mx0, my0, mx1, my1 = 8, 798, 500, 946
    d.rectangle((mx0, my0, mx1, my1), fill=(239, 246, 250), outline=TEAL, width=1)
    d.text((mx0 + 8, my0 + 6), "WHERE IT HAPPENED", font=font(FB, 11), fill=NAVY)

    def proj(lon, lat):
        return (mx0 + 12 + (lon + 168) / 348 * (mx1 - mx0 - 24),
                my0 + 26 + (82 - lat) / 140 * (my1 - my0 - 36))

    continents = [
        [(-165, 68), (-140, 72), (-125, 72), (-110, 68), (-95, 80), (-85, 70),
         (-80, 62), (-78, 58), (-85, 50), (-90, 48), (-88, 42), (-92, 35),
         (-97, 28), (-97, 22), (-105, 20), (-110, 24), (-117, 33), (-124, 40),
         (-124, 48), (-132, 56), (-152, 60), (-165, 60)],
        [(-78, 8), (-70, 11), (-62, 9), (-52, 5), (-50, 0), (-44, -3), (-35, -8),
         (-39, -14), (-40, -22), (-48, -27), (-55, -33), (-62, -39), (-65, -45),
         (-67, -52), (-71, -50), (-73, -40), (-73, -28), (-70, -18), (-75, -12),
         (-79, -5), (-80, 1)],
        [(-9, 43), (-2, 44), (0, 46), (-5, 48), (-2, 50), (2, 51), (5, 53),
         (8, 55), (8, 57), (12, 56), (18, 56), (21, 55), (24, 58), (28, 60),
         (30, 62), (28, 66), (32, 70), (20, 70), (12, 66), (5, 62), (5, 59),
         (0, 52), (-4, 44), (-9, 44)],
        [(-17, 15), (-10, 5), (0, 6), (6, 4), (9, 4), (13, -1), (12, -6),
         (13, -12), (15, -22), (17, -32), (19, -34), (26, -34), (31, -29),
         (35, -24), (36, -18), (40, -12), (40, -6), (42, -1), (48, 5), (51, 10),
         (44, 11), (40, 15), (38, 18), (34, 22), (32, 26), (30, 30), (20, 32),
         (11, 34), (0, 36), (-6, 35), (-10, 31), (-15, 25), (-17, 20)],
        [(30, 36), (36, 36), (42, 38), (48, 38), (54, 40), (60, 42), (70, 45),
         (80, 48), (90, 50), (100, 52), (110, 52), (120, 53), (130, 50),
         (140, 48), (142, 42), (140, 38), (135, 35), (130, 33), (127, 38),
         (122, 31), (120, 25), (115, 23), (108, 18), (106, 9), (103, 5),
         (100, 8), (98, 13), (95, 16), (92, 20), (88, 22), (80, 15), (77, 8),
         (73, 18), (68, 23), (61, 25), (57, 26), (52, 28), (50, 30), (48, 30),
         (44, 29), (42, 33), (36, 33), (30, 34)],
        [(113, -22), (114, -30), (118, -35), (124, -33), (130, -32), (135, -35),
         (138, -36), (142, -38), (146, -39), (150, -37), (153, -30), (153, -25),
         (150, -22), (146, -19), (143, -15), (142, -11), (136, -12), (132, -11),
         (128, -14), (124, -16), (119, -18), (114, -21)],
        [(95, 5), (100, 2), (104, -2), (107, -5), (110, -7), (112, -8), (108, -8),
         (104, -6), (100, -3), (96, 2)],
    ]
    for poly in continents:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=(209, 232, 220), outline=TEAL)
    marks = [(30, 39, "Antalya", 6, 2), (31, 50, "Kyiv", 6, -6),
             (106, -6, "Banten", -42, 2), (56, 26, "Hormuz", 6, -2),
             (-77, 39, "Washington", -62, -6), (-2, 53, "Manchester", -56, -12),
             (-107, 25, "Sinaloa", 6, -4), (30, 1, "Bunia", 6, 0)]
    for lon, lat, lab, ox, oy in marks:
        px, py = proj(lon, lat)
        d.ellipse((px - 3, py - 3, px + 3, py + 3), fill=RED)
        d.text((px + ox, py + oy), lab, font=font(FB, 8), fill=INK)

    # ---- ALSO TODAY (right, full height) ----
    d.rectangle((508, 622, 1016, 946), fill=(255, 255, 255), outline=INK, width=1)
    d.rectangle((508, 622, 1016, 626), fill=RED)
    d.text((516, 633), "ALSO TODAY  -  16 MORE STORIES", font=font(FB, 13), fill=RED)
    also = [
        "TRUMP sets New Year deadline for Iran, warns of strikes",
        "GAZA experts warn of toxic contamination across the strip",
        "S. KOREA education minister quits over exam-cheating scandal",
        "LIBYA Russian ship ablaze at port after suspected drone hit",
        "IOWA US Army to detonate unstable explosives despite court order",
        "INDONESIA MSCI in talks to avert two-step market downgrade",
        "OIL diesel shortage hides behind crude's swift recovery",
        "PACIFIC nations voice despair after COP31 flop; Australia row",
        "CHINA delegation 'disappointed' by COP31 no-deal outcome",
        "SPORT F1 signs Nike kit deal across F1 and F1 Academy",
        "TENNIS ATP approves $350m player compensation plan",
        "BASEBALL MLB owners refuse salary-cap deal; lockout looms",
        "MIAMI Heat plan $3.9m Grand Theft Auto VI launch takeover",
        "FOOTBALL LaLiga renews Verizon deal; Clasico drew 2.4m in US",
        "CONGO fighting near Ebola zone disrupts medical work",
        "EUROPE flash PMIs and NY Fed's Williams set the market day",
    ]
    y = 662
    for item in also:
        d.text((516, y), "- " + item, font=font(FR, 11), fill=INK)
        y += 18

    # ---- Footer / date check ----
    d.line((8, 952, 1016, 952), fill=INK, width=2)
    d.text((8, 958),
           "DATE CHECK: Every story above happened or was first reported on Monday 23 November 2026.",
           font=font(FB, 11), fill=INK)
    d.text((8, 978),
           "Sources: Reuters, AP, CNN, Xinhua and OneTurn roundup, all dated 23 Nov 2026. No earlier-day",
           font=font(FR, 10), fill=GREY)
    d.text((8, 994),
           "news is presented as today's. Figures are as reported that day.  -  THE WORLD TODAY, one page.",
           font=font(FR, 10), fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
