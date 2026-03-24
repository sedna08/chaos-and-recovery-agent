# Functional Design Document: Infrastructure Healer Agent

## 1. Introduction

### 1.1 Purpose

This document outlines the functional design for the `healer-agent` microservice. As the autonomous Tier-1 responder of the `chaos-and-recovery-agent` ecosystem, its primary role is to monitor system telemetry, diagnose application faults using a local Large Language Model (LLM), and perform infrastructure-level interventions (such as container restarts) to mitigate transient failures.

### 1.2 Scope

The service is strictly scoped to infrastructure orchestration and diagnostic observability. It explicitly **does not** modify, patch, or alter application source code. It serves as an intelligent triage system: resolving operational timeouts automatically while escalating hard-coded logical bugs to human engineers via structured logs.

## 2. Technology Stack

- **Language:** Python 3.12+
- **AI Inference:** Ollama SDK (Local LLM execution)
- **Container Orchestration:** Docker SDK for Python
- **Telemetry Ingestion:** HTTPX (Polling Grafana Loki API)
- **Data Validation:** Pydantic (Enforcing LLM JSON schemas)
- **Testing & Linting:** Pytest and Ruff

## 3. Component Architecture

The application follows an event-driven, decoupled architectural pattern based on the Observe-Orient-Decide-Act (OODA) loop.

```mermaid
graph TB
    subgraph Healer-Agent Microservice
        Main[OODA Loop Controller]
        Poller[LokiPoller]
        Decider[LLMDecider]
        Executor[DockerExecutor]
        Logger[AgentLogger]
    end

    Loki[(Grafana Loki)] -->|LogQL HTTP Request| Poller
    Poller --> Main
    Main -->|Raw Stack Trace| Decider
    Decider -->|Ollama /api/chat| LocalLLM((llama3.2 Model))
    LocalLLM -->|Structured JSON Decision| Decider
    Decider --> Main

    Main -->|Action: restart| Executor
    Executor -->|Docker API Socket| DockerDaemon[(Local Docker Daemon)]

    Main -->|Action: log_only| Logger
    Logger -->|Structured Incident Log| Loki
```

## 4. Core Capabilities

Unlike a standard API, the Healer Agent operates as a background worker. Its capabilities are defined by the operational decisions the LLM is permitted to make.

| Decision Action | Trigger Condition                                                                        | System Response                                                                                     |
| :-------------- | :--------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------- |
| `restart`       | Transient infrastructure faults (e.g., connection timeouts, deadlocks, OOM constraints). | Agent utilizes Docker SDK to restart the target container, restoring service availability.          |
| `log_only`      | Hard-coded application logic faults (e.g., `TypeError`, `KeyError`, syntax errors).      | Agent aborts intervention and outputs a structured diagnostic summary for human engineering review. |

## 5. System Workflows

### 5.1 Request Lifecycle (Sequence Diagram)

This diagram illustrates the autonomous flow of anomaly detection and remediation.

```mermaid
sequenceDiagram
    participant App as Monitored Container
    participant Watchdog as LokiPoller
    participant Ollama as LLMDecider
    participant Exec as DockerExecutor
    participant Log as AgentLogger

    App-->>Watchdog: Throws Unhandled Exception
    Watchdog->>Ollama: Forward Log Payload

    rect rgb(240, 240, 240)
        Note over Ollama, Exec: Triage & Decision Phase
        Ollama->>Ollama: Analyze Trace (Enforce JSON Schema)

        alt is Transient Fault
            Ollama-->>Exec: action="restart"
            Exec->>App: container.restart()
            Exec->>Log: Log successful mitigation
        else is Logical Bug
            Ollama-->>Log: action="log_only"
            Log->>Log: Output structured diagnostic payload
        end
    end
```

### 5.2 Internal Logic (Activity Flow Diagram)

This diagram maps the continuous polling and cursor-management process of the main loop.

```mermaid
flowchart TD
    Start(( )) --> InitializeCursor

    InitializeCursor -->|Sleep 15s| PollLoki

    PollLoki --> CheckResults{Errors Found?}
    CheckResults -->|No| PollLoki

    CheckResults -->|Yes: Max TS + 1ns| UpdateCursor
    UpdateCursor --> TriageLLM

    TriageLLM --> RouteDecision{Action Type?}
    RouteDecision -->|restart| RestartContainer
    RouteDecision -->|log_only| LogDiagnosis

    RestartContainer --> PollLoki
    LogDiagnosis --> PollLoki
```

## 6. Development & Quality Assurance Flow

To enforce code quality, the service utilizes Ruff and Pytest. The following flowchart dictates the required steps for modifying this service.

```mermaid
flowchart TD
    Start([Developer Modifies Code]) --> RunRuff[Run uv run ruff check .]

    RunRuff --> CheckLint{Passes?}
    CheckLint -->|No| FixLint[Fix Syntax/Formatting]
    FixLint --> RunRuff

    CheckLint -->|Yes| RunPytest[Run uv run pytest]
    RunPytest --> CheckTests{Passes?}

    CheckTests -->|No| FixTests[Fix Logic/Assertions]
    FixTests --> RunPytest

    CheckTests -->|Yes| RunAgent[Execute uv run python -m src.main]
    RunAgent --> End([Ready for Operation])
```

## 7. Project Directory Structure

The following tree represents the internal structure of the `healer-agent/` directory within the monorepo. It explicitly separates external integrations (Docker, LLM, Loki) into single-responsibility modules.

```text
healer-agent/
├── pyproject.toml               # Configuration for Ruff, Pytest, and dependencies
├── uv.lock                      # Deterministic dependency resolution
├── src/                         # Main application source code
│   ├── __init__.py
│   ├── main.py                  # Core OODA loop implementation
│   ├── models.py                # Pydantic schemas (RemediationAction)
│   ├── logger.py                # Structured JSON logging utility
│   ├── loki_client.py           # HTTP polling and cursor management
│   ├── llm_client.py            # Ollama interface and prompt engineering
│   └── docker_client.py         # Infrastructure intervention execution
└── tests/                       # Unit test directory
    ├── __init__.py
    ├── test_loki_client.py      # Mocks HTTPX and verifies cursor logic
    ├── test_llm_client.py       # Mocks Ollama and verifies Pydantic parsing
    └── test_docker_client.py    # Mocks Docker daemon interactions
```

---

```

```
