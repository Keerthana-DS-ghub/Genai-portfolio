# landing.py
import streamlit as st
import streamlit.components.v1 as components
import traceback
import base64
from pathlib import Path
from typing import List, Dict
from html import escape

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="GenAI Portfolio",
    layout="wide",
    page_icon="👩‍💻",
    initial_sidebar_state="collapsed",
)

from pathlib import Path

# ================= LOAD GLOBAL CSS =================
def load_css(relative_path: str):
    css_path = Path(__file__).parent / relative_path
    if css_path.exists():
        st.markdown(
            f"<style>{css_path.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )
    else:
        st.error(f"CSS file not found at: {css_path}")

load_css("styles/styles_main.css")



# ================= BACKGROUND =================
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], .stApp {
    background: linear-gradient(135deg,#050A14,#071A2F,#0A2F52) !important;
}
[data-testid="stSidebar"] { display:none !important; }
</style>
""", unsafe_allow_html=True)

# ================= NAV / HERO =================
from utils.topnav import render_top_nav, add_anchor
from utils.hero import render_hero
from utils.chat_strip import render_chat_strip



render_top_nav()

# ================= CONSTANTS =================
try:
    from utils.constants import info, socials
except Exception:
    info = {
        "name": "Keerthana S",
        "Intro": "GenAI | LLMOps | RAG Engineer",
        "About": "Building reliable, user-centric AI systems.",
        "Email": "skeerthi.datascience@gmail.com",
    }
    socials = {}

# ================= SKILLS =================
try:
    from utils.skill import skills as SKILLS_LIST, render_skills_html
except Exception:
    SKILLS_LIST = []
    def render_skills_html(*a, **k): return ""

# ================= PROJECTS =================
try:
    from utils.project import PROJECTS, render_glass_carousel
except Exception:
    PROJECTS = []
    render_glass_carousel = None

# ================= CERTIFICATES =================
try:
    from utils.certificates import get_certificate_display_data
except Exception:
    def get_certificate_display_data(): return []

# ================= CONTACT =================
from utils.contact import render_contact_professional

# =================================================
def render_landing():

    # -------- HERO --------
    add_anchor("about_section")
    render_hero(info, socials)
    render_chat_strip(info, socials)

    # -------- SKILLS --------
    add_anchor("skills_section")
    st.markdown("---")
    st.subheader("📚 Skills")
    st.components.v1.html(
        f"<div style='color:white'>{render_skills_html(SKILLS_LIST, columns=2)}</div>",
        height=480,
        scrolling=True,
    )

    # -------- PROJECTS --------
    add_anchor("works_section")
    st.markdown("---")
    st.subheader("💼 My Works")
    if callable(render_glass_carousel):
        render_glass_carousel(PROJECTS, height=500, card_width=520, visible=2)

        # -------- CERTIFICATES --------
    add_anchor("certificates_section")
    st.markdown("---")
    st.subheader("📜 Certificates")

    certs = get_certificate_display_data()

    if not certs:
        st.info("No certificates added yet.")
    else:
        cards_html = ""

        for c in certs:
            title = escape(c.get("title", ""))
            issuer = escape(c.get("issuer", ""))
            date = escape(c.get("date", ""))
            category = escape(c.get("category", "").upper())

            # image
            img_b64 = ""
            try:
                raw = Path(c.get("image", "")).read_bytes()
                img_b64 = "data:image/png;base64," + base64.b64encode(raw).decode()
            except Exception:
                pass

            thumb = (
                f"<img class='cert-thumb' src='{img_b64}'>"
                if img_b64
                else "<div class='cert-thumb-placeholder'>No Image</div>"
            )

            pill = f"<div class='cert-category'>{category}</div>" if category else ""

            cards_html += f"""
            <div class="cert-card">
                <div class="cert-thumb-wrap">{thumb}</div>
                <div class="cert-meta">
                    {pill}
                    <div class="cert-title">{title}</div>
                    <div class="cert-issuer">{issuer} • {date}</div>
                </div>
            </div>
            """

        st.components.v1.html(f"""
<style>
.cert-grid {{
  display:grid;
  grid-template-columns:repeat(2,1fr);
  gap:22px;
}}
@media(max-width:900px){{.cert-grid{{grid-template-columns:1fr;}}}}
.cert-card {{
  display:flex; gap:16px; padding:16px;
  border-radius:14px;
  background:rgba(255,255,255,0.04);
  border:1px solid rgba(255,255,255,0.08);
}}
.cert-thumb{{width:120px;height:120px;object-fit:cover;border-radius:10px;}}
.cert-thumb-placeholder{{width:120px;height:120px;
  background:rgba(255,255,255,0.12);
  display:flex;align-items:center;justify-content:center;
}}
.cert-title{{font-weight:700;color:white}}
.cert-issuer{{font-size:14px;color:#dbeafe}}
.cert-category {{
  display:inline-block;
  margin-bottom:6px;
  padding:4px 10px;
  font-size:11px;
  font-weight:700;
  border-radius:999px;
  color:#93c5fd;
  background:rgba(59,130,246,0.15);
  border:1px solid rgba(59,130,246,0.3);
}}
</style>

<div class="cert-grid">{cards_html}</div>
""", height=520)

    # -------- CONTACT --------
    add_anchor("contact_section")
    st.markdown("---")
    st.subheader("📬 Contact")
    render_contact_professional(info=info, socials=socials)

    st.markdown(
        "<div style='text-align:center;color:#cbd5f5;font-size:0.85rem'>Built with Streamlit · Designed & engineered by Keerthana S\n © 2025 Keerthana S. All rights reserved.</div>",
        unsafe_allow_html=True,
    )


# ================= ENTRY =================
if __name__ == "__main__":
    try:
        render_landing()
    except Exception:
        st.error("Landing page error")
        st.text(traceback.format_exc())
