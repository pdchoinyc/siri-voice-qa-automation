def classify_intent(text: str) -> str:
    text = text.lower().strip()

    intent_keywords = {
        "WEATHER": ["weather", "날씨", "天気"],
        "TIMER": ["timer", "타이머", "タイマー"],
        "ALARM": ["alarm", "알람", "アラーム"],
    }

    for intent, keywords in intent_keywords.items():
        if any(keyword.lower() in text for keyword in keywords):
            return intent

    return "UNKNOWN"