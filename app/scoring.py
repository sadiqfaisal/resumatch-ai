import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .config import (
    EXPERIENCE_WEIGHT,
    PREFERRED_SKILL_WEIGHT,
    REQUIRED_SKILL_WEIGHT,
    TFIDF_WEIGHT,
)

from .nlp_processor import preprocess_text
from .skills import calculate_skill_match


def extract_years_of_experience(text: str) -> float:
    text = str(text).lower()

    patterns = [
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?\s+(?:of\s+)?experience",
        r"experience\s*[:\-]\s*(\d+(?:\.\d+)?)\s*years?",
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?\s+in\s+",
    ]

    values = []

    for pattern in patterns:
        matches = re.findall(pattern, text)

        for match in matches:
            try:
                values.append(float(match))
            except ValueError:
                pass

    if not values:
        return 0.0

    return max(values)


def calculate_experience_score(
    candidate_years: float,
    required_years: float
) -> float:

    required_years = float(required_years or 0)
    candidate_years = float(candidate_years or 0)

    if required_years <= 0:
        return 1.0

    if candidate_years >= required_years:
        return 1.0

    return max(
        0.0,
        min(
            1.0,
            candidate_years / required_years
        )
    )


def calculate_tfidf_similarity(
    job_description: str,
    resume_texts: list[str]
) -> list[float]:

    documents = [
        preprocess_text(job_description)
    ]

    documents.extend(
        preprocess_text(text)
        for text in resume_texts
    )

    if len(documents) <= 1:
        return [0.0] * len(resume_texts)

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=1,
        sublinear_tf=True
    )

    matrix = vectorizer.fit_transform(
        documents
    )

    job_vector = matrix[0:1]

    resume_vectors = matrix[1:]

    similarities = cosine_similarity(
        job_vector,
        resume_vectors
    )[0]

    return [
        float(value)
        for value in similarities
    ]


def score_candidates(
    job_description: str,
    resumes: list[dict],
    required_skills: list[str],
    preferred_skills: list[str],
    required_years: float = 0
) -> list[dict]:

    if not resumes:
        return []

    resume_texts = [
        resume.get("text", "")
        for resume in resumes
    ]

    tfidf_scores = calculate_tfidf_similarity(
        job_description,
        resume_texts
    )

    results = []

    for index, resume in enumerate(resumes):

        skill_result = calculate_skill_match(
            resume["text"],
            required_skills,
            preferred_skills
        )

        experience_years = extract_years_of_experience(
            resume["text"]
        )

        experience_score = calculate_experience_score(
            experience_years,
            required_years
        )

        tfidf_score = tfidf_scores[index]

        required_score = skill_result[
            "required_score"
        ]

        preferred_score = skill_result[
            "preferred_score"
        ]

        final_score = (
            TFIDF_WEIGHT * tfidf_score
            + REQUIRED_SKILL_WEIGHT * required_score
            + PREFERRED_SKILL_WEIGHT * preferred_score
            + EXPERIENCE_WEIGHT * experience_score
        )

        result = {
            **resume,
            **skill_result,

            "tfidf_score": round(
                tfidf_score * 100,
                2
            ),

            "required_skill_score": round(
                required_score * 100,
                2
            ),

            "preferred_skill_score": round(
                preferred_score * 100,
                2
            ),

            "experience_score": round(
                experience_score * 100,
                2
            ),

            "experience_years": experience_years,

            "final_score": round(
                final_score * 100,
                2
            ),
        }

        results.append(result)

    results.sort(
        key=lambda item: item["final_score"],
        reverse=True
    )

    for rank, result in enumerate(
        results,
        start=1
    ):
        result["rank"] = rank

    return results
