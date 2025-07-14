# 🧠 Reddit User Persona Builder

A Python script that analyzes a Reddit user's public activity and generates a structured **User Persona** based on their comments and posts. Ideal for research, marketing, or social behavior analysis.

---

## 📌 Features

- ✅ Accepts a Reddit user profile URL as input
- 🔍 Scrapes the user's **posts** and **comments**
- 🧠 Builds a **User Persona** (name, interests, tone, personality traits, etc.)
- 📄 Outputs the persona to a neatly formatted **text file**
- 📝 Includes **citations** for each persona trait (linked back to the original post/comment)

---

## 🔧 Requirements

- Python 3.7+
- `praw` – Python Reddit API Wrapper
- `requests`
- `beautifulsoup4` *(optional if using HTML scraping)*

Install dependencies:

```bash
pip install praw requests beautifulsoup4
