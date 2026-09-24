import csv
from pathlib import Path


def create_csv_report(
    results: list[dict],
    report_path: str
) -> str:

    Path(report_path).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    fieldnames = [
        "Rank",
        "Candidate",
        "Resume",
        "Final Score",
        "TF-IDF Similarity",
        "Required Skills",
        "Preferred Skills",
        "Experience Score",
        "Experience Years",
        "Matched Required",
        "Missing Required",
        "Matched Preferred",
        "Missing Preferred",
    ]

    with open(
        report_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for result in results:

            writer.writerow({
                "Rank": result["rank"],
                "Candidate": result[
                    "candidate_name"
                ],
                "Resume": result[
                    "filename"
                ],
                "Final Score": result[
                    "final_score"
                ],
                "TF-IDF Similarity": result[
                    "tfidf_score"
                ],
                "Required Skills": ", ".join(
                    result["matched_required"]
                ),
                "Preferred Skills": ", ".join(
                    result["matched_preferred"]
                ),
                "Experience Score": result[
                    "experience_score"
                ],
                "Experience Years": result[
                    "experience_years"
                ],
                "Matched Required": ", ".join(
                    result["matched_required"]
                ),
                "Missing Required": ", ".join(
                    result["missing_required"]
                ),
                "Matched Preferred": ", ".join(
                    result["matched_preferred"]
                ),
                "Missing Preferred": ", ".join(
                    result["missing_preferred"]
                ),
            })

    return report_path
