import re


INTENT_KEYWORDS = {
    "WEATHER": ["weather", "날씨", "天気"],
    "TIMER": ["timer", "타이머", "タイマー"],
    "ALARM": ["alarm", "알람", "アラーム"],
}


def classify_intent(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("Input must be a string")

    text = text.lower().strip()

    if not text:
        return "UNKNOWN"

    detected_intents = []

    for intent, keywords in INTENT_KEYWORDS.items():
        for keyword in keywords:

            # English keywords require word boundaries.
            if keyword.isascii():
                pattern = (
                    rf"(?<![a-z0-9])"
                    rf"{re.escape(keyword.lower())}"
                    rf"(?![a-z0-9])"
                )
                matched = re.search(pattern, text) is not None

            # Korean and Japanese keywords use substring matching.
            else:
                matched = keyword in text

            if matched:
                detected_intents.append(intent)
                break

    if len(detected_intents) > 1:
        return "MULTIPLE_INTENTS"

    if len(detected_intents) == 1:
        return detected_intents[0]

    return "UNKNOWN"