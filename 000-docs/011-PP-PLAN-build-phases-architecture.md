# Perception Build Phases & Architecture Plan

**Project:** Perception With Intent
**Created:** 2025-11-14
**Version:** 1.0
**Status:** Phase 1 In Progress

---

## Executive Summary

This document outlines the complete build plan for Perception With Intent, an AI-powered news intelligence platform. The system uses 8 specialized AI agents orchestrated via Vertex AI Agent Engine, with tools exposed via MCP on Cloud Run, to deliver executive-level insights from any news source.

**Live URL:** https://perception-with-intent.web.app
**Repository:** https://github.com/jeremylongshore/perception-with-intent

---

## System Overview

### The Big Picture

```
Human World (Firebase Dashboard)
    ↓
Agent Brain (Vertex AI Engine - 8 Agents)
    ↓
Tool World (Cloud Run MCPs - 7 Services)
    ↓
Data World (Firestore + BigQuery)
```

### Key Principles

1. **Source Agnostic** - RSS, APIs, custom connectors (no vendor lock-in)
2. **Executive Focus** - Signal, not noise (AI-filtered insights)
3. **Production Quality** - Real code, not placeholders
4. **Progressive Hardening** - Develop loose, deploy tight

---

## Build Phases

### PHASE 1: Foundation - Firestore Schema ⏳ IN PROGRESS

**Duration:** 30 minutes
**Status:** 90% complete (blocked on Firestore Native Mode enablement)

#### Deliverables

✅ **Firestore Collections Designed**
- `/users/{userId}` - User profiles and preferences
- `/users/{userId}/topics/{topicId}` - User-specific topics
- `/users/{userId}/alerts/{alertId}` - User-configured alerts
- `/sources/{sourceId}` - Global source configuration
- `/articles/{articleId}` - All ingested articles
- `/briefs/{briefId}` - Daily executive briefs
- `/ingestion_runs/{runId}` - System activity logs

✅ **Security Rules Deployed**
- User isolation (can only access own data)
- Authentication required for all reads
- Write access restricted to backend/agents

