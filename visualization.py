# task4_visualization.py
# TrendPulse Task 4
# This script loads the analysed CSV file and creates visualizations
# using Matplotlib. The charts are saved as PNG images.

import pandas as pd
import matplotlib.pyplot as plt
import os

# -----------------------------
# Step 1: Load Data and Setup
# -----------------------------

# Load analysed data from Task 3
file_path = "data/trends_analysed.csv"
df = pd.read_csv(file_path)

# Create outputs folder if it does not exist
if not os.path.exists("outputs"):
    os.makedirs("outputs")


# -----------------------------
# Chart 1: Top 10 Stories by Score
# -----------------------------

# Sort stories by score and get top 10
top_stories = df.sort_values(by="score", ascending=False).head(10)

# Shorten long titles (max 50 characters)
titles = top_stories["title"].apply(lambda x: x[:50] + "..." if len(x) > 50 else x)

plt.figure(figsize=(10,6))
plt.barh(titles, top_stories["score"])
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")

# Highest score on top
plt.gca().invert_yaxis()

# Save chart
plt.savefig("outputs/chart1_top_stories.png")
plt.close()


# -----------------------------
# Chart 2: Stories per Category
# -----------------------------

category_counts = df["category"].value_counts()

plt.figure(figsize=(8,6))
plt.bar(category_counts.index, category_counts.values)

plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")

# Save chart
plt.savefig("outputs/chart2_categories.png")
plt.close()


# -----------------------------
# Chart 3: Score vs Comments
# -----------------------------

plt.figure(figsize=(8,6))

# Separate popular and non-popular stories
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()

# Save chart
plt.savefig("outputs/chart3_scatter.png")
plt.close()


# -----------------------------
# Bonus: Dashboard
# -----------------------------

fig, axes = plt.subplots(1, 3, figsize=(18,5))

# Chart 1 inside dashboard
axes[0].barh(titles, top_stories["score"])
axes[0].set_title("Top 10 Stories")
axes[0].set_xlabel("Score")
axes[0].set_ylabel("Title")
axes[0].invert_yaxis()

# Chart 2 inside dashboard
axes[1].bar(category_counts.index, category_counts.values)
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Stories")

# Chart 3 inside dashboard
axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Comments")
axes[2].legend()

# Overall dashboard title
plt.suptitle("TrendPulse Dashboard")

# Save dashboard
plt.savefig("outputs/dashboard.png")

plt.close()

print("Charts saved in outputs/ folder")
