
# Test Strategy

## 1. Purpose

This document describes the quality assurance strategy for
the Siri Voice QA Automation portfolio project.

The objective is to demonstrate systematic testing of
multilingual voice assistant workflows, including functional
correctness, speech recognition quality, intent classification,
performance measurement, and regression detection.

This project is independent and does not test Apple's Siri.

## 2. Quality Objectives

The test strategy focuses on five quality dimensions:

1. Functional correctness
2. Multilingual consistency
3. Speech recognition accuracy
4. Performance stability
5. Test result traceability

The framework is designed to distinguish between verified,
failed, and unexecuted test areas.

## 3. Test Scope

### In Scope

- Rule-based intent classification
- Korean, English, and Japanese test inputs
- Positive and negative test scenarios
- Invalid and boundary input handling
- WER and CER evaluation
- Local speech-to-text inference
- Downstream intent validation
- Speech inference latency measurement
- Baseline-based performance regression
- Automated test reporting
- GitHub Actions continuous integration

### Out of Scope

- Testing proprietary Siri services
- Production NLU model evaluation
- Large-scale speech model benchmarking
- End-to-end testing on Apple devices
- Real-world population-level accuracy claims
- Production load and scalability testing

## 4. Test Levels and Types

| Test Type | Validation Objective | Execution |
|---|---|---|
| Functional | Verify expected intent classification | CI |
| Multilingual | Verify supported language inputs | CI |
| Negative | Validate invalid and unsupported inputs | CI |
| Boundary | Verify edge cases and input handling | CI |
| Evaluation Utility | Validate speech metric calculations | CI |
| Reporting | Verify report and dashboard generation | CI |
| Speech QA | Evaluate recorded speech samples | Local |
| Performance | Measure inference latency and RTF | Local |
| Regression | Compare latency with stored baselines | Local |

The standard CI test suite currently reports 51 passing tests.
Four additional tests are excluded from the default CI selection.

## 5. Functional Test Strategy

The intent classifier is tested against five categories:

- WEATHER
- TIMER
- ALARM
- UNKNOWN
- MULTIPLE_INTENTS

Test scenarios include:

- Valid utterances for supported intents
- Multiple language variants
- Unsupported or unrelated requests
- Ambiguous and overlapping intent keywords
- Empty and malformed inputs
- Boundary and invalid input types

Expected intent labels are compared against actual classifier
outputs using automated assertions.

## 6. Multilingual Test Strategy

The supported locales are:

| Locale | Language |
|---|---|
| ko-KR | Korean |
| en-US | English |
| ja-JP | Japanese |

The strategy evaluates both text-based intent behavior and
locally recorded speech samples.

Multilingual coverage is currently limited to a small,
controlled dataset. Passing these samples does not demonstrate
general language robustness.

## 7. Speech Recognition Test Strategy

The local speech pipeline uses Faster-Whisper with the
multilingual Whisper Tiny model.

### Quality Metrics

**Word Error Rate (WER)**

WER = (Substitutions + Deletions + Insertions) / Reference Words

**Character Error Rate (CER)**

CER = (Substitutions + Deletions + Insertions) / Reference Characters

Lower WER and CER values indicate fewer transcription errors.

Speech recognition outputs are also passed to the intent
classifier to identify downstream classification failures.

### Current Sample Coverage

The local evaluation includes three recorded utterances,
one each for Korean, English, and Japanese.

The observed WER and CER were zero for these three samples
in the documented local run.

These results are sample-specific and are not generalized
model accuracy estimates.

## 8. Performance Test Strategy

The performance benchmark evaluates speech inference using:

- One warm-up run
- Ten measured runs per sample
- Average inference latency
- P95 inference latency
- Minimum and maximum latency
- Latency standard deviation
- Real-Time Factor (RTF)

RTF is calculated as:

RTF = Inference Duration / Audio Duration

An RTF below 1 indicates inference faster than the audio
duration under the measured conditions.

### Performance Regression Criteria

Current latency measurements are compared with stored
baseline values.

The configured maximum allowed regression is 20%.

A metric is considered a regression failure when its
measured value exceeds the permitted baseline threshold.

A passing regression comparison does not imply that the
system meets a production latency service-level objective.

## 9. Negative and Data Validation Strategy

Negative testing covers invalid inputs and inconsistent
benchmark data.

Examples include:

- Unsupported or malformed intent inputs
- Missing benchmark records
- Invalid numeric measurements
- Inconsistent locale information
- Invalid baseline configuration

These tests help detect incorrect assumptions and
prevent misleading regression results.

## 10. Defect Investigation Strategy

When a test fails, the investigation process is:

1. Reproduce the failure.
2. Capture expected and actual outputs.
3. Identify the affected component.
4. Measure the impact on quality metrics.
5. Investigate plausible contributing factors.
6. Apply or evaluate a corrective action.
7. Re-run the affected tests.
8. Document remaining uncertainty.

### Example: Japanese Speech Recognition Error

Expected:

今日の天気を教えて

Observed:

今日の電気を教えて

The transcription error changed the meaning of a key word
and resulted in an UNKNOWN intent instead of WEATHER.

The case illustrates error propagation from speech
recognition to downstream intent classification.

## 11. CI/CD Test Execution

GitHub Actions runs the standard Pytest suite for pushes
and pull requests targeting the main branch.

The workflow produces:

- Pytest execution results
- JUnit XML
- pytest-html report
- Unified QA summary JSON
- HTML QA dashboard

CI does not execute local speech recordings or
performance benchmark inference.

When the relevant benchmark outputs are unavailable,
the unified report marks those sections as NOT_RUN.

This prevents unexecuted checks from being presented
as successful validations.

## 12. Entry and Exit Criteria

### Entry Criteria

- Required Python dependencies are installed.
- Test data and configuration are available.
- The intended test environment is configured.
- Local audio fixtures are available when running speech tests.

### Exit Criteria

For the standard CI suite:

- All selected automated tests complete successfully.
- No selected test reports a failure or error.
- Generated reports accurately reflect execution results.

For local speech and performance testing:

- Required audio samples are available.
- Quality metrics are successfully generated.
- Regression results are evaluated against configured baselines.
- Failures and limitations are documented.

## 13. Risks and Limitations

| Risk | Impact | Mitigation |
|---|---|---|
| Small speech dataset | Limited representativeness | Expand sample diversity |
| Rule-based NLU | Limited language understanding | Document test-target scope |
| Local hardware variation | Unstable latency comparison | Record environment details |
| Private audio fixtures | No speech inference in CI | Add non-sensitive fixtures |
| Japanese tokenization | WER interpretation limitations | Explore language-aware metrics |
| Static performance baseline | Potential baseline bias | Revalidate baselines independently |

## 14. Future Improvements

- Increase multilingual test coverage.
- Add background noise and accent variations.
- Introduce public or synthetic audio fixtures for CI.
- Evaluate different Whisper model sizes.
- Add environment-aware performance baselines.
- Improve defect reporting and test traceability.
- Track performance trends across benchmark runs.

## 15. Summary

This strategy demonstrates a risk-aware and measurable
approach to testing multilingual voice assistant workflows.

The emphasis is on functional validation, speech quality,
performance regression, negative testing, and transparent
reporting of executed and unexecuted checks.
