"""Generate the original pixel-art bar scene inlined into the homepage viewport.

Run `python scripts/make_scene.py` after changing the scene, then rebuild.
The artwork is drawn from rectangles on a 320x180 grid; no third-party
assets are used. Animation classes are styled in site/styles.css.
"""
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[1]
W, H = 320, 180
rng = random.Random(813)
out = []

FONT = {  # 3x5 pixel glyphs
    "O": ["111", "101", "101", "101", "111"],
    "P": ["111", "101", "111", "100", "100"],
    "E": ["111", "100", "111", "100", "111"],
    "N": ["101", "111", "111", "111", "101"],
}


def rect(x, y, w, h, fill, extra=""):
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{extra}/>')


def text(word, x, y, scale, fill):
    for index, letter in enumerate(word):
        for row, line in enumerate(FONT[letter]):
            for col, bit in enumerate(line):
                if bit == "1":
                    rect(x + index * 4 * scale + col * scale, y + row * scale, scale, scale, fill)


def skyline(base, colour, min_w, max_w, min_h, max_h, lights):
    x = 14
    while x < 212:
        w = min(rng.randint(min_w, max_w), 212 - x)
        h = rng.randint(min_h, max_h)
        rect(x, base - h, w, h, colour)
        if lights:
            for wy in range(base - h + 2, base - 1, 3):
                for wx in range(x + 1, x + w - 1, 2):
                    roll = rng.random()
                    if roll < 0.2:
                        tone = rng.choice(["#3df2e0", "#ffc857", "#ff3d8b", "#9b6bff"])
                        blink = ' class="sc-blink"' if roll < 0.035 else ""
                        rect(wx, wy, 1, 1, tone, blink)
            if rng.random() < 0.3 and w > 5:
                rect(x + w // 2, base - h - 5, 1, 5, colour)
                rect(x + w // 2, base - h - 6, 1, 1, "#ff3d8b", ' class="sc-blink"')
        x += w + rng.choice([0, 0, 1])


# Wall
rect(0, 0, W, H, "#120d26")
for x in range(0, W, 16):
    rect(x, 0, 1, 128, "#171032")

# Window and the city beyond it
rect(10, 12, 206, 98, "#2c2158")
out.append('<clipPath id="sc-window"><rect x="14" y="16" width="198" height="90"/></clipPath>')
out.append('<g clip-path="url(#sc-window)">')
for y, h, tone in [(16, 20, "#150f35"), (36, 16, "#1f1247"), (52, 14, "#32155a"),
                   (66, 12, "#53186a"), (78, 12, "#7c1d70"), (90, 16, "#a8246f")]:
    rect(14, y, 198, h, tone)
rect(150, 30, 26, 12, "#3df2e0", ' opacity="0.16"')
rect(152, 32, 22, 8, "#3df2e0", ' opacity="0.35" class="sc-blink-slow"')
skyline(106, "#241a52", 8, 18, 22, 56, False)
skyline(106, "#0e0a20", 10, 24, 12, 40, True)
out.append('<g class="sc-rain-skew"><g class="sc-rain">')
drops = [(rng.randint(0, 262), rng.randint(0, 29)) for _ in range(24)]
for tile in range(-1, 4):  # the pattern repeats every 30px so the CSS loop is seamless
    for x, y in drops:
        rect(x, y + tile * 30, 1, 3, "#9fb4ff", ' opacity="0.4"')
out.append("</g></g>")
out.append('<polygon points="14,16 60,16 14,70" fill="#ffffff" opacity="0.04"/>')
out.append('<polygon points="120,16 150,16 70,106 40,106" fill="#ffffff" opacity="0.03"/>')
out.append("</g>")
rect(80, 16, 3, 90, "#2c2158")
rect(146, 16, 3, 90, "#2c2158")
rect(8, 108, 210, 4, "#3a2c74")
rect(8, 108, 210, 1, "#5a45a8")

# Neon sign
out.append('<g class="sc-neon">')
rect(226, 12, 84, 34, "#1a1338")
rect(226, 12, 84, 1, "#3a2c74")
rect(226, 45, 84, 1, "#3a2c74")
for row, width in enumerate([14, 12, 10, 8, 6, 4, 2]):
    rect(232 + row, 18 + row, width, 1, "#ff3d8b")
rect(238, 25, 2, 9, "#ff3d8b")
rect(234, 34, 10, 2, "#ff3d8b")
rect(244, 17, 3, 3, "#ffc857")
text("OPEN", 254, 22, 3, "#3df2e0")
out.append("</g>")

# Back shelves
rect(224, 54, 90, 66, "#1a1338")
rect(224, 54, 90, 1, "#3a2c74")
palette = ["#ff3d8b", "#3df2e0", "#ffc857", "#9b6bff", "#6ee7a0", "#ff7a45"]
for shelf in (74, 96, 118):
    x = 228
    while x < 306:
        w = rng.choice([4, 5, 6])
        h = rng.randint(9, 15)
        tone = rng.choice(palette)
        rect(x, shelf - h, w, h, tone, ' opacity="0.85"')
        rect(x, shelf - h, 1, h, "#ffffff", ' opacity="0.35"')
        rect(x + w // 2 - 1, shelf - h - 4, 2, 4, tone, ' opacity="0.85"')
        rect(x, shelf - h // 2, w, 3, "#120d26", ' opacity="0.45"')
        x += w + rng.choice([2, 3, 4])
    rect(224, shelf, 90, 2, "#3a2c74")
    rect(224, shelf + 2, 90, 1, "#3df2e0", ' opacity="0.45"')

# Pendant lamps
for x in (48, 114, 182, 268):
    rect(x, 0, 1, 9, "#3a2c74")
    out.append(f'<polygon points="{x - 3},9 {x + 4},9 {x + 7},15 {x - 6},15" fill="#3a2c74"/>')
    rect(x - 5, 15, 11, 1, "#ffc857")
    out.append(f'<polygon points="{x - 5},16 {x + 6},16 {x + 30},128 {x - 29},128" fill="#ffc857" opacity="0.045"/>')

# Counter
rect(0, 128, W, 2, "#5a45a8")
rect(0, 130, W, 8, "#2f2364")
rect(0, 138, W, 42, "#191233")
for x in range(0, W, 40):
    rect(x, 138, 1, 42, "#120d26")
rect(0, 141, W, 1, "#ff3d8b", ' class="sc-strip"')
rect(0, 142, W, 3, "#ff3d8b", ' opacity="0.14"')
rect(0, 176, W, 4, "#0b0817")

# Shaker
rect(42, 107, 10, 21, "#b9c0d9")
rect(42, 107, 2, 21, "#e8ecff")
rect(50, 107, 2, 21, "#7d86a8")
rect(42, 113, 10, 1, "#7d86a8")
rect(44, 101, 6, 6, "#8f97b8")
rect(45, 98, 4, 3, "#b9c0d9")

# Cocktail glass
for row, width in enumerate([14, 12, 12, 10, 8, 6, 4, 2]):
    tone = "#cfd6ff" if row < 2 else "#ff3d8b"
    rect(68 + (14 - width) // 2, 109 + row, width, 1, tone, ' opacity="0.9"')
rect(74, 117, 2, 9, "#cfd6ff")
rect(70, 126, 10, 2, "#cfd6ff")
rect(79, 106, 1, 5, "#6ee7a0")
rect(78, 105, 3, 2, "#ff7a45")

# Tumbler
rect(96, 114, 12, 14, "#cfd6ff", ' opacity="0.35"')
rect(97, 119, 10, 8, "#ffc857", ' opacity="0.85"')
rect(99, 117, 4, 4, "#ffffff", ' opacity="0.6"')
rect(96, 114, 1, 14, "#ffffff", ' opacity="0.5"')

# Terminal
rect(146, 94, 50, 32, "#2a2150")
rect(146, 94, 50, 1, "#5a45a8")
rect(149, 97, 44, 24, "#081417")
for index, width in enumerate([22, 34, 16, 28, 12]):
    rect(152, 100 + index * 4, width, 1, "#3df2e0" if index % 2 else "#6ee7a0", ' opacity="0.9"')
rect(166, 116, 3, 2, "#3df2e0", ' class="sc-cursor"')
rect(190, 123, 2, 1, "#ff3d8b")
rect(166, 126, 10, 2, "#2a2150")

# Second drink and coaster
rect(214, 127, 16, 1, "#3a2c74")
rect(217, 113, 10, 14, "#cfd6ff", ' opacity="0.3"')
rect(218, 116, 8, 10, "#3df2e0", ' opacity="0.75"')
rect(225, 109, 1, 8, "#ff86bd")

svg = (f'<svg class="bar-scene" viewBox="0 0 {W} {H}" role="img" shape-rendering="crispEdges" '
       f'aria-label="Pixel art of a neon-lit bar counter at night: rain over a city skyline, '
       f'bottles on back-lit shelves, a shaker, two drinks, and a terminal.">' + "".join(out) + "</svg>\n")
target = ROOT / "content" / "art" / "bar-scene.svg"
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(svg, encoding="utf-8")
print(f"Wrote {target.relative_to(ROOT)} ({len(out)} shapes).")
