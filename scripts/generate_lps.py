#!/usr/bin/env python3
"""
Generator script for 74+ SEO Landing Pages for Schipper Compact Wonen.
Preserves 100% of authentic WordPress text and SEO metadata,
rebuilding every page in the modern Scandinavian design language.
"""

import os
import json
import re
from html import unescape

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load cache and database
with open(os.path.join(BASE_DIR, 'lp_cache.json'), 'r', encoding='utf-8') as f:
    cache = json.load(f)

with open(os.path.join(BASE_DIR, 'database.json'), 'r', encoding='utf-8') as f:
    db = json.load(f)

with open(os.path.join(BASE_DIR, 'scripts', 'svg_sprite.html'), 'r', encoding='utf-8') as f:
    SVG_SPRITE = f.read()

# Filter products to those with existing local images on disk
RAW_PRODUCTS = db.get('staopstoelen', [])
PRODUCTS = [
    p for p in RAW_PRODUCTS
    if p.get('image') and os.path.exists(os.path.join(BASE_DIR, p['image']))
]

CITY_INFO = {
    'barendrecht': {
        'name': 'Barendrecht',
        'travel': 'slechts 15 minuten rijden via de A16',
        'intro': 'Woont u in Barendrecht of Carnisselande en zoekt u een hoogwaardige sta-op stoel of zorghulpmiddel op maat?',
        'delivery': 'Gratis bezorging en persoonlijke montage in Barendrecht en omstreken.'
    },
    'hendrik-ido-ambacht': {
        'name': 'Hendrik-Ido-Ambacht',
        'travel': 'slechts 10 minuten rijden via de N3 of A16',
        'intro': 'Woont u in Hendrik-Ido-Ambacht of de Volgerlanden en zoekt u ergonomisch zit- of ligcomfort?',
        'delivery': 'Gratis bezorging, afstelling en nazorg aan huis in Hendrik-Ido-Ambacht.'
    },
    'ridderkerk': {
        'name': 'Ridderkerk',
        'travel': 'slechts 15 minuten rijden via de A16 / A15',
        'intro': 'Woont u in Ridderkerk, Drievliet of Bolnes en bent u op zoek naar een deskundig aangemeten sta-op stoel?',
        'delivery': 'Kosteloze bezorging en ergonomische afstelling aan huis in Ridderkerk.'
    },
    'alblasserdam': {
        'name': 'Alblasserdam',
        'travel': 'slechts 12 minuten rijden via de N3',
        'intro': 'Woont u in Alblasserdam en zoekt u een betrouwbare specialist in sta-op stoelen of seniorencomfort?',
        'delivery': 'Persoonlijke levering en service aan huis in heel Alblasserdam.'
    },
    'rotterdam': {
        'name': 'Rotterdam',
        'travel': 'slechts 20 minuten rijden via de A16',
        'intro': 'Woont u in Rotterdam of Rotterdam-Zuid en zoekt u maatwerk zitcomfort of een erkende Fitform dealer?',
        'delivery': 'Snelle levering, vakkundige montage en gratis proefzitten aan huis in heel Rotterdam.'
    },
    'dordrecht': {
        'name': 'Dordrecht',
        'travel': 'gevestigd in uw eigen stad aan de Singel 313 (gratis parkeren)',
        'intro': 'Woont u in Dordrecht en wilt u ontspannen proefzitten bij dé lokale zit- en zorgspecialist?',
        'delivery': 'Als Dordts familiebedrijf leveren en installeren wij gratis bij u thuis in alle wijken van Dordrecht.'
    }
}

def detect_city(slug, title):
    combined = (slug + ' ' + title).lower()
    for city_key, city_data in CITY_INFO.items():
        if city_key in combined:
            return city_data
    return None

def clean_content(raw_html, title, root_rel='../../'):
    """Extract and sanitize text from Elementor markup, fix links, preserve semantics."""
    # 1. Strip WPForms and button widgets
    raw_html = re.sub(r'<div[^>]*elementor-widget-wpforms[\s\S]*?</div>\s*</div>\s*</div>', '', raw_html)
    raw_html = re.sub(r'<div[^>]*elementor-widget-button[\s\S]*?</div>\s*</div>\s*</div>', '', raw_html)
    raw_html = re.sub(r'<div[^>]*elementor-widget-image[\s\S]*?</div>\s*</div>\s*</div>', '', raw_html)
    raw_html = re.sub(r'<div[^>]*elementor-widget-divider[\s\S]*?</div>\s*</div>\s*</div>', '', raw_html)

    # 2. Extract text editor widget contents
    editor_parts = re.findall(r'<div class=\"elementor-widget-container\">([\s\S]*?)</div>', raw_html)
    if not editor_parts:
        content = raw_html
    else:
        content = '\n\n'.join(editor_parts)

    # 3. Strip script, style, comments
    content = re.sub(r'<script[\s\S]*?</script>', '', content)
    content = re.sub(r'<style[\s\S]*?</style>', '', content)
    content = re.sub(r'<!--[\s\S]*?-->', '', content)

    # 4. Clean attributes
    content = re.sub(r'\s+(class|style|id|data-[a-zA-Z0-9_\-]+)=\"[^\"]*\"', '', content)

    # 5. Convert h1 to h2, h4 to h3
    content = re.sub(r'<h1[^>]*>(.*?)</h1>', r'<h2>\1</h2>', content)
    content = re.sub(r'<h4[^>]*>(.*?)</h4>', r'<h3>\1</h3>', content)

    # 6. Remove duplicate top heading if it matches page title
    clean_title = ''.join(c.lower() for c in title if c.isalnum())
    match = re.match(r'^\s*<h[23][^>]*>(.*?)</h[23]>', content, re.DOTALL)
    if match:
        h_text = ''.join(c.lower() for c in match.group(1) if c.isalnum())
        if h_text and (h_text in clean_title or clean_title in h_text):
            content = content[match.end():].strip()

    # 7. Fix internal links
    content = re.sub(r'href=\"(?:https?://schippercompactwonen\.nl)?/advies-afspraak/?\"', 'href=\"javascript:openBookingModal(\'content-link\')\"', content)
    content = re.sub(r'href=\"(?:https?://schippercompactwonen\.nl)?/contact/?\"', 'href=\"#contact\"', content)
    content = re.sub(r'href=\"(?:https?://schippercompactwonen\.nl)?/cat/zitcomfort[^\"]*\"', f'href=\"{root_rel}collectie.html?cat=zitcomfort\"', content)
    content = re.sub(r'href=\"(?:https?://schippercompactwonen\.nl)?/cat/ligcomfort[^\"]*\"', f'href=\"{root_rel}collectie.html?cat=ligcomfort\"', content)
    content = re.sub(r'href=\"(?:https?://schippercompactwonen\.nl)?/cat/zorgcomfort[^\"]*\"', f'href=\"{root_rel}collectie.html?cat=zorgcomfort\"', content)
    content = re.sub(r'href=\"(?:https?://schippercompactwonen\.nl)?/zitcomfort/?\"', f'href=\"{root_rel}collectie.html?cat=zitcomfort\"', content)
    content = re.sub(r'href=\"(?:https?://schippercompactwonen\.nl)?/ligcomfort/?\"', f'href=\"{root_rel}collectie.html?cat=ligcomfort\"', content)
    content = re.sub(r'href=\"(?:https?://schippercompactwonen\.nl)?/zorgcomfort/?\"', f'href=\"{root_rel}collectie.html?cat=zorgcomfort\"', content)
    content = re.sub(r'href=\"(?:https?://schippercompactwonen\.nl)?/informatie/?\"', f'href=\"{root_rel}index.html#werkwijze\"', content)
    content = re.sub(r'href=\"(?:https?://)?callto:[0-9]+\"', 'href=\"tel:0786314858\"', content)
    content = re.sub(r'href=\"#contact\"', 'href=\"#contact\"', content)

    # 8. Clean empty tags and non-breaking space paragraphs
    content = re.sub(r'<p>\s*(?:&nbsp;|&#160;|\s|<br\s*/?>|<em>\s*(?:&nbsp;|&#160;|\s)*\s*</em>)*</p>', '', content)
    content = re.sub(r'<h[234]>\s*</h[234]>', '', content)
    content = re.sub(r'<em>\s*</em>', '', content)
    content = re.sub(r'<p>\s*</p>', '', content)

    # 9. Remove trailing contact headings if followed by nothing
    content = re.sub(r'<h[23][^>]*>(?:Neem contact|Contact opnemen|Maak een afspraak|Heeft u nog vragen)[^<]*</h[23]>\s*$', '', content, flags=re.IGNORECASE)

    return content.strip()

