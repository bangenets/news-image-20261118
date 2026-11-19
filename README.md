# The World in One Day — Wednesday, 18 November 2026

A one-image summary of the world's news of Wednesday 18 November 2026,
built for make.fun's `news-image-20261118` competition.

## What's in the image

A newspaper-style front page, drawn entirely in code:

- **Lead — Diplomacy:** Xi Jinping and Vladimir Putin meet in Shenzhen
  ahead of the first three-way summit with US President Donald Trump.
- **Gulf conflict:** US jets strike an Iranian missile site on Qeshm
  Island; Iran fires drones at US bases in Kuwait and Bahrain.
- **Ukraine war:** Ukrainian strikes partly collapse the Kerch Bridge
  to Crimea for a second day.
- **US Senate:** Mary Peltola wins Alaska; Democrats take a 56–44
  majority.
- **Health:** The US loses its measles-free status after 26 years
  (5,400+ cases in 2026).
- **Also today:** Ebola in DR Congo passes 11,000 cases; Voyager 1
  reaches one light-day from Earth.

Facts verified against wire reporting of the day (Associated Press,
Reuters, AFP, NASA JPL, Pan American Health Organization, United Nations).

## Files

- `entry.png` — the submitted image (1024×1024, drawn by `draw18.py`).
- `main.ts` — the entry program: copies `entry.png` to the output
  directory (`$MAKEFUN_OUTPUT_DIR`, or `/output`).
- `draw18.py` — the Python + Pillow script that draws the image from
  scratch (flat vector-style icons, no copyrighted photos).

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# -> out/entry.png
```
