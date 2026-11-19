"""Generates themed (dark + light) animated SVG cards for the profile README.
Usage: python3 render_cards.py OUT_DIR"""
import sys, io, base64, pathlib
from fontTools import subset
from fontTools.ttLib import TTFont

out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)

# ---- fonts: subset to printable ASCII + a few accents, embed as base64 WOFF ----
FONTS = {
  "MCrimson": "/usr/share/fonts/truetype/google-fonts/ofl/crimsontext/CrimsonText-SemiBold.ttf",
  "MInter":   "/usr/share/fonts/opentype/inter/Inter-Medium.otf",
  "MInterB":  "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf",
  "MMono":    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
}
_cache = {}
def font_face(name):
    if name not in _cache:
        opts = subset.Options(); opts.flavor = "woff"; opts.layout_features = ["kern", "liga"]
        f = TTFont(FONTS[name])
        s = subset.Subsetter(opts)
        s.populate(unicodes=list(range(0x20, 0x7F)) + [0xE9, 0xC9, 0x2019, 0xB7])
        s.subset(f)
        buf = io.BytesIO(); f.flavor = "woff"; f.save(buf)
        b64 = base64.b64encode(buf.getvalue()).decode()
        _cache[name] = f"@font-face{{font-family:'{name}';src:url(data:font/woff;base64,{b64}) format('woff')}}"
    return _cache[name]

SERIF = "font-family:'MCrimson',Georgia,serif"
SANS  = "font-family:'MInter',-apple-system,'Segoe UI',Arial,sans-serif"
SANSB = "font-family:'MInterB',-apple-system,'Segoe UI',Arial,sans-serif;font-weight:600"
MONO  = "font-family:'MMono',Consolas,monospace"

THEMES = {
 "dark": dict(bg0="#0b1020", bg1="#101a2e", grid="#ffffff", gridop=".045", card0="#141c2f", card1="#0d1322",
              inner="#0a0f1c", text="#f3f4f6", muted="#9ca3af", faint="#6b7280", edge="#ffffff", edgeop=".08",
              sky="#38bdf8", vio="#a78bfa", grn="#34d399", red="#f43f5e", track="#1f2937", orb=".55", knob="#ffffff"),
 "light": dict(bg0="#f8fafc", bg1="#e6ecfb", grid="#0f172a", gridop=".05", card0="#ffffff", card1="#f3f6fb",
              inner="#eef2f8", text="#0f172a", muted="#475569", faint="#64748b", edge="#0f172a", edgeop=".10",
              sky="#0284c7", vio="#7c3aed", grn="#059669", red="#e11d48", track="#d5dde9", orb=".40", knob="#ffffff"),
}

BASE_CSS = """
@keyframes rise{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes drift{0%,100%{transform:translate(0,0)}50%{transform:translate(34px,-20px)}}
@keyframes grow{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes write{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes blink{50%{opacity:0}}
@keyframes swing{0%{opacity:0;transform:translateY(26px) rotate(-2deg)}60%{opacity:1;transform:translateY(-5px) rotate(.6deg)}100%{opacity:1;transform:translateY(0) rotate(0)}}
.r{opacity:0;animation:rise .9s cubic-bezier(.2,.8,.2,1) forwards}
.f{opacity:0;animation:fade 1s ease forwards}
.fb{transform-box:fill-box}
@media (prefers-reduced-motion:reduce){*{animation:none!important;opacity:1!important;transform:none!important}}
"""

def svg(w, h, body, fonts, extra_css="", defs=""):
    ff = "".join(font_face(f) for f in fonts)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
            f'<style>{ff}{BASE_CSS}{extra_css}</style><defs>{defs}</defs>{body}</svg>')

