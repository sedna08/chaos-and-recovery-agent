Here is the updated README with the environment boot step and the manual testing process clearly integrated into the setup and usage flows.

---

# 🩹 Healer Agent

[](https://www.python.org/downloads/release/python-3120/)
[](https://github.com/astral-sh/ruff)
[](https://docs.pytest.org/)

> _Turning 3:00 AM pager alerts into automated, self-healing pull requests._

## 🌟 Highlights

The Healer Agent fundamentally shifts incident management from a reactive, human-driven process to a proactive, autonomous workflow.

- **Autonomous Remediation:** Detects unhandled exceptions and applies fixes automatically.
- **Absolute Privacy:** Powered entirely by local LLMs via Ollama. Zero data exfiltration.
- **Test-Driven Safety:** Sandboxes and tests all LLM-generated code. If tests fail, it loops and tries again (Reflexion pattern).
- **Docker Native:** Seamlessly interfaces with your existing local Docker environments and Grafana Loki telemetry.
- **Zero-Latency Inference:** Keeps LLM weights pinned to VRAM for near-instantaneous anomaly resolution.

## ℹ️ Overview

Modern microservices fail. Instead of waiting for an engineer to read the stack trace, the **Healer Agent** acts as an autonomous first responder integrated within the `chaos-and-recovery-agent` ecosystem.

Using the **Observe-Orient-Decide-Act (OODA)** loop, the agent tails your container logs via Grafana Loki. When an anomaly occurs, it isolates the exact lexical scope of the error using Abstract Syntax Tree (AST) parsing. It then queries a local Ollama model (like `llama3.2`) to generate a highly structured Python patch. Because LLMs can hallucinate, the agent intercepts the patch, spins up an ephemeral Docker container, and runs a `pytest` validation suite. Only passing code ever reaches your environment.

### ✍️ Author

Built as part of the [chaos-and-recovery-agent](https://github.com/sedna08/chaos-and-recovery-agent) ecosystem. I am building this to explore the boundaries of trusted, local AI in site reliability engineering.

## ⬇️ Installation instructions

The agent is designed to run alongside your existing `docker-compose` infrastructure.

**Prerequisites:**

1.  Python 3.12+
2.  Local Docker Daemon running.
3.  [Ollama](https://ollama.com/) running locally.
4.  Grafana Loki accessible at `http://localhost:3100`.

**Setup & Booting the Environment:**

We use `uv` for lightning-fast dependency management. Clone the repository, sync the environment, and boot your local LLM model before running the agent:

```bash
# 1. Clone the repository and sync dependencies
git clone https://github.com/sedna08/chaos-and-recovery-agent.git
cd chaos-and-recovery-agent/healer-agent
uv sync

# 2. Boot the environment by pulling the required Ollama model
ollama pull llama3.2
```

## 🚀 Usage instructions

Operating the Healer Agent requires zero manual API calls. Once started, it runs as a continuous watchdog.

**1. Start the Agent:**

Execute the main module to start the OODA loop. The agent will immediately begin polling your localized LogQL streams and outputting structured JSON logs for observability:

```bash
uv run python -m src.main
```

When an application container (e.g., `inventory-api`) crashes, you will see the agent automatically intercept the trace, decide on a remediation tactic, and execute it:

```json
{"time": "2026-03-24 19:18:17", "level": "INFO", "msg": "Polling Loki for errors", "payload": {"query": "{container=~\"inventory-api|store-frontend\"} |= \"Exception\""}}
{"time": "2026-03-24 19:18:22", "level": "INFO", "msg": "Requesting LLM remediation decision", "payload": {"container": "inventory-api", "model": "llama3.2"}}
{"time": "2026-03-24 19:18:24", "level": "INFO", "msg": "Initiating container restart", "payload": {"container": "inventory-api"}}
```

**2. Run the Manual Test:**

To verify the agent is working correctly, you can trigger a manual error in the `inventory-api` container from a separate terminal.

Send a log line to a container that matches the LogQL filter `{container=~"inventory-api|store-frontend"} |= "Exception"`:

```bash
docker logs inventory-api > /dev/null && echo "ERROR: Exception: Connection timeout in database pool" > /proc/1/fd/1
```

_(Note: This command simulates an exception message directly into the container's stdout, which Loki will ingest and the Healer Agent will intercept.)_

---
