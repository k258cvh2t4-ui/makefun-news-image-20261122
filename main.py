#!/usr/bin/env python3
"""make.fun entry: news-image-20261122 — "Sum up 22 November's world news in one image".

Writes the pre-rendered front page (entry.png, bundled in this repository)
to /output/entry.png. Deterministic: a byte-for-byte copy, no network,
no randomness, no timestamps — running it twice produces identical bytes.
"""
import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"


def main():
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(SRC, DST)
    with open(DST, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    print("wrote %s sha256=%s" % (DST, digest))


if __name__ == "__main__":
    main()
