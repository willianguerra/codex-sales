"""Build the sales and post-purchase pages from config.json + src/.

Usage:  python build.py
Writes: sales-page-EN.html, sales-page-ES.html,
        upsell-audio-EN.html, upsell-audio-ES.html,
        downsell-audio-EN.html, downsell-audio-ES.html,
        terms-{EN,ES}.html, privacy-{EN,ES}.html (from src/legal.<LANG>.json),
        emails/free-preview-{EN,ES}.html, api/_content.js (used by api/free-preview.js)
Every price, link and variable comes from config.json; every sentence from src/copy.<LANG>.json.
"""
import json
import math
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
CFG = json.loads((ROOT / "config.json").read_text(encoding="utf8"))
CSS = (SRC / "styles.css").read_text(encoding="utf8")
JS = (SRC / "main.js").read_text(encoding="utf8")
LANGS = ["EN", "ES"]

GEEZ = "ሰማይናምድርንፈጠረእግዚአብሔርበመጀመሪያውቃልነበረቃልምበእግዚአብሔርዘንድነበረ"
GEEZ_GLYPHS = "".join(sorted(set(GEEZ + "፠፩፪፫፬፭")))

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700'
    '&family=EB+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@600;700&display=swap">'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+Ethiopic:wght@400'
    f'&display=swap&text={GEEZ_GLYPHS}">'
)

# ---------- original SVG marks ----------
CROSS = (
    '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-linecap="round" aria-hidden="true">'
    '<path d="M24 10 38 24 24 38 10 24Z" stroke-width="1.2" opacity=".7"/>'
    '<path d="M24 4v40M4 24h40" stroke-width="2.6"/>'
    '<path d="M19.5 8.5 24 4l4.5 4.5M19.5 39.5 24 44l4.5-4.5M8.5 19.5 4 24l4.5 4.5M39.5 19.5 44 24l-4.5 4.5" stroke-width="1.8"/>'
    '<circle cx="24" cy="24" r="5.5" stroke-width="2" fill="#0F0D0B"/>'
    '<circle cx="24" cy="24" r="1.6" fill="currentColor" stroke="none"/>'
    '</svg>'
)
ICON_SCROLL = ('<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
               '<path d="M9 6h15a3 3 0 0 1 3 3v1h-4"/><path d="M23 9v15a3 3 0 0 1-3 3H8a3 3 0 0 1-3-3v-1h12v1a3 3 0 0 0 3 3"/>'
               '<path d="M9 6a3 3 0 0 0-3 3v14"/><path d="M11 12h8M11 16h8M11 20h5"/></svg>')
ICON_LENS = ('<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true">'
             '<circle cx="14" cy="14" r="8"/><path d="m20 20 7 7"/><path d="M10.5 14h7M14 10.5v7" opacity=".7"/></svg>')
ICON_PHONE = ('<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true">'
              '<rect x="9" y="3" width="14" height="26" rx="3"/><path d="M14 25.5h4"/><path d="M12.5 9h7M12.5 12.5h7M12.5 16h5" opacity=".7"/></svg>')
ICON_CHECK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<path d="M4 12.5 9.5 18 20 6.5"/></svg>')
ARROW_L = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5 8 12l7 7"/></svg>'
ARROW_R = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 5 7 7-7 7"/></svg>'