def pick_products(slug, title, content):
    text = (slug + ' ' + title + ' ' + content).lower()
    
    # Priority matching
    if 'fitform' in text:
        matches = [p for p in PRODUCTS if 'fitform' in p['name'].lower() and p.get('condition') != 'occasion']
        if len(matches) < 3:
            matches.extend([p for p in PRODUCTS if 'fitform' in p['name'].lower() and p not in matches])
    elif 'senioren' in text or 'fauteuil' in text or 'relax' in text:
        matches = [p for p in PRODUCTS if p.get('subcategory') == 'Relaxstoelen' or any(k in p['name'].lower() for k in ['farstrup', 'dylan', 'zwolle', 'cantate', 'casa'])]
    elif 'bed' in text or 'ligcomfort' in text:
        matches = [p for p in PRODUCTS if p.get('category') == 'Ligcomfort']
    elif 'rollator' in text or 'traplift' in text or 'zorgcomfort' in text:
        matches = [p for p in PRODUCTS if p.get('category') == 'Zorgcomfort']
    else:
        # Standard bestseller sta-op stoelen
        matches = [p for p in PRODUCTS if any(k in p['name'].lower() for k in ['fitform 570', 'alfred', 'rotterdam', 'dordrecht', 'sliedrecht', 'zwijndrecht'])]
    
    if len(matches) < 3:
        for p in PRODUCTS:
            if p not in matches:
                matches.append(p)
            if len(matches) >= 3:
                break
    return matches[:3]

