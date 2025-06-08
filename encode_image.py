#!/usr/bin/env python3
import sys
import struct
from PIL import Image


def rgb888_to_bgr555(r, g, b):
    # down-scale 8-bit to 5-bit
    r5 = r >> 3
    g5 = g >> 3
    b5 = b >> 3
    # pack into 0bggrr (BGR555) and leave high bit clear
    return (b5) | (g5 << 5) | (r5 << 10)


def encode_image(input_png, output_bin):
    img = Image.open(input_png).convert("RGB")
    w, h = img.size
    pixels = list(img.getdata())
    with open(output_bin, "wb") as f:
        for r, g, b in pixels:
            val = rgb888_to_bgr555(r, g, b)
            f.write(struct.pack("<H", val))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python encode.py input.png output.bin")
        sys.exit(1)
    encode_image(sys.argv[1], sys.argv[2])