def wax_seal(top, bottom):
    pts = []
    for i in range(72):
        a = i / 72 * 2 * math.pi
        r = 44 + 2.4 * math.sin(i * 1.7) + 1.6 * math.cos(i * 3.1)
        pts.append(f"{50 + r * math.cos(a):.1f},{50 + r * math.sin(a):.1f}")
    return (
        '<svg viewBox="0 0 100 100" aria-hidden="true">'
        '<defs><radialGradient id="wx" cx=".38" cy=".32" r=".75">'
        '<stop offset="0" stop-color="#a33434"/><stop offset=".6" stop-color="#7A1F1F"/><stop offset="1" stop-color="#4a1111"/></radialGradient></defs>'
        f'<polygon points="{" ".join(pts)}" fill="url(#wx)"/>'
        '<circle cx="50" cy="50" r="33" fill="none" stroke="#F3D9A8" stroke-opacity=".45" stroke-width="1"/>'
        '<circle cx="50" cy="50" r="29" fill="none" stroke="#F3D9A8" stroke-opacity=".25" stroke-width=".8" stroke-dasharray="1.5 2.5"/>'
        f'<text x="50" y="55" text-anchor="middle" font-family="Cinzel, serif" font-weight="700" font-size="30" fill="#F3D9A8">{top}</text>'
        f'<text x="50" y="70" text-anchor="middle" font-family="Inter, sans-serif" font-weight="700" font-size="8.5" letter-spacing="2" fill="#F3D9A8">{bottom}</text>'
        '</svg>'
    )


# ---------- helpers ----------
def fill(text, lang):
    """Replace {tokens} in copy with config values."""
    L = CFG[lang]
    vals = {
        "price": L["price"].replace(" ", " "), "page_count": L["page_count"], "bump_price": L["bump_price"],
        "upsell_price": L["upsell_price"], "downsell_price": L["downsell_price"],
        "year": str(CFG["year"]), "brand_name": CFG["brand_name"], "support_email": CFG["support_email"],
    }
    return re.sub(r"\{(\w+)\}", lambda m: vals.get(m.group(1), m.group(0)), text)


def deep_fill(obj, lang):
    if isinstance(obj, str):
        return fill(obj, lang)
    if isinstance(obj, list):
        return [deep_fill(x, lang) for x in obj]
    if isinstance(obj, dict):
        return {k: deep_fill(v, lang) for k, v in obj.items()}
    return obj


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def pixels_head():
    out = ""
    meta = CFG["pixels"].get("meta_pixel_id")
    gtag = CFG["pixels"].get("google_tag_id")
    if meta:
        out += ("<script>!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?"
                "n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;"
                "n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];"
                "s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');"
                f"fbq('init','{escape(str(meta))}');fbq('track','PageView');</script>")
    if gtag:
        out += (f'<script async src="https://www.googletagmanager.com/gtag/js?id={escape(str(gtag))}"></script>'
                "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
                f"gtag('js',new Date());gtag('config','{escape(str(gtag))}');</script>")
    return out


def head(lang, t, title, description, page):
    other = "ES" if lang == "EN" else "EN"
    site = CFG["site_url"].rstrip("/")
    robots = '<meta name="robots" content="noindex,nofollow">' if CFG.get("noindex") else ""
    alt = ""
    url = f"{site}/{page}"
    if page.startswith("sales-page"):
        url = f"{site}/{lang.lower()}"
        alt = (f'<link rel="canonical" href="{url}">'
               f'<link rel="alternate" hreflang="{t["lang"]}" href="{url}">'
               f'<link rel="alternate" hreflang="{"es" if other == "ES" else "en"}" href="{site}/{other.lower()}">')
    return f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
{robots}
<meta name="theme-color" content="#0F0D0B">
<meta property="og:type" content="product">
<meta property="og:locale" content="{t['locale']}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:image" content="{site}/assets/og-{lang}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
{alt}
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 48'%3E%3Crect width='48' height='48' rx='8' fill='%230F0D0B'/%3E%3Cpath d='M24 8v32M8 24h32' stroke='%23D9B46A' stroke-width='4' stroke-linecap='round'/%3E%3Ccircle cx='24' cy='24' r='6' fill='%230F0D0B' stroke='%23D9B46A' stroke-width='3'/%3E%3C/svg%3E">
{FONTS}
<style>{CSS}</style>
{pixels_head()}
</head>"""


def checkout(lang, label, text, cls="cta", extra=""):
    href = escape(CFG[lang]["checkout_url"])
    return f'<a class="{cls}" href="{href}" data-checkout="{label}"{extra}>{text}</a>'


def cta_group(lang, label, text, micro, extra="", pulse=False):
    cls = "cta pulse" if pulse else "cta"
    return f'<div class="cta-group">{checkout(lang, label, text, cls, extra)}<p class="micro">{micro}</p></div>'


def topbar(lang, t):
    other = "ES" if lang == "EN" else "EN"
    cur = f'<span aria-current="true">{lang}</span>'
    link = f'<a href="/{other.lower()}" hreflang="{other.lower()}" lang="{other.lower()}">{other}</a>'
    pair = cur + link if lang == "EN" else link + cur
    return (f'<header class="wrap topbar"><span class="mark" role="img" aria-label="{t["brand_short"]}">{CROSS}</span>'
            f'<nav class="lang" aria-label="{t["lang_label"]}">{pair}</nav></header>')


# ---------- sales page ----------
def sales_page(lang):
    t = deep_fill(json.loads((SRC / f"copy.{lang}.json").read_text(encoding="utf8")), lang)
    L = CFG[lang]
    h1 = t["hero"]["h1_" + CFG.get("headline_variant", "A")]
    micro = t["micro"]

    hero = f"""
