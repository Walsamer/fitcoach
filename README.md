<p align="center">
  <img src="https://github.com/walsamer/fitcoach/raw/main/assets/fitcoach_banner.png" alt="FitCoach Banner" width="600"/>
</p>

# FitCoach – Language-Based Strength Training & Logging Assistant

**FitCoach** is a lightweight LLM-powered prototype for analyzing and improving strength training routines using natural language logs.  
It is designed as an AI engineering showcase that combines rapid prototyping, clean modular design, and practical use of the OpenAI API and Streamlit.

---

## Features
- Automatic GPT-based log analysis (intensity, volume, pain flags, progression)
- Smart training recommendation generation
- Modular prompt system with fallback and customization support


## Coming soon:
- Free-text workout logging (e.g. `"Bench 3x7x16kg, Shoulder unstable"`)
- Fully functional Streamlit UI and command-line testing
- Optional CSV or SQLite storage (via `database.py`)
- Matplotlib-based training history plots (in progress)

---

## Tech Stack

| Component        | Tool / Library         |
|------------------|------------------------|
| LLM backend      | [OpenAI API](https://openai.com/api) (Chat Completions) |
| UI & prototyping | [Streamlit](https://streamlit.io) |
| Environment mgmt | [python-dotenv](https://pypi.org/project/python-dotenv/) |
| Prompt handling  | Pure Python (`.format`) or custom module |
| Data persistence | CSV / SQLite (planned via `database.py`) |
| Plotting         | Matplotlib (in progress) |

---

## Example

```text
Input:
[21.07.25] Bench 3x7x16kg, Hammer Curls 2x10x12kg. Feeling: Shoulder pump, slight instability.

LLM Analysis:
- Moderate push volume, stable sets
- Instability in right shoulder flagged
- Progress consistent with last session

Recommendation:
- Reduce volume or load on push movements in next session
- Add external rotations and stabilization work
- Emphasize pulling movements (rows, lat work)
