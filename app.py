import streamlit as st

st.set_page_config(
    page_title="Sentiment Analyst",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# SESSION STATE
# =====================================

if "menu" not in st.session_state:
    st.session_state.menu = "Overview"


def go_to_analysis():
    st.session_state.menu = "New Analysis"


# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --accent: #7665f5;
    --accent-hover: #6553e8;
    --accent-soft: rgba(118, 101, 245, 0.12);
}

.stApp {
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3, h4 {
    font-family: 'Space Grotesk', sans-serif !important;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    border-right: 1px solid var(--border-color);
}

.brand {
    padding: 12px 0 22px 0;
}

.brand-icon {
    color: var(--accent);
    font-size: 32px;
    font-weight: bold;
}

.brand-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 19px;
    font-weight: 700;
}

.brand-subtitle {
    font-size: 10px;
    letter-spacing: 2px;
    opacity: 0.65;
}

.eyebrow {
    color: var(--accent);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
}

.page-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 34px;
    font-weight: 700;
    margin-top: 6px;
}

.page-description {
    font-size: 14px;
    opacity: 0.7;
    margin-top: 5px;
}

.hero {
    background: var(--secondary-background-color);
    border: 1px solid var(--border-color);
    border-radius: 20px;
    padding: 30px;
    min-height: 250px;
}

.hero-badge {
    display: inline-block;
    padding: 6px 11px;
    border-radius: 30px;
    background: var(--accent-soft);
    color: var(--accent);
    font-size: 11px;
    font-weight: 700;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 31px;
    font-weight: 700;
    line-height: 1.2;
    margin-top: 17px;
}

.hero-description {
    font-size: 14px;
    opacity: 0.7;
    line-height: 1.7;
    margin-top: 12px;
}

.flow-panel {
    background: var(--secondary-background-color);
    border: 1px solid var(--border-color);
    border-radius: 20px;
    padding: 25px;
    min-height: 250px;
}

.flow-step {
    margin-top: 17px;
    font-size: 14px;
    font-weight: 600;
}

.flow-number {
    color: var(--accent);
    margin-right: 9px;
}

.stat-card {
    background: var(--secondary-background-color);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 20px;
    min-height: 120px;
}

.stat-label {
    font-size: 12px;
    opacity: 0.7;
}

.stat-number {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 29px;
    font-weight: 700;
    margin-top: 10px;
}

.stat-description {
    font-size: 11px;
    opacity: 0.6;
    margin-top: 4px;
}

.panel {
    background: var(--secondary-background-color);
    border: 1px solid var(--border-color);
    border-radius: 17px;
    padding: 22px;
}

.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    transition: 0.2s;
}

.stButton > button[kind="primary"] {
    background: var(--accent);
    border-color: var(--accent);
    color: white !important;
}

.stButton > button[kind="primary"]:hover {
    background: var(--accent-hover);
    border-color: var(--accent-hover);
}

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stTextArea"] textarea {
    border-radius: 10px;
}

div[data-testid="stDataFrame"] {
    border-radius: 12px;
}

