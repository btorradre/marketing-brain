"""Generate Motilli favicon: bold geometric 'M' on Motilli green, rounded square."""
from PIL import Image, ImageDraw

SIZE = 512
SCALE = 4
W = SIZE * SCALE
RADIUS = 96 * SCALE
BG = (148, 194, 24, 255)   # #94C218
FG = (255, 255, 255, 255)

img = Image.new("RGBA", (W, W), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
d.rounded_rectangle((0, 0, W, W), radius=RADIUS, fill=BG)

# M as four thick line segments with rounded caps/joints (drawn as a single polyline).
left   = int(W * 0.22)
right  = int(W * 0.78)
top    = int(W * 0.24)
bottom = int(W * 0.76)
mid_y  = int(W * 0.62)  # where the two diagonals meet
stroke = int(W * 0.16)
cx     = W // 2

# Outer poly: left leg up, diagonal down to center, diagonal up to right top, right leg down.
pts = [
    (left,   bottom),
    (left,   top),
    (cx,     mid_y),
    (right,  top),
    (right,  bottom),
]
d.line(pts, fill=FG, width=stroke, joint="curve")

# Round the four endpoints (caps) since PIL's polyline doesn't cap a thick line at ends.
r = stroke // 2
for (x, y) in [(left, bottom), (left, top), (right, top), (right, bottom)]:
    d.ellipse((x - r, y - r, x + r, y + r), fill=FG)

img = img.resize((SIZE, SIZE), Image.LANCZOS)
img.save("favicon-motilli.png", "PNG")
img.save("favicon-motilli.ico", format="ICO", sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
print("ok")
