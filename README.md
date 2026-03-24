# Automated Chaos Engineering & Recovery System

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-15+-black.svg?logo=next.js)](https://nextjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?logo=docker)](https://www.docker.com/)
[![Observability](https://img.shields.io/badge/Grafana-Loki-F46800.svg?logo=grafana)](https://grafana.com/oss/loki/)

> **Disclaimer: Active Development**
> The target microservices environment (Echo-Store) and the log-driven observability infrastructure are fully containerized and operational. The Python-based AI agents (Chaos Agent and Healer Agent) described in this documentation are currently under active development and are not yet included in the repository.

A closed-loop autonomous system demonstrating advanced Site Reliability Engineering (SRE) and DevOps principles. This project features a local microservices environment, a Python-based Chaos Agent that intentionally injects system faults, and a Healer Agent powered by a local Large Language Model (LLM) that detects, diagnoses, and autonomously remediates the failures.

## Table of Contents

- [About the Project](#about-the-project)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Documentation](#documentation)

## About the Project

This monorepo houses a complete, zero-cost, local engineering environment. It is designed to prove that LLMs can be securely integrated into operational pipelines to handle Level 1 / Level 2 incident response autonomously.

The environment consists of a dummy application ("Echo-Store") monitored by a log-driven observability stack. The planned architecture includes a Chaos Agent to break components, and a Healer Agent that polls the log database for anomalies, feeds the error context to a local instance of Ollama, and executes Docker SDK commands to restore the system.

## System Architecture

The target architecture relies entirely on Docker Compose and Log-Driven observability to maintain a minimal compute footprint.

```mermaid
graph TB
    subgraph Docker Compose Environment
        subgraph Echo-Store Application
            Front["Store-Frontend\nNext.js"]
            Back["Inventory-API\nFastAPI"]
            Front -->|HTTP GET /api/stock| Back
        end

        subgraph Log-Driven Observability
            Loki["Grafana Loki\nLog Database"]
            Promtail["Promtail\nLog Scraper"]
            Graf["Grafana\nDashboard"]
        end
    end

    subgraph Chaos Subsystem
        CA["Chaos Agent\nPython (In Development)"]
    end

    subgraph Autonomous Recovery Subsystem
        HA["Healer Agent\nPython Orchestrator (In Development)"]
        LLM["Local LLM Brain\nOllama"]
    end

    CA -.->|Injects faults via Docker SDK| Back
    Front -->|Emits stdout/stderr| Promtail
    Back -->|Emits stdout/stderr| Promtail
    Promtail -->|Pushes logs| Loki
    Loki -->|Visualizes logs| Graf

    HA -.->|Polls for Errors| Loki
    HA -.->|Prompts with Context| LLM
    LLM -.->|Returns JSON Action| HA
    HA -.->|Executes Remediation| Docker_Compose_Environment
```

## Project Structure

This monorepo separates the target application, the infrastructure configurations, and the automation agents.

```text
.
├── agents/                      # Python AI and Automation scripts (Pending)
│   ├── chaos-agent/             # Injects compute and state faults
│   └── healer-agent/            # Polls Loki and queries Ollama
│
├── infra/                       # Docker Compose and monitoring configuration
│   └── monitoring/              # Promtail, Loki, and Grafana configs
│
├── services/                    # Target dummy microservices
│   ├── inventory-api/           # FastAPI backend serving static data
│   └── store-frontend/          # Next.js SSR frontend gateway
│
├── docs/                        # Architectural diagrams and specifications
├── docker-compose.yml           # Core infrastructure definition
└── README.md                    # Project documentation
```

## Getting Started

### Prerequisites

To run the available infrastructure locally, you will need the following installed on your machine:

- Docker Desktop (or Docker Engine + Docker Compose plugin)
- Python 3.12+ (for future agent execution)
- Node.js 20.x+ (for frontend development)

### Installation

1.  Clone the repository:

    ```bash
    git clone <your-repo-url>
    cd automated-chaos-recovery
    ```

2.  Boot the infrastructure and microservices:

    ```bash
    cd infra
    docker compose up -d
    ```

3.  Verify the target health by navigating to the Store Frontend at `http://localhost:3000` to ensure the application is successfully fetching data from the Inventory API.

4.  Verify the observability stack is active by navigating to Grafana at `http://localhost:3001`.

## Documentation

Detailed functional specifications and service-level READMEs can be found below:

- [System Functional Design Document](https://www.google.com/search?q=docs/functional_design_document.md)
- [Store Frontend Documentation](https://www.google.com/search?q=services/store-frontend/README.md)
- [Inventory API Documentation](https://www.google.com/search?q=services/inventory-api/README.md)
