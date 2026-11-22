// news-image-20261121 entry point.
//
// The infographic is a fixed asset produced by render.py. This script
// only moves those exact bytes into the output directory, so every run
// writes an identical file.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const sourceDir = dirname(fileURLToPath(import.meta.url));
const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(targetDir, { recursive: true });
const pixels = readFileSync(join(sourceDir, "entry.png"));
writeFileSync(join(targetDir, "entry.png"), pixels);
