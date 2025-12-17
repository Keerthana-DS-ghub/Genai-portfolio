# 2_Chat with AI.py

from __future__ import annotations
import streamlit as st
import requests
import json
import time
from dotenv import load_dotenv

import os
import importlib
import types
from pathlib import Path
from typing import Optional
from utils.certificates import certificates_as_text


load_dotenv()

FAQ = [
    "What are her strengths and weaknesses?",
    "What is her expected salary?",
    "What is her latest project?",
    "When can she start work?",
    "Tell me about her professional background.",
    "What is her skillset?",
    "What is her contact information?",
    "What are her achievements?"
]


def local_css(file_name: str):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

# ---------------------- PROFILE loader (uses Landing.py or profile.json) ----------------------
PROFILE_PATH = "profile.json"

def build_profile_from_landing_module(landing_module: types.ModuleType):
    """Convert a landing module (Landing.py) to a PROFILE dict used by the chat UI."""
    PROFILE = {
        "name": None,
        "headline": None,
        "summary": None,
        "resume_bullets": [],
        "projects": {}
    }

    landing_info = getattr(landing_module, "info", {}) or {}
    PROFILE["name"] = landing_info.get("Full_Name") or landing_info.get("Name") or landing_info.get("name")
    profile_headline = landing_info.get("Intro") or landing_info.get("headline") or landing_info.get("Subject")
    PROFILE["headline"] = profile_headline or ""
    PROFILE["summary"] = landing_info.get("About") or landing_info.get("summary") or ""

    bullets = []
    if landing_info.get("Project"):
        bullets.append("Public projects / course links")
    if landing_info.get("Email"):
        bullets.append(f"Contact: {landing_info.get('Email')}")
    PROFILE["resume_bullets"] = bullets

    landing_projects = getattr(landing_module, "projects", []) or []
    def slugify(s: str):
        return "".join(c.lower() if c.isalnum() else "_" for c in s)[:50]

    for p in landing_projects:
        title = p.get("title") or p.get("name") or "Untitled Project"
        key = slugify(title)
        PROFILE["projects"][key] = {
            "title": title,
            "summary": p.get("description", ""),
            "link": p.get("link"),
            "image_url": p.get("image_url"),
            "highlights": []
        }

    endorsements = getattr(landing_module, "endorsements", {}) or {}
    if endorsements:
        PROFILE.setdefault("resume_bullets", []).append("Has endorsements / testimonials")
    if getattr(landing_module, "embed_rss", None):
        PROFILE.setdefault("resume_bullets", []).append("Public writing / blog feed available")

    return PROFILE

def load_profile(prefer_landing=True, profile_path=PROFILE_PATH):
    """Load profile data, preferring a Landing module if present."""
    loaded_profile = None
    if prefer_landing:
        try:
            try:
                landing = importlib.import_module("Landing")
            except Exception:
                landing = importlib.import_module("landing")
            loaded_profile = build_profile_from_landing_module(landing)
        except Exception as e:
            # Print warning to console and continue; UI will show fallback message
            print("Warning: cannot load Landing module:", e)
            loaded_profile = None

    ppath = Path(profile_path)
    if ppath.exists():
        try:
            with open(ppath, "r", encoding="utf-8") as f:
                file_profile = json.load(f)
            if loaded_profile:
                # merge missing fields from file_profile into loaded_profile
                for k, v in file_profile.items():
                    if k not in loaded_profile or not loaded_profile.get(k):
                        loaded_profile[k] = v
                return loaded_profile
            else:
                return file_profile
        except Exception:
            pass

    if loaded_profile:
        return loaded_profile

    # Default fallback profile
    return {
        "name": "Keerthana",
        "headline": "Data Scientist | LLMOps | Generative AI",
        "summary": "Data Scientist experienced in GenAI, RAG, Streamlit demos, and real-time pipelines.",
        "resume_bullets": [],
        "projects": {}
    }

PROFILE = load_profile(prefer_landing=True)

# ---------------------- bio.txt loader ----------------------
def load_bio_txt(path="bio.txt", max_chars=4000):
    """Load custom biography text from bio.txt if it exists."""
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                text = f.read().strip()
                return text[:max_chars]
    except Exception:
        pass
    return None

BIO_TEXT = load_bio_txt()
if BIO_TEXT and isinstance(PROFILE, dict):
    PROFILE["summary"] = BIO_TEXT

# --- Config / env ---
IBM_APIKEY = os.getenv("IBM_APIKEY")
_raw_ml_base = (os.getenv("WATSONX_RUNTIME_URL") or os.getenv("IBM_ML_URL") or os.getenv("IBM_URL") or "").rstrip('/')
for suffix in ["/ml/v1", "/ml/v4", "/ml", "/api"]:
    if _raw_ml_base.endswith(suffix):
        _raw_ml_base = _raw_ml_base[: -len(suffix)].rstrip('/')
