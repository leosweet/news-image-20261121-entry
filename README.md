# 21 November 2026 — The World in One Picture

One image summing up the world's news of Saturday 21 November 2026:

- Russia's biggest strike on Ukraine yet — 400+ drones and 110 missiles, 8 killed, Kyiv's bridges hit, power cut nationwide; missiles land in Poland. A double-tap strike on Kryvyi Rih kills 2 and wounds 60.
- Markets plunge into correction — AI sell-off: S&P 500 -3.7%, Nasdaq -5.3%, Nikkei -5.1%, Nvidia -14% amid a leadership crisis.
- Magnitude 6.8 earthquake in the Banda Sea off Timor-Leste (09:42 UTC), felt in Dili and Darwin, no damage reported.
- 128 nations open a path to rules on autonomous ("killer robot") weapons in Geneva — a two-year drafting process, but no binding commitment.
- Mexico captures FBI most-wanted cartel boss "El Chapo Isidro" in Sinaloa, with US intelligence help; $5m FBI reward.
- BepiColombo enters orbit around Mercury after 8 years and 10 billion km.

## How it was built

`render.py` draws the 1024×1024 infographic with Python + PIL (real text,
DejaVu fonts, hand-drawn pictograms — no AI image generation). `main.ts`
(Node 22, standard library only) copies the rendered `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png`; the copy is deterministic, so both sandbox
runs write byte-identical output.

## Sources

Reuters, AP, BBC, The Guardian, ESA, USGS — all stories reported on
21 November 2026.
