import os


BASE_DIR = os.path.abspath(
    os.path.dirname(os.path.dirname(__file__))
)

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
REPORT_FOLDER = os.path.join(BASE_DIR, "reports")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "outputs")

ALLOWED_EXTENSIONS = {"pdf"}

MAX_CONTENT_LENGTH = 16 * 1024 * 1024

TFIDF_WEIGHT = 0.50
REQUIRED_SKILL_WEIGHT = 0.30
PREFERRED_SKILL_WEIGHT = 0.10
EXPERIENCE_WEIGHT = 0.10

TOP_N = 10

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "ai-resume-ranker-development-key"
)
