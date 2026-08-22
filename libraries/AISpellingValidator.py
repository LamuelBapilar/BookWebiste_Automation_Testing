"""
AISpellingValidator.py
Uses the Groq API to check scraped book titles for spelling errors.
"""

import json
import re
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL = "openai/gpt-oss-120b"
GROQ_API = os.getenv("GROQ_API_KEY") 


class AISpellingValidator:
    ROBOT_LIBRARY_SCOPE = "SUITE"

    def __init__(self):
        if not GROQ_API:
            raise ValueError(
                "GROQ_API_KEY not found in environment variables. Please set it "
                "with GROQ_API_KEY=your_key_here in the project root."
            )       
        self.client = Groq(api_key=GROQ_API)
        self.misspelled = []

    def ai_check_titles_for_misspellings(self, books):
        titles = [book["title"] for book in books]
        # prompt Instruction for GROQ on how to process the data
        
        prompt = f"""You are a strict proofreader checking book titles for ACTUAL spelling mistakes only.

Titles:
{json.dumps(titles, indent=2)}

Rules:
- Only flag a word if it is a clear typo of a common English word (example: "recieve" instead of "receive", "wierd" instead of "weird").
- Do NOT flag invented words, character names, place names, brand names, or stylized fantasy/sci-fi terms, even if they look unusual (example: "Mesaerion", "Zephyria", "Nyxandra" are NOT misspellings — they are invented names).
- Do NOT flag proper nouns, author names, or foreign words.
- Do NOT flag informal or accepted alternate spellings of real words, even if unconventional (example: "Hijinx" is an accepted alternate spelling of "hijinks" — NOT a misspelling).
- Do NOT flag anything you are not highly confident is a genuine typo of a real, common English word.
- If a word could plausibly be intentional, stylistic, an alternate spelling, or a proper noun, treat it as NOT a misspelling.
- When in doubt, do NOT flag it. False positives are worse than missing a rare typo.

Respond ONLY with a JSON array, nothing else before or after it. Each item shaped like:
{{"title": "the full title", "misspelled_word": "the word", "suggestion": "corrected word"}}

If no misspellings are found, respond with exactly: []"""

        response = self.client.chat.completions.create(
            model=MODEL,
            max_tokens=2000, 
            reasoning_effort="low",
            messages=[{"role": "user", "content": prompt}]
        )

        raw_text = response.choices[0].message.content or ""
        raw_text = raw_text.strip()

        # raw AI response for debugging
        print("---- RAW AI RESPONSE ----")
        print(repr(raw_text))

        misspelled = self._extract_json_array(raw_text)
        self.misspelled = misspelled
        return misspelled

    def _extract_json_array(self, text):
        text = text.replace("```json", "").replace("```", "").strip()

        if not text:
            return [{"title": "PARSE_ERROR", "misspelled_word": "Empty response from AI model", "suggestion": ""}]

        match = re.search(r"\[.*\]", text, re.DOTALL)
        if not match:
            return [{"title": "PARSE_ERROR", "misspelled_word": text, "suggestion": ""}]

        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return [{"title": "PARSE_ERROR", "misspelled_word": text, "suggestion": ""}]

    def ai_titles_should_have_no_misspellings(self):
        if self.misspelled:
            raise AssertionError(f"AI flagged possible misspellings: {self.misspelled}")