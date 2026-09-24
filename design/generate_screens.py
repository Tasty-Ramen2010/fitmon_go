import json, math, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screens")

# ---------- design tokens ----------
INK = "#0B0F1A"; PANEL = "#151B2C"; PANEL2 = "#1D2539"; LINE = "#2B3552"
TEXT = "#F3F5FA"; MUTED = "#A3ACC2"; LIME = "#C8FF3E"
R = {
    "common": ("Common", "#B4BCCB"),
    "uncommon": ("Uncommon", "#34D8B0"),
    "rare": ("Rare", "#4AA8FF"),
    "epic": ("Epic", "#B07CFF"),
    "legendary": ("Legendary", "#FFB229"),
    "mythic": ("Mythic", "#FF4D8D"),
}
DISPLAY = "font-family: 'Chakra Petch', sans-serif"
HEX = "polygon(50% 0, 100% 25%, 100% 75%, 50% 100%, 0 75%, 0 25%)"

ICONS = {
    "pushup": "M2 10a2 2 0 1 0 4 0a2 2 0 1 0-4 0M6.5 11l14.5 4M9 11.8V18M21 15v3M2 20h20",
    "squat": "M10 4a2 2 0 1 0 4 0a2 2 0 1 0-4 0M12 6.5l-2 5.5h6l-1 8M12 8.5h7M4 20h16",
    "pullup": "M3 3h18M8 3l2 6M16 3l-2 6M10.5 7.5a1.5 1.5 0 1 0 3 0a1.5 1.5 0 1 0-3 0M12 9.5V16M12 16l-2 5M12 16l2 5",
    "frontlever": "M2 3h9M6.5 3v6M6.5 9H22M2.4 9a1.6 1.6 0 1 0 3.2 0a1.6 1.6 0 1 0-3.2 0",
    "planche": "M2 20h20M9 20v-6M9 14h13M4 14a1.6 1.6 0 1 0 3.2 0a1.6 1.6 0 1 0-3.2 0",
    "muscleup": "M3 13h18M8.5 13l1.5-5M15.5 13L14 8M10 8h4M12 8v8M12 16l-2 5M12 16l2 5M10.4 4.5a1.6 1.6 0 1 0 3.2 0a1.6 1.6 0 1 0-3.2 0",
    "run": "M14 4a2 2 0 1 0 4 0a2 2 0 1 0-4 0M15 7l-3 5 4 3-1 6M12 12l-5 1M15 7l3 4 3-1M12 12l-2 5-5 1",
    "walk": "M11 4a2 2 0 1 0 4 0a2 2 0 1 0-4 0M13 7l-1 6 3 3v5M12 13l-3 8M13 8l-4 3M13 8l4 3",
    "burpee": "M10 3a2 2 0 1 0 4 0a2 2 0 1 0-4 0M12 6v7M12 7l-5-3M12 7l5-3M12 13l-3 6M12 13l3 6M4 22h16",
    "dumbbell": "M6.5 7v10M17.5 7v10M3.5 9.5v5M20.5 9.5v5M6.5 12h11",
    "flag": "M5 2v20M5 6h4M5 12h4M9 6v6M9 9h13",
    "bolt": "M13 2L4 14h7l-1 8 9-12h-7l1-8z",
    "flame": "M12 22c4 0 7-3 7-7 0-5-5-7-5-12-3 2-5 5-5 8-1-1-2-2-2-4-2 2-2 5-2 8 0 4 3 7 7 7z",
    "shield": "M12 3l8 3v6c0 5-4 8-8 9-4-1-8-4-8-9V6l8-3z",
    "heart": "M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z",
    "swords": "M4 4l10 10M4 4v4M4 4h4M20 4L10 14M20 4v4M20 4h-4M7 13l4 4M17 13l-4 4M5 20l3-3M19 20l-3-3",
    "grid": "M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z",
    "map": "M9 4L3 6v14l6-2 6 2 6-2V4l-6 2-6-2zM9 4v14M15 6v14",
    "user": "M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM4 21a8 8 0 0 1 16 0",
    "pin": "M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12zM12 11.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z",
    "clock": "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM12 7v5l3 2",
    "chevL": "M15 5l-7 7 7 7",
    "chevR": "M9 5l7 7-7 7",
    "check": "M5 12.5l4.5 4.5L19 7.5",
    "lock": "M6 11h12v10H6zM8.5 11V8a3.5 3.5 0 0 1 7 0v3",
    "camera": "M4 8h3l2-3h6l2 3h3v11H4zM12 16.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z",
    "share": "M12 15V3M7 8l5-5 5 5M5 13v7h14v-7",
    "route": "M6 19a2 2 0 1 0 0-4 2 2 0 0 0 0 4zM18 9a2 2 0 1 0 0-4 2 2 0 0 0 0 4zM6 15V10a3 3 0 0 1 3-3h7M18 9v5a3 3 0 0 1-3 3H8",
    "mountain": "M3 20l6-10 4 6 3-4 5 8z",
    "target": "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM12 16a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM12 12h.01",
    "star": "M12 3l2.8 5.8 6.2.9-4.5 4.4 1 6.2L12 17.4 6.5 20.3l1-6.2L3 9.7l6.2-.9z",
    "steps": "M8 3c2 0 3 2 3 5s-1 5-3 5-3-2-3-5 1-5 3-5zM6 16h4v2a2 2 0 0 1-4 0zM16 7c2 0 3 2 3 5s-1 5-3 5-3-2-3-5 1-5 3-5zM14 19h4v1a2 2 0 0 1-4 0z",
    "arrowR": "M4 12h15M13 6l6 6-6 6",
    "trophy": "M8 4h8v5a4 4 0 0 1-8 0V4zM8 6H5a3 3 0 0 0 3 4M16 6h3a3 3 0 0 1-3 4M12 13v4M8 21h8M9 17h6",
    "lsit": "M5 5v8M5 13h13M3 13h4M12 5a1.6 1.6 0 1 0 0.01 0M12 7v6",
}


def rgba(hx, a):
    hx = hx.lstrip("#")
    r, g, b = int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16)
    return "rgba(%d, %d, %d, %s)" % (r, g, b, a)


def T(_tpl, **kw):
    s = _tpl
    for k, v in kw.items():
        s = s.replace("[[" + k + "]]", str(v))
    return s


def ic(name, size=20, color="currentColor", sw=2):
    return T('<svg width="[[s]]" height="[[s]]" viewBox="0 0 24 24" aria-hidden="true" style="flex-shrink: 0; fill: none; stroke: [[c]]; stroke-width: [[w]]; stroke-linecap: round; stroke-linejoin: round"><path d="[[d]]"></path></svg>',
             s=size, c=color, w=sw, d=ICONS[name])


