# utils/topnav.py
import streamlit as st
from textwrap import dedent


def render_top_nav():
    """Pure Streamlit glass-chip top nav (no JS, no iframe)."""

    st.markdown(dedent("""
    <style>
    .chip-bar {
        position: fixed;
        top: 18px;
        right: 18px;
        display: flex;
        gap: 10px;
        z-index: 999999;
        backdrop-filter: blur(8px);
    }

    .chip {
        background: rgba(255,255,255,0.06);
        padding: 8px 14px;
        border-radius: 999px;
        font-weight: 600;
        font-size: 14px;
        color: #eaf4ff;
        text-decoration: none;
        border: 1px solid rgba(255,255,255,0.08);
        transition: all .18s ease;
    }
    .chip:hover {
        background: rgba(116,185,255,0.18);
        color: #001a33;
        transform: translateY(-2px);
    }

    @media (max-width: 900px) {
        .chip-bar { right: 10px; left: 10px; justify-content:center; top: 10px; }
        .chip { font-size: 12px; padding: 6px 10px; }
    }
    </style>

    <div class="chip-bar">
        <a class="chip" href="#about_section">About</a>
        <a class="chip" href="#skills_section">Skills</a>
        <a class="chip" href="#works_section">Works</a>
        <a class="chip" href="#certificates_section">Certificates</a>
        <a class="chip" href="#contact_section">Contact</a>
    </div>
    """), unsafe_allow_html=True)

def add_anchor(anchor_id: str):
    """Creates a scroll target."""
    st.markdown(f"<div id='{anchor_id}'></div>", unsafe_allow_html=True)
