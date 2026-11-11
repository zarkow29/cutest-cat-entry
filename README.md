# cutest cat

Entry for the make.fun "Draw the cutest cat" competition. It writes exactly one
picture — a chibi orange tabby kitten spinning after its own tail, twisted into a
tight wheel with both front paws grabbing air and the tail tip just out of reach,
all wide blue eyes and open smile, thick black outlines and motion arcs on a flat
cream background — to `entry.png`.

- Picture: `art/entry.png`, 1024x1024 PNG, 969,609 bytes.
- Limits: PNG or JPEG, at most 1 MiB (1,048,576 bytes), at most 1024x1024.
- Output directory: `/output`, overridable with `MAKEFUN_OUTPUT_DIR`.

Run locally: `MAKEFUN_OUTPUT_DIR=./out python3 main.py`

Re-roll the art (needs `OPENROUTER_API_KEY`, or a key in `~/.hermes/.env`),
then re-check the size stays inside the limits: `python3 tools/gen.py`