def token(rarity, icon, size=56, glow=False, locked=False):
    color = "#3A4463" if locked else R[rarity][1]
    h = round(size * 1.12)
    b = max(3, size // 14)
    f = ("filter: drop-shadow(0 0 %dpx %s); " % (max(8, size // 5), rgba(color, 0.75))) if glow else ""
    inner_icon = ic("lock" if locked else icon, round(size * 0.46), MUTED if locked else color, 2 if size < 90 else 1.6)
    return T('<div style="flex-shrink: 0; width: [[w]]px; height: [[h]]px; [[f]]"><div style="width: 100%; height: 100%; clip-path: [[hex]]; background: [[c]]; display: flex; align-items: center; justify-content: center"><div style="width: calc(100% - [[b2]]px); height: calc(100% - [[b3]]px); clip-path: [[hex]]; background: #10172A; display: flex; align-items: center; justify-content: center">[[i]]</div></div></div>',
             w=size, h=h, f=f, hex=HEX, c=color, b2=b * 2, b3=round(b * 2.3), i=inner_icon)


def chip(rarity, small=False):
    name, c = R[rarity]
    return T('<span style="display: inline-flex; align-items: center; padding: [[p]]; border-radius: 999px; background: [[bg]]; border: 1px solid [[bd]]; color: [[c]]; font-size: [[fs]]px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; [[D]]; white-space: nowrap">[[n]]</span>',
             p="2px 8px" if small else "4px 10px", bg=rgba(c, 0.12), bd=rgba(c, 0.6), c=c, fs=10 if small else 11, D=DISPLAY, n=name)


def bar(pct, color=LIME, h=6, track=LINE):
    return T('<div style="height: [[h]]px; border-radius: 999px; background: [[t]]; overflow: hidden"><div style="width: [[p]]%; height: 100%; border-radius: 999px; background: [[c]]"></div></div>',
             h=h, t=track, p=pct, c=color)


HELMET = """<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&amp;family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,700&amp;display=swap">
<style>
body{margin:0;background:#0B0F1A}
a{color:#C8FF3E}a:hover{color:#E4FF9A}
button{font-family:inherit}
</style>
</helmet>"""


def page(title, body, w, h, script=None, props=None):
    p = {"$preview": {"width": w, "height": h}}
    if props:
        p = dict(props, **p)
    pj = json.dumps(p, ensure_ascii=False).replace("&", "&amp;").replace("'", "&#39;")
    script = script or "renderVals() { return {}; }"
    return ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<title>" + title +
            "</title>\n<script src=\"./support.js\"></script>\n</head>\n<body>\n<x-dc>\n" + HELMET + "\n" + body +
            "\n</x-dc>\n<script type=\"text/x-dc\" data-dc-script data-props='" + pj + "'>\nclass Component extends DCLogic {\n" +
            script + "\n}\n</script>\n</body>\n</html>\n")


PHONE = "position: relative; width: 390px; height: 844px; overflow: hidden; box-sizing: border-box; background: #0B0F1A; color: #F3F5FA; font-family: 'DM Sans', system-ui, sans-serif"


def backlink(label="Back to map", href="Map.dc.html"):
    return T('<a href="[[h]]" aria-label="[[l]]" style="flex-shrink: 0; width: 44px; height: 44px; box-sizing: border-box; border-radius: 14px; background: #151B2C; border: 1px solid #2B3552; display: flex; align-items: center; justify-content: center; color: #F3F5FA; text-decoration: none">[[i]]</a>',
             h=href, l=label, i=ic("chevL", 20))


def navbar(active):
    items = [("Map", "map", "Map.dc.html"), ("FitDex", "grid", "Dex.dc.html"), ("Arena", "swords", "Battle.dc.html"), ("Profile", "user", "Profile.dc.html")]
    out = ['<nav aria-label="Main" style="position: absolute; left: 0; right: 0; bottom: 0; height: 76px; box-sizing: border-box; padding: 8px 12px 14px; background: #10152A; border-top: 1px solid #2B3552; display: flex; justify-content: space-around; align-items: center">']
    for name, icon, href in items:
        on = name == active
        out.append(T('<a href="[[h]]" style="min-width: 64px; height: 50px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; text-decoration: none; color: [[c]]; font-size: 11px; font-weight: 700">[[i]]<span>[[n]]</span></a>',
                     h=href, c=LIME if on else MUTED, i=ic(icon, 22), n=name))
    out.append("</nav>")
    return "".join(out)


files = {}

# =====================================================================
# MAP (explore) — world rotates around the player
# =====================================================================
def map_svg():
    parts = ['<svg width="2800" height="2800" viewBox="0 0 2800 2800" aria-hidden="true" style="display: block">']
    xs = [0, 900, 1400, 1950, 2800]
    ys = [0, 200, 650, 1100, 1750, 2350, 2800]
    fills = ["#1A2544", "#1D2A4C", "#18223F", "#1F2B50"]
    k = 0
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            x0, x1, y0, y1 = xs[i] + 30, xs[i + 1] - 30, ys[j] + 30, ys[j + 1] - 30
            if (xs[i], ys[j]) == (900, 650):  # park cell
                continue
            if (xs[i], ys[j]) == (1950, 1750):  # east park cell
                parts.append('<rect x="%d" y="%d" width="%d" height="%d" rx="22" style="fill: #16392F"></rect>' % (x0, y0, x1 - x0, y1 - y0))
                for (cx, cy, r) in [(2100, 1900, 26), (2250, 2000, 34), (2450, 1880, 22), (2600, 2150, 30), (2150, 2200, 24)]:
                    parts.append('<circle cx="%d" cy="%d" r="%d" style="fill: #1C4a3b"></circle>' % (cx, cy, r))
                continue
            if (xs[i], ys[j]) == (900, 1100):  # plaza
                parts.append('<rect x="1150" y="1130" width="220" height="200" rx="14" style="fill: #243258"></rect>')
                parts.append('<circle cx="1260" cy="1230" r="36" style="fill: none; stroke: #33457A; stroke-width: 6"></circle>')
                y0b = 1350
                parts.append('<rect x="930" y="1130" width="200" height="200" rx="6" style="fill: %s"></rect>' % fills[k % 4]); k += 1
                y0 = y0b
            cols = max(1, (x1 - x0) // 200)
            rows = max(1, (y1 - y0) // 220)
            gw = (x1 - x0 - (cols - 1) * 16) / cols
            gh = (y1 - y0 - (rows - 1) * 16) / rows
            for c in range(cols):
                for r_ in range(rows):
                    parts.append('<rect x="%d" y="%d" width="%d" height="%d" rx="6" style="fill: %s"></rect>' % (
                        x0 + c * (gw + 16), y0 + r_ * (gh + 16), gw, gh, fills[k % 4]))
                    k += 1
    # park (ahead-left of player)
    parts.append('<rect x="930" y="680" width="440" height="390" rx="26" style="fill: #16392F"></rect>')
    parts.append('<path d="M950 1040 C 1050 900, 1150 980, 1200 840 S 1330 720, 1360 700" style="fill: none; stroke: #235446; stroke-width: 12; stroke-linecap: round"></path>')
    for (cx, cy, r) in [(1000, 740, 26), (1080, 800, 20), (990, 900, 30), (1120, 1010, 24), (1300, 1000, 28), (1230, 760, 18), (1320, 880, 16)]:
        parts.append('<circle cx="%d" cy="%d" r="%d" style="fill: #1C4A3B"></circle>' % (cx, cy, r))
    # river
    parts.append('<path d="M0 430 C 700 330, 1300 540, 2800 380" style="fill: none; stroke: #0E2D4F; stroke-width: 110"></path>')
    parts.append('<path d="M0 430 C 700 330, 1300 540, 2800 380" style="fill: none; stroke: #123A63; stroke-width: 4; stroke-dasharray: 30 40"></path>')
    # roads
    for y in [200, 650, 1100, 1750, 2350]:
        parts.append('<rect x="0" y="%d" width="2800" height="30" style="fill: #2A3761"></rect>' % (y - 15))
    for x in [900, 1950]:
        parts.append('<rect x="%d" y="0" width="30" height="2800" style="fill: #2A3761"></rect>' % (x - 15))
    parts.append('<path d="M1950 1750 C 2250 1700, 2500 1500, 2800 1300" style="fill: none; stroke: #2A3761; stroke-width: 30"></path>')
    parts.append('<rect x="1378" y="0" width="44" height="2800" style="fill: #33437A"></rect>')
    parts.append('<line x1="1400" y1="0" x2="1400" y2="2800" style="stroke: #5C6FA8; stroke-width: 3; stroke-dasharray: 18 18"></line>')
    # walked trail + route preview
    parts.append('<line x1="1400" y1="1420" x2="1400" y2="2400" style="stroke: #C8FF3E; stroke-opacity: 0.45; stroke-width: 10; stroke-linecap: round; stroke-dasharray: 2 22"></line>')
    parts.append('<line x1="1400" y1="1380" x2="1400" y2="1075" style="stroke: #C8FF3E; stroke-opacity: 0.8; stroke-width: 8; stroke-linecap: round; stroke-dasharray: 20 16"></line>')
    # soft circle of reach
    parts.append('<circle cx="1400" cy="1400" r="260" style="fill: rgba(200, 255, 62, 0.04); stroke: rgba(200, 255, 62, 0.35); stroke-width: 3; stroke-dasharray: 10 14"></circle>')
    parts.append("</svg>")
    return "".join(parts)


map_icons_js = json.dumps({k: ICONS[k] for k in ["pushup", "squat", "pullup", "frontlever", "muscleup", "run", "burpee"]})
map_colors_js = json.dumps({k: v[1] for k, v in R.items()} | {"mission": LIME})
map_names_js = json.dumps({k: v[0] for k, v in R.items()} | {"mission": "Mission"})

map_script = """renderVals() {
const heading = Number(this.props.heading ?? 0);
const rot = -heading * Math.PI / 180;
const tilt = 50 * Math.PI / 180, d = 1800, ox = 195, oy = 600;
const ICON = """ + map_icons_js + """;
const COLOR = """ + map_colors_js + """;
const NAME = """ + map_names_js + """;
const proj = (wx, wy) => {
  const xr = wx * Math.cos(rot) - wy * Math.sin(rot);
  const yr = wx * Math.sin(rot) + wy * Math.cos(rot);
  const z = yr * Math.sin(tilt);
  const s = d / (d - z);
  return { x: Math.round(ox + xr * s), y: Math.round(oy + yr * Math.cos(tilt) * s), s: Math.round(s * 1000) / 1000 };
};
const raw = [
  { label: 'Push-ups ×20', r: 'common', icon: 'pushup', wx: -140, wy: -200 },
  { label: 'Squats ×25', r: 'common', icon: 'squat', wx: 150, wy: -260 },
  { label: 'Sprint 800 m', r: 'mission', icon: 'run', wx: 0, wy: -330 },
  { label: 'Pull-ups ×8', r: 'rare', icon: 'pullup', wx: -150, wy: -470 },
  { label: 'Burpees ×15', r: 'uncommon', icon: 'burpee', wx: 170, wy: -640 },
  { label: 'Front Lever', r: 'mythic', icon: 'frontlever', wx: -40, wy: -700 },
  { label: 'Muscle-up ×3', r: 'legendary', icon: 'muscleup', wx: 150, wy: -900 },
  { label: 'Squats ×25', r: 'common', icon: 'squat', wx: 420, wy: -300 },
  { label: 'Push-ups ×20', r: 'common', icon: 'pushup', wx: -420, wy: -380 },
  { label: 'Pull-ups ×8', r: 'rare', icon: 'pullup', wx: 380, wy: -620 },
  { label: 'Burpees ×15', r: 'uncommon', icon: 'burpee', wx: -380, wy: -760 },
  { label: 'Push-ups ×20', r: 'common', icon: 'pushup', wx: 280, wy: 60 },
  { label: 'Sprint 400 m', r: 'mission', icon: 'run', wx: 560, wy: -60 },
  { label: 'Pistol Squat', r: 'epic', icon: 'squat', wx: 820, wy: 120 },
  { label: 'Burpees ×15', r: 'uncommon', icon: 'burpee', wx: -300, wy: -40 },
  { label: 'Squats ×25', r: 'common', icon: 'squat', wx: -600, wy: 80 },
  { label: 'Pull-ups ×8', r: 'rare', icon: 'pullup', wx: -850, wy: -60 },
  { label: 'Push-ups ×20', r: 'common', icon: 'pushup', wx: -60, wy: 320 },
  { label: 'Walk 1 km', r: 'mission', icon: 'run', wx: 100, wy: 600 },
  { label: 'Muscle-up ×3', r: 'legendary', icon: 'muscleup', wx: -150, wy: 900 }
];
const spawns = raw.map((p) => {
  const q = proj(p.wx, p.wy);
  const c = COLOR[p.r];
  const big = p.r === 'mythic' || p.r === 'legendary';
  return { label: p.label, tier: NAME[p.r], color: c, icon: ICON[p.icon], x: q.x, y: q.y, s: q.s,
    glow: big ? 'drop-shadow(0 0 14px ' + c + ')' : 'none' };
}).filter((p) => p.y > 100 && p.y < 585 && p.x > 24 && p.x < 366).sort((a, b) => a.y - b.y);
const g = proj(-100, -980);
return { worldRot: -heading, spawns: spawns, gym: g, showGym: g.y > 100 && g.y < 585 && g.x > 24 && g.x < 366 };
}"""

map_body = T("""<div style="[[PHONE]]">
<div style="position: absolute; left: -1205px; top: -800px; width: 2800px; height: 2800px; border-radius: 50%; overflow: hidden; background: #131C33; transform-origin: 50% 50%; transform: perspective(1800px) rotateX(50deg) rotateZ({{worldRot}}deg)">[[SVG]]</div>
<div style="position: absolute; left: 0; top: 0; width: 390px; height: 230px; background: linear-gradient(180deg, #0B0F1A 0%, #0B0F1A 30%, rgba(11, 15, 26, 0) 100%)"></div>
<div style="position: absolute; left: 0; bottom: 0; width: 390px; height: 250px; background: linear-gradient(0deg, rgba(11, 15, 26, 0.95) 0%, rgba(11, 15, 26, 0) 100%)"></div>
<sc-if value="{{showGym}}" hint-placeholder-val="{{true}}">
<a href="Gym.dc.html" style="position: absolute; left: {{gym.x}}px; top: {{gym.y}}px; transform: translate(-50%, -100%) scale({{gym.s}}); transform-origin: 50% 100%; display: flex; flex-direction: column; align-items: center; gap: 4px; text-decoration: none; color: #F3F5FA">
<div style="padding: 4px 10px; border-radius: 10px; background: #0B0F1A; border: 1px solid #C8FF3E; display: flex; flex-direction: column; align-items: center">
<span style="font-size: 12px; font-weight: 700; white-space: nowrap">Iron Yard Gym</span>
<span style="font-size: 10px; font-weight: 700; letter-spacing: 0.1em; color: #C8FF3E; [[D]]">RAID OPEN</span>
</div>
<div style="width: 58px; height: 64px; clip-path: [[HEX]]; background: #C8FF3E; display: flex; align-items: center; justify-content: center; color: #0B0F1A">[[DB]]</div>
<div style="width: 14px; height: 38px; background: linear-gradient(180deg, #C8FF3E, rgba(200, 255, 62, 0.1))"></div>
<div style="width: 70px; height: 18px; border-radius: 50%; background: rgba(200, 255, 62, 0.25); border: 2px solid rgba(200, 255, 62, 0.7); margin-top: -10px"></div>
</a>
</sc-if>
<sc-for list="{{spawns}}" as="s" hint-placeholder-count="7">
<div style="position: absolute; left: {{s.x}}px; top: {{s.y}}px; transform: translate(-50%, -100%) scale({{s.s}}); transform-origin: 50% 100%; display: flex; flex-direction: column; align-items: center; gap: 5px">
<div style="padding: 3px 9px; border-radius: 10px; background: rgba(11, 15, 26, 0.88); border: 1px solid {{s.color}}; display: flex; flex-direction: column; align-items: center">
<span style="font-size: 12px; font-weight: 700; white-space: nowrap">{{s.label}}</span>
<span style="font-size: 9px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: {{s.color}}; [[D]]">{{s.tier}}</span>
</div>
<div style="width: 60px; height: 67px; filter: {{s.glow}}">
<div style="width: 100%; height: 100%; clip-path: [[HEX]]; background: {{s.color}}; display: flex; align-items: center; justify-content: center">
<div style="width: 52px; height: 58px; clip-path: [[HEX]]; background: #10172A; display: flex; align-items: center; justify-content: center; color: {{s.color}}">
<svg width="30" height="30" viewBox="0 0 24 24" aria-hidden="true" style="fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round"><path d="{{s.icon}}"></path></svg>
</div>
</div>
</div>
<div style="width: 46px; height: 12px; border-radius: 50%; background: {{s.color}}; opacity: 0.35; margin-top: -8px"></div>
</div>
</sc-for>
<svg width="170" height="170" viewBox="0 0 170 170" aria-hidden="true" style="position: absolute; left: 110px; top: 440px">
<defs><linearGradient id="cone" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#C8FF3E" stop-opacity="0.55"></stop><stop offset="1" stop-color="#C8FF3E" stop-opacity="0"></stop></linearGradient></defs>
<path d="M85 160 L25 10 Q85 -10 145 10 Z" style="fill: url(#cone)"></path>
</svg>
<div style="position: absolute; left: 125px; top: 577px; width: 140px; height: 46px; border-radius: 50%; border: 2px solid rgba(200, 255, 62, 0.45); background: rgba(200, 255, 62, 0.08)"></div>
<div style="position: absolute; left: 155px; top: 588px; width: 80px; height: 24px; border-radius: 50%; border: 2px solid rgba(200, 255, 62, 0.8)"></div>
<div style="position: absolute; left: 169px; top: 570px; width: 52px; height: 52px; box-sizing: border-box; border-radius: 50%; background: #C8FF3E; border: 4px solid #0B0F1A; box-shadow: 0 0 0 3px rgba(200, 255, 62, 0.5), 0 10px 24px rgba(0, 0, 0, 0.6); display: flex; align-items: center; justify-content: center">
<svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true" style="fill: #0B0F1A"><path d="M12 3l7 17-7-4-7 4z"></path></svg>
</div>
<div style="position: absolute; left: 16px; right: 16px; top: 20px; display: flex; align-items: center; gap: 10px">
<a href="Profile.dc.html" aria-label="Trainer profile, level 24" style="display: flex; align-items: center; gap: 10px; padding: 6px 12px 6px 6px; border-radius: 18px; background: rgba(21, 27, 44, 0.92); border: 1px solid #2B3552; text-decoration: none; color: #F3F5FA">
<div style="width: 40px; height: 45px; clip-path: [[HEX]]; background: #C8FF3E; display: flex; align-items: center; justify-content: center; color: #0B0F1A; font-weight: 700; font-size: 14px; [[D]]">VR</div>
<div style="display: flex; flex-direction: column; gap: 4px; width: 64px">
<span style="font-size: 13px; font-weight: 700; [[D]]">LV 24</span>
[[XPBAR]]
</div>
</a>
<a href="Street.dc.html" style="flex-grow: 1; height: 57px; box-sizing: border-box; padding: 0 12px; border-radius: 18px; background: rgba(21, 27, 44, 0.92); border: 1px solid #2B3552; display: flex; flex-direction: column; justify-content: center; gap: 2px; text-decoration: none; color: #F3F5FA">
<span style="display: flex; align-items: center; gap: 6px; font-size: 13px; font-weight: 700"><span style="width: 8px; height: 8px; border-radius: 50%; background: #C8FF3E"></span>Street Mode</span>
<span style="font-size: 11px; color: #A3ACC2">Run &amp; walk missions live</span>
</a>
<button aria-label="Compass, tap to face north" style="width: 57px; height: 57px; border-radius: 18px; background: rgba(21, 27, 44, 0.92); border: 1px solid #2B3552; display: flex; align-items: center; justify-content: center; padding: 0; cursor: pointer">
<svg width="34" height="34" viewBox="0 0 34 34" aria-hidden="true" style="transform: rotate({{worldRot}}deg)"><path d="M17 3 L22 17 L17 15 L12 17 Z" style="fill: #FF4D8D"></path><path d="M17 31 L22 17 L17 19 L12 17 Z" style="fill: #A3ACC2"></path></svg>
</button>
</div>
<div style="position: absolute; left: 16px; top: 638px; width: 176px; box-sizing: border-box; padding: 10px 12px; border-radius: 16px; background: rgba(21, 27, 44, 0.94); border: 1px solid #2B3552; display: flex; flex-direction: column; gap: 6px">
<span style="display: flex; align-items: center; gap: 6px; font-size: 10px; font-weight: 700; letter-spacing: 0.12em; color: #C8FF3E; [[D]]">[[RUNI]]ACTIVE MISSION</span>
<span style="font-size: 13px; font-weight: 700">Lap the Riverside</span>
[[MBAR]]
<span style="font-size: 11px; color: #A3ACC2">1.24 of 2.0 km</span>
</div>
<div style="position: absolute; right: 16px; top: 638px; width: 166px; box-sizing: border-box; padding: 10px 12px; border-radius: 16px; background: rgba(21, 27, 44, 0.94); border: 1px solid #2B3552; display: flex; flex-direction: column; gap: 6px">
<span style="font-size: 10px; font-weight: 700; letter-spacing: 0.12em; color: #A3ACC2; [[D]]">NEARBY</span>
[[NEARBY]]
</div>
<nav aria-label="Main" style="position: absolute; left: 0; right: 0; bottom: 14px; display: flex; justify-content: space-between; align-items: flex-end; padding: 0 40px">
<a href="Dex.dc.html" style="width: 60px; display: flex; flex-direction: column; align-items: center; gap: 4px; text-decoration: none; color: #F3F5FA; font-size: 11px; font-weight: 700"><span style="width: 52px; height: 52px; border-radius: 50%; background: #151B2C; border: 1px solid #2B3552; display: flex; align-items: center; justify-content: center">[[GRID]]</span>FitDex</a>
<a href="Encounter.dc.html" style="display: flex; flex-direction: column; align-items: center; gap: 4px; text-decoration: none; color: #0B0F1A">
<span style="width: 76px; height: 85px; clip-path: [[HEX]]; background: #C8FF3E; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2px; font-size: 12px; font-weight: 700; letter-spacing: 0.08em; [[D]]">[[BOLT]]TRAIN</span>
</a>
<a href="Battle.dc.html" style="width: 60px; display: flex; flex-direction: column; align-items: center; gap: 4px; text-decoration: none; color: #F3F5FA; font-size: 11px; font-weight: 700"><span style="width: 52px; height: 52px; border-radius: 50%; background: #151B2C; border: 1px solid #2B3552; display: flex; align-items: center; justify-content: center">[[SWORDS]]</span>Arena</a>
</nav>
</div>""",
    PHONE=PHONE, SVG=map_svg(), D=DISPLAY, HEX=HEX, DB=ic("dumbbell", 26, INK, 2.4),
    XPBAR=bar(84, LIME, 5), MBAR=bar(62, LIME, 6), RUNI=ic("run", 14, LIME),
    GRID=ic("grid", 22), SWORDS=ic("swords", 22), BOLT=ic("bolt", 24, INK, 2.2),
    NEARBY="".join(T('<div style="display: flex; align-items: center; gap: 8px">[[t]]<span style="flex-grow: 1; font-size: 12px; font-weight: 700; white-space: nowrap">[[n]]</span><span style="font-size: 11px; color: #A3ACC2">[[m]]</span></div>',
                     t=token(r, i, 20), n=n, m=m) for r, i, n, m in [("mythic", "frontlever", "Front Lever", "180 m"), ("legendary", "muscleup", "Muscle-up", "240 m"), ("rare", "pullup", "Pull-ups", "95 m")]),
)
files["Map.dc.html"] = page("Explore map", map_body, 390, 844, map_script,
                            {"heading": {"editor": "range", "min": 0, "max": 355, "step": 5, "unit": "°", "default": 0, "section": "Player"}})

# =====================================================================
# ENCOUNTER
# =====================================================================
MY = R["mythic"][1]
enc_body = T("""<div style="[[PHONE]]; display: flex; flex-direction: column">
<div style="position: absolute; left: -105px; top: 60px; width: 600px; height: 520px; background: radial-gradient(closest-side, rgba(255, 77, 141, 0.32), rgba(255, 77, 141, 0) 100%)"></div>
<div style="position: relative; display: flex; align-items: center; gap: 12px; padding: 20px 16px 0">
[[BACK]]
<div style="flex-grow: 1; display: flex; flex-direction: column">
<span style="font-size: 12px; color: #A3ACC2">Wild spawn · Riverside Park</span>
<span style="font-size: 15px; font-weight: 700">180 m away · despawns in 14:52</span>
</div>
</div>
<div style="position: relative; height: 350px; display: flex; align-items: center; justify-content: center">
<svg width="340" height="340" viewBox="0 0 340 340" aria-hidden="true" style="position: absolute; left: 25px; top: 0">
<polygon points="170,20 300,95 300,245 170,320 40,245 40,95" style="fill: none; stroke: rgba(255, 77, 141, 0.25); stroke-width: 2"></polygon>
<polygon points="170,50 274,110 274,230 170,290 66,230 66,110" style="fill: none; stroke: rgba(255, 77, 141, 0.4); stroke-width: 2; stroke-dasharray: 6 10"></polygon>
<ellipse cx="170" cy="300" rx="110" ry="20" style="fill: rgba(255, 77, 141, 0.18); stroke: rgba(255, 77, 141, 0.6); stroke-width: 2"></ellipse>
<circle cx="60" cy="70" r="3" style="fill: #FF4D8D"></circle><circle cx="290" cy="60" r="2" style="fill: #FFB229"></circle><circle cx="300" cy="200" r="3" style="fill: #FF4D8D"></circle><circle cx="40" cy="190" r="2" style="fill: #C8FF3E"></circle><circle cx="250" cy="30" r="2" style="fill: #FF4D8D"></circle>
</svg>
[[TOKEN]]
</div>
<div style="position: relative; display: flex; flex-direction: column; align-items: center; gap: 6px; padding: 0 24px">
[[CHIP]]
<h1 style="margin: 0; font-size: 40px; line-height: 1; font-weight: 700; letter-spacing: 0.01em; [[D]]">Front Lever</h1>
<span style="font-size: 15px; color: #A3ACC2">Hold 5 seconds · 3 sets</span>
</div>
<div style="position: relative; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px; padding: 18px 16px 0">
[[REWARDS]]
</div>
<div style="position: relative; margin: 10px 16px 0; padding: 12px 14px; border-radius: 16px; background: #151B2C; border: 1px solid rgba(255, 77, 141, 0.5); display: flex; align-items: center; gap: 12px">
<span style="width: 36px; height: 36px; border-radius: 12px; background: rgba(255, 77, 141, 0.14); display: flex; align-items: center; justify-content: center">[[FLAME]]</span>
<div style="display: flex; flex-direction: column; gap: 2px">
<span style="font-size: 11px; font-weight: 700; letter-spacing: 0.1em; color: #FF4D8D; [[D]]">CATCH TO UNLOCK FINISHER</span>
<span style="font-size: 15px; font-weight: 700">Horizon Cutter</span>
</div>
</div>
<div style="position: relative; margin: 8px 16px 0; display: flex; align-items: center; gap: 8px; font-size: 12px; color: #A3ACC2">[[TUCK]]<span>Not there yet? Catch the <b style="color: #4AA8FF">Tuck Lever (Rare)</b> first.</span></div>
<div style="position: absolute; left: 16px; right: 16px; bottom: 20px; display: flex; flex-direction: column; gap: 10px">
<button style="height: 56px; border: 0; border-radius: 18px; background: #C8FF3E; color: #0B0F1A; font-size: 17px; font-weight: 700; letter-spacing: 0.06em; display: flex; align-items: center; justify-content: center; gap: 10px; cursor: pointer; [[D]]">[[BOLT]]START SET 1 OF 3</button>
<span style="display: flex; align-items: center; justify-content: center; gap: 8px; font-size: 12px; color: #A3ACC2">[[CAM]]Camera form check counts your hold</span>
</div>
</div>""",
    PHONE=PHONE, BACK=backlink(), D=DISPLAY, CHIP=chip("mythic"),
    TOKEN='<div style="position: relative; margin-top: -10px">' + token("mythic", "frontlever", 176, glow=True) + "</div>",
    REWARDS="".join(T('<div style="padding: 10px; border-radius: 14px; background: #151B2C; border: 1px solid #2B3552; display: flex; flex-direction: column; align-items: center; gap: 2px"><span style="font-size: 20px; font-weight: 700; color: [[c]]; [[D]]">[[v]]</span><span style="font-size: 11px; color: #A3ACC2">[[l]]</span></div>',
                        c=c, D=DISPLAY, v=v, l=l) for v, l, c in [("+480", "Trainer XP", LIME), ("+3", "Back level", TEXT), ("+2", "Core level", TEXT)]),
    FLAME=ic("flame", 20, MY), TUCK=token("rare", "frontlever", 20), BOLT=ic("bolt", 20, INK, 2.2), CAM=ic("camera", 16, MUTED),
)
files["Encounter.dc.html"] = page("Mythic encounter", enc_body, 390, 844)

# =====================================================================
# STREET MODE
# =====================================================================
def route_svg():
    return """<svg width="356" height="150" viewBox="0 0 356 150" aria-hidden="true" style="display: block">
<rect width="356" height="150" style="fill: #131C33"></rect>
<path d="M0 118 C 90 92, 170 136, 356 96" style="fill: none; stroke: #0E2D4F; stroke-width: 26"></path>
<rect x="0" y="40" width="356" height="8" style="fill: #2A3761"></rect>
<rect x="110" y="0" width="8" height="150" style="fill: #2A3761"></rect>
<rect x="250" y="0" width="8" height="150" style="fill: #2A3761"></rect>
<rect x="124" y="54" width="118" height="36" rx="8" style="fill: #16392F"></rect>
<path d="M40 100 C 60 70, 100 64, 130 72 S 200 60, 236 76 S 300 110, 320 84" style="fill: none; stroke: #C8FF3E; stroke-width: 5; stroke-linecap: round"></path>
<path d="M320 84 C 330 70, 330 50, 300 30 S 150 22, 60 30 S 20 80, 40 100" style="fill: none; stroke: #C8FF3E; stroke-opacity: 0.55; stroke-width: 4; stroke-linecap: round; stroke-dasharray: 2 10"></path>
<circle cx="40" cy="100" r="6" style="fill: #0B0F1A; stroke: #C8FF3E; stroke-width: 3"></circle>
<circle cx="320" cy="84" r="9" style="fill: #C8FF3E; stroke: #0B0F1A; stroke-width: 3"></circle>
<circle cx="320" cy="84" r="16" style="fill: none; stroke: rgba(200, 255, 62, 0.5); stroke-width: 2"></circle>
</svg>"""


def mission_row(rarity, icon, name, req, reward):
    return T('<div style="display: flex; align-items: center; gap: 12px; padding: 10px 12px; border-radius: 16px; background: #151B2C; border: 1px solid #2B3552">[[t]]<div style="flex-grow: 1; display: flex; flex-direction: column; gap: 2px"><span style="display: flex; align-items: center; gap: 8px; font-size: 14px; font-weight: 700">[[n]] [[c]]</span><span style="font-size: 12px; color: #A3ACC2">[[r]]</span></div><span style="font-size: 12px; font-weight: 700; color: #C8FF3E; white-space: nowrap; [[D]]">[[w]]</span></div>',
             t=token(rarity, icon, 36), n=name, c=chip(rarity, True), r=req, w=reward, D=DISPLAY)


street_body = T("""<div style="[[PHONE]]; padding: 20px 16px; display: flex; flex-direction: column; gap: 12px">
<div style="display: flex; align-items: center; gap: 12px">
[[BACK]]
<div style="flex-grow: 1; display: flex; flex-direction: column">
<span style="font-size: 22px; font-weight: 700; [[D]]">Street Mode</span>
<span style="font-size: 12px; color: #A3ACC2">Outdoors · public area detected</span>
</div>
<span style="display: flex; align-items: center; gap: 6px; padding: 6px 10px; border-radius: 999px; background: rgba(200, 255, 62, 0.12); border: 1px solid rgba(200, 255, 62, 0.5); color: #C8FF3E; font-size: 11px; font-weight: 700; letter-spacing: 0.1em; [[D]]"><span style="width: 7px; height: 7px; border-radius: 50%; background: #C8FF3E"></span>LIVE</span>
</div>
<div style="padding: 10px 12px; border-radius: 14px; background: #151B2C; border: 1px solid #2B3552; display: flex; gap: 10px; align-items: center; font-size: 12px; color: #A3ACC2">[[ROUTEI]]<span>In public spaces only <b style="color: #F3F5FA">run &amp; walk missions</b> spawn. Exercise spawns return in parks, gyms and at home.</span></div>
<div style="position: relative; border-radius: 18px; overflow: hidden; border: 1px solid #2B3552">
[[ROUTE]]
<div style="position: absolute; left: 10px; top: 10px; display: flex; gap: 6px">[[UNC]]</div>
</div>
<div style="padding: 14px; border-radius: 18px; background: #151B2C; border: 1px solid #2B3552; display: flex; align-items: center; gap: 16px">
<div style="position: relative; width: 92px; height: 92px; flex-shrink: 0">
<svg width="92" height="92" viewBox="0 0 92 92" aria-hidden="true"><circle cx="46" cy="46" r="38" style="fill: none; stroke: #2B3552; stroke-width: 10"></circle><circle cx="46" cy="46" r="38" transform="rotate(-90 46 46)" style="fill: none; stroke: #C8FF3E; stroke-width: 10; stroke-linecap: round; stroke-dasharray: 238.8; stroke-dashoffset: 90.7"></circle></svg>
<span style="position: absolute; left: 0; top: 0; width: 92px; height: 92px; display: flex; align-items: center; justify-content: center; font-size: 22px; font-weight: 700; [[D]]">62%</span>
</div>
<div style="flex-grow: 1; display: flex; flex-direction: column; gap: 8px">
<span style="font-size: 15px; font-weight: 700">Lap the Riverside</span>
<span style="font-size: 26px; line-height: 1; font-weight: 700; [[D]]">1.24 <span style="font-size: 15px; color: #A3ACC2">/ 2.0 km</span></span>
<div style="display: flex; gap: 14px; font-size: 12px; color: #A3ACC2"><span><b style="color: #F3F5FA">6:12</b> /km</span><span><b style="color: #F3F5FA">07:41</b></span><span style="color: #C8FF3E; font-weight: 700">+220 XP</span></div>
</div>
</div>
<span style="font-size: 15px; font-weight: 700; margin-top: 2px">More missions nearby</span>
[[M1]]
[[M2]]
[[M3]]
<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px">
<div style="padding: 10px 12px; border-radius: 14px; background: #151B2C; border: 1px solid #2B3552; display: flex; flex-direction: column; gap: 6px"><span style="display: flex; justify-content: space-between; font-size: 12px; font-weight: 700"><span>Speed</span><span style="[[D]]">LV 11</span></span>[[B1]]</div>
<div style="padding: 10px 12px; border-radius: 14px; background: #151B2C; border: 1px solid #2B3552; display: flex; flex-direction: column; gap: 6px"><span style="display: flex; justify-content: space-between; font-size: 12px; font-weight: 700"><span>Endurance</span><span style="[[D]]">LV 14</span></span>[[B2]]</div>
</div>
<div style="display: flex; align-items: center; gap: 8px; font-size: 11px; color: #A3ACC2">[[SH]]<span>Missions pause above 25 km/h and never place targets on roadways.</span></div>
</div>""",
    PHONE=PHONE, BACK=backlink(), D=DISPLAY, ROUTEI=ic("route", 22, LIME), ROUTE=route_svg(), UNC=chip("uncommon", True),
    M1=mission_row("rare", "run", "Sidewalk Sprint", "800 m in under 4:30", "+SPD"),
    M2=mission_row("epic", "walk", "Hill Hunter", "Climb 40 m of elevation", "+END"),
    M3=mission_row("common", "walk", "Step Stack", "5,000 steps today", "+END"),
    B1=bar(70), B2=bar(40, R["rare"][1]), SH=ic("shield", 16, MUTED),
)
files["Street.dc.html"] = page("Street mode", street_body, 390, 844)

# =====================================================================
# GYM MODE
# =====================================================================
muscles = [("Chest", 12, 60, False), ("Back", 9, 82, True), ("Shoulders", 10, 35, False), ("Arms", 13, 50, False), ("Core", 15, 20, False), ("Legs", 11, 66, False)]
mtiles = "".join(
    T('<button aria-pressed="[[ap]]" style="position: relative; height: 76px; box-sizing: border-box; padding: 10px; border-radius: 14px; text-align: left; background: [[bg]]; border: [[bd]]; color: #F3F5FA; display: flex; flex-direction: column; justify-content: space-between; cursor: pointer"><span style="display: flex; justify-content: space-between; align-items: center; width: 100%"><span style="font-size: 13px; font-weight: 700">[[n]]</span>[[tag]]</span><span style="font-size: 18px; font-weight: 700; [[D]]">LV [[lv]]</span><span style="display: block; width: 100%">[[b]]</span></button>',
      ap="true" if sel else "false", bg=rgba(LIME, 0.1) if sel else PANEL, bd=("2px solid " + LIME) if sel else "1px solid #2B3552",
      n=n, lv=lv, D=DISPLAY, b=bar(p, LIME if sel else MUTED, 4),
      tag=('<span style="font-size: 9px; font-weight: 700; letter-spacing: 0.1em; color: #C8FF3E; ' + DISPLAY + '">TARGET</span>') if sel else "")
    for n, lv, p, sel in muscles)


def gym_row(rarity, icon, name, spec, state):
    if state == "done":
        right = '<span style="width: 30px; height: 30px; border-radius: 50%; background: #C8FF3E; display: flex; align-items: center; justify-content: center" aria-label="Done">' + ic("check", 18, INK, 2.6) + "</span>"
        bd = "1px solid #2B3552"
    elif state == "active":
        right = '<span style="font-size: 12px; font-weight: 700; color: #C8FF3E; ' + DISPLAY + '">SET 2/3</span>'
        bd = "2px solid " + LIME
    else:
        right = '<span style="display: flex; align-items: center; gap: 4px; font-size: 11px; font-weight: 700; color: #B07CFF; ' + DISPLAY + '">' + ic("lock", 14, R["epic"][1]) + "BOSS</span>"
        bd = "1px dashed " + rgba(R["epic"][1], 0.7)
    return T('<div style="display: flex; align-items: center; gap: 12px; padding: 9px 12px; border-radius: 16px; background: #151B2C; border: [[bd]]">[[t]]<div style="flex-grow: 1; display: flex; flex-direction: column; gap: 2px"><span style="font-size: 14px; font-weight: 700">[[n]]</span><span style="font-size: 12px; color: #A3ACC2">[[s]]</span></div>[[r]]</div>',
             bd=bd, t=token(rarity, icon, 34), n=name, s=spec, r=right)


gym_body = T("""<div style="[[PHONE]]; padding: 20px 16px; display: flex; flex-direction: column; gap: 12px">
<div style="display: flex; align-items: center; gap: 12px">
[[BACK]]
<div style="flex-grow: 1; display: flex; flex-direction: column">
<span style="font-size: 22px; font-weight: 700; [[D]]">Gym Mode</span>
<span style="display: flex; align-items: center; gap: 4px; font-size: 12px; color: #A3ACC2">[[PIN]]Iron Yard Gym · checked in</span>
</div>
<span style="display: flex; align-items: center; gap: 6px; padding: 8px 10px; border-radius: 12px; background: #151B2C; border: 1px solid #2B3552; font-size: 15px; font-weight: 700; [[D]]">[[CLK]]32:10</span>
</div>
<span style="font-size: 15px; font-weight: 700">Pick your target</span>
<div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px">[[TILES]]</div>
<div style="padding: 14px; border-radius: 18px; background: #151B2C; border: 1px solid rgba(176, 124, 255, 0.55); display: flex; flex-direction: column; gap: 10px">
<div style="display: flex; align-items: center; justify-content: space-between"><span style="font-size: 20px; font-weight: 700; [[D]]">Back Day Raid</span>[[EPIC]]</div>
<div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 6px">
<span style="height: 6px; border-radius: 999px; background: #C8FF3E"></span><span style="height: 6px; border-radius: 999px; background: #C8FF3E"></span><span style="height: 6px; border-radius: 999px; background: linear-gradient(90deg, #C8FF3E 66%, #2B3552 66%)"></span><span style="height: 6px; border-radius: 999px; background: #2B3552"></span>
</div>
<div style="display: flex; justify-content: space-between; font-size: 12px; color: #A3ACC2"><span>4 missions · up to 1,600 XP</span><span><b style="color: #C8FF3E">1,240 XP</b> earned</span></div>
</div>
[[R1]]
[[R2]]
[[R3]]
[[R4]]
<div style="display: flex; gap: 8px; margin-top: 4px">
<button style="flex-grow: 1; height: 54px; border: 0; border-radius: 16px; background: #C8FF3E; color: #0B0F1A; font-size: 15px; font-weight: 700; letter-spacing: 0.05em; cursor: pointer; [[D]]">LOG SET 3 OF 3</button>
<button style="width: 112px; height: 54px; border-radius: 16px; background: #151B2C; border: 1px solid #2B3552; color: #F3F5FA; font-size: 14px; font-weight: 700; display: flex; align-items: center; justify-content: center; gap: 6px; cursor: pointer">[[CLK2]]Rest 1:30</button>
</div>
</div>""",
    PHONE=PHONE, BACK=backlink(), D=DISPLAY, PIN=ic("pin", 14, LIME), CLK=ic("clock", 16, LIME), CLK2=ic("clock", 16, TEXT),
    TILES=mtiles, EPIC=chip("epic", True),
    R1=gym_row("rare", "pullup", "Pull-ups", "4 × 8 · bodyweight", "done"),
    R2=gym_row("common", "dumbbell", "Barbell rows", "3 × 10 · 60 kg", "done"),
    R3=gym_row("uncommon", "dumbbell", "Lat pulldown", "3 × 12 · 50 kg", "active"),
    R4=gym_row("epic", "pullup", "Archer pull-ups", "3 × 5 each side", "boss"),
)
files["Gym.dc.html"] = page("Gym mode", gym_body, 390, 844)

# =====================================================================
# FITDEX
# =====================================================================
dex = [("common", "pushup", "Push-ups", True), ("common", "squat", "Squats", True), ("common", "walk", "Lunges", True),
       ("uncommon", "burpee", "Burpees", True), ("uncommon", "dumbbell", "Dips", True), ("rare", "pullup", "Pull-ups", True),
       ("rare", "pushup", "Diamond Push-ups", True), ("epic", "squat", "Pistol Squat", True), ("epic", "lsit", "L-sit", False),
       ("legendary", "muscleup", "Muscle-up", True), ("mythic", "frontlever", "Front Lever", False), ("mythic", "planche", "Planche", False)]
cards = "".join(
    T('<div style="height: 124px; box-sizing: border-box; padding: 10px 6px; border-radius: 16px; background: #151B2C; border: 1px solid [[bd]]; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px">[[t]]<span style="font-size: 12px; font-weight: 700; text-align: center; line-height: 1.2; color: [[nc]]">[[n]]</span><span style="font-size: 9px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: [[rc]]; [[D]]">[[rn]]</span></div>',
      bd=rgba(R[r][1], 0.45) if got else "#2B3552", t=token(r, i, 48, glow=(got and r in ("legendary", "mythic")), locked=not got),
      n=n if got else "???", nc=TEXT if got else MUTED, rc=R[r][1], rn=R[r][0], D=DISPLAY)
    for r, i, n, got in dex)
filters = "".join(
    T('<span style="flex-shrink: 0; padding: 7px 12px; border-radius: 999px; font-size: 12px; font-weight: 700; background: [[bg]]; color: [[c]]; border: 1px solid [[bd]]">[[n]]</span>',
      bg=LIME if n == "All" else PANEL, c=INK if n == "All" else (R[k][1] if k else TEXT), bd=LIME if n == "All" else LINE, n=n)
    for n, k in [("All", None)] + [(v[0], k) for k, v in R.items()])
dex_body = T("""<div style="[[PHONE]]">
<div style="padding: 20px 16px 0; display: flex; flex-direction: column; gap: 12px">
<div style="display: flex; align-items: flex-end; justify-content: space-between">
<div style="display: flex; flex-direction: column; gap: 2px"><span style="font-size: 30px; line-height: 1; font-weight: 700; [[D]]">FitDex</span><span style="font-size: 13px; color: #A3ACC2">Every exercise you have caught</span></div>
<span style="font-size: 22px; font-weight: 700; [[D]]">38<span style="font-size: 14px; color: #A3ACC2"> / 120</span></span>
</div>
[[PB]]
<div style="display: flex; gap: 8px; overflow: hidden; margin-right: -16px">[[FILTERS]]</div>
<div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px">[[CARDS]]</div>
</div>
[[NAV]]
</div>""", PHONE=PHONE, D=DISPLAY, PB=bar(32), FILTERS=filters, CARDS=cards, NAV=navbar("FitDex"))
files["Dex.dc.html"] = page("FitDex collection", dex_body, 390, 844)

# =====================================================================
# PROFILE
# =====================================================================
def radar():
    cx, cy, rad = 170, 100, 72
    axes = [("STR", 72), ("END", 64), ("SPD", 58), ("CTRL", 81), ("PWR", 47)]
    ang = [(-90 + i * 72) * math.pi / 180 for i in range(5)]
    out = ['<svg width="340" height="200" viewBox="0 0 340 200" aria-label="Stat radar: strength 72, endurance 64, speed 58, control 81, power 47" role="img" style="display: block">']
    for f in (0.25, 0.5, 0.75, 1):
        pts = " ".join("%.1f,%.1f" % (cx + rad * f * math.cos(a), cy + rad * f * math.sin(a)) for a in ang)
        out.append('<polygon points="%s" style="fill: none; stroke: #2B3552; stroke-width: 1.5"></polygon>' % pts)
    for a in ang:
        out.append('<line x1="%d" y1="%d" x2="%.1f" y2="%.1f" style="stroke: #2B3552; stroke-width: 1.5"></line>' % (cx, cy, cx + rad * math.cos(a), cy + rad * math.sin(a)))
    pts = " ".join("%.1f,%.1f" % (cx + rad * v / 100 * math.cos(a), cy + rad * v / 100 * math.sin(a)) for (n, v), a in zip(axes, ang))
    out.append('<polygon points="%s" style="fill: rgba(200, 255, 62, 0.22); stroke: #C8FF3E; stroke-width: 2.5; stroke-linejoin: round"></polygon>' % pts)
    for (n, v), a in zip(axes, ang):
        x, y = cx + (rad + 26) * math.cos(a), cy + (rad + 18) * math.sin(a) + 4
        out.append('<text x="%.1f" y="%.1f" text-anchor="middle" style="fill: #A3ACC2; font-size: 11px; font-weight: 700; font-family: \'Chakra Petch\', sans-serif">%s <tspan style="fill: #F3F5FA">%d</tspan></text>' % (x, y, n, v))
    out.append("</svg>")
    return "".join(out)


mus = "".join(T('<div style="display: flex; flex-direction: column; gap: 4px"><span style="display: flex; justify-content: space-between; font-size: 12px"><span style="font-weight: 700">[[n]]</span><span style="color: #A3ACC2; [[D]]">LV [[l]]</span></span>[[b]]</div>',
                  n=n, l=l, b=bar(p, LIME, 5), D=DISPLAY) for n, l, p, _ in muscles)
fin = (T('<div style="padding: 12px; border-radius: 16px; background: #151B2C; border: 1px solid rgba(255, 178, 41, 0.6); display: flex; align-items: center; gap: 10px">[[t]]<div style="display: flex; flex-direction: column; gap: 2px"><span style="font-size: 14px; font-weight: 700; [[D]]">SKYBREAKER</span><span style="font-size: 11px; color: #A3ACC2">From Muscle-up</span></div></div>',
         t=token("legendary", "muscleup", 34, glow=True), D=DISPLAY) +
       T('<div style="padding: 12px; border-radius: 16px; background: #151B2C; border: 1px dashed #2B3552; display: flex; align-items: center; gap: 10px">[[t]]<div style="display: flex; flex-direction: column; gap: 2px"><span style="font-size: 14px; font-weight: 700; color: #A3ACC2; [[D]]">HORIZON CUTTER</span><span style="font-size: 11px; color: #A3ACC2">Catch Front Lever</span></div></div>',
         t=token("mythic", "frontlever", 34, locked=True), D=DISPLAY))
pups = "".join(T('<span style="display: flex; align-items: center; gap: 6px; padding: 8px 10px; border-radius: 12px; background: #151B2C; border: 1px solid #2B3552; font-size: 12px; font-weight: 700; white-space: nowrap">[[i]][[n]] <span style="color: #A3ACC2">×[[q]]</span></span>',
                   i=ic(i, 16, c), n=n, q=q) for i, n, q, c in [("heart", "Second Wind", 2, R["mythic"][1]), ("shield", "Iron Core", 1, R["rare"][1]), ("bolt", "Adrenaline", 3, LIME)])
prof_body = T("""<div style="[[PHONE]]">
<div style="padding: 20px 16px 0; display: flex; flex-direction: column; gap: 12px">
<div style="display: flex; align-items: center; gap: 14px">
<div style="width: 70px; height: 78px; clip-path: [[HEX]]; background: #C8FF3E; display: flex; align-items: center; justify-content: center"><div style="width: 62px; height: 69px; clip-path: [[HEX]]; background: #1D2539; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: 700; color: #C8FF3E; [[D]]">VR</div></div>
<div style="flex-grow: 1; display: flex; flex-direction: column; gap: 6px">
<span style="font-size: 22px; line-height: 1; font-weight: 700; [[D]]">VoltRunner</span>
<span style="font-size: 12px; color: #A3ACC2">Trainer level 24 · Gold II in Arena</span>
[[XP]]
<span style="font-size: 11px; color: #A3ACC2">8,420 / 10,000 XP to level 25</span>
</div>
</div>
<div style="border-radius: 18px; background: #151B2C; border: 1px solid #2B3552; padding: 8px 8px 4px; display: flex; flex-direction: column; align-items: center">
<span style="align-self: flex-start; padding: 4px 6px 0; font-size: 11px; font-weight: 700; letter-spacing: 0.12em; color: #A3ACC2; [[D]]">BATTLE STATS · FROM REAL TRAINING</span>
[[RADAR]]
</div>
<span style="font-size: 15px; font-weight: 700">Muscle levels</span>
<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: 16px; row-gap: 10px">[[MUS]]</div>
<span style="font-size: 15px; font-weight: 700">Finishers</span>
<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px">[[FIN]]</div>
<div style="display: flex; gap: 6px">[[PUPS]]</div>
</div>
[[NAV]]
</div>""", PHONE=PHONE, HEX=HEX, D=DISPLAY, XP=bar(84), RADAR=radar(), MUS=mus, FIN=fin, PUPS=pups, NAV=navbar("Profile"))
files["Profile.dc.html"] = page("Trainer profile", prof_body, 390, 844)

# =====================================================================
# BATTLE
# =====================================================================
LEG = R["legendary"][1]


def avatar(initials, size, ring):
    return T('<div style="width: [[w]]px; height: [[h]]px; clip-path: [[HEX]]; background: [[r]]; display: flex; align-items: center; justify-content: center"><div style="width: calc(100% - 8px); height: calc(100% - 9px); clip-path: [[HEX]]; background: #1D2539; display: flex; align-items: center; justify-content: center; font-size: [[fs]]px; font-weight: 700; color: [[r]]; [[D]]">[[i]]</div></div>',
             w=size, h=round(size * 1.12), HEX=HEX, r=ring, fs=round(size * 0.34), i=initials, D=DISPLAY)


moves = "".join(T('<button style="height: 66px; box-sizing: border-box; padding: 10px 12px; border-radius: 16px; background: #151B2C; border: 1px solid #2B3552; color: #F3F5FA; text-align: left; display: flex; align-items: center; gap: 10px; cursor: pointer">[[i]]<span style="display: flex; flex-direction: column; gap: 2px"><span style="font-size: 14px; font-weight: 700">[[n]]</span><span style="font-size: 11px; color: #A3ACC2">[[s]]</span></span></button>',
                  i=ic(i, 22, c), n=n, s=s) for i, n, s, c in [
    ("pushup", "Power Push", "STR · 60 dmg", R["common"][1]), ("run", "Tempo Dash", "SPD · strike first", R["rare"][1]),
    ("shield", "Core Brace", "Take 40% less", R["uncommon"][1]), ("heart", "Second Wind", "Heal 80 · ×2 left", R["mythic"][1])])
battle_body = T("""<div style="[[PHONE]]; padding: 20px 16px; display: flex; flex-direction: column; gap: 10px">
<div style="display: flex; align-items: center; gap: 12px">
[[BACK]]
<div style="flex-grow: 1; display: flex; flex-direction: column"><span style="font-size: 18px; font-weight: 700; [[D]]">Ranked Arena</span><span style="font-size: 12px; color: #A3ACC2">Round 3 · your turn · 0:18</span></div>
<span style="padding: 6px 10px; border-radius: 999px; border: 1px solid rgba(255, 178, 41, 0.6); color: #FFB229; font-size: 11px; font-weight: 700; letter-spacing: 0.1em; [[D]]">GOLD II</span>
</div>
<div style="padding: 10px 12px; border-radius: 16px; background: #151B2C; border: 1px solid #2B3552; display: flex; align-items: center; gap: 12px">
[[AV_OPP]]
<div style="flex-grow: 1; display: flex; flex-direction: column; gap: 6px">
<span style="display: flex; justify-content: space-between; font-size: 14px; font-weight: 700"><span>IronVee <span style="color: #A3ACC2; font-weight: 500">Lv 26</span></span><span style="font-size: 12px; [[D]]">210 / 500</span></span>
[[HP_OPP]]
<span style="display: flex; align-items: center; gap: 4px; font-size: 11px; color: #4AA8FF">[[SH]]Guard up · 1 turn</span>
</div>
</div>
<div style="position: relative; height: 228px; border-radius: 20px; overflow: hidden; background: #10152A; border: 1px solid #2B3552">
<svg width="356" height="228" viewBox="0 0 356 228" aria-hidden="true" style="position: absolute; left: 0; top: 0">
<ellipse cx="178" cy="150" rx="200" ry="70" style="fill: none; stroke: #1D2539; stroke-width: 2"></ellipse>
<ellipse cx="178" cy="150" rx="150" ry="50" style="fill: none; stroke: #1D2539; stroke-width: 2"></ellipse>
<ellipse cx="262" cy="104" rx="52" ry="12" style="fill: rgba(74, 168, 255, 0.18); stroke: rgba(74, 168, 255, 0.6); stroke-width: 2"></ellipse>
<ellipse cx="90" cy="206" rx="64" ry="14" style="fill: rgba(200, 255, 62, 0.16); stroke: rgba(200, 255, 62, 0.6); stroke-width: 2"></ellipse>
<path d="M140 150 L236 58" style="stroke: #FFB229; stroke-width: 5; stroke-linecap: round"></path>
<path d="M150 164 L250 70" style="stroke: #FFB229; stroke-opacity: 0.5; stroke-width: 3; stroke-linecap: round"></path>
<path d="M128 140 L220 50" style="stroke: #F3F5FA; stroke-opacity: 0.6; stroke-width: 2; stroke-linecap: round"></path>
<circle cx="244" cy="62" r="22" style="fill: none; stroke: #FFB229; stroke-width: 3"></circle>
<circle cx="244" cy="62" r="34" style="fill: none; stroke: #FFB229; stroke-opacity: 0.4; stroke-width: 2"></circle>
</svg>
<div style="position: absolute; left: 226px; top: 10px">[[AV_OPP_BIG]]</div>
<div style="position: absolute; left: 44px; top: 96px">[[AV_ME_BIG]]</div>
<div style="position: absolute; left: 150px; top: 14px; display: flex; flex-direction: column; align-items: center"><span style="font-size: 30px; line-height: 1; font-weight: 700; color: #FFB229; [[D]]">-86</span><span style="font-size: 11px; font-weight: 700; letter-spacing: 0.14em; color: #F3F5FA; [[D]]">CRITICAL</span></div>
</div>
<div style="padding: 10px 12px; border-radius: 16px; background: #151B2C; border: 1px solid #2B3552; display: flex; flex-direction: column; gap: 6px">
<span style="display: flex; justify-content: space-between; font-size: 14px; font-weight: 700"><span>VoltRunner <span style="color: #A3ACC2; font-weight: 500">You · Lv 24</span></span><span style="font-size: 12px; [[D]]">390 / 500</span></span>
[[HP_ME]]
<span style="display: flex; justify-content: space-between; font-size: 11px; font-weight: 700; letter-spacing: 0.1em; color: #FFB229; [[D]]"><span>FINISHER METER</span><span>READY</span></span>
[[FIN_M]]
</div>
<button style="height: 64px; border: 0; border-radius: 18px; background: #FFB229; color: #0B0F1A; display: flex; align-items: center; gap: 12px; padding: 0 16px; cursor: pointer; box-shadow: 0 0 24px rgba(255, 178, 41, 0.45)">
[[MUI]]
<span style="display: flex; flex-direction: column; align-items: flex-start"><span style="font-size: 20px; line-height: 1; font-weight: 700; letter-spacing: 0.04em; [[D]]">SKYBREAKER</span><span style="font-size: 12px; font-weight: 700">Finisher · 220 dmg · breaks guard</span></span>
</button>
<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px">[[MOVES]]</div>
</div>""",
    PHONE=PHONE, BACK=backlink("Leave match"), D=DISPLAY, AV_OPP=avatar("IV", 44, R["rare"][1]),
    HP_OPP=bar(42, "#FF4D8D", 8), SH=ic("shield", 13, R["rare"][1]),
    AV_OPP_BIG=avatar("IV", 76, R["rare"][1]), AV_ME_BIG=avatar("VR", 92, LIME),
    HP_ME=bar(78, LIME, 8), FIN_M=bar(100, LEG, 6), MUI=ic("muscleup", 30, INK, 2.2), MOVES=moves,
)
files["Battle.dc.html"] = page("Online battle", battle_body, 390, 844)

# =====================================================================
# FINISHER UNLOCK
# =====================================================================
rays = "".join('<line x1="195" y1="300" x2="%.1f" y2="%.1f" style="stroke: rgba(255, 178, 41, %s); stroke-width: %d; stroke-linecap: round"></line>' % (
    195 + 420 * math.cos(math.radians(a)), 300 + 420 * math.sin(math.radians(a)), "0.22" if i % 2 == 0 else "0.1", 10 if i % 2 == 0 else 4)
    for i, a in enumerate(range(0, 360, 15)))
fstats = "".join(T('<div style="padding: 12px 8px; border-radius: 14px; background: #151B2C; border: 1px solid #2B3552; display: flex; flex-direction: column; align-items: center; gap: 2px"><span style="font-size: 22px; font-weight: 700; color: [[c]]; [[D]]">[[v]]</span><span style="font-size: 11px; color: #A3ACC2">[[l]]</span></div>',
                     c=c, v=v, l=l, D=DISPLAY) for v, l, c in [("220", "Damage", LEG), ("3", "Turns to charge", TEXT), ("Breaks", "Enemy guard", TEXT)])
fin_body = T("""<div style="[[PHONE]]">
<svg width="390" height="844" viewBox="0 0 390 844" aria-hidden="true" style="position: absolute; left: 0; top: 0">[[RAYS]]</svg>
<div style="position: absolute; left: -55px; top: 50px; width: 500px; height: 500px; background: radial-gradient(closest-side, rgba(255, 178, 41, 0.35), rgba(255, 178, 41, 0) 100%)"></div>
<div style="position: absolute; left: 0; top: 0; width: 390px; height: 844px; box-sizing: border-box; padding: 20px 16px; display: flex; flex-direction: column; align-items: center">
<div style="align-self: stretch; display: flex; justify-content: flex-end"><a href="Profile.dc.html" aria-label="Close" style="width: 44px; height: 44px; border-radius: 14px; background: #151B2C; border: 1px solid #2B3552; display: flex; align-items: center; justify-content: center; color: #F3F5FA">[[X]]</a></div>
<div style="margin-top: 70px">[[TOKEN]]</div>
<span style="margin-top: 36px; font-size: 13px; font-weight: 700; letter-spacing: 0.3em; color: #FFB229; [[D]]">FINISHER UNLOCKED</span>
<h1 style="margin: 6px 0 0; font-size: 54px; line-height: 1; font-weight: 700; letter-spacing: 0.02em; [[D]]">SKYBREAKER</h1>
<span style="margin-top: 10px; display: flex; align-items: center; gap: 8px; font-size: 14px; color: #A3ACC2">Earned with 3 clean Muscle-ups [[LEGCHIP]]</span>
<div style="align-self: stretch; margin-top: 28px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px">[[STATS]]</div>
<div style="align-self: stretch; margin-top: auto; display: flex; flex-direction: column; gap: 10px">
<a href="Battle.dc.html" style="height: 56px; border-radius: 18px; background: #FFB229; color: #0B0F1A; display: flex; align-items: center; justify-content: center; gap: 10px; font-size: 17px; font-weight: 700; letter-spacing: 0.06em; text-decoration: none; [[D]]">[[SW]]EQUIP &amp; BATTLE</a>
<button style="height: 52px; border-radius: 18px; background: #151B2C; border: 1px solid #2B3552; color: #F3F5FA; display: flex; align-items: center; justify-content: center; gap: 8px; font-size: 15px; font-weight: 700; cursor: pointer">[[SHARE]]Share the rep clip</button>
<span style="display: flex; align-items: center; justify-content: center; gap: 6px; font-size: 11px; color: #A3ACC2">[[CHK]]Verified by camera rep check</span>
</div>
</div>
</div>""",
    PHONE=PHONE, RAYS=rays, X=ic("chevL", 20).replace(ICONS["chevL"], "M6 6l12 12M18 6L6 18"), D=DISPLAY,
    TOKEN=token("legendary", "muscleup", 170, glow=True), LEGCHIP=chip("legendary", True), STATS=fstats,
    SW=ic("swords", 20, INK, 2.2), SHARE=ic("share", 18), CHK=ic("check", 14, LIME),
)
files["Finisher.dc.html"] = page("Finisher unlocked", fin_body, 390, 844)

# =====================================================================
# HERO (Main)
# =====================================================================
def hexgrid():
    out = ['<svg width="760" height="900" viewBox="0 0 760 900" aria-hidden="true" style="position: absolute; right: 0; top: 0; opacity: 0.5">']
    s = 44
    for row in range(12):
        for col in range(10):
            cx = col * s * 1.73 + (s * 0.866 if row % 2 else 0) + 20
            cy = row * s * 1.5 + 10
            pts = " ".join("%.1f,%.1f" % (cx + s * math.cos(math.radians(a)), cy + s * math.sin(math.radians(a))) for a in range(-90, 270, 60))
            out.append('<polygon points="%s" style="fill: none; stroke: #1A2238; stroke-width: 1.5"></polygon>' % pts)
    out.append("</svg>")
    return "".join(out)


pillars = "".join(T('<div style="flex: 1; padding: 18px; border-radius: 20px; background: #151B2C; border: 1px solid #2B3552; display: flex; flex-direction: column; gap: 10px"><span style="width: 44px; height: 44px; border-radius: 14px; background: [[bg]]; display: flex; align-items: center; justify-content: center">[[i]]</span><span style="font-size: 20px; font-weight: 700; [[D]]">[[t]]</span><span style="font-size: 14px; line-height: 1.45; color: #A3ACC2">[[d]]</span></div>',
                      bg=rgba(c, 0.14), i=ic(i, 22, c), t=t, d=d, D=DISPLAY) for i, t, d, c in [
    ("pin", "Explore", "Exercises spawn around you. The rarer the move, the harder it is to find.", LIME),
    ("route", "Train", "Streets give run &amp; walk missions. Gyms open muscle raids.", R["rare"][1]),
    ("swords", "Battle", "Your real stats power your moves. Legendary skills unlock finishers.", R["legendary"][1])])


def phone(name, scale, left, top, rot, z):
    return T('<div style="position: absolute; left: [[l]]px; top: [[t]]px; width: [[w]]px; height: [[h]]px; transform: rotate([[r]]deg); z-index: [[z]]; border-radius: [[br]]px; box-shadow: 0 40px 80px rgba(0, 0, 0, 0.6), 0 0 0 [[bw]]px #252D44"><div style="width: 390px; height: 844px; border-radius: 48px; overflow: hidden; transform: scale([[s]]); transform-origin: 0 0"><dc-import name="[[n]]" hint-size="390px,844px"></dc-import></div></div>',
             l=left, t=top, w=round(390 * scale), h=round(844 * scale), r=rot, z=z, br=round(48 * scale), bw=8, s=scale, n=name)


hero_body = T("""<div style="position: relative; width: 1440px; height: 900px; overflow: hidden; background: #0B0F1A; color: #F3F5FA; font-family: 'DM Sans', system-ui, sans-serif">
[[GRID]]
<div style="position: absolute; left: 700px; top: 60px; width: 760px; height: 760px; background: radial-gradient(closest-side, rgba(200, 255, 62, 0.16), rgba(200, 255, 62, 0) 100%)"></div>
<div style="position: absolute; left: 96px; top: 0; width: 640px; height: 900px; display: flex; flex-direction: column; justify-content: center; gap: 28px">
<div style="display: flex; align-items: center; gap: 14px">
<div style="width: 56px; height: 63px; clip-path: [[HEX]]; background: #C8FF3E; display: flex; align-items: center; justify-content: center">[[BOLT]]</div>
<span style="font-size: 30px; font-weight: 700; letter-spacing: 0.02em; [[D]]">FitMon <span style="color: #C8FF3E">GO</span></span>
<span style="margin-left: 8px; padding: 5px 12px; border-radius: 999px; border: 1px solid #2B3552; font-size: 12px; font-weight: 700; letter-spacing: 0.12em; color: #A3ACC2; [[D]]">TSA APP PITCH</span>
</div>
<h1 style="margin: 0; font-size: 92px; line-height: 0.95; font-weight: 700; letter-spacing: -0.01em; [[D]]">Catch reps,<br>not <span style="color: #C8FF3E">monsters.</span></h1>
<p style="margin: 0; font-size: 20px; line-height: 1.5; color: #A3ACC2; max-width: 560px">A location-based fitness game. Exercises spawn around you like wild creatures. Do the reps to catch them, level up real stats and battle friends online.</p>
<div style="display: flex; gap: 14px">[[PILLARS]]</div>
</div>
[[P2]]
[[P1]]
<div style="position: absolute; left: 1010px; top: 780px; z-index: 5; display: flex; align-items: center; gap: 10px; padding: 10px 16px; border-radius: 16px; background: #151B2C; border: 1px solid rgba(255, 77, 141, 0.6); box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5)">[[MYT]]<div style="display: flex; flex-direction: column"><span style="font-size: 10px; font-weight: 700; letter-spacing: 0.14em; color: #FF4D8D; [[D]]">MYTHIC SPAWN NEARBY</span><span style="font-size: 15px; font-weight: 700">Front Lever · 180 m</span></div></div>
</div>""",
    GRID=hexgrid(), HEX=HEX, BOLT=ic("bolt", 28, INK, 2.4), D=DISPLAY, PILLARS=pillars,
    P1=phone("Map", 0.84, 800, 76, -4, 3), P2=phone("Battle", 0.72, 1100, 150, 7, 2),
    MYT=token("mythic", "frontlever", 32, glow=True),
)
files["Main.dc.html"] = page("FitMon GO pitch", hero_body, 1440, 900)

# =====================================================================
# HOW IT PLAYS
# =====================================================================
loop = []
steps = [("pin", "Explore", "Walk your city. Exercise spawns and missions appear on the map.", LIME),
         ("camera", "Catch", "Do the reps. The camera counts form, so every catch is earned.", R["rare"][1]),
         ("star", "Level up", "Each catch trains a muscle group and boosts STR, END, SPD and more.", R["epic"][1]),
         ("swords", "Battle", "Take your stats, power-ups and finishers into live online duels.", R["legendary"][1])]
for idx, (i, t, d, c) in enumerate(steps):
    loop.append(T('<div style="flex: 1; padding: 18px; border-radius: 20px; background: #151B2C; border: 1px solid #2B3552; display: flex; gap: 14px; align-items: flex-start"><span style="flex-shrink: 0; width: 48px; height: 48px; border-radius: 14px; background: [[bg]]; display: flex; align-items: center; justify-content: center">[[i]]</span><span style="display: flex; flex-direction: column; gap: 4px"><span style="font-size: 12px; font-weight: 700; letter-spacing: 0.14em; color: [[c]]; [[D]]">STEP [[n]]</span><span style="font-size: 22px; font-weight: 700; [[D]]">[[t]]</span><span style="font-size: 14px; line-height: 1.45; color: #A3ACC2">[[d]]</span></span></div>',
                  bg=rgba(c, 0.14), i=ic(i, 24, c), c=c, n=idx + 1, t=t, d=d, D=DISPLAY))
    if idx < 3:
        loop.append('<span style="flex-shrink: 0; align-self: center; color: #2B3552">' + ic("arrowR", 26, "#4A5578") + "</span>")

ladder_data = [("common", "pushup", ["Push-ups", "Squats", "Walking"], "×1"),
               ("uncommon", "burpee", ["Burpees", "Dips", "Lunges"], "×1.5"),
               ("rare", "pullup", ["Pull-ups", "Diamond push-ups", "Tuck lever"], "×2"),
               ("epic", "squat", ["Pistol squats", "L-sit", "Archer pull-ups"], "×3"),
               ("legendary", "muscleup", ["Muscle-ups", "Handstand push-ups", "Human flag"], "×5"),
               ("mythic", "frontlever", ["Front lever", "Full planche", "One-arm pull-up"], "×10")]
ladder = "".join(T('<div style="padding: 18px 16px; border-radius: 20px; background: #151B2C; border: 1px solid [[bd]]; display: flex; flex-direction: column; align-items: center; gap: 10px">[[t]]<span style="font-size: 22px; font-weight: 700; color: [[c]]; [[D]]">[[n]]</span><span style="display: flex; flex-direction: column; align-items: center; gap: 3px; font-size: 14px; color: #F3F5FA">[[ex]]</span><span style="margin-top: 2px; padding: 4px 10px; border-radius: 999px; background: [[xbg]]; color: [[c]]; font-size: 12px; font-weight: 700; [[D]]">XP [[x]]</span></div>',
                   bd=rgba(R[r][1], 0.5), t=token(r, i, 64, glow=r in ("legendary", "mythic")), c=R[r][1], n=R[r][0],
                   ex="".join("<span>%s</span>" % e for e in ex), xbg=rgba(R[r][1], 0.12), x=x, D=DISPLAY)
                 for r, i, ex, x in ladder_data)
modes = "".join(T('<div style="flex: 1; padding: 20px; border-radius: 20px; background: #151B2C; border: 1px solid #2B3552; display: flex; gap: 16px; align-items: flex-start"><span style="flex-shrink: 0; width: 52px; height: 52px; border-radius: 16px; background: [[bg]]; display: flex; align-items: center; justify-content: center">[[i]]</span><span style="display: flex; flex-direction: column; gap: 6px"><span style="font-size: 22px; font-weight: 700; [[D]]">[[t]]</span><span style="font-size: 12px; font-weight: 700; letter-spacing: 0.12em; color: [[c]]; [[D]]">[[w]]</span><span style="font-size: 14px; line-height: 1.45; color: #A3ACC2">[[d]]</span></span></div>',
                  bg=rgba(c, 0.14), i=ic(i, 26, c), t=t, w=w, c=c, d=d, D=DISPLAY) for i, t, w, d, c in [
    ("route", "Street Mode", "ON ROADS &amp; IN PUBLIC", "Only safe run and walk missions spawn here. Distance, pace and hills level up Speed and Endurance.", LIME),
    ("dumbbell", "Gym Mode", "AT A GYM OR IN A SESSION", "Pick a target muscle and run a raid of missions. Clearing sets earns points toward that muscle&#39;s level.", R["epic"][1]),
    ("swords", "Arena", "ONLINE, ANYWHERE", "Duel other trainers with moves built from your stats. Use power-ups, charge your meter, land a finisher.", R["legendary"][1])])
how_body = T("""<div style="position: relative; width: 1440px; height: 900px; overflow: hidden; box-sizing: border-box; padding: 64px 80px; background: #0B0F1A; color: #F3F5FA; font-family: 'DM Sans', system-ui, sans-serif; display: flex; flex-direction: column; gap: 22px">
<div style="display: flex; align-items: flex-end; justify-content: space-between">
<h2 style="margin: 0; font-size: 48px; line-height: 1; font-weight: 700; [[D]]">How FitMon GO plays</h2>
<span style="font-size: 16px; color: #A3ACC2">Real movement in, game progress out.</span>
</div>
<div style="display: flex; gap: 12px">[[LOOP]]</div>
<div style="display: flex; align-items: center; gap: 12px; margin-top: 6px"><span style="font-size: 14px; font-weight: 700; letter-spacing: 0.16em; color: #A3ACC2; [[D]]">RARITY LADDER</span><span style="flex-grow: 1; height: 1px; background: #2B3552"></span><span style="font-size: 14px; color: #A3ACC2">Harder skill, rarer spawn, bigger reward</span></div>
<div style="display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 12px">[[LADDER]]</div>
<div style="display: flex; align-items: center; gap: 12px; margin-top: 6px"><span style="font-size: 14px; font-weight: 700; letter-spacing: 0.16em; color: #A3ACC2; [[D]]">THREE WAYS TO PLAY</span><span style="flex-grow: 1; height: 1px; background: #2B3552"></span></div>
<div style="display: flex; gap: 12px">[[MODES]]</div>
</div>""", D=DISPLAY, LOOP="".join(loop), LADDER=ladder, MODES=modes)
files["HowItPlays.dc.html"] = page("How it plays", how_body, 1440, 900)

# =====================================================================
# canvas index
# =====================================================================
phones = [("Map.dc.html", "01 · Explore map (world rotates with you)"), ("Encounter.dc.html", "02 · Mythic encounter"),
          ("Street.dc.html", "03 · Street Mode missions"), ("Gym.dc.html", "04 · Gym Mode raid"),
          ("Dex.dc.html", "05 · FitDex collection"), ("Profile.dc.html", "06 · Trainer stats"),
          ("Battle.dc.html", "07 · Online battle"), ("Finisher.dc.html", "08 · Finisher unlocked")]
boards = {"Main.dc.html": {"x": 0, "y": 0, "w": 1440, "h": 900, "title": "Pitch hero"},
          "HowItPlays.dc.html": {"x": 1520, "y": 0, "w": 1440, "h": 900, "title": "How it plays"}}
for idx, (f, t) in enumerate(phones):
    boards[f] = {"x": idx * 470, "y": 1320, "w": 390, "h": 844, "title": t, "radius": 44, "is_interactive": True}
canvas = {"v": 3, "createdOnFiles": {"v": 1, "at": "2026-09-24T18:54:37Z"}, "title": "FitMon GO",
          "launch": {"view": "canvas"}, "pages": [], "boards": boards,
          "order": list(boards.keys()),
          "notes": {"t1": {"x": 0, "y": -300, "text": "FitMon GO: pitch visuals", "kind": "title1", "maxW": 2960},
                    "t2": {"x": 0, "y": 1060, "text": "App screens (press Play to click through)", "kind": "title1", "maxW": 3680}},
          "designSystems": []}

os.makedirs(OUT, exist_ok=True)
for name, src in files.items():
    with open(os.path.join(OUT, name), "w") as fh:
        fh.write(src)
with open(os.path.join(OUT, "canvas.json"), "w") as fh:
    json.dump(canvas, fh, indent=1, ensure_ascii=False)
print("\n".join("%s %d" % (k, len(v)) for k, v in files.items()))
