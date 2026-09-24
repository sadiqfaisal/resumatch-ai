from pathlib import Path
import pymupdf


def extract_text_from_pdf(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {file_path}"
        )

    document = pymupdf.open(file_path)
    pages = []

    try:
        for page in document:
            text = page.get_text("text")

            if text:
                pages.append(text)

    finally:
        document.close()

    return "\n".join(pages).strip()


def extract_text_from_bytes(file_bytes: bytes) -> str:
    document = pymupdf.open(
        stream=file_bytes,
        filetype="pdf"
    )

    pages = []

    try:
        for page in document:
            text = page.get_text("text")

            if text:
                pages.append(text)

    finally:
        document.close()

    return "\n".join(pages).strip()
