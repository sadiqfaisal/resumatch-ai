from pathlib import Path
import re
import uuid

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)

from .config import (
    ALLOWED_EXTENSIONS,
    MAX_CONTENT_LENGTH,
    REPORT_FOLDER,
    SECRET_KEY,
    UPLOAD_FOLDER,
)

from .pdf_parser import extract_text_from_bytes
from .reporting import create_csv_report
from .scoring import score_candidates


app = Flask(__name__)

app.secret_key = SECRET_KEY

app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["REPORT_FOLDER"] = REPORT_FOLDER


Path(UPLOAD_FOLDER).mkdir(
    parents=True,
    exist_ok=True
)

Path(REPORT_FOLDER).mkdir(
    parents=True,
    exist_ok=True
)


def allowed_file(filename: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(
            ".",
            1
        )[1].lower() in ALLOWED_EXTENSIONS
    )


def clean_candidate_name(filename: str) -> str:
    stem = Path(filename).stem

    stem = re.sub(
        r"[_\-]+",
        " ",
        stem
    )

    stem = re.sub(
        r"\s+",
        " ",
        stem
    )

    return stem.strip().title()


def parse_skill_input(value: str) -> list[str]:
    return [
        item.strip()
        for item in str(value).split(",")
        if item.strip()
    ]


@app.route("/")
def index():
    return render_template(
        "index.html"
    )


@app.route(
    "/rank",
    methods=["POST"]
)
def rank_candidates():

    job_description = request.form.get(
        "job_description",
        ""
    ).strip()

    required_skills = parse_skill_input(
        request.form.get(
            "required_skills",
            ""
        )
    )

    preferred_skills = parse_skill_input(
        request.form.get(
            "preferred_skills",
            ""
        )
    )

    required_years_raw = request.form.get(
        "required_years",
        "0"
    ).strip()

    try:
        required_years = float(
            required_years_raw or 0
        )
    except ValueError:
        required_years = 0

    files = request.files.getlist(
        "resumes"
    )

    if not job_description:
        flash(
            "Please provide a job description.",
            "danger"
        )

        return redirect(
            url_for("index")
        )

    valid_files = [
        file
        for file in files
        if file and file.filename
    ]

    if not valid_files:
        flash(
            "Please upload at least one PDF resume.",
            "danger"
        )

        return redirect(
            url_for("index")
        )

    resumes = []

    for file in valid_files:

        if not allowed_file(file.filename):
            flash(
                f"Skipped unsupported file: {file.filename}",
                "warning"
            )
            continue

        try:
            file_bytes = file.read()

            text = extract_text_from_bytes(
                file_bytes
            )

            if not text:
                flash(
                    f"No readable text found in {file.filename}.",
                    "warning"
                )
                continue

            unique_name = (
                f"{uuid.uuid4().hex}_"
                f"{Path(file.filename).name}"
            )

            saved_path = (
                Path(UPLOAD_FOLDER)
                / unique_name
            )

            saved_path.write_bytes(
                file_bytes
            )

            resumes.append({
                "filename": file.filename,
                "candidate_name": clean_candidate_name(
                    file.filename
                ),
                "text": text,
            })

        except Exception as exc:
            flash(
                f"Could not process {file.filename}: {exc}",
                "danger"
            )

    if not resumes:
        flash(
            "No valid resumes could be processed.",
            "danger"
        )

        return redirect(
            url_for("index")
        )

    results = score_candidates(
        job_description=job_description,
        resumes=resumes,
        required_skills=required_skills,
        preferred_skills=preferred_skills,
        required_years=required_years,
    )

    report_name = (
        f"resume_ranking_"
        f"{uuid.uuid4().hex[:10]}.csv"
    )

    report_path = (
        Path(REPORT_FOLDER)
        / report_name
    )

    create_csv_report(
        results,
        str(report_path)
    )

    session["results"] = results
    session["report_path"] = str(
        report_path
    )

    return render_template(
        "results.html",
        results=results,
        required_skills=required_skills,
        preferred_skills=preferred_skills,
        required_years=required_years,
    )


@app.route(
    "/candidate/<int:rank>"
)
def candidate_detail(rank):

    results = session.get(
        "results",
        []
    )

    candidate = next(
        (
            item
            for item in results
            if item.get("rank") == rank
        ),
        None
    )

    if candidate is None:
        flash(
            "Candidate information is no longer available.",
            "warning"
        )

        return redirect(
            url_for("index")
        )

    return render_template(
        "candidate.html",
        candidate=candidate
    )


@app.route(
    "/download-report"
)
def download_report():

    report_path = session.get(
        "report_path"
    )

    if not report_path:
        flash(
            "No report is available.",
            "warning"
        )

        return redirect(
            url_for("index")
        )

    path = Path(report_path)

    if not path.exists():
        flash(
            "The report file could not be found.",
            "danger"
        )

        return redirect(
            url_for("index")
        )

    return send_file(
        path,
        as_attachment=True,
        download_name="resume_ranking_report.csv",
        mimetype="text/csv",
    )


@app.errorhandler(413)
def request_entity_too_large(error):
    flash(
        "Upload is too large. Maximum allowed size is 16 MB.",
        "danger"
    )

    return redirect(
        url_for("index")
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )
