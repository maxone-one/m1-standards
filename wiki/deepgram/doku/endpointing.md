> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://developers.deepgram.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://developers.deepgram.com/_mcp/server.

# Endpointing

`endpointing` *string*.

&#x20;Pre-recorded

&#x20;Streaming:Nova

&#x20;All available languages

Deepgram’s Endpointing feature can be used for speech detection by monitoring incoming streaming audio and relies on a Voice Activity Detector (VAD), which monitors the incoming audio and triggers when a sufficiently long pause is detected.

Endpointing helps to detects sufficiently long pauses that are likely to represent an endpoint in speech. When an endpoint is detected the model assumes that no additional data will improve it's prediction of the endpoint.

The transcript results are then finalized for the process time range and the JSON response is returned with a `speech_final` parameter set to `true`.

You can customize the length of time used to detect whether a speaker has finished speaking by setting the `endpointing` parameter to an integer value.

Endpointing can be used with Deepgram's [Interim Results](/docs/interim-results/) feature. To compare and contrast these features, and to explore best practices for using them together, see [Using Endpointing and Interim Results with Live Streaming Audio](/docs/understand-endpointing-interim-results/).

## Enable Feature

Endpointing is enabled by default and set to 10 milliseconds. and will return transcripts after detecting 10 milliseconds of silence.

The period of silence required for endpointing may also be configured. When you call Deepgram’s API, add an `endpointing` parameter set to an integer by setting endpointing to an integer representing a millisecond value:

`endpointing=500`

This will wait until 500 milliseconds of silence has passed to finalize and return transcripts.

Endpointing may be disabled by setting `endpointing=false`. If endpointing is disabled, transcriptions will be returned at a cadence determined by Deepgram's chunking algorithms.

```python Python

# For more Python SDK migration guides, visit:
# https://github.com/deepgram/deepgram-python-sdk/tree/main/docs

   with client.listen.v1.connect(
            model="nova-3",
            language="en-US",
            # Apply smart formatting to the output
            smart_format=True,
            # Raw audio format details
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            # To get UtteranceEnd, the following must be set:
            interim_results=True,
            utterance_end_ms="1000",
            vad_events=True,
            # Time in milliseconds of silence to wait for before finalizing speech
            endpointing=300
   ) as connection:
```

```java Java
import com.deepgram.DeepgramClient;
import com.deepgram.resources.listen.v1.websocket.V1WebSocketClient;
import com.deepgram.resources.listen.v1.websocket.V1ConnectOptions;

DeepgramClient client = DeepgramClient.builder().build();
V1WebSocketClient wsClient = client.listen().v1().v1WebSocket();

V1ConnectOptions options = V1ConnectOptions.builder()
    .model("nova-3")
    .language("en-US")
    // Apply smart formatting to the output
    .smartFormat(true)
    // To get UtteranceEnd, the following must be set:
    .interimResults(true)
    .utteranceEndMs(1000)
    .vadEvents(true)
    // Time in milliseconds of silence to wait for before finalizing speech
    .endpointing(300)
    .build();

wsClient.connect(options).get(10, TimeUnit.SECONDS);
```

## Results

When enabled, the transcript for each received streaming response shows a key called `speech_final`.

```json JSON
{
  "channel_index":[
    0,
    1
  ],
  "duration":1.039875,
  "start":0.0,
  "is_final":false,
  "speech_final":true,
  "channel":{
    "alternatives":[
      {
        "transcript":"another big",
        "confidence":0.9600255,
        "words":[
          {
            "word":"another",
            "start":0.2971154,
            "end":0.7971154,
            "confidence":0.9588303
          },
          {
            "word":"big",
            "start":0.85173076,
            "end":1.039875,
            "confidence":0.9600255
          }
        ]
      }
    ]
  }
}
...
```

---