def hero(t, P):
    W, H = 800, 300
    defs = f"""
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{P['bg0']}"/><stop offset="1" stop-color="{P['bg1']}"/></linearGradient>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{P['grid']}" stroke-opacity="{P['gridop']}"/></pattern>
    <filter id="blur"><feGaussianBlur stdDeviation="45"/></filter>
    <linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="-260" y1="0" x2="0" y2="0">
      <stop offset="0" stop-color="{P['text']}"/><stop offset=".42" stop-color="{P['text']}"/>
      <stop offset=".5" stop-color="{P['grn']}"/><stop offset=".58" stop-color="{P['text']}"/><stop offset="1" stop-color="{P['text']}"/>
      <animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="1100 0" begin="1.5s" dur="2.2s" repeatCount="1" fill="freeze"/>
    </linearGradient>
    <clipPath id="clip"><rect x="28" y="214" width="500" height="34"/></clipPath>"""
    css = ".o1{animation:drift 14s ease-in-out infinite}.o2{animation:drift 18s ease-in-out infinite reverse}.o3{animation:drift 22s ease-in-out infinite}" \
          ".type{transform-origin:left;transform-box:fill-box;animation:write 2.8s steps(46) 1.8s both}.cur{animation:blink 1s steps(1) infinite}"
    body = f"""
    <rect width="{W}" height="{H}" rx="24" fill="url(#bg)"/><rect width="{W}" height="{H}" rx="24" fill="url(#grid)"/>
    <g filter="url(#blur)" opacity="{P['orb']}">
      <circle class="o1" cx="660" cy="70" r="90" fill="{P['grn']}" opacity=".38"/>
      <circle class="o2" cx="560" cy="250" r="80" fill="{P['sky']}" opacity=".32"/>
      <circle class="o3" cx="750" cy="230" r="65" fill="{P['vio']}" opacity=".32"/>
    </g>
    <rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="23" fill="none" stroke="{P['edge']}" stroke-opacity="{P['edgeop']}"/>
    <text class="r" x="32" y="62" style="{MONO};animation-delay:.15s" font-size="14" letter-spacing="4" fill="{P['grn']}">HELLO, I AM</text>
    <text class="r" x="30" y="140" style="{SERIF};animation-delay:.4s" font-size="78" fill="url(#shine)">Maryam Imran</text>
    <text class="r" x="32" y="178" style="{SANS};animation-delay:.8s" font-size="20" fill="{P['muted']}">Builder. UBT student. Sustainability Club president.</text>
    <g clip-path="url(#clip)"><text class="type" x="32" y="238" style="{MONO}" font-size="17" fill="{P['text']}">$ building Flaire, a kill switch for AI agents</text></g>
    <rect class="cur" x="508" y="222" width="10" height="20" fill="{P['grn']}"/>
    <g class="f" style="animation-delay:1.2s">
      <circle cx="36" cy="273" r="4" fill="{P['grn']}"><animate attributeName="opacity" values="1;.25;1" dur="2s" repeatCount="indefinite"/></circle>
      <text x="50" y="278" style="{SANSB}" font-size="12" letter-spacing="1.2" fill="{P['faint']}">OPEN TO COLLABORATIONS, HACKATHONS AND ODD IDEAS</text>
    </g>"""
    (out/f"hero-{t}.svg").write_text(svg(W, H, body, ["MCrimson", "MInter", "MInterB", "MMono"], css, defs))

