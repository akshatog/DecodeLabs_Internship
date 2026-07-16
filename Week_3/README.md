# AI Recommendation Logic - Project 3 (Advanced Capstone)

Welcome to **Project 3** of the **DecodeLabs — Industrial Training Kit (Batch 2026)**.

This project focuses on building a robust **Tech Stack Recommender** using Content-Based Filtering. It takes a user's current skillset, matches it to the closest job roles, and uniquely identifies what the user needs to learn next to achieve their career goals.

## Features Checklist

- **[x] Expanded Dataset:** The knowledge base (`raw_skills.csv`) has been massively expanded to ~30 modern tech roles, spanning Web3, AR/VR, Prompt Engineering, Cloud Security, and Data Science.
- **[x] Skill Gap Analysis:** Not only does the system score your current profile, but it also cross-references the dataset to provide a concrete **"To Learn"** list for your top-matched roles.
- **[x] Advanced Scoring (TF-IDF & Cosine Similarity):** 
  - **TF-IDF** effectively down-weights generic skills (like "git") while rewarding specific, highly-valuable skills (like "pytorch" or "solidity").
  - **Cosine Similarity** ensures the system evaluates the *direction* of your profile, immune to the size bias of Euclidean distance.
- **[x] Threshold Filtering:** Enforces a similarity threshold so you aren't recommended roles that are completely irrelevant to your input.
- **[x] Rich CLI Experience:** Implements ANSI terminal colors to provide a beautiful, readable, and interactive continuous loop interface.

## How It Works

1. **Load Roles:** The system loads ~30 job roles and their deep tech stacks.
2. **Normalize Input:** User inputs are cleaned (lowercased, spaces replaced with underscores) to ensure strict matching.
3. **Vectorize:** The system builds a shared vocabulary space using `TfidfVectorizer` for all roles and the user.
4. **Rank & Recommend:** Calculates cosine similarity to find top matches.
5. **Gap Analysis:** Subtracts the user's skillset from the target role's skillset to map out a clear learning path.

## Prerequisites

Ensure you have Python installed, along with `scikit-learn`. 

```bash
pip install scikit-learn numpy
```

## How to Run

Execute the script from your terminal:

```bash
python Project_3.py
```

## Example Interaction

```text
=== AI Tech Stack Recommender ===

[Running Example Profile]

--- Your Profile ---
python, machine learning, docker, sql, aws

--- Top 3 Career Paths ---
 1. Machine Learning Engineer    | 46.0% Match
    To Learn: pytorch, statistics, tensorflow, mlops, data structures
 2. Data Engineer                | 43.1% Match
    To Learn: etl, hadoop, kafka, spark, data pipelines, +1 more
 3. Data Scientist               | 39.8% Match
    To Learn: pandas, numpy, scikit-learn, statistics, jupyter, +1 more

=== Try Your Own Profile ===
Enter your skills separated by commas (e.g. java, spring boot, sql, git)
Skills (or 'exit'): 
```
