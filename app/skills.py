import re


SKILL_ALIASES = {
    "python": ["python"],
    "java": ["java"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "c++": ["c++", "cpp"],
    "c#": ["c#", "csharp"],

    "sql": [
        "sql",
        "mysql",
        "postgresql",
        "postgres"
    ],

    "mongodb": ["mongodb", "mongo"],

    "html": ["html"],
    "css": ["css"],

    "react": ["react", "reactjs"],
    "angular": ["angular"],

    "node.js": [
        "node.js",
        "nodejs"
    ],

    "flask": ["flask"],
    "django": ["django"],
    "fastapi": ["fastapi"],

    "pandas": ["pandas"],
    "numpy": ["numpy"],

    "scikit-learn": [
        "scikit-learn",
        "sklearn",
        "scikit learn"
    ],

    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],

    "machine learning": [
        "machine learning",
        "machine-learning"
    ],

    "deep learning": [
        "deep learning",
        "deep-learning"
    ],

    "natural language processing": [
        "natural language processing",
        "nlp"
    ],

    "computer vision": [
        "computer vision"
    ],

    "data analysis": [
        "data analysis",
        "data analytics"
    ],

    "data visualization": [
        "data visualization",
        "data visualisation"
    ],

    "power bi": [
        "power bi",
        "powerbi"
    ],

    "tableau": ["tableau"],

    "excel": [
        "excel",
        "microsoft excel"
    ],

    "git": ["git"],
    "github": ["github"],
    "docker": ["docker"],

    "kubernetes": [
        "kubernetes",
        "k8s"
    ],

    "aws": [
        "aws",
        "amazon web services"
    ],

    "azure": ["azure"],

    "gcp": [
        "gcp",
        "google cloud"
    ],

    "linux": ["linux"],

    "rest api": [
        "rest api",
        "restful api"
    ],

    "api": ["api"],

    "agile": ["agile"],
    "scrum": ["scrum"],
}


def normalize_text(text: str) -> str:
    return str(text).lower()


def find_skills(text: str) -> list[str]:
    normalized = normalize_text(text)

    found = []

    for skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            pattern = (
                r"(?<!\w)"
                + re.escape(alias.lower())
                + r"(?!\w)"
            )

            if re.search(
                pattern,
                normalized,
                flags=re.IGNORECASE
            ):
                found.append(skill)
                break

    return sorted(set(found))


def calculate_skill_match(
    resume_text: str,
    required_skills: list[str],
    preferred_skills: list[str]
):
    resume_skills = set(
        find_skills(resume_text)
    )

    required = {
        skill.lower().strip()
        for skill in required_skills
        if skill.strip()
    }

    preferred = {
        skill.lower().strip()
        for skill in preferred_skills
        if skill.strip()
    }

    matched_required = sorted(
        resume_skills.intersection(required)
    )

    missing_required = sorted(
        required.difference(resume_skills)
    )

    matched_preferred = sorted(
        resume_skills.intersection(preferred)
    )

    missing_preferred = sorted(
        preferred.difference(resume_skills)
    )

    required_score = (
        len(matched_required) / len(required)
        if required
        else 1.0
    )

    preferred_score = (
        len(matched_preferred) / len(preferred)
        if preferred
        else 1.0
    )

    return {
        "resume_skills": sorted(resume_skills),
        "matched_required": matched_required,
        "missing_required": missing_required,
        "matched_preferred": matched_preferred,
        "missing_preferred": missing_preferred,
        "required_score": required_score,
        "preferred_score": preferred_score,
    }
