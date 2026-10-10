# Siri Voice QA Automation

A Python-based multilingual voice quality assurance automation project designed to demonstrate testing methodologies relevant to AI voice assistants, speech recognition, and natural language understanding (NLU).

The project combines automated intent classification tests, speech-to-text evaluation, multilingual test coverage, edge case validation, and continuous integration.

> **Disclaimer:** This is an independent QA portfolio project. It does not test Apple's proprietary Siri models or services.

## 1. Project Objectives

- Design and implement automated QA tests for voice assistant workflows.
- Validate intent classification across English, Korean, and Japanese.
- Evaluate speech recognition output using Word Error Rate (WER) and Character Error Rate (CER).
- Identify recognition errors and analyze their downstream impact on intent classification.
- Automate regression testing with Pytest and GitHub Actions.

## 2. Technology Stack

| Category | Technology |
|---|---|
| Programming | Python 3.13 |
| Test Framework | Pytest |
| Speech Recognition | Faster-Whisper (Whisper Tiny) |
| Speech Evaluation | JiWER |
| Intent Classification | Rule-based keyword classifier |
| Reporting | pytest-html, CSV |
| Continuous Integration | GitHub Actions |
| Version Control | Git, GitHub |

## 3. Test Architecture

The project supports two complementary testing workflows.

**Intent Classification Testing**

Text Input → Intent Classifier → Predicted Intent → Assertion → Pytest Report

**Speech Recognition Testing**

Audio Input → Whisper STT → Transcription → WER/CER Evaluation → Intent Classification → CSV Report

The intent classifier is a lightweight rule-based implementation used as a test target, not a production NLU model.

## 4. Test Coverage

The automated Pytest suite contains 40 tests covering:

- Intent classification for WEATHER, TIMER, ALARM, UNKNOWN, and MULTIPLE_INTENTS.
- English, Korean, and Japanese language inputs.
- Negative testing and unsupported requests.
- Boundary conditions and invalid input types.
- Text normalization and WER/CER evaluation.

A separate speech QA runner evaluates three recorded utterances, one per language.

## 5. Multilingual Speech QA Results

A local test run using Whisper Tiny produced the following results:

| Locale | WER | CER | Predicted Intent | Result |
|---|---:|---:|---|---|
| ko-KR | 0.00 | 0.00 | WEATHER | PASS |
| en-US | 0.00 | 0.00 | WEATHER | PASS |
| ja-JP | 0.00 | 0.00 | WEATHER | PASS |

These results represent a small, controlled sample set and should not be interpreted as general model accuracy.

Speech tests are currently executed locally and are not part of the GitHub Actions workflow.

## 6. QA Case Study: Japanese Speech Recognition Error

**Issue:** Incorrect recognition of a Japanese weather-related utterance.

**Expected transcription:**

今日の天気を教えて

**Observed transcription:**

今日の電気を教えて

The recognition error changed the meaning of the key word from "weather" to "electricity."

**Impact**

- Character Error Rate: 11.11%
- Predicted intent: UNKNOWN
- Expected intent: WEATHER
- Test result: FAIL

**Investigation**

1. Reproduced the error using the original Japanese audio recording.
2. Increased Whisper beam size from 1 to 5.
3. Observed that the same recognition error persisted.
4. Re-recorded the Japanese utterance under the same model configuration.
5. Verified that the new recording produced the expected transcription and WEATHER intent.

**Outcome**

The re-recorded sample passed with WER and CER equal to 0. The observations suggest that input audio characteristics may have contributed to the original failure, but do not establish a definitive root cause.

This case demonstrates how speech recognition errors can propagate into downstream intent classification.

## 7. Running Automated Tests

Create and activate a virtual environment:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run the Pytest suite:

```powershell
python -m pytest -v
```

Run the multilingual speech QA evaluation:

```powershell
python run_multilingual_speech_test.py
```

The speech evaluation requires local audio recordings referenced by `data/speech_test_data.json`.

Audio recordings are excluded from version control for privacy reasons.

## 8. Continuous Integration

GitHub Actions automatically runs the Pytest regression suite on pushes and pull requests targeting the main branch.

The workflow installs project dependencies, executes the tests, and uploads the generated HTML test report.

The multilingual audio evaluation is currently a separate local workflow.

## 9. Future Improvements

- Expand multilingual speech test datasets.
- Evaluate background noise and accent variations.
- Compare multiple Whisper model sizes.
- Improve Japanese WER measurement with language-aware tokenization.
- Add configurable accuracy thresholds and structured defect reports.
- Introduce audio-based regression testing in CI using appropriate non-sensitive test fixtures.

## 10. Project Scope

This project demonstrates independent QA engineering practices for AI voice assistant workflows, including test design, multilingual validation, automation, defect investigation, and CI integration.

It is not affiliated with or endorsed by Apple.