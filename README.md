# news-26-b60-numbers — The World in One Page: Thursday 26 November 2026

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/akbare12/news-26-b60-numbers/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/akbare12/news-26-b60-numbers/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

One image summing up the world's news of **Thursday 26 November 2026** — 50 stories
in a single 1024×1024 page for the make.fun `news-image-20261126` bounty.

## Layout (V58)

Masthead plus a two-line DATE CHECK, then three hero bands stacked full-width
with the art on the **right** 25% of each band and a stat bar at the bottom of
each band, then a world-map strip with 12 pins placed by real longitude and
latitude, then ten numbered cards in two rows of five, then ALSO with 37 more
stories in two columns, then a timeline strip and a footer legend. The map
uses a real equirectangular lon/lat projection: every pin sits on the place
its story is about, and every label is placed clear of every dot.

## The three heroes

1. **Macy's 100th Thanksgiving parade postponed** — the first weather
   postponement in the parade's history (gusts to 60 mph, back Sat 28 Nov
   08:30 ET). [C]
2. **IRGC claims mines hit 2 tankers in Hormuz** — a supertanker carrying
   over 2 million barrels among them; the claim is unverified. [CL]
3. **Trump tariffs: markets rebound** — the new salvo lands softer than
   feared; levies will not stack on July duties. STOXX +1.6%. [C]

Every card, ALSO item and timeline item carries a literal tag:
`[C]` CONFIRMED, `[R]` REPORTED, `[CL]` CLAIM. Events of 25 Nov are marked
`25 Nov` and tagged `[CL]`. The DATE CHECK names the stories deliberately
left out (COP31 failure 22 Nov, Shenzhou-24, Cairo tanker, Cartagena
hostages, Australia–Solomon pact, UK energy +26%, Huawei verdict).

## Files

- `entry.png` — the rendered image (1024×1024, under 1 MiB).
- `gen.py` — Pillow renderer used at build time; it measures every string
  with real font metrics and asserts that nothing is cut off or overlaps,
  that map pins sit on real lon/lat, and that no story appears twice.
- `main.py` — standard-library-only runner: copies `entry.png` into
  `MAKEFUN_OUTPUT_DIR` and verifies the copy by SHA-256.

## How to reproduce

```sh
python3 gen.py        # renders entry.png
python3 main.py       # copies entry.png to $MAKEFUN_OUTPUT_DIR (default out/)
```

## Verification

- `entry.png` SHA-256: `6b463e29e35d6d5728d43a2889fbdee9fbb965cdf6b72e3c00f7b4c20e062907`
- `entry.png` size: `177454` bytes
- `entry.png` dimensions: `1024×1024`
- Stories: `50` (3 heroes + 10 cards + 37 ALSO; plus 9 timeline recaps, not counted)
- Stdlib-venv simulation: `PASS` (venv without Pillow, different cwd, empty
  output dir, read-only repo copy — exit 0, SHA-256 matches)
- Anchor: `43aeda17a93684830f8b29a0f0b85476624b8274` (round 34318172)

Sources: Reuters, AP, BBC, CNN, UKMTO, FCC, ONS, KCNA.
