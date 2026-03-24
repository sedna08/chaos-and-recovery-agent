# Inventory API

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![uv](https://img.shields.io/badge/uv-fast-magenta.svg)](https://github.com/astral-sh/uv)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A lightweight, high-performance microservice built to serve static inventory data. It is specifically designed to maintain predictable, sub-millisecond response times to act as a highly visible target for an Automated Chaos Engineering System.

## Table of Contents

- [About the Project](#about-the-project)
- [Architecture & Design](#architecture--design)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Local Development](#local-development)
  - [Docker](#docker)
- [API Endpoints](#api-endpoints)
- [Testing & Quality](#testing--quality)

## About the Project

The Inventory API is the backend component of the Echo-Store application. It operates without an external database, serving JSON payloads directly from memory to ensure absolute baseline stability during normal operations. This makes any latency spikes injected by Chaos Agents easily identifiable.

## Architecture & Design

For a comprehensive breakdown of the component architecture, request lifecycles, and system workflows, please refer to the primary design document:

📄 **[Functional Design Document](docs/design_doc.md)**

## Getting Started

### Prerequisites

This project utilizes [uv](https://github.com/astral-sh/uv) for lightning-fast dependency management and virtual environment resolution.

- Python 3.12+
- `uv` installed locally
- Docker (optional, for containerization)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sedna08/chaos-and-recovery-agent.git
   cd services/inventory-api
   ```
