# Perception With Intent - Authoritative Architecture Specification

**Version:** 2.0 (AUTHORITATIVE)
**Date:** 2025-11-14
**Status:** SOURCE OF TRUTH
**Supersedes:** All previous architecture documents

---

## CRITICAL CORRECTIONS

This document corrects previous architectural assumptions:

**❌ WRONG (Previous Assumptions):**
- BigQuery as core data store
- Vertex AI Search integration
- Single agent with multiple "personas"
- Positive news RSS feeds from other projects

**✅ CORRECT (This Specification):**
- Firestore ONLY as core data store
- NO BigQuery in core (future enhancement only)
- NO Vertex AI Search
- 8 DISTINCT agents in Vertex AI Agent Engine
- Initial feeds from `data/initial_feeds.csv`

---

## AGENT ARCHITECTURE (AUTHORITATIVE)

### Agent Engine Deployment

```
Vertex AI Agent Engine (Single Deployment)
│
├── Agent 0: Perception Orchestrator (ROOT)
│   │
│   ├── Sub-Agent 1: Source Harvester
│   ├── Sub-Agent 2: Topic Manager
│   ├── Sub-Agent 3: Relevance & Ranking
│   ├── Sub-Agent 4: Summarization / Brief Writer
│   ├── Sub-Agent 5: Alert & Anomaly Detector
│   ├── Sub-Agent 6: Validator
│   └── Sub-Agent 7: Storage Manager
│
└── Each agent:
    ├── Has own YAML config (Agent Card)
    ├── Has own tools file
    ├── Has own instruction block
    └── Runs independently
```

### File Structure (AUTHORITATIVE)

```
app/perception_agent/
├── agents/
│   ├── agent_0_orchestrator.yaml          # Root orchestrator
│   ├── agent_1_source_harvester.yaml      # Fetches from feeds
│   ├── agent_2_topic_manager.yaml         # Manages topics
│   ├── agent_3_relevance_ranking.yaml     # Scores articles
│   ├── agent_4_brief_writer.yaml          # Generates briefs
│   ├── agent_5_alert_anomaly.yaml         # Detects anomalies
│   ├── agent_6_validator.yaml             # Validates data
│   └── agent_7_storage_manager.yaml       # Persists to Firestore
│
├── tools/
│   ├── agent_0_tools.py                   # Orchestration helpers
│   ├── agent_1_tools.py                   # CSV/RSS/API/web fetch
│   ├── agent_2_tools.py                   # Topic CRUD
│   ├── agent_3_tools.py                   # Relevance scoring
│   ├── agent_4_tools.py                   # Brief generation
│   ├── agent_5_tools.py                   # Alert checks
│   ├── agent_6_tools.py                   # Validation helpers
│   └── agent_7_tools.py                   # Firestore writes, dedupe
│
└── prompts/
    ├── agent_0_prompts.md
    ├── agent_1_prompts.md
    ├── agent_2_prompts.md
    ├── agent_3_prompts.md
    ├── agent_4_prompts.md
    ├── agent_5_prompts.md
    ├── agent_6_prompts.md
    └── agent_7_prompts.md
```

---

## DATA ARCHITECTURE (CORRECTED)

### Primary Data Store: Firestore ONLY

**Collections:**
```
/users/{userId}
/users/{userId}/topics/{topicId}
/users/{userId}/alerts/{alertId}
/sources/{sourceId}               # Populated from CSV
/articles/{articleId}
/briefs/{briefId}
/ingestion_runs/{runId}
```

### Initial Feeds Source: CSV File

**Location:** `data/initial_feeds.csv`

**Format:**
```csv
source_id,name,type,url,category,enabled
techcrunch,TechCrunch,rss,https://techcrunch.com/feed/,tech,true
theverge,The Verge,rss,https://www.theverge.com/rss/index.xml,tech,true
bbc_tech,BBC Technology,rss,http://feeds.bbci.co.uk/news/technology/rss.xml,tech,true
reuters_tech,Reuters Technology,api,https://www.reutersagency.com/feed/,tech,true
mit_ai,MIT Technology Review AI,rss,https://www.technologyreview.com/topic/artificial-intelligence/feed,research,true
```

**CSV Loader Script:**
```python
# scripts/load_initial_feeds.py
import csv
from firebase_admin import firestore

def load_feeds_from_csv(csv_path: str):
    db = firestore.client()

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            source_id = row['source_id']
            db.collection('sources').document(source_id).set({
                'id': source_id,
                'name': row['name'],
                'type': row['type'],
                'url': row['url'],
                'category': row['category'],
                'status': 'active' if row['enabled'] == 'true' else 'disabled',
                'lastChecked': None,
                'articlesLast24h': 0,
                'createdAt': firestore.SERVER_TIMESTAMP
            })
```

### BigQuery: FUTURE ONLY

BigQuery is **NOT** part of the core architecture. It may be added as a future enhancement for:
- Long-term analytics
- Historical data archival
- Advanced querying

**Current architecture uses Firestore exclusively.**

---

## AGENT DETAILS (8 DISTINCT AGENTS)

### Agent 0: Perception Orchestrator