TW, TH = 800, 200
def tile(name, t, P, accent, tag, title, d1, d2, visual, delay):
    defs = f'<linearGradient id="tb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P["card0"]}"/><stop offset="1" stop-color="{P["card1"]}"/></linearGradient>'
    body = f"""
    <g style="animation:swing 1.1s cubic-bezier(.2,.9,.3,1.1) {delay}s both;transform-origin:50% 100%;transform-box:fill-box">
      <rect x="1.5" y="1.5" width="{TW-3}" height="{TH-3}" rx="22" fill="url(#tb)" stroke="{accent}" stroke-opacity=".45" stroke-width="1.5"/>
      <rect x="30" y="26" width="{len(tag)*10+28}" height="26" rx="13" fill="{accent}" fill-opacity=".14"/>
      <text x="44" y="44" style="{SANSB}" font-size="12" letter-spacing="1.8" fill="{accent}">{tag}</text>
      <text x="30" y="102" style="{SERIF}" font-size="42" fill="{P['text']}">{title}</text>
      <text x="30" y="136" style="{SANS}" font-size="18" fill="{P['muted']}">{d1}</text>
      <text x="30" y="160" style="{SANS}" font-size="18" fill="{P['muted']}">{d2}</text>
      <rect x="456" y="22" width="316" height="156" rx="16" fill="{P['inner']}" stroke="{P['edge']}" stroke-opacity="{P['edgeop']}"/>
      {visual}
    </g>"""
    (out/f"{name}-{t}.svg").write_text(svg(TW, TH, body, ["MCrimson", "MInter", "MInterB", "MMono"], "", defs))

def flaire(t, P):
    a = P["sky"]
    vis = f"""
    <text x="478" y="52" style="{MONO}" font-size="12" fill="{P['faint']}">AGENT 01</text>
    <rect x="478" y="62" width="200" height="10" rx="5" fill="{P['track']}"/>
    <rect class="fb" x="478" y="62" width="200" height="10" rx="5" fill="{a}" style="transform-origin:left;animation:write 4s ease-in-out infinite alternate"/>
    <rect x="706" y="48" width="52" height="26" rx="13" fill="{a}"><animate attributeName="fill" values="{a};{a};{P['red']};{P['red']};{a}" keyTimes="0;.45;.5;.95;1" dur="6s" repeatCount="indefinite"/></rect>
    <circle cy="61" r="10" fill="{P['knob']}"><animate attributeName="cx" values="745;745;719;719;745" keyTimes="0;.45;.5;.95;1" dur="6s" repeatCount="indefinite"/></circle>
    <text x="758" y="94" text-anchor="end" style="{MONO}" font-size="10" letter-spacing=".5" fill="{P['faint']}">KILL SWITCH</text>
    <text x="478" y="124" style="{MONO}" font-size="12" fill="{P['faint']}">AGENT 02</text>
    <rect x="478" y="134" width="200" height="10" rx="5" fill="{P['track']}"/>
    <rect class="fb" x="478" y="134" width="120" height="10" rx="5" fill="{P['grn']}" style="transform-origin:left;animation:write 5s ease-in-out infinite alternate-reverse"/>
    <circle cx="745" cy="139" r="5" fill="{P['grn']}"><animate attributeName="opacity" values="1;.3;1" dur="2s" repeatCount="indefinite"/></circle>
    <text x="758" y="164" text-anchor="end" style="{MONO}" font-size="10" fill="{P['faint']}">WITHIN LIMIT</text>"""
    tile("flaire", t, P, a, "BUILDING", "Flaire", "Spend control for AI agents.", "One card each, one kill switch.", vis, .2)

def career(t, P):
    a = P["vio"]; lines = ""
    for i, w in enumerate([240, 170, 270, 200]):
        lines += f'<rect class="fb" x="480" y="{50+i*22}" width="{w}" height="9" rx="4.5" fill="{a}" fill-opacity="{.95-i*.14:.2f}" style="transform-origin:left;transform:scaleX(0);animation:write .8s ease {1.3+i*.35:.2f}s forwards"/>'
    vis = f"""{lines}
    <circle cx="744" cy="56" r="16" fill="{a}" fill-opacity=".16"/>
    <path d="M736 56l6 6 10-12" fill="none" stroke="{a}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="26" stroke-dashoffset="26"><animate attributeName="stroke-dashoffset" from="26" to="0" begin="3s" dur=".5s" fill="freeze"/></path>
    <text x="480" y="160" style="{MONO}" font-size="12" fill="{P['faint']}">r&#233;sum&#233; · LinkedIn · interviews</text>"""
    tile("career", t, P, a, "SHIPPING", "Career Studio", "An AI coach for students: r&#233;sum&#233;,", "LinkedIn, applications, interviews.", vis, .45)