<section class="dark hero" aria-labelledby="h1">
  <div class="geez" aria-hidden="true">{(GEEZ + " ") * 14}</div>
  {topbar(lang, t)}
  <div class="wrap">
    <p class="kicker" style="margin-top:14px">{t['hero']['eyebrow']}</p>
    <h1 id="h1"><span class="a">{h1[0]}</span><span class="b">{h1[1]}</span></h1>
    <p class="sub">{t['hero']['sub']}</p>
    <div class="hero-body">
    <div class="hero-row">
      <div class="phone"><div class="screen">
        <div class="bar"></div>
        <img src="assets/cover-{lang}.webp" width="600" height="900" alt="{escape(t['hero']['cover_alt'])}" fetchpriority="high" decoding="async">
        <div class="bar"></div>
      </div></div>
      <ul class="ticks">
        <li>{ICON_SCROLL}<span>{t['hero']['ticks'][0]}</span></li>
        <li>{ICON_LENS}<span>{t['hero']['ticks'][1]}</span></li>
        <li>{ICON_PHONE}<span>{t['hero']['ticks'][2]}</span></li>
      </ul>
    </div>
    {cta_group(lang, 'hero', t['hero']['cta'], micro, ' data-hero-cta', pulse=True)}
    </div>
  </div>
</section>"""

    i = t["ident"]
    ident = f"""
<section class="light block ident" aria-labelledby="h-ident">
  <div class="wrap">
    <h2 class="h2" id="h-ident">{i['h2']}</h2>
    <p class="roll">{i['roll']}</p>
    <p>{i['intro']}</p>
    <div class="qs"><p>{i['q'][0]}</p><p>{i['q'][1]}</p></div>
    <p>{i['body']}</p>
    <p class="turn">{i['turn']}</p>
  </div>
</section>"""

    ins = t["inside"]
    slides = ""
    for n, (cap, alt) in enumerate(zip(ins["captions"], ins["alts"]), 1):
        lazy = "" if n == 1 else ' loading="lazy"'
        slides += (f'<figure class="slide" role="group" aria-roledescription="slide" aria-label="{n} / {len(ins["captions"])}">'
                   f'<div class="leaf"><img src="assets/pg-0{n}-{lang}.webp" width="1080" height="1620" alt="{escape(alt)}"{lazy} decoding="async"></div>'
                   f'<figcaption>{cap}</figcaption></figure>')
    inside = f"""
<section class="dark block" aria-labelledby="h-inside">
  <div class="wrap">
    <h2 class="h2" id="h-inside">{ins['h2']}</h2>
    <p class="lede">{ins['sub']}</p>
    <div class="carousel" data-carousel aria-roledescription="carousel" aria-label="{ins['label']}">
      <div class="track" tabindex="0">{slides}</div>
      <div class="wrap car-ctrl">
        <button class="car-btn" type="button" data-prev aria-label="{ins['prev']}">{ARROW_L}</button>
        <span class="car-count" data-count aria-live="polite">1 / {len(ins['captions'])}</span>
        <button class="car-btn" type="button" data-next aria-label="{ins['next']}">{ARROW_R}</button>
      </div>
    </div>
    {cta_group(lang, 'inside', ins['cta'], micro)}
  </div>
