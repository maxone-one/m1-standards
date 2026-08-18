> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://developers.deepgram.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://developers.deepgram.com/_mcp/server.

# Compare Flux to Nova-3

# Feature Matrix Comparison

It's important to understand the differences between [Flux](/docs/models-languages-overview#flux) and [Nova-3](/docs/models-languages-overview#nova-3) so you can choose the right model for your use case. Below is a feature matrix comparison to help you understand the differences.

## Use Cases

| Feature                 | Flux | Nova-3 |
| ----------------------- | ---- | ------ |
| Voice Agents            | ✅    | ✅      |
| IVR Systems             | ✅    | ✅      |
| Agent Assist            | ✅    | ✅      |
| Real-time Transcription | ✅    | ✅      |
| Meeting Transcription   | 🚫   | ✅      |
| Event Captioning        | 🚫   | ✅      |
| Pre-recorded Audio      | 🚫   | ✅      |
| Call Analytics          | 🚫   | ✅      |

## Language Support

| Feature                     | Flux                                                                         | Nova-3                                                           |
| --------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| English                     | ✅                                                                            | ✅                                                                |
| Multilingual (10 languages) | ✅ `flux-general-multi` ([Language Prompting](/docs/flux/language-prompting)) | ✅ [See language support](/docs/models-languages-overview#nova-3) |
| 54 languages                | 🚫                                                                           | ✅                                                                |
| Language control            | `language_hint` parameter                                                    | `language` parameter                                             |
| Code-switching              | ✅ Native with `flux-general-multi`                                           | ✅ With `language=multi`                                          |

## Technical Details

| Feature                  | Flux         | Nova-3       |
| ------------------------ | ------------ | ------------ |
| Self-hosted Availability | ✅            | ✅            |
| Endpoint                 | `/v2/listen` | `/v1/listen` |

## Conversation Features

| Feature           | Flux | Nova-3 |
| ----------------- | ---- | ------ |
| Start of Turn     | ✅    | 🚫     |
| Speech Resumed    | ✅    | 🚫     |
| End of Turn       | ✅    | 🚫     |
| Eager End of Turn | ✅    | 🚫     |

## Transcription Features

| Feature                  | Flux                     | Nova-3 |
| ------------------------ | ------------------------ | ------ |
| Word Times               | ✅                        | ✅      |
| Smart Formatting         | 🚫                       | ✅      |
| Numerals                 | ✅                        | ✅      |
| Speaker Diarization      | 🚫                       | ✅      |
| Filler Words             | ✅ Transcribed by default | 🚫     |
| Profanity Filtering      | 🚫                       | ✅      |
| Redaction                | ✅ Numbers only           | ✅      |
| Find and Replace         | 🚫                       | ✅      |
| Keyterm Prompting        | ✅                        | ✅      |
| Search                   | 🚫                       | ✅      |
| Turn-based Transcription | ✅                        | 🚫     |

## Connection Management

| Feature                     | Flux                                            | Nova-3          |
| --------------------------- | ----------------------------------------------- | --------------- |
| Endpointing + Utterance End | ✅ (Replaced by model integrated turn detection) | ✅               |
| Interim Results             | ✅ (Replaced by Update Messages)                 | ✅               |
| Keep Alive                  | ✅ (Replaced by pings, 60s timeout)              | ✅ (12s timeout) |