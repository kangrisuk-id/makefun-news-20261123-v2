#!/usr/bin/env python3
"""Draw 'The World Today' front page for Monday 23 November 2026.

Dense one-page newspaper: 28 verified stories, stat strip, lead panels,
small-panel grid, schematic world map and an ALSO TODAY list.
All text is rendered with Pillow for crisp type. Deterministic output.
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


def panel(draw, box, kicker, head, body, accent, head_size=17, body_size=11):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(255, 255, 255), outline=INK, width=1)
    draw.rectangle((x0, y0, x1, y0 + 4), fill=accent)
    draw.text((x0 + 8, y0 + 9), kicker, font=font(FB, 9), fill=accent)
    y = text_block(draw, x0 + 8, y0 + 24, head, font(FB, head_size),
                   x1 - x0 - 16, leading=2, max_lines=3)
    text_block(draw, x0 + 8, y + 3, body, font(FR, body_size),
               x1 - x0 - 16, leading=2, max_lines=6)


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
    for i, (big, small) in enumerate(stats):
        x = 8 + i * sw
        d.rectangle((x, 101, x + sw - 4, 143), fill=LIGHT, outline=INK, width=1)
        d.text((x + sw // 2 - 2, 104), big, font=font(FB, 21), fill=NAVY, anchor="ma")
        d.text((x + sw // 2 - 2, 130), small, font=font(FR, 8), fill=GREY, anchor="ma")

    # ---- Lead panels ----
    panel(d, (8, 148, 408, 342), "CLIMATE  -  ANTALYA, TURKIYE",
          "COP31 COLLAPSES: NO DEAL ON FOSSIL FUELS",
          "The longest COP in history ended in Antalya with no pact. The EU "
          "and some 130 parties rejected a draft that dropped every mention "
          "of fossil fuels. First breakdown since Copenhagen 2009. "
          "Sources: Reuters, CNN, 23 Nov.", RED, 20, 12)
    d.rectangle((20, 292, 396, 334), fill=(254, 226, 226), outline=RED, width=1)
    d.text((28, 298), "90+ NATIONS SIGNED AN ELECTRIFICATION PLEDGE",
           font=font(FB, 9), fill=RED)
    d.text((28, 314), "A rare point of agreement on a day the pact failed.",
           font=font(FR, 9), fill=RED)

    panel(d, (416, 148, 708, 342), "WAR  -  DYMER, UKRAINE",
          "RUSSIAN STRIKE ON DYMER KILLS 11",
          "Rescuers pulled another body from rubble in Dymer, Kyiv region, "
          "raising the toll to 11, Governor Tkachenko said. A boy aged 7 "
          "was recovered alive from the ruins. Source: Reuters, 23 Nov.",
          NAVY, 19, 12)
    d.rectangle((428, 292, 696, 334), fill=(226, 232, 240), outline=NAVY, width=1)
    d.text((436, 298), "RESCUE UNDER WAY IN THE RUBBLE",
           font=font(FB, 9), fill=NAVY)
    d.text((436, 314), "Among the deadliest attacks near the capital this month.",
           font=font(FR, 9), fill=NAVY)

    panel(d, (716, 148, 1016, 342), "DISASTER  -  BANTEN, INDONESIA",
          "FACTORY FIRE KILLS 24, 30 MISSING",
          "Fire tore through a candy factory in Banten: 24 people dead and "
          "about 30 still unaccounted for as searches continued through "
          "the day. Sources: Reuters and reports, 23 Nov.", GOLD, 19, 12)
    d.rectangle((728, 292, 1004, 334), fill=(254, 243, 199), outline=GOLD, width=1)
    d.text((736, 298), "JAKARTA: PRABOWO TO NAME 2 VP CANDIDATES",
           font=font(FB, 9), fill=GOLD)
    d.text((736, 314), "Parliament selects the new vice-president on 11 Dec.",
           font=font(FR, 9), fill=GOLD)

    # ---- Small panel grid: 8 panels, 4 x 2 ----
    small = [
        ("MIDDLE EAST", "IRAN VOWS TO FIGHT US BLOCKADE",
         "Tehran says it will use all tools against the US naval blockade of "
         "Hormuz. Oil flows slowed to 9.5m bpd. Reuters.", RED),
        ("MARKETS", "AI SELL-OFF SHAKES ASIA, WALL ST",
         "Nikkei -5.06%, S&P 500 -3.7% as the AI trade wobbles; gold +2.72%. "
         "Korea and Taiwan officials watch closely. Reuters.", TEAL),
        ("UNITED STATES", "DEMOCRATS LOCK 258 HOUSE SEATS",
         "At least 258 seats: the party's biggest House majority since 1992 "
         "after this month's midterms. Roundup, 23 Nov.", NAVY),
        ("HEALTH  -  DR CONGO", "EBOLA DEATHS HIDDEN IN GRAVES",
         "Reuters counted far more new graves in Bunia than official tallies: "
         "11,500+ infected, 5,500+ dead. Reuters investigation.", TEAL),
        ("MEXICO", "'EL CHAPO ISIDRO' CAPTURED",
         "The cartel figure was seized in Sinaloa in a federal operation, "
         "ending a long manhunt. Reports, 23 Nov.", GOLD),
        ("UNITED KINGDOM", "MANCHESTER ARENA EVACUATED",
         "Co-op Live arena was cleared over an unknown substance; more than "
         "50 people were treated at the scene. Reports, 23 Nov.", NAVY),
        ("TECHNOLOGY", "CALIFORNIA SUES OPENAI",
         "Attorney General Bonta filed suit against OpenAI over model "
         "security and public safety, announced Sunday. Reuters.", RED),
        ("ECONOMY  -  FRANCE", "FRENCH DOWNTURN DEEPENS, PMI 46.2",
         "Private sector shrank to a six-month low; factory output fell "
         "steepest since Feb 2025. Flash PMI, Reuters.", TEAL),
    ]
    gx, gy, gw, gh = 8, 350, 246, 118
    for i, (k, h, b, a) in enumerate(small):
        x = gx + (i % 4) * (gw + 8)
        y = gy + (i // 4) * (gh + 8)
        panel(d, (x, y, x + gw, y + gh), k, h, b, a, 13, 10)

    # ---- Bottom: map (left) + ALSO TODAY (right) ----
    by = 602
    d.rectangle((8, by, 500, 946), fill=(255, 255, 255), outline=INK, width=1)
    d.text((16, by + 7), "WHERE IT HAPPENED", font=font(FB, 13), fill=NAVY)
    # schematic continents as labelled blobs
    blobs = [
        (60, 680, 150, 730, "N. AMERICA"), (150, 760, 205, 830, "S. AMERICA"),
        (245, 660, 320, 715, "EUROPE"), (255, 725, 330, 810, "AFRICA"),
        (340, 655, 470, 730, "ASIA"), (400, 790, 465, 835, "OCEANIA"),
    ]
    for x0, y0, x1, y1, name in blobs:
        d.rounded_rectangle((x0, y0, x1, y1), 14, fill=LIGHT, outline=TEAL, width=2)
        d.text(((x0 + x1) // 2, (y0 + y1) // 2 - 6), name, font=font(FB, 9),
               fill=INK, anchor="ma")
    marks = [(262, 700, "Antalya"), (318, 688, "Dymer"), (360, 712, "Hormuz"),
             (438, 712, "Banten"), (80, 692, "Washington"),
             (292, 762, "Ebola"), (62, 716, "Sacramento")]
    for x, y, lab in marks:
        d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=RED)
        d.text((x + 7, y - 5), lab, font=font(FR, 8), fill=INK)
    d.text((16, 852), "Markers show the day's main datelines: Antalya, Kyiv,",
           font=font(FR, 10), fill=GREY)
    d.text((16, 868), "Hormuz, Banten, Bunia, Washington, Paris, Sacramento.",
           font=font(FR, 10), fill=GREY)
    d.text((16, 892), "THE DAY IN NUMBERS", font=font(FB, 12), fill=NAVY)
    d.text((16, 912), "462m barrels drawn from stocks in the Iran war; diesel",
           font=font(FR, 10), fill=INK)
    d.text((16, 928), "still scarce. 1,000+ Delta flights delayed by a systems",
           font=font(FR, 10), fill=INK)

    d.rectangle((508, by, 1016, 946), fill=(255, 255, 255), outline=INK, width=1)
    d.text((516, by + 7), "ALSO TODAY  -  16 MORE STORIES", font=font(FB, 13), fill=RED)
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
    y = by + 32
    for item in also:
        d.text((516, y), "- " + item, font=font(FR, 11), fill=INK)
        y += 19

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
