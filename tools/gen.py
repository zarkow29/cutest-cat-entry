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
    "cute kawaii chibi white kitten sitting upright and facing the viewer, one "
    "front paw lifted in a friendly greeting at the viewer-right with pink paw "
    "pads and three round toe beans showing, the other front leg planted straight "
    "down, a small red heart sitting flat on the centre of its forehead, "
    "oversized rounded head on a small body with chibi proportions, huge sparkling "
    "blue eyes with black pupils and white catchlight dots, tiny curved black "
    "eyebrows, tiny pink triangular nose, small black W-shaped smiling mouth, "
    "three long thin black whiskers fanned out on each side, upright triangular "
    "ears with pale pink inner ears and small black tufts, soft fur tufts on the "
    "cheeks and chest, fluffy tail curled out to the viewer-left, hind legs tucked "
    "under the seated body, bold even black outlines, flat white fur with soft "
    "pale blue-grey cel shading under the chin chest legs tail and raised paw, "
    "simple oval mauve shadow beneath the body, plain solid pastel pink "
    "background, subject centred with generous negative space around it, "
    "sticker-like clean 2D vector illustration, affectionate friendly mood, "
    "square composition, no text"
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
