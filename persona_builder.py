import re
import requests
from collections import Counter

USER_AGENT = "UserPersonaBuilder/0.1"

STOP_WORDS = {
    'the','and','that','have','for','with','this','http','https','from','they','you','your',
    'about','just','like','when','what','there','their','would','could','should','them','these','those','http','https','into','some','only','being','been','were','was','such','also'
}


def fetch_json(url, params=None):
    headers = {'User-Agent': USER_AGENT}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def get_username(url):
    match = re.search(r"reddit.com/(?:u|user)/([^/]+)/?", url)
    if not match:
        raise ValueError("Could not parse username from URL")
    return match.group(1)


def get_posts(username, limit=100):
    data = fetch_json(f"https://www.reddit.com/user/{username}/submitted.json", params={'limit': limit})
    posts = []
    for child in data.get('data', {}).get('children', []):
        d = child['data']
        posts.append({
            'title': d.get('title',''),
            'selftext': d.get('selftext',''),
            'subreddit': d.get('subreddit',''),
            'url': f"https://www.reddit.com{d.get('permalink','')}"
        })
    return posts


def get_comments(username, limit=100):
    data = fetch_json(f"https://www.reddit.com/user/{username}/comments.json", params={'limit': limit})
    comments = []
    for child in data.get('data', {}).get('children', []):
        d = child['data']
        comments.append({
            'body': d.get('body',''),
            'subreddit': d.get('subreddit',''),
            'url': f"https://www.reddit.com{d.get('permalink','')}"
        })
    return comments


def extract_age(text):
    match = re.search(r"\b(?:I['`]m|I am) (\d{2})\b", text)
    if match:
        age = match.group(1)
        return age
    return None


def extract_location(text):
    match = re.search(r"\b(?:I live in|I'm from) ([A-Z][A-Za-z ,]+)", text)
    if match:
        return match.group(1)
    return None


def extract_occupation(text):
    match = re.search(r"\b(?:I work as|I am a|I'm a) ([A-Za-z ]+)", text)
    if match:
        return match.group(1)
    return None


def clean_words(text):
    words = re.findall(r"[a-zA-Z']{4,}", text.lower())
    return [w for w in words if w not in STOP_WORDS]


def analyze(username):
    posts = get_posts(username)
    comments = get_comments(username)

    persona = {
        'username': username,
        'age': None,
        'age_src': None,
        'location': None,
        'location_src': None,
        'occupation': None,
        'occupation_src': None,
    }

    word_counter = Counter()
    subreddit_counter = Counter()

    def check_traits(text, url):
        if persona['age'] is None:
            age = extract_age(text)
            if age:
                persona['age'] = age
                persona['age_src'] = url
        if persona['location'] is None:
            loc = extract_location(text)
            if loc:
                persona['location'] = loc
                persona['location_src'] = url
        if persona['occupation'] is None:
            occ = extract_occupation(text)
            if occ:
                persona['occupation'] = occ
                persona['occupation_src'] = url
        for word in clean_words(text):
            word_counter[word] += 1

    for p in posts:
        subreddit_counter[p['subreddit']] += 1
        check_traits(p.get('title','') + ' ' + p.get('selftext',''), p['url'])
    for c in comments:
        subreddit_counter[c['subreddit']] += 1
        check_traits(c['body'], c['url'])

    top_words = [w for w,_ in word_counter.most_common(10)]
    top_subs = [f"r/{s}" for s,_ in subreddit_counter.most_common(5)]

    persona['interests'] = top_words
    persona['subreddits'] = top_subs

    persona_lines = [
        f"User Persona for u/{persona['username']}",
        "-----------------------------------",
    ]
    if persona['age']:
        persona_lines.append(f"Age: {persona['age']} (source: {persona['age_src']})")
    if persona['location']:
        persona_lines.append(f"Location: {persona['location']} (source: {persona['location_src']})")
    if persona['occupation']:
        persona_lines.append(f"Occupation: {persona['occupation']} (source: {persona['occupation_src']})")
    if persona['subreddits']:
        persona_lines.append("Frequent Subreddits: " + ', '.join(persona['subreddits']))
    if persona['interests']:
        persona_lines.append("Key Topics: " + ', '.join(persona['interests']))

    return '\n'.join(persona_lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Build a user persona from a Reddit profile URL")
    parser.add_argument('profile_url', help='URL to the Reddit user profile')
    parser.add_argument('-o', '--output', help='Output file name')
    args = parser.parse_args()

    username = get_username(args.profile_url)
    persona_text = analyze(username)
    outfile = args.output or f"persona_{username}.txt"
    with open(outfile, 'w') as f:
        f.write(persona_text)
    print(f"Persona written to {outfile}")

if __name__ == '__main__':
    main()
