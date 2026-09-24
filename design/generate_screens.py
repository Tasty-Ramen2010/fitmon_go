"""FitMon GO pitch canvas, light "sunny park" redesign.

Look: warm cream paper, chunky rounded cards with flat bottom edges (Duolingo),
bright friendly map (Pokemon GO), soft organic blobs (Headspace), route cards
(Strava). Type: Fraunces (display serif), Nunito (rounded UI sans), Caveat
(hand-written notes).
"""
import json, math, os, re

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screens")

CREAM = "#FFF8EE"; CARD = "#FFFFFF"; SAND = "#F6EDDF"; LINE = "#EADFCF"
INK = "#22203A"; MUTED = "#6E6878"; SUN = "#FFCB47"; SUNDARK = "#E0A51A"
CORAL = "#FF7A59"; CORALTXT = "#B8431F"; SKY = "#CFEAFB"; MINT = "#D6F3E2"; PEACH = "#FFE4DA"; LILAC = "#EEE4FF"

# key: (name, mark colour [validated palette], text colour [AA on white], pastel fill)
R = {
    "common": ("Common", "#4C5B7C", "#4C5B7C", "#E9EDF5"),
    "uncommon": ("Uncommon", "#1A9A63", "#13784C", "#DBF4E7"),
    "rare": ("Rare", "#1B4AAE", "#1B4AAE", "#DFE8FB"),
    "epic": ("Epic", "#A673F7", "#7B3FD0", "#EEE4FF"),
    "legendary": ("Legendary", "#8F4A00", "#8F4A00", "#FFE9C2"),
    "mythic": ("Mythic", "#E04A7E", "#C0305F", "#FFE0EA"),
}
FD = "font-family: 'Fraunces', Georgia, serif"
FH = "font-family: 'Caveat', cursive"
CARDSTYLE = "background: #FFFFFF; border: 2px solid #EFE4D3; box-shadow: 0 3px 0 #EADFCF"
BLOBS = ["58% 42% 55% 45% / 52% 58% 42% 48%", "45% 55% 42% 58% / 55% 45% 55% 45%", "52% 48% 60% 40% / 45% 55% 45% 55%", "62% 38% 46% 54% / 48% 52% 48% 52%"]

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
    "lsit": "M5 5v8M5 13h13M3 13h4M10.4 5a1.6 1.6 0 1 0 3.2 0a1.6 1.6 0 1 0-3.2 0M12 7v6",
    "bolt": "M13 2L4 14h7l-1 8 9-12h-7l1-8z",
    "flame": "M12 22c4 0 7-3 7-7 0-5-5-7-5-12-3 2-5 5-5 8-1-1-2-2-2-4-2 2-2 5-2 8 0 4 3 7 7 7z",
    "shield": "M12 3l8 3v6c0 5-4 8-8 9-4-1-8-4-8-9V6l8-3z",
    "heart": "M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z",
    "swords": "M4 4l10 10M4 4v4M4 4h4M20 4L10 14M20 4v4M20 4h-4M7 13l4 4M17 13l-4 4M5 20l3-3M19 20l-3-3",
    "grid": "M4 7a3 3 0 0 1 3-3h1a3 3 0 0 1 3 3v1a3 3 0 0 1-3 3H7a3 3 0 0 1-3-3zM13 7a3 3 0 0 1 3-3h1a3 3 0 0 1 3 3v1a3 3 0 0 1-3 3h-1a3 3 0 0 1-3-3zM4 16a3 3 0 0 1 3-3h1a3 3 0 0 1 3 3v1a3 3 0 0 1-3 3H7a3 3 0 0 1-3-3zM13 16a3 3 0 0 1 3-3h1a3 3 0 0 1 3 3v1a3 3 0 0 1-3 3h-1a3 3 0 0 1-3-3z",
    "map": "M9 4L3 6v14l6-2 6 2 6-2V4l-6 2-6-2zM9 4v14M15 6v14",
    "user": "M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM4 21a8 8 0 0 1 16 0",
    "pin": "M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12zM12 11.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z",
    "clock": "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM12 7v5l3 2",
    "chevL": "M15 5l-7 7 7 7",
    "close": "M6 6l12 12M18 6L6 18",
    "check": "M5 12.5l4.5 4.5L19 7.5",
    "lock": "M6 11h12v10H6zM8.5 11V8a3.5 3.5 0 0 1 7 0v3",
    "camera": "M4 8h3l2-3h6l2 3h3v11H4zM12 16.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z",
    "share": "M12 15V3M7 8l5-5 5 5M5 13v7h14v-7",
    "route": "M6 19a2 2 0 1 0 0-4 2 2 0 0 0 0 4zM18 9a2 2 0 1 0 0-4 2 2 0 0 0 0 4zM6 15V10a3 3 0 0 1 3-3h7M18 9v5a3 3 0 0 1-3 3H8",
    "star": "M12 3l2.8 5.8 6.2.9-4.5 4.4 1 6.2L12 17.4 6.5 20.3l1-6.2L3 9.7l6.2-.9z",
    "handshake": "M3 11l4-4 4 2 2-2 4 1 4 3M3 11l5 5 2-1 2 2 2-1 2 1 5-5M9 13l2 2",
    "dice": "M5 4h14a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1zM8.5 8.5h.01M15.5 15.5h.01M12 12h.01M15.5 8.5h.01M8.5 15.5h.01",
    "gift": "M4 10h16v10H4zM3 7h18v3H3zM12 7v13M12 7c-2-4-6-3-5-1s5 1 5 1zM12 7c2-4 6-3 5-1s-5 1-5 1z",
    "arrowR": "M4 12h15M13 6l6 6-6 6",
}
SPARK = "M12 2c.6 4.2 1.8 5.4 6 6-4.2.6-5.4 1.8-6 6-.6-4.2-1.8-5.4-6-6 4.2-.6 5.4-1.8 6-6z"


def rgba(hx, a):
    hx = hx.lstrip("#")
    return "rgba(%d, %d, %d, %s)" % (int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16), a)


def T(_tpl, **kw):
    s = _tpl
    for k, v in kw.items():
        s = s.replace("[[" + k + "]]", str(v))
    return s


def ic(name, size=20, color="currentColor", sw=2.2):
    return T('<svg width="[[s]]" height="[[s]]" viewBox="0 0 24 24" aria-hidden="true" style="flex-shrink: 0; fill: none; stroke: [[c]]; stroke-width: [[w]]; stroke-linecap: round; stroke-linejoin: round"><path d="[[d]]"></path></svg>',
             s=size, c=color, w=sw, d=ICONS[name])


def spark(size, color, extra=""):
    return T('<svg width="[[s]]" height="[[s]]" viewBox="0 0 24 24" aria-hidden="true" style="[[x]]"><path d="[[d]]" style="fill: [[c]]"></path></svg>', s=size, c=color, d=SPARK, x=extra)


def token(rarity, icon, size=56, v=0, locked=False, sparkles=None):
    name, mark, txt, fill = R[rarity]
    if locked:
        mark, fill = "#C9BFB0", "#F3ECE1"
    b = max(2, round(size / 18))
    if sparkles is None:
        sparkles = (not locked) and rarity in ("legendary", "mythic") and size >= 40
    sp = ""
    if sparkles:
        sp = spark(round(size * 0.28), mark, "position: absolute; right: -%dpx; top: -%dpx" % (round(size * 0.08), round(size * 0.06))) + \
             spark(round(size * 0.18), mark, "position: absolute; left: -%dpx; bottom: %dpx" % (round(size * 0.06), round(size * 0.12)))
    return T('<div style="position: relative; flex-shrink: 0; width: [[w]]px; height: [[w]]px"><div style="width: 100%; height: 100%; box-sizing: border-box; border-radius: [[br]]; background: [[f]]; border: [[b]]px solid [[m]]; display: flex; align-items: center; justify-content: center">[[i]]</div>[[sp]]</div>',
             w=size, br=BLOBS[v % 4], f=fill, b=b, m=mark, i=ic("lock" if locked else icon, round(size * 0.5), "#9A8F80" if locked else mark, 2.2 if size < 90 else 1.7), sp=sp)


def pill(rarity, size=11):
    name, mark, txt, fill = R[rarity]
    return T('<span style="display: inline-flex; align-items: center; gap: 5px; padding: 3px 10px 3px 8px; border-radius: 999px; background: [[f]]; color: [[t]]; font-size: [[fs]]px; font-weight: 800; white-space: nowrap"><span style="width: 7px; height: 7px; border-radius: 50%; background: [[m]]"></span>[[n]]</span>',
             f=fill, t=txt, m=mark, fs=size, n=name)


def bar(pct, color=CORAL, h=8, track="#F1E7D8"):
    return T('<div style="height: [[h]]px; border-radius: 999px; background: [[t]]; overflow: hidden"><div style="width: [[p]]%; height: 100%; border-radius: 999px; background: [[c]]"></div></div>',
             h=h, t=track, p=pct, c=color)


