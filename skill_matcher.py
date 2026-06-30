from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILLS = [
    "python",
    "java",
    "sql",
    "flask",
    "django",
    "machine learning",
    "html",
    "css",
    "javascript",
    "git"
]

def extract_skills(text):
    found_skills = []

    for skill in SKILLS:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    return found_skills


def calculate_match(resume_text, jd_text):

    documents = [resume_text, jd_text]

    vectorizer = TfidfVectorizer()

    matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        matrix[0:1],
        matrix[1:2]
    )

    return round(similarity[0][0] * 100, 2)