def generate_lp_html(lp_item, is_rotterdam=False):
    slug = lp_item['slug']
    title = unescape(lp_item['title']['rendered'])
    yoast = lp_item.get('yoast_head_json', {})
    
    meta_title = yoast.get('title') or f"{title} | Schipper Compact Wonen"
    meta_desc = yoast.get('description') or f"Deskundig advies en groot assortiment {title}. Kom proefzitten in onze showroom in Dordrecht of kies voor gratis proefzitten aan huis."
    canonical = f"https://schippercompactwonen.nl/lp/{slug}/" if not is_rotterdam else "https://schippercompactwonen.nl/sta-op-stoelen-rotterdam/"
    
    root_rel = '../' if is_rotterdam else '../../'
    
    raw_content = lp_item.get('content', {}).get('rendered', '')
    article_html = clean_content(raw_content, title, root_rel=root_rel)
    
    city = detect_city(slug, title)
    featured_products = pick_products(slug, title, article_html)
    
    short_title = title.replace('Sta op stoel', '').replace('Fitform', '').strip()
    if not short_title:
        short_title = title

    # Build products cards HTML
    prod_cards_html = ""
    for prod in featured_products:
        p_name = prod['name']
        p_img = prod.get('image', 'assets/chair_custom.png')
        if not p_img.startswith('http'):
            p_img = f"{root_rel}{p_img}"
        p_badge = prod.get('badge') or ('Nieuw op maat' if prod.get('condition') == 'nieuw' else 'Direct leverbaar')
        p_price = f"&euro;&nbsp;{prod['price']}" if prod.get('price') else "Prijs op aanvraag"
        p_id = prod.get('id', '')
        
        specs = prod.get('specifications', {})
        spec_line = specs.get('Maatwerk') or specs.get('Merk') or '100% Ergonomisch zitcomfort'
        
        prod_cards_html += f"""
        <div class="prod-card">
          <div class="prod-card-top">
            <span class="badge">{p_badge}</span>
            <div class="prod-img-box">
              <img src="{p_img}" alt="{p_name}" loading="lazy" onerror="this.src='{root_rel}assets/chair_custom.png'">
            </div>
          </div>
          <div class="prod-card-body">
            <h3>{p_name}</h3>
            <p class="spec-note">{spec_line}</p>
            <div class="prod-foot">
              <div class="price">{p_price}</div>
              <a href="{root_rel}collectie.html?id={p_id}" class="btn-card">Bekijk stoel</a>
            </div>
          </div>
        </div>
        """

    # City sidebar block
    city_sidebar_html = ""
    if city:
        city_sidebar_html = f"""
        <div class="side-card side-region">
          <div class="side-region-head">
            <svg class="ic" aria-hidden="true"><use href="#i-map-pin"/></svg>
            <div>
              <h4>Regio {city['name']}</h4>
              <small>{city['travel']}</small>
            </div>
          </div>
          <p>{city['intro']}</p>
          <div class="side-check">
            <span>&#10003; <strong>Gratis thuisadvies</strong> in {city['name']}</span>
            <span>&#10003; <strong>Eigen bezorgdienst</strong> &amp; vakkundige montage</span>
            <span>&#10003; <strong>Showroom Dordrecht:</strong> Singel 313 (gratis parkeren)</span>
          </div>
          <button onclick="openBookingModal('sidebar-region')" class="btn btn-clay btn-sm w-full">
            <svg class="ic" aria-hidden="true"><use href="#i-calendar"/></svg>Afspraak inplannen
          </button>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{meta_title}</title>
  <meta name="description" content="{meta_desc}">
  <link rel="canonical" href="{canonical}">
  
  <!-- Open Graph -->
  <meta property="og:locale" content="nl_NL">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{meta_title}">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:site_name" content="Schipper Compact Wonen">
  
  <!-- Favicons -->
  <link rel="icon" type="image/svg+xml" href="{root_rel}favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="{root_rel}favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="{root_rel}favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="{root_rel}apple-touch-icon.png">
  <link rel="manifest" href="{root_rel}site.webmanifest">
  <meta name="theme-color" content="#A3B18A">
  <meta name="version" content="3.2.0">
  
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,400..700,100;1,9..144,400..600,100&family=Figtree:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <!-- Inline Styles -->
  <style>
    :root {{
      --sage:#A3B18A; --sage-l:#DCE3CF; --sage-xl:#EEF1E6; --moss:#588157; --forest:#344E41;
      --oat:#EDE6DA; --oat-d:#E2D8C6; --linen:#FAF7F1; --clay:#C4805F; --clay-d:#A9663F; --clay-l:#F1D9CB;
      --ink:#3D3B36; --muted:#6E6A60; --line:#DDD3C2;
    }}
    *,*::before,*::after {{ box-sizing:border-box }}
    html {{ scroll-behavior:smooth; overflow-x:clip; scrollbar-gutter:stable }}
    body {{
      margin:0; font-family:'Figtree',system-ui,sans-serif; color:var(--ink);
      background:var(--linen); line-height:1.65; -webkit-font-smoothing:antialiased;
      background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 .35 0 0 0 0 .3 0 0 0 0 .2 0 0 0 .05 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
    }}
    img {{ max-width:100%; display:block; height:auto }}
    a {{ color:inherit; text-decoration:none }}
    button {{ font:inherit; cursor:pointer; border:0; background:none; color:inherit }}
    .ic {{ display:inline-block; flex-shrink:0; vertical-align:middle; width:1.15em; height:1.15em }}
    .hidden {{ display:none!important }}
    .wrap {{ max-width:1200px; margin:0 auto; padding:0 24px }}
    h1,h2,h3,h4,.serif {{
      font-family:'Fraunces',Georgia,serif; font-variation-settings:'SOFT' 100,'WONK' 0;
      font-weight:500; color:var(--forest); margin:0; letter-spacing:-.01em; line-height:1.2;
    }}
    p {{ margin:0 }}

    /* Buttons */
    .btn {{
      display:inline-flex; align-items:center; justify-content:center; gap:10px;
      padding:14px 26px; border-radius:999px; font-weight:600; font-size:15px;
      transition:transform .2s ease, background .2s ease, box-shadow .2s ease; white-space:nowrap;
    }}
    .btn:hover {{ transform:translateY(-2px) }}
    .btn-primary {{ background:var(--forest); color:var(--linen); box-shadow:0 10px 24px -12px rgba(52,78,65,.7) }}
    .btn-primary:hover {{ background:var(--moss) }}
    .btn-clay {{ background:var(--clay); color:#fff; box-shadow:0 10px 24px -12px rgba(169,102,63,.8) }}
    .btn-clay:hover {{ background:var(--clay-d) }}
    .btn-ghost {{ background:transparent; color:var(--forest); border:1.5px solid var(--forest) }}
    .btn-ghost:hover {{ background:var(--forest); color:var(--linen) }}
    .btn-sm {{ padding:10px 18px; font-size:14px }}
    .w-full {{ width:100% }}

    /* Header */
    .strip {{ font-size:13px; color:var(--muted); padding:10px 0 0 }}
    .strip .wrap {{ display:flex; justify-content:center; gap:28px; flex-wrap:wrap }}
    .strip span, .strip a {{ display:inline-flex; align-items:center; gap:6px }}
    .strip .ic {{ color:var(--moss) }}
    header#main-header {{ position:sticky; top:12px; z-index:40; margin:12px auto 0; max-width:1200px; padding:0 16px }}
    .navbar {{
      display:flex; align-items:center; justify-content:space-between; gap:16px;
      background:rgba(250,247,241,.94); backdrop-filter:blur(10px);
      border:1px solid var(--line); border-radius:999px; padding:10px 10px 10px 22px; transition:box-shadow .3s;
    }}
    header.scrolled .navbar {{ box-shadow:0 14px 30px -18px rgba(61,59,54,.35) }}
    .logo {{ display:flex; align-items:center; gap:10px }}
    .logo-mark {{
      width:34px; height:40px; border-radius:999px 999px 8px 8px; background:var(--sage);
      display:grid; place-items:center; color:var(--forest); font-family:'Fraunces',serif; font-weight:600; font-size:18px; padding-top:4px;
    }}
    .logo b {{ font-family:'Fraunces',serif; font-weight:600; font-size:21px; color:var(--forest); display:block; line-height:1 }}
    .logo small {{ display:block; font-size:10px; letter-spacing:.24em; text-transform:uppercase; color:var(--muted); font-weight:600; margin-top:3px }}
    .nav {{ display:flex; gap:6px }}
    .nav a {{ padding:9px 16px; border-radius:999px; font-weight:500; font-size:15px; color:var(--ink); transition:background .2s, color .2s }}
    .nav a:hover {{ background:var(--sage-xl); color:var(--forest) }}
    .hdr-right {{ display:flex; align-items:center; gap:10px }}
    .menu-btn {{ display:none; width:44px; height:44px; border-radius:50%; background:var(--sage-xl); color:var(--forest); place-items:center }}
    .menu-btn .ic {{ width:22px; height:22px }}
    #mobile-menu {{ margin-top:8px; background:var(--linen); border:1px solid var(--line); border-radius:28px; padding:14px; box-shadow:0 20px 40px -20px rgba(61,59,54,.35) }}
    #mobile-menu a.ml {{ display:block; padding:12px 14px; border-radius:16px; font-weight:500 }}
    #mobile-menu a.ml:hover {{ background:var(--sage-xl) }}
    #mobile-menu .mm-cta {{ display:grid; gap:8px; margin-top:8px }}

    /* Breadcrumbs */
    .breadcrumbs {{ padding:24px 0 12px; font-size:13px; color:var(--muted) }}
    .breadcrumbs a {{ color:var(--moss); font-weight:500 }}
    .breadcrumbs a:hover {{ text-decoration:underline }}
    .breadcrumbs span.sep {{ margin:0 8px; opacity:.5 }}

    /* Hero */
    .lp-hero {{ padding:32px 0 44px }}
    .lp-hero-box {{
      background:linear-gradient(135deg, rgba(255,255,255,.9) 0%, rgba(238,241,230,.6) 100%);
      border:1px solid var(--line); border-radius:32px; padding:48px 44px; position:relative; overflow:hidden;
    }}
    .eyebrow {{ display:inline-flex; align-items:center; gap:8px; font-size:13px; font-weight:700; letter-spacing:.12em; text-transform:uppercase; color:var(--moss); margin-bottom:14px }}
    .eyebrow .ic {{ width:14px; height:14px }}
    .lp-hero h1 {{ font-size:clamp(30px, 4.2vw, 48px); margin-bottom:18px; color:var(--forest); max-width:850px }}
    .lp-hero-lede {{ font-size:18px; color:var(--muted); line-height:1.6; max-width:760px; margin-bottom:28px }}
    .lp-hero-actions {{ display:flex; gap:14px; flex-wrap:wrap; margin-bottom:32px }}
    .usp-pills {{ display:flex; gap:16px 24px; flex-wrap:wrap; padding-top:24px; border-top:1px solid rgba(221,211,194,.6); font-size:14px; font-weight:500; color:var(--forest) }}
    .usp-pills span {{ display:inline-flex; align-items:center; gap:6px }}
    .usp-pills .ic {{ color:var(--moss); width:16px; height:16px }}

    /* Layout */
    .lp-layout {{ display:grid; grid-template-columns:1fr 340px; gap:48px; padding-bottom:72px }}
    
    /* Article Content */
    .lp-article {{
      background:#fff; border:1px solid var(--line); border-radius:28px; padding:44px 48px; box-shadow:0 10px 30px -20px rgba(61,59,54,.15);
    }}
    .lp-article h2 {{ font-size:26px; margin:36px 0 16px; color:var(--forest); border-bottom:1.5px solid var(--sage-l); padding-bottom:8px }}
    .lp-article h2:first-child {{ margin-top:0 }}
    .lp-article h3 {{ font-size:20px; margin:24px 0 12px; color:var(--moss) }}
    .lp-article p {{ font-size:16px; line-height:1.75; color:var(--ink); margin-bottom:18px }}
    .lp-article ul, .lp-article ol {{ margin:0 0 20px 24px; padding:0; font-size:16px; line-height:1.7 }}
    .lp-article li {{ margin-bottom:8px }}
    .lp-article strong {{ color:var(--forest) }}
    .lp-article a {{ color:var(--clay); font-weight:600; text-decoration:underline; text-underline-offset:2px }}
    .lp-article a:hover {{ color:var(--clay-d) }}

    /* Sidebar */
    .lp-sidebar {{ display:flex; flex-direction:column; gap:24px }}
    .side-card {{
      background:#fff; border:1px solid var(--line); border-radius:24px; padding:28px; box-shadow:0 8px 24px -16px rgba(61,59,54,.15);
    }}
    .side-region {{ background:linear-gradient(135deg, #FAF7F1 0%, #EEF1E6 100%); border-color:var(--sage) }}
    .side-region-head {{ display:flex; gap:12px; align-items:center; margin-bottom:14px }}
    .side-region-head .ic {{ width:28px; height:28px; color:var(--moss) }}
    .side-region-head h4 {{ font-size:18px; margin:0 }}
    .side-region-head small {{ color:var(--moss); font-weight:600; font-size:12px }}
    .side-region p {{ font-size:14px; color:var(--muted); line-height:1.5; margin-bottom:16px }}
    .side-check {{ display:grid; gap:8px; font-size:13px; margin-bottom:20px; color:var(--forest) }}
    
    .side-quote {{ text-align:center; padding:28px 22px }}
    .side-avatar {{ width:72px; height:72px; border-radius:50%; object-fit:cover; margin:0 auto 14px; border:2px solid var(--sage) }}
    .side-quote blockquote {{ font-family:'Fraunces',serif; font-style:italic; font-size:15px; color:var(--forest); margin:0 0 12px; line-height:1.5 }}
    .side-quote cite {{ display:block; font-style:normal; font-size:13px; font-weight:600; color:var(--moss) }}
    .side-quote small {{ display:block; font-size:11px; color:var(--muted); margin-top:2px }}

    .side-contact h4 {{ font-size:18px; margin-bottom:14px }}
    .side-contact-list {{ display:grid; gap:10px; font-size:14px; margin-bottom:20px }}
    .side-contact-list a {{ display:inline-flex; align-items:center; gap:8px; color:var(--forest); font-weight:500 }}
    .side-contact-list .ic {{ color:var(--moss) }}

    /* Product Showcase */
    .lp-products {{ padding:48px 0 64px }}
    .sec-head {{ text-align:center; max-width:680px; margin:0 auto 36px }}
    .sec-head h2 {{ font-size:clamp(28px, 3.5vw, 38px); margin:10px 0 12px }}
    .sec-head p {{ font-size:16px; color:var(--muted) }}
    .prod-grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:24px }}
    .prod-card {{
      background:#fff; border:1px solid var(--line); border-radius:24px; overflow:hidden;
      display:flex; flex-direction:column; transition:transform .25s ease, box-shadow .25s ease;
    }}
    .prod-card:hover {{ transform:translateY(-4px); box-shadow:0 16px 36px -16px rgba(61,59,54,.2) }}
    .prod-card-top {{ background:var(--linen); padding:20px 20px 10px; position:relative; text-align:center }}
    .prod-card-top .badge {{
      position:absolute; top:14px; left:14px; background:var(--sage-xl); color:var(--forest);
      font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:.08em; padding:4px 10px; border-radius:999px;
    }}
    .prod-img-box {{ height:200px; display:flex; align-items:center; justify-content:center; padding:12px }}
    .prod-img-box img {{ max-height:100%; object-fit:contain; transition:transform .3s ease }}
    .prod-card:hover .prod-img-box img {{ transform:scale(1.04) }}
    .prod-card-body {{ padding:20px 24px; display:flex; flex-direction:column; flex:1 }}
    .prod-card-body h3 {{ font-size:18px; margin-bottom:6px; color:var(--forest) }}
    .spec-note {{ font-size:13px; color:var(--muted); margin-bottom:18px; flex:1 }}
    .prod-foot {{ display:flex; justify-content:space-between; align-items:center; padding-top:14px; border-top:1px solid var(--line) }}
    .prod-foot .price {{ font-family:'Fraunces',serif; font-size:18px; font-weight:600; color:var(--forest) }}
    .btn-card {{
      display:inline-flex; align-items:center; gap:6px; font-size:13px; font-weight:600; color:var(--clay);
      padding:6px 12px; border-radius:999px; background:var(--linen); transition:background .2s, color .2s;
    }}
    .btn-card:hover {{ background:var(--clay); color:#fff }}

    /* Trust banner */
    .trust-strip {{ background:var(--forest); color:var(--linen); border-radius:32px; padding:44px; margin-bottom:64px }}
    .trust-grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:28px }}
    .trust-item {{ display:flex; gap:14px; align-items:flex-start }}
    .trust-num {{
      width:36px; height:36px; border-radius:50%; background:var(--moss); color:var(--linen);
      display:grid; place-items:center; font-family:'Fraunces',serif; font-weight:600; font-size:16px; flex-shrink:0;
    }}
    .trust-item h4 {{ font-size:16px; color:#fff; margin-bottom:4px }}
    .trust-item p {{ font-size:13px; color:var(--sage-l); line-height:1.5 }}

    /* Modal */
    .modal {{ position:fixed; inset:0; z-index:100; display:flex; align-items:center; justify-content:center; padding:16px }}
    .modal-backdrop {{ position:fixed; inset:0; background:rgba(20,25,20,.65); backdrop-filter:blur(4px) }}
    .modal-in {{ position:relative; z-index:10; width:100%; max-width:540px }}
    .card {{ background:var(--linen); border:1px solid var(--line); border-radius:28px; padding:36px; box-shadow:0 30px 60px -20px rgba(0,0,0,.35); position:relative }}
    .card-x {{ position:absolute; top:20px; right:20px; width:36px; height:36px; border-radius:50%; background:var(--sage-xl); color:var(--forest); display:grid; place-items:center }}
    .card h3 {{ font-size:24px; margin:8px 0 10px }}
    .card p.lede {{ font-size:14px; color:var(--muted); margin-bottom:20px }}
    .qlabel {{ display:block; font-size:13px; font-weight:600; color:var(--forest); margin-bottom:8px }}
    .choice {{ display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:16px }}
    .choice label {{
      display:flex; align-items:center; gap:8px; padding:10px 14px; border:1.5px solid var(--line);
      border-radius:14px; font-size:13px; font-weight:500; cursor:pointer; background:#fff; transition:border-color .2s;
    }}
    .choice input {{ accent-color:var(--forest) }}
    .field {{ margin-bottom:14px }}
    .field label {{ display:block; font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:.06em; color:var(--forest); margin-bottom:6px }}
    .field input, .field textarea {{
      width:100%; padding:11px 14px; border-radius:12px; border:1.5px solid var(--line); font:inherit; font-size:14px; background:#fff; outline:none; transition:border-color .2s;
    }}
    .field input:focus, .field textarea:focus {{ border-color:var(--moss) }}
    .f2 {{ display:grid; grid-template-columns:1fr 1fr; gap:12px }}

    /* Footer */
    footer {{ background:var(--forest); color:var(--linen); padding:64px 0 32px; font-size:14px }}
    .fgrid {{ display:grid; grid-template-columns:2fr 1fr 1fr 1.5fr; gap:40px; margin-bottom:48px }}
    .fgrid h4 {{ font-size:16px; color:#fff; margin-bottom:16px }}
    .fgrid p {{ color:var(--sage-l); line-height:1.6 }}
    .fgrid ul {{ list-style:none; padding:0; margin:0; display:grid; gap:10px }}
    .fgrid a {{ color:var(--sage-l); transition:color .2s; display:inline-flex; align-items:center; gap:6px }}
    .fgrid a:hover {{ color:#fff }}
    .fbot {{ border-top:1px solid rgba(255,255,255,.15); padding-top:24px; display:flex; justify-content:space-between; flex-wrap:wrap; gap:12px; font-size:13px; color:var(--sage-l) }}

    /* Responsive */
    @media(max-width:960px) {{
      .lp-layout {{ grid-template-columns:1fr }}
      .lp-sidebar {{ order:-1 }}
      .fgrid {{ grid-template-columns:1fr 1fr; gap:32px }}
    }}
    @media(max-width:768px) {{
      .nav {{ display:none }}
      .menu-btn {{ display:grid }}
      .strip {{ display:none }}
      .lp-hero-box {{ padding:32px 24px }}
      .lp-article {{ padding:28px 22px }}
      .fgrid {{ grid-template-columns:1fr }}
      .choice, .f2 {{ grid-template-columns:1fr }}
    }}
  </style>

  <!-- Schema.org JSON-LD -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "WebPage",
        "@id": "{canonical}",
        "url": "{canonical}",
        "name": "{meta_title}",
        "description": "{meta_desc}",
        "isPartOf": {{
          "@type": "WebSite",
          "@id": "https://schippercompactwonen.nl/#website",
          "name": "Schipper Compact Wonen",
          "url": "https://schippercompactwonen.nl/"
        }}
      }},
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://schippercompactwonen.nl/" }},
          {{ "@type": "ListItem", "position": 2, "name": "Informatie & Regio", "item": "https://schippercompactwonen.nl/lp/" }},
          {{ "@type": "ListItem", "position": 3, "name": "{title}" }}
        ]
      }},
      {{
        "@type": "LocalBusiness",
        "name": "Schipper Compact Wonen BV",
        "image": "https://schippercompactwonen.nl/assets/winkel_showroom_dordrecht.png",
        "telephone": "078-6314858",
        "email": "info@schippercompactwonen.nl",
        "address": {{
          "@type": "PostalAddress",
          "streetAddress": "Singel 313",
          "addressLocality": "Dordrecht",
          "postalCode": "3313 GT",
          "addressCountry": "NL"
        }}
      }}
    ]
  }}
  </script>
</head>
<body>

  {SVG_SPRITE}

  <!-- Top Strip -->
  <div class="strip">
    <div class="wrap">
      <span><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg>Al ruim 35 jaar zit- en zorgspecialist</span>
      <span><svg class="ic" aria-hidden="true"><use href="#i-truck"/></svg>Gratis advies &amp; proefzitten aan huis</span>
      <span><svg class="ic" aria-hidden="true"><use href="#i-map-pin"/></svg>Showroom Singel 313, Dordrecht</span>
      <a href="tel:0786314858"><svg class="ic" aria-hidden="true"><use href="#i-phone"/></svg>078 - 631 48 58</a>
    </div>
  </div>

  <!-- Header -->
  <header id="main-header">
    <div class="navbar">
      <a href="{root_rel}index.html" class="logo" aria-label="Schipper Compact Wonen">
        <span class="logo-mark">S</span>
        <span><b>Schipper</b><small>Compact Wonen</small></span>
      </a>
      <nav class="nav" aria-label="Hoofdmenu">
        <a href="{root_rel}collectie.html">Collectie</a>
        <a href="{root_rel}index.html#werkwijze">Werkwijze</a>
        <a href="{root_rel}index.html#ervaringen">Ervaringen</a>
        <a href="{root_rel}afspraak.html">Afspraak Maken</a>
        <a href="#contact">Contact</a>
      </nav>
      <div class="hdr-right">
        <a href="{root_rel}afspraak.html" class="btn btn-clay btn-sm hdr-cta">
          <svg class="ic" aria-hidden="true"><use href="#i-calendar"/></svg>Plan Adviesgesprek
        </a>
        <button id="mobile-menu-btn" class="menu-btn" aria-label="Menu openen">
          <svg class="ic" aria-hidden="true"><use href="#i-menu"/></svg>
        </button>
      </div>
    </div>
    <div id="mobile-menu" class="hidden">
      <a class="ml" href="{root_rel}collectie.html">Collectie</a>
      <a class="ml" href="{root_rel}index.html#werkwijze">Werkwijze</a>
      <a class="ml" href="{root_rel}index.html#ervaringen">Ervaringen</a>
      <a class="ml" href="{root_rel}afspraak.html">Afspraak Maken</a>
      <a class="ml" href="#contact">Contact</a>
      <div class="mm-cta">
        <a href="{root_rel}afspraak.html" class="btn btn-clay">
          <svg class="ic" aria-hidden="true"><use href="#i-calendar"/></svg>Plan Adviesgesprek
        </a>
        <a href="tel:0786314858" class="btn btn-ghost">
          <svg class="ic" aria-hidden="true"><use href="#i-phone"/></svg>Bel direct: 078 - 631 48 58
        </a>
      </div>
    </div>
  </header>

  <main>
    <!-- Breadcrumbs -->
    <div class="wrap">
      <nav class="breadcrumbs" aria-label="Kruimelpad">
        <a href="{root_rel}index.html">Home</a>
        <span class="sep">/</span>
        <a href="{root_rel}lp/index.html">Informatie &amp; Regio</a>
        <span class="sep">/</span>
        <span>{short_title}</span>
      </nav>
    </div>

    <!-- Hero Section -->
    <section class="lp-hero">
      <div class="wrap">
        <div class="lp-hero-box">
          <span class="eyebrow">
            <svg class="ic" aria-hidden="true"><use href="#i-shield"/></svg>
            {'Zit- en Zorgspecialist regio ' + city['name'] if city else 'Ergonomisch Maatwerk & Comfort'}
          </span>
          <h1>{title}</h1>
          <p class="lp-hero-lede">{meta_desc}</p>
          <div class="lp-hero-actions">
            <button onclick="openBookingModal('hero-primary')" class="btn btn-clay">
              <svg class="ic" aria-hidden="true"><use href="#i-calendar"/></svg>Plan showroombezoek of thuisadvies
            </button>
            <a href="{root_rel}collectie.html" class="btn btn-ghost">
              <svg class="ic" aria-hidden="true"><use href="#i-arrow-right"/></svg>Bekijk complete collectie
            </a>
          </div>
          <div class="usp-pills">
            <span><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg>100% Maatwerk op uw lichaam</span>
            <span><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg>Advies door bewegingstechnoloog</span>
            <span><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg>Eigen bezorging &amp; montage</span>
            <span><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg>Erkend dealer Fitform &amp; Farstrup</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Main Content & Sidebar -->
    <section class="wrap">
      <div class="lp-layout">
        <!-- Editorial Content from WP -->
        <article class="lp-article">
          {article_html}
        </article>

        <!-- Sticky Sidebar -->
        <aside class="lp-sidebar">
          {city_sidebar_html}

          <div class="side-card side-quote">
            <img src="{root_rel}assets/geertjan_advies_showroom.jpg" alt="Geertjan Klein Haneveld, bewegingstechnoloog" class="side-avatar">
            <blockquote>"Goed zitten is maatwerk. Als bewegingstechnoloog help ik u aan een stoel die écht past bij uw lichaam en wensen."</blockquote>
            <cite>Geertjan Klein Haneveld</cite>
            <small>Bewegingstechnoloog &amp; Eigenaar</small>
          </div>

          <div class="side-card side-contact">
            <h4>Showroom &amp; Contact</h4>
            <div class="side-contact-list">
              <a href="tel:0786314858"><svg class="ic" aria-hidden="true"><use href="#i-phone"/></svg>078 - 631 48 58</a>
              <span><svg class="ic" aria-hidden="true"><use href="#i-map-pin"/></svg>Singel 313, 3313 GT Dordrecht</span>
              <span><svg class="ic" aria-hidden="true"><use href="#i-clock"/></svg>Di t/m Za geopend · Ma op afspraak</span>
            </div>
            <button onclick="openBookingModal('sidebar-contact')" class="btn btn-primary btn-sm w-full">
              <svg class="ic" aria-hidden="true"><use href="#i-calendar"/></svg>Vrijblijvend afspraak maken
            </button>
          </div>
        </aside>
      </div>
    </section>

    <!-- Featured Products Showcase -->
    <section class="lp-products">
      <div class="wrap">
        <div class="sec-head">
          <span class="eyebrow"><svg class="ic" aria-hidden="true"><use href="#i-star"/></svg>Aanbevolen Collectie</span>
          <h2>Populaire modellen passend bij uw zoekopdracht</h2>
          <p>Al onze modellen worden vakkundig aangemeten op zithoogte, zitdiepte en armleggerhoogte door onze bewegingstechnoloog.</p>
        </div>
        <div class="prod-grid">
          {prod_cards_html}
        </div>
      </div>
    </section>

    <!-- Trust 4 Steps -->
    <section class="wrap">
      <div class="trust-strip">
        <div class="trust-grid">
          <div class="trust-item">
            <div class="trust-num">1</div>
            <div>
              <h4>Persoonlijke intake</h4>
              <p>We luisteren naar uw specifieke klachten, wensen en woonruimte.</p>
            </div>
          </div>
          <div class="trust-item">
            <div class="trust-num">2</div>
            <div>
              <h4>Ergonomisch meten</h4>
              <p>Onze bewegingstechnoloog meet uw lichaam tot op de millimeter nauwkeurig in.</p>
            </div>
          </div>
          <div class="trust-item">
            <div class="trust-num">3</div>
            <div>
              <h4>Ontspannen proefzitten</h4>
              <p>In alle rust ervaren in onze showroom of geheel vrijblijvend bij u thuis.</p>
            </div>
          </div>
          <div class="trust-item">
            <div class="trust-num">4</div>
            <div>
              <h4>Eigen servicedienst</h4>
              <p>Volledig geïnstalleerd in uw woonkamer met jarenlange garantie en service.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>

  <!-- Interactive Booking Modal -->
  <div id="booking-modal" class="modal hidden" role="dialog" aria-modal="true" aria-labelledby="bm-title">
    <div class="modal-in">
      <div class="modal-backdrop" onclick="closeBookingModal()"></div>
      <div class="card">
        <button class="card-x" onclick="closeBookingModal()" aria-label="Sluiten">
          <svg class="ic" aria-hidden="true"><use href="#i-close"/></svg>
        </button>
        <div id="modal-form-container">
          <span class="eyebrow">100% Vrijblijvend</span>
          <h3 id="bm-title">Plan uw Persoonlijk Adviesgesprek</h3>
          <p class="lede">Geef hieronder uw voorkeur aan, of <a href="{root_rel}afspraak.html" style="color:var(--forest);font-weight:700;text-decoration:underline;">kies direct datum &amp; tijd in onze live agenda &rarr;</a></p>
          <form onsubmit="handleBookingSubmit(event)">
            <div>
              <span class="qlabel">Waar wilt u het advies ontvangen?</span>
              <div class="choice">
                <label><input type="radio" name="appointment-type" value="thuis" checked>Gratis aan huis</label>
                <label><input type="radio" name="appointment-type" value="showroom">In showroom Dordrecht</label>
              </div>
            </div>
            <div class="field">
              <label for="book-name">Uw naam *</label>
              <input type="text" id="book-name" required placeholder="Dhr. / Mw. Jansen">
            </div>
            <div class="f2">
              <div class="field">
                <label for="book-phone">Telefoonnummer *</label>
                <input type="tel" id="book-phone" required placeholder="078 - 123 45 67">
              </div>
              <div class="field">
                <label for="book-city">Woonplaats</label>
                <input type="text" id="book-city" value="{city['name'] if city else ''}" placeholder="Uw woonplaats">
              </div>
            </div>
            <div class="field">
              <label for="book-notes">Eventuele wensen of lichamelijke klachten</label>
              <textarea id="book-notes" rows="2" placeholder="Bijv. rugklachten, moeite met opstaan, interesse in Fitform..."></textarea>
            </div>
            <button type="submit" class="btn btn-clay w-full" style="padding:16px">
              <svg class="ic" aria-hidden="true"><use href="#i-calendar"/></svg>Afspraakverzoek versturen
            </button>
          </form>
        </div>
        <div id="modal-success-container" class="hidden" style="text-align:center; padding:20px 0">
          <div style="width:64px; height:64px; border-radius:50%; background:var(--sage-xl); color:var(--moss); display:grid; place-items:center; margin:0 auto 16px">
            <svg class="ic" style="width:32px; height:32px" aria-hidden="true"><use href="#i-check"/></svg>
          </div>
          <h3>Hartelijk dank voor uw aanvraag!</h3>
          <p class="lede" style="margin-top:8px">We hebben uw gegevens goed ontvangen. Onze specialist neemt binnen 1 werkdag telefonisch contact met u op.</p>
          <button onclick="closeBookingModal()" class="btn btn-primary" style="margin-top:20px">Sluiten</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <footer id="contact">
    <div class="wrap">
      <div class="fgrid">
        <div>
          <a href="{root_rel}index.html" class="logo" style="margin-bottom:18px">
            <span class="logo-mark" style="background:#FAF7F1;color:var(--forest)">S</span>
            <span><b style="color:#FAF7F1">Schipper</b><small style="color:var(--sage-l)">Compact Wonen</small></span>
          </a>
          <p>Al ruim 35 jaar dé zit- en zorgspecialist in comfortabel en zelfstandig wonen. Ergonomische sta-op stoelen, relaxfauteuils, hoog-laag bedden en loophulpmiddelen in de regio Drechtsteden &amp; Rijnmond.</p>
          <p style="margin-top:14px;font-size:13px;color:var(--sage-l)">Schipper Compact Wonen BV<br>KvK: 24391284 · BTW: NL815610427B01</p>
        </div>
        <div>
          <h4>Collectie</h4>
          <ul>
            <li><a href="{root_rel}collectie.html?cat=zitcomfort"><svg class="ic" aria-hidden="true"><use href="#i-chevron-right"/></svg>Zitcomfort: Sta-op Stoelen</a></li>
            <li><a href="{root_rel}collectie.html?cat=zitcomfort"><svg class="ic" aria-hidden="true"><use href="#i-chevron-right"/></svg>Senioren Relaxstoelen</a></li>
            <li><a href="{root_rel}collectie.html?cat=ligcomfort"><svg class="ic" aria-hidden="true"><use href="#i-chevron-right"/></svg>Ligcomfort: Hoog/laag Bedden</a></li>
            <li><a href="{root_rel}collectie.html?cat=zorgcomfort"><svg class="ic" aria-hidden="true"><use href="#i-chevron-right"/></svg>Zorgcomfort &amp; Rollators</a></li>
          </ul>
        </div>
        <div>
          <h4>Regio's &amp; Service</h4>
          <ul>
            <li><a href="{root_rel}lp/sta-op-stoel-dordrecht/index.html"><svg class="ic" aria-hidden="true"><use href="#i-chevron-right"/></svg>Dordrecht &amp; Drechtsteden</a></li>
            <li><a href="{root_rel}lp/sta-op-stoel-barendrecht/index.html"><svg class="ic" aria-hidden="true"><use href="#i-chevron-right"/></svg>Barendrecht &amp; Carnisselande</a></li>
            <li><a href="{root_rel}lp/sta-op-stoel-hendrik-ido-ambacht/index.html"><svg class="ic" aria-hidden="true"><use href="#i-chevron-right"/></svg>Hendrik-Ido-Ambacht</a></li>
            <li><a href="{root_rel}lp/sta-op-stoel-ridderkerk/index.html"><svg class="ic" aria-hidden="true"><use href="#i-chevron-right"/></svg>Ridderkerk &amp; Bolnes</a></li>
            <li><a href="{root_rel}sta-op-stoelen-rotterdam/index.html"><svg class="ic" aria-hidden="true"><use href="#i-chevron-right"/></svg>Rotterdam &amp; Rijnmond</a></li>
          </ul>
        </div>
        <div>
          <h4>Showroom Dordrecht</h4>
          <p style="margin-bottom:8px">Singel 313, 3313 GT Dordrecht<br>(hoek Merwedestraat / Reeweg)</p>
          <p style="margin-bottom:14px;font-size:13px;color:var(--sage-l)">Gratis parkeren voor de deur</p>
          <p><a href="tel:0786314858" style="color:#FAF7F1;font-weight:600"><svg class="ic" aria-hidden="true"><use href="#i-phone"/></svg>078 - 631 48 58</a></p>
        </div>
      </div>
      <div class="fbot">
        <span>&copy; 2026 Schipper Compact Wonen BV · Alle rechten voorbehouden <span class="site-version" style="display:inline-block;margin-left:8px;padding:2px 8px;background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.22);border-radius:999px;font-size:11px;font-weight:600;letter-spacing:0.04em;">v3.2.0</span></span>
        <span>Specialist in Zit-, Lig- en Zorgcomfort</span>
      </div>
    </div>
  </footer>

  <script>
    console.log('%c Schipper Compact Wonen • v3.2.0 (okt 2026) ', 'background: #344E41; color: #FAF7F1; font-weight: bold; padding: 4px 8px; border-radius: 4px;');
    const bookingModal = document.getElementById('booking-modal');
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    
    if (mobileMenuBtn) {{
      mobileMenuBtn.addEventListener('click', () => {{
        mobileMenu.classList.toggle('hidden');
      }});
    }}

    function openBookingModal(origin) {{
      if (mobileMenu) mobileMenu.classList.add('hidden');
      bookingModal.classList.remove('hidden');
      document.body.style.overflow = 'hidden';
    }}

    function closeBookingModal() {{
      bookingModal.classList.add('hidden');
      document.body.style.overflow = '';
      setTimeout(() => {{
        document.getElementById('modal-form-container').classList.remove('hidden');
        document.getElementById('modal-success-container').classList.add('hidden');
      }}, 300);
    }}

    function handleBookingSubmit(e) {{
      e.preventDefault();

      const name = document.getElementById('book-name') ? document.getElementById('book-name').value.trim() : '';
      const phone = document.getElementById('book-phone') ? document.getElementById('book-phone').value.trim() : '';
      const city = document.getElementById('book-city') ? document.getElementById('book-city').value.trim() : '';
      const notes = document.getElementById('book-notes') ? document.getElementById('book-notes').value.trim() : '';
      const typeInput = document.querySelector('input[name="appointment-type"]:checked');
      const appointmentType = typeInput ? typeInput.value : 'thuis';

      // Push to Google Calendar Webhook
      const GOOGLE_CALENDAR_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwyRN-iLM83LFZ4hZ08jzwpMdeHI6o5kU5fr0Bz2KpmOuG3XP5y_4zbyE2cO45WCdNN/exec";
      fetch(GOOGLE_CALENDAR_WEBHOOK_URL, {{
        method: "POST",
        headers: {{ "Content-Type": "text/plain" }},
        body: JSON.stringify({{
          brand: "Schipper Compact Wonen",
          site: "schippercompactwonen.nl",
          name: name,
          phone: phone,
          email: "",
          appointmentType: appointmentType,
          address: appointmentType === 'thuis' ? (city || "Aan Huis") : "Showroom Dordrecht (Merwedestraat 239)",
          notes: notes + " [Landingspagina: {title}]",
          emailSubject: "Nieuwe Landingspagina Aanvraag: {title}",
          senderName: "Geertjan Klein Haneveld - Schipper Compact Wonen",
          replyTo: "info@schippercompactwonen.nl",
          notificationEmail: "schipperwonen@gmail.com, info@schippercompactwonen.nl",
          timestamp: new Date().toISOString()
        }})
      }}).catch(err => console.warn("Google Webhook warning:", err));

      document.getElementById('modal-form-container').classList.add('hidden');
      document.getElementById('modal-success-container').classList.remove('hidden');
    }}

    window.addEventListener('keydown', (e) => {{
      if (e.key === 'Escape' && !bookingModal.classList.contains('hidden')) {{
        closeBookingModal();
      }}
    }});
  </script>
</body>
</html>
"""
    return html

