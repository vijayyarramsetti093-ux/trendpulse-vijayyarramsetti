# task2_data_processing.py
# TrendPulse Task 2
# This script loads the JSON file created in Task 1,
# cleans the data using Pandas, and saves the cleaned
# dataset as a CSV file.

import pandas as pd
import glob
import os

# Step 1: Locate the JSON file in the data folder
# We use glob so the script automatically finds trends_YYYYMMDD.json
json_files = glob.glob("data/trends_*.json")

if not json_files:
    print("No JSON file found in the data folder.")
    exit()

# Use the first JSON file found
json_file = json_files[0]

# Load JSON into a Pandas DataFrame
df = pd.read_json(json_file)

print(f"Loaded {len(df)} stories from {json_file}")

# -----------------------------
# Step 2: Clean the Data
# -----------------------------

# Remove duplicate stories based on post_id
before_duplicates = len(df)
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# Remove rows where important fields are missing
before_nulls = len(df)
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# Convert score and num_comments to integers
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# Remove low quality stories (score < 5)
before_low_scores = len(df)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# Remove extra whitespace from titles
df["title"] = df["title"].str.strip()

# -----------------------------
# Step 3: Save Clean Data
# -----------------------------

# Output CSV file
output_file = "data/trends_clean.csv"

# Save DataFrame
df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")

# Print stories per category
print("\nStories per category:")
category_counts = df["category"].value_counts()

for category, count in category_counts.items():
    print(f"  {category:<15} {count}")
