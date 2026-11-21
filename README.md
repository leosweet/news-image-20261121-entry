# 21 November 2026 — The World in One Picture

One image summing up the world's news of Saturday 21 November 2026:

- Russia's biggest strike on Ukraine yet — 400+ drones and 110 missiles on Kyiv, 8 killed, power cut in 10 regions; missiles land in Poland.
- Markets plunge into correction — AI sell-off: S&P 500 -3.7%, Nikkei -5.1%, Nvidia -14% as the SEC probes its accounting.
- Magnitude 6.8 earthquake off Timor-Leste (09:42 UTC), no tsunami threat.
- 128 nations agree to draft rules on autonomous ("killer robot") weapons in Geneva.
- Mexico captures FBI most-wanted cartel boss "El Chapo Isidro" in Sinaloa.
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
