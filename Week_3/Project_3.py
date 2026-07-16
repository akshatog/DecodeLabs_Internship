"""
Project 3: AI Recommendation Logic (Advanced Capstone)
DecodeLabs — Industrial Training Kit (Batch 2026)

Goal: A robust Tech Stack Recommender that not only maps skills to roles
using TF-IDF and Cosine Similarity, but also performs Skill Gap Analysis
to tell the user what to learn next.
"""

import csv
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- ANSI Colors for Terminal Output ---
class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def load_roles(csv_path="raw_skills.csv"):
    roles = []
    skill_docs = []
    raw_mappings = {}
    
    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                role_name = row["role"].strip()
                roles.append(role_name)
                # Store the actual list of skills for gap analysis later
                skills_list = [s.strip().lower().replace(" ", "_") for s in row["skills"].split(",") if s.strip()]
                raw_mappings[role_name] = set(skills_list)
                
                # Create the space-separated text doc for TF-IDF
                skill_docs.append(" ".join(skills_list))
    except FileNotFoundError:
        print(f"{Color.RED}Error: Dataset '{csv_path}' not found.{Color.ENDC}")
        exit(1)
        
    return roles, skill_docs, raw_mappings


def normalize_skills(raw_skills):
    """Normalize input: lowercase and replace spaces with underscores."""
    cleaned = [s.strip().lower().replace(" ", "_") for s in raw_skills if s.strip()]
    if len(cleaned) < 3:
        raise ValueError("Please provide at least 3 skills for accurate matching.")
    return cleaned


def score_and_rank(user_skills, roles, skill_docs, top_n=5, threshold=0.05):
    user_profile = " ".join(user_skills)
    corpus = skill_docs + [user_profile]

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    role_vectors = tfidf_matrix[:-1]
    user_vector = tfidf_matrix[-1]

    # Compute Cosine Similarity
    similarities = cosine_similarity(user_vector, role_vectors).flatten()

    # Sort descending
    ranked = sorted(zip(roles, similarities), key=lambda x: x[1], reverse=True)
    
    # Filter by threshold and take Top N
    filtered = [(r, s) for r, s in ranked if s >= threshold]
    return filtered[:top_n]


def analyze_skill_gap(user_skills, target_role, raw_mappings):
    """Identify which skills the user is missing for a target role."""
    user_set = set(user_skills)
    required_set = raw_mappings.get(target_role, set())
    
    missing = required_set - user_set
    return list(missing)


def print_recommendations(user_skills, top_matches, raw_mappings):
    print(f"\n{Color.BOLD}--- Your Profile ---{Color.ENDC}")
    print(f"{Color.BLUE}{', '.join(user_skills).replace('_', ' ')}{Color.ENDC}\n")
    
    if not top_matches:
        print(f"{Color.WARNING}No strong matches found. Try adding more specific technical skills.{Color.ENDC}\n")
        return

    print(f"{Color.BOLD}--- Top {len(top_matches)} Career Paths ---{Color.ENDC}")
    for rank, (role, score) in enumerate(top_matches, start=1):
        match_pct = round(score * 100, 1)
        
        # Determine color based on match percentage
        if match_pct >= 40:
            color = Color.GREEN
        elif match_pct >= 20:
            color = Color.WARNING
        else:
            color = Color.RED
            
        print(f" {rank}. {Color.BOLD}{role:<30}{Color.ENDC} | {color}{match_pct}% Match{Color.ENDC}")
        
        # Skill Gap Analysis
        missing_skills = analyze_skill_gap(user_skills, role, raw_mappings)
        if missing_skills:
            # Format nicely by removing underscores
            missing_clean = [s.replace('_', ' ') for s in missing_skills]
            gap_str = ", ".join(missing_clean[:5])
            if len(missing_clean) > 5:
                gap_str += f", +{len(missing_clean)-5} more"
            print(f"    {Color.HEADER}To Learn:{Color.ENDC} {gap_str}")
        else:
            print(f"    {Color.HEADER}To Learn:{Color.ENDC} You have all the core skills!")
        print()


def recommend_pipeline(raw_skills_list, csv_path="raw_skills.csv", top_n=5):
    try:
        roles, skill_docs, raw_mappings = load_roles(csv_path)
        user_skills = normalize_skills(raw_skills_list)
        top_matches = score_and_rank(user_skills, roles, skill_docs, top_n=top_n)
        print_recommendations(user_skills, top_matches, raw_mappings)
    except ValueError as e:
        print(f"{Color.RED}Error: {e}{Color.ENDC}")


if __name__ == "__main__":
    print(f"{Color.BOLD}=== AI Tech Stack Recommender ==={Color.ENDC}")
    
    # Example Run
    print("\n[Running Example Profile]")
    example = ["python", "machine learning", "docker", "sql", "aws"]
    recommend_pipeline(example, top_n=3)

    # Interactive Run
    print(f"{Color.BOLD}=== Try Your Own Profile ==={Color.ENDC}")
    print("Enter your skills separated by commas (e.g. java, spring boot, sql, git)")
    
    while True:
        raw = input(f"{Color.BLUE}Skills (or 'exit'): {Color.ENDC}")
        if raw.strip().lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        if raw.strip():
            skills = raw.split(",")
            recommend_pipeline(skills)