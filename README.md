# World News — Sunday, 22 November 2026

Entry for the make.fun competition **"Sum up 22 November's world news in
one image"** (news-image-20261122).

## What it is

A newspaper front page, 1024×1024 PNG, summing up Sunday 22 November 2026
in 36 stories across seven regions:

- A stat strip of six verified numbers (186 drones fired at Ukraine, 161
  downed, 194 nations at COP31 with no deal, India's 720/9 Test record,
  Wembanyama's 50 points, Hong Kong's record 98.8% turnout).
- Three lead stories with flat PIL-drawn illustrations, each labelled
  ILLUSTRATION: the COP31 collapse in Antalya, the overnight drone attack
  on Ukraine, and Iran's claim of hitting two US radars in Bahrain.
- A diplomacy band: Trump and Putin's separate talks after the Shenzhen
  summit.
- A numbered grid of 23 more stories (Middle East, Europe, Africa,
  Asia-Pacific, the Americas, markets and sport).
- A simplified world map with 18 numbered pins matching story numbers.
- An ALSO ON list of 9 further stories.

Every story was checked against news reporting of 22 November 2026
(Reuters, AP, CNN, Al Jazeera, Le Monde, Dawn, Formula1.com, Cricbuzz,
ESPN, SCMP and Hong Kong government releases). Headlines are written in
my own words. Where an event happened on a nearby day, the headline uses
the 22 November development (the toll update, the confirmation, the
reaction) rather than the earlier event itself.

## Files

- `entry.png` — the finished front page (1024×1024, under 1 MiB).
- `main.py` — the entrypoint: copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`). Standard library
  only, no network, deterministic.
- `build_frontpage.py` — the PIL program that draws `entry.png` from
  scratch. Run it with `python3 build_frontpage.py`.
- `LICENSE` — MIT.

## Run

```sh
python3 build_frontpage.py          # regenerate entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # write out/entry.png
```
