# Coding Standards

## Module structure
Each module folder (ingestion, normalization, kg, retriever, generator, eval, 
report) contains its own Python files. Shared utilities go in a `common/` folder 
if needed later.

## Naming
- Files: snake_case.py
- Functions: snake_case()
- Classes: PascalCase

## Environment variables
All API keys and secrets go in `.env` (never committed — see .gitignore).
Access via `os.getenv("KEY_NAME")` with python-dotenv.

## Commits
One logical change per commit. Reference the week/day in commit messages 
(e.g. "Week 7 Day 2: repo scaffolding").