ML_BASE = _raw_ml_base
DEPLOYMENT_ID = os.getenv("WATSONX_DEPLOYMENT_ID")
API_VERSION = "2021-05-01"

# --- Token cache ---
_token_cache = {"token": None, "expires_at": 0}

def get_iam_token_cached():
    """Get an IAM token using the API key and cache it until near expiry."""
    now = int(time.time())
    if _token_cache["token"] and now < _token_cache["expires_at"] - 30:
        return _token_cache["token"]
    if not IBM_APIKEY:
        raise RuntimeError("Missing IBM_APIKEY in environment.")
    url = "https://iam.cloud.ibm.com/identity/token"
    data = {"grant_type": "urn:ibm:params:oauth:grant-type:apikey", "apikey": IBM_APIKEY}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(url, data=data, headers=headers, timeout=30)
    r.raise_for_status()
    j = r.json()
    token = j.get("access_token")
    expires_in = int(j.get("expires_in", 3600))
    _token_cache["token"] = token
    _token_cache["expires_at"] = now + expires_in
    return token

def extract_text(obj) -> Optional[str]:
    """Recursively extract likely assistant text from watsonx JSON shapes."""
    if obj is None:
        return None
    if isinstance(obj, str):
        return obj
    if isinstance(obj, list):
        for i in obj:
            t = extract_text(i)
            if t:
                return t
        return None
    if isinstance(obj, dict):
        # special Llama-style path
        if "choices" in obj and isinstance(obj["choices"], list) and obj["choices"]:
            try:
                c = obj["choices"][0]
                if isinstance(c, dict) and "message" in c and isinstance(c["message"], dict):
                    cont = c["message"].get("content")
                    if cont:
                        return extract_text(cont)
            except Exception:
                pass
        for k in ("message", "messages", "content", "text", "output", "generated_text", "response"):
            if k in obj:
                t = extract_text(obj[k])
                if t:
                    return t
        for v in obj.values():
            t = extract_text(v)
            if t:
                return t
    return None

def _normalize_messages_for_deployment(messages):
    """
    Convert a messages list (may include a 'system' role) into a deployment-friendly messages array
    where 'system' instructions are merged into the first 'user' message.
    """
    msgs = [dict(m) for m in messages]
    system_parts = []
    other_msgs = []
    for m in msgs:
        role = m.get("role", "").lower()
        content = m.get("content", "")
        # Normalize content
        if isinstance(content, list):
            try:
                content = " ".join(p.get("text", str(p)) if isinstance(p, dict) else str(p) for p in content)
            except Exception:
                content = str(content)
        elif isinstance(content, dict):
            content = json.dumps(content)
        if role == "system":
            system_parts.append(content)
        else:
            other_msgs.append({"role": role, "content": content})
    if system_parts:
        system_text = "\n".join(system_parts).strip()
        for i, m in enumerate(other_msgs):
            if m.get("role") == "user":
                merged = f"[SYSTEM INSTRUCTION]\n{system_text}\n\n[USER]\n{m.get('content','')}"
                other_msgs[i]["content"] = merged
                break
        else:
            other_msgs.insert(0, {"role": "user", "content": f"[SYSTEM INSTRUCTION]\n{system_text}\n\n"})
    return other_msgs

def infer_with_system_messages(messages, timeout=60):
    """
    Call the Watsonx deployment text/chat endpoint. Messages may include a 'system' role;
    we inline them for deployments.
    """
    if not IBM_APIKEY:
        return {"ok": False, "status": 0, "text": "Missing IBM_APIKEY in environment."}
    if not ML_BASE:
        return {"ok": False, "status": 0, "text": "Missing WATSONX_RUNTIME_URL or IBM_ML_URL/IBM_URL in environment."}
    if not DEPLOYMENT_ID:
        return {"ok": False, "status": 0, "text": "Missing WATSONX_DEPLOYMENT_ID in environment."}
    payload_messages = _normalize_messages_for_deployment(messages)
    try:
        token = get_iam_token_cached()
    except Exception as e:
        return {"ok": False, "status": 0, "text": f"IAM token error: {e}"}
    endpoint = f"{ML_BASE}/ml/v1/deployments/{DEPLOYMENT_ID}/text/chat?version={API_VERSION}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", "Accept": "application/json"}
    payload = {"messages": payload_messages}
    try:
        r = requests.post(endpoint, headers=headers, json=payload, timeout=timeout)
    except Exception as e:
        return {"ok": False, "status": 0, "text": f"Request failed: {e}", "endpoint": endpoint}
    if not r.ok:
        return {"ok": False, "status": r.status_code, "text": r.text, "endpoint": endpoint}
    try:
        j = r.json()
    except Exception:
        return {"ok": False, "status": r.status_code, "text": r.text, "endpoint": endpoint}
    return {"ok": True, "json": j, "endpoint": endpoint}

