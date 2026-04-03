# task1_data_collection.py
# TrendPulse Task 1
# This script fetches trending stories from the HackerNews API,
# categorizes them based on keywords in the title,
# and saves the collected data into a JSON file.

import requests
import json
import os
import time
from datetime import datetime

# Header required by the assignment
headers = {"User-Agent": "TrendPulse/1.0"}

# API endpoints
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Category keywords (case-insensitive matching)
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Store collected stories
collected_stories = []

# Track how many stories per category
category_counts = {category: 0 for category in categories}


# Function to categorize a story based on title keywords
def get_category(title):
    title_lower = title.lower()
    for category, keywords in categories.items():
        for word in keywords:
            if word in title_lower:
                return category
    return None


# Step 1: Fetch top story IDs
try:
    response = requests.get(TOP_STORIES_URL, headers=headers)
    response.raise_for_status()
    story_ids = response.json()[:500]  # first 500 IDs
except requests.RequestException as e:
    print("Failed to fetch top stories:", e)
    exit()


# Step 2: Fetch each story's details
for story_id in story_ids:

    # Stop if all categories have 25 stories
    if all(count >= 25 for count in category_counts.values()):
        break

    try:
        story_response = requests.get(ITEM_URL.format(story_id), headers=headers)
        story_response.raise_for_status()
        story = story_response.json()
    except requests.RequestException:
        print(f"Failed to fetch story {story_id}")
        continue

    # Some stories may not have a title
    if not story or "title" not in story:
        continue

    title = story["title"]
    category = get_category(title)

    # Skip stories that don't match any category
    if category is None:
        continue

    # Skip if category already has 25 stories
    if category_counts[category] >= 25:
        continue

    # Extract required fields
    story_data = {
        "post_id": story.get("id"),
        "title": story.get("title"),
        "category": category,
        "score": story.get("score", 0),
        "num_comments": story.get("descendants", 0),
        "author": story.get("by"),
        "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    collected_stories.append(story_data)
    category_counts[category] += 1


# Sleep 2 seconds between category loops (assignment requirement)
for category in categories:
    time.sleep(2)


# Step 3: Save results to JSON file
# Create data folder if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

# File name with date
date_str = datetime.now().strftime("%Y%m%d")
file_path = f"data/trends_{date_str}.json"

# Save JSON
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(collected_stories, f, indent=4)

# Print final result
print(f"Collected {len(collected_stories)} stories. Saved to {file_path}")
