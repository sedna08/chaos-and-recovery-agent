# Store Frontend

[![Next.js 15+](https://img.shields.io/badge/Next.js-15+-black.svg?logo=next.js)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg?logo=typescript)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4+-38B2AC.svg?logo=tailwind-css)](https://tailwindcss.com/)
[![Tested with Jest](https://img.shields.io/badge/tested_with-jest-99424f.svg?logo=jest)](https://jestjs.io/)

A modern, highly observable web application built to serve as the user-facing gateway for the Echo-Store microservices architecture. Designed with robust error boundaries and structured logging to monitor system degradation injected by Automated Chaos Engineering Systems.

## Table of Contents

- [About the Project](#about-the-project)
- [Architecture & Design](#architecture--design)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Local Development](#local-development)
  - [Docker](#docker)
- [Testing & Quality](#testing--quality)

## About the Project

The Store Frontend is a lightweight but robust React application that connects to the internal `inventory-api` to fetch and display real-time stock levels and pricing on a clean dashboard.

Beyond rendering data, this service is built with resiliency and observability in mind. It handles backend dependency failures gracefully, rendering high-visibility degraded states while emitting low-cardinality logs for system healers and developers.

## Architecture & Design

This application strictly adheres to SOLID principles, DRY methodologies, and clean code practices.

- **Framework:** Next.js App Router utilizing React Server Components.
- **Styling:** TailwindCSS for a responsive, modern UI design.
- **Observability:** `pino` and `pino-pretty` for highly structured, low-cardinality JSON logging.
- **Resilience:** Global React Error Boundaries catch Server-Side Rendering (SSR) exceptions to prevent full application crashes.

For frontend UI/UX design references, see our implementation notes aligned with modern dashboard standards.

## Getting Started

### Prerequisites

This project utilizes standard Node.js package management.

- Node.js 20.x or higher
- `npm` installed locally
- Docker (for containerized deployment)

### Installation

1. Clone the repository:

   ```bash
   git clone <your-repo-url>
   cd store-frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Configure your environment variables:
   ```bash
   cp .env.example .env.local
   ```
   _Note: Ensure `INVENTORY_API_URL` is pointing to your backend service._

## Usage

### Local Development

Start the Next.js development server with hot-module reloading:

```bash
npm run dev
```

To test backend degradation locally or view detailed health probe logs, start the server with debug logging enabled:

```bash
LOG_LEVEL=debug npm run dev
```

### Docker

This project includes a highly optimized, multi-stage Dockerfile that leverages Next.js standalone output for a minimal production footprint.

1. Build the image:

   ```bash
   docker build -t store-frontend:local .
   ```

2. Run the container:
   ```bash
   docker run -p 3000:3000 -e INVENTORY_API_URL=[http://host.docker.internal:8000](http://host.docker.internal:8000) store-frontend:local
   ```

## Testing & Quality

To ensure code remains bulletproof, this project utilizes a strictly Test-Driven Development (TDD) approach. The Jest testing suite validates both React UI rendering (via `jsdom`) and server-side API Route Handlers (via `node` environment).

Run the test suite:

```bash
npm run test
```

Run tests in watch mode for active development:

```bash
npm run test:watch
```
