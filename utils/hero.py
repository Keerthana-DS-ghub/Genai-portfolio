# utils/hero.py

import streamlit as st
from PIL import Image
import html as _html

# ---------------- Animated About Text ----------------
def build_animated_text(text: str, font_size: int = 22, step: float = 0.06):
    """Return HTML for word-by-word fade-in animated paragraph."""
    words = _html.escape(text).split()
    delay = 0.0
    spans = ""

    for w in words:
        spans += (
            f"<span style='opacity:0; "
            f"animation: fadeIn 0.7s forwards; "
            f"animation-delay:{delay:.2f}s; "
            f"display:inline-block; margin-right:6px;'>{w}</span>"
        )
        delay += step

    html = f"""
    <style>
    @keyframes fadeIn {{
        0%   {{ opacity:0; transform: translateY(6px); }}
        100% {{ opacity:1; transform: translateY(0);    }}
    }}
    .about-anim {{
        font-size:{font_size}px;
        color:#e8f1ff;
        line-height:1.65;
        margin-top:14px;
        max-width:780px;
    }}
    </style>

    <div class="about-anim">{spans}</div>
    """
    return html


# ---------------- HERO SECTION (MAIN) ----------------
def render_hero(info, socials):
    # Global layout tweaks: reduce top padding and center left column content
    st.markdown(
        """
        <style>
        /* Reduce default Streamlit top padding */
        section.main > div.block-container {
            padding-top: 1.5rem !important;
        }

        /* Vertically center hero text */
        .hero-left {
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Safely read data
    name_raw = info.get("name", "Keerthana")
    name = _html.escape(str(name_raw).strip())
    title = _html.escape(info.get("title", "GenAI Engineer | LLMOps | Data Scientist"))
    about = info.get("About", info.get("Intro", ""))
    email = info.get("Email", "")
    photo = info.get("ProfileImage", "images/profile1.png")

    # Socials (not directly used here but kept if needed later)
    linkedin = socials.get("LinkedIn", "") if isinstance(socials, dict) else ""
    github   = socials.get("GitHub", "")   if isinstance(socials, dict) else ""

    col_left, col_right = st.columns([2, 1])

    # ------------ LEFT: TEXT ------------
    with col_left:
        st.markdown('<div class="hero-left">', unsafe_allow_html=True)

        # Main heading
        st.markdown(
            f"""
            <h1 style="
                font-size:46px;
                color:#e9f3ff;
                margin: 0 0 8px 0;
            ">
                I'm <span style="color:#74b9ff;">{name}</span>
            </h1>
            """,
            unsafe_allow_html=True,
        )

        # Subtitle
        st.markdown(
            f"""
            <h3 style="
                font-size:28px;
                color:#dceeff;
                margin: 0 0 10px 0;
            ">
                {title}
            </h3>
            """,
            unsafe_allow_html=True,
        )

        # Animated about paragraph
        animated = build_animated_text(about, font_size=22, step=0.05)
        st.markdown(animated, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
    # Vertical alignment spacer to match centered hero text
        st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)
        try:
            st.image(photo, width=420)
        except Exception:
            try:
                img = Image.open(photo)
                st.image(img, width=420)
            except Exception as e2:
                st.warning(
                    f"Profile image not found. Tried: {photo}. Error: {e2}"
                    )


