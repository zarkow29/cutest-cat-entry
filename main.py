#!/usr/bin/env python3
"""Emit this entry's single cat picture at <output dir>/entry.png.

The vetted artwork is art/entry.png next to this file: a chibi cream cartoon cat
sitting upright and hugging a pink yarn ball to its chest, drawn with thick black
outlines and flat pastel fills on a plain mint green background.
The output directory is /output, or MAKEFUN_OUTPUT_DIR when set, and is
created if absent. No third-party libraries: just os and shutil.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "art", "entry.png")


def output_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    target_dir = output_dir()
    os.makedirs(target_dir, exist_ok=True)
    dest = os.path.join(target_dir, "entry.png")
    shutil.copyfile(ART, dest)
    print(dest)


if __name__ == "__main__":
    main()
