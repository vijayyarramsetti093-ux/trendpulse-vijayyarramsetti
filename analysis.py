# task3_analysis.py
# TrendPulse Task 3
# This script loads the cleaned CSV from Task 2,
# performs analysis using Pandas and NumPy,
# creates new columns, and saves the updated data.

import pandas as pd
import numpy as np

# -----------------------------
# Step 1: Load and Explore Data
# -----------------------------

# Load the cleaned CSV file
file_path = "data/trends_clean.csv"
df = pd.read_csv(file_path)

# Print dataset shape
print(f"Loaded data: {df.shape}")

# Print first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Calculate average score and comments using Pandas
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"\nAverage score   : {avg_score:.2f}")
print(f"Average comments: {avg_comments:.2f}")


# -----------------------------
# Step 2: Analysis with NumPy
# -----------------------------

print("\n--- NumPy Stats ---")

scores = df["score"].to_numpy()

# Mean, median, std deviation
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)

print(f"Mean score   : {mean_score:.2f}")
print(f"Median score : {median_score:.2f}")
print(f"Std deviation: {std_score:.2f}")

# Max and Min score
max_score = np.max(scores)
min_score = np.min(scores)

print(f"Max score    : {max_score}")
print(f"Min score    : {min_score}")

# Category with most stories
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
top_count = category_counts.max()

print(f"\nMost stories in: {top_category} ({top_count} stories)")

# Story with most comments
max_comments_index = df["num_comments"].idxmax()
most_commented_title = df.loc[max_comments_index, "title"]
most_comments = df.loc[max_comments_index, "num_comments"]

print(f"\nMost commented story: \"{most_commented_title}\" — {most_comments} comments")


# -----------------------------
# Step 3: Add New Columns
# -----------------------------

# Engagement metric: comments per upvote
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Popular flag based on average score
df["is_popular"] = df["score"] > avg_score


# -----------------------------
# Step 4: Save Updated Data
# -----------------------------

output_file = "data/trends_analysed.csv"

df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")
