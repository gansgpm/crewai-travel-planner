"""
Week 4 · Day 3 — CrewAI Travel Planner Agent
Social Eagle · Gen AI Architect Program

The user types in a city, and a Travel Planner agent suggests 3 places to visit.

The API key is read from a .env file in this folder (never hard-coded here):
  OPENAI_API_KEY=sk-...
  MODEL=openai/gpt-4o-mini
The .env file is listed in .gitignore, so it is never pushed to GitHub.

Run:  python travel_planner.py
"""

import os
import sys
from getpass import getpass
from pathlib import Path

from dotenv import load_dotenv

# --- 1. Load OPENAI_API_KEY and MODEL from the .env file next to this script --
ENV_FILE = Path(__file__).with_name(".env")
# override=True: the .env file wins over any old value set in the terminal.
load_dotenv(ENV_FILE, override=True)


def is_real_key(key: str) -> bool:
    """A real OpenAI key starts with 'sk-', is long, and isn't example text."""
    k = key.lower()
    return k.startswith("sk-") and len(key) >= 40 and "your" not in k and "paste" not in k


api_key = os.getenv("OPENAI_API_KEY", "").strip()
if not is_real_key(api_key):
    # First run (or .env still has example text): ask once, then save to .env
    print("No real OpenAI API key found in .env.")
    print("Paste your key below. Nothing will show while you paste - that's normal.")
    api_key = getpass("OpenAI API key: ").strip()
    if not is_real_key(api_key):
        sys.exit(
            "That doesn't look like a real OpenAI key. It should start with sk- and be "
            "a long string. Create one at platform.openai.com -> API keys."
        )
    model = os.getenv("MODEL", "").strip() or "openai/gpt-4o-mini"
    ENV_FILE.write_text(f"OPENAI_API_KEY={api_key}\nMODEL={model}\n", encoding="utf-8")
    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["MODEL"] = model
    print("Key saved to .env - you won't be asked again.\n")

from crewai import Agent, Crew, Task  # noqa: E402  (imported after the key is ready)

# --- 2. Ask the user for a city ---------------------------------------------
city = input("Which city? ").strip()
if not city:
    sys.exit("Please type a city name.")

# --- 3. The agent: role, goal and backstory as real sentences ---------------
planner = Agent(
    role="Local Travel Planner",
    goal=(
        "Recommend the three places in a city that a first-time visitor "
        "should not miss, each with one practical tip."
    ),
    backstory=(
        "You are a seasoned travel planner who has helped hundreds of first-time "
        "visitors make the most of short trips. Your travellers usually have only "
        "a day or two, so you skip long histories and pick the three places that "
        "give the truest feel of the city. You write like a friend sending quick "
        "advice: one short line per place, with a useful tip such as the best time to go."
    ),
    verbose=True,
)

# --- 4. The task: exactly 3 places, with the output shape spelled out -------
task = Task(
    description=(
        "Suggest exactly 3 places to visit in {city} for a first-time visitor "
        "with limited time. Pick well-known, real places located in {city} itself. "
        "For each place, say what makes it special and give one practical tip."
    ),
    expected_output=(
        "Exactly 3 numbered lines and nothing else: no introduction, no headings, "
        "no closing remarks. Each line must follow this format:\n"
        "<number>. <Place name> - <what makes it special>, <one short tip>\n"
        "Keep the text after the dash under 15 words."
    ),
    agent=planner,
)

# --- 5. Assemble the crew and run it ----------------------------------------
crew = Crew(agents=[planner], tasks=[task])

result = crew.kickoff(inputs={"city": city})  # fills {city} in the task description

print(f"\nTop 3 places to visit in {city}:")
print(result)