def green(t, P):
    a = P["grn"]; bars = ""
    for i, h in enumerate([34, 52, 44, 74, 62, 90]):
        bars += f'<rect class="fb" x="{610+i*26}" y="{160-h}" width="16" height="{h}" rx="4" fill="{a}" fill-opacity="{.45+i*.1:.2f}" style="transform-origin:bottom;transform:scaleY(0);animation:grow .8s cubic-bezier(.2,.8,.2,1) {1.2+i*.12:.2f}s forwards"/>'
    counts = ""
    for i, n in enumerate("012"):
        hide = f'<set attributeName="visibility" to="hidden" begin="{1.3+(i+1)*.45:.2f}s" fill="freeze"/>' if i < 2 else ""
        counts += f'<text x="480" y="130" style="{SERIF}" font-size="76" fill="{a}" visibility="hidden">{n}<set attributeName="visibility" to="visible" begin="{1.3+i*.45:.2f}s" fill="freeze"/>{hide}</text>'
    vis = f"""{counts}
    <text x="534" y="98" style="{MONO}" font-size="12" fill="{P['muted']}">literacy</text>
    <text x="534" y="114" style="{MONO}" font-size="12" fill="{P['muted']}">challenges</text>
    <text x="534" y="130" style="{MONO}" font-size="12" fill="{P['muted']}">run</text>{bars}"""
    tile("green", t, P, a, "LEADING", "UBT Sustainability", "President of the club. Bilingual tests", "that turn campus data into evidence.", vis, .7)

def stack(t, P):
    W, H = 800, 72
    items = ["Python", "FastAPI", "TypeScript", "React", "Tailwind", "PostgreSQL", "Supabase", "Claude API", "Vercel", "Render", "Git"]
    cols = [P["sky"], P["grn"], P["vio"]]; x, chips = 0, ""
    for i, n in enumerate(items):
        w = len(n) * 9 + 44; c = cols[i % 3]
        chips += (f'<rect x="{x}" y="19" width="{w}" height="34" rx="17" fill="{c}" fill-opacity=".12" stroke="{c}" stroke-opacity=".5"/>'
                  f'<circle cx="{x+18}" cy="36" r="4" fill="{c}"/><text x="{x+32}" y="41" style="{SANSB}" font-size="14" fill="{P["text"]}">{n}</text>')
        x += w + 12
    css = f"@keyframes scroll{{to{{transform:translateX(-{x}px)}}}}.m{{animation:scroll 30s linear infinite}}"
    defs = (f'<linearGradient id="l"><stop offset="0" stop-color="{P["card1"]}"/><stop offset="1" stop-color="{P["card1"]}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="r"><stop offset="0" stop-color="{P["card1"]}" stop-opacity="0"/><stop offset="1" stop-color="{P["card1"]}"/></linearGradient>'
            f'<clipPath id="c"><rect width="{W}" height="{H}" rx="18"/></clipPath>')
    body = f"""<rect width="{W}" height="{H}" rx="18" fill="{P['card1']}" stroke="{P['edge']}" stroke-opacity="{P['edgeop']}"/>
    <g clip-path="url(#c)"><g class="m">{chips}<g transform="translate({x},0)">{chips}</g><g transform="translate({x*2},0)">{chips}</g></g>
    <rect width="70" height="{H}" fill="url(#l)"/><rect x="{W-70}" width="70" height="{H}" fill="url(#r)"/></g>"""
    (out/f"stack-{t}.svg").write_text(svg(W, H, body, ["MInterB"], css, defs))

for t, P in THEMES.items():
    hero(t, P); flaire(t, P); career(t, P); green(t, P); stack(t, P)
print("ok")
