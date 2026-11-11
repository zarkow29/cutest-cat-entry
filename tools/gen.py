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
    "cute kawaii cartoon white kitten sitting upright facing forward, wearing an "
    "oversized bright red knitted beanie pulled low over the forehead with a folded "
    "ribbed cuff and a fluffy pom-pom on top, ears poking out sideways through the "
    "hat, viewer-left front paw raised and touching the brim as if tipping the hat, "
    "other front paw planted between the hind paws, big glossy eyes with "
    "heterochromia, viewer-left eye blue and viewer-right eye green, black pupils, "
    "white eye highlights, tiny pink triangular nose, small closed curved smile, "
    "pink inner ears, thin black whiskers, fluffy white fur with soft gray cel "
    "shading under the chin, chest and legs, fluffy tail curling upward on the "
    "viewer-right side, soft oval shadow beneath the body, flat solid light sage "
    "green background, thick clean black linework, flat colors, subtle cel shading, "
    "subject centered with breathing room, sticker-like 2D vector illustration, "
    "cozy wintery mood, square composition, no text"
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
