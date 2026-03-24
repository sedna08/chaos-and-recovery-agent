<div align="center">

# Automated Chaos Engineering & Recovery System

_A closed-loop autonomous ecosystem demonstrating advanced Site Reliability Engineering (SRE) and AI-driven DevOps principles._

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688.svg?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-15+-black.svg?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![Observability](https://img.shields.io/badge/Grafana-Loki-F46800.svg?style=flat-square&logo=grafana&logoColor=white)](https://grafana.com/oss/loki/)

</div>

> **⚠️ Disclaimer: Active Development** > The target microservices environment (Echo-Store), the log-driven observability infrastructure, and the autonomous **Healer Agent** are fully operational. The Python-based **Chaos Agent** (automated fault injection) is currently under active development.

---

## 📖 About the Project

This monorepo houses a complete, zero-cost, local engineering environment. It is designed to prove that Local Large Language Models (LLMs) can be securely integrated into operational pipelines to handle Level 1 / Level 2 incident response autonomously.

The environment consists of a dummy application ("Echo-Store") monitored by a unified telemetry stack. The standout feature is the **Healer Agent**, an autonomous first responder that uses the **Observe-Orient-Decide-Act (OODA)** loop. It tails container logs and hardware metrics, feeds the error context to a local instance of Ollama, and executes Docker SDK commands to restore the system—ensuring absolute privacy with **zero data exfiltration**.

## 🏗️ System Architecture

The architecture relies entirely on Docker Compose and a **Sanitized Telemetry Pipeline** where metrics and logs share a unified Loki backend to maintain a minimal compute footprint.

```mermaid
graph TB
    subgraph Docker Compose Environment
        subgraph Echo-Store Application
            Front["Store-Frontend\nNext.js"]
            Back["Inventory-API\nFastAPI"]
            Front -->|HTTP GET /api/stock| Back
        end

        subgraph Unified Observability
            Loki["Grafana Loki\nLog Database"]
            Promtail["Promtail\nApplication Logs"]
            Telegraf["Telegraf\nInfrastructure Metrics"]
            Graf["Grafana\nDashboard"]
        end
    end

    subgraph Autonomous Recovery Subsystem
        HA["Healer Agent\nPython (OODA Loop)"]
        LLM["Local LLM Brain\nOllama"]
    end

    Front -->|Emits stdout/stderr| Promtail
    Back -->|Emits stdout/stderr| Promtail
    Promtail -->|Pushes logs| Loki

    Telegraf -->|Scrapes Docker Stats| Loki
    Loki -->|Visualizes Metrics| Graf

    HA -.->|Observe: Polls Loki via HTTPX| Loki
    HA -.->|Orient: Pydantic Schema Prompt| LLM
    LLM -.->|Decide: Return JSON Action| HA
    HA -.->|Act: Execute SDK Restart / Log| Docker_Compose_Environment
```

## 📊 Observability & Dashboards

This project uses **Unified Log-Driven Metrics**. Instead of traditional exporters, system metrics are extracted from Telegraf's `logfmt` stream in Loki using precise LogQL `unwrap` functions.

### Visualizing Metrics in Grafana

To visualize the health of the **Echo-Store**, navigate to Grafana at `http://localhost:3001` and create a **Time series** panel using the following aggregated query:

#### 1\. CPU Utilization (%)

```logql
avg_over_time({job="debug_metrics""} | logfmt | usage_percent != "" | unwrap usage_percent [1m]) by (container_name)
```

> [\!TIP]
> **Panel Configuration:** Set the Thresholds in Grafana to turn red at **90** with an Area fill to visually match the Healer Agent's intervention trigger point.

## ⚡ Manual Fault Injection (Testing)

To verify the Healer Agent's OODA loop, manually trigger faults from your terminal. Ensure the Healer Agent is running before executing these commands.

| Test Profile        | Command                                                                                                                                                   | Expected Healer Action                                                    |
| :------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------ |
| **CPU Starvation**  | `docker exec -d inventory-api stress-ng --cpu 4 --timeout 60`                                                                                             | Detects metric spike -\> Diagnoses starvation -\> **Restarts Container**  |
| **Memory Leak**     | `docker exec -d store-frontend stress-ng --vm 1 --vm-bytes 500M --vm-populate --vm-hang 0 --temp-path /tmp --timeout 60`                                  | Detects RAM spillage -\> Diagnoses OOM risk -\> **Restarts Container**    |
| **Code Escalation** | `docker exec inventory-api sh -c 'echo "ERROR: Exception: TypeError: unsupported operand type(s) for +: int and str in core.py line 112" > /proc/1/fd/1'` | Catches explicit error -\> Diagnoses logical bug -\> **Logs & Escalates** |

## 📂 Project Structure

This monorepo separates the target application, the infrastructure configurations, and the automation agents.

```text
.
├── agents/                      # Python AI and Automation scripts
│   ├── chaos-agent/             # (In Development) Automated fault injection
│   └── healer-agent/            # Live OODA loop responder (Loki -> Ollama -> Docker)
│
├── infra/                       # Docker Compose and monitoring configuration
│   └── monitoring/              # Promtail, Loki, Telegraf, and Grafana configs
│
├── services/                    # Target dummy microservices
│   ├── inventory-api/           # FastAPI backend serving static data
│   └── store-frontend/          # Next.js SSR frontend gateway
│
├── docs/                        # Architectural diagrams and specifications
├── docker-compose.yml           # Core infrastructure definition
└── README.md                    # Project documentation
```

## 🚀 Getting Started

### Prerequisites

To run the available infrastructure locally, you will need the following installed on your machine:

- **Docker Desktop** (or Docker Engine + Docker Compose plugin)
- **Python 3.12+** (`uv` package manager recommended)
- **Ollama** (Running locally with your preferred model)
- **Node.js 20.x+** (Only required for local frontend development)

### Installation & Launch

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/sedna08/chaos-and-recovery-agent.git](https://github.com/sedna08/chaos-and-recovery-agent.git)
    cd chaos-and-recovery-agent
    ```

2.  **Boot the infrastructure and microservices:**

    ```bash
    docker compose up -d
    ```

3.  **Verify the Environment:**
    - Navigate to the Store Frontend at `http://localhost:3000`.
    - Verify the observability stack is active at `http://localhost:3001`.

4.  **Start the Healer Agent:**

    ```bash
    cd agents/healer-agent
    uv run python -m src.main
    ```

## 📚 Documentation

Detailed functional specifications and service-level READMEs can be found below:

- [System Functional Design Document](https://www.google.com/search?q=docs/functional_design_document.md)
- [Healer Agent Documentation](https://www.google.com/search?q=agents/healer-agent/README.md)
- [Store Frontend Documentation](https://www.google.com/search?q=services/store-frontend/README.md)
- [Inventory API Documentation](https://www.google.com/search?q=services/inventory-api/README.md)

<!-- end list -->
