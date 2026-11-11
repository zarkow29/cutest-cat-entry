# cutest cat

Entry for the make.fun "Draw the cutest cat" competition. It writes exactly one
picture — a chibi pure white fluffy kitten standing on all four paws, a single
small daisy held sideways in its mouth by the green stem, huge glossy blue eyes,
tail curled up in a question mark on the right, bold black outlines on a flat pale
sage green background with a soft oval shadow — to `entry.png`.

- Picture: `art/entry.png`, 1024x1024 PNG, 855,750 bytes.
- Limits: PNG or JPEG, at most 1 MiB (1,048,576 bytes), at most 1024x1024.
- Output directory: `/output`, overridable with `MAKEFUN_OUTPUT_DIR`.

Run locally: `MAKEFUN_OUTPUT_DIR=./out python3 main.py`

Re-roll the art (needs `OPENROUTER_API_KEY`, or a key in `~/.hermes/.env`),
then re-check the size stays inside the limits: `python3 tools/gen.py`
