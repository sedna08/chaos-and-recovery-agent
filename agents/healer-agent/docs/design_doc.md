# Design Document: Autonomous Self-Healing Agent Integration via Ollama

## 1. System Overview

The Healing Agent is an autonomous, machine-driven anomaly resolution service integrated within the `chaos-and-recovery-agent` ecosystem. Powered by a local Large Language Model (LLM) via the Ollama platform and its official Python SDK, the agent fundamentally shifts incident management from a reactive, human-driven process to a proactive, self-healing workflow.

The primary objective of the Healing Agent is to continuously monitor system telemetry and logs, detect unhandled exceptions or anomalies, and autonomously generate, validate, and apply corrective actions—ranging from container restarts to code patches. By operating entirely on local hardware or managed internal clusters via Ollama, the system guarantees zero data exfiltration, strict privacy compliance, and circumvents the latency and recurring API costs associated with cloud-based AI providers.

The agent's development and operational lifecycle strictly adheres to SOLID, DRY, and KISS engineering principles. Furthermore, a rigorous Test-Driven Development (TDD) approach is mandated. The fundamental assumption of the system is that LLM outputs are inherently untrusted and prone to hallucination; therefore, no generative AI output is applied to the live environment without first passing validation.

## 2. System Architecture

The Healing Agent abandons monolithic design in favor of a highly decoupled, event-driven microservices architecture. This ensures fault tolerance; the failure of the monitored application will not cascade into the failure of the Healing Agent.

The architecture is built upon three core operational patterns:

- **The Observe-Orient-Decide-Act (OODA) Framework:** This continuous feedback loop drives the core workflow. The agent observes telemetry via Loki, orients itself to the error context, decides on a fix via Ollama inference, and acts by executing container operations or staging code patches.
- **The Orchestrator-Worker Pattern:** To optimize local compute resources, a central Orchestrator LLM (e.g., a lightweight 1.5B/3B model like Llama 3.2 or Qwen) triages incoming errors. Simple operational issues (like connection timeouts requiring restarts) are handled directly. Complex logical faults can be delegated to a larger, more capable Worker model for deep reasoning.
- **The Reflexion (Self-Healing) Pattern:** Standard linear LLM chains are brittle. If the validation sandbox rejects a proposed code patch (e.g., due to a failed `pytest` run), the resulting stderr output is captured and fed back into the Ollama model. The LLM is prompted to reason about its previous failure and generate a revised patch, looping until the test passes or a retry limit is reached.

## 3. System Components

The agent is modularized into specialized, single-responsibility Python components.

### 3.1 Telemetry and Event Watchdog (`LokiPoller`)

This module acts as the sensory input, utilizing an HTTP-based polling mechanism against a local Grafana Loki instance. By executing targeted LogQL queries (e.g., `{container=~"inventory-api"} |= "Exception"`), it continuously extracts raw stack traces and fault payloads. It manages its own state using a high-water mark cursor to prevent redundant processing of historical logs.

### 3.2 Context Builder and AST Analyzer (`ContextBuilder`)

To provide the LLM with localized lexical scope, this module parses the failing application's Abstract Syntax Tree (AST) using Python's built-in `ast` module. It extracts the specific enclosing function or class associated with the stack trace line number. It can also generate vector embeddings of the error to query a historical vector database, appending proven past solutions to the LLM's prompt via Retrieval-Augmented Generation (RAG).

### 3.3 Ollama Orchestration Client Interface (`LLMDecider`)

This module handles inference communication with the local LLM. It constructs dynamic prompts and enforces strict JSON-structured outputs. By leveraging Pydantic, the agent passes `format=RemediationAction.model_json_schema()` to the Ollama API, ensuring the model's response maps deterministically to a structured Python object containing the fields `rationale`, `action`, and `target_container`.

It tracks performance telemetry provided by the Ollama API payload—specifically `eval_count` (output tokens) and `eval_duration` (time spent generating)—to continuously calculate the system's Output Tokens Per Second (TPS) using the following formula:

$$TPS = \frac{\text{eval\_count}}{\text{eval\_duration} \times 10^{-9}}$$

### 3.4 Execution and Validator Sandbox (`ExecutionSandbox`)

To uphold the TDD mandate, this component intercepts the LLM's proposed code patches and stages them in an ephemeral execution environment using Python's `tempfile` module. It dynamically invokes `pytest` via `subprocess.run` to execute existing and newly generated regression tests against the patched code.

- **Success:** If the exit code is 0, the patch is verified.
- **Failure:** The module intercepts the failed assertion data (stderr), which can trigger the Reflexion loop.
- **TDD Mocking Layer:** For testing the agent itself, this module heavily utilizes `pytest-mock` and `unittest.mock.patch` to intercept subprocess calls and API requests, injecting simulated outputs without relying on non-deterministic LLM behavior.

## 4. Sequence Diagrams

The following sequence illustrates the autonomous loop initiated when an anomaly is detected.

```mermaid
sequenceDiagram
    participant App as Monitored Application
    participant Watchdog as LokiPoller
    participant Context as ContextBuilder
    participant Ollama as LLMDecider
    participant Sandbox as ExecutionSandbox / DockerExecutor

    App-->>Watchdog: Throws Unhandled Exception (stdout/stderr to Loki)
    Watchdog->>Context: Push raw stack trace payload
    Context->>Context: Parse AST & locate failing function
    Context->>Context: RAG Query for historical fixes
    Context->>Ollama: Formatted Prompt + AST Context

    rect rgb(240, 240, 240)
        Note over Ollama, Sandbox: Decision & Action Loop
        Ollama->>Ollama: Inference (Enforced JSON Pydantic Schema)

        alt Action == "restart"
            Ollama->>Sandbox: Deliver RemediationAction(restart)
            Sandbox->>App: Execute container restart via DockerExecutor
        else Action == "patch"
            Ollama->>Sandbox: Deliver code patch
            Sandbox->>Sandbox: Apply patch to ephemeral clone
            Sandbox->>Sandbox: Execute pytest suite

            alt Tests Fail
                Sandbox-->>Ollama: Return stderr & failing test assertions
                Ollama->>Ollama: Analyze failure (Self-Correction)
            else Tests Pass
                Sandbox->>App: Deploy verified patch
            end
        end
    end
```

## 5. Interfaces with Local Docker Environment

The Healing Agent heavily interfaces with the local containerized infrastructure to monitor applications, execute remediation tactics, and spin up secure validation environments.

- **Python Docker SDK Integration (`DockerExecutor`):** The agent utilizes the `docker` library to interact programmatically with the local Docker daemon. Using `client = docker.from_env()`, the agent can issue automated `client.containers.get('service_name').restart()` commands to mitigate unresponsive services, or spin up isolated containers for sandboxing.

- **LogQL and Grafana Loki Telemetry:** For monitoring the existing Docker environment, the `LokiPoller` queries the local Grafana Loki API. By querying specific labels, the agent programmatically tails container logs to detect application crashes without needing direct access to the container filesystems.

- **Ollama Container Configuration:** To ensure the local Ollama LLM does not introduce high latency during the "Orient" and "Decide" phases, the Ollama Docker container should be explicitly configured with the `OLLAMA_KEEP_ALIVE=24h` (or `-1`) environment variable. This forces the container to permanently pin the LLM weights inside the GPU VRAM, dropping the `load_duration` metric to zero and enabling near-instantaneous inference.

---
