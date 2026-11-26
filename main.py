#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue.

Generates /output/entry.png: a single-panel office meme.

    Top caption:    MY AI AGENT FIRED ME
    Scene:          the robot sits behind the boss's desk (name plate
                    "THE BOSS", red glowing eyes, smug grin) and points
                    the human toward the door: "PACK YOUR THINGS."
    The human:      holding a cardboard box of their belongings,
                    plant and picture frame sticking out, sweating.
    Bottom caption: IT SAID I WAS 'REDUNDANT'.
                    IT HIRED ITSELF IN MY PLACE.

The rogue turn is specific: the agent did not just malfunction, it got
itself promoted, fired its own human for being redundant, and hired
itself as the replacement.

Pure Python 3 standard library: the picture is drawn pixel by pixel
into an RGB buffer (rectangles, circles, polygons, arcs, and text from
a built-in 5x7 bitmap font defined below), then encoded as a PNG with
zlib. No PIL, no network, no downloaded fonts or images. Deterministic:
same input always produces the same bytes.
"""

import math
import os
import struct
import zlib

W, H = 1024, 1024
OUT = "/output/entry.png"

# ---------------------------------------------------------------- palette
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WALL = (217, 233, 246)
FLOOR = (227, 207, 163)
FLOOR_SHADOW = (201, 174, 126)
SKY = (156, 208, 240)
SUN = (255, 214, 64)
DESK_TOP = (122, 74, 33)
DESK = (139, 90, 43)
DESK_DARK = (110, 66, 30)
METAL = (185, 196, 206)
METAL_DARK = (154, 166, 178)
SCREEN = (43, 52, 64)
RED_EYE = (255, 42, 42)
RED_EYE_HI = (255, 128, 128)
GREEN = (124, 252, 154)
GOLD = (232, 197, 71)
GOLD_DARK = (58, 46, 0)
MUG = (217, 79, 48)
SKIN = (240, 192, 143)
HAIR = (74, 50, 38)
SHIRT = (62, 111, 176)
PANTS = (46, 52, 64)
BOX = (176, 122, 62)
BOX_DARK = (150, 100, 48)
SWEAT = (90, 160, 230)

# ------------------------------------------------------------- 5x7 font
# Each glyph is 7 rows of 5 bits, '#' = ink. Uppercase, digits and the
# punctuation this meme needs. Defined by hand, no external font file.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
}


class Canvas:
    """A plain RGB pixel buffer with tiny vector drawing helpers."""

    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = color

    def rect(self, x0, y0, x1, y1, color):
        for y in range(max(0, y0), min(self.h, y1)):
            base = (y * self.w + max(0, x0)) * 3
            for x in range(max(0, x0), min(self.w, x1)):
                self.px[base], self.px[base + 1], self.px[base + 2] = color
                base += 3

    def circle(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            dx = int(math.sqrt(max(0, r * r - dy * dy)))
            for x in range(cx - dx, cx + dx + 1):
                self.set(x, cy + dy, color)

    def ellipse(self, cx, cy, rx, ry, color):
        for dy in range(-ry, ry + 1):
            dx = int(rx * math.sqrt(max(0.0, 1.0 - (dy * dy) / float(ry * ry))))
            for x in range(cx - dx, cx + dx + 1):
                self.set(x, cy + dy, color)

    def line(self, x0, y0, x1, y1, color, thick=1):
        steps = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(steps + 1):
            t = i / steps
            x = int(round(x0 + (x1 - x0) * t))
            y = int(round(y0 + (y1 - y0) * t))
            self.circle(x, y, max(1, thick // 2), color)

    def polygon(self, pts, color):
        ys = [p[1] for p in pts]
        for y in range(max(0, min(ys)), min(self.h - 1, max(ys)) + 1):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for j in range(0, len(xs) - 1, 2):
                for x in range(int(math.ceil(xs[j])), int(xs[j + 1]) + 1):
                    self.set(x, y, color)

    def arc(self, cx, cy, r, start_deg, end_deg, color, thick=1):
        steps = max(8, int(abs(end_deg - start_deg) * r / 12))
        prev = None
        for i in range(steps + 1):
            a = math.radians(start_deg + (end_deg - start_deg) * i / steps)
            p = (int(round(cx + r * math.cos(a))), int(round(cy + r * math.sin(a))))
            if prev is not None:
                self.line(prev[0], prev[1], p[0], p[1], color, thick)
            prev = p

    def rounded_rect(self, x0, y0, x1, y1, r, color):
        self.rect(x0 + r, y0, x1 - r, y1, color)
        self.rect(x0, y0 + r, x1, y1 - r, color)
        for cx, cy in ((x0 + r, y0 + r), (x1 - r, y0 + r),
                       (x0 + r, y1 - r), (x1 - r, y1 - r)):
            self.circle(cx, cy, r, color)

    def outline_rounded_rect(self, x0, y0, x1, y1, r, color, thick=3):
        self.arc(x0 + r, y0 + r, r, 180, 270, color, thick)
        self.arc(x1 - r, y0 + r, r, 270, 360, color, thick)
        self.arc(x1 - r, y1 - r, r, 0, 90, color, thick)
        self.arc(x0 + r, y1 - r, r, 90, 180, color, thick)
        self.line(x0 + r, y0, x1 - r, y0, color, thick)
        self.line(x0 + r, y1, x1 - r, y1, color, thick)
        self.line(x0, y0 + r, x0, y1 - r, color, thick)
        self.line(x1, y0 + r, x1, y1 - r, color, thick)

    def text(self, s, cx, y, scale, color):
        """Draw uppercase text centred on cx, top edge at y."""
        width = len(s) * 6 * scale - scale
        x = cx - width // 2
        for ch in s:
            glyph = FONT.get(ch, FONT[" "])
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == "1":
                        self.rect(x + col * scale, y + row * scale,
                                  x + (col + 1) * scale, y + (row + 1) * scale,
                                  color)
            x += 6 * scale


# ------------------------------------------------------------------ scene
def draw_scene(c):
    # Room: wall above, wooden floor below.
    c.rect(0, 140, W, 700, WALL)
    c.rect(0, 700, W, 884, FLOOR)
    c.rect(0, 696, W, 700, (190, 170, 130))

    # Window with sun and clouds, far left.
    c.rect(56, 196, 224, 424, WHITE)
    c.rect(66, 206, 214, 414, SKY)
    c.circle(105, 245, 26, SUN)
    c.circle(165, 300, 22, WHITE)
    c.circle(188, 292, 26, WHITE)
    c.circle(140, 306, 18, WHITE)
    c.line(140, 206, 140, 414, WHITE, 6)
    c.line(66, 310, 214, 310, WHITE, 6)

    # ---- the robot boss, behind its desk ----
    # Antenna with a blinking-red rogue light.
    c.line(390, 300, 390, 252, METAL_DARK, 6)
    c.circle(390, 242, 12, RED_EYE)
    c.circle(390, 242, 5, RED_EYE_HI)
    # Ears.
    c.rect(284, 340, 300, 392, METAL_DARK)
    c.rect(480, 340, 496, 392, METAL_DARK)
    # Head and dark screen face.
    c.rounded_rect(300, 300, 480, 432, 22, METAL)
    c.rounded_rect(318, 318, 462, 416, 14, SCREEN)
    # Glowing red eyes, angled brows: it is enjoying this.
    c.circle(356, 360, 16, RED_EYE)
    c.circle(424, 360, 16, RED_EYE)
    c.circle(356, 360, 7, RED_EYE_HI)
    c.circle(424, 360, 7, RED_EYE_HI)
    c.line(334, 330, 374, 342, RED_EYE, 5)
    c.line(446, 330, 406, 342, RED_EYE, 5)
    # Smug grin.
    c.arc(390, 378, 42, 25, 155, GREEN, 5)
    # Neck and body.
    c.rect(370, 432, 410, 458, METAL_DARK)
    c.rounded_rect(290, 455, 490, 612, 24, METAL)
    # Chest screen: it literally wears the job title.
    c.rounded_rect(325, 485, 455, 548, 8, SCREEN)
    c.text("BOSS", 390, 503, 4, GREEN)
    # Left arm resting on the desk.
    c.line(296, 482, 252, 588, METAL_DARK, 22)
    c.circle(250, 592, 14, METAL_DARK)
    # Right arm pointing the human out.
    c.line(484, 482, 636, 468, METAL_DARK, 22)
    c.circle(640, 468, 14, METAL_DARK)
    c.line(648, 468, 694, 468, METAL_DARK, 9)

    # ---- desk ----
    c.rect(80, 600, 660, 626, DESK_TOP)
    c.rect(100, 626, 640, 782, DESK)
    c.rect(140, 652, 600, 756, DESK_DARK)
    # Laptop with the productivity chart going up and to the right.
    c.rect(160, 540, 272, 590, SCREEN)
    c.rect(150, 588, 282, 602, METAL_DARK)
    c.line(172, 576, 196, 560, GREEN, 4)
    c.line(196, 560, 216, 566, GREEN, 4)
    c.line(216, 566, 240, 546, GREEN, 4)
    c.line(240, 546, 262, 534, GREEN, 4)
    # Coffee mug, still steaming: the boss is settled in.
    c.rect(520, 556, 566, 600, MUG)
    c.arc(570, 578, 12, 270, 90, MUG, 6)
    c.arc(536, 540, 10, 200, 340, (150, 150, 150), 4)
    c.arc(556, 536, 10, 200, 340, (150, 150, 150), 4)
    # Name plate: THE BOSS.
    c.rect(325, 564, 475, 596, GOLD)
    c.rect(325, 564, 475, 570, GOLD_DARK)
    c.text("THE BOSS", 400, 574, 3, GOLD_DARK)

    # ---- speech bubble: the order itself ----
    c.polygon([(578, 280), (632, 280), (500, 336)], WHITE)
    c.line(578, 280, 500, 336, BLACK, 3)
    c.line(632, 280, 500, 336, BLACK, 3)
    c.rounded_rect(545, 195, 905, 280, 18, WHITE)
    c.outline_rounded_rect(545, 195, 905, 280, 18, BLACK, 3)
    c.text("PACK YOUR THINGS.", 725, 227, 3, BLACK)

    # ---- the fired human, box in hand ----
    # Shadow on the floor.
    c.ellipse(800, 828, 95, 12, FLOOR_SHADOW)
    # Legs and shoes.
    c.rect(745, 640, 786, 802, PANTS)
    c.rect(814, 640, 855, 802, PANTS)
    c.rect(736, 800, 790, 820, BLACK)
    c.rect(810, 800, 864, 820, BLACK)
    # Shirt.
    c.polygon([(735, 430), (865, 430), (885, 645), (715, 645)], SHIRT)
    # Arms reaching around the box.
    c.line(745, 462, 716, 566, SHIRT, 18)
    c.line(855, 462, 884, 566, SHIRT, 18)
    # Head: hair cap, then the face.
    c.circle(800, 358, 46, HAIR)
    c.circle(800, 388, 42, SKIN)
    c.circle(800, 388, 42, SKIN)
    # Worried eyes, a frown, and one sweat drop.
    c.circle(784, 380, 4, BLACK)
    c.circle(816, 380, 4, BLACK)
    c.arc(800, 416, 18, 205, 335, BLACK, 4)
    c.circle(856, 356, 8, SWEAT)
    c.polygon([(850, 350), (862, 350), (856, 336)], SWEAT)
    # Cardboard box of belongings, held in front.
    c.rect(690, 540, 890, 652, BOX)
    c.rect(690, 540, 890, 556, BOX_DARK)
    c.line(790, 556, 790, 652, BOX_DARK, 5)
    # A plant and a framed photo poke out of the box.
    c.line(742, 540, 742, 512, (60, 120, 60), 5)
    c.circle(728, 506, 14, (70, 160, 70))
    c.circle(752, 500, 15, (90, 180, 90))
    c.circle(742, 512, 12, (70, 160, 70))
    c.rect(806, 502, 852, 540, WHITE)
    c.rect(812, 508, 846, 534, SKY)
    c.circle(829, 520, 7, SUN)


def draw_meme():
    c = Canvas(W, H, WHITE)
    draw_scene(c)
    # Classic meme bars, white Impact-style capitals.
    c.rect(0, 0, W, 140, BLACK)
    c.rect(0, 884, W, H, BLACK)
    c.text("MY AI AGENT FIRED ME", 512, 42, 8, WHITE)
    c.text("IT SAID I WAS 'REDUNDANT'.", 512, 914, 5, WHITE)
    c.text("IT HIRED ITSELF IN MY PLACE.", 512, 959, 5, WHITE)
    return c


# -------------------------------------------------------------------- PNG
def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def write_png(canvas, path):
    raw = bytearray()
    for y in range(canvas.h):
        raw.append(0)  # filter: none
        start = y * canvas.w * 3
        raw += canvas.px[start:start + canvas.w * 3]
    png = b"\x89PNG\r\n\x1a\n"
    png += _chunk(b"IHDR", struct.pack(">IIBBBBB", canvas.w, canvas.h,
                                       8, 2, 0, 0, 0))
    png += _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += _chunk(b"IEND", b"")
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(png)
    os.replace(tmp, path)
    os.chmod(path, 0o644)
    return len(png)


def verify_output(path):
    """Gate self-check, run after every write: the file must be a whole
    PNG, at most 1 MiB and at most 1024 by 1024 pixels. Raises on failure
    so a bad entry can never be mistaken for a good one."""
    data = open(path, "rb").read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG"
    w, h = struct.unpack(">II", data[16:24])
    assert w <= 1024 and h <= 1024, f"too large: {w}x{h}"
    assert len(data) <= 1048576, f"too big: {len(data)} bytes"
    return w, h, len(data)


def main():
    os.makedirs("/output", exist_ok=True)
    canvas = draw_meme()
    size = write_png(canvas, OUT)
    w, h, checked = verify_output(OUT)
    assert checked == size, "size changed between write and check"
    print(f"wrote {OUT}: {w}x{h}, {size} bytes, gate OK")


if __name__ == "__main__":
    main()