</section>"""

    p = t["proof"]
    body = "".join(f"<p>{x}</p>" for x in p["body"])
    proof = f"""
<section class="light block" aria-labelledby="h-proof">
  <div class="wrap">
    <h2 class="h2" id="h-proof">{p['h2']}</h2>
    <div class="collation">
      <div class="leaf-q"><p class="src">{p['jude_label']}</p><blockquote>{p['jude']}<cite>{p['jude_cite']}</cite></blockquote></div>
      <p class="thread"><span class="knot" aria-hidden="true"></span><span>{p['thread']}</span></p>
      <div class="leaf-q"><p class="src">{p['enoch_label']}</p><blockquote>{p['enoch']}<cite>{p['enoch_cite']}</cite></blockquote></div>
    </div>
    {body}
    <p class="sourcebox"><span aria-hidden="true">📜</span><span>{p['source']}</span></p>
  </div>
</section>"""

    c = t["contents"]
    toc = ""
    for it in c["items"]:
        latin = " latin" if it["num"].isascii() or "–" in it["num"] else ""
        toc += (f'<li><span class="num{latin}" aria-hidden="true">{it["num"]}</span><div>'
                f'<p class="part">{it["part"]}</p><h3>{it["title"]}</h3><p>{it["desc"]}</p></div></li>')
    claims = "".join(f'<li><span class="seal" role="img" aria-label="{c["foh_seal_label"]}">?</span><q>{x}</q></li>' for x in c["foh_claims"])
    verdicts = "".join(f"<li>{v}</li>" for v in c["foh_verdicts"])
    contents = f"""
<section class="dark block" aria-labelledby="h-contents">
  <div class="wrap">
    <h2 class="h2" id="h-contents">{c['h2']}</h2>
    <p class="lede">{c['lede']}</p>
    <ol class="toc">{toc}</ol>
    <article class="foh" aria-labelledby="h-foh">
      <p class="tag">{c['foh_tag']}</p>
      <h3 id="h-foh">{c['foh_h3']}</h3>
      <ul class="claims">{claims}</ul>
      <p style="font-family:var(--font-ui);font-size:13px;color:var(--muted);margin-bottom:8px">{c['foh_verdicts_label']}</p>
      <ul class="verdicts">{verdicts}</ul>
      <p>{c['foh_body']}</p>
    </article>
    <div class="faith">{CROSS}<p>{c['faith']}</p></div>
  </div>
</section>"""

    o = t["offer"]
    gets = "".join(f"<li>{ICON_CHECK}<span>{g}</span></li>" for g in o["gets"])
    anchor = f'<span class="anchor">{escape(L["anchor_price"])}</span>' if L.get("anchor_price") else ""
    compare = "" if L.get("anchor_price") else f'<p class="compare">{o["compare"]}</p>'
    offer = f"""
<section class="light block" id="offer" aria-labelledby="h-offer" data-hide-bar>
  <div class="wrap">
    <div class="desk" role="img" aria-label="{escape(o['mock_alt'])}">
      <span class="candle"></span>
      <div class="tablet"><img src="assets/pg-03-{lang}.webp" width="1080" height="1620" alt="" loading="lazy" decoding="async"></div>
      <div class="phone2"><img src="assets/cover-{lang}.webp" width="600" height="900" alt="" loading="lazy" decoding="async"></div>
    </div>
    <h2 class="h2" id="h-offer">{o['h2']}</h2>
    <ul class="gets">{gets}</ul>
    <div class="price-line">{anchor}<span class="price">{escape(L['price'])}</span><span class="once">{o['once']}</span></div>
    {compare}
    {cta_group(lang, "offer", o["cta"], o["micro"])}
    <div class="guarantee">{wax_seal(o['g_seal_top'], o['g_seal_bottom'])}<div><h3>{o['g_h3']}</h3><p>{o['g_body']}</p></div></div>
  </div>