def generate_lp_overview(lps):
    """Generates lp/index.html linking to all landing pages neatly categorized."""
    regio_lps = [('../sta-op-stoelen-rotterdam/index.html', 'Sta op Stoelen Rotterdam (Specialist)')]
    brand_lps = []
    chair_lps = []
    care_lps = []
    
    for lp in lps:
        slug = lp['slug']
        title = unescape(lp['title']['rendered'])
        item = (f"{slug}/index.html", title)
        
        if any(c in slug for c in ['dordrecht', 'barendrecht', 'hendrik-ido-ambacht', 'ridderkerk', 'rotterdam', 'alblasserdam']):
            regio_lps.append(item)
        elif 'fitform' in slug:
            brand_lps.append(item)
        elif any(k in slug for k in ['bed', 'matras', 'zorg', 'rollator', 'bodem']):
            care_lps.append(item)
        else:
            chair_lps.append(item)

    def render_links(items):
        res = '<div class="hub-grid">'
        for href, title in sorted(items, key=lambda x: x[1]):
            res += f'<a href="{href}" class="hub-link"><svg class="ic" aria-hidden="true"><use href="#i-chevron-right"/></svg>{title}</a>'
        res += '</div>'
        return res

    html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Informatiepagina &amp; Regionale Diensten | Schipper Compact Wonen</title>
  <meta name="description" content="Compleet overzicht van al onze regionale diensten, adviespagina's voor sta-op stoelen, Fitform dealers, seniorenledikanten en zorghulpmiddelen in Drechtsteden &amp; Rijnmond.">
  <link rel="canonical" href="https://schippercompactwonen.nl/lp/">
  
  <!-- Favicons -->
  <link rel="icon" type="image/svg+xml" href="../favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="../favicon-32x32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="../apple-touch-icon.png">
  <meta name="theme-color" content="#A3B18A">
  
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,400..700,100;1,9..144,400..600,100&family=Figtree:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <style>
    :root {{
      --sage:#A3B18A; --sage-l:#DCE3CF; --sage-xl:#EEF1E6; --moss:#588157; --forest:#344E41;
      --oat:#EDE6DA; --linen:#FAF7F1; --clay:#C4805F; --ink:#3D3B36; --muted:#6E6A60; --line:#DDD3C2;
    }}
    *,*::before,*::after {{ box-sizing:border-box }}
    body {{ margin:0; font-family:'Figtree',sans-serif; color:var(--ink); background:var(--linen); line-height:1.6 }}
    .wrap {{ max-width:1200px; margin:0 auto; padding:0 24px }}
    h1,h2,h3 {{ font-family:'Fraunces',serif; color:var(--forest) }}
    .hub-hero {{ text-align:center; padding:64px 0 40px }}
    .hub-hero h1 {{ font-size:clamp(32px, 4.5vw, 48px); margin:12px 0 }}
    .hub-hero p {{ font-size:18px; color:var(--muted); max-width:680px; margin:0 auto }}
    .hub-sec {{ margin-bottom:48px; background:#fff; border:1px solid var(--line); border-radius:24px; padding:36px }}
    .hub-sec h2 {{ font-size:24px; margin-bottom:20px; border-bottom:2px solid var(--sage-l); padding-bottom:8px }}
    .hub-grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:12px }}
    .hub-link {{
      display:flex; align-items:center; gap:8px; padding:10px 14px; background:var(--linen);
      border-radius:12px; font-size:14px; font-weight:500; color:var(--forest); transition:all .2s;
    }}
    .hub-link:hover {{ background:var(--forest); color:#fff; transform:translateX(3px) }}
    .hub-link .ic {{ width:14px; height:14px; color:var(--moss) }}
    .hub-link:hover .ic {{ color:var(--sage-l) }}
    .ic {{ display:inline-block; vertical-align:middle }}
  </style>
</head>
<body>
  {SVG_SPRITE}
  <main class="wrap">
    <div class="hub-hero">
      <a href="../index.html" style="font-weight:600; color:var(--moss)">&larr; Terug naar Schipper Compact Wonen</a>
      <h1>Informatie &amp; Regionale Diensten</h1>
      <p>Hieronder vindt u een overzicht van al onze lokale landingspagina's, merkenspecialisaties en productgidsen voor de regio Drechtsteden en Rijnmond.</p>
    </div>

    <section class="hub-sec">
      <h2>Regionale pagina's (Drechtsteden &amp; Rijnmond)</h2>
      {render_links(regio_lps)}
    </section>

    <section class="hub-sec">
      <h2>Fitform Merkspecialismen</h2>
      {render_links(brand_lps)}
    </section>

    <section class="hub-sec">
      <h2>Sta-op Stoelen &amp; Zitcomfort Gidsen</h2>
      {render_links(chair_lps)}
    </section>

    <section class="hub-sec">
      <h2>Lig- en Zorgcomfort</h2>
      {render_links(care_lps)}
    </section>

    <footer style="text-align:center; padding:32px 0; font-size:13px; color:var(--muted)">
      &copy; 2026 Schipper Compact Wonen BV · Alle rechten voorbehouden <span class="site-version" style="display:inline-block;margin-left:8px;padding:2px 8px;background:var(--oat);border:1px solid var(--line);border-radius:999px;font-size:11px;font-weight:600;letter-spacing:0.04em;">v3.2.0</span>
    </footer>
  </main>
  <script>
    console.log('%c Schipper Compact Wonen • v3.2.0 (okt 2026) ', 'background: #344E41; color: #FAF7F1; font-weight: bold; padding: 4px 8px; border-radius: 4px;');
  </script>
</body>
</html>
"""
    return html

def generate_sitemap(lps):
    """Generates clean sitemap.xml for Google Search Console."""
    urls = [
        '<url><loc>https://schippercompactwonen.nl/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>',
        '<url><loc>https://schippercompactwonen.nl/collectie</loc><changefreq>weekly</changefreq><priority>0.9</priority></url>',
        '<url><loc>https://schippercompactwonen.nl/afspraak</loc><changefreq>weekly</changefreq><priority>0.9</priority></url>',
        '<url><loc>https://schippercompactwonen.nl/lp/</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>',
        '<url><loc>https://schippercompactwonen.nl/sta-op-stoelen-rotterdam/</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>'
    ]
    
    for lp in lps:
        slug = lp['slug']
        urls.append(f'<url><loc>https://schippercompactwonen.nl/lp/{slug}/</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>')
        
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>
"""
    return sitemap

def main():
    lps = cache.get('lps', [])
    rotterdam = cache.get('rotterdam')
    
    print(f"Generating {len(lps)} LP pages with refined styling and verified assets...")
    
    count = 0
    for lp in lps:
        slug = lp['slug']
        out_dir = os.path.join(BASE_DIR, 'lp', slug)
        os.makedirs(out_dir, exist_ok=True)
        out_file = os.path.join(out_dir, 'index.html')
        
        page_html = generate_lp_html(lp, is_rotterdam=False)
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(page_html)
        count += 1

    print(f"Generated {count} LP pages in /lp/[slug]/index.html")

    # Generate Rotterdam page
    if rotterdam:
        rdam_dir = os.path.join(BASE_DIR, 'sta-op-stoelen-rotterdam')
        os.makedirs(rdam_dir, exist_ok=True)
        rdam_file = os.path.join(rdam_dir, 'index.html')
        rdam_html = generate_lp_html(rotterdam, is_rotterdam=True)
        with open(rdam_file, 'w', encoding='utf-8') as f:
            f.write(rdam_html)
        print("Generated sta-op-stoelen-rotterdam/index.html")

    # Generate LP Hub Overview
    hub_file = os.path.join(BASE_DIR, 'lp', 'index.html')
    hub_html = generate_lp_overview(lps)
    with open(hub_file, 'w', encoding='utf-8') as f:
        f.write(hub_html)
    print("Generated lp/index.html (Hub Overview)")

    # Generate sitemap.xml
    sitemap_file = os.path.join(BASE_DIR, 'sitemap.xml')
    sitemap_xml = generate_sitemap(lps)
    with open(sitemap_file, 'w', encoding='utf-8') as f:
        f.write(sitemap_xml)
    print("Generated sitemap.xml with all URLs!")

if __name__ == '__main__':
    main()
