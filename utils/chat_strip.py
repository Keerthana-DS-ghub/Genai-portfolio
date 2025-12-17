import streamlit as st

ICON_LINKEDIN = "https://cdn-icons-png.flaticon.com/512/3536/3536505.png"
ICON_GITHUB   = "https://cdn-icons-png.flaticon.com/512/733/733553.png"
ICON_MAIL     = "https://cdn-icons-png.flaticon.com/512/732/732200.png"


def render_chat_strip(info, socials):
    linkedin = socials.get("LinkedIn", "").strip()
    github   = socials.get("GitHub", "").strip()
    email    = info.get("Email", "").strip() or socials.get("Email", "").strip()

    # ---------- CSS (ONLY ICONS + ALIGNMENT) ----------
    st.markdown(
        """
        <style>
        .hero-icon-pill {
            width: 42px;
            height: 42px;
            border-radius: 999px;
            background: rgba(15,23,42,0.95);
            border: 1px solid rgba(148,163,184,0.55);
            display: flex;
            align-items: center;
            justify-content: center;
            transition: 0.18s ease;
        }

        .hero-icon-pill img {
            width: 20px;
            height: 20px;
        }

        .hero-icon-pill:hover {
            transform: translateY(-2px);
            border-color: #38bdf8;
            background: rgba(56,189,248,0.15);
        }

        .chat-ai-btn-wrapper {
            margin-top: -4px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---------- LAYOUT ----------
    col1, col2, col3, col4 = st.columns([0.04, 0.04, 0.04, 0.35])

    with col1:
        if linkedin:
            st.markdown(
                f'<a class="hero-icon-pill" href="{linkedin}" target="_blank">'
                f'<img src="{ICON_LINKEDIN}"></a>',
                unsafe_allow_html=True,
            )

    with col2:
        if github:
            st.markdown(
                f'<a class="hero-icon-pill" href="{github}" target="_blank">'
                f'<img src="{ICON_GITHUB}"></a>',
                unsafe_allow_html=True,
            )

    with col3:
        if email:
            st.markdown(
                f'<a class="hero-icon-pill" href="mailto:{email}">'
                f'<img src="{ICON_MAIL}"></a>',
                unsafe_allow_html=True,
            )

    with col4:
        st.markdown('<div class="chat-ai-btn-wrapper">', unsafe_allow_html=True)
        clicked = st.button("Chat with my AI", key="chat_with_ai")
        st.markdown('</div>', unsafe_allow_html=True)

    if clicked:
        st.markdown(
            "<meta http-equiv='refresh' content='0; url=Chat_with_AI' />",
            unsafe_allow_html=True,
        )
