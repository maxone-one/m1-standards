LiveKit docs › Build Agents › Logic & Structure › Tool definition & use › Async tools

---

# Async tools

> Handle long-running tools so agents can keep talking.

## Overview

Tools that take more than a few seconds block the conversation until they return. The agent stops talking, the user hears silence, and a regular tool can't send progress updates, be cancelled, or stop the LLM from calling the same tool twice.

Use async tools for anything that takes more than a few seconds, such as booking a flight, running a web search, or processing a document.

In Node.js, you define a normal `llm.tool(...)`. The tool becomes non-blocking the first time its `execute` function calls `await ctx.update(...)`. Forward the provided `abortSignal` to long-running work so interruptions and cancellation can stop it promptly.

## Updating the user

Use `ctx.update(message)` to send progress to the user while the tool keeps running. It adds a status to the chat context, the LLM reads it, voices something natural to the user, and the conversation continues. Use this for information the LLM should know about, such as a partial result or a phase change.

`RunContext` also provides filler speech to play audio directly through `session.say()`, bypassing the LLM. Use this for filler like "hang on a sec" or "still working on it" during work the LLM doesn't need to track. In Python this is `ctx.with_filler(...)`; in Node.js this is `ctx.filler(...)`.

### Progress updates

Define a regular function tool. Inside, call `ctx.update(message)` whenever you want to share progress, and `return` the final result when the tool is done:

**Python**:

```python
from livekit.agents import Agent, RunContext, function_tool


class TravelAgent(Agent):
    def __init__(self):
        super().__init__(instructions="You are a travel assistant.")

    @function_tool()
    async def book_flight(
        self, ctx: RunContext, origin: str, destination: str, date: str
    ) -> str:
        """Book a flight for the user.

        Args:
            origin: Departure city or airport code.
            destination: Arrival city or airport code.
            date: Travel date (YYYY-MM-DD).
        """
        await ctx.update(f"Searching flights from {origin} to {destination} on {date}.")
        # agent says: "Sure, let me look up flights from New York to Tokyo on April 15th."

        flights = await search_flights(origin, destination, date)
        await ctx.update(f"Found {len(flights)} options. Booking the best one now.")
        # agent says: "I found 3 options. Booking the best one for you now."

        booking = await confirm_booking(flights[0])
        return f"Booked! Confirmation number: {booking.id}"
        # agent says: "All set. Your booking confirmation number is FL-847293."

```

---

**Node.js**:

```typescript
import { llm } from '@livekit/agents';
import { z } from 'zod';

const bookFlight = llm.tool({
  name: 'bookFlight',
  description: 'Book a flight for the user.',
  parameters: z.object({
    origin: z.string().describe('Departure city or airport code.'),
    destination: z.string().describe('Arrival city or airport code.'),
    date: z.string().describe('Travel date (YYYY-MM-DD).'),
  }),
  execute: async ({ origin, destination, date }, { ctx, abortSignal }) => {
    await ctx.update(`Searching flights from ${origin} to ${destination} on ${date}.`);
    // agent says: "Sure, let me look up flights from New York to Tokyo on April 15th."

    const flights = await searchFlights(origin, destination, date, { signal: abortSignal });
    await ctx.update(`Found ${flights.length} options. Booking the best one now.`);
    // agent says: "I found 3 options. Booking the best one for you now."

    const booking = await confirmBooking(flights[0], { signal: abortSignal });
    return `Booked! Confirmation number: ${booking.id}`;
    // agent says: "All set. Your booking confirmation number is FL-847293."
  },
});

```

The agent waits for the first `ctx.update()` from each tool that calls it, so the user hears acknowledgement immediately. Tools that never call `ctx.update()` behave like regular synchronous tools. Later updates are added to the agent's chat context as they arrive, and the agent generates a new reply once it's idle.

### Filler speech

Open a filler scope around a long-running operation, and the filler plays once the session has been continuously idle for `delay` seconds. Fillers only play during quiet pauses, so they don't talk over the user or pile up behind other agent speech.

**Python**:

