import streamlit as st


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

        :root {
            --bg: #f5f7fb;
            --panel: rgba(255, 255, 255, 0.88);
            --panel-border: rgba(18, 38, 63, 0.08);
            --text: #10233d;
            --muted: #6a7a90;
            --primary: #0f766e;
            --accent: #f97316;
            --positive: #15803d;
            --shadow: 0 18px 50px rgba(15, 23, 42, 0.08);
        }

        .stApp {
            background:
                radial-gradient(circle at top right, rgba(249, 115, 22, 0.18), transparent 25%),
                radial-gradient(circle at top left, rgba(15, 118, 110, 0.18), transparent 22%),
                linear-gradient(180deg, #f9fbff 0%, #eef4fb 100%);
            color: var(--text);
            font-family: 'IBM Plex Sans', sans-serif;
        }

        h1, h2, h3 {
            font-family: 'Space Grotesk', sans-serif;
            color: var(--text);
            letter-spacing: -0.03em;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #132238 100%);
            border-right: 1px solid rgba(255,255,255,0.06);
        }

        [data-testid="stSidebar"] * {
            color: #eff6ff !important;
        }

        .optiq-hero {
            padding: 1.4rem 1.6rem;
            border: 1px solid rgba(255,255,255,0.06);
            background: linear-gradient(135deg, rgba(15,118,110,0.95), rgba(15,23,42,0.94));
            box-shadow: var(--shadow);
            border-radius: 22px;
            color: white;
            margin-bottom: 1rem;
        }

        .optiq-card {
            background: var(--panel);
            border: 1px solid var(--panel-border);
            border-radius: 20px;
            padding: 1.1rem 1.2rem;
            box-shadow: var(--shadow);
            backdrop-filter: blur(14px);
        }

        .optiq-card .label {
            color: var(--muted);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .optiq-card .value {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.9rem;
            font-weight: 700;
            margin-top: 0.3rem;
            color: var(--text);
        }

        .optiq-card .delta {
            margin-top: 0.35rem;
            color: var(--primary);
            font-size: 0.92rem;
        }

        .optiq-section {
            margin: 0.25rem 0 1rem;
            color: var(--muted);
            font-size: 1rem;
        }

        .stTextArea textarea, .stTextInput input {
            border-radius: 16px !important;
            border: 1px solid rgba(15, 23, 42, 0.12) !important;
        }

        .stButton button {
            border-radius: 999px;
            background: linear-gradient(135deg, var(--primary), #0891b2);
            color: white;
            border: none;
            font-weight: 600;
            padding: 0.55rem 1.2rem;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="optiq-hero">
            <h1 style="margin:0;">{title}</h1>
            <p style="margin:0.5rem 0 0; font-size:1rem; color:rgba(255,255,255,0.85);">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
