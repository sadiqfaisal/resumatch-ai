from pathlib import Path

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


BASE_DIR = Path(__file__).resolve().parent

RESUME_DIR = (
    BASE_DIR
    / "data"
    / "sample_resumes"
)

JOB_DIR = (
    BASE_DIR
    / "data"
    / "sample_jobs"
)


RESUME_DIR.mkdir(
    parents=True,
    exist_ok=True
)

JOB_DIR.mkdir(
    parents=True,
    exist_ok=True
)


resumes = {

"Aarav_Sharma.pdf": """
AARAV SHARMA

Machine Learning Engineer

Professional Summary

Machine Learning Engineer with 3 years of experience
building machine learning and data analysis solutions.
Experienced in Python, SQL, Pandas, NumPy, Scikit-learn,
Flask, Git, Docker, AWS, REST API development and
data processing.

Technical Skills

Python
SQL
Machine Learning
Pandas
NumPy
Scikit-learn
Git
Flask
Docker
AWS
REST API
Data Analysis

Experience

Machine Learning Engineer
3 years of experience

Developed Python machine learning pipelines.
Prepared and analyzed structured datasets.
Built predictive models using Scikit-learn.
Created REST APIs using Flask.
Worked with SQL databases.
Containerized applications using Docker.
Used AWS for deployment and cloud workflows.

Education

Bachelor of Technology in Computer Science
""",

"Priya_Verma.pdf": """
PRIYA VERMA

Data Analyst

Professional Summary

Data Analyst with 2 years of experience working with
business datasets and analytical reporting.

Technical Skills

Python
SQL
Excel
Power BI
Tableau
Pandas
NumPy
Data Analysis
Git

Experience

Data Analyst
2 years of experience

Analyzed business datasets using Python and Pandas.
Created dashboards using Power BI and Tableau.
Performed SQL queries and reporting.
Used Excel for data cleaning and analysis.
Collaborated with business stakeholders.

Education

Bachelor of Science in Statistics
""",

"Rahul_Mehta.pdf": """
RAHUL MEHTA

Software Developer

Professional Summary

Software Developer with 1 year of experience developing
web applications and backend services.

Technical Skills

JavaScript
React
Node.js
MongoDB
HTML
CSS
Git
REST API

Experience

Software Developer
1 year of experience

Developed web applications using JavaScript and React.
Created backend services using Node.js.
Worked with MongoDB databases.
Built REST API integrations.
Used Git for source control.

Education

Bachelor of Engineering in Information Technology
"""
}


styles = getSampleStyleSheet()


for filename, content in resumes.items():

    output_path = (
        RESUME_DIR / filename
    )

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=LETTER,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )

    story = []

    for line in content.strip().splitlines():

        line = line.strip()

        if not line:
            story.append(
                Spacer(1, 8)
            )

        elif line.isupper():
            story.append(
                Paragraph(
                    f"<b>{line}</b>",
                    styles["Heading2"]
                )
            )

        else:
            story.append(
                Paragraph(
                    line,
                    styles["BodyText"]
                )
            )

    document.build(story)


job_description = """
Machine Learning Intern

We are looking for a Machine Learning Intern to support
development of machine learning and data analysis solutions.

Responsibilities:

Build and evaluate machine learning models.

Prepare and analyze datasets.

Develop Python-based data processing workflows.

Work with SQL databases.

Collaborate with engineers and data scientists.

Create APIs and analytical tools.
""".strip()


(
    JOB_DIR
    / "machine_learning_intern.txt"
).write_text(
    job_description,
    encoding="utf-8"
)


print("Sample resumes created:")
for filename in resumes:
    print(" -", filename)

print(
    "Sample job description created."
)
