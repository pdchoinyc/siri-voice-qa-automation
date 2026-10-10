from faster_whisper import WhisperModel


class SpeechRecognizer:
    def __init__(self):
        self.model = WhisperModel(
            "tiny",
            device="cpu",
            compute_type="int8",
            cpu_threads=4
        )

    def transcribe(self, audio_path, language=None):
        segments, info = self.model.transcribe(
            audio_path,
            language=language,
            beam_size=5
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
        )

        return {
            "text": text.strip(),
            "language": info.language,
            "language_probability": info.language_probability
        }