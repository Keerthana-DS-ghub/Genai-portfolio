# utils/skill.py
import html as _html
import os

def render_skills_html(skills_list, columns=2, card_size=96):
    try:
        cols = max(1, int(columns))
    except Exception:
        cols = 2
    cs = int(card_size)

    groups = skills_list or []

    # build cards
    cards = []
    for g in groups:
        cat = _html.escape(g.get("category", ""))
        grp_icon = _html.escape(g.get("icon", ""))
        items_raw = g.get("items", []) or []
        pill_html = []
        for it in items_raw:
            if isinstance(it, dict):
                name = _html.escape(it.get("name", ""))
            else:
                name = _html.escape(str(it))
            pill_html.append(f'<button class="pill" type="button" aria-label="{name}">{name}</button>')

        cards.append(f'''
        <section class="skill-card" aria-labelledby="cat-{cat}">
          <div class="card-head">
            <div class="cat-left"><span class="grp-icon">{grp_icon}</span><h3 id="cat-{cat}" class="cat-title">{cat}</h3></div>
            <div class="count">• {len(items_raw)} skills</div>
          </div>
          <div class="card-body">
            {"".join(pill_html)}
          </div>
        </section>
        ''')

    # final html + css
    html = f'''
    <div class="skills-root">
      <div class="skills-grid">
        {"".join(cards)}
      </div>
    </div>

    <style>
    :root {{
      --glass-bg: rgba(255,255,255,0.02);
      --glass-border: rgba(255,255,255,0.06);
      --accent-a: #60a5fa;
      --accent-b: #7c3aed;
      --text: #e7f4ff;
      --muted: rgba(223,243,255,0.8);
      --pill-bg: rgba(255,255,255,0.03);
      --pill-border: rgba(255,255,255,0.04);
      --pill-radius: 999px;
      --pill-pad-vert: 8px;
      --pill-pad-horz: 12px;
      --card-radius: 14px;
      --card-padding: 16px;
      --tile-size: {cs}px;
    }}

    .skills-root {{ width:100%; padding:12px 6px; box-sizing:border-box; font-family: Inter, system-ui, -apple-system; color:var(--text); }}
    .skills-grid {{
      display: grid;
      grid-template-columns: repeat({cols}, 1fr);
      gap: 16px;
    }}

    .skill-card {{
      background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.02));
      border: 1px solid var(--glass-border);
      border-radius: var(--card-radius);
      padding: var(--card-padding);
      box-shadow: 0 12px 30px rgba(2,6,23,0.6), inset 0 -6px 30px rgba(8,45,90,0.06);
      transition: transform .16s ease, box-shadow .18s ease;
    }}
    .skill-card:focus-within, .skill-card:hover {{ transform: translateY(-4px); box-shadow: 0 20px 44px rgba(2,6,23,0.66); }}

    .card-head {{ display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:10px; }}
    .cat-left {{ display:flex; align-items:center; gap:12px; }}
    .grp-icon {{
      width:40px; height:40px; display:flex; align-items:center; justify-content:center; border-radius:10px;
      background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)); font-size:18px;
      border:1px solid rgba(255,255,255,0.03);
    }}
    .cat-title {{
      margin:0;
      padding:0;
      font-size:16px;
      font-weight:700;
      color:#87CFFF !important;
    }}

    .count {{ color:var(--muted); font-size:13px; }}

    .card-body {{
      display:flex;
      flex-wrap:wrap;
      gap:10px;
    }}

    .pill {{
      display:inline-flex;
      align-items:center;
      justify-content:center;
      padding: var(--pill-pad-vert) var(--pill-pad-horz);
      border-radius: var(--pill-radius);
      background: var(--pill-bg);
      border: 1px solid var(--pill-border);
      color: var(--text);
      font-size:13px;
      cursor: default;
      transition: transform .14s ease, background .14s ease, box-shadow .14s ease;
      opacity:0;
      transform: translateY(8px);
      animation: pillIn .32s forwards;
    }}
    .pill:hover {{ transform: translateY(-4px) scale(1.02); box-shadow: 0 10px 22px rgba(2,6,23,0.5); }}
    .pill:focus {{ outline: 2px solid rgba(96,165,250,0.12); }}

    /* staggered animation using nth-child */
    .card-body .pill:nth-child(1) {{ animation-delay: 0.03s; }}
    .card-body .pill:nth-child(2) {{ animation-delay: 0.06s; }}
    .card-body .pill:nth-child(3) {{ animation-delay: 0.09s; }}
    .card-body .pill:nth-child(4) {{ animation-delay: 0.12s; }}
    .card-body .pill:nth-child(5) {{ animation-delay: 0.15s; }}
    .card-body .pill:nth-child(6) {{ animation-delay: 0.18s; }}
    .card-body .pill:nth-child(7) {{ animation-delay: 0.21s; }}
    .card-body .pill:nth-child(8) {{ animation-delay: 0.24s; }}
    .card-body .pill:nth-child(9) {{ animation-delay: 0.27s; }}

    @keyframes pillIn {{
      to {{ opacity:1; transform: none; }}
    }}

    /* responsive */
    @media (max-width: 980px) {{
      .skills-grid {{ grid-template-columns: repeat(1, 1fr); }}
    }}
    </style>
    '''

    return html


# -------------------- skills --------------------
skills = [
    {
        "category": "Programming & Data Science",
        "icon": "💻",
        "items": [
            "Python",
            "Pandas",
            "NumPy",
            "Scikit-learn",
            "SQL",
            "Statistics",
            "Probability",
            "Exploratory Data Analysis (EDA)",
            "Machine Learning"
        ]
    },
    {
        "category": "AI/ML & NLP",
        "icon": "🤖",
        "items": [
            "Regression",
            "Classification",
            "Model Evaluation",
            "LLMs (RAG, Embeddings, Prompt Engineering)",
            "Tokenization",
            "Lemmatization",
            "Stemming"
        ]
    },
    {
        "category": "Frameworks & Tools",
        "icon": "🛠️",
        "items": [
            "LangChain",
            "Hugging Face Transformers",
            "ChromaDB (Vector DB)",
            "FastAPI",
            "Flask",
            "Matplotlib",
            "Seaborn"
        ]
    },
    {
        "category": "Data & Deployment",
        "icon": "☁️",
        "items": [
            "Data Preprocessing",
            "Feature Engineering",
            "Real-time Data Pipelines",
            "Git / GitHub",
            "Power BI (Visualization)"
        ]
    }
]

# small import confirmation printed to terminal
print("[utils.skill] glass-pills version loaded — groups =", len(skills))