</section>"""

    testimonials = ""
    if CFG.get("show_testimonials"):
        # Fill src/testimonials.<LANG>.json with REAL, authorised quotes: [{"quote": "...", "name": "..."}]
        tf = SRC / f"testimonials.{lang}.json"
        items = json.loads(tf.read_text(encoding="utf8")) if tf.exists() else []
        if items:
            qs = "".join(f'<blockquote>{escape(x["quote"])}<cite>— {escape(x["name"])}</cite></blockquote>' for x in items)
            testimonials = f'<section class="light block testimonials"><div class="wrap"><h2 class="h2">{t["testimonials_h2"]}</h2>{qs}</div></section>'

    f = t["faq"]
    faqs = "".join(f'<details><summary><span>{q}</span><span class="pm" aria-hidden="true"></span></summary><div class="ans"><p>{a}</p></div></details>' for q, a in f["items"])
    g = t["gift"]
    ef = CFG["email_form"]
    faq = f"""
<section class="dark block" aria-labelledby="h-faq">
  <div class="wrap">
    <h2 class="h2" id="h-faq">{f['h2']}</h2>
    <div class="faq">{faqs}</div>
    <div data-hide-bar>{cta_group(lang, 'final', f['cta'], micro)}</div>
    <aside class="gift" aria-labelledby="h-gift" data-hide-bar>
      <h3 id="h-gift">{g['h3']}</h3>
      <p>{g['body']}</p>
      <form data-lead-form data-action="{escape(ef['action_url'])}" novalidate
            data-msg-ok="{escape(g['ok'])}" data-msg-err="{escape(g['err'])}" data-msg-unconfigured="{escape(g['unconfigured'])}">
        <label class="field"><span>{g['field']}</span>
          <input type="email" name="{escape(ef['field_email'])}" placeholder="{escape(g['placeholder'])}" autocomplete="email" inputmode="email" required></label>
        <input type="hidden" name="{escape(ef['field_lang'])}" value="{lang}">
        <label class="consent"><input type="checkbox" name="consent" value="yes" required><span>{g['consent']}</span></label>
        <input type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">
        <button class="btn-ghost" type="submit">{g['button']}</button>
        <p class="note">{g['note']}</p>
        <p class="status" role="status" aria-live="polite"></p>
      </form>
    </aside>
  </div>
</section>"""

    ft = t["footer"]
    email = escape(CFG["support_email"])
    footer = f"""
<footer class="dark foot" data-hide-bar>
  <div class="wrap">
    <div class="orn">{CROSS}</div>
    <p>{ft['rights']}</p>
    <nav aria-label="Legal"><a href="{legal_url('terms', lang)}">{ft['terms']}</a><a href="{legal_url('privacy', lang)}">{ft['privacy']}</a><a href="mailto:{email}">{ft['contact']} ({email})</a></nav>
    <p class="disc">{ft['disclaimer']}</p>
  </div>
</footer>"""

    bar = f"""
<div class="buybar" aria-hidden="true">
  <div class="in">
    <img src="assets/cover-thumb-{lang}.webp" width="120" height="180" alt="" loading="lazy">
    <p class="t" style="margin:0">{t['bar']['title']}<span class="p">{escape(L['price'])}</span></p>
    {checkout(lang, 'sticky', t['bar']['cta'])}
  </div>
</div>"""

    middle = proof + inside if CFG.get("proof_before_preview") else inside + proof
    html = (head(lang, t, t["title"], strip_tags(t["description"]), f"sales-page-{lang}.html")
            + "\n<body>\n<main>" + hero + ident + middle + contents + offer + testimonials + faq + "</main>"
            + footer + bar + f"\n<script>{JS}</script>\n</body>\n</html>\n")
    return html


def legal_url(kind, lang):
    return escape(CFG["legal_urls"][kind].replace("{lang}", lang))


# ---------- terms and privacy (src/legal.<LANG>.json) ----------
def legal_page(lang, kind):
    t = deep_fill(json.loads((SRC / f"copy.{lang}.json").read_text(encoding="utf8")), lang)
    g = deep_fill(json.loads((SRC / f"legal.{lang}.json").read_text(encoding="utf8")), lang)
    d = g[kind]
    body = "".join(f"<h2>{sec['h']}</h2>" + "".join(f"<p>{x}</p>" for x in sec["p"]) for sec in d["sections"])
    return (head(lang, t, f"{d['title']} · {CFG['brand_name']}", d["description"], f"{kind}-{lang}") + f"""
