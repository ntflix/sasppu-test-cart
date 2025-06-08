import struct

data = open("plane.bin", "rb").read()
# unpack all pixels as little-endian uint16
pixels = struct.unpack("<%dH" % (len(data) // 2), data)


# convert each to 8-bit RGB
def bgr555_to_rgb888(c):
    b = (c) & 0x1F
    g = (c >> 5) & 0x1F
    r = (c >> 10) & 0x1F
    return ((r << 3) | (r >> 2), (g << 3) | (g >> 2), (b << 3) | (b >> 2))


rgb_pixels = [bgr555_to_rgb888(c) for c in pixels]
# you can then reshape into 32 rows of 512 pixels each
