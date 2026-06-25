#!/usr/bin/env python3
"""
Morning Edition Magazine Generator
Produces a self-contained HTML editorial magazine with 10 distinct spreads.
Usage: python3 generator.py stories.json > magazines/YYYY-MM-DD.html
"""

import json, sys, datetime, html as html_mod

def load_stories(path):
    with open(path) as f:
        return json.load(f)

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Morning Edition — {date_display}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,600;0,9..144,700;0,9..144,900;1,9..144,400&family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,700;14..32,900&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth;font-size:18px}}
body{{font-family:'Inter',system-ui,sans-serif;line-height:1.5;color:#1a1a1a;background:#f8f5f0;overflow-x:hidden}}
h1,h2,h3,.fraunces{{font-family:'Fraunces',Georgia,serif}}

/* MASTHEAD */
.masthead{{padding:3rem 2rem 1.5rem;text-align:center;border-bottom:3px double #1a1a1a;margin-bottom:0}}
.masthead .tag{{font-family:'Inter';font-size:0.7rem;letter-spacing:0.35em;text-transform:uppercase;color:#8b4513;margin-bottom:0.5rem}}
.masthead h1{{font-size:clamp(2.5rem,8vw,6rem);font-weight:900;line-height:0.95;letter-spacing:-0.03em}}
.masthead .dateline{{font-size:0.8rem;color:#666;letter-spacing:0.2em;text-transform:uppercase;margin-top:0.8rem}}
.masthead .subtitle{{font-size:1rem;color:#444;max-width:600px;margin:1rem auto 0;font-weight:300}}

/* SPREAD COMMONS */
.spread{{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:4rem 2rem;position:relative;overflow:hidden}}
.spread-inner{{max-width:1100px;width:100%;position:relative;z-index:2}}
.numeral{{font-family:'Fraunces',serif;font-size:clamp(6rem,15vw,16rem);font-weight:900;line-height:0.75;position:absolute;opacity:0.06;user-select:none;pointer-events:none;z-index:1}}
.story-title{{font-family:'Fraunces',serif;font-size:clamp(2rem,5vw,4rem);font-weight:700;line-height:1.05;letter-spacing:-0.02em;margin-bottom:1.5rem}}
.story-meta{{font-size:0.75rem;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:0.8rem;font-weight:500}}
.story-desc{{font-size:1.1rem;line-height:1.7;max-width:650px;margin-bottom:1.5rem}}
.story-link{{display:inline-block;font-family:'Inter';font-weight:700;font-size:0.85rem;letter-spacing:0.08em;text-transform:uppercase;text-decoration:none;padding-bottom:2px;border-bottom:2px solid;transition:all 0.2s}}
.story-link:hover{{opacity:0.7;padding-bottom:4px}}

/* 1. HERO */
.s1{{background:#111;color:#fff}}
.s1 .numeral{{color:#fff;opacity:0.05;font-size:clamp(8rem,22vw,22rem);right:0;top:50%;transform:translateY(-50%)}}
.s1 .story-title{{font-size:clamp(2.8rem,7vw,5.5rem);font-weight:900}}
.s1 .story-link{{color:#fff;border-color:#fff}}

/* 2. MIDNIGHT */
.s2{{background:#0a0a10;color:#e0e0e0;background-image:radial-gradient(ellipse at 30% 20%,rgba(30,60,255,0.08) 0%,transparent 60%)}}
.s2 .numeral{{color:#3050ff;opacity:0.08;left:10%;top:20%}}
.s2 .story-title{{color:#fff}}
.s2 .story-meta{{color:#3050ff}}
.s2 .story-link{{color:#3050ff;border-color:#3050ff}}

/* 3. ROSE STAMP */
.s3{{background:#fff5f5}}
.s3 .stamp{{position:absolute;right:3rem;top:3rem;border:4px solid #e53e3e;color:#e53e3e;padding:0.5rem 1.5rem;font-family:'Inter';font-weight:900;font-size:0.85rem;letter-spacing:0.15em;text-transform:uppercase;transform:rotate(8deg);z-index:3;opacity:0.85}}
.s3 .numeral{{color:#e53e3e;opacity:0.05;right:0;bottom:0}}
.s3 .story-title{{color:#1a1a1a}}
.s3 .story-link{{color:#e53e3e;border-color:#e53e3e}}

/* 4. TERMINAL */
.s4{{background:#0c0c0c;font-family:'SF Mono','Fira Code','Cascadia Code',monospace;color:#00ff41}}
.s4 .story-title{{font-family:'SF Mono','Fira Code',monospace;font-size:clamp(1.5rem,3.5vw,2.8rem);font-weight:400}}
.s4 .story-title::before{{content:'$ ';color:#666}}
.s4 .story-meta{{color:#0a0;font-family:monospace}}
.s4 .story-desc{{font-family:'SF Mono','Fira Code',monospace;color:#0c0;font-size:0.95rem;max-width:700px}}
.s4 .story-link{{font-family:monospace;color:#00ff41;border-color:#00ff41;border-bottom-style:dashed}}
.s4 .numeral{{font-family:monospace;color:#00ff41;opacity:0.04;right:5%;top:50%;transform:translateY(-50%)}}

/* 5. ACADEMIC */
.s5{{background:#fefae0;color:#3c2415;background-image:linear-gradient(to bottom,transparent 39px,#d4c5a0 39px,#d4c5a0 40px,transparent 40px);background-size:100% 40px}}
.s5 .story-title{{font-weight:400;font-style:italic}}
.s5 .story-title::first-letter{{font-size:clamp(3.5rem,8vw,6rem);float:left;line-height:0.7;padding-right:0.3rem;font-weight:900;font-style:normal;color:#8b4513}}
.s5 .story-desc{{text-align:justify;font-size:1.05rem}}
.s5 .story-link{{color:#8b4513;border-color:#8b4513}}
.s5 .numeral{{color:#8b4513;opacity:0.04;left:5%;top:10%}}

/* 6. MANIFESTO */
.s6{{background:#000;color:#fff}}
.s6 .story-inner{{border-left:6px solid #e53e3e;padding-left:3rem}}
.s6 .story-title{{font-size:clamp(2rem,5vw,3.5rem);font-weight:900;text-transform:uppercase}}
.s6 .story-meta{{color:#e53e3e}}
.s6 .story-link{{color:#e53e3e;border-color:#e53e3e}}
.s6 .numeral{{color:#e53e3e;opacity:0.06;right:5%;bottom:5%}}

/* 7. EDITORIAL */
.s7{{background:#f4f1ea;color:#1a1a1a}}
.s7 .spread-inner{{display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:start}}
.s7 .col-right{{border-left:1px solid #ccc;padding-left:3rem}}
.s7 .story-title{{font-size:clamp(1.8rem,3.5vw,2.8rem);font-weight:600}}
.s7 .story-desc{{text-align:justify;column-count:2;column-gap:1.5rem}}
.s7 .story-link{{color:#1a1a1a;border-color:#1a1a1a}}
.s7 .numeral{{color:#1a1a1a;opacity:0.03;right:10%;bottom:10%}}
@media(max-width:768px){{.s7 .spread-inner{{grid-template-columns:1fr}}.s7 .col-right{{border-left:0;padding-left:0;border-top:1px solid #ccc;padding-top:2rem}}}}

/* 8. BIG STAT */
.s8{{background:#fff;color:#1a1a1a}}
.s8 .big-num{{font-family:'Fraunces',serif;font-size:clamp(8rem,20vw,18rem);font-weight:900;line-height:0.8;margin-bottom:0.5rem}}
.s8 .story-title{{font-size:clamp(1.5rem,3vw,2.2rem);font-weight:600}}
.s8 .story-desc{{max-width:500px}}
.s8 .story-link{{color:#1a1a1a;border-color:#1a1a1a}}

/* 9. BRUTALIST */
.s9{{background:#fff;font-family:monospace;color:#000;border:8px solid #000;margin:0}}
.s9 *{{font-family:monospace}}
.s9 .story-title{{font-weight:700;border-bottom:2px solid #000;display:inline-block;padding-bottom:0.3rem}}
.s9 .story-meta{{color:#666}}
.s9 .story-link{{color:#000;border-color:#000;border-bottom-style:solid}}
.s9 .numeral{{opacity:0.03;color:#000}}

/* 10. FINALE */
.s10{{background:linear-gradient(135deg,#1a1a2e 0%,#16213e 40%,#0f3460 70%,#533483 100%);color:#fff;text-align:center}}
.s10 .story-title{{font-size:clamp(2.5rem,6vw,4.5rem);font-weight:300;letter-spacing:0.05em}}
.s10 .story-desc{{font-size:1.2rem;font-weight:300;opacity:0.8}}
.s10 .story-link{{color:#fff;border-color:rgba(255,255,255,0.4)}}
.s10 .numeral{{opacity:0.04;color:#fff;left:50%;top:50%;transform:translate(-50%,-50%);font-size:clamp(12rem,30vw,30rem)}}

/* COLOPHON */
.colophon{{padding:3rem 2rem;text-align:center;background:#111;color:#666;font-size:0.7rem;letter-spacing:0.1em;text-transform:uppercase}}
.colophon a{{color:#999;text-decoration:none;border-bottom:1px solid #444}}
.colophon a:hover{{color:#fff}}

/* INDEX NAV */
.issue-nav{{padding:1.5rem 2rem;text-align:center;background:#fff;border-bottom:1px solid #eee;font-size:0.8rem}}
.issue-nav a{{color:#1a1a1a;text-decoration:none;margin:0 0.5rem;border-bottom:1px solid #ddd}}
.issue-nav a:hover{{border-color:#1a1a1a}}

@media(max-width:600px){{
  .spread{{padding:2rem 1rem;min-height:auto}}
  .story-title{{font-size:clamp(1.5rem,6vw,2.5rem)}}
  .story-desc{{font-size:0.95rem}}
}}
</style>
</head>
<body>

<!-- MASTHEAD -->
<header class="masthead">
<div class="tag">The Daily Briefing for AI Builders</div>
<h1>MORNING<br>EDITION</h1>
<div class="dateline">{date_display}</div>
<div class="subtitle">10 trending prompts, templates & agent patterns — curated from X and Reddit, designed for your stack.</div>
</header>

<!-- SPREADS -->
{spreads}

<!-- COLOPHON -->
<footer class="colophon">
<p>Morning Edition · Published daily at 7am AWST · Curated by <a href="https://github.com/nerodesign/morning-edition">StudioOps</a></p>
<p>Sources: <a href="https://x.com">X (Twitter)</a> · <a href="https://reddit.com">Reddit</a> · All prompts link to original posts</p>
<p style="margin-top:0.5rem;color:#444">Built with Fraunces & Inter · {gen_date}</p>
</footer>
</body>
</html>"""

SPREAD_TEMPLATES = [
    # 0: HERO
    """<section class="spread s1">
<span class="numeral">{num}</span>
<div class="spread-inner">
<div class="story-meta">{source} &mdash; {category}</div>
<h2 class="story-title">{title}</h2>
<p class="story-desc">{desc}</p>
<a class="story-link" href="{url}" target="_blank" rel="noopener">View Source &rarr;</a>
</div>
</section>""",
    # 1: MIDNIGHT
    """<section class="spread s2">
<span class="numeral">{num}</span>
<div class="spread-inner">
<div class="story-meta">{source} &mdash; {category}</div>
<h2 class="story-title">{title}</h2>
<p class="story-desc">{desc}</p>
<a class="story-link" href="{url}" target="_blank" rel="noopener">Open Thread &rarr;</a>
</div>
</section>""",
    # 2: ROSE STAMP
    """<section class="spread s3">
<span class="stamp">TRENDING</span>
<span class="numeral">{num}</span>
<div class="spread-inner">
<div class="story-meta">{source} &mdash; {category}</div>
<h2 class="story-title">{title}</h2>
<p class="story-desc">{desc}</p>
<a class="story-link" href="{url}" target="_blank" rel="noopener">See Prompt &rarr;</a>
</div>
</section>""",
    # 3: TERMINAL
    """<section class="spread s4">
<span class="numeral">{num}</span>
<div class="spread-inner">
<div class="story-meta">{source} &mdash; {category}</div>
<h2 class="story-title">{title}</h2>
<p class="story-desc">{desc}</p>
<a class="story-link" href="{url}" target="_blank" rel="noopener">cat prompt.txt &rarr;</a>
</div>
</section>""",
    # 4: ACADEMIC
    """<section class="spread s5">
<span class="numeral">{num}</span>
<div class="spread-inner">
<div class="story-meta">{source} &mdash; {category}</div>
<h2 class="story-title">{title}</h2>
<p class="story-desc">{desc}</p>
<a class="story-link" href="{url}" target="_blank" rel="noopener">Read Full Thread &rarr;</a>
</div>
</section>""",
    # 5: MANIFESTO
    """<section class="spread s6">
<span class="numeral">{num}</span>
<div class="spread-inner">
<div class="story-inner">
<div class="story-meta">{source} &mdash; {category}</div>
<h2 class="story-title">{title}</h2>
<p class="story-desc">{desc}</p>
<a class="story-link" href="{url}" target="_blank" rel="noopener">View Template &rarr;</a>
</div>
</div>
</section>""",
    # 6: EDITORIAL
    """<section class="spread s7">
<span class="numeral">{num}</span>
<div class="spread-inner">
<div class="col-left">
<div class="story-meta">{source}</div>
<h2 class="story-title">{title}</h2>
</div>
<div class="col-right">
<p class="story-desc">{desc}</p>
<a class="story-link" href="{url}" target="_blank" rel="noopener">Read More &rarr;</a>
<p style="font-family:monospace;font-size:0.65rem;color:#999;margin-top:1rem;text-transform:uppercase;letter-spacing:0.1em">{category}</p>
</div>
</div>
</section>""",
    # 7: BIG STAT
    """<section class="spread s8">
<span class="numeral">{num}</span>
<div class="spread-inner">
<div class="big-num">{num}</div>
<div class="story-meta">{source} &mdash; {category}</div>
<h2 class="story-title">{title}</h2>
<p class="story-desc">{desc}</p>
<a class="story-link" href="{url}" target="_blank" rel="noopener">Get Prompt &rarr;</a>
</div>
</section>""",
    # 8: BRUTALIST
    """<section class="spread s9">
<span class="numeral">{num}</span>
<div class="spread-inner">
<div class="story-meta">{source} // {category}</div>
<h2 class="story-title">{title}</h2>
<p class="story-desc">{desc}</p>
<a class="story-link" href="{url}" target="_blank" rel="noopener">[ OPEN ]</a>
</div>
</section>""",
    # 9: FINALE
    """<section class="spread s10">
<span class="numeral">{num}</span>
<div class="spread-inner">
<div class="story-meta" style="opacity:0.6">{source} &mdash; {category}</div>
<h2 class="story-title">{title}</h2>
<p class="story-desc">{desc}</p>
<a class="story-link" href="{url}" target="_blank" rel="noopener">Explore &rarr;</a>
</div>
</section>""",
]

NUMERALS = ['01','02','03','04','05','06','07','08','09','10']

def render(stories):
    spreads_html = []
    for i, s in enumerate(stories[:10]):
        template = SPREAD_TEMPLATES[i]
        spreads_html.append(template.format(
            num=NUMERALS[i],
            title=html_mod.escape(s.get('title','Untitled')),
            desc=html_mod.escape(s.get('description','')),
            url=html_mod.escape(s.get('url','#')),
            source=html_mod.escape(s.get('source','Unknown')),
            category=html_mod.escape(s.get('category','Prompt'))
        ))
    return TEMPLATE.format(
        date_display="{dt:%A}, {dt:%d} {dt:%B} {dt:%Y}".format(dt=datetime.date.today()),
        spreads='\n'.join(spreads_html),
        gen_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M UTC')
    )

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 generator.py stories.json", file=sys.stderr)
        sys.exit(1)
    stories = load_stories(sys.argv[1])
    print(render(stories))
