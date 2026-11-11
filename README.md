# cutest cat

Entry for the make.fun "Draw the cutest cat" competition. It writes exactly one
picture — a chibi white kitten sitting upright and facing the viewer, one front paw
raised in a friendly greeting with pink toe beans showing, a small red heart on its
forehead, huge blue eyes, a tiny pink nose and a small smiling mouth, whiskers out
wide, tail curled off to the left, bold black outlines on flat white fills with pale
blue-grey shading over a plain pastel pink background and a soft oval shadow — to
`entry.png`.

- Picture: `art/entry.png`, 1024x1024 PNG, 894,692 bytes.
- Limits: PNG or JPEG, at most 1 MiB (1,048,576 bytes), at most 1024x1024.
- Output directory: `/output`, overridable with `MAKEFUN_OUTPUT_DIR`.

Run locally: `MAKEFUN_OUTPUT_DIR=./out python3 main.py`

Re-roll the art (needs `OPENROUTER_API_KEY`, or a key in `~/.hermes/.env`),
then re-check the size stays inside the limits: `python3 tools/gen.py`
