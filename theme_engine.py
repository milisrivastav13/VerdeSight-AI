import streamlit as st


# ============================================================
# VERDESIGHT AI THEMES
# ============================================================

THEMES = {

    "Neon Green": {
        "primary": "#00E676",
        "secondary": "#00C853",
        "background": "#07110B",
        "text": "#E8F5E9",
    },

    "Cyber Cyan": {
        "primary": "#00E5FF",
        "secondary": "#00B8D4",
        "background": "#071116",
        "text": "#E0F7FA",
    },

    "Violet Pulse": {
        "primary": "#B388FF",
        "secondary": "#7C4DFF",
        "background": "#0E0918",
        "text": "#F3E5F5",
    },

    "Sunset Magenta": {
        "primary": "#FF4081",
        "secondary": "#F50057",
        "background": "#180810",
        "text": "#FCE4EC",
    },

    "Arctic Blue": {
        "primary": "#40C4FF",
        "secondary": "#0091EA",
        "background": "#061018",
        "text": "#E1F5FE",
    },

    "Emerald Gold": {
        "primary": "#69F0AE",
        "secondary": "#FFD740",
        "background": "#0A120D",
        "text": "#F1F8E9",
    },
}


# ============================================================
# APPLY THEME
# ============================================================

def apply_theme(theme_name):

    if theme_name not in THEMES:

        theme_name = "Neon Green"

    theme = THEMES[theme_name]

    # --------------------------------------------------------
    # Native Streamlit configuration
    # --------------------------------------------------------

    st.session_state["active_theme"] = theme_name

    # --------------------------------------------------------
    # Small native accent indicators
    # --------------------------------------------------------

    st.sidebar.caption(
        f"Theme: {theme_name}"
    )