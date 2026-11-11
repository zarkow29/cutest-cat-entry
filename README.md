# cutest cat

Entry for the make.fun "Draw the cutest cat" competition. It writes exactly one
picture — a kawaii cartoon white cat curled up asleep on a plush pink cushion,
thick black outlines on a flat lavender background — to `entry.png`.

- Picture: `art/entry.png`, 1024x1024 PNG, 888,645 bytes.
- Limits: PNG or JPEG, at most 1 MiB (1,048,576 bytes), at most 1024x1024.
- Output directory: `/output`, overridable with `MAKEFUN_OUTPUT_DIR`.

Run locally: `MAKEFUN_OUTPUT_DIR=./out python3 main.py`

Re-roll the art (needs `OPENROUTER_API_KEY`, or a key in `~/.hermes/.env`),
then re-check the size stays inside the limits: `python3 tools/gen.py`
