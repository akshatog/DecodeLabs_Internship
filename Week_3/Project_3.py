"""
Project 3: AI Recommendation Logic — Capstone: Tech Stack Recommender
DecodeLabs — Industrial Training Kit (Batch 2026)

Goal: Map a user's raw skills to the closest-matching job roles using
Content-Based Filtering (no other-user data needed — avoids the "cold
start" problem the slides warn about).

The 4-step ranking pipeline from the brief:
  1. INGESTION -> capture user state (min 3 skills)
  2. SCORING   -> TF-IDF vectorize + Cosine Similarity against every role
  3. SORTING   -> rank roles by similarity score, descending
  4. FILTERING -> truncate to Top-N (Top 3) to avoid choice overload

Why TF-IDF + Cosine, not raw binary overlap + Euclidean:
  - Binary overlap treats "python" and "git" (common across roles) the
    same as rare, specific skills — TF-IDF's IDF term down-weights the
    generic ones and rewards the specific ones (slides 10-12).
  - Euclidean distance is sensitive to profile "size" (a role with more
    listed skills looks farther away even if it's a great match).
    Cosine similarity only cares about direction/orientation, so it's
    invariant to that — the industry-standard choice (slides 14-16).
"""

import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_roles(csv_path="raw_skills.csv"):
    """
    Load job roles and their skill tags from raw_skills.csv.
    Each row becomes one "item" in the recommendation engine (slide 22).
    """
    roles = []
    skill_docs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            roles.append(row["role"])
            # Turn the comma-separated skill list into a space-separated
            # "document" — this is the shared vocabulary space (slide 9).
            skills = row["skills"].replace(",", " ")
            skill_docs.append(skills)
    return roles, skill_docs


def normalize_skills(raw_skills):
    """
    PHASE 1: INGESTION
    Normalize user input to match the dataset's vocabulary: lowercase,
    spaces -> underscores (so "machine learning" matches "machine_learning"
    instead of splitting into two mismatched tokens — the exact vocabulary
    mismatch problem flagged on slide 9).
    """
    cleaned = [s.strip().lower().replace(" ", "_") for s in raw_skills if s.strip()]
    if len(cleaned) < 3:
        raise ValueError("Please provide at least 3 skills for accurate matching.")
    return cleaned


def score_and_rank(user_skills, roles, skill_docs, top_n=3):
    """
    PHASE 2: SCORING
    Build one shared TF-IDF vocabulary across ALL job-role documents plus
    the user's own profile, so they live in the same vector space.
    Then compute cosine similarity between the user vector and every
    role vector.

    PHASE 3: SORTING
    Rank descending by similarity score.

    PHASE 4: FILTERING
    Keep only the Top-N (default 3) so the user isn't overwhelmed.
    """
    user_profile = " ".join(user_skills)

    # Corpus = every role's skill document + the user's profile (last item)
    corpus = skill_docs + [user_profile]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    role_vectors = tfidf_matrix[:-1]   # all rows except the last
    user_vector = tfidf_matrix[-1]     # the last row = user profile

    # Cosine similarity between the user vector and every role vector
    similarities = cosine_similarity(user_vector, role_vectors).flatten()

    # Pair each role with its score, sort descending (Step 3: Sorting)
    ranked = sorted(zip(roles, similarities), key=lambda pair: pair[1], reverse=True)

    # Step 4: Filtering -> Top-N only
    return ranked[:top_n]


def recommend(raw_skills, csv_path="raw_skills.csv", top_n=3):
    """End-to-end pipeline: ingestion -> scoring -> sorting -> filtering."""
    roles, skill_docs = load_roles(csv_path)
    user_skills = normalize_skills(raw_skills)
    top_matches = score_and_rank(user_skills, roles, skill_docs, top_n=top_n)
    return user_skills, top_matches


def print_recommendations(user_skills, top_matches):
    print(f"\nUser profile: {user_skills}\n")
    print(f"Top {len(top_matches)} recommended career paths:\n")
    for rank, (role, score) in enumerate(top_matches, start=1):
        match_pct = round(score * 100, 1)
        print(f"  {rank}. {role:<28} — {match_pct}% match")
    print()


if __name__ == "__main__":
    # Example from the brief (slide 23): ["Python", "Cloud Computing", "Automation"]
    example_skills = ["Python", "Cloud Computing", "Automation"]
    user_skills, top_matches = recommend(example_skills)
    print_recommendations(user_skills, top_matches)

    # Interactive mode: type your own 3+ skills
    print("--- Try your own skills (comma-separated, e.g. java,sql,git) ---")
    raw = input("Enter your skills: ")
    if raw.strip():
        try:
            skills_list = raw.split(",")
            user_skills, top_matches = recommend(skills_list)
            print_recommendations(user_skills, top_matches)
        except ValueError as e:
            print(f"Error: {e}")