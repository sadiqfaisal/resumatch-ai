import re
import spacy


def load_nlp():
    try:
        return spacy.load(
            "en_core_web_sm",
            disable=["parser", "ner"]
        )
    except Exception:
        # Deployment-safe fallback.
        return spacy.blank("en")


nlp = load_nlp()


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def preprocess_text(text: str) -> str:
    text = clean_text(text)

    if not text:
        return ""

    doc = nlp(text)

    tokens = []

    for token in doc:
        if token.is_space or token.is_punct:
            continue

        value = token.lemma_.lower().strip()

        if not value or value == "-pron-":
            value = token.text.lower().strip()

        if len(value) > 1:
            tokens.append(value)

    return " ".join(tokens)


def extract_keywords(text: str, limit: int = 25):
    processed = preprocess_text(text)

    if not processed:
        return []

    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9+#.-]*\b", processed)

    stopwords = {
        "the", "and", "for", "with", "from", "this", "that",
        "are", "was", "were", "will", "have", "has", "had",
        "you", "your", "our", "their", "they", "them", "into",
        "about", "using", "use", "work", "working", "candidate",
        "role", "team", "experience", "years", "year"
    }

    frequency = {}

    for word in words:
        word = word.lower()

        if word in stopwords:
            continue

        if len(word) < 2:
            continue

        frequency[word] = frequency.get(word, 0) + 1

    ranked = sorted(
        frequency.items(),
        key=lambda item: (-item[1], item[0])
    )

    return [word for word, _ in ranked[:limit]]
