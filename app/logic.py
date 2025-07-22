"""central logic
- takes raw logs
- calls openai
- returns Analysis and Recommendation as two strings for streamlit UI
"""

from __future__ import annotations

import json
import os
from typing import Tuple

import openai
from dotenv import load_dotenv

# Configuration & API Setup
load_dotenv()

OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

if not OPENAI_API_KEY:
    raise EnvironmentError(
        "OPENAI_API_KEY missing. Create an .env file or export the key!"
    )

#openai python client configuration
openai.api_key = OPENAI_API_KEY




##Call the prompts from app.prompts or use fallback prompt:

DEFAULT_PROMPT_TMPL = (
    """
Du bist ein virtueller Krafttraining‐Coach. Analysiere das folgende Trainingslog
und gib ein JSON‐Objekt mit exakt zwei Schlüsseln zurück:
- "analysis": string  – Zusammenfassung (Leistung, Probleme, Intensität).
- "recommendation": string – Detaillierter Vorschlag fürs nächste Training.

__LOG__:
""""""{raw_log}""""""

Achte auf:
• Wiederholungen, Gewichte, Volumen
• subjektives Feeling (z. B. Schmerzen, Instabilität)
• progressive Steigerung oder Regression
"""
)


try: #checks if custom prompt exists, otherwise using fallback prompt
    from app.prompts import ANALYSE_AND_RECOMMEND_PROMPT as CUSTOM_PROMPT_TMPL  # type: ignore

    PROMPT_TEMPLATE = CUSTOM_PROMPT_TMPL
except ModuleNotFoundError:
    PROMPT_TEMPLATE = DEFAULT_PROMPT_TMPL


##Public API

def analyze_and_recommend(raw_log: str) -> Tuple[str, str]:
    """Main function, that will be called by *app/main.py*
    
    Parameters:
    raw_log: str
        raw text input, the user types in a chat format
        
    Returs:
        Tuple[str, str]
            (analysis, recommendation)"""
    prompt = PROMPT_TEMPLATE.format(raw_log=raw_log.strip())
    response = openai.chat.completions.create(
        model = OPENAI_MODEL,
        temperature = 0.3,
        messages = [
            {
                "role": "system",
                "content": "Du bist ein erfahrener, sachlicher Krafttraining-Coach."
            },
            {"role": "user", "content": prompt}
        ]
    )

    # Assistant output in JSON
    content = response.choices[0].message.content.strip()

    try:
        data = json.loads(content)
        analysis = data.get("analysis", "(Parsing‑Fehler: Feld 'analysis' fehlt)")
        recommendation = data.get(
            "recommendation", "(Parsing‑Fehler: Feld 'recommendation' fehlt)"
        )
    except json.JSONDecodeError:
        # Fallback: Wir konnten kein valides JSON parsen → volle Antwort splitten
        analysis, recommendation = _fallback_parse(content)

    return analysis, recommendation

#Helper function (Fallback)
def _fallback_parse(content: str) -> Tuple[str, str]:
    """Tries to split heuristically"""

    sep_keywords = ["empfehlung", "recommendation", "vorschlag"]
    lower = content.lower()

    for kw in sep_keywords:
        idx = lower.find(kw)
        if idx != -1:
            return content[:idx].strip(), content[idx:].strip()

    # return everything together as "content"
    return content, "(no recommendation found)"

if __name__ == "__main__":
    example_log = """[21.07.25] Bench 3x7x16kg, Hammer Curls 2x10x12kg. Feeling: Pump, rechte Schulter instabil."""
    ana, rec = analyze_and_recommend(example_log)
    print("ANALYSE\n-------\n", ana)
    print("\nEMPFEHLUNG\n----------\n", rec)
