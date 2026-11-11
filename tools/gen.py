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
    "cute kawaii chibi orange tabby kitten spinning in place chasing its own "
    "tail, body twisted into a tight near-circular wheel, oversized head flung "
    "around to the viewer-left as it snaps after the tail tip, joyfully "
    "wide-eyed expression with a tiny open smile, huge blue eyes with big black "
    "pupils and star-shaped white highlights, tiny pink triangular nose, "
    "triangular ears with pink inner ears and zigzag fur tufts, long thin white "
    "whiskers fanning outward, darker orange tabby stripes across the head, back "
    "and tail, cream muzzle, chest, paws and jagged tail tip, both front paws "
    "reaching after the tail with pink toe beans showing, one hind paw lifted "
    "mid-stride, thick striped tail curving around the body on the viewer-right "
    "just out of reach, bold black motion arcs and speed dashes circling the "
    "whole spin, plain solid cream background, no ground shadow, thick clean "
    "black linework, flat colors, light cel shading, subject centered with "
    "balancing negative space, sticker-like 2D vector illustration, frantic "
    "playful mood, square composition, no text"
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