```python
from livekit.agents import Agent, RunContext, function_tool


class TravelAgent(Agent):
    def __init__(self):
        super().__init__(instructions="You are a travel assistant.")

    @function_tool()
    async def book_flight(
        self, ctx: RunContext, origin: str, destination: str, date: str
    ) -> str:
        """Book a flight."""
        # Plays "Still searching..." once the session has been idle for 5 seconds.
        async with ctx.with_filler("Still searching, hang on a sec.", delay=5):
            return await book_flight_api(origin, destination, date)

```

---

**Node.js**:

```typescript
import { llm } from '@livekit/agents';
import { z } from 'zod';

const bookFlight = llm.tool({
  name: 'bookFlight',
  description: 'Book a flight.',
  parameters: z.object({
    origin: z.string(),
    destination: z.string(),
    date: z.string(),
  }),
  execute: async ({ origin, destination, date }, { ctx, abortSignal }) => {
    // Plays "Still searching..." once the session has been idle for 5 seconds.
    return await ctx.filler(
      'Still searching, hang on a sec.',
      { delay: 5000, signal: abortSignal },
      () => bookFlightApi(origin, destination, date, { signal: abortSignal }),
    );
  },
});

```

The following parameters are available on `with_filler` (Python) or `filler` (Node.js):

- **`source`** _(str | Callable)_: The filler to play. Pass a string for a fixed line, or a callable that receives the iteration count. A callable returning `None` (Python) or `null` / `undefined` (Node.js) skips that round and retries on the next interval. The step counter only advances when audio plays, so a series of empty returns doesn't count against `max_steps` / `maxSteps`.

- **`delay`** _(float)_ (optional) - Default: `0`: Continuous session-idle required before each play. Python uses seconds. Node.js uses milliseconds.

- **`interval`** _(float | None)_ (optional) - Default: `None`: Time between plays. Python uses seconds. Node.js uses milliseconds. `None` / omitted plays at most once.

- **`max_steps`** _(int | None)_ (optional) - Default: `None`: Maximum number of times the filler plays. Python uses `max_steps`; Node.js uses `maxSteps`. `None` means no limit.

- **`signal`** _(AbortSignal)_ (optional): Available in:
- [x] Node.js
- [ ] Python

Optional external cancellation signal for the filler scheduler.

### Combining both

Most long-running tools use both channels: `ctx.update()` for key events (start, phase change, final result) and filler speech for the gaps between them. The following example uses both channels in a single tool:

**Python**:

```python
from livekit.agents import Agent, RunContext, function_tool


class TravelAgent(Agent):
    def __init__(self):
        super().__init__(instructions="You are a travel assistant.")

    @function_tool()
    async def book_flight(
        self, ctx: RunContext, origin: str, destination: str, date: str
    ) -> str:
        """Book a flight."""
        # One real update. The LLM voices a natural intro to the user.
        await ctx.update(
            f"Searching flights from {origin} to {destination} on {date}. "
            "This will take a couple of minutes."
        )

        # Phase 1: searching. Single acoustic filler if the user stays quiet for 5s.
        async with ctx.with_filler("Still searching, hang on a sec.", delay=5):
            flights = await search_flights(origin, destination, date)

        # Phase 2: confirming. Rotating fillers, up to 3 plays with 10s between them.
        followups = [
            "Almost there, just confirming.",
            "Still working on it, won't be long.",
            "Hang tight, almost done.",
        ]
        async with ctx.with_filler(
            lambda step: followups[step], delay=5, interval=10, max_steps=len(followups)
        ):
            booking = await confirm_booking(flights[0])

        # The final return is voiced as a follow-up reply when the agent is
        # next idle. No extra ctx.update() needed.
        return f"Booked! Confirmation number: {booking.id}"

```

---

**Node.js**:

```typescript
const bookFlight = llm.tool({
  name: 'bookFlight',
  description: 'Book a flight.',
  parameters: z.object({
    origin: z.string(),
    destination: z.string(),
    date: z.string(),
  }),
  execute: async ({ origin, destination, date }, { ctx, abortSignal }) => {
    await ctx.update(
      `Searching flights from ${origin} to ${destination} on ${date}. ` +
        'This will take a couple of minutes.',
    );

    const flights = await ctx.filler(
      'Still searching, hang on a sec.',
      { delay: 5000, signal: abortSignal },
      () => searchFlights(origin, destination, date, { signal: abortSignal }),
    );

    const followups = [
      'Almost there, just confirming.',
      "Still working on it, won't be long.",
      'Hang tight, almost done.',
    ];
    const booking = await ctx.filler(
      (step) => followups[step],
      { delay: 5000, interval: 10000, maxSteps: followups.length, signal: abortSignal },
      () => confirmBooking(flights[0], { signal: abortSignal }),
    );

    return `Booked! Confirmation number: ${booking.id}`;
  },
});

```

