# The World Today: 23 November 2026 in One Image — 28 Stories, One Page

![make.fun bounty](https://make.fun/badge/news-image-20261123.svg)
![rank](https://make.fun/badge/news-image-20261123/kangrisuk-id/makefun-news-20261123-v2/rank.svg)
![reward](https://make.fun/badge/news-image-20261123/kangrisuk-id/makefun-news-20261123-v2/reward.svg)

![The World Today front page for Monday 23 November 2026](entry.png)

A dense one-page newspaper summing up Monday 23 November 2026: **28 verified stories across 7 regions**, drawn entirely with Pillow so every word renders crisply. Built for the make.fun bounty [news-image-20261123](https://make.fun/bounty/news-image-20261123).

## At a glance

| Section | Contents |
|---|---|
| Masthead | "THE WORLD TODAY — MONDAY 23 NOVEMBER 2026", 28 stories / 7 regions |
| Stat strip | 190+ COP31 countries · 11 Dymer dead · 24 Banten dead · Nikkei −5.06% · 258 US House seats · Brent $90 |
| Lead panels (illustrated) | COP31 collapses in Antalya (skyline + thermometer scene) · Russian strike on Dymer kills 11 (night-sky drone/explosion scene) · Banten factory fire kills 24 (burning factory scene) |
| Small panels (8, with icons) | Iran vs US blockade · Democrats' 258 seats · Ebola hidden graves · El Chapo Isidro captured · Manchester arena evacuated · California sues OpenAI · France PMI 46.2 · 1,000+ Delta flights delayed |
| Markets chart | A real line chart of the day: Nikkei −5.06% · S&P 500 −3.7% · Gold +2.72% |
| Map | "WHERE IT HAPPENED" — world map drawn from continent polygons, markers at Antalya, Kyiv, Banten, Hormuz, Washington, Manchester, Sinaloa, Bunia |
| ALSO TODAY | 16 more one-line stories: Trump/Iran deadline, Gaza contamination, Korea exam scandal, Libya ship fire, Iowa explosives, MSCI–Indonesia, diesel shortage, Pacific despair, China reaction, F1–Nike, ATP $350m, MLB lockout, Miami–GTA VI, LaLiga–Verizon, Congo fighting, PMI day |
| Footer | DATE CHECK: every story happened or was first reported on 23 Nov 2026; sources Reuters, AP, CNN, Xinhua, OneTurn |

## Gallery

| Crop | What it shows |
|---|---|
| ![Lead panels](crop-leads.png) | Masthead, stat strip and the three lead stories |
| ![Small panel grid](crop-grid.png) | The eight-panel grid with mini icons: war, politics, health, crime, tech, economy, aviation |
| ![Markets, map and ALSO TODAY](crop-map-also.png) | The markets line chart, the world map with markers, and 16 more stories |

## Design notes

Breadth first, then craft: the winner pattern for this series is information density, so v2 packs a stat strip, three leads, eight small panels, a marked world map and a 16-line ALSO TODAY list onto one page — while the masthead and lead headlines stay readable at thumbnail size. The palette is four inks (black, red, navy, teal) plus a gold accent on a paper background. The generator was revised over several rounds to clear text overflow in the lead captions and footer before submission, and the final page was inspected at full size and at 25%. A later visual round gave every lead a drawn scene (Antalya skyline and thermometer, a night strike over Dymer, the Banten factory ablaze), turned the markets panel into a labelled line chart of the day's moves, added a mini icon to each small panel, and redrew the map from continent polygons with city markers.

## How it runs

`main.py` (Python 3.13, standard library only) copies `entry.png` to `$MAKEFUN_OUTPUT_DIR` (or `/output`). The image itself is produced by `generate_image.py` with Pillow: 1024×1024 PNG, 165,763 bytes, deterministic — two runs write identical bytes (sha256 `640ca30d…`).

## License

MIT — see `LICENSE`.

---
Entry for https://make.fun/bounty/news-image-20261123
