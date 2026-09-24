# ResuMatch AI

## AI-Powered Resume Ranker

ResuMatch AI is an AI-assisted resume screening and candidate ranking application built with Python and Streamlit. It analyzes PDF resumes against a hiring profile and produces structured, explainable ranking signals for human review.

> Candidate ranking should support — not replace — human review.

## Features

- PDF resume text extraction with PyMuPDF
- spaCy NLP processing
- TF-IDF resume/job relevance
- Required and preferred skill matching
- Experience analysis
- Explainable weighted candidate scoring
- Candidate ranking
- Report generation
- Streamlit interface
- Sample job and resumes
- Automated scoring tests

## Scoring Model

| Component | Weight |
|---|---:|
| Resume / Job Relevance | 50% |
| Required Skills | 30% |
| Preferred Skills | 10% |
| Experience | 10% |
| **Total** | **100%** |

Final Score = 0.50 × Resume Relevance + 0.30 × Required Skill Match + 0.10 × Preferred Skill Match + 0.10 × Experience Match.

## Example Candidates

- Aarav Sharma — ML Engineer — 3 years
- Priya Verma — Data Analyst — 2 years
- Rahul Mehta — Software Developer — 1 year

Sample job: data/sample_jobs/machine_learning_intern.txt
Sample resumes: data/sample_resumes/

## Technology Stack

Python, Streamlit, spaCy, scikit-learn, PyMuPDF, pandas, NumPy, ReportLab, openpyxl, Plotly, Flask.

## Live Demo`r`n`r`nhttps://resumatch-ai12.streamlit.app/`r`n`r`n## Local Setup

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    streamlit run .\streamlit_app.py

Live Demo: https://resumatch-ai12.streamlit.app/

## Testing

Run: pytest -q
Tests are located in tests/test_scoring.py.

## Deployment

Repository: sadiqfaisal/resumatch-ai
Branch: main
Main file: streamlit_app.py
Dependency file: requirements.txt

## Responsible Use

ResuMatch AI is an assistive screening tool, not an autonomous hiring decision-maker. Human reviewers should verify extracted information and make final hiring decisions using appropriate human judgment.

## Future Improvements

Semantic embeddings, improved skill aliases, section-aware parsing, stronger experience extraction, candidate explanations, fairness monitoring, ranking evaluation, authentication, persistent storage, and production monitoring.

## License

This project is currently intended as an internship and portfolio project.