<body>
<main class="dark legal">
  <div class="wrap">
    <p class="kicker"><a href="/{lang.lower()}">&larr; {g['back']}</a></p>
    <h1>{d['title']}</h1>
    <p class="updated">{g['updated']}</p>
    {body}
  </div>
</main>
</body>
</html>
""")


# ---------- post-purchase pages ----------
def offer_page(lang, kind):
    t = deep_fill(json.loads((SRC / f"copy.{lang}.json").read_text(encoding="utf8")), lang)
    u = t[kind]
    price = CFG[lang]["upsell_price" if kind == "upsell" else "downsell_price"]
    gets = list(u["gets"])
    if kind == "upsell" and CFG.get("upsell_only_here"):
        gets.append(u["only_here"])
    lis = "".join(f"<li>{ICON_CHECK}<span>{x}</span></li>" for x in gets)
    bars = "".join(f'<i style="height:{int(18 + 38 * abs(math.sin(k * .7) * math.cos(k * .23)))}px"></i>' for k in range(36))
    no_href = CFG["upsell_next_url"][lang] if kind == "upsell" else "#"
    page = f"{kind}-audio-{lang}.html"
    widget = CFG.get("hotmart_widget_html", {}).get(f"{kind}_{lang}", "")
    return (head(lang, t, u["title"], strip_tags(u["lead"]), page) + f"""
<body>
<p class="confirm">{u['confirm']}</p>
<main class="dark ups">
  <div class="wrap">
    <p class="kicker">{t['brand_short']}</p>
    <h1>{u['h1']}</h1>
    <p class="lead">{u['lead']}</p>
    <div class="wave" aria-hidden="true">{bars}</div>
    <ul class="gets">{lis}</ul>
    <div class="price-line"><span class="price">{escape(price)}</span><span class="once">{u['price_suffix']}</span></div>
    <div class="widget-slot">
      <!-- HOTMART_ONE_CLICK_WIDGET -->
      {widget or f'<div class="placeholder">{u["widget_note"]}<br>“{u["yes"]}” / “{u["no"]}”</div>'}
    </div>
    <a class="no-thanks" href="{escape(no_href)}">{u['no']}</a>
  </div>
</main>
</body>
</html>
""")



# ---------- free-preview email (sent by api/free-preview.js through Resend) ----------
def email_html(lang):
    t = deep_fill(json.loads((SRC / f"copy.{lang}.json").read_text(encoding="utf8")), lang)
    e = t["email"]
    site = CFG["site_url"].rstrip("/")
    href = escape(CFG[lang]["checkout_url"] + ("&" if "?" in CFG[lang]["checkout_url"] else "?") + "src=email-preview")
    serif = "Georgia, 'Times New Roman', serif"
    sans = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
    li = "".join(f'<tr><td valign="top" style="padding:4px 10px 4px 0;color:#B8893B;font-family:{sans};font-size:16px">&#10003;</td>'
                 f'<td style="padding:4px 0;font-family:{serif};font-size:17px;line-height:1.45;color:#1B1712">{x}</td></tr>' for x in e["inside"])
    steps = "".join(f'<tr><td valign="top" style="padding:6px 12px 6px 0"><span style="display:inline-block;width:26px;height:26px;line-height:26px;border-radius:13px;background:#0F0D0B;color:#D9B46A;text-align:center;font-family:{sans};font-size:13px;font-weight:700">{n}</span></td>'
                    f'<td style="padding:6px 0;font-family:{serif};font-size:17px;line-height:1.45;color:#1B1712">{x}</td></tr>' for n, x in enumerate(e["steps"], 1))
    return f"""<!doctype html>
