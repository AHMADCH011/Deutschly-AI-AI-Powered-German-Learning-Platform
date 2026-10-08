import streamlit as st

from groq_service import translate_with_ai, ask_tutor
from quiz_data import CHAPTERS, get_quiz
from database import init_db, get_progress, save_quiz_result


# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Deutschly AI",
    page_icon="🇩🇪",
    layout="wide"
)

# Initialize database
init_db()


# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
    .main-title {
        font-size: 48px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 20px;
        color: #666;
        margin-bottom: 30px;
    }

    .card {
        padding: 22px;
        border-radius: 15px;
        border: 1px solid #ddd;
        margin-bottom: 15px;
        background-color: #fafafa;
    }

    .german {
        font-size: 26px;
        font-weight: 700;
    }

    .stat {
        text-align: center;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #ddd;
    }

    .xp {
        font-size: 30px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Session state
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "selected_chapter" not in st.session_state:
    st.session_state.selected_chapter = None


def go_to(page):
    st.session_state.page = page
    st.rerun()


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.title("🇩🇪 Deutschly AI")

    st.caption("German learning for Pakistani students")

    if st.button("🏠 Dashboard", use_container_width=True):
        go_to("Dashboard")

    if st.button("📚 Learning Path", use_container_width=True):
        go_to("Learning Path")

    if st.button("🤖 AI Translator", use_container_width=True):
        go_to("AI Translator")

    if st.button("👨‍🏫 AI Tutor", use_container_width=True):
        go_to("AI Tutor")

    st.divider()

    st.markdown("### 🎯 Your Goal")

    st.write("Learn German from A0 → B2")

    st.write("🇵🇰 Pakistani student focused")

    st.divider()

    st.caption("Deutschly AI v1.0")


# -----------------------------
# Get progress
# -----------------------------
progress = get_progress()

completed_chapters = sum(
    1 for item in progress
    if item["completed"] == 1
)

total_xp = sum(
    item["xp"] for item in progress
)

total_chapters = len(CHAPTERS)

progress_percentage = int(
    (completed_chapters / total_chapters) * 100
) if total_chapters else 0


# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.page == "Dashboard":

    st.markdown(
        '<div class="main-title">🇩🇪 Deutschly AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Learn German with AI — explained in a way Pakistani students understand.</div>',
        unsafe_allow_html=True
    )

    # Stats
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Level", "A0")

    with col2:
        st.metric("Progress", f"{progress_percentage}%")

    with col3:
        st.metric("Completed", f"{completed_chapters}/{total_chapters}")

    with col4:
        st.metric("XP", total_xp)

    st.divider()

    st.subheader("🚀 Continue Learning")

    next_chapter = None

    for chapter in CHAPTERS:

        chapter_progress = next(
            (
                item
                for item in progress
                if item["chapter_id"] == chapter["id"]
            ),
            None
        )

        if not chapter_progress or chapter_progress["completed"] == 0:
            next_chapter = chapter
            break

    if next_chapter:

        st.markdown(
            f"""
            <div class="card">
                <h3>📖 {next_chapter["title"]}</h3>
                <p>{next_chapter["description"]}</p>
                <p><b>Level:</b> {next_chapter["level"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Start Learning →",
            type="primary"
        ):
            st.session_state.selected_chapter = next_chapter["id"]
            go_to("Chapter")

    else:

        st.success(
            "🎉 Congratulations! You completed all available chapters!"
        )

    st.divider()

    st.subheader("✨ Why Deutschly AI?")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("### 🇵🇰 Pakistani Friendly")
        st.write(
            "Learn German using English and Roman Urdu explanations."
        )

    with c2:
        st.markdown("### 🤖 AI Powered")
        st.write(
            "Use AI to translate sentences and ask questions."
        )

    with c3:
        st.markdown("### 🎯 Practical")
        st.write(
            "Learn German for university, travel and daily life."
        )


# ============================================================
# LEARNING PATH
# ============================================================

elif st.session_state.page == "Learning Path":

    st.title("📚 German Learning Path")

    st.write(
        "Complete each chapter and pass the quiz with at least 70%."
    )

    for chapter in CHAPTERS:

        chapter_progress = next(
            (
                item
                for item in progress
                if item["chapter_id"] == chapter["id"]
            ),
            None
        )

        completed = (
            chapter_progress
            and chapter_progress["completed"] == 1
        )

        # Unlock logic
        if chapter["id"] == 1:
            unlocked = True
        else:
            previous = next(
                (
                    item
                    for item in progress
                    if item["chapter_id"] == chapter["id"] - 1
                ),
                None
            )

            unlocked = (
                previous
                and previous["completed"] == 1
            )

        with st.container(border=True):

            col1, col2, col3 = st.columns([1, 4, 1])

            with col1:

                if completed:
                    st.success("✅")
                elif unlocked:
                    st.info("🔓")
                else:
                    st.warning("🔒")

            with col2:

                st.subheader(
                    f"Chapter {chapter['id']}: {chapter['title']}"
                )

                st.write(chapter["description"])

                st.caption(
                    f"Level: {chapter['level']}"
                )

                if completed and chapter_progress:
                    st.write(
                        f"Best Score: {chapter_progress['score']}%"
                    )

            with col3:

                if unlocked:

                    if st.button(
                        "Open",
                        key=f"open_{chapter['id']}"
                    ):

                        st.session_state.selected_chapter = chapter["id"]

                        go_to("Chapter")

                else:

                    st.write("Locked")


# ============================================================
# CHAPTER
# ============================================================

elif st.session_state.page == "Chapter":

    chapter_id = st.session_state.selected_chapter

    chapter = next(
        (
            item
            for item in CHAPTERS
            if item["id"] == chapter_id
        ),
        None
    )

    if not chapter:

        st.error("Chapter not found.")

        if st.button("Back"):
            go_to("Learning Path")

    else:

        if st.button("← Back to Learning Path"):
            go_to("Learning Path")

        st.title(
            f"📖 Chapter {chapter['id']}: {chapter['title']}"
        )

        st.caption(
            f"Level: {chapter['level']}"
        )

        # Chapter content
        if chapter_id == 1:

            st.subheader("🇩🇪 German Alphabet")

            st.write(
                "German uses the Latin alphabet with some additional characters."
            )

            st.markdown("""
            **Important German letters**

            A → Ah  
            B → Beh  
            C → Tseh  
            D → Deh  
            E → Eh  
            F → Eff  
            G → Geh  
            H → Hah  
            I → Ee  
            J → Yot  
            K → Kah  
            L → Ell  
            M → Em  
            N → En  
            O → Oh  
            P → Peh  
            Q → Kuh  
            R → Err  
            S → Ess  
            T → Teh  
            U → Oo  
            V → Fau  
            W → Veh  
            X → Iks  
            Y → Ypsilon  
            Z → Tsett
            """)

            st.info(
                "Tip: Practice saying the alphabet aloud."
            )

        elif chapter_id == 2:

            st.subheader("👋 German Greetings")

            st.markdown("""
            **Hallo** → Hello

            **Guten Morgen** → Good morning

            **Guten Tag** → Good day

            **Guten Abend** → Good evening

            **Tschüss** → Goodbye

            **Danke** → Thank you

            **Bitte** → Please / You're welcome
            """)

        elif chapter_id == 3:

            st.subheader("🔢 Numbers 1–20")

            numbers = {
                1: "eins",
                2: "zwei",
                3: "drei",
                4: "vier",
                5: "fünf",
                6: "sechs",
                7: "sieben",
                8: "acht",
                9: "neun",
                10: "zehn",
                11: "elf",
                12: "zwölf",
                13: "dreizehn",
                14: "vierzehn",
                15: "fünfzehn",
                16: "sechzehn",
                17: "siebzehn",
                18: "achtzehn",
                19: "neunzehn",
                20: "zwanzig"
            }

            for number, german in numbers.items():
                st.write(f"**{number} → {german}**")

        elif chapter_id == 4:

            st.subheader("🙋 Introduce Yourself")

            st.markdown("""
            **Ich heiße Ahmad.**

            My name is Ahmad.

            Roman Urdu:

            Mera naam Ahmad hai.

            ---

            **Ich bin Student.**

            I am a student.

            Roman Urdu:

            Main student hoon.

            ---

            **Ich komme aus Pakistan.**

            I come from Pakistan.

            Roman Urdu:

            Main Pakistan se hoon.
            """)

        elif chapter_id == 5:

            st.subheader("🏠 Everyday German")

            st.markdown("""
            Wasser → Water

            Haus → House

            Universität → University

            Freund → Friend

            Essen → Food

            Arbeit → Work

            Buch → Book

            Schule → School
            """)

        st.divider()

        if st.button(
            "📝 Take Chapter Quiz",
            type="primary"
        ):
            go_to("Quiz")


# ============================================================
# QUIZ
# ============================================================

elif st.session_state.page == "Quiz":

    chapter_id = st.session_state.selected_chapter

    chapter = next(
        (
            item
            for item in CHAPTERS
            if item["id"] == chapter_id
        ),
        None
    )

    if not chapter:

        st.error("Chapter not found.")

    else:

        st.title(
            f"📝 Quiz: {chapter['title']}"
        )

        quiz = get_quiz(chapter_id)

        if not quiz:

            st.warning("Quiz is not available yet.")

        else:

            answers = {}

            for index, question in enumerate(quiz):

                st.markdown(
                    f"### {index + 1}. {question['question']}"
                )

                answers[index] = st.radio(
                    "Choose an answer:",
                    question["options"],
                    key=f"q_{chapter_id}_{index}"
                )

            if st.button(
                "Submit Quiz",
                type="primary"
            ):

                correct = 0

                for index, question in enumerate(quiz):

                    if answers[index] == question["answer"]:
                        correct += 1

                score = int(
                    (correct / len(quiz)) * 100
                )

                passed = score >= 70

                xp = score * 10 if passed else 0

                save_quiz_result(
                    chapter_id,
                    chapter["title"],
                    score,
                    xp,
                    passed
                )

                st.divider()

                if passed:

                    st.success(
                        f"🎉 Passed! Your score is {score}%"
                    )

                    st.balloons()

                    st.info(
                        f"⭐ You earned {xp} XP!"
                    )

                    if chapter_id < len(CHAPTERS):

                        st.write(
                            "🔓 The next chapter is now unlocked."
                        )

                    if st.button("Continue Learning"):

                        go_to("Learning Path")

                else:

                    st.error(
                        f"You scored {score}%. You need at least 70% to pass."
                    )

                    st.warning(
                        "📚 Review the chapter and try again."
                    )


# ============================================================
# AI TRANSLATOR
# ============================================================

elif st.session_state.page == "AI Translator":

    st.title("🤖 AI German Translator")

    st.write(
        "Write English, Urdu or Roman Urdu and Deutschly AI will teach you the German version."
    )

    text = st.text_area(
        "Enter your sentence",
        placeholder="Example: hi kya haal hai"
    )

    if st.button(
        "Translate with AI",
        type="primary"
    ):

        if not text.strip():

            st.warning("Please enter a sentence.")

        else:

            with st.spinner("AI is translating..."):

                try:

                    result = translate_with_ai(text)

                    st.subheader("🇩🇪 German")

                    st.markdown(
                        f'<div class="german">{result["german"]}</div>',
                        unsafe_allow_html=True
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.subheader("🇬🇧 English")

                        st.write(
                            result["english"]
                        )

                    with col2:

                        st.subheader("🇵🇰 Roman Urdu")

                        st.write(
                            result["roman_urdu"]
                        )

                    st.subheader("📚 Level")

                    st.info(
                        result["level"]
                    )

                    st.subheader("💡 Explanation")

                    st.write(
                        result["explanation"]
                    )

                    st.subheader("🔎 Word Breakdown")

                    for word in result["words"]:

                        st.write(
                            f"**{word['german']}** → {word['meaning']}"
                        )

                except Exception as e:

                    st.error(
                        f"AI Error: {str(e)}"
                    )


# ============================================================
# AI TUTOR
# ============================================================

elif st.session_state.page == "AI Tutor":

    st.title("👨‍🏫 AI German Tutor")

    st.write(
        "Ask your German teacher anything."
    )

    question = st.text_area(
        "Your question",
        placeholder="Example: How do I introduce myself in German?"
    )

    if st.button(
        "Ask AI Tutor",
        type="primary"
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Your AI tutor is thinking..."
            ):

                try:

                    answer = ask_tutor(question)

                    st.markdown(answer)

                except Exception as e:

                    st.error(
                        f"AI Error: {str(e)}"
                    )
