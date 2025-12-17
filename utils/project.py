# utils/project.py

from html import escape
from pathlib import Path
from typing import List, Dict, Optional
import base64
import os

import streamlit as st
import streamlit.components.v1 as components

# Helper: convert local file 

def file_to_data_uri(rel_path: str) -> str:
    """
    Convert a local file path (relative to current working dir) to a base64 data URI.
    If file not found or error, returns the original rel_path (so HTTP/absolute URLs still pass through).
    """
    try:
        if not rel_path:
            return ""
        # if already a data URI or remote URL, return unchanged
        if rel_path.startswith("data:") or rel_path.startswith("http://") or rel_path.startswith("https://"):
            return rel_path

        p = Path(os.getcwd()) / rel_path
        if not p.exists():
            # try as absolute path if user passed absolute
            p2 = Path(rel_path)
            if p2.exists():
                p = p2
            else:
                return rel_path

        ext = p.suffix.lower().lstrip(".")
        mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp", "gif": "image/gif"}.get(ext, None)
        if not mime:
            # unknown extension: let Streamlit handle it by returning path
            return rel_path

        raw = p.read_bytes()
        b64 = base64.b64encode(raw).decode("ascii")
        return f"data:{mime};base64,{b64}"
    except Exception:
        return rel_path

PROJECTS: List[Dict] = [
    {
        "title": "AI Portfolio (This site)",
        "short_description": "My GenAI portfolio built with Streamlit — RAG demos, projects and docs.",
        "full_description": "This portfolio showcases my RAG demos, Streamlit apps, and GenAI experiments. Built with Streamlit, custom components and local embeddings.",
        "tech": ["Streamlit", "Python", "RAG", "LLMOps"],
        "link": "https://github.com/Keerthana-DS-ghub/Genai-portfolio",
        "image_url": "images/Portfolio.jpg",
    },
    {
        "title": "AI-Powered RAG Assistant",
        "short_description": "Context-aware RAG chatbot using LangChain, WatsonX embeddings & ChromaDB.",
        "full_description": "Developed a fully functional RAG chatbot capable of answering questions from uploaded documents. Integrated IBM WatsonX Embeddings with LangChain and ChromaDB.",
        "tech": ["LangChain", "IBM WatsonX", "ChromaDB", "Gradio", "Python"],
        "link": "https://github.com/Keerthana-DS-ghub/AI-Powered-RAG-Assistant-Using-LangChain-and-Gradio",
        "image_url": "images/Rag.webp",
    },
    {
        "title": "NLP Text Preprocessing Pipeline",
        "short_description": "Tokenization, normalization, stopword removal, stemming & lemmatization.",
        "full_description": "Robust text preprocessing pipeline using NLTK / spaCy and Pandas to clean text for downstream tasks.",
        "tech": ["Python", "NLTK", "spaCy", "Pandas"],
        "link": "https://github.com/Keerthana-DS-ghub/Text_Preprocessing/blob/main/README.md",
        "image_url": "images/NLP.png",
    },
    {
        "title": "Time Series Forecasting with ARIMA & SARIMAX",
        "short_description": "Forecasting with ARIMA/SARIMAX; stationarity & seasonality analysis.",
        "full_description": "Built forecasting models using ARIMA and SARIMAX for real-world datasets, with ADF tests and decomposition.",
        "tech": ["Python", "Statsmodels", "Pandas", "Matplotlib"],
        "link": "https://github.com/Keerthana-DS-ghub/Time-Serie-Arima-Sarimax",
        "image_url": "images/TimeSeries.jpg",
    },
    {
    "title": "Credit Card Fraud Detection",
    "short_description": "Machine Learning–based fraud detection on highly imbalanced credit card transaction data.",
    "full_description": (
        "Built a fraud detection system using multiple ML models on a highly imbalanced dataset."
        "Performed EDA, feature scaling, and correlation analysis. "
        "Handled class imbalance using undersampling, oversampling, and SMOTE. "
        "Trained and evaluated Logistic Regression, Decision Tree, Random Forest, SVM, and XGBoost models."
        "Focused on Recall, Precision, F1-score, and ROC-AUC to minimize false negatives in fraud detection."
    ),
    "tech": ["Python","Pandas","NumPy","Scikit-learn","Imbalanced-learn","Matplot","XGBoost"],
    "link": "https://github.com/Keerthana-DS-ghub/Credit_Card_Fraud_Detection",  
    "image_url": "images/creditcard1.png"
    },

    {
        "title": "Real-Time AMFI Mutual Fund Analysis",
        "short_description": "Automated AMFI NAV ingestion into MySQL and Power BI dashboards.",
        "full_description": "Automated extraction of AMFI mutual fund data using Python and wrote ingestion scripts to MySQL; visualized in Power BI.",
        "tech": ["Python", "MySQL", "Power BI"],
        "link": "https://github.com/Keerthana-DS-ghub/-Real-Time-AMFI-Mutual-Fund-Data-Analysis",
        "image_url": "images/Amfi.png",
    },
    {
        "title": "Pandas: Hotel Booking Insights",
        "short_description": "EDA, outlier removal & visualizations for hotel booking data.",
        "full_description": "Merged datasets, removed outliers (3-sigma) and visualized booking trends to extract user behaviour patterns.",
        "tech": ["Pandas", "Matplotlib", "Python"],
        "link": "https://github.com/Keerthana-DS-ghub/Analysing_Hotel_booking",
        "image_url": "images/HotelBooking.png",
    },
    {
        "title": "SQL Project: Sales Forecast & Revenue Analysis",
        "short_description": "Multi-table MySQL analysis: forecasting, margin breakdown, deductions.",
        "full_description": "Multi-table analytics using MySQL covering forecasting, pricing, invoice deductions and manufacturing cost analysis.",
        "tech": ["MySQL", "SQL", "Power BI"],
        "link": "https://github.com/Keerthana-DS-ghub/SQL_Project",
        "image_url": "images/SQL BANNER1.png",
    },
    {
        "title": "Employee Performance Dashboard (Power BI)",
        "short_description": "HR analytics dashboard: attrition, performance, salary trends (DAX).",
        "full_description": "Interactive HR analytics dashboard using Power BI and advanced DAX measures.",
        "tech": ["Power BI", "DAX", "Excel"],
        "link": "https://github.com/Keerthana-DS-ghub/Employee-Performance-Analysis",
        "image_url": "images/PowerBI.jpg",
    },
]

