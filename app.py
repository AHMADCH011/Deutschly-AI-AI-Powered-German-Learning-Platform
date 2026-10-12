import streamlit as st

from groq_service import translate_with_ai, ask_tutor
from quiz_data import CHAPTERS, get_quiz
from database import init_db, get_progress, save_quiz_result


# ─────────────────────────────────────────
# Page configuration
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Deutschly AI",
    page_icon="🇩🇪",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()


# ─────────────────────────────────────────
# Global CSS — professional dark-accented theme
# ─────────────────────────────────────────
st.markdown(
    """
<style>
/* ── Google font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Root reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 1.5rem 2.5rem 3rem 2.5rem;
    max-width: 1200px;
}

/* ══════════════════════════════════════════
   SIDEBAR
══════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    border-right: 1px solid rgba(255,255,255,0.07);
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 18px 0 8px 0;
    margin-bottom: 4px;
}
.sidebar-brand-flag { font-size: 32px; }
.sidebar-brand-text {
    font-size: 20px;
    font-weight: 800;
    background: linear-gradient(90deg, #e2e8f0, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.sidebar-caption {
    font-size: 11px;
    color: #94a3b8 !important;
    letter-spacing: 0.04em;
    margin-bottom: 20px;
}

/* Nav buttons inside sidebar */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #cbd5e1 !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    font-size: 13.5px !important;
    padding: 10px 14px !important;
    text-align: left !important;
    transition: all 0.2s ease !important;
    margin-bottom: 4px !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(167,139,250,0.15) !important;
    border-color: rgba(167,139,250,0.4) !important;
    color: #f1f5f9 !important;
    transform: translateX(3px) !important;
}

.sidebar-goal-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 14px 16px;
    margin: 12px 0;
}
.sidebar-goal-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #a78bfa !important;
    margin-bottom: 6px;
}
.sidebar-goal-text { font-size: 13px; }
.sidebar-version {
    font-size: 10px;
    color: #475569 !important;
    text-align: center;
    margin-top: 8px;
}

/* ══════════════════════════════════════════
   HERO SECTION
══════════════════════════════════════════ */
.hero {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #4c1d95 100%);
    border-radius: 20px;
    padding: 44px 48px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(167,139,250,0.25) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: -40px;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(99,102,241,0.2) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-size: 46px;
    font-weight: 800;
    color: #fff;
    line-height: 1.1;
    margin-bottom: 10px;
}
.hero-subtitle {
    font-size: 17px;
    color: #c4b5fd;
    max-width: 520px;
    line-height: 1.6;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    color: #e9d5ff;
    font-size: 11px;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 14px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* ══════════════════════════════════════════
   METRIC / STAT CARDS
══════════════════════════════════════════ */
.stat-card {
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 24px 22px;
    position: relative;
    overflow: hidden;
    transition: box-shadow 0.2s, transform 0.2s;
}
.stat-card:hover {
    box-shadow: 0 8px 30px rgba(99,102,241,0.12);
    transform: translateY(-2px);
}
.stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
}
.stat-card.purple::before { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }
.stat-card.blue::before   { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
.stat-card.green::before  { background: linear-gradient(90deg, #10b981, #34d399); }
.stat-card.gold::before   { background: linear-gradient(90deg, #f59e0b, #fbbf24); }

.stat-icon {
    font-size: 28px;
    margin-bottom: 8px;
    display: block;
}
.stat-label {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: #94a3b8;
    margin-bottom: 4px;
}
.stat-value {
    font-size: 32px;
    font-weight: 800;
    color: #1e293b;
    line-height: 1;
}
.stat-sub {
    font-size: 12px;
    color: #94a3b8;
    margin-top: 4px;
}

/* ══════════════════════════════════════════
   PROGRESS BAR
══════════════════════════════════════════ */
.progress-wrap {
    background: #f1f5f9;
    border-radius: 999px;
    height: 8px;
    overflow: hidden;
    margin: 8px 0 4px;
}
.progress-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #8b5cf6, #3b82f6);
    transition: width 0.6s ease;
}

/* ══════════════════════════════════════════
   CHAPTER / FEATURE CARDS
══════════════════════════════════════════ */
.chapter-card {
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 22px 26px;
    margin-bottom: 12px;
    transition: box-shadow 0.2s, border-color 0.2s;
}
.chapter-card:hover {
    box-shadow: 0 4px 20px rgba(99,102,241,0.1);
    border-color: #c4b5fd;
}
.chapter-card.completed { border-left: 4px solid #10b981; }
.chapter-card.unlocked  { border-left: 4px solid #8b5cf6; }
.chapter-card.locked    { border-left: 4px solid #e2e8f0; opacity: 0.65; }

.chapter-badge {
    display: inline-block;
    font-size: 10px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 20px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.badge-completed { background: #d1fae5; color: #065f46; }
.badge-unlocked  { background: #ede9fe; color: #5b21b6; }
.badge-locked    { background: #f1f5f9; color: #94a3b8; }

.chapter-title {
    font-size: 17px;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 4px;
}
.chapter-desc { font-size: 13.5px; color: #64748b; line-height: 1.5; }
.chapter-level {
    font-size: 11px;
    font-weight: 600;
    color: #a78bfa;
    margin-top: 8px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ══════════════════════════════════════════
   NEXT CHAPTER HERO CARD
══════════════════════════════════════════ */
.next-card {
    background: linear-gradient(135deg, #f5f3ff, #ede9fe);
    border: 1.5px solid #c4b5fd;
    border-radius: 18px;
    padding: 28px 32px;
    margin-bottom: 24px;
}
.next-card-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #7c3aed;
    margin-bottom: 8px;
}
.next-card-title {
    font-size: 24px;
    font-weight: 800;
    color: #1e1b4b;
    margin-bottom: 6px;
}
.next-card-desc { font-size: 14px; color: #5b21b6; line-height: 1.6; }

/* ══════════════════════════════════════════
   FEATURE HIGHLIGHTS
══════════════════════════════════════════ */
.feature-card {
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 28px 24px;
    text-align: center;
    transition: box-shadow 0.2s, transform 0.2s;
}
.feature-card:hover {
    box-shadow: 0 8px 24px rgba(99,102,241,0.1);
    transform: translateY(-3px);
}
.feature-icon { font-size: 36px; margin-bottom: 12px; display: block; }
.feature-title { font-size: 15px; font-weight: 700; color: #1e293b; margin-bottom: 6px; }
.feature-text  { font-size: 13px; color: #64748b; line-height: 1.6; }

/* ══════════════════════════════════════════
   PAGE HEADER BAND
══════════════════════════════════════════ */
.page-header {
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 22px 28px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 16px;
}
.page-header-icon { font-size: 36px; }
.page-header-title {
    font-size: 26px;
    font-weight: 800;
    color: #1e293b;
    margin: 0;
}
.page-header-sub { font-size: 13px; color: #64748b; margin: 2px 0 0 0; }

/* ══════════════════════════════════════════
   TRANSLATOR RESULT
══════════════════════════════════════════ */
.result-german {
    background: linear-gradient(135deg, #1e1b4b, #312e81);
    color: #fff;
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 20px;
}
.result-german-word {
    font-size: 40px;
    font-weight: 800;
    letter-spacing: 0.02em;
}
.result-german-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #c4b5fd;
    margin-bottom: 8px;
}
.result-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 20px 24px;
    height: 100%;
}
.result-box-label {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: #94a3b8;
    margin-bottom: 8px;
}
.result-box-value { font-size: 15px; color: #1e293b; font-weight: 500; }

.word-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #ede9fe;
    border: 1px solid #c4b5fd;
    border-radius: 8px;
    padding: 6px 14px;
    margin: 4px;
    font-size: 13px;
    color: #4c1d95;
    font-weight: 500;
}
.word-chip b { color: #6d28d9; }

/* ══════════════════════════════════════════
   QUIZ
══════════════════════════════════════════ */
.quiz-question {
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 22px 26px;
    margin-bottom: 16px;
}
.quiz-question-num {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #8b5cf6;
    margin-bottom: 6px;
}
.quiz-question-text {
    font-size: 17px;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 14px;
}

.score-pass {
    background: linear-gradient(135deg, #d1fae5, #a7f3d0);
    border: 2px solid #10b981;
    border-radius: 18px;
    padding: 32px;
    text-align: center;
}
.score-fail {
    background: linear-gradient(135deg, #fee2e2, #fecaca);
    border: 2px solid #ef4444;
    border-radius: 18px;
    padding: 32px;
    text-align: center;
}
.score-number {
    font-size: 72px;
    font-weight: 900;
    line-height: 1;
    margin-bottom: 4px;
}
.score-pass .score-number  { color: #065f46; }
.score-fail .score-number  { color: #7f1d1d; }
.score-label  { font-size: 16px; font-weight: 600; }

/* ══════════════════════════════════════════
   TUTOR CHAT
══════════════════════════════════════════ */
.tutor-answer {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #8b5cf6;
    border-radius: 12px;
    padding: 20px 24px;
    margin-top: 16px;
}

/* ══════════════════════════════════════════
   SECTION HEADING
══════════════════════════════════════════ */
.section-heading {
    font-size: 19px;
    font-weight: 800;
    color: #1e293b;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ══════════════════════════════════════════
   BUTTONS OVERRIDE
══════════════════════════════════════════ */
.main .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    border: none !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    box-shadow: 0 4px 12px rgba(124,58,237,0.3) !important;
    transition: all 0.2s !important;
}
.main .stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px rgba(124,58,237,0.4) !important;
}
.main .stButton > button[kind="secondary"] {
    border-radius: 10px !important;
    font-weight: 500 !important;
}

/* ══════════════════════════════════════════
   INPUTS
══════════════════════════════════════════ */
.stTextArea textarea {
    border-radius: 12px !important;
    border: 1.5px solid #e2e8f0 !important;
    font-size: 14px !important;
    transition: border-color 0.2s !important;
}
.stTextArea textarea:focus {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.12) !important;
}

/* ══════════════════════════════════════════
   DIVIDER
══════════════════════════════════════════ */
hr { border-color: #f1f5f9 !important; margin: 24px 0 !important; }

/* ══════════════════════════════════════════
   CONTENT CARD (chapter content)
══════════════════════════════════════════ */
.content-card {
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 16px;
}
.vocab-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid #f1f5f9;
}
.vocab-row:last-child { border-bottom: none; }
.vocab-de { font-size: 18px; font-weight: 700; color: #1e293b; }
.vocab-en { font-size: 14px; color: #64748b; }
.vocab-ru { font-size: 12px; color: #94a3b8; font-style: italic; }
</style>
""",
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────
# Session state
# ─────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "selected_chapter" not in st.session_state:
    st.session_state.selected_chapter = None


def go_to(page):
    st.session_state.page = page
    st.rerun()


# ─────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <span class="sidebar-brand-flag">🇩🇪</span>
            <span class="sidebar-brand-text">Deutschly AI</span>
        </div>
        <div class="sidebar-caption">German learning for Pakistani students</div>
        """,
        unsafe_allow_html=True,
    )

    nav_items = [
        ("🏠", "Dashboard"),
        ("📚", "Learning Path"),
        ("🤖", "AI Translator"),
        ("👨‍🏫", "AI Tutor"),
    ]
    for icon, label in nav_items:
        if st.button(f"{icon}  {label}", use_container_width=True, key=f"nav_{label}"):
            go_to(label)

    st.markdown(
        """
        <div class="sidebar-goal-box">
            <div class="sidebar-goal-title">🎯 Your Goal</div>
            <div class="sidebar-goal-text">Learn German <b>A0 → B2</b></div>
            <div style="margin-top:4px; font-size:12px; color:#94a3b8;">🇵🇰 Pakistani student focused</div>
        </div>
        <div class="sidebar-version">Deutschly AI v1.0</div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────
# Progress data
# ─────────────────────────────────────────
progress = get_progress()

completed_chapters = sum(1 for item in progress if item["completed"] == 1)
total_xp = sum(item["xp"] for item in progress)
total_chapters = len(CHAPTERS)
progress_percentage = int((completed_chapters / total_chapters) * 100) if total_chapters else 0


# ════════════════════════════════════════════════════════════════
# DASHBOARD
# ════════════════════════════════════════════════════════════════
if st.session_state.page == "Dashboard":

    # Hero
    st.markdown(
        """
        <div class="hero">
            <div class="hero-badge">✨ AI-Powered German Learning</div>
            <div class="hero-title">🇩🇪 Deutschly AI</div>
            <div class="hero-subtitle">
                Learn German step-by-step — with explanations in English &amp; Roman Urdu,
                built specifically for Pakistani students.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Stat cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            """
            <div class="stat-card purple">
                <span class="stat-icon">🏆</span>
                <div class="stat-label">Current Level</div>
                <div class="stat-value">A0</div>
                <div class="stat-sub">Beginner</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div class="stat-card blue">
                <span class="stat-icon">📈</span>
                <div class="stat-label">Progress</div>
                <div class="stat-value">{progress_percentage}%</div>
                <div class="progress-wrap">
                    <div class="progress-fill" style="width:{progress_percentage}%"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""
            <div class="stat-card green">
                <span class="stat-icon">✅</span>
                <div class="stat-label">Chapters Done</div>
                <div class="stat-value">{completed_chapters}</div>
                <div class="stat-sub">out of {total_chapters}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f"""
            <div class="stat-card gold">
                <span class="stat-icon">⭐</span>
                <div class="stat-label">Total XP</div>
                <div class="stat-value">{total_xp:,}</div>
                <div class="stat-sub">Experience points</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='margin-top:28px'></div>", unsafe_allow_html=True)

    # Next chapter
    st.markdown('<div class="section-heading">🚀 Continue Learning</div>', unsafe_allow_html=True)

    next_chapter = None
    for chapter in CHAPTERS:
        cp = next((item for item in progress if item["chapter_id"] == chapter["id"]), None)
        if not cp or cp["completed"] == 0:
            next_chapter = chapter
            break

    if next_chapter:
        st.markdown(
            f"""
            <div class="next-card">
                <div class="next-card-label">📖 Up Next</div>
                <div class="next-card-title">Chapter {next_chapter['id']}: {next_chapter['title']}</div>
                <div class="next-card-desc">{next_chapter['description']}</div>
                <div style="margin-top:10px;font-size:12px;font-weight:600;color:#7c3aed;
                            text-transform:uppercase;letter-spacing:0.07em;">
                    Level: {next_chapter['level']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Start Learning →", type="primary"):
            st.session_state.selected_chapter = next_chapter["id"]
            go_to("Chapter")
    else:
        st.success("🎉 Congratulations! You completed all available chapters!")

    st.markdown("<div style='margin-top:32px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-heading">✨ Why Deutschly AI?</div>', unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)
    features = [
        ("🇵🇰", "Pakistani Friendly", "Learn German using English & Roman Urdu explanations, tailored for Pakistani students."),
        ("🤖", "AI Powered", "Translate any sentence and ask the AI tutor questions 24/7 — instantly."),
        ("🎯", "Practical Skills", "Learn German for university, travel, and everyday life in Pakistan & abroad."),
    ]
    for col, (icon, title, text) in zip([f1, f2, f3], features):
        with col:
            st.markdown(
                f"""
                <div class="feature-card">
                    <span class="feature-icon">{icon}</span>
                    <div class="feature-title">{title}</div>
                    <div class="feature-text">{text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ════════════════════════════════════════════════════════════════
# LEARNING PATH
# ════════════════════════════════════════════════════════════════
elif st.session_state.page == "Learning Path":

    st.markdown(
        """
        <div class="page-header">
            <div class="page-header-icon">📚</div>
            <div>
                <div class="page-header-title">German Learning Path</div>
                <div class="page-header-sub">Complete each chapter and pass the quiz with at least 70%.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Mini progress bar
    st.markdown(
        f"""
        <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:16px 20px;margin-bottom:20px;">
            <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                <span style="font-size:13px;font-weight:600;color:#1e293b;">Overall Progress</span>
                <span style="font-size:13px;font-weight:700;color:#8b5cf6;">{progress_percentage}%</span>
            </div>
            <div class="progress-wrap" style="height:10px;">
                <div class="progress-fill" style="width:{progress_percentage}%"></div>
            </div>
            <div style="font-size:12px;color:#94a3b8;margin-top:6px;">{completed_chapters} of {total_chapters} chapters completed</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for chapter in CHAPTERS:
        cp = next((item for item in progress if item["chapter_id"] == chapter["id"]), None)
        completed = cp and cp["completed"] == 1

        if chapter["id"] == 1:
            unlocked = True
        else:
            prev = next((item for item in progress if item["chapter_id"] == chapter["id"] - 1), None)
            unlocked = prev and prev["completed"] == 1

        if completed:
            card_class, badge_class, badge_text = "completed", "badge-completed", "✅ Completed"
        elif unlocked:
            card_class, badge_class, badge_text = "unlocked", "badge-unlocked", "🔓 Available"
        else:
            card_class, badge_class, badge_text = "locked", "badge-locked", "🔒 Locked"

        score_html = (
            f"<span style='color:#10b981;font-size:12px;font-weight:600;margin-top:6px;display:block;'>Best Score: {cp['score']}%</span>"
            if completed and cp else ""
        )

        st.markdown(
            f"""
            <div class="chapter-card {card_class}">
                <span class="chapter-badge {badge_class}">{badge_text}</span>
                <div class="chapter-title">Chapter {chapter['id']}: {chapter['title']}</div>
                <div class="chapter-desc">{chapter['description']}</div>
                <div class="chapter-level">Level: {chapter['level']}</div>
                {score_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

        if unlocked:
            btn_type = "secondary" if completed else "primary"
            if st.button("Open Chapter →", key=f"open_{chapter['id']}", type=btn_type):
                st.session_state.selected_chapter = chapter["id"]
                go_to("Chapter")
        else:
            st.markdown(
                "<div style='color:#94a3b8;font-size:13px;padding:4px 0 12px 4px;'>🔒 Complete the previous chapter to unlock</div>",
                unsafe_allow_html=True,
            )


# ════════════════════════════════════════════════════════════════
# CHAPTER
# ════════════════════════════════════════════════════════════════
elif st.session_state.page == "Chapter":

    chapter_id = st.session_state.selected_chapter
    chapter = next((item for item in CHAPTERS if item["id"] == chapter_id), None)

    if not chapter:
        st.error("Chapter not found.")
        if st.button("← Back"):
            go_to("Learning Path")
    else:
        if st.button("← Back to Learning Path"):
            go_to("Learning Path")

        st.markdown(
            f"""
            <div class="page-header">
                <div class="page-header-icon">📖</div>
                <div>
                    <div class="page-header-title">Chapter {chapter['id']}: {chapter['title']}</div>
                    <div class="page-header-sub">Level: {chapter['level']} · Read the lesson, then take the quiz.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Chapter content ──────────────────────────────
        if chapter_id == 1:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown("### 🔤 German Alphabet")
            st.write("German uses the Latin alphabet with some extra characters (Ä, Ö, Ü, ß).")
            letters = [
                ("A","Ah"), ("B","Beh"), ("C","Tseh"), ("D","Deh"), ("E","Eh"),
                ("F","Eff"), ("G","Geh"), ("H","Hah"), ("I","Ee"), ("J","Yot"),
                ("K","Kah"), ("L","Ell"), ("M","Em"), ("N","En"), ("O","Oh"),
                ("P","Peh"), ("Q","Kuh"), ("R","Err"), ("S","Ess"), ("T","Teh"),
                ("U","Oo"), ("V","Fau"), ("W","Veh"), ("X","Iks"), ("Y","Ypsilon"), ("Z","Tsett"),
            ]
            cols = st.columns(4)
            for i, (letter, sound) in enumerate(letters):
                with cols[i % 4]:
                    st.markdown(
                        f"<div style='background:#f5f3ff;border-radius:10px;padding:10px 14px;"
                        f"margin-bottom:8px;text-align:center;'>"
                        f"<div style='font-size:22px;font-weight:800;color:#6d28d9;'>{letter}</div>"
                        f"<div style='font-size:11px;color:#7c3aed;'>{sound}</div>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
            st.markdown('</div>', unsafe_allow_html=True)
            st.info("💡 Tip: Practice saying the alphabet aloud every day for 2 minutes.")

        elif chapter_id == 2:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown("### 👋 German Greetings")
            greetings = [
                ("Hallo", "Hello", "Salam / Hello"),
                ("Guten Morgen", "Good morning", "Subah bakhair"),
                ("Guten Tag", "Good day", "Din bakhair"),
                ("Guten Abend", "Good evening", "Shaam bakhair"),
                ("Tschüss", "Goodbye", "Allah hafiz"),
                ("Danke", "Thank you", "Shukriya"),
                ("Bitte", "Please / You're welcome", "Meherbani / Koi baat nahi"),
            ]
            for de, en, ru in greetings:
                st.markdown(
                    f"""
                    <div class="vocab-row">
                        <div class="vocab-de">{de}</div>
                        <div class="vocab-en">{en}</div>
                        <div class="vocab-ru">🇵🇰 {ru}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

        elif chapter_id == 3:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown("### 🔢 Numbers 1–20")
            numbers = {1:"eins",2:"zwei",3:"drei",4:"vier",5:"fünf",6:"sechs",7:"sieben",
                       8:"acht",9:"neun",10:"zehn",11:"elf",12:"zwölf",13:"dreizehn",
                       14:"vierzehn",15:"fünfzehn",16:"sechzehn",17:"siebzehn",18:"achtzehn",
                       19:"neunzehn",20:"zwanzig"}
            cols = st.columns(4)
            for i, (num, word) in enumerate(numbers.items()):
                with cols[i % 4]:
                    st.markdown(
                        f"<div style='background:#f0fdf4;border-radius:10px;padding:10px 12px;"
                        f"margin-bottom:8px;text-align:center;'>"
                        f"<div style='font-size:20px;font-weight:800;color:#065f46;'>{num}</div>"
                        f"<div style='font-size:13px;color:#10b981;font-weight:600;'>{word}</div>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
            st.markdown('</div>', unsafe_allow_html=True)

        elif chapter_id == 4:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown("### 🙋 Introduce Yourself")
            phrases = [
                ("Ich heiße Ahmad.", "My name is Ahmad.", "Mera naam Ahmad hai."),
                ("Ich bin Student.", "I am a student.", "Main student hoon."),
                ("Ich komme aus Pakistan.", "I come from Pakistan.", "Main Pakistan se hoon."),
            ]
            for de, en, ru in phrases:
                st.markdown(
                    f"""
                    <div style="background:#f5f3ff;border-radius:12px;padding:18px 22px;margin-bottom:12px;">
                        <div style="font-size:20px;font-weight:800;color:#4c1d95;margin-bottom:6px;">{de}</div>
                        <div style="font-size:14px;color:#6d28d9;margin-bottom:2px;">🇬🇧 {en}</div>
                        <div style="font-size:13px;color:#7c3aed;font-style:italic;">🇵🇰 {ru}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

        elif chapter_id == 5:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown("### 🏠 Everyday German Vocabulary")
            vocab = [
                ("Wasser", "Water"), ("Haus", "House"), ("Universität", "University"),
                ("Freund", "Friend"), ("Essen", "Food"), ("Arbeit", "Work"),
                ("Buch", "Book"), ("Schule", "School"),
            ]
            for de, en in vocab:
                st.markdown(
                    f"""
                    <div class="vocab-row">
                        <div class="vocab-de">{de}</div>
                        <div class="vocab-en">{en}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)
        if st.button("📝 Take Chapter Quiz", type="primary"):
            go_to("Quiz")


# ════════════════════════════════════════════════════════════════
# QUIZ
# ════════════════════════════════════════════════════════════════
elif st.session_state.page == "Quiz":

    chapter_id = st.session_state.selected_chapter
    chapter = next((item for item in CHAPTERS if item["id"] == chapter_id), None)

    if not chapter:
        st.error("Chapter not found.")
        if st.button("← Back"):
            go_to("Learning Path")
    else:
        st.markdown(
            f"""
            <div class="page-header">
                <div class="page-header-icon">📝</div>
                <div>
                    <div class="page-header-title">Quiz: {chapter['title']}</div>
                    <div class="page-header-sub">Level: {chapter['level']} · Need 70% or more to pass.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.info("💡 Choose the correct answer for each question. You need **at least 70%** to pass and unlock the next chapter.")

        quiz = get_quiz(chapter_id)
        if not quiz:
            st.warning("Quiz is not available yet.")
        else:
            answers = {}
            for index, question in enumerate(quiz):
                st.markdown(
                    f"""
                    <div class="quiz-question">
                        <div class="quiz-question-num">Question {index + 1} of {len(quiz)}</div>
                        <div class="quiz-question-text">{question['question']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                answers[index] = st.radio(
                    "Select your answer:",
                    question["options"],
                    key=f"q_{chapter_id}_{index}",
                    label_visibility="collapsed",
                )
                st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)

            st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
            if st.button("✅ Submit Quiz", type="primary", use_container_width=True):

                correct = sum(
                    1 for index, question in enumerate(quiz)
                    if answers.get(index) == question["answer"]
                )
                score = int((correct / len(quiz)) * 100)
                passed = score >= 70
                xp = score * 10 if passed else 0

                save_quiz_result(chapter_id, chapter["title"], score, xp, passed)

                st.session_state.quiz_submitted = True
                st.session_state.quiz_score = score
                st.session_state.quiz_correct = correct
                st.session_state.quiz_total = len(quiz)

                st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

                if passed:
                    st.markdown(
                        f"""
                        <div class="score-pass">
                            <div class="score-number">{score}%</div>
                            <div class="score-label" style="color:#065f46;">🎉 Excellent! You passed!</div>
                            <div style="margin-top:10px;font-size:14px;color:#047857;">
                                {correct} / {len(quiz)} correct · You earned <b>{xp} XP</b>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.balloons()
                    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

                    if chapter_id < len(CHAPTERS):
                        st.success("🔓 The next chapter is now unlocked!")
                    else:
                        st.success("🏆 You completed all available chapters!")

                    if st.button("📚 Continue Learning", use_container_width=True, type="primary"):
                        go_to("Learning Path")
                else:
                    st.markdown(
                        f"""
                        <div class="score-fail">
                            <div class="score-number">{score}%</div>
                            <div class="score-label" style="color:#7f1d1d;">You need 70% to pass</div>
                            <div style="margin-top:10px;font-size:14px;color:#991b1b;">
                                {correct} / {len(quiz)} correct · Review the chapter and try again.
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)
                    if st.button("🔄 Review Chapter", use_container_width=True):
                        go_to("Chapter")


# ════════════════════════════════════════════════════════════════
# AI TRANSLATOR
# ════════════════════════════════════════════════════════════════
elif st.session_state.page == "AI Translator":

    st.markdown(
        """
        <div class="page-header">
            <div class="page-header-icon">🤖</div>
            <div>
                <div class="page-header-title">AI German Translator</div>
                <div class="page-header-sub">Write in English, Urdu, or Roman Urdu — get instant German with explanation.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    text = st.text_area(
        "Enter your sentence",
        placeholder="Example: hi kya haal hai  /  How are you?  /  Mujhe paani chahiye",
        height=110,
    )

    if st.button("Translate with AI 🚀", type="primary"):
        if not text.strip():
            st.warning("Please enter a sentence to translate.")
        else:
            with st.spinner("AI is translating…"):
                try:
                    result = translate_with_ai(text)

                    # German block
                    st.markdown(
                        f"""
                        <div class="result-german">
                            <div class="result-german-label">🇩🇪 German</div>
                            <div class="result-german-word">{result['german']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(
                            f"""
                            <div class="result-box">
                                <div class="result-box-label">🇬🇧 English</div>
                                <div class="result-box-value">{result['english']}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    with col2:
                        st.markdown(
                            f"""
                            <div class="result-box">
                                <div class="result-box-label">🇵🇰 Roman Urdu</div>
                                <div class="result-box-value">{result['roman_urdu']}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

                    lvl_col, exp_col = st.columns([1, 2])
                    with lvl_col:
                        st.markdown(
                            f"""
                            <div class="result-box">
                                <div class="result-box-label">📚 Level</div>
                                <div class="result-box-value">{result['level']}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    with exp_col:
                        st.markdown(
                            f"""
                            <div class="result-box">
                                <div class="result-box-label">💡 Explanation</div>
                                <div class="result-box-value">{result['explanation']}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)
                    st.markdown("**🔎 Word Breakdown**")
                    chips_html = "".join(
                        f"<span class='word-chip'><b>{w['german']}</b> → {w['meaning']}</span>"
                        for w in result["words"]
                    )
                    st.markdown(
                        f"<div style='margin-top:8px'>{chips_html}</div>",
                        unsafe_allow_html=True,
                    )

                except Exception as e:
                    st.error(f"AI Error: {str(e)}")


# ════════════════════════════════════════════════════════════════
# AI TUTOR
# ════════════════════════════════════════════════════════════════
elif st.session_state.page == "AI Tutor":

    st.markdown(
        """
        <div class="page-header">
            <div class="page-header-icon">👨‍🏫</div>
            <div>
                <div class="page-header-title">AI German Tutor</div>
                <div class="page-header-sub">Ask anything about German grammar, vocabulary, or pronunciation.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Example questions
    st.markdown("**💬 Suggested questions:**")
    ex_cols = st.columns(3)
    examples = [
        "How do I use 'der', 'die', 'das'?",
        "How do I introduce myself in German?",
        "What is the difference between du and Sie?",
    ]
    for col, ex in zip(ex_cols, examples):
        with col:
            st.markdown(
                f"<div style='background:#f5f3ff;border:1px solid #c4b5fd;border-radius:10px;"
                f"padding:10px 12px;font-size:12.5px;color:#5b21b6;cursor:pointer;"
                f"text-align:center;'>{ex}</div>",
                unsafe_allow_html=True,
            )

    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

    question = st.text_area(
        "Your question",
        placeholder="Example: How do I say 'I want to eat' in German?",
        height=120,
    )

    if st.button("Ask AI Tutor 🎓", type="primary"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Your AI tutor is thinking…"):
                try:
                    answer = ask_tutor(question)
                    st.markdown(
                        f'<div class="tutor-answer">{answer}</div>',
                        unsafe_allow_html=True,
                    )
                except Exception as e:
                    st.error(f"AI Error: {str(e)}")