**YAML Config:**
```yaml
# agents/agent_0_orchestrator.yaml
name: perception_orchestrator
description: Root orchestrator for Perception news intelligence workflow
model: gemini-2.0-flash
agent_class: Agent

instruction: |
  You are the Editor-in-Chief of Perception With Intent.

  Workflow:
  1. Read active sources and topics from Firestore
  2. Dispatch Source Harvester to fetch articles in parallel
  3. Call Relevance & Ranking to score articles
  4. Call Brief Writer to generate executive summary
  5. Call Alert & Anomaly for threshold checks
  6. Call Validator to ensure data quality
  7. Call Storage Manager to persist everything
  8. Log ingestion run

tools:
  - name: agent_0_tools

sub_agents:
  - config_path: ./agent_1_source_harvester.yaml
  - config_path: ./agent_2_topic_manager.yaml
  - config_path: ./agent_3_relevance_ranking.yaml
  - config_path: ./agent_4_brief_writer.yaml
  - config_path: ./agent_5_alert_anomaly.yaml
  - config_path: ./agent_6_validator.yaml
  - config_path: ./agent_7_storage_manager.yaml
```

### Agent 1: Source Harvester

**Purpose:** Fetch raw content from RSS/API/web sources

**Tools:**
- `fetch_from_csv` - Load sources from CSV
- `fetch_rss_feed` - Parse RSS feeds
- `fetch_api_feed` - Call API endpoints
- `fetch_webpage` - Scrape web pages

**YAML:**
```yaml
name: perception_source_harvester
description: Fetches news articles from configured sources
model: gemini-2.0-flash
agent_class: Agent

instruction: |
  You fetch news from RSS feeds, APIs, and web pages.

  For each source:
  - Determine type (RSS/API/web)
  - Call appropriate fetch tool
  - Normalize article data (title, url, publishedAt, content)
  - Return list of raw articles

tools:
  - name: agent_1_tools
```

### Agent 2: Topic Manager

**Purpose:** Manage what topics we're monitoring

**Tools:**
- `get_active_topics` - Read from Firestore
- `create_topic` - Add new topic
- `update_topic` - Modify existing
- `delete_topic` - Remove topic

### Agent 3: Relevance & Ranking

**Purpose:** Score and filter articles by topic relevance

**Tools:**
- `score_article_relevance` - Use Gemini to score 1-10
- `match_article_to_topics` - Find topic matches
- `calculate_importance` - Overall importance score

### Agent 4: Brief Writer

**Purpose:** Generate executive daily briefs

**YAML:**
```yaml
name: perception_brief_writer
description: Summarizes top-ranked articles into executive brief
model: gemini-2.0-flash
agent_class: Agent

instruction: |
  You are an expert executive brief writer.

  Given scored articles:
  - Produce concise daily brief for decision-makers
  - Include:
    * 1-2 sentence headline summary
    * 3-7 key bullet points
    * Strategic implications per topic
  - Keep tone neutral and analytical
  - Output well-structured JSON

tools:
  - name: agent_4_tools
```

### Agent 5: Alert & Anomaly Detector

**Purpose:** Watch for spikes, sentiment shifts, keyword thresholds

**Tools:**
- `check_keyword_frequency` - Detect spikes
- `analyze_sentiment_shift` - Trend changes
- `evaluate_thresholds` - User-defined alerts

### Agent 6: Validator

**Purpose:** Quality control before storage

**Tools:**
- `validate_article_schema` - Check required fields
- `detect_duplicates` - URL/hash matching
- `verify_data_quality` - Content checks

### Agent 7: Storage Manager

**Purpose:** Persist validated data to Firestore

**Tools:**
- `store_articles` - Write to `/articles`
- `store_brief` - Write to `/briefs`
- `log_ingestion_run` - Write to `/ingestion_runs`
- `deduplicate_by_url` - Prevent duplicates

---

## MCP TOOLS (Cloud Run Services)

Each MCP tool is a separate Cloud Run HTTP service.

### 1. fetch_rss_feed

**Endpoint:** `POST /tools/fetch_rss_feed`

**Input:**
```json
{
  "feed_url": "https://techcrunch.com/feed/",
  "time_window_hours": 24
}
```

**Output:**
```json
{
  "articles": [
    {
      "title": "Article Title",
      "url": "https://...",
      "publishedAt": "2025-11-14T12:00:00Z",
      "source": "TechCrunch",
      "content": "Full article text..."
    }
  ]
}
```

### 2. fetch_api_feed

**Endpoint:** `POST /tools/fetch_api_feed`

### 3. fetch_webpage

**Endpoint:** `POST /tools/fetch_webpage`

### 4. store_articles

**Endpoint:** `POST /tools/store_articles`

### 5. generate_brief

**Endpoint:** `POST /tools/generate_brief`

### 6. log_ingestion_run

**Endpoint:** `POST /tools/log_ingestion_run`

### 7. send_notification (Future)

**Endpoint:** `POST /tools/send_notification`

---

## OBSERVABILITY (STRICT REQUIREMENTS)

### OpenTelemetry Tracing

**Pattern for all agents:**