hr {
    opacity: 0.25;
}
</style>
""", unsafe_allow_html=True)


# =====================================
# SIDEBAR NAVIGATION
# =====================================

with st.sidebar:

    st.markdown("""
    <div class="brand">
        <div class="brand-icon">◈</div>
        <div class="brand-title">Sentiment Analyst</div>
        <div class="brand-subtitle">SOCIAL INTELLIGENCE</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    menu = st.radio(
        "WORKSPACE",
        [
            "Overview",
            "New Analysis",
            "Sentiment Explorer",
            "History",
            "Settings"
        ],
        key="menu"
    )

    st.divider()

    st.caption("CONNECTED PLATFORM")

    st.markdown("""
    <div style="font-size:13px;">
        <span style="color:#16a34a;">●</span>
        YouTube
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.caption("SENTIMENT ANALYST · VERSION 1.0")


# =====================================
# OVERVIEW
# =====================================

if menu == "Overview":

    st.markdown("""
    <div class="eyebrow">WORKSPACE / OVERVIEW</div>
    <div class="page-title">Your intelligence hub.</div>
    <div class="page-description">
        Discover what people think, feel, and say.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    hero_col, flow_col = st.columns([1.5, 1])

    with hero_col:

        st.markdown("""
        <div class="hero">
            <div class="hero-badge">AI POWERED · SOCIAL LISTENING</div>
            <div class="hero-title">
                Turn conversations<br>into insights.
            </div>
            <div class="hero-description">
                Collect public comments, understand audience opinions,
                and transform raw conversations into meaningful data.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with flow_col:

        st.markdown("""
        <div class="flow-panel">
            <div class="eyebrow">HOW IT WORKS</div>

            <div class="flow-step">
                <span class="flow-number">01</span> Collect data
            </div>
            <div style="font-size:12px;opacity:.65;margin-left:29px;">
                Gather social media comments
            </div>

            <div class="flow-step">
                <span class="flow-number">02</span> Process text
            </div>
            <div style="font-size:12px;opacity:.65;margin-left:29px;">
                Clean and prepare comments
            </div>

            <div class="flow-step">
                <span class="flow-number">03</span> Analyze sentiment
            </div>
            <div style="font-size:12px;opacity:.65;margin-left:29px;">
                Discover public opinions
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # MAIN ACTION

    st.markdown("### Start Your Analysis")

    st.markdown("""
    <div class="panel">
        <div style="font-size:19px;font-weight:700;">
            Ready to explore public opinion?
        </div>
        <div style="font-size:13px;opacity:.7;margin-top:8px;">
            Create a project, collect YouTube comments, and analyze
            audience sentiment in one workspace.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "＋  Create New Analysis",
        type="primary",
        use_container_width=True
    ):
        go_to_analysis()
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # EMPTY STATE

    st.markdown("### Your Workspace")

    st.caption("Your analysis activity will appear here.")

    st.markdown("""
    <div class="panel" style="text-align:center;padding:35px 20px;">
        <div style="font-size:34px;color:#7665f5;">◈</div>
        <div style="font-size:18px;font-weight:700;margin-top:12px;">
            No analysis yet
        </div>
        <div style="font-size:13px;opacity:.65;margin-top:7px;">
            Start your first project to see your collected data,
            analysis results, and insights here.
        </div>
    </div>
    """, unsafe_allow_html=True)


# =====================================
# NEW ANALYSIS
# =====================================

elif menu == "New Analysis":

    st.markdown("""
    <div class="eyebrow">WORKSPACE / PROJECT</div>
    <div class="page-title">New Analysis</div>
    <div class="page-description">
        Configure a new social media data collection project.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):

        st.markdown("### Project Configuration")

        project_name = st.text_input(
            "Project Name",
            placeholder="Example: Public opinion about fuel prices"
        )

        platform = st.selectbox(
            "Select Platform",
            ["YouTube"]
        )

        url = st.text_input(
            "Content URL",
            placeholder="Paste YouTube video URL here..."
        )

        max_comments = st.select_slider(
            "Maximum Comments",
            options=[100, 250, 500, 1000, 2500, 5000, 10000],
            value=500
        )

        st.divider()

        if st.button("Start Collection →", type="primary"):

            if not project_name.strip():
                st.warning("Enter a project name first.")

            elif not url.strip():
                st.warning("Enter a content URL first.")

            else:
                st.info("Scraping engine is not connected yet.")


# =====================================
# SENTIMENT EXPLORER
# =====================================

elif menu == "Sentiment Explorer":

    st.markdown("""
    <div class="eyebrow">WORKSPACE / NLP</div>
    <div class="page-title">Sentiment Explorer</div>
    <div class="page-description">
        Explore classified audience opinions.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="panel" style="text-align:center;padding:35px 20px;">
        <div style="font-size:34px;color:#7665f5;">◈</div>
        <div style="font-size:18px;font-weight:700;margin-top:12px;">
            No sentiment data available
        </div>
        <div style="font-size:13px;opacity:.65;margin-top:7px;">
            Complete a data collection and sentiment analysis
            project to explore visualizations and classified comments.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.info("Sentiment classification engine has not been connected yet.")


# =====================================
# HISTORY
# =====================================

elif menu == "History":

    st.markdown("""
    <div class="eyebrow">WORKSPACE / ARCHIVE</div>
    <div class="page-title">Analysis History</div>
    <div class="page-description">
        Review your previous analysis projects.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="panel">
        <div style="font-size:30px;color:#7665f5;">◷</div>
        <div style="font-size:18px;font-weight:700;margin-top:10px;">
            No saved analyses
        </div>
        <div style="font-size:13px;opacity:.7;margin-top:6px;">
            Your completed projects will appear here.
        </div>
    </div>
    """, unsafe_allow_html=True)


# =====================================
# SETTINGS
# =====================================

elif menu == "Settings":

    st.markdown("""
    <div class="eyebrow">WORKSPACE / PREFERENCES</div>
    <div class="page-title">Settings</div>
    <div class="page-description">
        Configure your analysis preferences.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):

        st.markdown("### General Preferences")

        language = st.selectbox(
            "Analysis Language",
            ["Indonesian", "English"]
        )

        method = st.selectbox(
            "Analysis Method",
            ["Machine Learning", "Lexicon Based"]
        )

        platform = st.selectbox(
            "Default Platform",
            ["YouTube"]
        )

        st.button("Save Preferences", type="primary")

        st.caption("Preferences are not saved permanently yet.")