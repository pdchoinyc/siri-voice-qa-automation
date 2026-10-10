from pathlib import Path

from src.speech_recognizer import SpeechRecognizer
from src.speech_evaluator import evaluate_transcription


def main():
    audio_path = Path("audio_samples/test_ko.m4a")

    if not audio_path.exists():
        print(f"Audio file not found: {audio_path}")
        return

    recognizer = SpeechRecognizer()

    result = recognizer.transcribe(
        str(audio_path),
        language="ko"
    )

    reference = "오늘 날씨 알려줘"

    metrics = evaluate_transcription(
        reference,
        result["text"]
    )

    print("Reference:", reference)
    print("Recognized:", result["text"])
    print("Language:", result["language"])
    print("WER:", round(metrics["wer"], 4))
    print("CER:", round(metrics["cer"], 4))


if __name__ == "__main__":
    main()