"""Generate docs/pipeline.png flowchart with Pillow (stdlib + pillow only)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1500, 850
BG = (17, 24, 39)
CARD = [(37, 99, 235), (5, 150, 105), (124, 58, 237), (2, 132, 199), (22, 163, 74)]
FG = (255, 255, 255)
SUB = (229, 231, 235)
img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def font(size):
    for name in ("arial.ttf", "DejaVuSans-Bold.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()

f_title = font(44); f_head = font(26); f_body = font(22); f_foot = font(20)
d.text((W // 2, 50), "Data Engineering Fundamentals Pipeline", fill=FG, font=f_title, anchor="mt")
d.text((W // 2, 105), "Linux  •  REST APIs  •  Docker  •  Git branching + PRs", fill=SUB, font=f_body, anchor="mt")

stages = [
    ("1  SECURE LANDING ZONES", "Linux  •  chmod 750 / 700", ["raw/ 750 ingress", "staging/ 750 team", "processed/ 700 restricted"]),
    ("2  LOG ANALYSIS", "grep  awk  sort  uniq", ["app.log: 500 lines", "81 ERROR / 84 WARN", "analysis_errors.txt"]),
    ("3  REST API INGEST", "jsonplaceholder.typicode.com", ["10 users + 100 posts", "users_*.json / .csv", "→ data/landing/raw/"]),
    ("4  DOCKER", "de-fundamentals:1.0", ["ingest reproduced", "postgres:16 pg_isready", "compose up / down"]),
    ("5  GIT + PULL REQUEST", "branch → PR → merge", ["feature/* branches", "PR #1 merged", "AbhiramMandala"]),
]

n = len(stages)
gap = 24
cw = (W - 2 * 40 - gap * (n - 1)) // n
top, ch = 170, 480
for i, (head, tool, lines) in enumerate(stages):
    x0 = 40 + i * (cw + gap)
    x1 = x0 + cw
    d.rounded_rectangle([x0, top, x1, top + ch], radius=22, fill=CARD[i])
    d.text(((x0 + x1) // 2, top + 34), head, fill=FG, font=f_head, anchor="mt")
    d.text(((x0 + x1) // 2, top + 76), tool, fill=(255, 255, 255), font=f_body, anchor="mt")
    d.line([x0 + 24, top + 112, x1 - 24, top + 112], fill=(255, 255, 255), width=2)
    y = top + 140
    for ln in lines:
        d.text(((x0 + x1) // 2, y), "•  " + ln, fill=FG, font=f_body, anchor="mt")
        y += 44
    # step number circle
    d.ellipse([x0 + 18, top + 14, x0 + 62, top + 58], fill=(255, 255, 255))
    d.text((x0 + 40, top + 36), str(i + 1), fill=CARD[i], font=f_head, anchor="mm")
    # arrow to next
    if i < n - 1:
        ax0 = x1 + 2
        ax1 = x1 + gap - 2
        my = top + ch // 2
        d.line([ax0, my, ax1, my], fill=(156, 163, 175), width=5)
        d.polygon([(ax1, my - 10), (ax1, my + 10), (ax1 + 10, my)], fill=(156, 163, 175))

d.text((W // 2, H - 90), "raw  →  staging  →  processed  •  local Linux demo (ubuntu:22.04)  •  GitHub: AbhiramMandala/data-engineering-project",
       fill=SUB, font=f_foot, anchor="mt")
d.text((W // 2, H - 55), "fetch_api.py  •  log_analysis.sh  •  Dockerfile  •  docker-compose.yml", fill=SUB, font=f_foot, anchor="mt")

Path("docs").mkdir(exist_ok=True)
img.save("docs/pipeline.png")
print("saved docs/pipeline.png", img.size)
