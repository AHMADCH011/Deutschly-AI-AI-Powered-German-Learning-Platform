# ============================================================
# DEUTSCHLY AI - CHAPTERS & QUIZZES
# ============================================================

CHAPTERS = [

    {
        "id": 1,
        "title": "German Alphabet",
        "level": "A0",
        "description": "Learn the German alphabet and pronunciation."
    },

    {
        "id": 2,
        "title": "Greetings",
        "level": "A0",
        "description": "Learn basic German greetings and polite expressions."
    },

    {
        "id": 3,
        "title": "Numbers 1–20",
        "level": "A0",
        "description": "Learn German numbers from one to twenty."
    },

    {
        "id": 4,
        "title": "Introduce Yourself",
        "level": "A0",
        "description": "Learn how to introduce yourself in German."
    },

    {
        "id": 5,
        "title": "Everyday German",
        "level": "A0",
        "description": "Learn useful German words for everyday life."
    }
]


# ============================================================
# QUIZZES
# ============================================================

QUIZZES = {

    # --------------------------------------------------------
    # CHAPTER 1
    # --------------------------------------------------------

    1: [

        {
            "question": "Which letter is pronounced 'Ah'?",
            "options": [
                "A",
                "B",
                "C",
                "D"
            ],
            "answer": "A"
        },

        {
            "question": "Which letter is pronounced 'Beh'?",
            "options": [
                "A",
                "B",
                "E",
                "F"
            ],
            "answer": "B"
        },

        {
            "question": "Which letter is pronounced 'Tseh'?",
            "options": [
                "A",
                "B",
                "C",
                "D"
            ],
            "answer": "C"
        }

    ],


    # --------------------------------------------------------
    # CHAPTER 2
    # --------------------------------------------------------

    2: [

        {
            "question": "What does 'Hallo' mean?",
            "options": [
                "Hello",
                "Goodbye",
                "Thank you",
                "Please"
            ],
            "answer": "Hello"
        },

        {
            "question": "What does 'Danke' mean?",
            "options": [
                "Hello",
                "Thank you",
                "Goodbye",
                "Morning"
            ],
            "answer": "Thank you"
        },

        {
            "question": "What does 'Tschüss' mean?",
            "options": [
                "Hello",
                "Thank you",
                "Goodbye",
                "Please"
            ],
            "answer": "Goodbye"
        }

    ],


    # --------------------------------------------------------
    # CHAPTER 3
    # --------------------------------------------------------

    3: [

        {
            "question": "What is 1 in German?",
            "options": [
                "eins",
                "zwei",
                "drei",
                "vier"
            ],
            "answer": "eins"
        },

        {
            "question": "What is 5 in German?",
            "options": [
                "vier",
                "fünf",
                "sechs",
                "sieben"
            ],
            "answer": "fünf"
        },

        {
            "question": "What is 10 in German?",
            "options": [
                "zehn",
                "elf",
                "zwölf",
                "neun"
            ],
            "answer": "zehn"
        }

    ],


    # --------------------------------------------------------
    # CHAPTER 4
    # --------------------------------------------------------

    4: [

        {
            "question": "What does 'Ich heiße Ahmad' mean?",
            "options": [
                "I am Ahmad",
                "My name is Ahmad",
                "I live in Ahmad",
                "I like Ahmad"
            ],
            "answer": "My name is Ahmad"
        },

        {
            "question": "What does 'Ich bin Student' mean?",
            "options": [
                "I am a student",
                "I am a teacher",
                "I am a doctor",
                "I am a driver"
            ],
            "answer": "I am a student"
        },

        {
            "question": "What does 'Ich komme aus Pakistan' mean?",
            "options": [
                "I live in Pakistan",
                "I come from Pakistan",
                "I like Pakistan",
                "I visit Pakistan"
            ],
            "answer": "I come from Pakistan"
        }

    ],


    # --------------------------------------------------------
    # CHAPTER 5
    # --------------------------------------------------------

    5: [

        {
            "question": "What does 'Wasser' mean?",
            "options": [
                "Food",
                "Water",
                "House",
                "Work"
            ],
            "answer": "Water"
        },

        {
            "question": "What does 'Haus' mean?",
            "options": [
                "House",
                "Water",
                "University",
                "Friend"
            ],
            "answer": "House"
        },

        {
            "question": "What does 'Universität' mean?",
            "options": [
                "University",
                "School",
                "House",
                "Work"
            ],
            "answer": "University"
        }

    ]
}


# ============================================================
# GET QUIZ
# ============================================================

def get_quiz(chapter_id):
    """
    Return quiz questions for a chapter.
    """

    return QUIZZES.get(chapter_id, [])
