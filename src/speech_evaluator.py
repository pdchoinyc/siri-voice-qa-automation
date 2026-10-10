import unicodedata

from jiwer import wer, cer


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.lower()

    # Remove punctuation.
    text = "".join(
        char for char in text
        if not unicodedata.category(char).startswith("P")
    )

    # Normalize whitespace.
    return " ".join(text.split())


def evaluate_transcription(reference, hypothesis):
    normalized_reference = normalize_text(reference)
    normalized_hypothesis = normalize_text(hypothesis)

    return {
        "wer": wer(normalized_reference, normalized_hypothesis),
        "cer": cer(normalized_reference, normalized_hypothesis)
    }