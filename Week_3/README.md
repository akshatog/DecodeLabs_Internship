# AI Recommendation Logic - Project 3

Welcome to **Project 3** of the **DecodeLabs — Industrial Training Kit (Batch 2026)**.

This project focuses on building a **Tech Stack Recommender** using Content-Based Filtering. It takes a user's current skillset and maps it to the closest-matching job roles, successfully bypassing the "cold start" problem common to collaborative filtering.

## Features Checklist

This project successfully implements the 4-step ranking pipeline defined in the assignment brief:

- **[x] Ingestion:** Captures and normalizes the user's raw skills (requiring a minimum of 3 skills) to precisely match the dataset's vocabulary (handling spaces and capitalization).
- **[x] Scoring (TF-IDF & Cosine Similarity):** 
  - Leverages **TF-IDF** (Term Frequency-Inverse Document Frequency) instead of raw binary overlap. This down-weights generic skills (like "git") and appropriately rewards rare, highly specific skills.
  - Computes the **Cosine Similarity** between the user's profile and each job role. Unlike Euclidean distance, this measures orientation, ensuring the system isn't biased against roles with long lists of skills.
- **[x] Sorting:** Ranks all available job roles in descending order based on their similarity score to the user's profile.
- **[x] Filtering:** Truncates the results to the Top-N (default Top 3) matches to prevent choice overload.

## How It Works

The recommendation engine relies on a provided dataset (`raw_skills.csv`) containing various tech roles and their core skills. 

1. **Load Roles:** The system loads the job roles and converts their comma-separated skill lists into text "documents".
2. **Normalize Input:** The user provides their skills, which are cleaned (e.g., "machine learning" becomes "machine_learning") to ensure strict 1:1 matching with the dataset vocabulary.
3. **Vectorize:** The system builds a shared vocabulary space using `TfidfVectorizer` for all job roles alongside the user's profile.
4. **Rank & Recommend:** It calculates the cosine similarity, pairs each role with its score, sorts them descendingly, and filters down to the top recommendations.

## Prerequisites

Ensure you have Python installed, along with the `scikit-learn` package. You can install the required dependency via pip:

```bash
pip install scikit-learn
```

## How to Run

Execute the script from your terminal:

```bash
python Project_3.py
```

## Example Interaction

The script first runs a predefined example from the slides and then drops into an interactive mode so you can test your own unique skillset:

```text
User profile: ['python', 'cloud_computing', 'automation']

Top 3 recommended career paths:

  1. DevOps Engineer              — 32.5% match
  2. Cloud Architect              — 30.1% match
  3. Site Reliability Engineer    — 27.8% match

--- Try your own skills (comma-separated, e.g. java,sql,git) ---
Enter your skills: python, data analysis, statistics
```
