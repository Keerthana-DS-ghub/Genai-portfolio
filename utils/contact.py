# utils/contact.py
from html import escape
import streamlit.components.v1 as components
import base64

__all__ = ["render_contact_professional"]

ICON_LINKEDIN = "https://cdn-icons-png.flaticon.com/512/3536/3536505.png"
ICON_GITHUB   = "https://cdn-icons-png.flaticon.com/512/733/733553.png"
ICON_MAIL     = "https://cdn-icons-png.flaticon.com/512/732/732200.png"


def load_base64(path):
    """Convert local image file into base64 string for HTML embedding."""
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None


def _load_defaults():
    """Safely load info + socials from constants."""
    try:
        from utils.constants import info, socials
        return info or {}, socials or {}
    except Exception:
        return {}, {}


def render_contact_professional(info=None, socials=None, height=330):
    # Load defaults safely
    
    default_info, default_socials = _load_defaults()

    info = info or default_info
    socials = socials or default_socials

    # Extract fields

    name = escape(info.get("name", "Keerthana S"))
    role = escape(info.get("title", "GenAI Engineer | LLMOps | Data Scientist"))
    email = escape(info.get("Email", ""))
    linkedin = escape(socials.get("LinkedIn", ""))
    github = escape(socials.get("GitHub", ""))
    location = escape(info.get("Location", "Chennai, India"))
    photo_path = info.get("ProfileImage", "").strip()

    initials = "".join([p[0].upper() for p in name.split()][:2])

    # Avatar — Base64 Image
    
    avatar_html = ""
    if photo_path:
        base64_img = load_base64(photo_path)
        if base64_img:
            avatar_html = (
                f'<img src="data:image/png;base64,{base64_img}" '
                f'class="contact-avatar-img"/>'
            )

    # Fallback if image not loaded
    if not avatar_html:
        avatar_html = f'<div class="contact-avatar-fallback">{initials}</div>'

    # Social Icons
    
    socials_html = f"""
    <a href="{linkedin}" target="_blank" class="contact-social-pill"><img src="{ICON_LINKEDIN}" /></a>
    <a href="{github}" target="_blank" class="contact-social-pill"><img src="{ICON_GITHUB}" /></a>
    <a href="mailto:{email}" class="contact-social-pill"><img src="{ICON_MAIL}" /></a>
    """

    email_html = (
        f'<a href="mailto:{email}" class="contact-email">{email}</a>'
        if email else "Not provided"
    )

    
    # HTML + CSS
    
    html = f"""
    <style>
    .contact-card {{
        max-width: 840px;
        margin: 20px auto;
        background: rgba(15,23,42,0.88);
        border-radius: 22px;
        padding: 26px 30px;
        display: flex;
        gap: 24px;
        align-items: center;
        border: 1px solid rgba(255,255,255,0.06);
        box-shadow: 0 20px 50px rgba(0,0,0,0.55);
        backdrop-filter: blur(14px);
    }}

    .contact-avatar {{
        width: 120px;
        height: 120px;
        border-radius: 18px;
        overflow: hidden;
        background: #0ea5e9;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 40px;
        font-weight: 800;
        color: white;
    }}

    .contact-avatar-img {{
        width: 100%;
        height: 100%;
        display: block !important;
        object-fit: cover;
        object-position: top center;
        border-radius: 18px;
    }}

    .contact-avatar-fallback {{
        width: 120px;
        height: 120px;
        border-radius: 18px;
        background: #0ea5e9;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 42px;
        font-weight: 700;
        color: white;
    }}

    .contact-content {{
        flex: 1;
        color: #e5edff;
    }}

    .contact-name {{
        font-size: 26px;
        font-weight: 800;
        margin-bottom: 4px;
    }}

    .contact-role {{
        font-size: 15px;
        opacity: 0.9;
        margin-bottom: 12px;
    }}

    .location-pill {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 999px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        font-size: 14px;
        margin-bottom: 10px;
    }}

    .contact-social-row {{
        display: flex;
        gap: 12px;
        margin-bottom: 12px;
    }}

    .contact-social-pill {{
        width: 40px;
        height: 40px;
        border-radius: 999px;
        background: rgba(15,23,42,0.95);
        border: 1px solid rgba(148,163,184,0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        transition: 0.15s;
    }}

    .contact-social-pill:hover {{
        transform: translateY(-3px);
        border-color: #38bdf8;
        background: rgba(56,189,248,0.2);
    }}

    .contact-social-pill img {{
        width: 20px;
    }}

    .contact-email {{
        color: #c7e4ff;
        font-weight: 600;
        text-decoration: underline;
    }}

    .contact-caption {{
        text-align:center;
        margin-top:8px;
        font-size: 12px;
        opacity: 0.7;
    }}
    </style>

    <div class="contact-card">
        <div class="contact-avatar">{avatar_html}</div>

        <div class="contact-content">
            <div class="contact-name">{name}</div>
            <div class="contact-role">{role}</div>

            <div class="location-pill">📍 {location}</div>

            <div class="contact-social-row">{socials_html}</div>

            <div><strong>Email:</strong> {email_html}</div>

            <div class="contact-caption">
                Prefer quick answers? You can chat with my AI assistant anytime.
            </div>
        </div>
    </div>
    """

    components.html(html, height=height + 10, scrolling=False)
