LiveKit docs › Manage & Deploy › Agent deployment › Overview

---

# Agent deployment overview

> Overview of deploying agents, including deployment management, secrets, builds, logs, and monitoring.

## Overview

Deploy your agents to LiveKit Cloud to run them on LiveKit's global network and infrastructure. LiveKit Cloud provides automatic scaling and load balancing, ensuring capacity for new sessions up to the limits of your plan. Deploy your agent with a single LiveKit CLI command.

> ℹ️ **Note**
> 
> For deployments to other environments, see [Self-hosted deployments](https://docs.livekit.io/deploy/custom/deployments.md).

### Dashboard

The LiveKit Cloud dashboard provides a view into the status of your deployed and self-hosted agents.

- **Realtime metrics**: Monitor session count, agent status, and more.
- **Error tracking**: Identify and diagnose errors in agent sessions.
- **Usage and limits**: Track usage, billing, and limits.

- **[Agents dashboard](https://cloud.livekit.io/projects/p_/agents)**: Monitor and manage your deployed agents in the LiveKit Cloud dashboard.

## Agent deployment quickstart

New to deploying agents? Follow the quickstart guide to deploy your first agent to LiveKit Cloud.

- **[Agent deployment quickstart](https://docs.livekit.io/deploy/agents/quickstart.md)**: Quickstart guide for deploying your first agent to LiveKit Cloud.

## Deployment management

Use the LiveKit CLI to configure, deploy, and manage your agent deployments. The deployment management page covers configuration, deploying new versions, rolling back, and understanding cold starts.

- **[Deployment management](https://docs.livekit.io/deploy/agents/managing-deployments.md)**: Configure, deploy, and manage your agent deployments.

## Secrets management

Securely store and manage sensitive information like API keys, database credentials, and authentication tokens for your agent deployments. LiveKit Cloud encrypts and securely injects these values into your agent containers at runtime.

- **[Secrets management](https://docs.livekit.io/deploy/agents/secrets.md)**: Securely manage API keys and other sensitive data.

## Logs

Monitor and debug your deployed agents with runtime, build, and session logs.

- **[Logs](https://docs.livekit.io/deploy/agents/logs.md)**: View and collect logs from your deployed agents.

## Log drains

For agents deployed to LiveKit Cloud, forward runtime logs to an external monitoring service like Datadog, CloudWatch, Sentry, or New Relic for centralized search, alerting, and long-term retention. [Agent Observability](https://docs.livekit.io/deploy/observability/insights.md) stores per-session logs, but server-level events like crashes and startup failures happen outside of any session and are only accessible through a log drain.

- **[Log drains](https://docs.livekit.io/deploy/agents/log-drains.md)**: Set up log forwarding to your monitoring stack.

## Builds and Dockerfiles

Configure the build process for your agent containers, including Dockerfile setup, build context, and build timeouts. LiveKit Cloud builds container images based on your code and Dockerfile.

- **[Builds and Dockerfiles](https://docs.livekit.io/deploy/agents/builds.md)**: Guide to the LiveKit Cloud build process, plus Dockerfile templates and resources.

---

This document was rendered at 2026-08-19T12:44:47.075Z.
For the latest version of this document, see [https://docs.livekit.io/deploy/agents.md](https://docs.livekit.io/deploy/agents.md).

To explore all LiveKit documentation, see [llms.txt](https://docs.livekit.io/llms.txt).