# Contributing

Welcome! This document explains how to clone the project, run the app locally, and contribute changes via branches and pull requests.

## Quick clone (recommended)
You can either fork the repo and clone your fork, or clone directly (if you have push access).

Fork & clone (recommended for group work):
1. Go to https://github.com/adaughte777/stormsensexu and click "Fork".
2. Clone your fork:
   git clone https://github.com/<your-username>/stormsensexu.git
   cd stormsensexu

Clone directly (if you have access):
   git clone https://github.com/adaughte777/stormsensexu.git
   cd stormsensexu

## Set up the dev environment
macOS / Linux:
1. ./setup.sh
2. source .venv/bin/activate
3. streamlit run app.py

Windows (Command Prompt):
1. run setup_windows.bat
2. call .\.venv\Scripts\activate
3. python -m streamlit run app.py

If you prefer manual steps:
1. python3 -m venv .venv
2. source .venv/bin/activate  (Windows: .\.venv\Scripts\activate)
3. pip install -r requirements.txt
4. streamlit run app.py

## Branching & Pull Requests
- Create a feature branch:
  git checkout -b feature/short-description
- Make changes, then:
  git add .
  git commit -m "Short, clear message describing the change"
- Push:
  git push origin feature/short-description
- Open a Pull Request on GitHub from your branch into `main`. Request reviews from teammates.

## Coding standards & notes
- Keep changes focused and create one PR per feature/fix.
- Update README.md with any major changes and screenshots.
- If you add new packages, add them to requirements.txt.

## Help
If you have any trouble running the app or pushing changes, ask in the project channel or open an issue in the repo.
