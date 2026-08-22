LiveKit docs › Manage & Deploy › Agent deployment › Log drains

---

# Log drains

> Forward runtime logs from agents deployed to LiveKit Cloud to external monitoring services like Datadog, CloudWatch, Sentry, New Relic, Splunk, Google Cloud, and syslog-compatible endpoints.

## Overview

Log drains let you forward runtime logs to your existing monitoring stack. Use a log drain to collect all of your agent's runtime logs — including server-level events like crashes, startup errors, and dispatch failures. This gives you centralized search, alerting, long-term retention, and visibility across all replicas. Log drains are available for agents deployed to LiveKit Cloud.

Log drains forward **runtime logs only** — the raw stdout and stderr output from your agent process. They don't include traces, build logs, transcripts, or audio recordings. For those, use the following:

- **Traces**: Export directly from your agent code. See [Export traces](https://docs.livekit.io/deploy/observability/tracing.md).
- **Transcripts, audio, and session data**: Available through [Agent Observability](https://docs.livekit.io/deploy/observability/insights.md) in the LiveKit Cloud dashboard.
- **Build logs**: Available in the [LiveKit CLI](https://docs.livekit.io/deploy/agents/logs.md#build-logs) and the Cloud dashboard.

Log forwarding runs in a sidecar process alongside your agent — it's invisible to your agent code. The `lk agent logs` CLI command only tails logs from a single agent server instance. If your agent runs at scale across multiple replicas, a log drain is the only way to see logs from all instances.

## Supported destinations

Runtime logs can be forwarded to the following external monitoring services. The table lists the required configuration for each destination:

| Destination | Required secrets | Optional secrets |
| [Datadog](#datadog) | `DATADOG_TOKEN` | `DATADOG_REGION` (default: `us1`) |
| [CloudWatch](#cloudwatch) | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | `AWS_REGION` (default: `us-west-2`) |
| [Sentry](#sentry) | `SENTRY_DSN` |  |
| [New Relic](#new-relic) | `NEW_RELIC_LICENSE_KEY` |  |
| [Splunk](#splunk) | `LOGS_ENABLE_SPLUNK`, `SPLUNK_HEC_TOKEN`, `SPLUNK_HEC_URL` | `SPLUNK_INDEX`, `SPLUNK_SOURCETYPE`, `SPLUNK_SOURCE` |
| [Google Cloud](#google-cloud) | `LOGS_ENABLE_GCP`, `GOOGLE_CLOUD_PROJECT`, `GOOGLE_APPLICATION_CREDENTIALS` |  |
| [Syslog](#syslog) | `SYSLOG_ENDPOINT` | `SYSLOG_TOKEN` |

## Datadog integration

Automatically forward all runtime logs to your Datadog account. Add a Datadog client token as a [secret](https://docs.livekit.io/deploy/agents/secrets.md) to enable log forwarding. If your account is in a region other than `us1`, you can also set the region.

Use the following command to set your Datadog secret:

```shell
lk agent update-secrets --secrets "DATADOG_TOKEN=your-client-token" --secrets "DATADOG_REGION=us1"

```

- **`DATADOG_TOKEN`** _(string)_: Your Datadog [client token](https://docs.datadoghq.com/account_management/api-app-keys/#client-tokens).

- **`DATADOG_REGION`** _(string)_ (optional) - Default: `us1`: Your Datadog region. Supported regions are `us1`, `us3`, `us5`, `us1-fed`, `eu`, and `ap1`.

#### Log fields

The following log fields are set in Datadog for all log lines sent from LiveKit Cloud:

| Field | Value | Description |
| host | <worker-id> | A unique identifier for the specific agent server instance emitting the log. |
| source | <agent-id> | The ID of the agent, as in `livekit.toml` and the dashboard. |
| service | `"cloud.livekit.io"` |  |
| stream | `stdout` or `stderr` | Indicates whether the log originated from stdout or stderr. |

#### Troubleshooting Datadog

If logs aren't appearing in Datadog, confirm `DATADOG_REGION` matches your Datadog account's region (defaults to `us1`).

## CloudWatch integration

Automatically forward all runtime logs to your CloudWatch account. Add your AWS access key ID and secret access key as [secrets](https://docs.livekit.io/deploy/agents/secrets.md) to enable log forwarding. The AWS region defaults to `us-west-2` — set the `AWS_REGION` secret to use a different region.

Use the following command to set your CloudWatch secrets:

```shell
lk agent update-secrets --secrets "AWS_ACCESS_KEY_ID=your-access-key-id" --secrets "AWS_SECRET_ACCESS_KEY=your-secret-access-key" --secrets "AWS_REGION=us-west-2"

```

- **`AWS_ACCESS_KEY_ID`** _(string)_: Your AWS [access key ID](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html).

- **`AWS_SECRET_ACCESS_KEY`** _(string)_: Your AWS [secret access key](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html).

- **`AWS_REGION`** _(string)_ (optional) - Default: `us-west-2`: Your AWS region. See the [AWS regions](https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html) page for a list of all supported regions.

#### Log fields

The following log fields are set in CloudWatch for all log lines sent from LiveKit Cloud:

| Field | Value | Description |
| logGroupName | <agent-id> | The CloudWatch log group, named with your agent ID. |
| logStreamName | <worker-id> | A unique identifier for the specific agent server instance emitting the log. |
| message | Log line content | The raw log output from your agent process. |

#### Troubleshooting CloudWatch

If logs aren't appearing in CloudWatch, check the following:

- Confirm the `AWS_REGION` secret matches the region you're viewing in the AWS console (defaults to `us-west-2`).
- Confirm the IAM user has `logs:CreateLogGroup`, `logs:CreateLogStream`, and `logs:PutLogEvents` permissions.
- Logs appear under the log group `<agent-id>`. The log group is created automatically on first write — if it doesn't exist, logs haven't been delivered yet.

## Sentry integration

Automatically forward all runtime logs to your Sentry account. Add your Sentry DSN as a [secret](https://docs.livekit.io/deploy/agents/secrets.md) to enable log forwarding.

Use the following command to set your Sentry secret:

```shell
lk agent update-secrets --secrets "SENTRY_DSN=your-sentry-dsn"

```

- **`SENTRY_DSN`** _(string)_: Your Sentry [DSN](https://docs.sentry.io/product/sentry-basics/dsn-explainer/).

#### Log fields

The following log fields are set in Sentry for all log lines sent from LiveKit Cloud:

| Field | Value | Description |
| agent_id | <agent-id> | The ID of the agent, as in `livekit.toml` and the dashboard. |
| worker_id | <worker-id> | A unique identifier for the specific agent server instance emitting the log. |
| hostname | `livekit.hosted.agents` | Constant service identifier. |

## New Relic integration

Automatically forward all runtime logs to your New Relic account. Add your New Relic license key as a [secret](https://docs.livekit.io/deploy/agents/secrets.md) to enable log forwarding.

Use the following command to set your New Relic secret:

```shell
lk agent update-secrets --secrets "NEW_RELIC_LICENSE_KEY=your-license-key"

```

- **`NEW_RELIC_LICENSE_KEY`** _(string)_: Your New Relic [license key](https://docs.newrelic.com/docs/apis/intro-apis/new-relic-api-keys/).

#### Log fields

The following log fields are set in New Relic for all log lines sent from LiveKit Cloud:

| Field | Value | Description |
| agentId | <agent-id> | The ID of the agent, as in `livekit.toml` and the dashboard. |
| workerId | <worker-id> | A unique identifier for the specific agent server instance emitting the log. |
| hostname | `livekit.hosted.agents` | Constant service identifier. |
| message | Log line content | The raw log output from your agent process. |
| level | Log level string | The log level extracted from the log line (for example, `info`, `error`, `warn`). |
| stream | `stdout` or `stderr` | Indicates whether the log originated from stdout or stderr. |

## Splunk integration

Automatically forward all runtime logs to your Splunk instance using the HTTP Event Collector (HEC). Add your HEC token, endpoint URL, and the `LOGS_ENABLE_SPLUNK` flag as [secrets](https://docs.livekit.io/deploy/agents/secrets.md) to enable log forwarding.

Use the following command to set your Splunk secrets:

```shell
lk agent update-secrets --secrets "LOGS_ENABLE_SPLUNK=1" --secrets "SPLUNK_HEC_TOKEN=your-hec-token" --secrets "SPLUNK_HEC_URL=https://<your-instance>.splunkcloud.com:8088"

```

- **`LOGS_ENABLE_SPLUNK`** _(string)_: Set to `1` to enable Splunk log forwarding. Required even when the HEC token and URL are set.

- **`SPLUNK_HEC_TOKEN`** _(string)_: Your Splunk [HTTP Event Collector token](https://docs.splunk.com/Documentation/Splunk/latest/Data/UsetheHTTPEventCollector).

- **`SPLUNK_HEC_URL`** _(string)_: Your Splunk HEC endpoint URL, including the port. For example, `https://<your-instance>.splunkcloud.com:8088`.

- **`SPLUNK_INDEX`** _(string)_ (optional): The Splunk index to send events to. If not set, events are sent to the default index configured for your HEC token.

- **`SPLUNK_SOURCETYPE`** _(string)_ (optional) - Default: `_json`: The Splunk [source type](https://docs.splunk.com/Documentation/Splunk/latest/Data/Whysourcetypesmatter) assigned to log events. Controls how Splunk parses and formats the data.

- **`SPLUNK_SOURCE`** _(string)_ (optional) - Default: `livekit:cloud-agents`: The Splunk [source](https://docs.splunk.com/Documentation/Splunk/latest/Data/Aboutdefaultfields) field for log events. Identifies where the data originated.

#### Log fields

Each log line is sent as a JSON event to the HEC endpoint. The following top-level HEC fields are set for every event:

| Field | Value | Description |
| host | <worker-id> | A unique identifier for the specific agent server instance emitting the log. |
| source | Value of `SPLUNK_SOURCE`, or `livekit:cloud-agents` | Identifies the source of the log events. |
| sourcetype | Value of `SPLUNK_SOURCETYPE`, or `_json` | The Splunk source type assigned to log events. |

The event body contains the following fields:

| Field | Value | Description |
| message | Log line content | The raw log output from your agent process. |
| stream | `stdout` or `stderr` | Indicates whether the log originated from stdout or stderr. |
| level | Log level string | The log level extracted from the log line (for example, `info`, `error`, `warn`). |
| agent_id | <agent-id> | The ID of the agent, as in `livekit.toml` and the dashboard. |
| worker_id | <worker-id> | A unique identifier for the specific agent server instance emitting the log. |
| hostname | `livekit.hosted.agents` | Constant service identifier. |

#### Troubleshooting Splunk

If logs aren't appearing in Splunk, check the following:

- Confirm `LOGS_ENABLE_SPLUNK` is set. Without this secret, the integration stays disabled even if the HEC token and URL are configured.
- Confirm `SPLUNK_HEC_URL` includes the correct port (typically `8088` for HEC).
- Confirm the HEC token has permission to write to the target index.

## Google Cloud integration

Automatically forward all runtime logs to [Google Cloud Logging](https://cloud.google.com/logging/docs). Mount a service account JSON key as a [file-mounted secret](https://docs.livekit.io/deploy/agents/secrets.md#file-mounted-secrets), then set the project ID and credentials path.

Use the following command to set your Google Cloud secrets. The `--secret-mount` flag uploads your local credentials file to `/etc/secrets/google-application-credentials.json` in the agent container:

```shell
lk agent update-secrets --secrets "LOGS_ENABLE_GCP=1" --secrets "GOOGLE_CLOUD_PROJECT=your-project-id" --secrets "GOOGLE_APPLICATION_CREDENTIALS=/etc/secrets/google-application-credentials.json" --secret-mount ./google-application-credentials.json

```

- **`LOGS_ENABLE_GCP`** _(string)_: Set to any non-empty string to enable Google Cloud log forwarding. Required even when the project ID and credentials are set.

To disable, you can [overwrite all secrets](https://docs.livekit.io/deploy/agents/secrets.md#overwriting-all-secrets) or delete the secret in LiveKit Cloud. Select your agent from the [Agents dashboard](https://cloud.livekit.io/projects/p_/agents) and see **Secrets** in **Agent configuration**.

- **`GOOGLE_CLOUD_PROJECT`** _(string)_: Your Google Cloud [project ID](https://cloud.google.com/resource-manager/docs/creating-managing-projects).

- **`GOOGLE_APPLICATION_CREDENTIALS`** _(string)_: Path to the service account JSON key inside the agent container. After mounting with `--secret-mount`, this is `/etc/secrets/google-application-credentials.json`. The service account needs the [Logs Writer](https://cloud.google.com/logging/docs/access-control#logging.writer) role (`roles/logging.logWriter`).

#### Troubleshooting Google Cloud

If logs aren't appearing in Cloud Logging, check the following:

- Confirm `LOGS_ENABLE_GCP` is set to `1`. If this isn't set, the integration is disabled.
- Confirm `GOOGLE_APPLICATION_CREDENTIALS` matches the mounted path (`/etc/secrets/<filename>`).
- Confirm the service account has the `roles/logging.logWriter` role on the target project.

## Syslog integration

Automatically forward all runtime logs to any syslog-compatible endpoint over TCP+TLS. This supports any service or infrastructure that accepts syslog input, including Papertrail, Mezmo (LogDNA), and syslog-ng. Add the syslog endpoint as a [secret](https://docs.livekit.io/deploy/agents/secrets.md) to enable log forwarding.

Use the following command to set your syslog secrets:

```shell
lk agent update-secrets --secrets "SYSLOG_ENDPOINT=logs.example.com:6514" --secrets "SYSLOG_TOKEN=your-token"

```

- **`SYSLOG_ENDPOINT`** _(string)_: The host and port of your syslog receiver. For example, `logs.example.com:6514`. The connection always uses TCP with TLS 1.2 or higher.

- **`SYSLOG_TOKEN`** _(string)_ (optional): An authentication token prepended to each syslog message. Some providers (such as Papertrail) require this to route logs to the correct account.

#### Message format

Messages follow [RFC 5424](https://datatracker.ietf.org/doc/html/rfc5424) with a newline terminator:

```
[SYSLOG_TOKEN ]<PRI>1 TIMESTAMP HOSTNAME APPNAME PROCID MSGID STRUCTURED-DATA MSG\n

```

| Field | Value | Description |
| SYSLOG_TOKEN | Token value | The provided token, followed by a space. Omitted when `SYSLOG_TOKEN` is not set. |
| PRI | Facility × 8 + severity | Facility is always 1 (user-level). Severity is defined in the [severity mapping](#severity-mapping) below. |
| TIMESTAMP | RFC 3339 timestamp | The time the log line was emitted. |
| HOSTNAME | <agent-id> | The ID of the agent, as in `livekit.toml` and the dashboard. |
| APPNAME | `livekit.hosted.agents` | Constant identifier for LiveKit Cloud agent logs. |
| PROCID | <worker-id> | A unique identifier for the specific agent server instance emitting the log. |
| MSGID | `-` | Not used. |
| STRUCTURED-DATA | `-` | Not used. |
| MSG | Log line content | The decoded log line from the agent process. |

Example message with a token:

```
my-api-key <14>1 2026-01-15T10:30:00Z CA_abcd1234 livekit.hosted.agents CAW_zyxw9876 - - hello world

```

#### Severity mapping

Agent log levels are mapped to RFC 5424 severity values:

| Agent level | Syslog severity | Numeric |
| `panic`, `fatal` | Critical | 2 |
| `error` | Error | 3 |
| `warn`, `warning` | Warning | 4 |
| `info` | Informational | 6 |
| `debug`, `trace` | Debug | 7 |

Unrecognized levels default to Informational (6).

#### Troubleshooting syslog

If logs aren't appearing at your syslog endpoint, check the following:

- Confirm `SYSLOG_ENDPOINT` is in `host:port` format (for example, `logs.example.com:6514`).
- Confirm your receiver supports TCP+TLS on the configured port.

---

This document was rendered at 2026-08-19T12:45:13.362Z.
For the latest version of this document, see [https://docs.livekit.io/deploy/agents/log-drains.md](https://docs.livekit.io/deploy/agents/log-drains.md).

To explore all LiveKit documentation, see [llms.txt](https://docs.livekit.io/llms.txt).