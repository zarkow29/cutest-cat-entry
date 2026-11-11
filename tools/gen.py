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
    "cute kawaii chibi cream kitten peeking out of an open brown cardboard box, "
    "only its oversized head, two front paws and fluffy tail showing, body hidden "
    "inside the box, both rounded front paws draped over the front edge of the box "
    "with soft toe lines, head centred and facing the viewer with a slight innocent "
    "tilt, huge glossy round black eyes with big white catchlights and tiny curved "
    "eyebrow dashes, pleading wide-eyed expression, tiny pink triangular nose, small "
    "W-shaped mouth, upright triangular ears with pale pink inner ears and little fur "
    "tufts, long thin white whiskers fanning outward, solid cream off-white fur with "
    "no stripes, soft cheek tufts, box top flaps folded open and angled outward, one "
    "small rectangular tape label on the box front, thick fluffy cream tail curling "
    "upward on the viewer-right like a question mark with a jagged fluffy tip, plain "
    "solid dusty rose pink background, no ground shadow, thick clean black linework, "
    "flat colors, light cel shading, subject centred with generous balancing negative "
    "space, sticker-like 2D vector illustration, cozy playful innocent mood, square "
    "composition, no text"
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
