def classify_intent(text: str) -> str:
    text = text.lower().strip()

    if "weather" in text or "날씨" in text:
        return "WEATHER"

    if "timer" in text or "타이머" in text:
        return "TIMER"

    if "alarm" in text or "알람" in text:
        return "ALARM"

    return "UNKNOWN"