```python
from opentelemetry import trace

tracer = trace.get_tracer("perception.agent_4.brief_writer")

async def generate_brief(articles: list[dict]) -> dict:
    with tracer.start_as_current_span("generate_brief") as span:
        span.set_attribute("agent.name", "perception_brief_writer")
        span.set_attribute("articles.count", len(articles))
        span.set_attribute("agent.version", "1.0")

        # ... generate brief ...

        span.set_attribute("brief.highlights_count", len(brief['highlights']))
        return brief
```

### Metrics

**Required metrics per agent:**

```python
from opentelemetry import metrics

meter = metrics.get_meter("perception.agent_1.source_harvester")

articles_ingested = meter.create_counter(
    "articles_ingested",
    unit="1",
    description="Articles fetched by Source Harvester"
)

fetch_duration = meter.create_histogram(
    "fetch_duration_ms",
    unit="ms",
    description="Time to fetch articles from source"
)
```

**Metrics to track:**
- `articles_ingested` (Agent 1)
- `articles_filtered` (Agent 3)
- `briefs_generated` (Agent 4)
- `alerts_triggered` (Agent 5)
- `validation_failures` (Agent 6)
- `firestore_writes` (Agent 7)
- `ingestion_run_duration_ms` (Agent 0)

### Structured Logging

```python
import logging
import json

logger = logging.getLogger("perception.agent_4")

logger.info(json.dumps({
    "agent_name": "perception_brief_writer",
    "run_id": run_id,
    "action": "generate_brief",
    "articles_count": len(articles),
    "brief_id": brief_id
}))
```

### Cloud Monitoring Dashboard

**Charts:**
1. Ingestion runs per day (line chart)
2. Briefs generated per day (counter)
3. p95 latency per agent (heatmap)
4. Error rate per agent (stacked area)
5. Articles ingested per source (bar chart)
6. Alert triggers over time (time series)

---

## TECHNOLOGY STACK (CORRECTED)

### Frontend
- React 18 + TypeScript + Vite
- TailwindCSS
- Firebase Auth + Firestore SDK
- Firebase Hosting

### Backend / Agents
- **Vertex AI Agent Engine** (single deployment)
- **Google ADK** (Python)
- **Model:** Gemini 2.0 Flash
- **Protocol:** A2A (within Agent Engine)

### Tools (MCP)
- Cloud Run services (FastAPI Python)
- Service account auth for Firestore
- HTTP endpoints for agent tools

### Data
- **Firestore** (Native Mode) - ONLY core data store
- **CSV** (`data/initial_feeds.csv`) - Initial source bootstrap
- **BigQuery** - Future enhancement ONLY (not core)

### Infrastructure
- Terraform for IaC
- GitHub Actions + WIF for CI/CD
- Agent Engine staging bucket (ADK requirement only)

---

## BUILD PHASES (CORRECTED)

### Phase 1: Firestore Foundation ✅ (IN PROGRESS)

**Deliverables:**
- ✅ Firestore Native Mode enabled
- ✅ Collections defined (users, sources, articles, briefs, ingestion_runs)
- ✅ Security rules deployed
- 🔄 CSV loader script for initial feeds
- 🔄 Seed data (using CSV, not hardcoded)

### Phase 2: Dashboard UI

**No changes from previous plan** - UI remains the same

### Phase 3: Agent Cards (8 Individual YAMLs)

**Corrected:**
- Create 8 separate YAML files (not 1 with modes)
- Each in `app/perception_agent/agents/`
- Each with own tools file
- Document in `000-docs/agents/` to match

### Phase 4: MCP Tool Architecture

**Corrected:**
- Tools are Cloud Run HTTP services (not embedded)
- No BigQuery tools
- Focus on RSS/API fetch, Firestore writes, brief generation

### Phase 5: First MCP Tool

**Corrected:**
- Deploy `fetch_rss_feed` to Cloud Run
- Add OpenTelemetry instrumentation
- Verify traces in Cloud Trace

### Phase 6: Pipeline Documentation

**Corrected:**
- Diagram shows 8 agents (not 1)
- No BigQuery in data flow
- CSV as initial source
- Firestore as only persistent store

### Phase 7: Working Ingestion

**Corrected:**
- Trigger Agent 0 (orchestrator)
- Agent 0 calls Agents 1-7 in sequence
- Sources from Firestore (loaded from CSV)
- Results written to Firestore only

---

## WHAT CHANGED FROM PREVIOUS DOCS

**Major Corrections:**

1. **Data Store:** BigQuery removed from core, Firestore is ONLY store
2. **Agent Count:** 8 distinct agents, not 1 with personas
3. **Initial Feeds:** CSV file, not positive news RSS
4. **Observability:** OpenTelemetry required, not optional
5. **Architecture:** Vertex AI Agent Engine native, not custom orchestration

**Files to Update:**
- `001-AT-ARCH-firestore-schema.md` - Remove BigQuery references
- `011-PP-PLAN-build-phases-architecture.md` - Correct agent count, data stores
- All agent YAML files - Split into 8 separate configs

---

**Last Updated:** 2025-11-14
**Status:** AUTHORITATIVE - Supersedes all previous architecture docs
**Next:** Implement corrections across all files