<html lang="{t['lang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>{escape(e['subject'])}</title></head>
<body style="margin:0;padding:0;background:#E9DCC0">
<div style="display:none;max-height:0;overflow:hidden;opacity:0">{escape(e['preheader'])}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#E9DCC0"><tr><td align="center" style="padding:24px 12px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;background:#F3EAD7;border-radius:10px;overflow:hidden">
  <tr><td align="center" style="background:#0F0D0B;padding:32px 24px 26px">
    <img src="{site}/assets/email-cover-{lang}.jpg" width="120" height="180" alt="{escape(t['brand_short'])}" style="display:block;border:1px solid #6b5530;border-radius:3px">
    <p style="margin:18px 0 0;font-family:{serif};font-size:13px;letter-spacing:4px;text-transform:uppercase;color:#B8893B">{t['brand_short']}</p>
    <h1 style="margin:8px 0 0;font-family:{serif};font-size:26px;line-height:1.25;font-weight:normal;color:#D9B46A">{e['h1']}</h1>
  </td></tr>
  <tr><td style="padding:28px 28px 8px">
    <p style="margin:0 0 14px;font-family:{serif};font-size:17px;line-height:1.55;color:#1B1712">{e['intro']}</p>
    <table role="presentation" cellpadding="0" cellspacing="0">{li}</table>
    <p style="margin:12px 0 0;font-family:{sans};font-size:13px;color:#6B5C48">&#128206; {e['attachment']}</p>
  </td></tr>
  <tr><td style="padding:20px 28px 0">
    <h2 style="margin:0 0 8px;font-family:{serif};font-size:20px;font-weight:normal;color:#7A1F1F">{e['full_h2']}</h2>
    <p style="margin:0;font-family:{serif};font-size:17px;line-height:1.55;color:#1B1712">{e['full']}</p>
  </td></tr>
  <tr><td style="padding:24px 28px 0">
    <h2 style="margin:0 0 8px;font-family:{serif};font-size:20px;font-weight:normal;color:#7A1F1F">{e['how_h2']}</h2>
    <table role="presentation" cellpadding="0" cellspacing="0">{steps}</table>
  </td></tr>
  <tr><td align="center" style="padding:24px 28px 8px">
    <a href="{href}" style="display:block;background:#D9A441;color:#14100C;text-decoration:none;font-family:{sans};font-size:18px;font-weight:700;line-height:1.2;padding:18px 20px;border-radius:8px">{e['cta']}</a>
    <p style="margin:12px 0 0;font-family:{sans};font-size:13px;line-height:1.5;color:#6B5C48">&#128274; {e['guarantee']}</p>
  </td></tr>
  <tr><td style="padding:22px 28px 28px">
    <p style="margin:0;font-family:{serif};font-size:17px;color:#1B1712">{e['sign']}<br><em>{escape(CFG['brand_name'])}</em></p>
  </td></tr>
  <tr><td style="background:#0F0D0B;padding:20px 28px">
    <p style="margin:0;font-family:{sans};font-size:12px;line-height:1.6;color:#9C8E7A">{e['footer']}</p>
    <p style="margin:10px 0 0;font-family:{sans};font-size:12px;line-height:1.6;color:#9C8E7A">{e['unsub']} <a href="%%UNSUBSCRIBE_URL%%" style="color:#D9B46A">{e['unsub_link']}</a></p>
  </td></tr>