The two channels stay separate. `ctx.update()` adds to the chat context (the LLM reads it on its next turn). `ctx.with_filler()` / `ctx.filler()` plays audio directly without going through the chat context. The LLM keeps full context for the events that matter, and the user keeps hearing the agent during long operations.

## Pausing for user input

Sometimes a background tool needs to talk to the user mid-run before it can finish, such as collecting a missing detail, confirming a decision, or running a [prebuilt task](https://docs.livekit.io/agents/prebuilt/tasks.md) like `GetEmailTask`.

Wrap this interactive work in a `ctx.foreground()` block. It first plays any reply the tool has already queued, waits for the session to be idle, then prevents other agent speech for the duration of the block. This keeps the exchange clean and matches what the user hears to the order of your code.

**Python**:

```python
from livekit.agents import Agent, RunContext, function_tool
from livekit.agents.beta.workflows import GetEmailTask


class TravelAgent(Agent):
    def __init__(self):
        super().__init__(instructions="You are a travel assistant.")
        self._user_email: str | None = None

    @function_tool()
    async def book_flight(
        self, ctx: RunContext, origin: str, destination: str, date: str
    ) -> str:
        """Book a flight."""
        await ctx.update(
            f"Searching flights from {origin} to {destination} on {date}. "
            "This will take a couple of minutes."
        )
        flights = await search_flights(origin, destination, date)

        # Collect the email before confirming. foreground() ensures the
        # email task doesn't collide with the agent's other speech.
        if self._user_email is None:
            async with ctx.foreground():
                result = await GetEmailTask(
                    chat_ctx=self.chat_ctx,
                    extra_instructions="Tell the user you need their email to confirm the booking.",
                )
            self._user_email = result.email_address

        booking = await confirm_booking(flights[0], email=self._user_email)
        return f"Booked! Confirmation number: {booking.id}"

```

---

**Node.js**:

Node.js has no prebuilt email task, so build the interactive step with `AgentTask` and run it inside the `foreground()` callback:

```typescript
import { llm, voice } from '@livekit/agents';
import { z } from 'zod';

let userEmail: string | null = null;

function createEmailTask(): voice.AgentTask<{ emailAddress: string }> {
  const task = voice.AgentTask.create<{ emailAddress: string }>({
    instructions:
      'Collect the user email address to confirm the booking. ' +
      'As soon as you have it, call saveEmail.',
    tools: [
      llm.tool({
        name: 'saveEmail',
        description: 'Save the user email address.',
        parameters: z.object({
          emailAddress: z.string().describe('The user email address.'),
        }),
        execute: async ({ emailAddress }) => {
          task.complete({ emailAddress });
          return `Saved email address ${emailAddress}.`;
        },
      }),
    ],
    onEnter: (ctx) => {
      ctx.session.generateReply({
        instructions: 'Ask the user for their email address in one short sentence, then call saveEmail.',
      });
    },
  });
  return task;
}

const bookFlight = llm.tool({
  name: 'bookFlight',
  description: 'Book a flight.',
  parameters: z.object({
    origin: z.string(),
    destination: z.string(),
    date: z.string(),
  }),
  execute: async ({ origin, destination, date }, { ctx }) => {
    await ctx.update(
      `Searching flights from ${origin} to ${destination} on ${date}. ` +
        'This will take a couple of minutes.',
    );
    const flights = await searchFlights(origin, destination, date);

    // Collect the email before confirming. foreground() ensures the
    // email task doesn't collide with the agent's other speech.
    if (!userEmail) {
      const email = await ctx.foreground(async () => {
        ctx.session.say('I need your email to confirm the booking.');
        return createEmailTask().run();
      });
      userEmail = email.emailAddress;
    }

    const booking = await confirmBooking(flights[0], userEmail);
    return `Booked! Confirmation number: ${booking.id}`;
  },
});

```

Use `ctx.foreground()` to wrap any interactive step inside a long-running tool: an `await AgentTask()`, a direct `session.say()`, or a group of calls that must run together without a reply landing between them.

## Cancellation

By default, async tools finish what they're doing regardless of what the user does. To let the LLM cancel a running tool, opt in with the `CANCELLABLE` flag:

**Python**:

```python
from livekit.agents import RunContext, function_tool
from livekit.agents.llm import ToolFlag


@function_tool(flags=ToolFlag.CANCELLABLE)
async def book_flight(ctx: RunContext, origin: str, destination: str, date: str) -> str:
    return ""  # implementation

```

---

**Node.js**:

```typescript
const bookFlight = llm.tool({
  name: 'bookFlight',
  description: 'Book a flight for the user.',
  flags: llm.ToolFlag.CANCELLABLE,
  parameters: z.object({
    origin: z.string(),
    destination: z.string(),
    date: z.string(),
  }),
  execute: async ({ origin, destination, date }, { abortSignal }) => {
    return await bookFlightApi(origin, destination, date, { signal: abortSignal });
  },
});

```

When any cancellable tool is registered, two companion tools are automatically exposed to the LLM:

- `get_running_tasks()` / `lk_agents_get_running_tasks` returns the cancellable calls that are currently running.
- `cancel_task(call_id)` / `lk_agents_cancel_task` cancels one of them by ID. In Python this raises `asyncio.CancelledError` inside the tool. In Node.js, pass `abortSignal` to long-running work so it can stop when the operation is aborted.

Cancellation is opt-in because most tools (orders, writes, payments) aren't safe to interrupt partway through. Make sure cancellable tools can be safely stopped at any point.

If a cancellable tool calls `ctx.disallow_interruptions()` in Python or `ctx.disallowInterruptions()` in Node.js, calling the cancellation tool on it raises `ToolError` instead of cancelling the tool.

MCP tools opt into the same flag through `MCPToolOptions`. See [Per-tool options](https://docs.livekit.io/agents/logic/tools/mcp.md#tool-options).

## Duplicate-call handling

When the LLM calls a tool that's already running, the framework handles the duplicate based on the `on_duplicate` argument to `@function_tool` in Python or the `onDuplicate` option to `llm.tool()` in Node.js. Duplicates are detected by tool name only, not by arguments.

| Mode | Description |
| `allow` | Default. Runs the duplicate without restriction. |
| `reject` | Rejects the duplicate and tells the LLM to cancel via `cancel_task` instead. |
| `replace` | Cancels the running call and starts a new one. Requires the running tool to opt into [cancellation](#cancellation), otherwise the duplicate call raises a `ToolError`. |
| `confirm` | Sends the name and arguments of the running call back to the LLM and asks it to re-call with explicit confirmation if a duplicate is needed. |

For example, to require LLM confirmation before a duplicate runs:

**Python**:

```python
@function_tool(on_duplicate="confirm")
async def book_flight(ctx: RunContext, origin: str, destination: str, date: str) -> str:
    return ""  # implementation

```

---

**Node.js**:

```typescript
const bookFlight = llm.tool({
  name: 'bookFlight',
  description: 'Book a flight for the user.',
  onDuplicate: 'confirm',
  parameters: z.object({
    origin: z.string(),
    destination: z.string(),
    date: z.string(),
  }),
  execute: async ({ origin, destination, date }) => {
    return await bookFlightApi(origin, destination, date);
  },
});

```

## Agent handoffs

By default, async tools belong to the `Agent` they're attached to. Tools placed on `Agent(tools=...)` (or bound as `@function_tool` methods on the agent class) belong to that agent, and any pending updates from them are dropped during an [agent handoff](https://docs.livekit.io/agents/logic/agents-handoffs.md).

To keep a tool running across handoffs, so its final result and any updates go to whichever agent is active when the tool finishes, bundle it into an `AsyncToolset` and pass that to the `AgentSession`:

**Python**:

```python
from livekit.agents import AgentSession, RunContext, function_tool
from livekit.agents.llm.async_toolset import AsyncToolset


@function_tool()
async def book_flight(ctx: RunContext, origin: str, destination: str, date: str) -> str:
    return ""  # implementation


session = AgentSession(
    # ... stt, llm, tts, etc.
    tools=[AsyncToolset(id="booking", tools=[book_flight])],
)

```

---

**Node.js**:

```typescript
const bookFlight = llm.tool({
  name: 'bookFlight',
  description: 'Book a flight for the user.',
  parameters: z.object({
    origin: z.string(),
    destination: z.string(),
    date: z.string(),
  }),
  execute: async ({ origin, destination, date }, { ctx }) => {
    await ctx.update('Searching flights.');
    return await bookFlightApi(origin, destination, date);
  },
});

const session = new voice.AgentSession({
  // ... stt, llm, tts, etc.
  tools: [llm.AsyncToolset.create({ id: 'booking', tools: [bookFlight] })],
});

```

An `AsyncToolset` keeps its tools alive across handoffs, including any pending updates from tools that are still running. Plain function tools passed directly to `AgentSession(tools=[...])` aren't carried across handoffs on their own. Only tools wrapped inside an `AsyncToolset` are. Use `llm.AsyncToolset.create({ id, tools, toolHandling })` when you need a lifecycle scope or custom prompt handling; a normal `llm.tool()` is enough for basic async behavior.

## Prompt templates

The framework sends the LLM a short instruction template around each async tool event: a `ctx.update()` call, a duplicate rejection, or a follow-up reply after a tool finishes. The defaults are tuned for natural agent responses, but you can override any of them by passing a `tool_handling` mapping with an `async_options` block in Python or `toolHandling.asyncOptions` in Node.js.

**Python**:

```python
from livekit.agents import AgentSession


session = AgentSession(
    # ... stt, llm, tts, etc.
    tool_handling={
        "async_options": {
            "update_template": (
                "Background tool `{function_name}` reports: {message}. "
                "Acknowledge briefly. Don't summarize results that aren't in the message."
            ),
        },
    },
)

```

---

**Node.js**:

```typescript
const session = new voice.AgentSession({
  // ... stt, llm, tts, etc.
  toolHandling: {
    asyncOptions: {
      updateTemplate:
        'Background tool `{functionName}` reports: {message}. ' +
        "Acknowledge briefly. Don't summarize results that aren't in the message.",
    },
  },
});

```

The available `async_options` keys are:

| Python key | Node.js key | Sent to the LLM when |
| `update_template` | `updateTemplate` | A `ctx.update(message)` call is being delivered to the LLM. |
| `duplicate_reject_template` | `duplicateRejectTemplate` | A duplicate call is blocked by `on_duplicate="reject"` or `onDuplicate: 'reject'`. |
| `duplicate_confirm_template` | `duplicateConfirmTemplate` | A duplicate call needs LLM confirmation under `on_duplicate="confirm"` or `onDuplicate: 'confirm'`. |
| `reply_at_tail_template` | `replyAtTailTemplate` | A follow-up reply runs while the pending update is still the latest chat item. |
| `reply_maybe_covered_template` | `replyMaybeCoveredTemplate` | A follow-up reply runs after newer messages have arrived in the chat context. |

Unspecified keys fall back to defaults. Each value can be a template string or a callable. Both forms receive the same named variables for that template. Set `tool_handling` / `toolHandling` on an `AsyncToolset`, on an `Agent`, or on an `AgentSession`. The framework resolves templates from `AsyncToolset` first, then the `Agent`, then the `AgentSession`, falling back to defaults for any key you don't override.

## Additional resources

For more information on concepts covered in this topic, see the following related topics:

- **[Interruptions](https://docs.livekit.io/agents/logic/tools/definition.md#interruptions)**: Handle or prevent interruptions in a blocking tool with `wait_if_not_interrupted` and `disallow_interruptions()`.

- **[User feedback](https://docs.livekit.io/agents/logic/external-data.md#user-feedback)**: Manual techniques for status updates during tool execution.

---

This document was rendered at 2026-08-18T22:33:34.684Z.
For the latest version of this document, see [https://docs.livekit.io/agents/logic/tools/async.md](https://docs.livekit.io/agents/logic/tools/async.md).

To explore all LiveKit documentation, see [llms.txt](https://docs.livekit.io/llms.txt).