✅ **Seed Data Script Created**
- 5 demo sources (TechCrunch, The Verge, BBC, Reuters, MIT)
- 3 sample articles with AI analysis
- 1 daily brief (today's date)
- 1 ingestion run log

⏸️ **Blocked:** Need Firestore Native Mode enabled in console

**Documentation:** `001-AT-ARCH-firestore-schema.md`

---

### PHASE 2: Dashboard UI 📋 PENDING

**Duration:** 2 hours
**Deliverable:** Fully functional authenticated dashboard

#### Dashboard Sections (Cards)

1. **Today's Brief**
   - AI-generated daily summary
   - 3-7 key highlights
   - Link to full brief page

2. **Topic Watchlist**
   - List of monitored topics
   - Last update time, 24h article count
   - Sentiment/impact indicators
   - "Edit Topics" action

3. **Source Health & Coverage**
   - Active sources count
   - Failed sources / errors
   - Most active sources (bar chart)

4. **Alerts & Thresholds**
   - Configured alerts status
   - Recent triggers
   - "New Alert" button

5. **System Activity / Ingestion Log**
   - Recent runs with timestamps
   - Articles ingested, briefs generated
   - System health indicator

6. **Footer**
   - "Perception With Intent — Created by Intent Solutions IO"
   - Link to https://intentsolutions.io

#### Technical Implementation

- React + TypeScript + Vite
- Firebase Auth state management
- Firestore real-time listeners
- TailwindCSS for styling
- Protected routes (redirect unauthenticated users)

#### Mock vs Real Data

- Initial: Display with placeholder data
- Phase 5+: Connect to real ingestion pipeline

---

### PHASE 3: Agent Card Definitions 📋 PENDING

**Duration:** 1 hour
**Deliverable:** Complete agent architecture documentation

#### Agent Cards (YAML in `000-docs/agents/`)

**1. Agent 0: Perception Orchestrator**
- **Role:** Coordinates daily news workflow
- **Inputs:** User topics, source list, raw articles
- **Outputs:** Briefs, summaries, alerts
- **Tools:** Orchestration tools (coordinates other agents)
- **Trigger:** Scheduled (7:30 AM CST) + ad-hoc

**2. Agent 1: Source Harvester**
- **Role:** Fetches raw content from feeds/APIs
- **Tools:** `fetch_rss`, `fetch_api`, `fetch_webpage`
- **Outputs:** Raw articles to Firestore
- **Trigger:** Called by Orchestrator

**3. Agent 2: Topic Manager**
- **Role:** Manages what topics we're tracking
- **Tools:** `topic_tools` (Firestore CRUD)
- **Outputs:** Active topic lists
- **Trigger:** On-demand + daily sync

**4. Agent 3: Relevance & Ranking**
- **Role:** Filters and scores articles per topic
- **Tools:** Gemini for relevance evaluation
- **Outputs:** Scored articles (1-10 scale)
- **Trigger:** Post-ingestion

**5. Agent 4: Summarization / Brief Writer**
- **Role:** Creates daily briefs and topic summaries
- **Tools:** `generate_brief` (Gemini-powered)
- **Outputs:** Executive briefs in Firestore
- **Trigger:** After relevance scoring

**6. Agent 5: Alert & Anomaly**
- **Role:** Watches for spikes, sentiment shifts
- **Tools:** `check_thresholds`, `trigger_alert`
- **Outputs:** Alerts to users
- **Trigger:** Post-analysis

**7. Agent 6: Validator**
- **Role:** Quality control before storage
- **Tools:** `validation_tools`
- **Outputs:** Validation reports
- **Trigger:** Before storage operations

**8. Agent 7: Storage Manager**
- **Role:** Saves validated data to Firestore
- **Tools:** `storage_tools`
- **Outputs:** Write confirmations
- **Trigger:** After validation

#### Agent Card Format

Each YAML includes:
- Name, description
- Input data, output data
- Tools used
- Trigger type
- Example prompt/instruction block

---

### PHASE 4: MCP Tool Architecture 📋 PENDING

**Duration:** 1.5 hours
**Deliverable:** Tool specifications + deployment plan

#### MCP Tools (Cloud Run Services)

**1. fetch_rss_feed**
- **Input:** Feed URL, time window
- **Output:** Normalized article list (title, url, source, content)
- **Endpoint:** `POST /tools/fetch_rss_feed`

**2. fetch_api_feed**
- **Input:** API endpoint, headers, params
- **Output:** Normalized article list
- **Endpoint:** `POST /tools/fetch_api_feed`

**3. fetch_webpage**
- **Input:** URL
- **Output:** Cleaned article content (title + body)
- **Endpoint:** `POST /tools/fetch_webpage`

**4. store_articles**
- **Input:** List of normalized articles
- **Behavior:** Dedupe by URL, write to Firestore
- **Endpoint:** `POST /tools/store_articles`

**5. generate_brief**
- **Input:** Topic, time window, article IDs
- **Output:** JSON brief (headline, key points, implications)
- **Endpoint:** `POST /tools/generate_brief`

**6. log_ingestion_run**
- **Input:** Counts + timestamps
- **Output:** Writes to `ingestion_runs` collection
- **Endpoint:** `POST /tools/log_ingestion_run`

**7. send_notification** (Future)
- **Input:** Alert data, delivery method
- **Output:** Slack/email notification
- **Endpoint:** `POST /tools/send_notification`

#### MCP Server Architecture

- **Stack:** FastAPI (Python) or Express (Node.js)
- **Deployment:** Cloud Run (scale-to-zero)
- **Auth:** Service account with Firestore write access
- **MCP Registration:** JSON/YAML tool definitions
- **Documentation:** `000-docs/tools/`

---

### PHASE 5: First Working MCP Tool 📋 PENDING

**Duration:** 2 hours
**Deliverable:** Live `fetch_rss_feed` tool on Cloud Run

#### Implementation Steps

1. **Create FastAPI Service**
   ```python
   @app.post("/tools/fetch_rss_feed")
   async def fetch_rss(feed_id: str, time_window: Optional[int] = 24):
       # Fetch RSS feed
       # Parse articles
       # Normalize data
       return {"articles": [...]}
   ```

2. **Docker Containerization**
   - Dockerfile with Python 3.11
   - Requirements: feedparser, beautifulsoup4, requests

3. **Cloud Run Deployment**
   ```bash
   gcloud run deploy fetch-rss-mcp \
     --source . \
     --region us-central1 \
     --allow-unauthenticated
   ```

4. **MCP Registration**
   - Create tool definition JSON
   - Register with ADK app
   - Test from Orchestrator

5. **Integration Test**
   - Call tool with real RSS feed
   - Verify normalized output
   - Check Firestore write

---

### PHASE 6: Pipeline Documentation 📋 PENDING

**Duration:** 1 hour
**Deliverable:** End-to-end architecture diagram + docs

#### Document: `000-docs/architecture/perception-pipeline.md`

**Sections:**

1. **System Flow Diagram**
   - Visual representation of data flow
   - Agent interactions via A2A
   - MCP tool calls
   - Firestore writes

2. **Source Configuration**
   - How sources are stored in Firestore
   - Adding new sources
   - Source health monitoring

3. **Ingestion Trigger**
   - Scheduled (Cloud Scheduler)
   - Manual (dashboard button)
   - API-triggered

4. **Orchestrator Steps**
   ```
   1. Read active sources from Firestore
   2. For each source:
      - Call appropriate MCP tool
      - Retrieve new articles
      - Normalize and dedupe
      - Store via store_articles tool
   3. Call Relevance/Ranking Agent
   4. Call Summarization Agent
   5. Call Alert Agent
   6. Log ingestion run
   ```

5. **Dashboard Consumption**
   - Real-time Firestore queries
   - Index requirements
   - Query optimization

6. **Error Handling**
   - Failed sources
   - Duplicate detection
   - Validation failures

---

### PHASE 7: Working Ingestion Flow 📋 PENDING

**Duration:** 2.5 hours
**Deliverable:** One-click "Run Ingestion" that produces a brief

#### Implementation

**1. Backend Trigger Endpoint**
```typescript
// Cloud Function or Cloud Run endpoint
export async function triggerIngestion(req, res) {
  const runId = generateRunId();

  // Start ingestion run
  await db.collection('ingestion_runs').doc(runId).set({
    startedAt: Timestamp.now(),
    status: 'running',
    trigger: 'manual'
  });

  // Call Orchestrator via A2A
  const result = await callOrchestrator({
    action: 'daily_ingestion',
    runId
  });

  res.json({ runId, status: 'started' });
}
```

**2. Orchestrator Logic**
```python
async def daily_ingestion(run_id: str):
    # 1. Get active sources
    sources = await get_active_sources()

    # 2. Fetch from each source
    articles = []
    for source in sources:
        result = await call_mcp_tool('fetch_rss_feed', {
            'feed_url': source['url']
        })
        articles.extend(result['articles'])

    # 3. Dedupe and store
    await call_mcp_tool('store_articles', {'articles': articles})

    # 4. Score relevance
    scored = await call_agent('relevance_scorer', {'articles': articles})

    # 5. Generate brief
    brief = await call_agent('brief_writer', {'articles': scored})

    # 6. Check alerts
    await call_agent('alert_checker', {'articles': scored})

    # 7. Log completion
    await update_ingestion_run(run_id, 'completed')
```

**3. Dashboard Integration**
- Add "Run Ingestion Now" button
- Show loading state
- Display results when complete
- Refresh article list and brief

**4. Test Flow**
1. Click "Run Ingestion Now" in dashboard
2. Watch system activity log update
3. See articles appear in feed
4. View generated daily brief
5. Check alert triggers (if any)

---

## Technology Stack

### Frontend
- **Framework:** React 18 + TypeScript
- **Build:** Vite
- **Styling:** TailwindCSS
- **State:** Firebase SDK (real-time)
- **Hosting:** Firebase Hosting
- **Auth:** Firebase Authentication

### Backend
- **Agents:** Google ADK (Agent Development Kit)
- **Orchestration:** Vertex AI Agent Engine
- **Protocol:** A2A (Agent-to-Agent)
- **AI Model:** Gemini 2.0 Flash
- **Tools:** MCP (Model Context Protocol)
- **Services:** Cloud Run (FastAPI/Express)

### Data
- **Database:** Firestore (NoSQL)
- **Analytics:** BigQuery (future)
- **Storage:** Cloud Storage (future)

### Infrastructure
- **IaC:** Terraform
- **CI/CD:** GitHub Actions
- **Auth:** Workload Identity Federation (WIF)
- **Monitoring:** Cloud Logging + Monitoring

---

## Cost Estimates

**Monthly operational costs** (based on 100 articles/day):

| Component | Monthly Cost |
|-----------|--------------|
| Cloud Run MCPs | ~$15 (scale-to-zero) |
| Vertex AI Agents | ~$25 |
| Gemini 2.0 Flash | ~$20 |
| Firestore | ~$10 |
| Firebase Hosting | $0 (Spark plan) |
| **Total** | **~$70/month** |

---

## Success Criteria

### Phase Completion Metrics

**Phase 1:** Schema + security rules deployed, seed data ready
**Phase 2:** Dashboard renders all 6 sections with auth
**Phase 3:** All 8 agent cards documented
**Phase 4:** MCP tool specs complete, deployment plan ready
**Phase 5:** One MCP tool live and callable
**Phase 6:** Pipeline diagram + docs published
**Phase 7:** End-to-end flow works (click → articles → brief)

### MVP Launch Criteria

- ✅ User can create account and login
- ✅ Dashboard displays meaningful data
- ✅ At least one source fetches real news
- ✅ AI generates actual brief (not mock)
- ✅ Manual "Run Ingestion" works
- ✅ System activity log shows runs

---

## Next Steps

### Immediate (This Session)

1. **Enable Firestore Native Mode** (requires console access)
2. **Run seed script** to populate demo data
3. **Start Phase 2** - Build dashboard UI

### Near Term (Next 1-2 Days)

4. Complete Phases 2-4 (Dashboard + Agent Cards + MCP Specs)
5. Deploy first MCP tool (Phase 5)
6. Test end-to-end flow (Phase 7)

### Future Enhancements

- Scheduled ingestion (Cloud Scheduler)
- Email/Slack notifications
- Custom topic creation via UI
- Advanced alerting rules
- BigQuery analytics
- Multi-user/team accounts

---

## Quality Standards

### Code Quality

- TypeScript strict mode enabled
- ESLint + Prettier configured
- Component-based architecture
- Error boundaries for React
- Comprehensive error handling

### Documentation

- All agents have YAML cards
- All tools have API specs
- Architecture diagrams included
- README with quick start
- Deployment guides

### Security

- Authentication required for all data
- User isolation enforced
- Secrets in Secret Manager
- SPIFFE IDs for production
- Security rules tested

---

## References

- **Firestore Schema:** `001-AT-ARCH-firestore-schema.md`
- **Deployment Status:** `002-OD-DEPL-deployment-status.md`
- **WIF Setup:** `003-OD-GUID-wif-setup-guide.md`
- **GitHub Setup:** `004-OD-GUID-github-setup.md`
- **Agents Overview:** `006-AT-ARCH-agents-deployment.md`
- **Product Roadmap:** `008-PP-PLAN-product-roadmap.md`

---

**Last Updated:** 2025-11-14
**Next Review:** After Phase 2 completion
**Owner:** Intent Solutions IO
**Status:** Active Development
