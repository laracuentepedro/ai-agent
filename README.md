## AI Agent (Gemini) + Sandbox Tools + Example Calculator

A small, local AI coding assistant that uses Google Gemini with function-calling to safely operate on a sandboxed working directory. The repo also includes a tiny calculator app used as a demo/target for the agent’s tools (list files, read files, write files, and run Python files).

### Why this project?
- Demonstrate a safe, tool-using AI agent loop
- Show simple guardrails around filesystem access
- Provide a concrete demo target (the calculator) the agent can inspect, run, and modify

---

## Repository layout
- main.py — CLI entry for the AI agent loop (Gemini 2.0 Flash)
- config.py — Agent configuration (working_dir, system prompt, read limits)
- functions/ — Function-calling tools exposed to Gemini
  - get_files_info.py — List files (guarded to working_dir)
  - get_file_content.py — Read file content (guarded to working_dir)
  - write_file.py — Write files (guarded to working_dir)
  - run_python_file.py — Execute a Python file (guarded to working_dir)
- calculator/ — Example target project the agent can work on
  - main.py — Simple CLI for evaluating expressions
  - pkg/calculator.py — Infix calculator with operator precedence
  - pkg/render.py — JSON formatting helper
- tests.py, get_file_content_tests.py, get_file_info_tests.py, write_file_tests.py — Simple scripts exercising the tools
- pyproject.toml — Project metadata and dependencies

---

## Requirements
- Python 3.13+
- A Google Gemini API key exported as GEMINI_API_KEY (or set in a .env file)

---

## Installation
Choose one of the following:

1) Using pip (recommended for most users)
- Create and activate a virtual environment
  - macOS/Linux:
    - python3 -m venv .venv
    - source .venv/bin/activate
  - Windows (PowerShell):
    - py -m venv .venv
    - .venv\\Scripts\\Activate.ps1
- Install project dependencies from pyproject.toml
  - pip install -e .

2) Using uv (optional, if you use uv)
- Install deps according to pyproject.toml
  - uv sync

Environment variables
- Create a .env file at the repo root (or export in your shell):
  - GEMINI_API_KEY=your_api_key_here

---

## Usage

### Run the AI Agent
The agent reads your prompt, may decide to call tools, and will iterate up to 20 turns.

- Basic:
  - python main.py "How do I fix the calculator?"
- With verbose logs:
  - python main.py "List files in the project" --verbose

What the tools do
- get_files_info(dir) — Lists files/sizes, but only within the configured working_dir
- get_file_content(path) — Reads a file inside working_dir up to a safe limit
- write_file(path, content) — Creates/overwrites a file inside working_dir
- run_python_file(path, args=[]) — Runs a Python script inside working_dir with optional args

By default, working_dir is set to ./calculator in config.py. You can point it to any local project directory you want the agent to operate on.

### Run the Calculator directly
- python calculator/main.py "3 + 5"
- Output will be JSON, e.g. {"expression": "3 + 5", "result": 8}

Notes
- The calculator expects space-separated tokens (e.g., "3 + 5 * 2").
- It supports +, -, *, / with basic precedence.

---

## Quick tests / demos
These are simple scripts that demonstrate the tools and guardrails.

- Run a Python file within working_dir:
  - python tests.py
- Read file content (valid and invalid paths):
  - python get_file_content_tests.py
- List files (valid and invalid dirs):
  - python get_file_info_tests.py
- Write files within working_dir (and a blocked attempt outside it):
  - python write_file_tests.py

---

## Configuration
- Edit config.py to change:
  - working_dir — The root directory the agent is allowed to interact with
  - max_read_chars — Max bytes to read from a file in a single call
  - system_prompt — High-level behavior and guardrails for the agent

---

## Troubleshooting
- ImportError: No module named google.genai
  - Ensure the venv is activated and dependencies are installed (pip install -e . or uv sync)
- Authentication/Permission errors
  - Verify GEMINI_API_KEY is set in your environment or .env file
- Python version issues
  - Confirm you’re running Python 3.13+ (python --version)

---

## Roadmap ideas
- Add pytest tests and CI
- Optional console script entry points
- Richer tools (search, refactor helpers)
- Safer write/edit flows (diff previews)
