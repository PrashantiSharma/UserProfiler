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
- `requests`

Install dependencies:

```bash
pip install requests
```

## 🚀 Usage

Run the `persona_builder.py` script with a Reddit profile URL:

```bash
python persona_builder.py https://www.reddit.com/user/example_user/

```

The script sends requests to `old.reddit.com` with a standard browser
`User-Agent` so it can access Reddit's public JSON feeds without authentication.
If you still see a `403` error, ensure your network allows outbound HTTPS
requests.
