import os
import json
import re

import streamlit as st
from openai import OpenAI


MODEL = "openrouter/free"


def get_api_key():

    try:
        if "OPENROUTER_API_KEY" in st.secrets:
            return st.secrets["OPENROUTER_API_KEY"]
    except Exception:
        pass

    return os.getenv("OPENROUTER_API_KEY")


def get_client():

    api_key = get_api_key()

    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY is missing. "
            "Add it to Streamlit Secrets."
        )

    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )


def ask_openrouter(system_prompt, user_prompt):

    client = get_client()

    response = client.chat.completions.create(

        model=MODEL,

        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],

        temperature=0.3,

        max_tokens=1200
    )

    return response.choices[0].message.content


def translate_with_ai(text):

    system_prompt = """
You are Deutschly AI, a German teacher designed
especially for Pakistani students.

The student may write English, Urdu, or Roman Urdu.

Translate the sentence into natural German.

Return ONLY valid JSON.

Use exactly this structure:

{
    "german": "German sentence",
    "english": "English meaning",
    "roman_urdu": "Roman Urdu meaning",
    "level": "A0/A1/A2/B1/B2",
    "explanation": "Simple explanation",
    "words": [
        {
            "german": "German word",
            "meaning": "English meaning"
        }
    ]
}
"""

    result = ask_openrouter(
        system_prompt,
        text
    )

    result = re.sub(
        r"```json|```",
        "",
        result
    ).strip()

    try:

        return json.loads(result)

    except json.JSONDecodeError:

        raise ValueError(
            "The AI returned an invalid JSON response. "
            "Please try again."
        )


def ask_tutor(question):

    system_prompt = """
You are Deutschly AI German Tutor.

You teach German to Pakistani students.

The student is a beginner.

Use simple English and Roman Urdu when useful.

When explaining German:

1. Give the German sentence.
2. Give English meaning.
3. Give Roman Urdu meaning.
4. Explain the grammar simply.
5. Give one additional example.
6. Give a small practice exercise.

Be friendly, encouraging and concise.
"""

    return ask_openrouter(
        system_prompt,
        question
    )
