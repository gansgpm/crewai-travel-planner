# CrewAI Travel Planner Agent

A single-agent [CrewAI](https://docs.crewai.com) app: type in a city, and a **Travel Planner** agent suggests the **3 places a first-time visitor should not miss**, each with a short practical tip.

Built for **Social Eagle · Gen AI Architect Program — Week 4, Day 3**.

---

## Example output

```
Which city? Jaipur

Top 3 places to visit in Jaipur:
1. Amber Fort - hilltop fort with mirrored halls, go early
2. Hawa Mahal - the pink facade, best in morning light
3. City Palace - royal courtyards and a textile museum
```

When the script runs, the agent's working output (`verbose=True`) appears above the final answer.

---

## How it works

| Piece | What it does |
|---|---|
| **Agent** | A *Local Travel Planner* with a role, goal and backstory. The backstory says it writes for first-time visitors with only a day or two, so it picks must-see places and gives practical tips instead of long histories. |
| **Task** | Asks for exactly 3 places in `{city}`. The `expected_output` fixes the shape: 3 numbered lines in the format `Place - why it's special, one tip`, with no introduction or closing. |
| **Crew** | Combines the agent and task, then runs them with `crew.kickoff(inputs={"city": city})`, which fills the `{city}` placeholder. |

---

## Tech stack

- Python 3.10 – 3.13 (CrewAI does not support 3.14 yet)
- [CrewAI](https://pypi.org/project/crewai/)
- OpenAI API (`gpt-4o-mini` by default)
- `python-dotenv` to read the API key from a `.env` file

---

## Setup

### 1. Clone and create a virtual environment

**Windows (Command Prompt)**
```cmd
git clone https://github.com/gansgpm/crewai-travel-planner.git
cd crewai-travel-planner
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**macOS / Linux**
```bash
git clone https://github.com/gansgpm/crewai-travel-planner.git
cd crewai-travel-planner
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Add your OpenAI API key

Copy `.env.example` to `.env` and put your key in it:

```
OPENAI_API_KEY=sk-...your key...
MODEL=openai/gpt-4o-mini
```

Or skip this step. On the first run, the script asks you to paste your key (input is hidden) and saves it to `.env` for you.

### 3. Run

```cmd
python travel_planner.py
```

Try a few different cities and the suggestions change each time.

---

## Project structure

```
crewai-travel-planner/
├── travel_planner.py   # Agent, Task and Crew
├── requirements.txt    # crewai, python-dotenv
├── .env.example        # Template for your API key
├── .gitignore          # Keeps .env and venv out of Git
└── README.md
```

---

## Security

The API key is **never hard-coded**. It is read from environment variables loaded from `.env`, and `.env` is listed in `.gitignore`, so it is never committed to GitHub.

---

## Author

[@gansgpm](https://github.com/gansgpm) · Social Eagle Gen AI Architect Program