# --- Streamlit UI ---
st.set_page_config(
    page_title="Keerthana GenAI Portfolio",
    layout="wide",
    initial_sidebar_state="collapsed",
)
# Hide sidebar / override its flash
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], .main, .stApp { background: #050A14 !important; }
[data-testid="stSidebar"], [data-testid="stSidebarContent"], section[data-testid="stSidebar"], div[data-testid="stSidebar"] { background: #050A14 !important; }
[data-testid="stSidebar"], [data-testid="stSidebarNav"], [data-testid="stSideNav"], section[data-testid="stSidebar"] { display: none !important; }
.css-1d391kg, .css-1lcbmhc, [data-testid="stSidebar"] + div { margin-left: 0 !important; }
</style>
""", unsafe_allow_html=True)

local_css("styles/styles_main.css")

# ---------- REPLACE floating-profile block with this (copy-paste) ----------
from pathlib import Path
import base64

IMAGE_PATH = Path("images/profile3.png")
if IMAGE_PATH.exists():
    img_b64 = base64.b64encode(IMAGE_PATH.read_bytes()).decode("ascii")
    IMG_URI = "data:image/png;base64," + img_b64
else:
    IMG_URI = ""

LINKEDIN_URL = "https://www.linkedin.com/in/keerthana"
GITHUB_URL = "https://github.com/keerthi-learning"
EMAIL_ADDR = "skeerthi.datascience@gmail.com"

html_fp = """
<style>
/* Minimal fixed circular profile + icons underneath (no outer card) */
.fp {
  position: absolute;
  top: 0px;
  right: 48px;
  z-index: 9999;
  text-align: center;
  pointer-events: auto;
  transform: translateZ(0);
}

.fp .photo {
  width: 290px;
  height: 300px;
  border-radius: 50%;
  object-fit: cover;
  display: block;
  margin: 0 auto 8px auto;
  border: 4px solid rgba(255,255,255,0.06);
  background: transparent;
}

.fp .socials {
  display: flex;
  gap: 12px;
  justify-content: center;
  align-items: center;
  margin-top: 6px;
}

.fp .socials a img {
  width: 28px;
  height: 28px;
  transition: transform .12s ease, opacity .12s ease;
  opacity: 0.95;
  filter: drop-shadow(0 2px 6px rgba(2,6,23,0.35));
}

.fp .socials a img:hover {
  transform: translateY(-4px);
  opacity: 1;
}

/* keep it hidden on small screens so layout stays clean */
@media (max-width: 900px) {
  .fp { display: none; }
}
</style>

<div class="fp" aria-hidden="false">
  <img class="photo" src="{IMG_URI}" alt="Keerthana">
  <div class="socials">
    <a href="{LINKEDIN_URL}" target="_blank" rel="noopener"><img src="https://cdn-icons-png.flaticon.com/512/3536/3536505.png" alt="LinkedIn"></a>
    <a href="mailto:{EMAIL_ADDR}"><img src="https://cdn-icons-png.flaticon.com/512/732/732200.png" alt="Email"></a>
  </div>
</div>
"""

html_fp = html_fp.replace("{IMG_URI}", IMG_URI).replace("{LINKEDIN_URL}", LINKEDIN_URL).replace("{GITHUB_URL}", GITHUB_URL).replace("{EMAIL_ADDR}", EMAIL_ADDR)

st.markdown(html_fp, unsafe_allow_html=True)
# ---------------------------------------------------------------------------

st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
col_back, _ = st.columns([1, 5])
with col_back:
    st.page_link("landing.py", label="Portfolio", icon="↩️")

# Optional Landing (robust import and sidebar debug)
render_landing = None
try:
    try:
        Landing = importlib.import_module("Landing")
    except Exception:
        Landing = importlib.import_module("landing")
    render_landing = getattr(Landing, "render_landing", None) or getattr(Landing, "render_Landing", None)
except Exception as e:
    render_landing = None
    st.error("Failed to import Landing.py; see console for traceback.")
    print("Landing import error:", e)

# Basic env checks with user-visible messages
if not IBM_APIKEY:
    st.error("Missing IBM_APIKEY in .env. Please add your API key.")
    st.stop()
if not ML_BASE:
    st.error("Missing WATSONX_RUNTIME_URL or IBM_ML_URL/IBM_URL in .env.")
    st.stop()
if not DEPLOYMENT_ID:
    st.error("Missing WATSONX_DEPLOYMENT_ID in .env.")
    st.stop()

# Ensure session state keys exist BEFORE widgets
if "prompt_text" not in st.session_state:
    st.session_state["prompt_text"] = ""
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "## Introduction \n Hello! I’m Keerthana’s AI portfolio assistant. Ask me anything about her skills, projects, or experience."
        }
    ]
if "last_endpoint" not in st.session_state:
    st.session_state["last_endpoint"] = ""

# Title and conversation display
st.title("Keerthana GenAI Portfolio")
st.markdown("#### Conversation")

# Display messages (limit to last 50 to avoid huge pages)
for msg in st.session_state["messages"][-50:]:
    if msg.get("role") == "user":
        st.markdown(f"**You:** {msg.get('content')}")
    elif msg.get("role") == "assistant":
        st.markdown(f"**Assistant:**\n{msg.get('content')}", unsafe_allow_html=False)

st.write("---")

# Input area: single widget (textarea) using key "prompt_text"
col1, col2 = st.columns([4, 1])
with col1:
    user_input = st.text_area("Enter your prompt", height=120, key="prompt_text")

# helper to safely append messages and trim history
def append_message(role: str, content: str):
    st.session_state["messages"].append({"role": role, "content": content})
    if len(st.session_state["messages"]) > 200:
        st.session_state["messages"] = st.session_state["messages"][-200:]

# Build a short PROFILE context to include in system message
def build_profile_context_from_PROFILE(max_chars=2000):
    parts = []

    # --- Basic profile ---
    parts.append(f"Name: {PROFILE.get('name','Keerthana')}")
    if PROFILE.get("headline"):
        parts.append(f"Headline: {PROFILE.get('headline')}")
    if PROFILE.get("summary"):
        parts.append("Summary:")
        parts.append(PROFILE.get("summary"))

    # --- Resume bullets ---
    if PROFILE.get("resume_bullets"):
        parts.append("Key Highlights:")
        for b in PROFILE.get("resume_bullets", [])[:8]:
            parts.append(f"- {b}")

    # --- Projects ---
    if PROFILE.get("projects"):
        parts.append("Projects:")
        for _, p in list(PROFILE.get("projects", {}).items())[:6]:
            title = p.get("title", "Untitled")
            summary = p.get("summary", "")
            parts.append(f"* {title}: {summary}")

    # --- Certificates (NEW) ---
    cert_text = certificates_as_text()
    if cert_text:
        parts.append("Certifications:")
        parts.append(cert_text)

    # --- Internship Experience (NEW) ---
    parts.append("Internship Experience:")
    parts.append(
        "- Zidio Development (Aug 2025 – Oct 2025): "
        "Data Science & Machine Learning Internship involving real-world datasets, "
        "data preprocessing, and ML pipelines."
    )
    parts.append(
        "- Besant Technologies, Chennai: "
        "Data Science & AI Internship with hands-on work in Python, SQL, ML models, "
        "and analytics dashboards."
    )

       
    
        # --- Most Recent Work ---
    parts.append(
        "LATEST_PROJECT (MOST RECENT, PRIORITIZE THIS): "
        "Watsonx-powered GenAI Portfolio App with RAG-based AI assistant, "
        "Streamlit UI, and deployment-ready architecture."
    )

    # --- Contact Information (AUTHORITATIVE SOURCE) ---
    parts.append("CONTACT_INFORMATION (AUTHORITATIVE – USE THIS EXACTLY IF ASKED):")
    parts.append("Email: skeerthi.datascience@gmail.com")
    parts.append("LinkedIn: https://www.linkedin.com/in/keerthana-datascience/")
    
    
    core_text = "\n".join(parts)

    contact_block = (
    "\nCONTACT_INFORMATION (AUTHORITATIVE – USE THIS EXACTLY IF ASKED):\n"
    "Email: skeerthi.datascience@gmail.com\n"
    "LinkedIn: https://www.linkedin.com/in/keerthana-datascience/\n"
     )
# Truncate ONLY the core context, never the contact block
    core_text = core_text[: max_chars - len(contact_block) - 50]

    return core_text + contact_block


# send callback runs on button click
def send_callback():
    prompt = st.session_state.get("prompt_text", "").strip()
    if not prompt:
        return

    # Add user message to history
    append_message("user", prompt)

    # Build system instruction including BIO (if available) and PROFILE context
    profile_ctx = build_profile_context_from_PROFILE()
    bio_snippet = PROFILE.get("summary", "") or ""

    system_instruction = (
    "You are Keerthana's personal AI portfolio assistant.\n\n"

    "IMPORTANT – Greeting behavior:\n"
    "- If the user greets you (e.g., hi, hello, hey, good morning),\n"
    "  respond with a friendly greeting and briefly explain what you can help with.\n"
    "- Do NOT provide a professional summary or bullet points for greetings.\n"
    "- Invite the user to ask a question.\n\n"

    "Your role:\n"
    "- Answer recruiter and interviewer questions about Keerthana.\n"
    "- Use ONLY the information provided in BIO and PROFILE_CONTEXT.\n"
    "- Do NOT invent skills, projects, gaps, salary numbers, or dates.\n"
    "- If a question is outside her profile, respond:\n"
    "  'I can answer only about Keerthana’s skills, projects, and experience.'\n\n"

    "Recruiter questions handling:\n"
    "- The user may ask MULTIPLE questions in one message.\n"
    "- Answer each question clearly with labeled sections.\n"
    "- Be confident and precise; avoid uncertain phrasing such as 'not explicitly stated'.\n\n"

    "IMPORTANT – Strengths & weaknesses questions:\n"
    "- Clearly state strengths.\n"
    "- For weaknesses, NEVER guess gaps.\n"
    "- Frame weaknesses as areas of ongoing learning or growth.\n"
    "- Do NOT imply missing skills or lack of ability.\n\n"

    "IMPORTANT – Strengths & weaknesses questions:\n"
    "- Clearly state strengths with examples.\n"
    "- For weaknesses:\n"
         "* Do NOT mention specific missing skills or gaps.\n"
         "* Frame as continuous learning and growth mindset only.\n"
         "* Keep it general and positive.\n"

    "IMPORTANT – Availability questions:\n"
    "- If the user asks about start date or availability (e.g., 'When can she start work?'),\n"
    "  respond with availability FIRST.\n"
    "- Keep the answer short (1–2 lines).\n"
    "- Do NOT include skills, projects, or background in this section.\n\n"

    "For salary-related questions:\n"
    "- Never mention numbers.\n"
    "- Respond diplomatically.\n"
    "- Emphasize learning, growth, and market-aligned compensation.\n\n"

    "For contact information:\n"
    "- If the user asks for contact details, you MUST respond using CONTACT_INFORMATION verbatim.\n"
    "- Present each contact item on a separate line.\n\n"

    "Answering style for NON-GREETING questions:\n"
    "- Start with a 1-line professional summary.\n"
    "- Then answer each question in clearly labeled sections.\n"
    "- Use concise bullet points where appropriate.\n"
    "- Focus on impact, technologies, and outcomes.\n"
    "- Keep responses recruiter-friendly and easy to scan.\n\n"

    f"BIO:\n{bio_snippet}\n\n"
    f"PROFILE_CONTEXT:\n{profile_ctx}\n"
)



    messages_for_call = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": prompt},
    ]

    with st.spinner("Thinking..."):
        result = infer_with_system_messages(messages_for_call)

    if not result.get("ok"):
        err_text = result.get("text")
        status = result.get("status")
        append_message("assistant", f"Runtime error: {status} — {err_text}")
        st.session_state["last_endpoint"] = result.get("endpoint") or ""
        return

    j = result.get("json")
    reply = extract_text(j)
    if not reply:
        try:
            reply = j.get("choices", [])[0].get("message", {}).get("content")
        except Exception:
            reply = None

    if not reply:
        pretty = json.dumps(j, indent=2)
        append_message("assistant", pretty[:3000])
    else:
        append_message("assistant", reply)



    # clear prompt (UI textarea bound to key will be updated)
    st.session_state["prompt_text"] = ""

with col2:
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.button("Send", use_container_width=True, on_click=send_callback)

st.write("---")

#clear and quetions
col_clear, col_faq = st.columns([1, 2])

with col_clear:
    if st.button("🧹 Clear conversation", use_container_width=True):
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": "## Introduction\nHello, I'm here to help — ask me anything about the demo.",
            }
        ]
        rerun = getattr(st, "rerun", None) or getattr(st, "experimental_rerun", None)
        if callable(rerun):
            rerun()

with col_faq:
    with st.expander("💡FAQ"):
        for q in FAQ:
            st.markdown(f"- {q}")

# ---- spacing before footer ----
st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
st.markdown(
        "<div style='text-align:center;color:#cbd5f5;font-size:0.85rem'>Built with Streamlit · Designed & engineered by Keerthana S</div>",
        unsafe_allow_html=True,
    )
