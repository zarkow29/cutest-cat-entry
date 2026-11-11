#!/usr/bin/env python3
"""Re-roll the cat art via OpenRouter image generation, overwriting art/entry.png.

Reads OPENROUTER_API_KEY from the environment, or from
/home/ubuntu/.hermes/.env when it is unset. Standard library only.
"""

import base64
import json
import os
import struct
import urllib.request

ENV_PATH = "/home/ubuntu/.hermes/.env"
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(os.path.dirname(HERE), "art", "entry.png")
PROMPT = (
    "cute kawaii chibi gray kitten sitting inside a large cream-colored teacup, "
    "oversized head poking above the thick rounded rim, worried surprised "
    "expression with small black curved eyebrows and a tiny downturned mouth, "
    "big expressive eyes with teal irises, yellow-green outer rings, black pupils "
    "and white highlights, tiny pink triangular nose, triangular ears with pink "
    "inner ears, thin black whiskers fanning sideways, ragged fur tufts on cheeks "
    "and chest, one front paw draped over the front rim with toe lines, fluffy "
    "tail curled upward to the viewer-right, one hind paw peeking out at the lower "
    "right, cup has a C-shaped handle on the right and a white vertical highlight "
    "on the left, soft darker mustard oval shadow beneath the cup, solid warm "
    "mustard yellow background, thick clean black linework, flat colors, minimal "
    "shading, subject centered with balancing negative space, sticker-like 2D "
    "vector illustration, anxious cozy mood, square composition, no text"
)


def api_key():
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:
        return key
    with open(ENV_PATH, encoding="utf-8") as handle:
        for line in handle:
            name, _, value = line.strip().partition("=")
            if name == "OPENROUTER_API_KEY":
                return value.strip().strip('"').strip("'")
    raise SystemExit("OPENROUTER_API_KEY not set and not found in " + ENV_PATH)


def main():
    payload = json.dumps({
        "model": "google/gemini-2.5-flash-image",
        "messages": [{"role": "user", "content": PROMPT}],
        "modalities": ["image", "text"],
    }).encode()
    request = urllib.request.Request(ENDPOINT, data=payload, headers={
        "Authorization": "Bearer " + api_key(),
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(request, timeout=180) as response:
        body = json.load(response)

    message = body["choices"][0]["message"]
    url = message["images"][0]["image_url"]["url"]
    raw = base64.b64decode(url.split(",", 1)[1])

    os.makedirs(os.path.dirname(ART), exist_ok=True)
    with open(ART, "wb") as handle:
        handle.write(raw)
    width, height = struct.unpack(">II", raw[16:24])
    print("bytes", len(raw))
    print("pixels %dx%d" % (width, height))


if __name__ == "__main__":
    main()
