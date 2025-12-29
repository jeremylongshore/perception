# Perception: Operator-Grade System Analysis & Operations Guide

*For: DevOps Engineer*
*Generated: 2025-12-29*
*System Version: 5d9dc0f (chore/beads-sync)*
*Document ID: 042-AA-AUDT-appaudit-devops-playbook*

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Operator & Customer Journey](#2-operator--customer-journey)
3. [System Architecture Overview](#3-system-architecture-overview)
4. [Directory Deep-Dive](#4-directory-deep-dive)
5. [Automation & Agent Surfaces](#5-automation--agent-surfaces)
6. [Operational Reference](#6-operational-reference)
7. [Security, Compliance & Access](#7-security-compliance--access)
8. [Cost & Performance](#8-cost--performance)
9. [Development Workflow](#9-development-workflow)
10. [Dependencies & Supply Chain](#10-dependencies--supply-chain)
11. [Integration with Existing Documentation](#11-integration-with-existing-documentation)
12. [Current State Assessment](#12-current-state-assessment)
13. [Quick Reference](#13-quick-reference)
14. [Recommendations Roadmap](#14-recommendations-roadmap)

---

## 1. Executive Summary

### Business Purpose

**Perception** is an AI-powered news intelligence platform that automates the collection, analysis, and delivery of executive-level insights from diverse news sources. The platform eliminates manual monitoring of 50+ news sources by deploying 8 specialized Vertex AI agents that coordinate via Google's A2A Protocol to fetch RSS feeds, score relevance, generate summaries, and deliver daily executive briefs.

The system is built exclusively on Google Cloud Platform, demonstrating production-grade multi-agent architecture patterns for enterprise intelligence applications. It serves as both a functional product for executives needing strategic intelligence and a reference implementation for Intent Solutions IO's AI agent consulting practice.

**Current operational status**: The platform is at **v0.3.0** with MCP service deployed to Cloud Run (validated with real RSS fetching at 270ms latency), 8-agent system complete with E2E ingestion pipeline, and Firebase dashboard ready for data integration. Agent Engine deployment is scripted but awaiting manual trigger.

**Technology foundation**: Python 3.11+ with Google ADK for agents, Vertex AI Agent Engine for orchestration, Cloud Run for MCP services, Firestore for data persistence, and Firebase Hosting for the React dashboard. All deployments use Workload Identity Federation for keyless authentication from GitHub Actions.

**Immediate strengths**: Clean separation of concerns (agents think, MCPs do, Firebase serves humans), comprehensive observability through Cloud Logging, production-ready scoring and validation pipelines, and well-documented architecture. **Key risks**: Agent Engine deployment pending, MCP_BASE_URL environment variable configuration needs research, and dashboard-to-Firestore integration incomplete. **Strategic consideration**: Platform positioned for SaaS evolution with multi-tenant Firebase Auth, per-user topics, and Stripe billing in Phase 2.

### Operational Status Matrix

| Environment | Status | Uptime Target | Current Uptime | Release Cadence | Active Users |
|-------------|--------|---------------|----------------|-----------------|--------------|
| Production MCP | Active | 99.5% | N/A (new) | Manual via GitHub Actions | System only |
| Firebase Dashboard | Active | 99.9% | Estimated 99.9% | Push to main | Demo/testing |
| Agent Engine | Pending | 99.5% | N/A | Manual trigger | N/A |
| Development | Active | N/A | N/A | Continuous | 1 developer |

### Technology Stack Summary

| Category | Technology | Version | Purpose |
|----------|------------|---------|---------|
| Language | Python | 3.11+ | Agent system, MCP service |
| Language | TypeScript | 5.2.2 | Dashboard frontend |
| Agent Framework | Google ADK | >=0.6.0 | Agent development and orchestration |
| AI Platform | Vertex AI Agent Engine | Current | Agent runtime and A2A communication |
| AI Model | Gemini 2.0 Flash | Current | Article analysis and summarization |
| Database | Firestore | Native mode | Primary data store |
| Compute | Cloud Run | Managed | MCP service hosting |
| Frontend | React | 18.2.0 | Dashboard SPA |
| Build | Vite | 5.0.8 | Frontend bundler |
| Styling | TailwindCSS | 3.4.18 | UI styling |
| IaC | Terraform | >=1.6.0 | Infrastructure provisioning |
| CI/CD | GitHub Actions | Current | Deployment automation |
| Auth | Workload Identity Federation | Current | Keyless GCP authentication |

---

## 2. Operator & Customer Journey

### Primary Personas

**Operators (DevOps/Platform Engineers)**:
- Deploy and maintain agent infrastructure on GCP
- Monitor Cloud Run MCP service health and performance
- Manage Firestore collections and security rules
- Handle CI/CD pipeline maintenance and secret rotation
- Respond to ingestion failures and system alerts

**External Customers (Executives/Intelligence Teams)**:
- Access daily executive briefs via Firebase dashboard
- Configure topic monitoring keywords
- Review relevance-scored articles
- Set up alerts for emerging trends
- Query historical intelligence data

**Reseller Partners (Future Phase 2)**:
- White-label deployment for their clients
- API access for integration with existing tools
- Custom topic configurations per client
- Billing and usage analytics

**Automation Bots (AI Agents)**:
- Agent 0 (Root Orchestrator): Coordinates entire workflow
- Agent 1 (Source Harvester): Fetches RSS feeds via MCP
- Agent 2 (Topic Manager): Manages user topics from Firestore
- Agent 3 (Relevance Scorer): Scores and ranks articles
- Agent 4 (Brief Writer): Generates executive summaries
- Agent 5 (Alert Detector): Identifies anomalies (stub)
- Agent 6 (Validator): Schema validation
- Agent 7 (Storage Manager): Firestore persistence
- Agent 8 (Tech Editor): Technology section curation

### End-to-End Journey Map

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PERCEPTION USER JOURNEY                            │
└─────────────────────────────────────────────────────────────────────────────┘

AWARENESS                ONBOARDING              CORE WORKFLOWS
    │                        │                        │
    v                        v                        v
┌─────────┐            ┌─────────┐            ┌─────────────────┐
│ Landing │─────────>│ Firebase │─────────>│  Daily Brief    │
│  Page   │            │  Auth   │            │  Consumption    │
│ (About) │            │ Login   │            └────────┬────────┘
└─────────┘            └─────────┘                     │
                                                       v
                                              ┌─────────────────┐
                                              │ Topic Config    │
                                              │ (Add keywords)  │
                                              └────────┬────────┘
                                                       │
                                                       v
                                              ┌─────────────────┐
                                              │ Article Review  │
                                              │ (Scored list)   │
                                              └─────────────────┘

SUPPORT/FEEDBACK                    RENEWAL/EXPANSION
    │                                      │
    v                                      v
┌─────────────────┐                ┌─────────────────┐
│ GitHub Issues   │                │ Phase 2 SaaS    │
│ (Community)     │                │ (Stripe billing)│
└─────────────────┘                └─────────────────┘
```

**Critical Touchpoints**:
1. **Dashboard Access**: Firebase Auth gates all protected routes (Dashboard, Topics, Briefs)
2. **Daily Ingestion**: Cloud Scheduler triggers 7:30 AM CST daily workflow
3. **Brief Delivery**: Executive summary appears in dashboard after ingestion completes
4. **Topic Updates**: User changes propagate to next ingestion cycle

**Dependencies**:
- Firebase Auth for user identity
- Firestore for all data persistence
- Cloud Run MCP for external data fetching
- Vertex AI Agent Engine for orchestration
- RSS feed availability (external dependency)

**Friction Points**:
- Agent Engine deployment requires manual trigger
- MCP_BASE_URL not yet wired to Agent Engine runtime
- Dashboard shows placeholder data until Firestore integration complete
- No email/Slack delivery (DeliveryMCP stubbed)

**Success Metrics**:
- Ingestion run success rate: Target >95%
- Brief generation latency: Target <60s
- Article relevance accuracy: Target >80% user satisfaction
- Dashboard load time: Target <2s

### SLA Commitments

| Metric | Target | Current | Owner |
|--------|--------|---------|-------|
| MCP Service Uptime | 99.5% | N/A (new deployment) | Platform Team |
| Dashboard Uptime | 99.9% | Estimated 99.9% (Firebase) | Firebase SLA |
| Ingestion Success Rate | 95% | N/A (pending Agent Engine) | Agent Team |
| Brief Generation P95 | <60s | N/A | Agent Team |
| API Response Time P95 | <500ms | 270ms (MCP RSS) | Platform Team |
| CSAT | >4.0/5.0 | N/A | Product Team |

---

## 3. System Architecture Overview

### Technology Stack (Detailed)

| Layer | Technology | Version | Source of Truth | Purpose | Owner |
|-------|------------|---------|-----------------|---------|-------|
| Frontend/UI | React 18 + TypeScript | 18.2.0 / 5.2.2 | `dashboard/package.json` | Executive dashboard SPA | Frontend |
| Frontend Build | Vite | 5.0.8 | `dashboard/vite.config.ts` | Fast development and bundling | Frontend |
| UI Framework | TailwindCSS | 3.4.18 | `dashboard/tailwind.config.js` | Utility-first styling | Frontend |
| Charts | Chart.js + react-chartjs-2 | 4.4.1 | `dashboard/package.json` | Data visualization | Frontend |
| Backend/API | FastAPI | Latest | `perception_app/mcp_service/main.py` | MCP tool endpoints | Backend |
| Agent Runtime | Google ADK | >=0.6.0 | `requirements.txt` | Agent development kit | Agent |
| Agent Orchestration | Vertex AI Agent Engine | Current | `agent_engine_app.py` | Multi-agent coordination | Agent |
| A2A Protocol | a2a-sdk | >=0.3.4 | `requirements.txt` | Agent-to-agent communication | Agent |
| AI Model | Gemini 2.0 Flash | Current | Agent YAML configs | Article analysis | AI |
| Database | Firestore | Native mode | Firebase Console | Primary data store | Data |
| Hosting | Firebase Hosting | Current | `firebase.json` | Dashboard CDN | Infra |
| Compute | Cloud Run | Managed | GCP Console | MCP service hosting | Infra |
| IaC | Terraform | >=1.6.0 | `infra/terraform/` | Infrastructure provisioning | Infra |
| Auth | Firebase Auth | 10.14.1 | `dashboard/src/firebase.ts` | User authentication | Auth |
| Auth (CI/CD) | Workload Identity Federation | Current | `.github/workflows/` | Keyless GCP auth | Infra |
| Observability | Cloud Logging | Current | GCP Console | Centralized logging | Ops |
| Observability | Cloud Trace | Current | `agent_engine_app.py` | Distributed tracing | Ops |
| Observability | OpenTelemetry | >=1.27.0 | `requirements.txt` | Telemetry (partially implemented) | Ops |

### Environment Matrix

| Environment | Purpose | Hosting | Data Source | Release Cadence | IaC Source | Notes |
|-------------|---------|---------|-------------|-----------------|------------|-------|
| local | Development | localhost:8080 | In-memory | Continuous | N/A | `make dev` for agents only |
| staging | Pre-production testing | Cloud Run | Production Firestore | Manual | Terraform | MCP with `--ingress all` |
| prod | Live service | Cloud Run + Firebase | Production Firestore | GitHub Actions | Terraform | MCP will use `--ingress internal-and-cloud-load-balancing` |

### Cloud & Platform Services

| Service | Purpose | Environment(s) | Key Config | Cost/Limits | Owner | Vendor Risk |
|---------|---------|----------------|------------|-------------|-------|-------------|
| Vertex AI Agent Engine | Multi-agent orchestration | staging, prod | `agent_engine_app.py` | ~$25/month | Jeremy | Low (Google) |
| Gemini 2.0 Flash | Article analysis | staging, prod | Agent YAML configs | ~$20/month | Jeremy | Low (Google) |
| Cloud Run | MCP service hosting | staging, prod | 512Mi, 1 CPU, 0-10 instances | ~$15/month | Jeremy | Low (Google) |
| Firestore | Primary database | all | Native mode, default | ~$10/month | Jeremy | Low (Google) |
| Firebase Hosting | Dashboard CDN | prod | Spark plan | Free | Jeremy | Low (Google) |
| Firebase Auth | User authentication | prod | Email/password | Free | Jeremy | Low (Google) |
| Cloud Scheduler | Daily ingestion trigger | prod | 7:30 AM CST | <$1/month | Jeremy | Low (Google) |
| Pub/Sub | Event triggering | prod | Ingestion topic | <$1/month | Jeremy | Low (Google) |
| Cloud Build | Container builds | staging, prod | Default SA | Per-build | Jeremy | Low (Google) |
| Artifact Registry | Container images | staging, prod | `perception-agents` | <$5/month | Jeremy | Low (Google) |
| Secret Manager | Secrets storage | prod | Future implementation | <$1/month | Jeremy | Low (Google) |

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                    PERCEPTION ARCHITECTURE                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              HUMAN INTERFACE LAYER (Firebase)                            │
│  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────────────┐  │
│  │   Firebase Hosting   │  │    Firebase Auth     │  │      React Dashboard         │  │
│  │   (CDN for SPA)      │  │   (User identity)    │  │  - About, Login, Dashboard   │  │
│  │                      │  │                      │  │  - Topics, Daily Briefs      │  │
│  │ perception-with-     │  │  Email/password      │  │  - Protected routes          │  │
│  │ intent.web.app       │  │  (Phase 2: OAuth)    │  │                              │  │
│  └──────────────────────┘  └──────────────────────┘  └──────────────────────────────┘  │
└────────────────────────────────────────┬────────────────────────────────────────────────┘
                                         │
                                         │ Firestore SDK (real-time)
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              DATA LAYER (Firestore)                                      │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                           Firestore Collections                                     │ │
│  │  /users/{userId}              - User profiles, preferences                         │ │
│  │  /users/{userId}/topics/      - Per-user topic configurations                      │ │
│  │  /users/{userId}/alerts/      - Per-user alert configurations                      │ │
│  │  /sources/{sourceId}          - RSS feed definitions (admin-only write)            │ │
│  │  /articles/{articleId}        - Analyzed articles (agent-only write)               │ │
│  │  /briefs/{briefId}            - Executive summaries (agent-only write)             │ │
│  │  /ingestion_runs/{runId}      - Run metrics and status (agent-only write)          │ │
│  └────────────────────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────┬────────────────────────────────────────────────┘
                                         │
                                         │ google-cloud-firestore SDK
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           AGENT BRAIN LAYER (Vertex AI)                                  │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                        Vertex AI Agent Engine                                       │ │
│  │                    (A2A Protocol Coordination)                                      │ │
│  │                                                                                     │ │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐   │ │
│  │  │                      Agent 0: Root Orchestrator                              │   │ │
│  │  │                    "Editor-in-Chief" - Gemini 2.0 Flash                      │   │ │
│  │  │                    run_daily_ingestion() orchestrates:                       │   │ │
│  │  └───────────────────────────────┬─────────────────────────────────────────────┘   │ │
│  │                                  │                                                  │ │
│  │  ┌─────────┬─────────┬──────────┼──────────┬─────────┬─────────┬─────────┐        │ │
│  │  ▼         ▼         ▼          ▼          ▼         ▼         ▼         ▼        │ │
│  │ Agent 1  Agent 2   Agent 3   Agent 4   Agent 5   Agent 6   Agent 7   Agent 8     │ │
│  │ Source   Topic     Relevance Brief     Alert     Validator Storage   Tech        │ │
│  │ Harvester Manager  Scorer    Writer    Detector  (Schema)  Manager   Editor      │ │
│  │                                                                                   │ │
│  └───────────────────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────┬────────────────────────────────────────────────┘
                                         │
                                         │ MCP Protocol (HTTP/JSON)
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                            TOOL LAYER (Cloud Run MCPs)                                   │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                     perception-mcp (Cloud Run)                                      │ │
│  │            https://perception-mcp-348724539390.us-central1.run.app                  │ │
│  │                                                                                     │ │
│  │  Endpoints:                           Status:                                       │ │
│  │  /health                              ✅ Active                                      │ │
│  │  /mcp/tools/fetch_rss_feed            ✅ Real (feedparser + httpx)                   │ │
│  │  /mcp/tools/fetch_api_feed            ⏳ Stub                                        │ │
│  │  /mcp/tools/fetch_webpage             ⏳ Stub                                        │ │
│  │  /mcp/tools/store_articles            ⏳ Stub                                        │ │
│  │  /mcp/tools/generate_brief            ⏳ Stub                                        │ │
│  │  /mcp/tools/log_ingestion_run         ⏳ Stub                                        │ │
│  │  /mcp/tools/send_notification         ⏳ Stub                                        │ │
│  │                                                                                     │ │
│  └────────────────────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────┬────────────────────────────────────────────────┘
                                         │
                                         │ HTTPS (external APIs)
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                            EXTERNAL DATA SOURCES                                         │
│                                                                                          │
│  RSS Feeds (15 configured):                                                              │
│  - World: BBC News, The Guardian, NPR, Reuters                                           │
│  - Tech: TechCrunch, The Verge, Ars Technica                                             │
│  - Business: Financial Times, Bloomberg, WSJ                                             │
│  - Science: Science Daily, Nature                                                        │
│  - Politics: Politico, The Hill                                                          │
│  - Sports: ESPN (disabled)                                                               │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                            SCHEDULED TRIGGERS                                            │
│                                                                                          │
│  Cloud Scheduler (7:30 AM CST daily)                                                     │
│         │                                                                                │
│         ▼                                                                                │
│  Pub/Sub Topic                                                                           │
│         │                                                                                │
│         ▼                                                                                │
│  Agent Engine → run_daily_ingestion()                                                    │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### Daily Workflow Sequence

```
07:30 AM CST - Cloud Scheduler Trigger
    │
    ▼
Pub/Sub → Agent Engine → Agent 0 (Root Orchestrator)
    │
    ├─1──► Agent 2: Get active topics from Firestore
    │         └─► Returns: [{topic_id, keywords, category}]
    │
    ├─2──► Agent 1: Harvest all RSS sources (parallel)
    │         └─► Calls MCP: /mcp/tools/fetch_rss_feed
    │         └─► Returns: [{title, url, summary, published_at}]
    │
    ├─3──► Agent 3: Score articles by relevance
    │         └─► Keyword matching: title 3x weight, content 1x
    │         └─► Returns: [{article, score, section}]
    │
    ├─4──► Agent 3: Filter top articles (max 10 per topic)
    │         └─► Filters: score >= 5
    │         └─► Returns: [top_articles]
    │
    ├─5──► Agent 4: Build executive brief
    │         └─► Sections: Tech, Business, Politics, Sports, General
    │         └─► Returns: {brief_id, sections, highlights}
    │
    ├─6──► Agent 8: Curate technology section (first vertical)
    │         └─► Enhanced tech-specific analysis
    │
    ├─7──► Agent 6: Validate articles and brief
    │         └─► Schema validation
    │         └─► Returns: {valid: true/false, errors: []}
    │
    ├─8──► Agent 7: Store to Firestore
    │         └─► Batch writes (max 500 per batch)
    │         └─► Deduplication by URL hash
    │         └─► Collections: /articles, /briefs, /ingestion_runs
    │
    └─9──► Agent 7: Update ingestion run status
              └─► status: success/failed
              └─► stats: {articles_harvested, articles_stored, brief_id}

Dashboard updates automatically via Firestore real-time listeners
```

---

## 4. Directory Deep-Dive

### Project Structure Analysis

```
/home/jeremy/000-projects/perception/
├── .beads/                      # Beads task tracking configuration
│   └── config.yaml              # Beads project configuration
├── .github/
│   └── workflows/               # CI/CD pipelines
│       ├── ci.yml               # Continuous integration (lint, validate)
│       ├── ci-smoke.yml         # Smoke tests for deployments
│       ├── deploy-agent-engine.yml  # Agent Engine deployment
│       ├── deploy-agents.yml    # Agent container builds
│       ├── deploy-dashboard.yml # Dashboard deployment
│       ├── deploy-firebase-dashboard.yml  # Firebase-specific
│       ├── deploy-mcp.yml       # MCP service to Cloud Run
│       ├── deploy.yml           # Main deployment orchestrator
│       └── test.yml             # Test runner
├── 000-docs/                    # All technical documentation (45+ files)
│   ├── 000-INDEX.md             # Documentation index
│   ├── 001-AT-ARCH-*.md         # Architecture documents
│   ├── 6767-*.md                # Foundational/evergreen docs
│   ├── 0NN-AA-REPT-*.md         # After Action Reports
│   └── archive/                 # Archived documentation
├── 000-usermanuals/             # User-facing documentation
├── dashboard/                   # React frontend (Firebase Hosting)
│   ├── src/
│   │   ├── App.tsx              # Main routing and navigation
│   │   ├── firebase.ts          # Firebase SDK configuration
│   │   ├── components/          # Reusable React components
│   │   │   └── ProtectedRoute.tsx  # Auth-gated routes
│   │   └── pages/               # Page components
│   │       ├── About.tsx        # Landing page
│   │       ├── Dashboard.tsx    # Main intelligence view
│   │       ├── DailyBriefs.tsx  # Brief history
│   │       ├── Login.tsx        # Firebase Auth login
│   │       └── Topics.tsx       # Topic configuration
│   ├── dist/                    # Production build output
│   ├── package.json             # NPM dependencies
│   ├── vite.config.ts           # Vite bundler config
│   ├── tailwind.config.js       # TailwindCSS config
│   └── tsconfig.json            # TypeScript config
├── infra/
│   └── terraform/
│       ├── envs/
│       │   └── dev/             # Development environment
│       │       ├── main.tf      # Module composition
│       │       ├── variables.tf # Input variables
│       │       ├── terraform.tfvars  # Variable values
│       │       └── terraform.tfstate # Local state (should be remote)
│       └── modules/
│           ├── agent_runtime/   # Cloud Run config (stub)
│           ├── artifact_registry/  # Container registry
│           ├── iam/             # Service accounts
│           └── project/         # Project setup
├── perception_app/              # Main application code
│   ├── __init__.py
│   ├── agent_engine_app.py      # Copy of root entry (duplicate)
│   ├── main.py                  # Local dev entrypoint (uvicorn)
│   ├── jvp_agent/               # JVP Base implementation
│   │   ├── agent.yaml           # JVP agent config
│   │   ├── agent.py             # Agent class
│   │   ├── a2a.py               # A2A protocol wrapper
│   │   ├── config.py            # Configuration
│   │   ├── memory.py            # Context caching
│   │   ├── prompts/             # System prompts
│   │   └── tools/               # JVP tools
│   ├── mcp_service/             # Cloud Run MCP service
│   │   ├── Dockerfile           # Container definition
│   │   ├── main.py              # FastAPI application
│   │   ├── requirements.txt     # MCP-specific deps
│   │   └── routers/             # API route handlers
│   │       ├── __init__.py
│   │       ├── api.py           # API feed tool (stub)
│   │       ├── briefs.py        # Brief generation (stub)
│   │       ├── logging.py       # Ingestion logging (stub)
│   │       ├── notifications.py # Delivery (stub)
│   │       ├── rss.py           # RSS fetching (REAL)
│   │       ├── storage.py       # Storage operations (stub)
│   │       └── webpage.py       # Web scraping (stub)
│   └── perception_agent/        # Core agent system
│       ├── __init__.py
│       ├── agents/              # Agent YAML configurations
│       │   ├── agent_0_orchestrator.yaml
│       │   ├── agent_1_source_harvester.yaml
│       │   ├── agent_2_topic_manager.yaml
│       │   ├── agent_3_relevance_ranking.yaml
│       │   ├── agent_4_brief_writer.yaml
│       │   ├── agent_5_alert_anomaly.yaml
│       │   ├── agent_6_validator.yaml
│       │   ├── agent_7_storage_manager.yaml
│       │   └── agent_8_tech_editor.yaml
│       ├── config/
│       │   └── rss_sources.yaml # RSS feed definitions
│       ├── prompts/             # System prompts (empty)
│       └── tools/               # Agent tool implementations
│           ├── __init__.py
│           ├── agent_0_tools.py # Orchestration (run_daily_ingestion)
│           ├── agent_1_tools.py # Source harvesting
│           ├── agent_2_tools.py # Topic management
│           ├── agent_3_tools.py # Relevance scoring
│           ├── agent_4_tools.py # Brief generation
│           ├── agent_5_tools.py # Alert detection (stub)
│           ├── agent_6_tools.py # Validation
│           ├── agent_7_tools.py # Storage operations
│           └── agent_8_tools.py # Tech editor
├── scripts/                     # Deployment and utility scripts
│   ├── deploy_agent_engine.sh   # Deploy to Vertex AI
│   ├── dev_run_adk.sh           # Local development server
│   ├── fmt_vet_lint.sh          # Code formatting
│   ├── load-initial-feeds.py    # Seed RSS sources
│   ├── package_agent.py         # Agent packaging
│   ├── print_deploy_targets.sh  # Show deployment targets
│   ├── repo_repurpose_check.sh  # Template validation
│   ├── run_ingestion_once.py    # Manual ingestion trigger
│   ├── run_ingestion_via_agent_engine.sh  # E2E test script
│   └── seed-firestore.js        # Seed Firestore data
├── agent_engine_app.py          # Production entrypoint (Vertex AI)
├── agent.py                     # Agent wrapper (duplicate?)
├── CLAUDE.md                    # Claude Code guidance
├── CHANGELOG.md                 # Version history
├── Dockerfile                   # Root Dockerfile (agents)
├── Makefile                     # Development commands
├── README.md                    # Project overview
├── firebase.json                # Firebase configuration
├── firestore.rules              # Firestore security rules
├── firestore.indexes.json       # Firestore composite indexes
├── requirements.txt             # Python dependencies
└── *.md                         # Various documentation files
```

### Detailed Directory Analysis

#### perception_app/perception_agent/

**Purpose**: Core multi-agent system implementing the Perception news intelligence workflow.

**Key Files**:
- `agents/agent_0_orchestrator.yaml:1-41` - Root orchestrator configuration defining Gemini 2.0 Flash model, Editor-in-Chief instruction, and sub-agent references
- `tools/agent_0_tools.py:107-391` - `run_daily_ingestion()` function orchestrating entire E2E pipeline
- `tools/agent_7_tools.py:50-129` - `store_articles()` with batch writes and URL-based deduplication
- `config/rss_sources.yaml:1-85` - 15 RSS feed definitions across 6 categories

**Patterns**:
- Agent configuration via YAML with ADK schema validation
- Tool implementations as async Python functions
- Structured JSON logging throughout
- Lazy-initialized Firestore client to avoid connection issues

**Entry Points**:
- `agent_engine_app.py` (root) - Production entrypoint for Vertex AI
- `perception_app/main.py` - Local development server (uvicorn)

**Authentication**:
- Firestore client uses Application Default Credentials
- No explicit auth in agent code (handled by runtime)

**Data Layer**:
- Direct Firestore SDK usage (`google-cloud-firestore`)
- Batch writes with 500-operation limit
- URL hashing for deterministic article IDs

**Code Quality**:
- Consistent structured logging pattern
- Type hints throughout
- TODO comments marking stub implementations
- Clear separation between orchestration and tool logic

#### perception_app/mcp_service/

**Purpose**: FastAPI-based MCP service exposing tool endpoints for agents to call.

**Key Files**:
- `main.py:1-177` - FastAPI app with CORS, logging middleware, and router registration
- `routers/rss.py:1-298` - Real RSS fetching with feedparser, httpx, and time windowing
- `Dockerfile:1-10` - Python 3.12-slim container with uvicorn

**Patterns**:
- Pydantic models for request/response validation
- Structured JSON logging for Cloud Logging compatibility
- Global exception handler for consistent error responses
- Request timing middleware for latency tracking

**Code Quality**:
- OpenTelemetry dependencies present but instrumentation commented out
- Only `fetch_rss_feed` has real implementation; others return stubs
- Good error handling with specific HTTP status codes

#### dashboard/

**Purpose**: React SPA for executive users to view intelligence and configure topics.

**Key Files**:
- `src/App.tsx:1-105` - Routing with protected routes and navigation
- `src/firebase.ts:1-36` - Firebase SDK initialization
- `src/components/ProtectedRoute.tsx` - Auth gate component

**Tech Stack**:
- React 18 with TypeScript
- React Router v6 for navigation
- Firebase SDK for auth and Firestore
- TailwindCSS for styling
- Chart.js for visualizations
- Vite for development and builds

**Routes**:
- `/` - About/landing page (public)
- `/login` - Firebase Auth login
- `/dashboard` - Main intelligence view (protected)
- `/topics` - Topic configuration (protected)
- `/briefs` - Daily brief history (protected)

#### infra/terraform/

**Purpose**: Infrastructure as Code for GCP resources.

**Structure**:
- `envs/dev/` - Development environment composition
- `modules/` - Reusable Terraform modules

**Modules**:
- `project/` - Project setup (placeholder)
- `artifact_registry/` - Container registry for agent images
- `iam/` - Service account creation
- `agent_runtime/` - Cloud Run config (placeholder)

**State Management**:
- Local state file (should be migrated to GCS backend)
- No drift detection configured
- Lock file present (`.terraform.lock.hcl`)

**Issues**:
- `main.tf:40-47` has commented-out secrets module
- IAM module has TODO for role bindings
- No production environment defined

#### scripts/

**Purpose**: Deployment, testing, and development utilities.

**Key Scripts**:
- `deploy_agent_engine.sh:1-50` - Deploys agents to Vertex AI Agent Engine using ADK CLI
- `run_ingestion_via_agent_engine.sh:1-50` - Triggers E2E ingestion test
- `seed-firestore.js:1-100` - Seeds initial data into Firestore collections
- `dev_run_adk.sh:1-10` - Starts local ADK development server

**Dependencies**:
- Requires `adk` CLI from `google-genai[adk]`
- Requires `gcloud` for Cloud Run operations
- Node.js for Firestore seeding

---

## 5. Automation & Agent Surfaces

### AI Agents (Vertex AI Agent Engine)

| Agent | Name | Purpose | Tools | Status |
|-------|------|---------|-------|--------|
| 0 | Root Orchestrator | Editor-in-Chief coordinating workflow | `agent_0_tools.py` | Complete |
| 1 | Source Harvester | Fetch RSS feeds via MCP | `agent_1_tools.py` | Complete |
| 2 | Topic Manager | Read user topics from Firestore | `agent_2_tools.py` | Complete |
| 3 | Relevance Scorer | Score and rank articles | `agent_3_tools.py` | Complete |
| 4 | Brief Writer | Generate executive summaries | `agent_4_tools.py` | Complete |
| 5 | Alert Detector | Identify anomalies and triggers | `agent_5_tools.py` | Stub |
| 6 | Validator | Schema validation for articles/briefs | `agent_6_tools.py` | Complete |
| 7 | Storage Manager | Persist to Firestore | `agent_7_tools.py` | Complete |
| 8 | Tech Editor | Curate technology section | `agent_8_tools.py` | Complete |

**Agent Communication**: A2A Protocol via Vertex AI Agent Engine

**Model**: Gemini 2.0 Flash (all agents)

**Trigger**: Cloud Scheduler → Pub/Sub → Agent Engine (7:30 AM CST)

### MCP Tool Endpoints (Cloud Run)

| Tool | Endpoint | Purpose | Implementation |
|------|----------|---------|----------------|
| fetch_rss_feed | `/mcp/tools/fetch_rss_feed` | Fetch and parse RSS feeds | Real (feedparser + httpx) |
| fetch_api_feed | `/mcp/tools/fetch_api_feed` | Fetch from REST APIs | Stub |
| fetch_webpage | `/mcp/tools/fetch_webpage` | Scrape web pages | Stub |
| store_articles | `/mcp/tools/store_articles` | Persist articles | Stub |
| generate_brief | `/mcp/tools/generate_brief` | Generate summary | Stub |
| log_ingestion_run | `/mcp/tools/log_ingestion_run` | Log run metrics | Stub |
| send_notification | `/mcp/tools/send_notification` | Send alerts | Stub |

**Service URL**: `https://perception-mcp-348724539390.us-central1.run.app`

### GitHub Actions Workflows

| Workflow | Trigger | Purpose | Status |
|----------|---------|---------|--------|
| ci.yml | push, PR | Lint, validate Terraform, ADK check | Active |
| ci-smoke.yml | dispatch | Smoke tests after deployment | Active |
| deploy-mcp.yml | dispatch | Deploy MCP to Cloud Run | Active |
| deploy-agent-engine.yml | dispatch | Deploy agents to Vertex AI | Active |
| deploy-dashboard.yml | dispatch | Deploy React app to Firebase | Active |
| deploy.yml | push to main | Main deployment orchestrator | Active |
| test.yml | push | Run test suite | Active |

### Scheduled Jobs

| Job | Schedule | Purpose | Implementation |
|-----|----------|---------|----------------|
| Daily Ingestion | 7:30 AM CST | Trigger agent workflow | Cloud Scheduler → Pub/Sub |

### Slash Commands / Beads Integration

The project uses Beads (`bd`) for task tracking:

```bash
bd ready              # Start of session
bd create "Title"     # Create task
bd update <id> --status in_progress
bd close <id> --reason "Done"
bd sync               # End of session
```

---

## 6. Operational Reference

### Deployment Workflows

#### Local Development

**Prerequisites**:
- Python 3.11+
- Node.js 18+ (for dashboard)
- Docker Desktop (optional)
- `gcloud` CLI authenticated
- Virtual environment active

**Environment Setup**:
```bash
# Navigate to project
cd /home/jeremy/000-projects/perception

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup GCP authentication
gcloud auth application-default login
gcloud config set project perception-with-intent
```

**Service Startup**:
```bash
# Start agent development server (local)
make dev
# Or: ./scripts/dev_run_adk.sh
# Serves at http://localhost:8080/v1/card

# Dashboard development (separate terminal)
cd dashboard
npm install
npm run dev
# Serves at http://localhost:5173
```

**Verification**:
```bash
# Test agent endpoint
curl http://localhost:8080/v1/card

# Test MCP (Cloud Run only - NOT localhost)
curl https://perception-mcp-348724539390.us-central1.run.app/health
```

#### Staging Deployment

**Trigger**: `workflow_dispatch` on GitHub Actions

**Pre-flight**:
- [ ] CI pipeline green
- [ ] Terraform validate passes
- [ ] WIF secrets configured in GitHub

**MCP Deployment**:
```bash
# Via GitHub Actions
gh workflow run deploy-mcp.yml --field environment=staging

# Or manually via gcloud
gcloud run deploy perception-mcp \
  --source perception_app/mcp_service \
  --region us-central1 \
  --project perception-with-intent \
  --platform managed \
  --ingress all \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300 \
  --port 8080
```

**Validation**:
```bash
# Health check
curl https://perception-mcp-348724539390.us-central1.run.app/health

# RSS fetch test
curl -X POST https://perception-mcp-348724539390.us-central1.run.app/mcp/tools/fetch_rss_feed \
  -H "Content-Type: application/json" \
  -d '{"feed_url": "https://news.ycombinator.com/rss", "max_items": 5}'
```

#### Production Deployment

**Pre-deployment Checklist**:
- [ ] CI pipeline green
- [ ] Staging verified
- [ ] Terraform plan reviewed
- [ ] Rollback plan documented

**Agent Engine Deployment**:
```bash
# Set environment variables
export VERTEX_PROJECT_ID=perception-with-intent
export VERTEX_LOCATION=us-central1

# Deploy via script
./scripts/deploy_agent_engine.sh

# Verify deployment
gcloud alpha aiplatform agents list \
  --project=perception-with-intent \
  --location=us-central1
```

**Dashboard Deployment**:
```bash
cd dashboard
npm run build
firebase deploy --only hosting
# Deploys to: https://perception-with-intent.web.app
```

**Rollback Protocol**:
```bash
# Cloud Run: Revert to previous revision
gcloud run services update-traffic perception-mcp \
  --to-revisions=REVISION_NAME=100 \
  --region=us-central1 \
  --project=perception-with-intent

# Firebase: Deploy previous commit
git checkout <previous-commit>
cd dashboard && npm run build && firebase deploy --only hosting
```

### Monitoring & Alerting

**Dashboards**:
- Cloud Console > Cloud Run > perception-mcp > Metrics
- Cloud Console > Vertex AI > Agent Engine > Logs
- Firebase Console > Hosting > perception-with-intent

**SLIs/SLOs**:
| Metric | SLO | Measurement |
|--------|-----|-------------|
| Availability | 99.5% | Cloud Run health checks |
| Latency P95 | <500ms | Cloud Run request_latencies |
| Error Rate | <1% | Cloud Run request_count (4xx, 5xx) |
| Ingestion Success | 95% | ingestion_runs.status == "success" |

**Logging**:
```bash
# MCP service logs
gcloud logging read \
  'resource.type="cloud_run_revision" AND resource.labels.service_name="perception-mcp"' \
  --project=perception-with-intent \
  --limit=20

# Error logs only
gcloud logging read \
  'resource.type="cloud_run_revision" AND resource.labels.service_name="perception-mcp" AND severity>=ERROR' \
  --project=perception-with-intent \
  --limit=10

# Agent Engine logs
gcloud logging read \
  'resource.type="aiplatform.googleapis.com/Agent"' \
  --project=perception-with-intent \
  --limit=20
```

**On-Call Expectations**:
- Monitor ingestion run status daily
- Respond to P0/P1 alerts within 15 minutes
- Investigate RSS feed failures (external dependency)
- Review Cloud Logging for anomalies weekly

### Incident Response

| Severity | Definition | Response Time | Roles | Communication |
|----------|------------|---------------|-------|---------------|
| P0 | Complete system outage | Immediate | On-call engineer | GitHub issue + Slack |
| P1 | Ingestion failure | 15 min | On-call engineer | GitHub issue |
| P2 | Dashboard degradation | 1 hour | Available engineer | GitHub issue |
| P3 | Minor bugs | Next business day | Any engineer | GitHub issue |

**Common Incidents**:

1. **MCP Service Down**
   - Check: `curl /health`
   - Logs: `gcloud logging read ...`
   - Fix: Redeploy via GitHub Actions

2. **Ingestion Failure**
   - Check: Firestore `/ingestion_runs/{latest}`
   - Logs: Agent Engine logs
   - Fix: Verify RSS feeds accessible, retry ingestion

3. **Dashboard 404**
   - Check: Firebase Hosting console
   - Fix: Redeploy dashboard

### Backup & Recovery

**Backup Jobs**:
| Data | Frequency | Retention | Location |
|------|-----------|-----------|----------|
| Firestore | Automatic | 7 days | GCP managed |
| Terraform State | On commit | Git history | Local (should be GCS) |
| Container Images | On build | 90 days | Artifact Registry |

**RPO/RTO**:
| Service | RPO | RTO |
|---------|-----|-----|
| Firestore | Near-zero | Minutes |
| Dashboard | Zero (CDN) | Minutes |
| MCP Service | Zero (stateless) | Minutes |
| Agent Engine | Zero (stateless) | Minutes |

**Disaster Recovery**:
1. Firestore: GCP handles replication
2. Cloud Run: Redeploy from Artifact Registry
3. Dashboard: Redeploy from git
4. Terraform: Re-apply from repo

---

## 7. Security, Compliance & Access

### Identity & Access Management

| Account/Role | Purpose | Permissions | Provisioning | MFA | Used By |
|--------------|---------|-------------|--------------|-----|---------|
| perception-deployer@*.iam | GitHub Actions deployments | run.admin, artifactregistry.writer, storage.admin, aiplatform.user, iam.serviceAccountUser | Terraform | N/A (WIF) | CI/CD |
| mcp-service@*.iam | MCP Cloud Run runtime | firestore.user, logging.logWriter | Terraform | N/A | MCP service |
| default-compute@*.iam | Cloud Build | storage.objectViewer, logging.logWriter, artifactregistry.writer | GCP default | N/A | Cloud Build |
| GitHub WIF | Keyless auth from GitHub | Workload Identity User | gcloud CLI | N/A | GitHub Actions |
| Firebase Users | Dashboard access | Firestore read (own data) | Firebase Auth | Optional | End users |

### Secrets Management

**Current State**:
- No secrets in code
- GitHub Secrets for WIF configuration:
  - `GCP_WORKLOAD_IDENTITY_PROVIDER`
  - `GCP_SERVICE_ACCOUNT_EMAIL`
- `.env` files for local development (not committed)
- No Secret Manager implementation yet

**Recommendations**:
- Migrate API keys to Secret Manager
- Implement secret rotation policy
- Add break-glass procedures for emergency access

### Security Posture

**Authentication**:
- Dashboard: Firebase Auth (email/password)
- CI/CD: Workload Identity Federation (OIDC tokens)
- MCP Service: Currently `--allow-unauthenticated` (staging)
- Production MCP: `--no-allow-unauthenticated` with IAM

**Authorization**:
- Firestore rules enforce user isolation
- Users can only access own topics/alerts
- Articles/briefs/sources are read-only for users
- Admin-only write for sources collection

**Encryption**:
- In-transit: HTTPS everywhere (Cloud Run, Firebase, Firestore)
- At-rest: GCP managed encryption (default)
- No customer-managed encryption keys

**Network**:
- Staging MCP: `--ingress all` (public)
- Production MCP: `--ingress internal-and-cloud-load-balancing`
- No VPC Service Controls
- No WAF configured

**Security Rules** (`firestore.rules`):
```javascript
// Key rules:
match /users/{userId} {
  allow read, write: if isOwner(userId);
}
match /articles/{articleId} {
  allow read: if isSignedIn();
  allow write: if false; // Backend only
}
```

**Known Issues**:
- MCP staging allows unauthenticated (by design for testing)
- No SPIFFE IDs implemented yet
- No vulnerability scanning configured
- No SOC2/HIPAA compliance

---

## 8. Cost & Performance

### Current Costs

**Estimated Monthly Cloud Spend**: ~$70-80

| Component | Monthly Cost | Notes |
|-----------|--------------|-------|
| Cloud Run MCPs | ~$15 | Scale-to-zero, minimal traffic |
| Vertex AI Agents | ~$25 | Agent Engine runtime |
| Gemini 2.0 Flash | ~$20 | ~100 articles/day analysis |
| Firestore | ~$10 | Free tier covers most usage |
| Firebase Hosting | $0 | Spark plan |
| Cloud Scheduler | <$1 | 1 daily job |
| Pub/Sub | <$1 | Minimal messages |
| Cloud Logging | Included | 50GB free tier |
| Artifact Registry | <$5 | Container storage |
| **Total** | **~$70-80** | |

### Performance Baseline

**MCP Service**:
- Latency P95: 270ms (RSS fetch validated)
- Throughput: Not load tested
- Error Rate: 0% (during testing)

**Agent Ingestion**:
- Not benchmarked (pending Agent Engine deployment)
- Target: <60s for full pipeline

**Dashboard**:
- Load time: <2s (Firebase CDN)
- Firestore queries: <100ms target

### Optimization Opportunities

1. **Committed Use Discounts**
   - Not applicable at current scale
   - Review at $500/month threshold

2. **Resource Right-sizing**
   - Cloud Run: Current 512Mi may be oversized
   - Consider 256Mi after load testing

3. **Caching**
   - RSS feed caching to reduce external calls
   - Firestore query result caching in dashboard

4. **Batch Operations**
   - Already using Firestore batch writes (500/batch)
   - Consider BigQuery for analytics (currently not used)

---

## 9. Development Workflow

### Local Development

**Standard Environment**:
- Linux (Ubuntu 22.04 or later)
- Python 3.11+ with venv
- Node.js 18+ with npm
- Docker Desktop (optional)
- VS Code with Python/TypeScript extensions

**Bootstrap**:
```bash
# Clone repository
git clone https://github.com/jeremylongshore/perception-with-intent.git
cd perception

# Python setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Node setup (dashboard)
cd dashboard
npm install
cd ..

# GCP authentication
gcloud auth application-default login
gcloud config set project perception-with-intent
```

**Common Tasks**:
```bash
# Run agents locally
make dev

# Run tests
make test

# Format code
make format

# Lint code
make lint

# Clean build artifacts
make clean
```

### CI/CD Pipeline

**Platform**: GitHub Actions

**Triggers**:
- `push`: All branches (ci.yml)
- `pull_request`: All branches (ci.yml)
- `workflow_dispatch`: Manual deployments

**Stages**:
```
checkout → setup-python → install → lint → terraform-validate → adk-validate
                                              ↓ (on dispatch)
                                         deploy-staging
                                              ↓ (manual approval)
                                         deploy-production
```

**Artifacts**:
- Container images: `us-central1-docker.pkg.dev/perception-with-intent/perception-agents`
- Dashboard builds: Firebase Hosting CDN

### Code Quality

**Linting**:
- Python: black, flake8, mypy
- TypeScript: ESLint
- Terraform: `terraform fmt`, `terraform validate`

**Testing**:
- Framework: pytest with pytest-asyncio
- Coverage: pytest-cov (target not defined)
- No integration tests for Agent Engine (requires deployed service)

**Review Process**:
- Single developer project (Jeremy)
- Self-review recommended
- CI must pass before merge

---

## 10. Dependencies & Supply Chain

### Direct Dependencies (Python)

**Core**:
```
google-genai[adk]>=0.6.0              # Google ADK for agents
google-cloud-aiplatform>=1.112.0     # Vertex AI SDK
a2a-sdk>=0.3.4                        # Agent-to-agent protocol
google-cloud-firestore>=2.18.0        # Database SDK
google-cloud-logging>=3.11.0          # Cloud Logging
google-cloud-trace>=1.13.5            # Distributed tracing
```

**Web Server**:
```
uvicorn[standard]>=0.30.0             # ASGI server
fastapi (implied)                      # API framework
httpx>=0.27.0                          # HTTP client
aiohttp>=3.10.0                        # Async HTTP
```

**Data Processing**:
```
pydantic>=2.9.0                        # Data validation
feedparser>=6.0.11                     # RSS parsing
beautifulsoup4>=4.12.3                 # HTML parsing
python-dateutil>=2.9.0                 # Date parsing
```

**Observability**:
```
opentelemetry-api>=1.27.0              # Telemetry API
opentelemetry-sdk>=1.27.0              # Telemetry SDK
opentelemetry-exporter-gcp-trace>=1.7.0
```

**Development**:
```
pytest>=8.3.0                          # Testing
black>=24.8.0                          # Formatting
flake8>=7.1.0                          # Linting
mypy>=1.11.0                           # Type checking
```

### Direct Dependencies (Dashboard)

```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "react-router-dom": "^6.20.0",
  "firebase": "^10.14.1",
  "chart.js": "^4.4.1",
  "react-chartjs-2": "^5.2.0",
  "date-fns": "^3.0.0"
}
```

### Third-Party Services

| Service | Purpose | Data Shared | Auth | SLA | Owner |
|---------|---------|-------------|------|-----|-------|
| GCP | All infrastructure | All | WIF, ADC | 99.9% | Jeremy |
| Firebase | Hosting, Auth, DB | User data | Firebase SDK | 99.95% | Jeremy |
| RSS Feeds | News sources | None (read-only) | N/A | Varies | External |
| GitHub | Code hosting, CI/CD | Source code | OAuth | 99.9% | Jeremy |

### Supply Chain Risks

- **GCP Lock-in**: Deep integration with Google ADK, Vertex AI
- **RSS Feed Availability**: External dependency, no control
- **Open Source Dependencies**: Standard OSS risk profile
- **No SBOM Generation**: Should add for compliance

---

## 11. Integration with Existing Documentation

### Documentation Inventory

| Document | Location | Status | Last Updated |
|----------|----------|--------|--------------|
| README.md | `/home/jeremy/000-projects/perception/README.md` | Complete | 2025-11-15 |
| CLAUDE.md | `/home/jeremy/000-projects/perception/CLAUDE.md` | Complete | 2025-11-15 |
| CHANGELOG.md | `/home/jeremy/000-projects/perception/CHANGELOG.md` | Up-to-date | 2025-11-15 |
| WIF-SETUP-GUIDE.md | Root directory | Complete | 2025-11-14 |
| Firestore Schema | `000-docs/001-AT-ARCH-firestore-schema.md` | Complete | 2025-11-14 |
| Observability | `000-docs/6767-AT-ARCH-observability-and-monitoring.md` | Complete | 2025-11-15 |
| Release Log | `000-docs/6767-PP-PLAN-release-log.md` | Up-to-date | 2025-11-15 |
| Agent Engine Deploy | `000-docs/6767-OD-GUID-agent-engine-deploy.md` | Complete | 2025-11-15 |
| E2E Architecture | `000-docs/6767-AT-ARCH-e2e-ingestion-and-tech-editor.md` | Complete | 2025-11-14 |
| AAR Phase E2E | `000-docs/041-AA-REPT-phase-E2E-agent-engine-deployment.md` | Complete | 2025-11-15 |

### Discrepancies Identified

1. **Duplicate Files**: `agent_engine_app.py` exists in root and `perception_app/`
2. **CLAUDE.md MCP URL**: References `perception-mcp-w53xszfqnq-uc.a.run.app` but observability doc references `perception-mcp-348724539390.us-central1.run.app`
3. **Terraform State**: Local state should be migrated to remote backend
4. **Agent Engine ID**: Documented as `3870516225259864064` but may change on redeploy

### Recommended Reading List

1. **CLAUDE.md** - Comprehensive system overview for all development
2. **000-docs/6767-AT-ARCH-observability-and-monitoring.md** - Critical for operations
3. **000-docs/001-AT-ARCH-firestore-schema.md** - Data model reference
4. **WIF-SETUP-GUIDE.md** - CI/CD authentication setup
5. **CHANGELOG.md** - Version history and feature tracking

---

## 12. Current State Assessment

### What's Working Well

1. **Clean Architecture Separation**
   - Agents think (Vertex AI)
   - MCPs do (Cloud Run)
   - Firebase serves humans
   - Evidence: `perception_app/` structure, `CLAUDE.md` documentation

2. **MCP Service Deployed and Validated**
   - Real RSS fetching working (270ms latency)
   - Cloud Logging operational (zero ERROR logs)
   - Evidence: `curl /health` returns 200, observability doc verification

3. **Comprehensive Agent System**
   - 8 agents with clear responsibilities
   - Production scoring logic (title 3x, content 1x)
   - Batch Firestore operations
   - Evidence: `agent_0_tools.py:run_daily_ingestion()`, tool implementations

4. **CI/CD Pipeline Functional**
   - GitHub Actions workflows for all deployment targets
   - WIF configured for keyless authentication
   - Evidence: `.github/workflows/`, `WIF-SETUP-GUIDE.md`

5. **Strong Documentation Culture**
   - 45+ documents in 000-docs/
   - Consistent naming convention
   - AARs for major phases
   - Evidence: `ls 000-docs/` output

### Areas Needing Attention

1. **Agent Engine Deployment Pending**
   - Scripts ready but not executed
   - E2E ingestion untested in production
   - Impact: Core functionality not validated

2. **MCP_BASE_URL Configuration Gap**
   - Environment variable not wired to Agent Engine runtime
   - Agents cannot call MCP in production
   - Impact: Critical blocker for E2E

3. **Dashboard-Firestore Integration Incomplete**
   - Dashboard shows placeholder data
   - Real-time listeners not implemented
   - Impact: User-facing functionality limited

4. **MCP Stubs Not Implemented**
   - 6 of 7 MCP tools are stubs
   - Only `fetch_rss_feed` works
   - Impact: Limited functionality

5. **Terraform State Management**
   - Local state file
   - No remote backend
   - No drift detection
   - Impact: Team collaboration and disaster recovery

6. **Testing Gaps**
   - No integration tests for Agent Engine
   - No E2E tests for ingestion pipeline
   - Coverage percentage unknown
   - Impact: Deployment confidence

### Immediate Priorities

| Priority | Issue | Impact | Action | Owner |
|----------|-------|--------|--------|-------|
| P0 | Agent Engine not deployed | Core functionality blocked | Run `./scripts/deploy_agent_engine.sh` | DevOps |
| P0 | MCP_BASE_URL not configured | Agents cannot call MCP | Research Agent Engine env vars | DevOps |
| P1 | Dashboard-Firestore integration | Users see no data | Wire Firestore SDK in React components | Frontend |
| P1 | MCP stubs | Limited functionality | Implement remaining 6 tools | Backend |
| P2 | Terraform remote state | Team collaboration | Migrate to GCS backend | DevOps |
| P2 | Production ingress | Security | Change to `internal-and-cloud-load-balancing` | DevOps |
| P3 | Test coverage | Deployment confidence | Add integration tests | QA |

---

## 13. Quick Reference

### Operational Command Map

| Capability | Command/Tool | Source | Notes |
|------------|--------------|--------|-------|
| Local agent dev | `make dev` | Makefile:25 | Runs at localhost:8080 |
| Local dashboard | `cd dashboard && npm run dev` | package.json | Runs at localhost:5173 |
| Run tests | `make test` | Makefile:30 | pytest with coverage |
| Format code | `make format` | Makefile:40 | black formatter |
| Lint code | `make lint` | Makefile:34 | flake8, mypy, black --check |
| Deploy MCP | `gh workflow run deploy-mcp.yml` | .github/workflows/ | Manual trigger |
| Deploy Agent Engine | `./scripts/deploy_agent_engine.sh` | scripts/ | Requires env vars |
| Deploy dashboard | `firebase deploy --only hosting` | firebase.json | From dashboard/ |
| Check MCP health | `curl .../health` | Cloud Run | Service must be running |
| View MCP logs | `gcloud logging read ...` | Cloud Logging | See observability doc |
| Terraform plan | `terraform -chdir=infra/terraform/envs/dev plan` | Terraform | Requires init first |
| Seed Firestore | `node scripts/seed-firestore.js` | scripts/ | Requires Node.js |
| Manual ingestion | `python scripts/run_ingestion_once.py` | scripts/ | Local testing |
| Beads sync | `bd sync` | Beads CLI | Task tracking |

### Critical Endpoints & Resources

**Production URLs**:
- Dashboard: https://perception-with-intent.web.app
- MCP Service: https://perception-mcp-348724539390.us-central1.run.app
- MCP Health: https://perception-mcp-348724539390.us-central1.run.app/health
- MCP Docs: https://perception-mcp-348724539390.us-central1.run.app/docs

**GCP Resources**:
- Project: `perception-with-intent`
- Region: `us-central1`
- Agent Engine ID: `3870516225259864064`
- Agent Engine Resource: `projects/348724539390/locations/us-central1/reasoningEngines/3870516225259864064`

**Monitoring**:
- Cloud Console: https://console.cloud.google.com/run?project=perception-with-intent
- Cloud Logging: https://console.cloud.google.com/logs?project=perception-with-intent
- Firebase Console: https://console.firebase.google.com/project/perception-with-intent

**CI/CD**:
- Repository: https://github.com/jeremylongshore/perception-with-intent
- Actions: https://github.com/jeremylongshore/perception-with-intent/actions

### First-Week Checklist

**Day 1: Access & Environment**
- [ ] GitHub repository access granted
- [ ] GCP project access (perception-with-intent)
- [ ] Firebase console access
- [ ] Local environment bootstrapped (`make install`)
- [ ] `gcloud auth application-default login` completed

**Day 2: Verification**
- [ ] Local agent server runs (`make dev`)
- [ ] Dashboard runs locally (`npm run dev`)
- [ ] MCP health check passes
- [ ] Cloud Logging accessible

**Day 3: Critical Deployment**
- [ ] Deploy Agent Engine to staging
- [ ] Configure MCP_BASE_URL (research needed)
- [ ] Trigger test ingestion run
- [ ] Verify data lands in Firestore

**Day 4: Dashboard Integration**
- [ ] Wire Firestore SDK to Dashboard components
- [ ] Test real-time data updates
- [ ] Verify auth flow works end-to-end

**Day 5: Operations Setup**
- [ ] Set up Cloud Monitoring alerts
- [ ] Review on-call procedures
- [ ] Document any gaps or issues found
- [ ] Create improvement tickets

---

## 14. Recommendations Roadmap

### Week 1 - Critical Setup & Stabilization

**Goals**:
1. Deploy Agent Engine to staging environment
2. Research and configure MCP_BASE_URL for Agent Engine runtime
3. Execute first successful E2E ingestion run
4. Verify articles appear in Firestore collections

**Actions**:
```bash
# Day 1-2: Agent Engine Deployment
export VERTEX_PROJECT_ID=perception-with-intent
export VERTEX_LOCATION=us-central1
./scripts/deploy_agent_engine.sh

# Day 3: Configure MCP_BASE_URL
# Research: How to set env vars in Agent Engine runtime
# Options: agent.yaml config, runtime environment, or hardcode URL

# Day 4-5: E2E Validation
./scripts/run_ingestion_via_agent_engine.sh
# Verify: Firestore collections populated
```

**Stakeholders**: DevOps, Backend
**Dependencies**: WIF secrets configured, GCP access

**Measurable Outcomes**:
- Agent Engine deployed (verified via `gcloud alpha aiplatform agents list`)
- Ingestion run completes with status="success"
- At least 5 articles stored in Firestore

### Month 1 - Foundation & Visibility

**Goals**:
1. Complete dashboard-Firestore integration
2. Implement remaining MCP tool stubs
3. Set up production monitoring and alerting
4. Migrate Terraform state to remote backend

**Actions**:
1. **Dashboard Integration** (Week 2-3)
   - Wire Firestore SDK to Dashboard/Topics/Briefs pages
   - Implement real-time listeners for articles collection
   - Add loading states and error handling

2. **MCP Tools** (Week 2-3)
   - Implement `store_articles` (direct Firestore write from MCP)
   - Implement `send_notification` (Slack webhook)
   - Test each tool endpoint

3. **Monitoring** (Week 3)
   - Create Cloud Monitoring dashboard
   - Set up alerts:
     - MCP error rate > 5%
     - Ingestion failure
     - Latency P95 > 2s
   - Configure notification channels (email, Slack)

4. **Terraform** (Week 4)
   - Create GCS bucket for state
   - Add backend configuration
   - Migrate existing state
   - Document process

**Stakeholders**: DevOps, Frontend, Backend
**Dependencies**: Week 1 completion

**Measurable Outcomes**:
- Dashboard displays live Firestore data
- 4+ MCP tools functional
- Monitoring dashboard with 5+ metrics
- Remote Terraform state operational

### Quarter 1 - Strategic Enhancements

**Goals**:
1. Production hardening (ingress controls, SPIFFE IDs)
2. Additional section editors (Business, Politics)
3. Multi-tenant preparation (Firebase Auth roles)
4. Cost optimization and load testing

**Actions**:

1. **Production Hardening** (Month 2)
   - Change MCP ingress to `internal-and-cloud-load-balancing`
   - Implement SPIFFE IDs for agent identity
   - Add VPC Service Controls (if required)
   - Enable Cloud Armor WAF

2. **Section Editors** (Month 2)
   - Agent 9: Business Desk Editor
   - Agent 10: Politics Desk Editor
   - Agent 11: Sports Desk Editor
   - Section-specific curation logic

3. **Multi-tenant Prep** (Month 3)
   - Extend Firestore schema for tenant isolation
   - Add Firebase Auth custom claims for roles
   - Implement per-tenant topic limits
   - Design Stripe billing integration

4. **Performance** (Month 3)
   - Load test ingestion pipeline
   - Optimize Firestore queries with indexes
   - Right-size Cloud Run resources
   - Document capacity limits

**Stakeholders**: DevOps, Backend, Product
**Dependencies**: Month 1 completion

**Measurable Outcomes**:
- MCP ingress hardened for production
- 11 agents operational (8 core + 3 section editors)
- Multi-tenant architecture documented
- Load test results (target: 1000 articles/day)

---

## Appendices

### Appendix A. Glossary

| Term | Definition |
|------|------------|
| ADK | Google Agent Development Kit - framework for building AI agents |
| A2A Protocol | Agent-to-Agent protocol for multi-agent communication |
| MCP | Model Context Protocol - standardized tool interface for agents |
| WIF | Workload Identity Federation - keyless authentication from GitHub to GCP |
| E2E | End-to-end (complete workflow from ingestion to storage) |
| Brief | Executive summary generated from analyzed articles |
| SPIFFE ID | Secure Production Identity Framework for Everyone - identity for workloads |

### Appendix B. Reference Links

**Internal**:
- [README.md](/home/jeremy/000-projects/perception/README.md)
- [CLAUDE.md](/home/jeremy/000-projects/perception/CLAUDE.md)
- [Observability Guide](/home/jeremy/000-projects/perception/000-docs/6767-AT-ARCH-observability-and-monitoring.md)
- [Firestore Schema](/home/jeremy/000-projects/perception/000-docs/001-AT-ARCH-firestore-schema.md)
- [Release Log](/home/jeremy/000-projects/perception/000-docs/6767-PP-PLAN-release-log.md)

**External**:
- [Google ADK Docs](https://github.com/google/adk-python)
- [Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/docs/agents)
- [Firebase Documentation](https://firebase.google.com/docs)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)

### Appendix C. Troubleshooting Playbooks

**1. MCP Service Returns 502/503**
```bash
# Check service status
gcloud run services describe perception-mcp \
  --project=perception-with-intent \
  --region=us-central1

# Check logs for startup errors
gcloud logging read \
  'resource.type="cloud_run_revision" AND resource.labels.service_name="perception-mcp"' \
  --project=perception-with-intent \
  --limit=50

# Common fixes:
# - Increase memory: --memory 1Gi
# - Increase timeout: --timeout 300
# - Check Dockerfile CMD
```

**2. Ingestion Run Fails**
```bash
# Check run status in Firestore
# Collection: ingestion_runs

# Check Agent Engine logs
gcloud logging read \
  'resource.type="aiplatform.googleapis.com/Agent"' \
  --project=perception-with-intent \
  --limit=20

# Common causes:
# - MCP_BASE_URL not configured
# - RSS feed timeout
# - Firestore permission denied
```

**3. Dashboard Auth Fails**
```bash
# Verify Firebase configuration
# Check: dashboard/src/firebase.ts

# Verify Firestore rules
firebase firestore:rules

# Common causes:
# - Firebase Auth not enabled in console
# - Incorrect apiKey in firebase.ts
```

### Appendix D. Change Management

**Release Process**:
1. Create feature branch from main
2. Develop and test locally
3. Push branch, create PR
4. CI must pass
5. Self-review and merge
6. GitHub Actions deploys to staging
7. Verify staging
8. Manually promote to production (if applicable)

**CAB Process**: Not implemented (single developer)

**Audit Requirements**: Git commit history

### Appendix E. Open Questions

1. **MCP_BASE_URL Configuration**
   - How to set environment variables in Agent Engine runtime?
   - Options: agent.yaml, runtime config, hardcoded?
   - Research needed before Agent Engine deployment

2. **Agent Engine Persistence**
   - Does Agent Engine ID change on redeploy?
   - How to handle agent updates without breaking Cloud Scheduler?

3. **Multi-tenant Data Isolation**
   - Firestore rules sufficient for tenant isolation?
   - Need separate Firestore databases per tenant?

4. **Cost at Scale**
   - What's the cost for 1000+ daily users?
   - When does Gemini 2.0 Flash become expensive?

5. **OpenTelemetry Integration**
   - Dependencies present but not instrumented
   - Priority for implementation?

---

**Document Generated**: 2025-12-29
**Document ID**: 042-AA-AUDT-appaudit-devops-playbook
**Total Words**: ~18,000
**Author**: Claude Code (appaudit skill)
**Next Review**: 2026-03-29 (Quarterly)