def avatar(initials, size, bg, fg=INK, v=0, ring="#FFFFFF"):
    return T('<div style="flex-shrink: 0; width: [[s]]px; height: [[s]]px; box-sizing: border-box; border-radius: [[br]]; background: [[bg]]; border: [[b]]px solid [[r]]; display: flex; align-items: center; justify-content: center; color: [[fg]]; font-size: [[fs]]px; font-weight: 700; font-style: italic; [[FD]]">[[i]]</div>',
             s=size, br=BLOBS[v % 4], bg=bg, b=max(2, size // 16), r=ring, fg=fg, fs=round(size * 0.36), i=initials, FD=FD)


def btn_primary(label, icon=None, href=None, h=56, bg=SUN, edge=SUNDARK, extra=""):
    inner = (ic(icon, 20, INK, 2.4) if icon else "") + label
    style = "height: %dpx; box-sizing: border-box; border: 0; border-radius: 999px; background: %s; box-shadow: 0 5px 0 %s; color: #22203A; font-size: 17px; font-weight: 900; display: flex; align-items: center; justify-content: center; gap: 10px; cursor: pointer; text-decoration: none; %s" % (h, bg, edge, extra)
    if href:
        return '<a href="%s" style="%s">%s</a>' % (href, style, inner)
    return '<button style="%s">%s</button>' % (style, inner)


def btn_secondary(label, icon=None, href=None, h=52, extra=""):
    inner = (ic(icon, 18, INK) if icon else "") + label
    style = "height: %dpx; box-sizing: border-box; border-radius: 999px; background: #FFFFFF; border: 2px solid #EADFCF; box-shadow: 0 4px 0 #EADFCF; color: #22203A; font-size: 15px; font-weight: 800; display: flex; align-items: center; justify-content: center; gap: 8px; cursor: pointer; text-decoration: none; %s" % (h, extra)
    if href:
        return '<a href="%s" style="%s">%s</a>' % (href, style, inner)
    return '<button style="%s">%s</button>' % (style, inner)


HELMET = """<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500..800;1,9..144,500..800&amp;family=Nunito:wght@500;600;700;800;900&amp;family=Caveat:wght@600;700&amp;display=swap">
<style>
body{margin:0;background:#FFF8EE}
a{color:#B8431F}a:hover{color:#8E3014}
button{font-family:inherit}
</style>
</helmet>"""


def page(title, body, w, h, script=None, props=None):
    p = {"$preview": {"width": w, "height": h}}
    if props:
        p = dict(props, **p)
    pj = json.dumps(p, ensure_ascii=False).replace("&", "&amp;").replace("'", "&#39;")
    script = script or "renderVals() { return {}; }"
    # No decorative italics anywhere: <i> becomes a plain span, italic styles are dropped.
    body = re.sub(r'<i( style="[^"]*")?>', r'<span\1>', body).replace("</i>", "</span>").replace("font-style: italic; ", "")
    return ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<title>" + title +
            "</title>\n<script src=\"./support.js\"></script>\n</head>\n<body>\n<x-dc>\n" + HELMET + "\n" + body +
            "\n</x-dc>\n<script type=\"text/x-dc\" data-dc-script data-props='" + pj + "'>\nclass Component extends DCLogic {\n" +
            script + "\n}\n</script>\n</body>\n</html>\n")


PHONE = "position: relative; width: 390px; height: 844px; overflow: hidden; box-sizing: border-box; background: #FFF8EE; color: #22203A; font-family: 'Nunito', system-ui, sans-serif"


def backlink(label="Back to map", href="Map.dc.html", icon="chevL"):
    return T('<a href="[[h]]" aria-label="[[l]]" style="flex-shrink: 0; width: 46px; height: 46px; box-sizing: border-box; border-radius: 50%; background: #FFFFFF; border: 2px solid #EADFCF; box-shadow: 0 3px 0 #EADFCF; display: flex; align-items: center; justify-content: center; color: #22203A; text-decoration: none">[[i]]</a>',
             h=href, l=label, i=ic(icon, 20, INK, 2.6))


def header(title, sub, right="", back=None):
    return T('<div style="display: flex; align-items: center; gap: 12px">[[b]]<div style="flex-grow: 1; display: flex; flex-direction: column; gap: 1px"><span style="font-size: 26px; line-height: 1.05; font-weight: 700; [[FD]]">[[t]]</span><span style="font-size: 13px; font-weight: 600; color: #6E6878">[[s]]</span></div>[[r]]</div>',
             b=back if back is not None else backlink(), FD=FD, t=title, s=sub, r=right)


def navbar(active):
    items = [("Map", "map", "Map.dc.html"), ("FitDex", "grid", "Dex.dc.html"), ("Arena", "swords", "Battle.dc.html"), ("Profile", "user", "Profile.dc.html")]
    out = ['<nav aria-label="Main" style="position: absolute; left: 12px; right: 12px; bottom: 14px; height: 70px; box-sizing: border-box; padding: 0 8px; border-radius: 28px; ' + CARDSTYLE + '; display: flex; justify-content: space-around; align-items: center">']
    for name, icon, href in items:
        on = name == active
        out.append(T('<a href="[[h]]" style="min-width: 64px; display: flex; flex-direction: column; align-items: center; gap: 2px; text-decoration: none; color: [[c]]; font-size: 11px; font-weight: 800"><span style="width: 48px; height: 32px; border-radius: 999px; background: [[bg]]; display: flex; align-items: center; justify-content: center">[[i]]</span><span>[[n]]</span></a>',
                     h=href, c=INK if on else MUTED, bg=SUN if on else "transparent", i=ic(icon, 20), n=name))
    out.append("</nav>")
    return "".join(out)


def note(text, color=CORALTXT, size=22, extra=""):
    return '<span style="font-size: %dpx; line-height: 1; font-weight: 700; color: %s; %s; %s">%s</span>' % (size, color, FH, extra, text)


def card(inner, extra=""):
    return '<div style="border-radius: 24px; %s; %s">%s</div>' % (CARDSTYLE, extra, inner)


files = {}

# =====================================================================
# MAP
# =====================================================================
def map_svg():
    p = ['<svg width="2800" height="2800" viewBox="0 0 2800 2800" aria-hidden="true" style="display: block">']
    xs = [0, 900, 1400, 1950, 2800]
    ys = [0, 200, 650, 1100, 1750, 2350, 2800]
    fills = ["#F7EEDC", "#F3E8D3", "#F9F1E3", "#F1E6CF"]
    k = 0
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            x0, x1, y0, y1 = xs[i] + 34, xs[i + 1] - 34, ys[j] + 34, ys[j + 1] - 34
            key = (xs[i], ys[j])
            if key == (900, 650):
                continue
            if key == (1950, 1750):
                p.append('<rect x="%d" y="%d" width="%d" height="%d" rx="60" style="fill: #C9E7A9"></rect>' % (x0, y0, x1 - x0, y1 - y0))
                for (cx, cy, r) in [(2100, 1900, 34), (2250, 2010, 42), (2450, 1880, 30), (2600, 2150, 38), (2150, 2200, 30)]:
                    p.append('<circle cx="%d" cy="%d" r="%d" style="fill: #A9D98A"></circle>' % (cx, cy, r))
                continue
            if key == (900, 1100):
                p.append('<rect x="1150" y="1134" width="216" height="200" rx="40" style="fill: #F1E1C4"></rect>')
                p.append('<circle cx="1258" cy="1234" r="40" style="fill: #BCE3F7; stroke: #FFFFFF; stroke-width: 8"></circle>')
                p.append('<rect x="934" y="1134" width="196" height="200" rx="26" style="fill: %s"></rect>' % fills[k % 4]); k += 1
                y0 = 1354
            cols = max(1, (x1 - x0) // 200)
            rows = max(1, (y1 - y0) // 220)
            gw = (x1 - x0 - (cols - 1) * 18) / cols
            gh = (y1 - y0 - (rows - 1) * 18) / rows
            for c in range(cols):
                for r_ in range(rows):
                    p.append('<rect x="%d" y="%d" width="%d" height="%d" rx="26" style="fill: %s"></rect>' % (
                        x0 + c * (gw + 18), y0 + r_ * (gh + 18), gw, gh, fills[k % 4]))
                    k += 1
    p.append('<rect x="930" y="680" width="440" height="390" rx="70" style="fill: #C9E7A9"></rect>')
    p.append('<path d="M950 1040 C 1050 900, 1150 980, 1200 840 S 1330 720, 1360 700" style="fill: none; stroke: #F4EBD6; stroke-width: 16; stroke-linecap: round"></path>')
    for (cx, cy, r) in [(1000, 740, 30), (1080, 800, 24), (990, 910, 34), (1120, 1010, 28), (1300, 1000, 32), (1230, 760, 22), (1320, 880, 20)]:
        p.append('<circle cx="%d" cy="%d" r="%d" style="fill: #A9D98A"></circle>' % (cx, cy, r))
    p.append('<path d="M0 430 C 700 330, 1300 540, 2800 380" style="fill: none; stroke: #BCE3F7; stroke-width: 120; stroke-linecap: round"></path>')
    p.append('<path d="M0 430 C 700 330, 1300 540, 2800 380" style="fill: none; stroke: #DDF1FB; stroke-width: 6; stroke-dasharray: 40 60; stroke-linecap: round"></path>')
    for y in [200, 650, 1100, 1750, 2350]:
        p.append('<rect x="0" y="%d" width="2800" height="40" style="fill: #E6D9C3"></rect><rect x="0" y="%d" width="2800" height="30" style="fill: #FFFFFF"></rect>' % (y - 20, y - 15))
    for x in [900, 1950]:
        p.append('<rect x="%d" y="0" width="40" height="2800" style="fill: #E6D9C3"></rect><rect x="%d" y="0" width="30" height="2800" style="fill: #FFFFFF"></rect>' % (x - 20, x - 15))
    p.append('<path d="M1950 1750 C 2250 1700, 2500 1500, 2800 1300" style="fill: none; stroke: #E6D9C3; stroke-width: 40"></path><path d="M1950 1750 C 2250 1700, 2500 1500, 2800 1300" style="fill: none; stroke: #FFFFFF; stroke-width: 30"></path>')
    p.append('<rect x="1372" y="0" width="56" height="2800" style="fill: #E6D9C3"></rect><rect x="1378" y="0" width="44" height="2800" style="fill: #FFFFFF"></rect>')
    p.append('<line x1="1400" y1="0" x2="1400" y2="2800" style="stroke: #F2C14E; stroke-width: 4; stroke-dasharray: 22 22; stroke-linecap: round"></line>')
    p.append('<line x1="1400" y1="1430" x2="1400" y2="2400" style="stroke: #FF7A59; stroke-opacity: 0.6; stroke-width: 12; stroke-linecap: round; stroke-dasharray: 1 26"></line>')
    p.append('<line x1="1400" y1="1370" x2="1400" y2="1075" style="stroke: #FF7A59; stroke-width: 9; stroke-linecap: round; stroke-dasharray: 18 18"></line>')
    p.append('<circle cx="1400" cy="1400" r="270" style="fill: rgba(255, 122, 89, 0.06); stroke: rgba(255, 122, 89, 0.55); stroke-width: 4; stroke-dasharray: 2 18; stroke-linecap: round"></circle>')
    p.append("</svg>")
    return "".join(p)


js_rar = json.dumps({k: {"name": v[0], "mark": v[1], "text": v[2], "fill": v[3]} for k, v in R.items()} |
                    {"mission": {"name": "Mission", "mark": CORAL, "text": CORALTXT, "fill": PEACH}})
map_script = """renderVals() {
const heading = Number(this.props.heading ?? 0);
const rot = -heading * Math.PI / 180;
const tilt = 50 * Math.PI / 180, d = 1800, ox = 195, oy = 600;
const ICON = """ + json.dumps({k: ICONS[k] for k in ["pushup", "squat", "pullup", "frontlever", "muscleup", "run", "burpee"]}) + """;
const RAR = """ + js_rar + """;
const SHAPES = """ + json.dumps(BLOBS) + """;
const proj = (wx, wy) => {
  const xr = wx * Math.cos(rot) - wy * Math.sin(rot);
  const yr = wx * Math.sin(rot) + wy * Math.cos(rot);
  const z = yr * Math.sin(tilt);
  const s = d / (d - z);
  return { x: Math.round(ox + xr * s), y: Math.round(oy + yr * Math.cos(tilt) * s), s: Math.round(s * 1000) / 1000 };
};
const onScreen = (q) => q.y > 110 && q.y < 585 && q.x > 24 && q.x < 366;
const raw = [
  { label: 'Push-ups ×20', r: 'common', icon: 'pushup', wx: -140, wy: -200 },
  { label: 'Pull-ups ×8', r: 'rare', icon: 'pullup', wx: -100, wy: -420 },
  { label: 'Front Lever', r: 'mythic', icon: 'frontlever', wx: -40, wy: -720 },
  { label: 'Squats ×25', r: 'common', icon: 'squat', wx: 300, wy: 40 },
  { label: 'Pistol Squat', r: 'epic', icon: 'squat', wx: 820, wy: 120 },
  { label: 'Burpees ×15', r: 'uncommon', icon: 'burpee', wx: -300, wy: -40 },
  { label: 'Pull-ups ×8', r: 'rare', icon: 'pullup', wx: -850, wy: -60 },
  { label: 'Push-ups ×20', r: 'common', icon: 'pushup', wx: -60, wy: 320 },
  { label: 'Muscle-up ×3', r: 'legendary', icon: 'muscleup', wx: -150, wy: 900 }
];
const spawns = raw.map((p, i) => {
  const q = proj(p.wx, p.wy);
  const c = RAR[p.r];
  return { label: p.label, tier: c.name, mark: c.mark, text: c.text, fill: c.fill, shape: SHAPES[i % 4], icon: ICON[p.icon],
    x: q.x, y: q.y, s: q.s, sparkle: p.r === 'mythic' || p.r === 'legendary' };
}).filter(onScreen).sort((a, b) => a.y - b.y);
const g = proj(-180, -1000);
const t = proj(150, -560);
return { worldRot: -heading, spawns: spawns, gym: g, showGym: onScreen(g), rival: t, showRival: onScreen(t) };
}"""

map_body = T("""<div style="[[PHONE]]">
<div style="position: absolute; left: -1205px; top: -800px; width: 2800px; height: 2800px; border-radius: 50%; overflow: hidden; background: #E4F1D2; transform-origin: 50% 50%; transform: perspective(1800px) rotateX(50deg) rotateZ({{worldRot}}deg)">[[SVG]]</div>
<div style="position: absolute; left: 0; top: 0; width: 390px; height: 250px; background: linear-gradient(180deg, #BFE4FA 0%, #D3EDFB 38%, rgba(228, 241, 210, 0) 100%)"></div>
<div style="position: absolute; left: 34px; top: 108px; width: 74px; height: 24px; border-radius: 999px; background: #FFFFFF; opacity: 0.9"></div>
<div style="position: absolute; left: 54px; top: 94px; width: 34px; height: 30px; border-radius: 50%; background: #FFFFFF; opacity: 0.9"></div>
<div style="position: absolute; left: 272px; top: 122px; width: 90px; height: 26px; border-radius: 999px; background: #FFFFFF; opacity: 0.85"></div>
<div style="position: absolute; left: 298px; top: 106px; width: 40px; height: 34px; border-radius: 50%; background: #FFFFFF; opacity: 0.85"></div>
<div style="position: absolute; left: 0; bottom: 0; width: 390px; height: 260px; background: linear-gradient(0deg, rgba(255, 248, 238, 0.96) 0%, rgba(255, 248, 238, 0) 100%)"></div>
<sc-if value="{{showGym}}" hint-placeholder-val="{{true}}">
<a href="Gym.dc.html" style="position: absolute; left: {{gym.x}}px; top: {{gym.y}}px; transform: translate(-50%, -100%) scale({{gym.s}}); transform-origin: 50% 100%; display: flex; flex-direction: column; align-items: center; gap: 4px; text-decoration: none; color: #22203A">
<span style="padding: 5px 12px; border-radius: 16px; background: #FFFFFF; border: 2px solid #7B3FD0; display: flex; flex-direction: column; align-items: center; line-height: 1.1">
<span style="font-size: 12px; font-weight: 800; white-space: nowrap">Iron Yard Gym</span>
<span style="font-size: 15px; font-weight: 700; color: #7B3FD0; [[FH]]">raid open!</span>
</span>
<span style="width: 62px; height: 62px; box-sizing: border-box; border-radius: 22px; background: #EEE4FF; border: 3px solid #A673F7; display: flex; align-items: center; justify-content: center">[[DB]]</span>
<span style="width: 10px; height: 26px; border-radius: 999px; background: #A673F7"></span>
<span style="width: 60px; height: 14px; border-radius: 50%; background: rgba(34, 32, 58, 0.14); margin-top: -8px"></span>
</a>
</sc-if>
<sc-for list="{{spawns}}" as="s" hint-placeholder-count="7">
<div style="position: absolute; left: {{s.x}}px; top: {{s.y}}px; transform: translate(-50%, -100%) scale({{s.s}}); transform-origin: 50% 100%; display: flex; flex-direction: column; align-items: center; gap: 5px">
<span style="padding: 3px 10px 2px; border-radius: 14px; background: #FFFFFF; border: 2px solid {{s.mark}}; display: flex; flex-direction: column; align-items: center; line-height: 1.05">
<span style="font-size: 12px; font-weight: 800; white-space: nowrap">{{s.label}}</span>
<span style="font-size: 15px; font-weight: 700; color: {{s.text}}; [[FH]]">{{s.tier}}</span>
</span>
<span style="position: relative; width: 58px; height: 58px">
<span style="width: 58px; height: 58px; box-sizing: border-box; border-radius: {{s.shape}}; background: {{s.fill}}; border: 3px solid {{s.mark}}; display: flex; align-items: center; justify-content: center; color: {{s.mark}}">
<svg width="30" height="30" viewBox="0 0 24 24" aria-hidden="true" style="fill: none; stroke: currentColor; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round"><path d="{{s.icon}}"></path></svg>
</span>
<sc-if value="{{s.sparkle}}" hint-placeholder-val="{{false}}"><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true" style="position: absolute; right: -8px; top: -6px"><path d="[[SPARK]]" style="fill: {{s.mark}}"></path></svg></sc-if>
</span>
<span style="width: 46px; height: 12px; border-radius: 50%; background: rgba(34, 32, 58, 0.14); margin-top: -8px"></span>
</div>
</sc-for>
<sc-if value="{{showRival}}" hint-placeholder-val="{{true}}">
<a href="DuelInvite.dc.html" style="position: absolute; left: {{rival.x}}px; top: {{rival.y}}px; transform: translate(-50%, -100%) scale({{rival.s}}); transform-origin: 50% 100%; display: flex; flex-direction: column; align-items: center; gap: 4px; text-decoration: none; color: #22203A">
<span style="position: relative; padding: 5px 12px; border-radius: 16px; background: #22203A; color: #FFFFFF; font-size: 12px; font-weight: 800; white-space: nowrap">Maya wants to duel!</span>
<span style="width: 50px; height: 50px; box-sizing: border-box; border-radius: 50%; background: #FF7A59; border: 4px solid #FFFFFF; box-shadow: 0 3px 0 rgba(34, 32, 58, 0.18); display: flex; align-items: center; justify-content: center; color: #22203A; font-size: 18px; font-weight: 700; font-style: italic; [[FD]]">M</span>
<span style="width: 40px; height: 10px; border-radius: 50%; background: rgba(34, 32, 58, 0.16); margin-top: -6px"></span>
</a>
</sc-if>
<svg width="170" height="170" viewBox="0 0 170 170" aria-hidden="true" style="position: absolute; left: 110px; top: 440px">
<defs><linearGradient id="cone" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#FFCB47" stop-opacity="0.7"></stop><stop offset="1" stop-color="#FFCB47" stop-opacity="0"></stop></linearGradient></defs>
<path d="M85 160 L25 10 Q85 -10 145 10 Z" style="fill: url(#cone)"></path>
</svg>
<div style="position: absolute; left: 125px; top: 578px; width: 140px; height: 46px; box-sizing: border-box; border-radius: 50%; border: 3px solid rgba(255, 203, 71, 0.9); background: rgba(255, 203, 71, 0.18)"></div>
<div style="position: absolute; left: 167px; top: 566px; width: 56px; height: 56px; box-sizing: border-box; border-radius: 50%; background: #FFCB47; border: 5px solid #FFFFFF; box-shadow: 0 4px 0 rgba(34, 32, 58, 0.18); display: flex; align-items: center; justify-content: center">
<svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l7 17-7-4-7 4z" style="fill: #22203A; stroke: #22203A; stroke-width: 1.5; stroke-linejoin: round"></path></svg>
</div>
<div style="position: absolute; left: 14px; right: 14px; top: 18px; display: flex; align-items: center; gap: 8px">
<a href="Profile.dc.html" aria-label="Trainer profile, level 24" style="display: flex; align-items: center; gap: 8px; padding: 5px 12px 5px 5px; border-radius: 999px; [[CARD]]; text-decoration: none; color: #22203A">
[[AV]]
<span style="display: flex; flex-direction: column; gap: 4px; width: 58px"><span style="font-size: 13px; font-weight: 900">Lv 24</span>[[XPBAR]]</span>
</a>
<a href="Street.dc.html" style="flex-grow: 1; height: 56px; box-sizing: border-box; padding: 0 14px; border-radius: 999px; [[CARD]]; display: flex; flex-direction: column; justify-content: center; text-decoration: none; color: #22203A; line-height: 1.15">
<span style="display: flex; align-items: center; gap: 6px; font-size: 14px; font-weight: 900"><span style="width: 9px; height: 9px; border-radius: 50%; background: #1A9A63"></span>Street mode</span>
<span style="font-size: 12px; font-weight: 700; color: #6E6878">Run &amp; walk missions on</span>
</a>
<button aria-label="Compass, tap to face north" style="flex-shrink: 0; width: 56px; height: 56px; box-sizing: border-box; border-radius: 50%; [[CARD]]; display: flex; align-items: center; justify-content: center; padding: 0; cursor: pointer">
<svg width="32" height="32" viewBox="0 0 34 34" aria-hidden="true" style="transform: rotate({{worldRot}}deg)"><path d="M17 3 L22 17 L17 15 L12 17 Z" style="fill: #FF7A59; stroke: #FF7A59; stroke-width: 2; stroke-linejoin: round"></path><path d="M17 31 L22 17 L17 19 L12 17 Z" style="fill: #D6CCBC; stroke: #D6CCBC; stroke-width: 2; stroke-linejoin: round"></path></svg>
</button>
</div>
<div style="position: absolute; left: 34px; right: 34px; top: 662px; height: 60px; box-sizing: border-box; padding: 0 16px 0 8px; border-radius: 999px; [[CARD]]; display: flex; align-items: center; gap: 10px">
<span style="flex-shrink: 0; width: 42px; height: 42px; border-radius: 50%; background: #FFE4DA; display: flex; align-items: center; justify-content: center">[[RUNI]]</span>
<span style="flex-grow: 1; display: flex; flex-direction: column; gap: 5px"><span style="display: flex; justify-content: space-between; font-size: 14px; font-weight: 900"><span>Lap the Riverside</span><span style="font-weight: 800; color: #6E6878">1.24 / 2 km</span></span>[[MBAR]]</span>
</div>
<nav aria-label="Main" style="position: absolute; left: 0; right: 0; bottom: 16px; display: flex; justify-content: space-between; align-items: flex-end; padding: 0 40px">
<a href="Dex.dc.html" style="width: 60px; display: flex; flex-direction: column; align-items: center; gap: 4px; text-decoration: none; color: #22203A; font-size: 12px; font-weight: 800"><span style="width: 54px; height: 54px; box-sizing: border-box; border-radius: 50%; [[CARD]]; display: flex; align-items: center; justify-content: center">[[GRID]]</span>FitDex</a>
<a href="Encounter.dc.html" aria-label="Train: open the nearest spawn" style="width: 80px; height: 80px; box-sizing: border-box; border-radius: 50%; background: #FFCB47; border: 5px solid #FFFFFF; box-shadow: 0 5px 0 #E0A51A; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0; text-decoration: none; color: #22203A; font-size: 13px; font-weight: 900">[[BOLT]]Train</a>
<a href="Battle.dc.html" style="width: 60px; display: flex; flex-direction: column; align-items: center; gap: 4px; text-decoration: none; color: #22203A; font-size: 12px; font-weight: 800"><span style="width: 54px; height: 54px; box-sizing: border-box; border-radius: 50%; [[CARD]]; display: flex; align-items: center; justify-content: center">[[SWORDS]]</span>Arena</a>
</nav>
</div>""",
    PHONE=PHONE, SVG=map_svg(), FD=FD, FH=FH, CARD=CARDSTYLE, SPARK=SPARK, DB=ic("dumbbell", 28, "#7B3FD0", 2.4),
    AV=avatar("VR", 44, SUN, INK, 0), XPBAR=bar(84, CORAL, 6), MBAR=bar(62, CORAL, 8),
    GRID=ic("grid", 22, INK), SWORDS=ic("swords", 22, INK), BOLT=ic("bolt", 26, INK, 2.4),
    RUNI=ic("run", 22, CORALTXT),
)
files["Map.dc.html"] = page("Explore map", map_body, 390, 844, map_script,
                            {"heading": {"editor": "range", "min": 0, "max": 355, "step": 5, "unit": "°", "default": 0, "section": "Player"}})

# =====================================================================
# ENCOUNTER
# =====================================================================
MYT = R["mythic"]
reward = lambda v, l, c: T('<div style="padding: 12px 8px; border-radius: 20px; [[CARD]]; display: flex; flex-direction: column; align-items: center; gap: 0"><span style="font-size: 26px; font-weight: 700; color: [[c]]; [[FD]]">[[v]]</span><span style="font-size: 12px; font-weight: 700; color: #6E6878">[[l]]</span></div>', CARD=CARDSTYLE, c=c, v=v, l=l, FD=FD)
enc_body = T("""<div style="[[PHONE]]">
<div style="position: absolute; left: 30px; top: 100px; width: 330px; height: 290px; border-radius: 58% 42% 55% 45% / 52% 58% 42% 48%; background: #FFE0EA"></div>
<div style="position: absolute; left: 16px; right: 16px; top: 20px; display: flex; align-items: center; gap: 12px">
[[BACK]]
<div style="display: flex; flex-direction: column; line-height: 1.2"><span style="font-size: 13px; font-weight: 700; color: #6E6878">Wild spawn · Riverside Park</span><span style="font-size: 15px; font-weight: 900">180 m away · gone in 14:52</span></div>
</div>
<div style="position: absolute; left: 0; top: 161px; width: 390px; display: flex; justify-content: center">[[TOKEN]]</div>
<div style="position: absolute; left: 16px; right: 16px; top: 412px; display: flex; flex-direction: column; align-items: center; gap: 6px">
[[PILL]]
<h1 style="margin: 0; font-size: 46px; line-height: 1; font-weight: 700; letter-spacing: -0.01em; [[FD]]">Front Lever</h1>
<span style="font-size: 15px; font-weight: 700; color: #6E6878">Hold 5 seconds · 3 sets</span>
</div>
<div style="position: absolute; left: 16px; right: 16px; top: 528px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px">[[REWARDS]]</div>
<div style="position: absolute; left: 16px; right: 16px; top: 624px; padding: 12px 14px; box-sizing: border-box; border-radius: 22px; background: #FFE0EA; display: flex; align-items: center; gap: 12px">
<span style="flex-shrink: 0; width: 40px; height: 40px; border-radius: 50%; background: #FFFFFF; display: flex; align-items: center; justify-content: center">[[FLAME]]</span>
<span style="font-size: 14px; font-weight: 700; line-height: 1.3">Catch it to unlock the <b style="font-weight: 900; color: #C0305F">Horizon Cutter</b> finisher</span>
</div>
<div style="position: absolute; left: 16px; right: 16px; bottom: 22px; display: flex; flex-direction: column; gap: 10px">
[[CTA]]
<span style="display: flex; align-items: center; justify-content: center; gap: 6px; font-size: 12px; font-weight: 700; color: #6E6878">[[CAM]]Your camera checks the hold, so every catch is earned</span>
</div>
</div>""",
    PHONE=PHONE, BACK=backlink(), FD=FD, FH=FH, PILL=pill("mythic", 13),
    TOKEN=token("mythic", "frontlever", 168, v=1),
    REWARDS=reward("+480", "Trainer XP", CORALTXT) + reward("+3", "Back level", INK) + reward("+2", "Core level", INK),
    FLAME=ic("flame", 20, MYT[2]), CAM=ic("camera", 16, MUTED),
    CTA=btn_primary("Start set 1 of 3", "bolt"),
)
files["Encounter.dc.html"] = page("Mythic encounter", enc_body, 390, 844)

# =====================================================================
# STREET MODE
# =====================================================================
route = """<svg width="354" height="150" viewBox="0 0 354 150" aria-hidden="true" style="display: block">
<rect width="354" height="150" style="fill: #E4F1D2"></rect>
<path d="M-10 120 C 90 92, 170 138, 364 96" style="fill: none; stroke: #BCE3F7; stroke-width: 30; stroke-linecap: round"></path>
<rect x="0" y="36" width="354" height="12" style="fill: #FFFFFF"></rect>
<rect x="106" y="0" width="12" height="150" style="fill: #FFFFFF"></rect>
<rect x="246" y="0" width="12" height="150" style="fill: #FFFFFF"></rect>
<rect x="126" y="56" width="112" height="36" rx="18" style="fill: #C9E7A9"></rect>
<rect x="12" y="58" width="84" height="30" rx="14" style="fill: #F7EEDC"></rect>
<rect x="268" y="58" width="74" height="26" rx="13" style="fill: #F7EEDC"></rect>
<path d="M40 100 C 60 70, 100 64, 130 72 S 200 60, 236 76 S 300 110, 320 84" style="fill: none; stroke: #FF7A59; stroke-width: 6; stroke-linecap: round"></path>
<path d="M320 84 C 330 70, 330 50, 300 26 S 150 20, 60 26 S 20 80, 40 100" style="fill: none; stroke: #FF7A59; stroke-width: 4; stroke-linecap: round; stroke-dasharray: 1 11"></path>
<circle cx="40" cy="100" r="7" style="fill: #FFFFFF; stroke: #FF7A59; stroke-width: 3"></circle>
<circle cx="320" cy="84" r="11" style="fill: #FFCB47; stroke: #FFFFFF; stroke-width: 4"></circle>
</svg>"""


def mission_row(rarity, icon, name, req, reward, v):
    return T('<div style="display: flex; align-items: center; gap: 12px; padding: 10px 14px 10px 10px; border-radius: 22px; [[CARD]]">[[t]]<div style="flex-grow: 1; display: flex; flex-direction: column; gap: 1px"><span style="display: flex; align-items: center; gap: 8px; font-size: 15px; font-weight: 900">[[n]]</span><span style="font-size: 12px; font-weight: 700; color: #6E6878">[[r]]</span></div><span style="display: flex; flex-direction: column; align-items: flex-end; gap: 3px">[[p]]<span style="font-size: 13px; font-weight: 900; color: #B8431F">[[w]]</span></span></div>',
             CARD=CARDSTYLE, t=token(rarity, icon, 40, v=v), n=name, r=req, p=pill(rarity, 10), w=reward)


street_body = T("""<div style="[[PHONE]]; padding: 20px 16px; display: flex; flex-direction: column; gap: 12px">
[[HEAD]]
<div style="padding: 10px 14px; border-radius: 20px; background: #D6F3E2; display: flex; gap: 10px; align-items: center; font-size: 13px; font-weight: 700; line-height: 1.35; color: #22203A">[[WALK]]<span>Out in public, only <b style="font-weight: 900">run &amp; walk missions</b> spawn. Exercises come back in parks, gyms and at home.</span></div>
<div style="position: relative; border-radius: 24px; overflow: hidden; border: 2px solid #EFE4D3; box-shadow: 0 3px 0 #EADFCF">
[[ROUTE]]
<span style="position: absolute; left: 12px; top: 10px; padding: 4px 10px; border-radius: 999px; background: #FFFFFF; font-size: 17px; font-weight: 700; color: #B8431F; line-height: 1; [[FH]]">today&#39;s loop</span>
</div>
<div style="padding: 14px; border-radius: 24px; [[CARD]]; display: flex; align-items: center; gap: 16px">
<div style="position: relative; width: 96px; height: 96px; flex-shrink: 0">
<svg width="96" height="96" viewBox="0 0 96 96" aria-hidden="true"><circle cx="48" cy="48" r="39" style="fill: none; stroke: #F1E7D8; stroke-width: 12"></circle><circle cx="48" cy="48" r="39" transform="rotate(-90 48 48)" style="fill: none; stroke: #FF7A59; stroke-width: 12; stroke-linecap: round; stroke-dasharray: 245; stroke-dashoffset: 93"></circle></svg>
<span style="position: absolute; left: 0; top: 0; width: 96px; height: 96px; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: 700; [[FD]]">62%</span>
</div>
<div style="flex-grow: 1; display: flex; flex-direction: column; gap: 6px">
<span style="display: flex; align-items: center; gap: 8px; font-size: 15px; font-weight: 900">Lap the Riverside [[UNC]]</span>
<span style="font-size: 30px; line-height: 1; font-weight: 700; [[FD]]">1.24 <span style="font-size: 16px; font-weight: 600; color: #6E6878">/ 2.0 km</span></span>
<div style="display: flex; gap: 12px; font-size: 13px; font-weight: 700; color: #6E6878"><span><b style="color: #22203A">6:12</b>/km</span><span><b style="color: #22203A">07:41</b></span><span style="color: #B8431F; font-weight: 900">+220 XP</span></div>
</div>
</div>
<span style="font-size: 20px; font-weight: 700; margin-top: 2px; [[FD]]">More missions <i>nearby</i></span>
[[M1]]
[[M2]]
[[M3]]
<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px">
<div style="padding: 10px 14px; border-radius: 20px; [[CARD]]; display: flex; flex-direction: column; gap: 6px"><span style="display: flex; justify-content: space-between; font-size: 13px; font-weight: 800"><span>Speed</span><span>Lv 11</span></span>[[B1]]</div>
<div style="padding: 10px 14px; border-radius: 20px; [[CARD]]; display: flex; flex-direction: column; gap: 6px"><span style="display: flex; justify-content: space-between; font-size: 13px; font-weight: 800"><span>Endurance</span><span>Lv 14</span></span>[[B2]]</div>
</div>
<div style="display: flex; align-items: center; gap: 8px; font-size: 12px; font-weight: 700; color: #6E6878">[[SH]]<span>Missions pause above 25 km/h and never put targets on roads.</span></div>
</div>""",
    PHONE=PHONE, FD=FD, FH=FH, CARD=CARDSTYLE,
    HEAD=header("Street mode", "Outdoors · public area", '<span style="display: flex; align-items: center; gap: 6px; padding: 6px 12px; border-radius: 999px; background: #D6F3E2; color: #13784C; font-size: 13px; font-weight: 900"><span style="width: 8px; height: 8px; border-radius: 50%; background: #1A9A63"></span>Live</span>'),
    WALK=ic("walk", 24, "#13784C"), ROUTE=route, UNC=pill("uncommon", 10),
    M1=mission_row("rare", "run", "Sidewalk Sprint", "800 m in under 4:30", "+Speed", 0),
    M2=mission_row("epic", "walk", "Hill Hunter", "Climb 40 m of hills", "+Endurance", 1),
    M3=mission_row("common", "walk", "Step Stack", "5,000 steps today", "+Endurance", 2),
    B1=bar(70), B2=bar(40, R["rare"][1]), SH=ic("shield", 16, MUTED),
)
files["Street.dc.html"] = page("Street mode", street_body, 390, 844)

# =====================================================================
# GYM MODE
# =====================================================================
muscles = [("Chest", 12, 60, False), ("Back", 9, 82, True), ("Shoulders", 10, 35, False), ("Arms", 13, 50, False), ("Core", 15, 20, False), ("Legs", 11, 66, False)]
mtiles = "".join(
    T('<button aria-pressed="[[ap]]" style="height: 80px; box-sizing: border-box; padding: 10px 12px; border-radius: 22px; text-align: left; background: [[bg]]; border: [[bd]]; box-shadow: 0 3px 0 [[sh]]; color: #22203A; display: flex; flex-direction: column; justify-content: space-between; cursor: pointer"><span style="display: flex; justify-content: space-between; align-items: center; width: 100%"><span style="font-size: 14px; font-weight: 900">[[n]]</span>[[tag]]</span><span style="font-size: 12px; font-weight: 800; color: #6E6878">Level [[lv]]</span><span style="display: block; width: 100%">[[b]]</span></button>',
      ap="true" if sel else "false", bg="#FFF1CC" if sel else CARD, bd=("3px solid " + SUN) if sel else "2px solid #EFE4D3", sh=SUNDARK if sel else LINE,
      n=n, lv=lv, b=bar(p, CORAL if sel else "#CFC3B1", 6),
      tag=('<span style="font-size: 16px; font-weight: 700; color: #B8431F; line-height: 1; ' + FH + '">target</span>') if sel else "")
    for n, lv, p, sel in muscles)


def gym_row(rarity, icon, name, spec, state, v):
    if state == "done":
        right = '<span style="width: 32px; height: 32px; border-radius: 50%; background: #1A9A63; display: flex; align-items: center; justify-content: center" aria-label="Done">' + ic("check", 18, "#FFFFFF", 3) + "</span>"
        box = CARDSTYLE
    elif state == "active":
        right = '<span style="padding: 4px 10px; border-radius: 999px; background: #FFCB47; font-size: 12px; font-weight: 900">Set 2 of 3</span>'
        box = "background: #FFFFFF; border: 3px solid #FFCB47; box-shadow: 0 3px 0 #E0A51A"
    else:
        right = '<span style="display: flex; align-items: center; gap: 4px; padding: 4px 10px; border-radius: 999px; background: #EEE4FF; font-size: 12px; font-weight: 900; color: #7B3FD0">' + ic("lock", 13, "#7B3FD0") + "Boss</span>"
        box = "background: #FFFFFF; border: 2px dashed #A673F7"
    return T('<div style="display: flex; align-items: center; gap: 12px; padding: 9px 12px 9px 9px; border-radius: 22px; [[box]]">[[t]]<div style="flex-grow: 1; display: flex; flex-direction: column; gap: 1px"><span style="font-size: 15px; font-weight: 900">[[n]]</span><span style="font-size: 12px; font-weight: 700; color: #6E6878">[[s]]</span></div>[[r]]</div>',
             box=box, t=token(rarity, icon, 38, v=v), n=name, s=spec, r=right)


gym_body = T("""<div style="[[PHONE]]; padding: 20px 16px; display: flex; flex-direction: column; gap: 12px">
[[HEAD]]
<div style="display: flex; align-items: baseline; justify-content: space-between"><span style="font-size: 20px; font-weight: 700; [[FD]]">Pick your <i>target</i></span><span style="font-size: 18px; font-weight: 700; color: #6E6878; [[FH]]">tap a muscle</span></div>
<div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px">[[TILES]]</div>
<div style="padding: 14px 16px; border-radius: 26px; background: #EEE4FF; display: flex; flex-direction: column; gap: 10px">
<div style="display: flex; align-items: center; justify-content: space-between"><span style="font-size: 24px; font-weight: 700; [[FD]]">Back Day <i>Raid</i></span>[[EPIC]]</div>
<div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 6px">
<span style="height: 10px; border-radius: 999px; background: #A673F7"></span><span style="height: 10px; border-radius: 999px; background: #A673F7"></span><span style="height: 10px; border-radius: 999px; background: linear-gradient(90deg, #A673F7 66%, #FFFFFF 66%)"></span><span style="height: 10px; border-radius: 999px; background: #FFFFFF"></span>
</div>
<div style="display: flex; justify-content: space-between; font-size: 13px; font-weight: 700; color: #4A4458"><span>4 missions · up to 1,600 XP</span><span><b style="font-weight: 900; color: #22203A">1,240 XP</b> so far</span></div>
</div>
[[R1]]
[[R2]]
[[R3]]
[[R4]]
<div style="display: flex; gap: 10px; margin-top: 2px">
[[LOG]]
[[REST]]
</div>
</div>""",
    PHONE=PHONE, FD=FD, FH=FH,
    HEAD=header("Gym mode", "Iron Yard Gym · checked in", '<span style="display: flex; align-items: center; gap: 6px; padding: 8px 12px; border-radius: 999px; ' + CARDSTYLE + '; font-size: 16px; font-weight: 700; ' + FD + '">' + ic("clock", 16, CORALTXT) + "32:10</span>"),
    TILES=mtiles, EPIC=pill("epic", 11),
    R1=gym_row("rare", "pullup", "Pull-ups", "4 × 8 · bodyweight", "done", 0),
    R2=gym_row("common", "dumbbell", "Barbell rows", "3 × 10 · 60 kg", "done", 1),
    R3=gym_row("uncommon", "dumbbell", "Lat pulldown", "3 × 12 · 50 kg", "active", 2),
    R4=gym_row("epic", "pullup", "Archer pull-ups", "3 × 5 each side", "boss", 3),
    LOG=btn_primary("Log set 3 of 3", None, None, 54, extra="flex-grow: 1"),
    REST=btn_secondary("Rest 1:30", "clock", None, 54, extra="width: 124px"),
)
files["Gym.dc.html"] = page("Gym mode", gym_body, 390, 844)

# =====================================================================
# FITDEX
# =====================================================================
# What this trainer actually owns: a pyramid, rarest on top.
owned = [
    ("mythic", [("planche", "Planche")]),
    ("legendary", [("muscleup", "Muscle-up")]),
    ("epic", [("squat", "Pistol Squat"), ("lsit", "L-sit")]),
    ("rare", [("pullup", "Pull-ups"), ("pushup", "Diamond Push-ups"), ("frontlever", "Tuck Lever")]),
    ("uncommon", [("burpee", "Burpees"), ("dumbbell", "Dips"), ("squat", "Jump Squats"), ("walk", "Step-ups")]),
    ("common", [("pushup", "Push-ups"), ("squat", "Squats"), ("walk", "Lunges"), ("pushup", "Plank"), ("burpee", "Sit-ups")]),
]
tiers = []
k = 0
for r, items in owned:
    cells = []
    for icon, name in items:
        badge = ('<span style="position: absolute; right: -6px; top: -6px; padding: 1px 6px; border-radius: 999px; background: #FF7A59; color: #22203A; font-size: 10px; font-weight: 900">new</span>') if name == "Burpees" else ""
        cells.append(T('<div style="width: 66px; display: flex; flex-direction: column; align-items: center; gap: 4px"><span style="position: relative">[[t]][[b]]</span><span style="font-size: 11px; font-weight: 800; line-height: 1.1; text-align: center">[[n]]</span></div>',
                       t=token(r, icon, 40, v=k, sparkles=False), b=badge, n=name))
        k += 1
    tiers.append(T('<div style="display: flex; flex-direction: column; align-items: center; gap: 5px"><span style="display: flex; align-items: center; gap: 6px">[[p]]<span style="font-size: 12px; font-weight: 800; color: #6E6878">[[c]] caught</span></span><div style="display: flex; justify-content: center; gap: 4px">[[cells]]</div></div>',
                   p=pill(r, 11), c=len(items), cells="".join(cells)))
dex_body = T("""<div style="[[PHONE]]">
<div style="position: absolute; right: -40px; top: -50px; width: 190px; height: 170px; border-radius: 58% 42% 55% 45% / 52% 58% 42% 48%; background: #FFE9C2"></div>
<div style="position: relative; padding: 22px 16px 0; display: flex; flex-direction: column; gap: 16px">
<div style="display: flex; align-items: flex-end; justify-content: space-between">
<div style="display: flex; flex-direction: column; gap: 2px"><span style="font-size: 38px; line-height: 1; font-weight: 700; [[FD]]">FitDex</span><span style="font-size: 14px; font-weight: 700; color: #6E6878">Your collection, rarest at the top</span></div>
<span style="display: flex; flex-direction: column; align-items: flex-end; line-height: 1"><span style="font-size: 34px; font-weight: 700; [[FD]]">16</span><span style="font-size: 12px; font-weight: 800; color: #6E6878">FitMon</span></span>
</div>
<div style="padding: 14px 8px 16px; border-radius: 28px; [[CARD]]; display: flex; flex-direction: column; gap: 10px">[[TIERS]]</div>
</div>
[[NAV]]
</div>""", PHONE=PHONE, FD=FD, CARD=CARDSTYLE, TIERS="".join(tiers), NAV=navbar("FitDex"))
files["Dex.dc.html"] = page("FitDex collection", dex_body, 390, 844)

# =====================================================================
# PROFILE
# =====================================================================
def radar():
    cx, cy, rad = 170, 98, 70
    axes = [("Strength", 72), ("Endurance", 64), ("Speed", 58), ("Control", 81), ("Power", 47)]
    ang = [(-90 + i * 72) * math.pi / 180 for i in range(5)]
    o = ['<svg width="340" height="196" viewBox="0 0 340 196" role="img" aria-label="Battle stats: strength 72, endurance 64, speed 58, control 81, power 47" style="display: block">']
    for f in (0.33, 0.66, 1):
        pts = " ".join("%.1f,%.1f" % (cx + rad * f * math.cos(a), cy + rad * f * math.sin(a)) for a in ang)
        o.append('<polygon points="%s" style="fill: none; stroke: #EFE4D3; stroke-width: 2; stroke-linejoin: round"></polygon>' % pts)
    pts = " ".join("%.1f,%.1f" % (cx + rad * v / 100 * math.cos(a), cy + rad * v / 100 * math.sin(a)) for (n, v), a in zip(axes, ang))
    o.append('<polygon points="%s" style="fill: rgba(255, 122, 89, 0.22); stroke: #FF7A59; stroke-width: 3; stroke-linejoin: round"></polygon>' % pts)
    for (n, v), a in zip(axes, ang):
        o.append('<circle cx="%.1f" cy="%.1f" r="4.5" style="fill: #FF7A59; stroke: #FFFFFF; stroke-width: 2"></circle>' % (cx + rad * v / 100 * math.cos(a), cy + rad * v / 100 * math.sin(a)))
        x, y = cx + (rad + 34) * math.cos(a), cy + (rad + 16) * math.sin(a) + 4
        o.append('<text x="%.1f" y="%.1f" text-anchor="middle" style="fill: #6E6878; font-size: 12px; font-weight: 800; font-family: Nunito, sans-serif">%s <tspan style="fill: #22203A; font-weight: 900">%d</tspan></text>' % (x, y, n, v))
    o.append("</svg>")
    return "".join(o)


mus = "".join(T('<div style="display: flex; flex-direction: column; gap: 4px"><span style="display: flex; justify-content: space-between; font-size: 13px; font-weight: 800"><span>[[n]]</span><span style="color: #6E6878">Lv [[l]]</span></span>[[b]]</div>',
                  n=n, l=l, b=bar(p, CORAL, 7)) for n, l, p, _ in muscles)
fin = (T('<div style="padding: 10px 12px 10px 10px; border-radius: 22px; background: #FFE9C2; display: flex; align-items: center; gap: 10px">[[t]]<div style="display: flex; flex-direction: column; line-height: 1.15"><span style="font-size: 16px; font-weight: 700; font-style: italic; [[FD]]">Skybreaker</span><span style="font-size: 12px; font-weight: 700; color: #6E5A3A">from Muscle-up</span></div></div>',
         t=token("legendary", "muscleup", 38, v=2, sparkles=False), FD=FD) +
       T('<div style="padding: 10px 12px 10px 10px; border-radius: 22px; border: 2px dashed #D9CCB8; display: flex; align-items: center; gap: 10px">[[t]]<div style="display: flex; flex-direction: column; line-height: 1.15"><span style="font-size: 16px; font-weight: 700; font-style: italic; color: #6E6878; [[FD]]">Horizon Cutter</span><span style="font-size: 12px; font-weight: 700; color: #6E6878">catch Front Lever</span></div></div>',
         t=token("mythic", "frontlever", 38, v=3, locked=True), FD=FD))
pups = "".join(T('<span style="display: flex; align-items: center; gap: 6px; padding: 7px 12px 7px 8px; border-radius: 999px; background: [[bg]]; font-size: 13px; font-weight: 800; white-space: nowrap">[[i]][[n]] <span style="color: #6E6878">×[[q]]</span></span>',
                   bg=bg, i=ic(i, 16, c), n=n, q=q) for i, n, q, c, bg in [("heart", "Second Wind", 2, R["mythic"][2], R["mythic"][3]), ("shield", "Iron Core", 1, R["rare"][2], R["rare"][3]), ("bolt", "Adrenaline", 3, CORALTXT, PEACH)])
prof_body = T("""<div style="[[PHONE]]">
<div style="position: absolute; left: -60px; top: -70px; width: 260px; height: 220px; border-radius: 45% 55% 42% 58% / 55% 45% 55% 45%; background: #FFE4DA"></div>
<div style="position: relative; padding: 24px 16px 0; display: flex; flex-direction: column; gap: 12px">
<div style="display: flex; align-items: center; gap: 14px">
[[AV]]
<div style="flex-grow: 1; display: flex; flex-direction: column; gap: 5px">
<span style="font-size: 28px; line-height: 1; font-weight: 700; [[FD]]">Volt<i>Runner</i></span>
<span style="font-size: 13px; font-weight: 700; color: #6E6878">Trainer level 24 · Gold II in the Arena</span>
[[XP]]
<span style="font-size: 12px; font-weight: 700; color: #6E6878">8,420 / 10,000 XP to level 25</span>
</div>
</div>
<div style="border-radius: 26px; [[CARD]]; padding: 10px 8px 4px; display: flex; flex-direction: column; align-items: center">
<span style="align-self: flex-start; padding: 0 8px; font-size: 19px; font-weight: 700; color: #B8431F; line-height: 1; [[FH]]">battle stats, earned by real reps</span>
[[RADAR]]
</div>
<span style="font-size: 20px; font-weight: 700; [[FD]]">Muscle <i>levels</i></span>
<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: 18px; row-gap: 10px">[[MUS]]</div>
<span style="font-size: 20px; font-weight: 700; [[FD]]">Finishers</span>
<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px">[[FIN]]</div>
<div style="display: flex; gap: 6px">[[PUPS]]</div>
</div>
[[NAV]]
</div>""", PHONE=PHONE, FD=FD, FH=FH, CARD=CARDSTYLE, AV=avatar("VR", 76, SUN, INK, 1), XP=bar(84, CORAL, 8), RADAR=radar(), MUS=mus, FIN=fin, PUPS=pups, NAV=navbar("Profile"))
files["Profile.dc.html"] = page("Trainer profile", prof_body, 390, 844)

# =====================================================================
# ONLINE BATTLE
# =====================================================================
LEG = R["legendary"]


def fighter(rarity, icon, size, look, v=0):
    """A FitMon as a character: blob body, eyes looking at the opponent, cheeks, smile, move emblem."""
    name, mark, txt, fill = R[rarity]
    e = round(size * 0.2)
    p_ = round(e * 0.55)
    eyes = ""
    for cx in (0.36, 0.64):
        x = round(size * cx - e / 2 + look * size * 0.05)
        eyes += ('<span style="position: absolute; left: %dpx; top: %dpx; width: %dpx; height: %dpx; border-radius: 50%%; background: #FFFFFF; border: 2px solid %s; box-sizing: border-box; display: flex; align-items: center; justify-content: center">'
                 '<span style="width: %dpx; height: %dpx; border-radius: 50%%; background: #22203A; transform: translate(%dpx, 1px)"></span></span>') % (x, round(size * 0.22), e, e, mark, p_, p_, round(look * e * 0.16))
        eyes += '<span style="position: absolute; left: %dpx; top: %dpx; width: %dpx; height: %dpx; border-radius: 50%%; background: %s; opacity: 0.35"></span>' % (
            round(size * cx - e * 0.45 + look * size * 0.05 + (-e * 0.35 if cx < 0.5 else e * 0.35)), round(size * 0.22 + e + 3), round(e * 0.9), round(e * 0.45), mark)
    mw = round(size * 0.16)
    mouth = '<svg width="%d" height="%d" viewBox="0 0 20 10" aria-hidden="true" style="position: absolute; left: %dpx; top: %dpx"><path d="M3 2 Q10 9 17 2" style="fill: none; stroke: #22203A; stroke-width: 2.5; stroke-linecap: round"></path></svg>' % (
        mw, round(mw / 2), round(size / 2 - mw / 2 + look * size * 0.05), round(size * 0.46))
    d = round(size * 0.36)
    emblem = T('<span style="position: absolute; left: [[l]]px; top: [[t]]px; width: [[d]]px; height: [[d]]px; box-sizing: border-box; border-radius: 50%; background: #FFFFFF; border: 3px solid [[m]]; display: flex; align-items: center; justify-content: center">[[i]]</span>',
               l=round(size / 2 - d / 2), t=round(size * 0.6), d=d, m=mark, i=ic(icon, round(d * 0.62), mark, 2.4))
    return T('<div style="position: relative; width: [[s]]px; height: [[s]]px"><div style="position: absolute; left: 0; top: 0; width: [[s]]px; height: [[s]]px; box-sizing: border-box; border-radius: [[br]]; background: [[f]]; border: [[b]]px solid [[m]]"></div>[[eyes]][[mouth]][[emblem]]</div>',
             s=size, br=BLOBS[v % 4], f=fill, b=max(3, size // 26), m=mark, eyes=eyes, mouth=mouth, emblem=emblem)


moves = "".join(T('<button style="height: 64px; box-sizing: border-box; padding: 8px 10px 8px 8px; border-radius: 22px; background: [[bg]]; border: 0; box-shadow: 0 3px 0 [[sh]]; color: #22203A; text-align: left; display: flex; align-items: center; gap: 10px; cursor: pointer"><span style="flex-shrink: 0; width: 44px; height: 44px; border-radius: 50%; background: #FFFFFF; display: flex; align-items: center; justify-content: center">[[i]]</span><span style="display: flex; flex-direction: column; line-height: 1.2"><span style="font-size: 15px; font-weight: 900">[[n]]</span><span style="font-size: 12px; font-weight: 700; color: #4A4458">[[s]]</span></span></button>',
                  bg=R[r][3], sh=rgba(R[r][1], 0.35), i=ic(i, 22, R[r][2]), n=n, s=s) for i, n, s, r in [
    ("pushup", "Power Push", "Strength · 60 dmg", "common"), ("run", "Tempo Dash", "Speed · hits first", "rare"),
    ("shield", "Core Brace", "Take 40% less", "uncommon"), ("heart", "Second Wind", "Heal 80 · 2 left", "mythic")])
pips = "".join('<span style="width: 16px; height: 8px; border-radius: 999px; background: #E0A51A"></span>' for _ in range(4))
battle_body = T("""<div style="[[PHONE]]">
<div style="position: absolute; left: 0; top: 0; width: 390px; height: 500px; background: linear-gradient(180deg, #BFE4FA 0%, #E6F5FD 60%)"></div>
<div style="position: absolute; left: 30px; top: 186px; width: 84px; height: 24px; border-radius: 999px; background: #FFFFFF"></div>
<div style="position: absolute; left: 52px; top: 172px; width: 38px; height: 32px; border-radius: 50%; background: #FFFFFF"></div>
<div style="position: absolute; left: 150px; top: 238px; width: 64px; height: 18px; border-radius: 999px; background: #FFFFFF; opacity: 0.8"></div>
<svg width="390" height="500" viewBox="0 0 390 500" aria-hidden="true" style="position: absolute; left: 0; top: 0">
<path d="M0 250 C 70 215, 150 240, 220 222 S 340 200, 390 226 L390 500 L0 500 Z" style="fill: #CDE8B0"></path>
<path d="M0 290 C 110 262, 250 300, 390 272 L390 500 L0 500 Z" style="fill: #BFE0A0"></path>
<ellipse cx="195" cy="380" rx="250" ry="96" style="fill: #F3E3C3"></ellipse>
<ellipse cx="195" cy="380" rx="200" ry="72" style="fill: none; stroke: #FFFFFF; stroke-width: 4"></ellipse>
<line x1="195" y1="308" x2="195" y2="452" style="stroke: #FFFFFF; stroke-width: 4"></line>
<ellipse cx="195" cy="380" rx="36" ry="13" style="fill: none; stroke: #FFFFFF; stroke-width: 4"></ellipse>
<ellipse cx="290" cy="258" rx="74" ry="17" style="fill: #A9D98A; stroke: #8FC56F; stroke-width: 3"></ellipse>
<ellipse cx="110" cy="444" rx="94" ry="21" style="fill: #A9D98A; stroke: #8FC56F; stroke-width: 3"></ellipse>
<path d="M176 346 C 206 300, 232 262, 262 214" style="fill: none; stroke: #FF7A59; stroke-width: 9; stroke-linecap: round"></path>
<path d="M192 360 C 222 316, 250 282, 280 238" style="fill: none; stroke: #FFCB47; stroke-width: 6; stroke-linecap: round"></path>
<path d="M312 132 l9 22 23 -6 -16 17 16 17 -23 -6 -9 22 -9 -22 -23 6 16 -17 -16 -17 23 6z" style="fill: #FFCB47; stroke: #FFFFFF; stroke-width: 4; stroke-linejoin: round"></path>
</svg>
<div style="position: absolute; left: 240px; top: 146px">[[OPP]]</div>
<div style="position: absolute; left: 44px; top: 306px">[[ME]]</div>
<div style="position: absolute; left: 262px; top: 96px; padding: 4px 12px 6px; border-radius: 18px; background: #FFFFFF; border: 2px solid #EFE4D3; box-shadow: 0 3px 0 #EADFCF; transform: rotate(6deg); display: flex; flex-direction: column; align-items: center; line-height: 1"><span style="font-size: 30px; font-weight: 800; color: #B8431F; [[FD]]">−86</span><span style="font-size: 11px; font-weight: 900; letter-spacing: 0.04em">Critical hit</span></div>
<div style="position: absolute; left: 16px; right: 16px; top: 18px; display: flex; align-items: center; gap: 10px">
[[BACK]]
<span style="flex-grow: 1; display: flex; justify-content: center"><span style="padding: 7px 14px; border-radius: 999px; background: #FFFFFF; border: 2px solid #EFE4D3; font-size: 13px; font-weight: 900">Ranked arena · Round 3</span></span>
<span style="display: flex; align-items: center; gap: 6px; padding: 7px 12px; border-radius: 999px; background: #22203A; color: #FFFFFF; font-size: 14px; font-weight: 900">[[CLK]]0:18</span>
</div>
<div style="position: absolute; left: 16px; top: 82px; width: 196px; box-sizing: border-box; padding: 10px 12px; border-radius: 22px; [[CARD]]; display: flex; flex-direction: column; gap: 6px">
<span style="display: flex; justify-content: space-between; align-items: baseline"><span style="font-size: 15px; font-weight: 900">IronVee</span><span style="font-size: 12px; font-weight: 800; color: #6E6878">Lv 26</span></span>
[[HP_OPP]]
<span style="display: flex; justify-content: space-between; align-items: center"><span style="font-size: 12px; font-weight: 800; color: #6E6878">210 / 500</span><span style="display: flex; align-items: center; gap: 4px; padding: 2px 8px; border-radius: 999px; background: #DFE8FB; color: #1B4AAE; font-size: 11px; font-weight: 900">[[SH]]Guard up</span></span>
</div>
<div style="position: absolute; right: 16px; top: 318px; width: 188px; box-sizing: border-box; padding: 10px 12px; border-radius: 22px; [[CARD]]; display: flex; flex-direction: column; gap: 6px">
<span style="display: flex; justify-content: space-between; align-items: baseline"><span style="font-size: 15px; font-weight: 900">VoltRunner</span><span style="font-size: 12px; font-weight: 800; color: #6E6878">Lv 24</span></span>
[[HP_ME]]
<span style="font-size: 12px; font-weight: 800; color: #6E6878">390 / 500</span>
<span style="display: flex; align-items: center; justify-content: space-between"><span style="font-size: 11px; font-weight: 900; color: #8F4A00">Finisher</span><span style="display: flex; gap: 3px">[[PIPS]]</span></span>
</div>
<div style="position: absolute; left: 0; right: 0; top: 488px; bottom: 0; box-sizing: border-box; padding: 18px 16px 20px; border-radius: 32px 32px 0 0; background: #FFF8EE; border-top: 2px solid #EFE4D3; display: flex; flex-direction: column; gap: 12px">
<div style="display: flex; align-items: center; justify-content: space-between"><span style="display: flex; align-items: center; gap: 8px; font-size: 15px; font-weight: 900"><span style="width: 10px; height: 10px; border-radius: 50%; background: #FF7A59"></span>Power Push landed a critical hit!</span><span style="font-size: 12px; font-weight: 800; color: #6E6878">Your turn</span></div>
[[FINBTN]]
<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px">[[MOVES]]</div>
<span style="text-align: center; font-size: 12px; font-weight: 700; color: #6E6878">Every move is powered by your real training stats</span>
</div>
</div>""",
    PHONE=PHONE, FD=FD, CARD=CARDSTYLE, BACK=backlink("Leave match"), CLK=ic("clock", 14, "#FFFFFF", 2.6),
    OPP=fighter("epic", "pullup", 100, -1, 1), ME=fighter("legendary", "muscleup", 132, 1, 0),
    HP_OPP=bar(42, R["mythic"][1], 10), SH=ic("shield", 12, R["rare"][2], 2.6),
    HP_ME=bar(78, R["uncommon"][1], 10), PIPS=pips,
    FINBTN=T('<button style="height: 64px; box-sizing: border-box; border: 0; border-radius: 999px; background: #FFCB47; box-shadow: 0 5px 0 #E0A51A; color: #22203A; display: flex; align-items: center; gap: 12px; padding: 0 18px 0 9px; cursor: pointer"><span style="width: 46px; height: 46px; border-radius: 50%; background: #FFFFFF; display: flex; align-items: center; justify-content: center">[[i]]</span><span style="flex-grow: 1; display: flex; flex-direction: column; align-items: flex-start; line-height: 1.1"><span style="font-size: 22px; font-weight: 700; [[FD]]">Skybreaker</span><span style="font-size: 12px; font-weight: 800">Finisher · 220 dmg · breaks guard</span></span><span style="font-size: 12px; font-weight: 900; padding: 4px 10px; border-radius: 999px; background: #FFFFFF">Ready</span></button>',
             i=ic("muscleup", 28, "#8F4A00", 2.2), FD=FD),
    MOVES=moves,
)
files["Battle.dc.html"] = page("Online battle", battle_body, 390, 844)

# =====================================================================
# FINISHER UNLOCKED
# =====================================================================
confetti_cols = [CORAL, SUN, R["rare"][1], R["uncommon"][1], R["epic"][1], R["mythic"][1]]
conf = []
import random
random.seed(7)
for n in range(34):
    x, y = random.randint(10, 370), random.randint(60, 420)
    if 110 < x < 280 and 110 < y < 330:
        continue
    w, h = random.choice([(10, 18), (8, 8), (14, 6)])
    conf.append('<span style="position: absolute; left: %dpx; top: %dpx; width: %dpx; height: %dpx; border-radius: 999px; background: %s; transform: rotate(%ddeg)"></span>' % (x, y, w, h, random.choice(confetti_cols), random.randint(0, 180)))
fstats = "".join(T('<div style="padding: 12px 6px; border-radius: 22px; [[CARD]]; display: flex; flex-direction: column; align-items: center"><span style="font-size: 26px; font-weight: 700; color: [[c]]; [[FD]]">[[v]]</span><span style="font-size: 12px; font-weight: 700; color: #6E6878">[[l]]</span></div>',
                     CARD=CARDSTYLE, c=c, v=v, l=l, FD=FD) for v, l, c in [("220", "damage", LEG[2]), ("3", "turns to charge", INK), ("Breaks", "enemy guard", INK)])
fin_body = T("""<div style="[[PHONE]]">
<div style="position: absolute; left: 60px; top: 110px; width: 270px; height: 250px; border-radius: 52% 48% 60% 40% / 45% 55% 45% 55%; background: #FFE9C2"></div>
[[CONF]]
<div style="position: absolute; left: 0; top: 0; width: 390px; height: 844px; box-sizing: border-box; padding: 20px 16px 22px; display: flex; flex-direction: column; align-items: center">
<div style="align-self: stretch; display: flex; justify-content: flex-end">[[CLOSE]]</div>
<div style="margin-top: 70px">[[TOKEN]]</div>
<span style="margin-top: 40px; font-size: 32px; font-weight: 700; color: #B8431F; transform: rotate(-3deg); [[FH]]">new finisher unlocked!</span>
<h1 style="margin: 2px 0 0; font-size: 60px; line-height: 1; font-weight: 700; font-style: italic; letter-spacing: -0.01em; [[FD]]">Skybreaker</h1>
<span style="margin-top: 12px; display: flex; align-items: center; gap: 8px; font-size: 15px; font-weight: 700; color: #6E6878">Earned with 3 clean Muscle-ups [[LEGP]]</span>
<div style="align-self: stretch; margin-top: 26px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px">[[STATS]]</div>
<div style="align-self: stretch; margin-top: auto; display: flex; flex-direction: column; gap: 12px">
[[EQUIP]]
[[SHARE]]
<span style="display: flex; align-items: center; justify-content: center; gap: 6px; font-size: 12px; font-weight: 700; color: #6E6878">[[CHK]]Checked by the camera, so it&#39;s the real deal</span>
</div>
</div>
</div>""",
    PHONE=PHONE, FD=FD, FH=FH, CONF="".join(conf), CLOSE=backlink("Close", "Profile.dc.html", "close"),
    TOKEN=token("legendary", "muscleup", 160, v=0), LEGP=pill("legendary", 11), STATS=fstats,
    EQUIP=btn_primary("Equip &amp; battle", "swords", "Battle.dc.html"), SHARE=btn_secondary("Share the rep clip", "share"), CHK=ic("check", 14, R["uncommon"][2], 3),
)
files["Finisher.dc.html"] = page("Finisher unlocked", fin_body, 390, 844)

# =====================================================================
# STREET DUELS (new feature)
# =====================================================================
ODDS = [("common", 40), ("uncommon", 27), ("rare", 17), ("epic", 10), ("legendary", 4), ("mythic", 2)]


def odds_stack(h=16):
    segs = "".join('<span title="%s: %d%% chance" style="flex: %d; height: %dpx; border-radius: 999px; background: %s"></span>' % (R[k][0], v, v, h, R[k][1]) for k, v in ODDS)
    return '<div role="img" aria-label="Steal odds: common 40%, uncommon 27%, rare 17%, epic 10%, legendary 4%, mythic 2%" style="display: flex; gap: 2px">' + segs + "</div>"


def odds_legend(fs=12):
    return '<div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); row-gap: 4px; column-gap: 8px">' + "".join(
        '<span style="display: flex; align-items: center; gap: 6px; font-size: %dpx; font-weight: 700; color: #4A4458"><span style="width: 9px; height: 9px; border-radius: 50%%; background: %s"></span>%s <b style="color: #22203A; font-weight: 900">%d%%</b></span>' % (fs, R[k][1], R[k][0], v)
        for k, v in ODDS) + "</div>"


SETS = [
    ("Squat hold", "Last one standing", "squat", "Pistol Power", "+5 s hold", "epic", "Iron Legs", "+4 s hold", "uncommon"),
    ("Push-up race", "Most reps in 30 s", "pushup", "Diamond Grip", "every 5th rep ×2", "rare", "Quick Hands", "+3 rep head start", "common"),
    ("50 m sprint", "GPS timed", "run", "Tailwind", "−0.3 s", "rare", "Fast Feet", "−0.4 s", "uncommon"),
]


def set_row(i, s, state=None):
    name, rule, icon, mb, mbe, mr, tb, tbe, tr = s
    badge = ""
    if state == "won":
        badge = '<span style="padding: 3px 10px; border-radius: 999px; background: #D6F3E2; color: #13784C; font-size: 12px; font-weight: 900">Won</span>'
    elif state == "live":
        badge = '<span style="padding: 3px 10px; border-radius: 999px; background: #FFCB47; font-size: 12px; font-weight: 900">Live</span>'
    return T('<div style="padding: 10px 12px; border-radius: 22px; [[CARD]]; display: flex; flex-direction: column; gap: 8px"><div style="display: flex; align-items: center; gap: 10px"><span style="flex-shrink: 0; width: 34px; height: 34px; border-radius: 50%; background: #FFE4DA; display: flex; align-items: center; justify-content: center; font-size: 15px; font-weight: 800; color: #B8431F; [[FD]]">[[n]]</span><span style="flex-grow: 1; display: flex; flex-direction: column; line-height: 1.15"><span style="font-size: 15px; font-weight: 900">[[name]]</span><span style="font-size: 12px; font-weight: 700; color: #6E6878">[[rule]]</span></span>[[badge]]</div><div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 6px"><span style="display: flex; align-items: center; gap: 6px; padding: 5px 8px; border-radius: 14px; background: [[mf]]; font-size: 11px; font-weight: 800; line-height: 1.2">[[mi]]<span>You: [[mb]] <span style="font-weight: 700; color: #4A4458">[[mbe]]</span></span></span><span style="display: flex; align-items: center; gap: 6px; padding: 5px 8px; border-radius: 14px; background: [[tf]]; font-size: 11px; font-weight: 800; line-height: 1.2">[[ti]]<span>Maya: [[tb]] <span style="font-weight: 700; color: #4A4458">[[tbe]]</span></span></span></div></div>',
             CARD=CARDSTYLE, FD=FD, n=i + 1, name=name, rule=rule, badge=badge, mf=R[mr][3], mi=ic("bolt", 14, R[mr][2]), mb=mb, mbe=mbe,
             tf=R[tr][3], ti=ic("bolt", 14, R[tr][2]), tb=tb, tbe=tbe)


mini_map = """<svg width="358" height="130" viewBox="0 20 358 130" aria-hidden="true" style="display: block">
<rect width="358" height="170" style="fill: #E4F1D2"></rect>
<rect x="0" y="92" width="358" height="22" style="fill: #FFFFFF"></rect>
<rect x="150" y="0" width="22" height="170" style="fill: #FFFFFF"></rect>
<rect x="14" y="14" width="120" height="64" rx="24" style="fill: #F7EEDC"></rect>
<rect x="188" y="14" width="156" height="64" rx="24" style="fill: #C9E7A9"></rect>
<rect x="14" y="128" width="120" height="30" rx="15" style="fill: #F7EEDC"></rect>
<rect x="188" y="128" width="156" height="30" rx="15" style="fill: #F3E8D3"></rect>
<path d="M100 104 C 150 60, 210 60, 262 100" style="fill: none; stroke: #22203A; stroke-width: 3; stroke-dasharray: 2 9; stroke-linecap: round"></path>
<circle cx="100" cy="104" r="46" style="fill: rgba(255, 203, 71, 0.18); stroke: #FFCB47; stroke-width: 2.5"></circle>
<circle cx="262" cy="100" r="46" style="fill: rgba(255, 122, 89, 0.14); stroke: #FF7A59; stroke-width: 2.5"></circle>
</svg>"""

invite_body = T("""<div style="[[PHONE]]; padding: 20px 16px; display: flex; flex-direction: column; gap: 10px">
[[HEAD]]
<div style="position: relative; border-radius: 26px; overflow: hidden; border: 2px solid #EFE4D3; box-shadow: 0 3px 0 #EADFCF">
[[MAP]]
<div style="position: absolute; left: 74px; top: 56px">[[AV_ME]]</div>
<div style="position: absolute; left: 236px; top: 52px">[[AV_MAYA]]</div>
</div>
<div style="display: flex; flex-direction: column; gap: 2px">
<span style="font-size: 28px; line-height: 1.05; font-weight: 700; [[FD]]">Maya_lifts wants to <i>duel</i></span>
<span style="font-size: 14px; font-weight: 700; color: #6E6878">Lv 22 · 51 FitMon · best of 3 sets, 2 minutes</span>
</div>
[[S1]]
[[S2]]
[[S3]]
<div style="padding: 12px 14px; border-radius: 22px; background: #FFF1CC; display: flex; flex-direction: column; gap: 8px">
<span style="display: flex; align-items: center; gap: 8px; font-size: 15px; font-weight: 900">[[DICE]]Winner steals 1 random FitMon</span>
[[STACK]]
[[LEGEND]]
</div>
<div style="display: flex; gap: 10px; margin-top: auto">
[[ACCEPT]]
[[DECLINE]]
</div>
</div>""",
    PHONE=PHONE, FD=FD, FH=FH, HEAD=header("Street duel", "A trainer nearby wants to battle"), MAP=mini_map,
    AV_ME=avatar("VR", 52, SUN, INK, 0), AV_MAYA=avatar("M", 56, CORAL, INK, 2),
    S1=set_row(0, SETS[0]), S2=set_row(1, SETS[1]), S3=set_row(2, SETS[2]),
    DICE=ic("dice", 20, INK), STACK=odds_stack(12), LEGEND=odds_legend(11),
    ACCEPT=btn_primary("Accept duel", "handshake", "DuelLive.dc.html", 56, extra="flex-grow: 1"),
    DECLINE=btn_secondary("Not now", None, "Map.dc.html", 56, extra="width: 118px"),
)
files["DuelInvite.dc.html"] = page("Duel invite", invite_body, 390, 844)

cam = """<svg width="358" height="120" viewBox="0 0 358 120" aria-hidden="true" style="display: block">
<rect width="358" height="120" rx="22" style="fill: #2E2B45"></rect>
<path d="M18 36 V18 H36 M322 18 H340 V36 M340 84 V102 H322 M36 102 H18 V84" style="fill: none; stroke: #FFCB47; stroke-width: 4; stroke-linecap: round; stroke-linejoin: round"></path>
<path d="M92 92 H270" style="stroke: #4A4666; stroke-width: 4; stroke-linecap: round"></path>
<circle cx="108" cy="58" r="10" style="fill: none; stroke: #FFFFFF; stroke-width: 4"></circle>
<path d="M120 62 L250 80 M138 65 V92 M250 80 V92" style="fill: none; stroke: #FFFFFF; stroke-width: 5; stroke-linecap: round"></path>
<circle cx="138" cy="65" r="4" style="fill: #FF7A59"></circle><circle cx="250" cy="80" r="4" style="fill: #FF7A59"></circle><circle cx="120" cy="62" r="4" style="fill: #FF7A59"></circle>
</svg>"""

live_body = T("""<div style="[[PHONE]]; padding: 20px 16px; display: flex; flex-direction: column; gap: 10px">
[[HEAD]]
<div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 6px">
<span style="padding: 7px 0; border-radius: 999px; background: #D6F3E2; color: #13784C; text-align: center; font-size: 12px; font-weight: 900">Set 1 · won</span>
<span style="padding: 7px 0; border-radius: 999px; background: #FFCB47; text-align: center; font-size: 12px; font-weight: 900">Set 2 · live</span>
<span style="padding: 7px 0; border-radius: 999px; border: 2px dashed #D9CCB8; text-align: center; font-size: 12px; font-weight: 800; color: #6E6878">Set 3</span>
</div>
<div style="padding: 14px; border-radius: 28px; [[CARD]]; display: flex; flex-direction: column; gap: 10px">
<div style="display: flex; align-items: baseline; justify-content: space-between"><span style="font-size: 24px; font-weight: 700; [[FD]]">Push-up <i>race</i></span><span style="display: flex; align-items: center; gap: 6px; font-size: 22px; font-weight: 700; color: #B8431F; [[FD]]">[[CLK]]0:12</span></div>
<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px">
<div style="padding: 12px; border-radius: 22px; background: #FFF1CC; display: flex; flex-direction: column; align-items: center; gap: 2px">[[AV_ME]]<span style="font-size: 13px; font-weight: 900; margin-top: 4px">You</span><span style="font-size: 64px; line-height: 1; font-weight: 800; [[FD]]">18</span><span style="font-size: 12px; font-weight: 700; color: #6E6878">reps</span></div>
<div style="padding: 12px; border-radius: 22px; background: #FFE4DA; display: flex; flex-direction: column; align-items: center; gap: 2px">[[AV_MAYA]]<span style="font-size: 13px; font-weight: 900; margin-top: 4px">Maya</span><span style="font-size: 64px; line-height: 1; font-weight: 800; [[FD]]">20</span><span style="font-size: 12px; font-weight: 700; color: #6E6878">reps</span></div>
</div>
</div>
<span style="font-size: 20px; font-weight: 700; [[FD]]">This set&#39;s <i>buffs</i></span>
<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px">
<div style="padding: 10px; border-radius: 22px; background: #DFE8FB; display: flex; flex-direction: column; gap: 6px">[[TOK_ME]]<span style="font-size: 14px; font-weight: 900">Diamond Grip</span><span style="font-size: 12px; font-weight: 700; color: #3A3550; line-height: 1.3">Every 5th rep counts double. From your Diamond Push-ups.</span></div>
<div style="padding: 10px; border-radius: 22px; background: #E9EDF5; display: flex; flex-direction: column; gap: 6px">[[TOK_MAYA]]<span style="font-size: 14px; font-weight: 900">Quick Hands</span><span style="font-size: 12px; font-weight: 700; color: #3A3550; line-height: 1.3">Starts 3 reps ahead. From Maya&#39;s Push-ups.</span></div>
</div>
<div style="position: relative">[[CAM]]<span style="position: absolute; left: 16px; bottom: 12px; font-size: 18px; font-weight: 700; color: #FFCB47; [[FH]]">rep check: form looks good</span></div>
<span style="font-size: 20px; font-weight: 700; color: #B8431F; text-align: center; line-height: 1.1; [[FH]]">2 behind, but your next rep is a double!</span>
[[NEXT]]
</div>""",
    PHONE=PHONE, FD=FD, FH=FH, CARD=CARDSTYLE,
    HEAD=header("Street duel", "vs Maya_lifts · 40 m away", '<span style="padding: 6px 14px; border-radius: 999px; background: #22203A; color: #FFFFFF; font-size: 18px; font-weight: 700; ' + FD + '">1 – 0</span>', backlink("Forfeit duel", "Map.dc.html", "close")),
    CLK=ic("clock", 20, CORALTXT), AV_ME=avatar("VR", 44, SUN, INK, 0, "#FFFFFF"), AV_MAYA=avatar("M", 44, CORAL, INK, 2, "#FFFFFF"),
    TOK_ME=token("rare", "pushup", 34, v=1), TOK_MAYA=token("common", "pushup", 34, v=2), CAM=cam,
    NEXT=btn_primary("See the result", "arrowR", "DuelResult.dc.html", 54),
)
files["DuelLive.dc.html"] = page("Duel in progress", live_body, 390, 844)

reel = [("common", "squat", "Squats", False), ("rare", "pullup", "Pull-ups", False), ("uncommon", "burpee", "Burpees", True), ("mythic", "frontlever", "Front Lever", False), ("common", "walk", "Lunges", False)]
reel_html = "".join(
    T('<div style="flex-shrink: 0; display: flex; flex-direction: column; align-items: center; gap: 4px; opacity: [[o]]">[[t]]</div>', o="1" if pick else "0.45", t=token(r, i, 78 if pick else 50, v=k, sparkles=False))
    for k, (r, i, n, pick) in enumerate(reel))
result_body = T("""<div style="[[PHONE]]">
[[CONF]]
<div style="position: absolute; left: 0; top: 0; width: 390px; height: 844px; box-sizing: border-box; padding: 20px 16px 22px; display: flex; flex-direction: column; gap: 12px">
<div style="display: flex; justify-content: flex-end">[[CLOSE]]</div>
<div style="display: flex; flex-direction: column; align-items: center; gap: 2px; margin-top: 4px">
<span style="font-size: 30px; font-weight: 700; color: #B8431F; transform: rotate(-3deg); [[FH]]">you did it!</span>
<h1 style="margin: 0; font-size: 50px; line-height: 1; font-weight: 700; [[FD]]">You won <i>2–1</i></h1>
</div>
<div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 6px">
<span style="padding: 8px 4px; border-radius: 18px; background: #D6F3E2; display: flex; flex-direction: column; align-items: center; line-height: 1.2"><span style="font-size: 12px; font-weight: 900; color: #13784C">Squat hold</span><span style="font-size: 12px; font-weight: 700">0:52 vs 0:47</span></span>
<span style="padding: 8px 4px; border-radius: 18px; background: #FFE4DA; display: flex; flex-direction: column; align-items: center; line-height: 1.2"><span style="font-size: 12px; font-weight: 900; color: #B8431F">Push-up race</span><span style="font-size: 12px; font-weight: 700">24 vs 26</span></span>
<span style="padding: 8px 4px; border-radius: 18px; background: #D6F3E2; display: flex; flex-direction: column; align-items: center; line-height: 1.2"><span style="font-size: 12px; font-weight: 900; color: #13784C">50 m sprint</span><span style="font-size: 12px; font-weight: 700">7.9 s vs 8.4 s</span></span>
</div>
<div style="padding: 14px 0 16px; border-radius: 28px; [[CARD]]; display: flex; flex-direction: column; align-items: center; gap: 10px">
<span style="display: flex; align-items: center; gap: 8px; font-size: 15px; font-weight: 900">[[DICE]]Stealing from Maya&#39;s FitDex…</span>
<div style="position: relative; width: 100%; height: 104px; overflow: hidden; display: flex; align-items: center; justify-content: center; gap: 14px">
[[REEL]]
<svg width="24" height="14" viewBox="0 0 24 14" aria-hidden="true" style="position: absolute; left: 183px; top: 0"><path d="M2 2 H22 L12 12 Z" style="fill: #22203A; stroke: #22203A; stroke-width: 2; stroke-linejoin: round"></path></svg>
</div>
<span style="font-size: 26px; line-height: 1.05; font-weight: 700; text-align: center; [[FD]]">You got <i>Burpees!</i></span>
[[UNC]]
</div>
<div style="padding: 12px 14px; border-radius: 22px; background: #FFF1CC; display: flex; flex-direction: column; gap: 8px">
<span style="font-size: 14px; font-weight: 800; line-height: 1.3">Common FitMon get picked most. Maya&#39;s Mythic Front Lever only had a <b style="font-weight: 900; color: #C0305F">2% chance</b>.</span>
[[STACK]]
</div>
<div style="display: flex; flex-direction: column; gap: 12px; margin-top: auto">
[[ADD]]
<span style="display: flex; align-items: center; justify-content: center; gap: 6px; font-size: 12px; font-weight: 700; color: #6E6878">[[CLK]]Rematch with Maya opens in 24 h</span>
</div>
</div>
</div>""",
    PHONE=PHONE, FD=FD, FH=FH, CARD=CARDSTYLE, CONF="".join(c for c in conf[:14]), CLOSE=backlink("Close", "Map.dc.html", "close"),
    DICE=ic("dice", 20, INK), REEL=reel_html, UNC=pill("uncommon", 12), STACK=odds_stack(12),
    ADD=btn_primary("Add to my FitDex", "gift", "Dex.dc.html"), CLK=ic("clock", 14, MUTED),
)
files["DuelResult.dc.html"] = page("Duel result", result_body, 390, 844)

# =====================================================================
# HERO (Main)
# =====================================================================
def phone(name, scale, left, top, rot, z):
    return T('<div style="position: absolute; left: [[l]]px; top: [[t]]px; width: [[w]]px; height: [[h]]px; box-sizing: border-box; transform: rotate([[r]]deg); z-index: [[z]]; border-radius: [[br]]px; background: #22203A; padding: 9px; box-shadow: 0 30px 60px rgba(34, 32, 58, 0.18)"><div style="width: [[iw]]px; height: [[ih]]px; border-radius: [[ibr]]px; overflow: hidden"><div style="width: 390px; height: 844px; transform: scale([[s]]); transform-origin: 0 0"><dc-import name="[[n]]" hint-size="390px,844px"></dc-import></div></div></div>',
             l=left, t=top, w=round(390 * scale) + 18, h=round(844 * scale) + 18, r=rot, z=z, br=round(48 * scale) + 9, iw=round(390 * scale), ih=round(844 * scale), ibr=round(44 * scale), s=scale, n=name)


pillars = "".join(T('<div style="display: flex; align-items: center; gap: 16px"><span style="flex-shrink: 0; width: 52px; height: 52px; border-radius: [[br]]; background: [[bg]]; display: flex; align-items: center; justify-content: center">[[i]]</span><span style="display: flex; flex-direction: column; gap: 2px"><span style="font-size: 19px; font-weight: 900">[[t]]</span><span style="font-size: 16px; line-height: 1.4; font-weight: 600; color: #6E6878">[[d]]</span></span></div>',
                      br=BLOBS[k], bg=bg, i=ic(i, 24, c), t=t, d=d) for k, (i, t, d, c, bg) in enumerate([
    ("pin", "Explore", "Exercises spawn around you. The rarer the move, the harder it is to find.", CORALTXT, PEACH),
    ("route", "Train", "Run and walk missions outdoors, muscle raids at the gym.", "#13784C", MINT),
    ("swords", "Battle", "Duel online, or meet a trainer nearby and play for their FitMon.", "#7B3FD0", LILAC)]))

hero_body = T("""<div style="position: relative; width: 1440px; height: 900px; overflow: hidden; background: #FFF8EE; color: #22203A; font-family: 'Nunito', system-ui, sans-serif">
<div style="position: absolute; left: 820px; top: 70px; width: 600px; height: 560px; border-radius: 58% 42% 55% 45% / 52% 58% 42% 48%; background: #D6F3E2"></div>
<div style="position: absolute; left: 1150px; top: 520px; width: 330px; height: 330px; border-radius: 45% 55% 42% 58% / 55% 45% 55% 45%; background: #FFE4DA"></div>
<div style="position: absolute; left: 760px; top: 600px; width: 200px; height: 180px; border-radius: 52% 48% 60% 40% / 45% 55% 45% 55%; background: #FFE9C2"></div>
<svg width="1440" height="900" viewBox="0 0 1440 900" aria-hidden="true" style="position: absolute; left: 0; top: 0"><path d="M-20 820 C 200 760, 420 880, 640 820 S 900 740, 1100 800" style="fill: none; stroke: #F1E4CF; stroke-width: 3; stroke-dasharray: 2 12; stroke-linecap: round"></path></svg>
<div style="position: absolute; left: 104px; top: 0; width: 620px; height: 900px; display: flex; flex-direction: column; justify-content: center">
<div style="display: flex; align-items: center; gap: 12px">
<span style="width: 48px; height: 48px; border-radius: 58% 42% 55% 45% / 52% 58% 42% 48%; background: #FFCB47; display: flex; align-items: center; justify-content: center">[[BOLT]]</span>
<span style="font-size: 28px; font-weight: 800; [[FD]]">FitMon <span style="color: #B8431F">GO</span></span>
</div>
<h1 style="margin: 44px 0 0; font-size: 92px; line-height: 1; font-weight: 700; letter-spacing: -0.02em; [[FD]]">Catch reps,<br>not <span style="color: #B8431F">monsters.</span></h1>
<p style="margin: 28px 0 0; font-size: 21px; line-height: 1.5; font-weight: 600; color: #4A4458; max-width: 540px">A fitness game played on a real map. Exercises spawn around you, you do the reps to catch them, and your real stats power your battles.</p>
<div style="margin-top: 44px; display: flex; flex-direction: column; gap: 22px">[[PILLARS]]</div>
<span style="margin-top: 44px; align-self: flex-start; padding: 6px 14px; border-radius: 999px; background: #FFFFFF; border: 2px solid #EADFCF; font-size: 13px; font-weight: 800; color: #6E6878">TSA app pitch</span>
</div>
[[P2]]
[[P1]]
<span style="position: absolute; left: 800px; top: 30px; transform: rotate(-5deg); font-size: 30px; font-weight: 700; color: #B8431F; [[FH]]">a wild Front Lever appeared!</span>
<svg width="90" height="80" viewBox="0 0 90 80" aria-hidden="true" style="position: absolute; left: 910px; top: 70px"><path d="M8 6 C 20 40, 44 60, 78 64" style="fill: none; stroke: #B8431F; stroke-width: 3; stroke-linecap: round"></path><path d="M66 54 L80 64 L66 74" style="fill: none; stroke: #B8431F; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round"></path></svg>
<span style="position: absolute; left: 1060px; top: 820px; transform: rotate(-3deg); font-size: 28px; font-weight: 700; color: #7B3FD0; [[FH]]">bump into a trainer? duel!</span>
</div>""",
    FD=FD, FH=FH, BOLT=ic("bolt", 28, INK, 2.4), PILLARS=pillars,
    P1=phone("Map", 0.82, 880, 100, -4, 3), P2=phone("DuelInvite", 0.7, 1110, 150, 6, 2),
)
files["Main.dc.html"] = page("FitMon GO pitch", hero_body, 1440, 900)

# =====================================================================
# HOW IT PLAYS
# =====================================================================
steps = [("pin", "Explore", "Walk your city. Exercise spawns and missions pop up on the map.", CORALTXT, PEACH),
         ("camera", "Catch", "Do the reps. The camera checks your form, so every catch is earned.", R["rare"][2], R["rare"][3]),
         ("star", "Level up", "Each catch trains a muscle and boosts Strength, Speed and more.", "#13784C", MINT),
         ("swords", "Battle", "Take your stats, power-ups and finishers into duels.", "#7B3FD0", LILAC)]
loop = []
for idx, (i, t, d, c, bg) in enumerate(steps):
    loop.append(T('<div style="flex: 1; padding: 18px; border-radius: 28px; [[CARD]]; display: flex; gap: 14px; align-items: flex-start"><span style="flex-shrink: 0; width: 52px; height: 52px; border-radius: [[br]]; background: [[bg]]; display: flex; align-items: center; justify-content: center">[[i]]</span><span style="display: flex; flex-direction: column; gap: 2px"><span style="font-size: 20px; font-weight: 700; line-height: 1; color: [[c]]; [[FH]]">step [[n]]</span><span style="font-size: 24px; font-weight: 700; [[FD]]">[[t]]</span><span style="font-size: 14px; line-height: 1.45; font-weight: 600; color: #6E6878">[[d]]</span></span></div>',
                  CARD=CARDSTYLE, br=BLOBS[idx], bg=bg, i=ic(i, 24, c), c=c, n=idx + 1, t=t, d=d, FD=FD, FH=FH))
    if idx < 3:
        loop.append('<svg width="34" height="40" viewBox="0 0 34 40" aria-hidden="true" style="flex-shrink: 0; align-self: center"><path d="M3 26 C 10 8, 20 8, 28 20" style="fill: none; stroke: #CFC3B1; stroke-width: 3; stroke-linecap: round"></path><path d="M20 18 L29 21 L28 11" style="fill: none; stroke: #CFC3B1; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round"></path></svg>')

ladder_data = [("common", "pushup", ["Push-ups", "Squats", "Walking"], "×1"),
               ("uncommon", "burpee", ["Burpees", "Dips", "Lunges"], "×1.5"),
               ("rare", "pullup", ["Pull-ups", "Diamond push-ups", "Tuck lever"], "×2"),
               ("epic", "squat", ["Pistol squats", "L-sit", "Archer pull-ups"], "×3"),
               ("legendary", "muscleup", ["Muscle-ups", "Handstand push-ups", "Human flag"], "×5"),
               ("mythic", "frontlever", ["Front lever", "Full planche", "One-arm pull-up"], "×10")]
ladder = "".join(T('<div style="padding: 18px 14px; border-radius: 28px; background: [[f]]; display: flex; flex-direction: column; align-items: center; gap: 8px">[[t]]<span style="font-size: 24px; font-weight: 700; color: [[c]]; [[FD]]">[[n]]</span><span style="display: flex; flex-direction: column; align-items: center; gap: 2px; font-size: 14px; font-weight: 700; color: #3A3550; text-align: center">[[ex]]</span><span style="margin-top: 2px; padding: 4px 12px; border-radius: 999px; background: #FFFFFF; color: [[c]]; font-size: 13px; font-weight: 900">XP [[x]]</span></div>',
                   f=R[r][3], t=token(r, i, 64, v=k), c=R[r][2], n=R[r][0], ex="".join("<span>%s</span>" % e for e in ex), x=x, FD=FD)
                 for k, (r, i, ex, x) in enumerate(ladder_data))
modes = "".join(T('<div style="flex: 1; padding: 18px; border-radius: 28px; [[CARD]]; display: flex; flex-direction: column; gap: 6px; position: relative"><span style="width: 48px; height: 48px; border-radius: [[br]]; background: [[bg]]; display: flex; align-items: center; justify-content: center">[[i]]</span><span style="font-size: 22px; font-weight: 700; [[FD]]">[[t]]</span><span style="font-size: 13px; font-weight: 900; color: [[c]]">[[w]]</span><span style="font-size: 14px; line-height: 1.45; font-weight: 600; color: #6E6878">[[d]]</span>[[badge]]</div>',
                  CARD=CARDSTYLE, br=BLOBS[k], bg=bg, i=ic(i, 24, c), t=t, w=w, c=c, d=d, FD=FD,
                  badge=('<span style="position: absolute; right: 16px; top: 16px; padding: 3px 12px; border-radius: 999px; background: #FFCB47; font-size: 18px; font-weight: 700; ' + FH + '">new!</span>') if k == 3 else "")
                for k, (i, t, w, d, c, bg) in enumerate([
    ("route", "Street mode", "On roads &amp; in public", "Only safe run and walk missions. Distance, pace and hills level up Speed and Endurance.", "#13784C", MINT),
    ("dumbbell", "Gym mode", "At a gym or in a session", "Pick a target muscle and clear a raid of missions to level it up.", "#7B3FD0", LILAC),
    ("swords", "Arena", "Online, anywhere", "Duel trainers with moves built from your stats, power-ups and finishers.", "#8F4A00", R["legendary"][3]),
    ("handshake", "Street duels", "When trainers meet", "Best of 3 sets with buffs. The winner steals one random FitMon.", CORALTXT, PEACH)]))
how_body = T("""<div style="position: relative; width: 1440px; height: 900px; overflow: hidden; box-sizing: border-box; padding: 56px 80px; background: #FFF8EE; color: #22203A; font-family: 'Nunito', system-ui, sans-serif; display: flex; flex-direction: column; gap: 20px">
<div style="position: absolute; right: -80px; top: -90px; width: 360px; height: 260px; border-radius: 58% 42% 55% 45% / 52% 58% 42% 48%; background: #FFE9C2"></div>
<div style="position: relative; display: flex; align-items: flex-end; justify-content: space-between">
<h2 style="margin: 0; font-size: 60px; line-height: 1; font-weight: 700; letter-spacing: -0.01em; [[FD]]">How FitMon GO <i>plays</i></h2>
</div>
<div style="position: relative; display: flex; gap: 8px">[[LOOP]]</div>
<div style="display: flex; align-items: baseline; gap: 14px"><span style="font-size: 26px; font-weight: 700; [[FD]]">The rarity <i>ladder</i></span><span style="font-size: 15px; font-weight: 700; color: #6E6878">Harder skill, rarer spawn, bigger reward</span></div>
<div style="display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 12px">[[LADDER]]</div>
<div style="display: flex; align-items: baseline; gap: 14px"><span style="font-size: 26px; font-weight: 700; [[FD]]">Four ways to <i>play</i></span></div>
<div style="display: flex; gap: 12px">[[MODES]]</div>
</div>""", FD=FD, FH=FH, LOOP="".join(loop), LADDER=ladder, MODES=modes)
files["HowItPlays.dc.html"] = page("How it plays", how_body, 1440, 900)

# =====================================================================
# STREET DUELS explainer board
# =====================================================================
flow = [("handshake", "1. Meet up", "Two trainers within 50 m both get a duel invite. Both have to say yes.", CORALTXT, PEACH),
        ("bolt", "2. Best of 3", "Three quick sets. In each set, both players get a buff from their own FitMon.", "#13784C", MINT),
        ("dice", "3. Steal", "Whoever wins two sets steals one random FitMon from the other player.", "#7B3FD0", LILAC)]
flow_html = "".join(T('<div style="padding: 18px; border-radius: 28px; [[CARD]]; display: flex; gap: 14px; align-items: flex-start"><span style="flex-shrink: 0; width: 52px; height: 52px; border-radius: [[br]]; background: [[bg]]; display: flex; align-items: center; justify-content: center">[[i]]</span><span style="display: flex; flex-direction: column; gap: 2px"><span style="font-size: 24px; font-weight: 700; [[FD]]">[[t]]</span><span style="font-size: 15px; line-height: 1.45; font-weight: 600; color: #6E6878">[[d]]</span></span></div>',
                      CARD=CARDSTYLE, br=BLOBS[k], bg=bg, i=ic(i, 24, c), t=t, d=d, FD=FD) for k, (i, t, d, c, bg) in enumerate(flow))
set_cards = "".join(T('<div style="padding: 16px; border-radius: 26px; [[CARD]]; display: flex; flex-direction: column; gap: 8px">[[t]]<span style="font-size: 16px; font-weight: 700; color: #B8431F; line-height: 1; [[FH]]">set [[n]]</span><span style="font-size: 22px; font-weight: 700; line-height: 1; [[FD]]">[[name]]</span><span style="font-size: 13px; font-weight: 700; color: #6E6878">[[rule]]</span><span style="display: flex; align-items: center; gap: 6px; padding: 6px 10px; border-radius: 14px; background: [[f]]; font-size: 13px; font-weight: 800">[[bi]][[mb]] <span style="font-weight: 700; color: #4A4458">[[mbe]]</span></span></div>',
                        CARD=CARDSTYLE, t=token(s[5], s[2], 44, v=k, sparkles=False), n=k + 1, name=s[0], rule=s[1], f=R[s[5]][3], bi=ic("bolt", 14, R[s[5]][2]), mb=s[3], mbe=s[4], FD=FD, FH=FH)
                    for k, s in enumerate(SETS))
bars = "".join(T('<div title="[[n]]: [[v]]% chance of being stolen" style="display: grid; grid-template-columns: 110px 1fr 48px; align-items: center; gap: 12px"><span style="display: flex; align-items: center; gap: 8px; font-size: 15px; font-weight: 800">[[tk]][[n]]</span><span style="height: 22px; display: block"><span style="display: block; width: [[w]]%; height: 22px; border-radius: 4px 11px 11px 4px; background: [[m]]"></span></span><span style="font-size: 18px; font-weight: 700; text-align: right; [[FD]]">[[v]]%</span></div>',
                   n=R[k][0], v=v, w=round(v / 40 * 100, 1), m=R[k][1], tk=token(k, "star", 22, v=j, sparkles=False), FD=FD)
               for j, (k, v) in enumerate(ODDS))
duels_body = T("""<div style="position: relative; width: 1440px; height: 900px; overflow: hidden; box-sizing: border-box; padding: 56px 80px; background: #FFF8EE; color: #22203A; font-family: 'Nunito', system-ui, sans-serif">
<div style="position: absolute; left: -90px; bottom: -110px; width: 420px; height: 300px; border-radius: 45% 55% 42% 58% / 55% 45% 55% 45%; background: #FFE4DA"></div>
<div style="position: absolute; right: -60px; top: -70px; width: 300px; height: 240px; border-radius: 52% 48% 60% 40% / 45% 55% 45% 55%; background: #EEE4FF"></div>
<div style="position: relative; display: grid; grid-template-columns: 560px 1fr; column-gap: 56px; height: 100%">
<div style="display: flex; flex-direction: column; gap: 18px">
<span style="align-self: flex-start; padding: 4px 14px; border-radius: 999px; background: #FFCB47; font-size: 22px; font-weight: 700; [[FH]]">new feature</span>
<h2 style="margin: 0; font-size: 76px; line-height: 0.95; font-weight: 700; letter-spacing: -0.02em; [[FD]]">Street <i style="color: #B8431F">duels</i></h2>
<p style="margin: 0; font-size: 19px; line-height: 1.5; font-weight: 600; color: #4A4458">Bump into another trainer in real life and battle for one of their FitMon. It&#39;s quick and it&#39;s fair: rare catches are hard to lose.</p>
[[FLOW]]
<div style="display: flex; flex-wrap: wrap; gap: 8px">[[RULES]]</div>
</div>
<div style="display: flex; flex-direction: column; gap: 18px; padding-top: 8px">
<span style="font-size: 26px; font-weight: 700; [[FD]]">Three sets, three <i>buffs</i></span>
<div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px">[[SETS]]</div>
<div style="padding: 22px 24px; border-radius: 30px; [[CARD]]; display: flex; flex-direction: column; gap: 12px">
<div style="display: flex; align-items: baseline; justify-content: space-between"><span style="font-size: 26px; font-weight: 700; [[FD]]">Steal <i>odds</i> by rarity</span><span style="font-size: 13px; font-weight: 700; color: #6E6878">Chance the stolen FitMon is from each tier</span></div>
[[BARS]]
<span style="font-size: 22px; font-weight: 700; color: #B8431F; [[FH]]">your Mythics are 20× safer than your Commons</span>
</div>
</div>
</div>
</div>""", FD=FD, FH=FH, CARD=CARDSTYLE, FLOW=flow_html, SETS=set_cards, BARS=bars,
    RULES="".join('<span style="display: flex; align-items: center; gap: 6px; padding: 7px 12px; border-radius: 999px; background: #FFFFFF; border: 2px solid #EADFCF; font-size: 13px; font-weight: 800">%s%s</span>' % (ic(i, 16, INK), t)
                  for i, t in [("shield", "Your 3 favorite FitMon are always safe"), ("clock", "24 h before a rematch"), ("check", "Camera checks every rep")]))
files["StreetDuels.dc.html"] = page("Street duels", duels_body, 1440, 900)

# =====================================================================
# canvas index
# =====================================================================
row2 = [("Map.dc.html", "01 · Explore map (world turns with you)"), ("Encounter.dc.html", "02 · Mythic encounter"),
        ("Street.dc.html", "03 · Street mode"), ("Gym.dc.html", "04 · Gym mode raid"),
        ("Dex.dc.html", "05 · FitDex"), ("Profile.dc.html", "06 · Trainer stats")]
row3 = [("Battle.dc.html", "07 · Online arena"), ("Finisher.dc.html", "08 · Finisher unlocked"),
        ("DuelInvite.dc.html", "09 · Street duel invite"), ("DuelLive.dc.html", "10 · Street duel, set 2"),
        ("DuelResult.dc.html", "11 · Street duel result + steal")]
boards = {"Main.dc.html": {"x": 0, "y": 0, "w": 1440, "h": 900, "title": "Pitch hero"},
          "HowItPlays.dc.html": {"x": 1520, "y": 0, "w": 1440, "h": 900, "title": "How it plays"},
          "StreetDuels.dc.html": {"x": 3040, "y": 0, "w": 1440, "h": 900, "title": "Street duels (new feature)"}}
for idx, (f, t) in enumerate(row2):
    boards[f] = {"x": idx * 470, "y": 1320, "w": 390, "h": 844, "title": t, "radius": 44, "is_interactive": True}
for idx, (f, t) in enumerate(row3):
    boards[f] = {"x": idx * 470, "y": 2544, "w": 390, "h": 844, "title": t, "radius": 44, "is_interactive": True}
canvas = {"v": 3, "createdOnFiles": {"v": 1, "at": "2026-09-24T18:54:37Z"}, "title": "FitMon GO",
          "launch": {"view": "canvas"}, "pages": [], "boards": boards, "order": list(boards.keys()),
          "notes": {"t1": {"x": 0, "y": -300, "text": "FitMon GO: pitch visuals", "kind": "title1", "maxW": 4480},
                    "t2": {"x": 0, "y": 1060, "text": "Explore & train (press Play to click through)", "kind": "title1", "maxW": 2740},
                    "t3": {"x": 0, "y": 2284, "text": "Battle & street duels", "kind": "title1", "maxW": 2270}},
          "designSystems": []}

os.makedirs(OUT, exist_ok=True)
for name, src in files.items():
    with open(os.path.join(OUT, name), "w") as fh:
        fh.write(src)
with open(os.path.join(OUT, "canvas.json"), "w") as fh:
    json.dump(canvas, fh, indent=1, ensure_ascii=False)
print("\n".join("%s %d" % (k, len(v)) for k, v in files.items()))
