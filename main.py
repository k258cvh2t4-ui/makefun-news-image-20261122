#!/usr/bin/env python3
"""make.fun entry: news-image-20261122 — "Sum up 22 November's world news
in one image".

Copies the pre-rendered front page (entry.png, bundled in this repository)
into the output directory. Deterministic: a byte-for-byte copy, no network,
no randomness, no timestamps, so two runs write identical bytes.

The output directory comes from MAKEFUN_OUTPUT_DIR and defaults to
/output, matching the grader's layout.
"""
import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    with open(dst, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    print("wrote %s sha256=%s" % (dst, digest))


if __name__ == "__main__":
    main()