def render_glass_projects(projects: Optional[List[Dict]] = None, cols: int = 3, card_width: int = 340):
    projects = projects if projects is not None else PROJECTS
    if not projects:
        st.info("No projects to show.")
        return

    cards_html = []
    for idx, p in enumerate(projects):
        title = escape(p.get("title", "Untitled"))
        short = escape(p.get("short_description") or p.get("description") or "")
        raw_img = p.get("image_url") or p.get("image") or ""
        # convert local files to data uri for iframe-safe rendering
        img_src = file_to_data_uri(raw_img) if raw_img else ""
        img = escape(img_src)
        tech = p.get("tech") or p.get("tags") or []
        tech_html = " ".join(f"<span class='tag'>{escape(t)}</span>" for t in tech[:6])
        raw_link = p.get("link") or p.get("url")
        link = escape(raw_link) if raw_link and raw_link != "#" else ""


        if img:
            thumb_html = f'<div class="card-thumb"><img src="{img}" alt="{title}" loading="lazy"/></div>'
        else:
            thumb_html = '<div class="card-thumb empty">No image</div>'

        card = f"""
        <div class="glass-card" data-idx="{idx}">
            {thumb_html}
            <div class="card-body">
                <div class="card-title">{title}</div>
                <div class="card-desc">{short}</div>
                <div class="card-tags">{tech_html}</div>
                <div class="card-actions">
                    <a class="btn-link" href="{link}" target="_blank" rel="noreferrer">Repo</a>
                </div>
            </div>
        </div>
        """
        cards_html.append(card)

    html = f"""
    <style>
    .glass-wrap{{display:grid;grid-template-columns:repeat({cols}, minmax(0,1fr));gap:20px;align-items:start}}
    @media (max-width:1100px){{ .glass-wrap{{grid-template-columns:repeat(2, minmax(0,1fr))}} }}
    @media (max-width:640px){{ .glass-wrap{{grid-template-columns:repeat(1, minmax(0,1fr))}} }}

    .glass-card{{background:linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02)); border:1px solid rgba(255,255,255,0.06); border-radius:14px; overflow:hidden; box-shadow: 0 8px 30px rgba(2,6,23,0.6); backdrop-filter: blur(6px); display:flex; flex-direction:column; min-height:260px; transition:transform .18s ease, box-shadow .18s ease}}
    .glass-card:hover{{transform:translateY(-6px); box-shadow: 0 18px 48px rgba(2,6,23,0.75)}}
    .card-thumb{{height:160px; background:#eef2ff; overflow:hidden; display:block}}
    .card-thumb img{{width:100%; height:100%; object-fit:cover; display:block}}
    .card-thumb.empty{{display:flex;align-items:center;justify-content:center;color:#7b8aa2;background:linear-gradient(180deg,#f6f9ff,#eef2ff)}}
    .card-body{{padding:14px; display:flex; flex-direction:column; gap:8px; flex:1}}
    .card-title{{font-weight:700; color:#fff; font-size:1.05rem; margin-bottom:4px}}
    .card-desc{{color:#dce9ff; font-size:0.92rem; line-height:1.25; max-height:3.6em; overflow:hidden}}
    .card-tags{{margin-top:6px}}
    .tag{{display:inline-block;padding:6px 8px;background:rgba(255,255,255,0.04);border-radius:999px;font-size:12px;margin-right:6px;color:#cfe9ff}}
    .card-actions{{margin-top:auto; display:flex; gap:8px; align-items:center}}
    .btn-link{{padding:8px 12px;border-radius:10px;background:transparent;border:1px solid rgba(255,255,255,0.06);color:#cfe9ff;text-decoration:none;font-weight:600}}
    </style>

    <div class="glass-wrap">
        {''.join(cards_html)}
    </div>
    """

    try:
        # height heuristic: base + rows * extra
        rows = max(1, (len(projects) + cols - 1) // cols)
        iframe_h = 340 + (rows - 1) * 40
        components.html(html, height=iframe_h, scrolling=True)
    except Exception:
        # fallback to simple Streamlit columns (server side)
        cols_layout = st.columns(cols)
        for i, p in enumerate(projects):
            col = cols_layout[i % cols]
            with col:
                st.subheader(p.get("title", "Untitled"))
                if p.get("image_url"):
                    try:
                        # Streamlit can show local images normally
                        st.image(p.get("image_url"), use_column_width=True)
                    except Exception:
                        st.write("Image:", p.get("image_url"))
                st.write(p.get("short_description") or p.get("description") or "")
                tech = p.get("tech") or p.get("tags") or []
                if tech:
                    st.markdown("**Tech:** " + ", ".join(tech))
                if p.get("link"):
                    st.markdown(f"[Repository / Demo]({p.get('link')})")


def render_glass_carousel(projects: Optional[List[Dict]] = None, height: int = 780, card_width: int = 360, visible: int = 3):
    """
    Render a horizontal glass-morphism carousel of project cards.

    Args:
        projects: list of project dicts (defaults to PROJECTS)
        height: iframe height to reserve for the carousel (px)
        card_width: preferred card width (px)
        visible: hint for how many cards should be visible (not enforced)
    """
    projects = projects if projects is not None else PROJECTS
    if not projects:
        st.info("No projects to show.")
        return

    slides = []
    for idx, p in enumerate(projects):
        title = escape(p.get("title", "Untitled"))
        short = escape(p.get("short_description") or p.get("description") or "")
        raw_img = p.get("image_url") or p.get("image") or ""
        img_src = file_to_data_uri(raw_img) if raw_img else ""
        img = escape(img_src)
        tech = p.get("tech") or p.get("tags") or []
        tech_html = " ".join(f"<span class='tag'>{escape(t)}</span>" for t in tech[:6])
        raw_link = p.get("link") or p.get("url")
        link = escape(raw_link) if raw_link and raw_link != "#" else ""


        thumb = (
            f'<div class="media"><img src="{img}" alt="{title}" loading="lazy"/></div>'
            if img else '<div class="media empty">No image</div>'
        )

        card_html = f"""
        <div class="slide" data-idx="{idx}" role="group" aria-label="project {idx+1}">
          <div class="card">
            {thumb}
            <div class="body">
              <div class="card-title">{title}</div>
              <div class="card-desc">{short}</div>
              <div class="tags">{tech_html}</div>
              <div class="card-actions">
              {(
                  f'<a class="btn-link" href="{link}" target="_blank" '
                  f'rel="noreferrer noopener">Repo</a>'
              ) if link else ''}
                  </div>

            </div>
          </div>
        </div>
        """
        slides.append(card_html)

    # Template uses placeholders replaced below to avoid f-string/css/JS brace conflicts
    html_template = """
    <style>
    :root{ --card-radius:14px; --card-gap:20px; --arrow-size:48px; }

    .carousel-shell{position:relative;padding:18px 8px;}
    .carousel-viewport{display:flex;gap:var(--card-gap);overflow-x:auto;scroll-snap-type:x mandatory;padding:12px;scroll-behavior:smooth;align-items:start}
    .carousel-viewport::-webkit-scrollbar{height:10px}
    .slide{flex:0 0 __CARD_WIDTH__px;scroll-snap-align:center}
    .card{
      background:linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.015));
      border:1px solid rgba(255,255,255,0.04);
      border-radius:var(--card-radius);
      overflow:hidden;
      box-shadow: 0 10px 40px rgba(2,6,23,0.55);
      backdrop-filter: blur(6px);
      display:flex;
      flex-direction:column;
      min-height:__MIN_HEIGHT__px;
    }

    /* media area: larger, respects rounded corners */
    .card > .media{
     height:280px;           /* fixed media height */
     overflow:hidden;
   }

    .card > .media img{
     width:100%;
     height:100%;
     object-fit:cover;
   }

    .media.empty{display:flex;align-items:center;justify-content:center;color:#7b8aa2;padding:24px}

    .body{padding:18px;display:flex;flex-direction:column;gap:10px;flex:1}
    .card-title{font-weight:800;color:#fff;font-size:1.05rem}
    .card-desc{color:#dce9ff;max-height:4.2em;overflow:hidden}
    .tags{margin-top:8px}
    .tag{display:inline-block;padding:6px 10px;background:rgba(255,255,255,0.03);border-radius:999px;font-size:12px;margin-right:6px;color:#cfe9ff}
    .card-actions{margin-top:auto;display:flex;gap:8px;align-items:center}
    .btn-link{padding:10px 14px;border-radius:12px;background:transparent;border:1px solid rgba(255,255,255,0.06);color:#cfe9ff;text-decoration:none;font-weight:700}

    /* arrows */
    .carousel-arrow{position:absolute;top:50%;transform:translateY(-50%);width:var(--arrow-size);height:var(--arrow-size);border-radius:12px;border:1px solid rgba(255,255,255,0.06);background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));display:flex;align-items:center;justify-content:center;cursor:pointer;box-shadow:0 8px 22px rgba(2,6,23,0.6);z-index:2}
    .arrow-left{left:8px}
    .arrow-right{right:8px}
    .arrow-disabled{opacity:0.28;pointer-events:none}

    /* responsive */
    @media (max-width:1100px){ .slide{flex:0 0 __CARD_WIDTH_MOBILE__px} }
    @media (max-width:760px){ .slide{flex:0 0 __CARD_WIDTH_MOBILE2__px} .carousel-arrow{display:none} }
    </style>

    <div class="carousel-shell" role="region" aria-label="projects carousel">
      <div class="carousel-viewport" id="cv" tabindex="0">
        __SLIDES__
      </div>

      <button class="carousel-arrow arrow-left" id="cprev" title="Previous" aria-label="previous project">‹</button>
      <button class="carousel-arrow arrow-right" id="cnext" title="Next" aria-label="next project">›</button>
    </div>

    <script>
    (function(){
      const cv = document.getElementById('cv');
      const prev = document.getElementById('cprev');
      const next = document.getElementById('cnext');
      const cardW = __CARD_WIDTH__ + 20; // card width + gap estimate

      function scrollByAmount(amount) {
        if (!cv) return;
        cv.scrollBy({left: amount, behavior: 'smooth'});
      }

      prev.addEventListener('click', ()=> scrollByAmount(-cardW));
      next.addEventListener('click', ()=> scrollByAmount(cardW));

      // keyboard support
      cv.addEventListener('keydown', function(e){
        if(e.key === 'ArrowRight') { scrollByAmount(cardW); e.preventDefault(); }
        if(e.key === 'ArrowLeft') { scrollByAmount(-cardW); e.preventDefault(); }
      });

      function updateArrows() {
        if (!cv) return;
        const atStart = cv.scrollLeft <= 10;
        const atEnd = cv.scrollLeft + cv.clientWidth >= cv.scrollWidth - 10;
        prev.classList.toggle('arrow-disabled', atStart);
        next.classList.toggle('arrow-disabled', atEnd);
      }

      cv.addEventListener('scroll', updateArrows);
      window.addEventListener('resize', updateArrows);
      setTimeout(updateArrows, 200);

    })();
    </script>
    """

    # Replace placeholders safely
    html = html_template.replace("__CARD_WIDTH__", str(card_width))
    min_h = max(320, int(height - 80))
    html = html.replace("__MIN_HEIGHT__", str(min_h))
    html = html.replace("__SLIDES__", "".join(slides))
    html = html.replace("__CARD_WIDTH_MOBILE__", str(int(card_width * 0.9)))
    html = html.replace("__CARD_WIDTH_MOBILE2__", str(int(card_width * 0.78)))

    try:
        # allocate iframe height large enough so images/cards aren't clipped
        iframe_height = max(height, min_h + 40)
        components.html(html, height=iframe_height, scrolling=False)
    except Exception:
        # fallback to grid renderer (server-side)
        render_glass_projects(projects, cols=3, card_width=card_width)
