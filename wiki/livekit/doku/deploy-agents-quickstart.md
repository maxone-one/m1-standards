LiveKit docs › Manage & Deploy › Agent deployment › Quickstart

---

# Agent deployment quickstart

> Quickstart guide for deploying your first agent to LiveKit Cloud.

## Overview

Follow these steps to deploy your first agent to LiveKit Cloud.

## Prerequisites

This guide assumes that you already have:

- The latest version of the [LiveKit CLI](https://docs.livekit.io/reference/developer-tools/livekit-cli.md)
- A [LiveKit Cloud](https://cloud.livekit.io) project
- A working agent. Create one using the [Voice AI quickstart](https://docs.livekit.io/agents/start/voice-ai.md) or one of the following starter templates:

- **[Python starter template](https://github.com/livekit-examples/agent-starter-python)**: A ready-to-deploy voice AI agent built with Python.

- **[Node.js starter template](https://github.com/livekit-examples/agent-starter-node)**: A ready-to-deploy voice AI agent built with Node.js.

## Deploy your agent

Use the following steps with the LiveKit CLI to deploy your agent.

1. Navigate to your project directory:

```shell
cd your-agent-project

```
2. Authenticate with LiveKit Cloud:

```shell
lk cloud auth

```

This opens a browser window to link your LiveKit Cloud project to the CLI. If you've already authenticated and have linked projects, use `lk project list` to list all linked projects. Then, set the default project for agent deployment with `lk project set-default "<project-name>"`.
3. Deploy your agent:

```shell
lk agent create

```

This registers your agent with LiveKit Cloud and assigns a unique ID. The ID is written to a new [`livekit.toml`](https://docs.livekit.io/deploy/agents/managing-deployments.md#toml) file along with the associated project and other default configuration. If you don't already have a `Dockerfile`, the CLI creates one for you.

Next, the CLI uploads your agent code to the LiveKit Cloud build service, builds an image from your Dockerfile, and then deploys it to your LiveKit Cloud project. See the [Builds and Dockerfiles](https://docs.livekit.io/deploy/agents/builds.md) guide for details on the build process, logs, and templates.

Deployment preserves the agent's [dispatch name](https://docs.livekit.io/agents/server/agent-dispatch.md#dispatch-name) from the source code, so the AGENT-NAME you set during `lk agent init` is what you use to target the agent for explicit dispatch.

Your agent is now deployed to LiveKit Cloud and is ready to handle requests. To inspect its behavior in detail, start a debugging session in the [Agent Console](https://docs.livekit.io/agents/start/console.md). To start building an interface for your users, explore [custom frontends](https://docs.livekit.io/agents/start/frontend.md) or [telephony integration](https://docs.livekit.io/agents/start/telephony.md).

## Monitor status and logs

Use the CLI to monitor the [status](https://docs.livekit.io/reference/developer-tools/livekit-cli/agent.md#status) and [logs](https://docs.livekit.io/reference/developer-tools/livekit-cli/agent.md#logs) of your agent.

1. Monitor agent status:

```shell
lk agent status

```

This shows status, replica count, and other details for your running agent.
2. Tail agent logs:

```shell
lk agent logs

```

This shows a live tail of the logs for the new instance of your deployed agent.

## Next steps

Now that your agent is deployed, learn about:

- [Deploying new versions](https://docs.livekit.io/deploy/agents/managing-deployments.md#deploy) of your agent
- [Managing secrets](https://docs.livekit.io/deploy/agents/secrets.md) for your deployment
- [Monitoring logs](https://docs.livekit.io/deploy/agents/logs.md) and debugging issues
- [Configuring builds](https://docs.livekit.io/deploy/agents/builds.md) and Dockerfiles

---

This document was rendered at 2026-08-19T12:44:47.332Z.
For the latest version of this document, see [https://docs.livekit.io/deploy/agents/quickstart.md](https://docs.livekit.io/deploy/agents/quickstart.md).

To explore all LiveKit documentation, see [llms.txt](https://docs.livekit.io/llms.txt).