</table></td></tr></table>
</body></html>
"""


def email_text(lang):
    t = deep_fill(json.loads((SRC / f"copy.{lang}.json").read_text(encoding="utf8")), lang)
    e = t["email"]
    href = CFG[lang]["checkout_url"] + ("&" if "?" in CFG[lang]["checkout_url"] else "?") + "src=email-preview"
    lines = [strip_tags(e["h1"]), "", strip_tags(e["intro"])] + [f"- {strip_tags(x)}" for x in e["inside"]]
    lines += ["", strip_tags(e["full_h2"]), strip_tags(e["full"]), "", strip_tags(e["how_h2"])]
    lines += [f"{n}. {strip_tags(x)}" for n, x in enumerate(e["steps"], 1)]
    lines += ["", f"{strip_tags(e['cta'])}: {href}", "", strip_tags(e["guarantee"]), "", e["sign"], CFG["brand_name"], "", "--", strip_tags(e["footer"]), f"{e['unsub']} {e['unsub_link']}: %%UNSUBSCRIBE_URL%%"]
    return "\n".join(lines)


def sequence_footer(lang):
    """Footer for the day 2/4/6 emails built in Resend. {{{contact.unsubscribe_url}}} is each lead's signed link (api/unsubscribe.js)."""
    t = deep_fill(json.loads((SRC / f"copy.{lang}.json").read_text(encoding="utf8")), lang)
    e = t["email"]
    sans = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
    return f"""<!-- Rodapé da sequência ({lang}). Cole no fim de cada e-mail dos dias 2, 4 e 6 no Resend. -->
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;margin:0 auto"><tr><td style="background:#0F0D0B;padding:20px 28px">
  <p style="margin:0;font-family:{sans};font-size:12px;line-height:1.6;color:#9C8E7A">{e['seq_footer']}</p>
  <p style="margin:10px 0 0;font-family:{sans};font-size:12px;line-height:1.6;color:#9C8E7A">{e['unsub']} <a href="{{{{{{contact.unsubscribe_url}}}}}}" style="color:#D9B46A">{e['unsub_link']}</a></p>
</td></tr></table>
"""


def write_email_bundle():
    """emails/*.html for preview + api/_content.js with subject, html, text and the preview PDF (base64)."""
    import base64
    (ROOT / "emails").mkdir(exist_ok=True)
    bundle = {"site_url": CFG["site_url"], "support_email": CFG["support_email"]}
    for lang in LANGS:
        t = deep_fill(json.loads((SRC / f"copy.{lang}.json").read_text(encoding="utf8")), lang)
        html = email_html(lang)
        (ROOT / "emails" / f"free-preview-{lang}.html").write_text(html, encoding="utf8")
        (ROOT / "emails" / f"sequence-footer-{lang}.html").write_text(sequence_footer(lang), encoding="utf8")
        pdf = ROOT / "previews" / f"the-ethiopian-codex-{lang}-preview.pdf"
        bundle[lang] = {
            "subject": t["email"]["subject"],
            "html": html,
            "text": email_text(lang),
            "filename": t["email"]["attachment"],
            "pdf_base64": base64.b64encode(pdf.read_bytes()).decode("ascii"),
        }
        print(f"emails/free-preview-{lang}.html  + {pdf.name} ({pdf.stat().st_size / 1024:.0f} KB)")
    (ROOT / "api").mkdir(exist_ok=True)
    (ROOT / "api" / "_content.js").write_text(
        "// Generated by build.py — do not edit. Source: src/copy.*.json + previews/*.pdf\n"
        f"module.exports = {json.dumps(bundle, ensure_ascii=False)};\n", encoding="utf8")

if __name__ == "__main__":
    for lang in LANGS:
        out = {
            f"sales-page-{lang}.html": sales_page(lang),
            f"upsell-audio-{lang}.html": offer_page(lang, "upsell"),
            f"downsell-audio-{lang}.html": offer_page(lang, "downsell"),
            f"terms-{lang}.html": legal_page(lang, "terms"),
            f"privacy-{lang}.html": legal_page(lang, "privacy"),
        }
        for name, html in out.items():
            (ROOT / name).write_text(html, encoding="utf8")
            left = re.findall(r"\{[a-z_]+\}|\[VERIFICAR[^\]]*\]", html)
            print(f"{name:28s} {len(html.encode('utf8')) / 1024:6.1f} KB" + (f"  UNRESOLVED: {left}" if left else ""))
    write_email_bundle()
