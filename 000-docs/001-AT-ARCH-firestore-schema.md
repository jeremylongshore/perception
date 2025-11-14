# Firestore Schema - Perception With Intent

**Project:** perception-with-intent
**Database:** Firestore (default)
**Created:** 2025-11-14
**Version:** 1.0

---

## Collection Structure

```
/users/{userId}
/users/{userId}/topics/{topicId}
/users/{userId}/alerts/{alertId}
/sources/{sourceId}
/articles/{articleId}
/briefs/{briefId}
/ingestion_runs/{runId}
```

---

## 1. users Collection

**Path:** `/users/{userId}`
**Purpose:** User profiles and preferences
**Security:** User can only read/write their own document

### Schema

```typescript
interface User {
  uid: string                    // Firebase Auth UID
  email: string                  // User email
  displayName?: string           // Optional display name
  createdAt: Timestamp           // Account creation
  lastLogin: Timestamp           // Last login time
  preferences: {
    briefFrequency: 'daily' | 'weekly'
    emailNotifications: boolean
    slackWebhook?: string
  }
  subscription: {
    tier: 'free' | 'pro' | 'enterprise'
    status: 'active' | 'canceled' | 'trial'
    trialEndsAt?: Timestamp
  }
}
```

### Example

```json
{
  "uid": "abc123",
  "email": "user@example.com",
  "displayName": "John Doe",
  "createdAt": "2025-11-14T10:00:00Z",
  "lastLogin": "2025-11-14T14:30:00Z",
  "preferences": {
    "briefFrequency": "daily",
    "emailNotifications": true
  },
  "subscription": {
    "tier": "free",
    "status": "active"
  }
}
```

---

## 2. topics Subcollection

**Path:** `/users/{userId}/topics/{topicId}`
**Purpose:** User-specific topics to monitor
**Security:** User can only access their own topics

### Schema

```typescript
interface Topic {
  id: string                     // Auto-generated ID
  userId: string                 // Owner UID
  name: string                   // Display name (e.g., "AI Regulation")
  keywords: string[]             // Search keywords
  category: string               // Category (e.g., "tech", "business", "sports")
  active: boolean                // Is this topic being monitored?
  createdAt: Timestamp
  updatedAt: Timestamp
  lastArticleAt?: Timestamp      // Last time we found an article for this topic
  articleCount24h: number        // Count of articles in last 24 hours
  sentiment?: 'positive' | 'neutral' | 'negative'
  priority: 'high' | 'medium' | 'low'
}
```

### Example

```json
{
  "id": "topic_1",
  "userId": "abc123",
  "name": "AI Regulation",
  "keywords": ["AI regulation", "artificial intelligence law", "EU AI Act"],
  "category": "tech",
  "active": true,
  "createdAt": "2025-11-14T10:00:00Z",
  "updatedAt": "2025-11-14T10:00:00Z",
  "articleCount24h": 12,
  "priority": "high"
}
```

---

## 3. alerts Subcollection

**Path:** `/users/{userId}/alerts/{alertId}`
**Purpose:** User-configured alerts and thresholds
**Security:** User can only access their own alerts

### Schema

```typescript
interface Alert {
  id: string
  userId: string
  name: string                   // Alert name
  condition: {
    type: 'keyword_frequency' | 'sentiment_shift' | 'source_spike'
    keyword?: string             // For keyword_frequency
    topicId?: string             // Link to topic
    threshold: number            // Trigger threshold
    timeWindow: 'hour' | 'day' | 'week'
  }
  status: 'active' | 'paused' | 'triggered'
  lastTriggered?: Timestamp
  triggerCount: number           // How many times it's been triggered
  deliveryMethod: 'dashboard' | 'email' | 'slack'
  createdAt: Timestamp
}
```

### Example

```json
{
  "id": "alert_1",
  "userId": "abc123",
  "name": "Gemini 2.0 Spike Alert",
  "condition": {
    "type": "keyword_frequency",
    "keyword": "Gemini 2.0",
    "threshold": 10,
    "timeWindow": "hour"
  },
  "status": "active",
  "triggerCount": 3,
  "deliveryMethod": "dashboard",
  "createdAt": "2025-11-14T10:00:00Z"
}
```

---

## 4. sources Collection

**Path:** `/sources/{sourceId}`
**Purpose:** Global source configuration (RSS, APIs, custom)
**Security:** Read: all authenticated users, Write: admin only

### Schema

```typescript
interface Source {
  id: string
  name: string                   // Display name (e.g., "TechCrunch AI")
  type: 'rss' | 'api' | 'custom'
  url: string                    // Feed URL or API endpoint
  category: string               // Primary category
  topicTags: string[]            // Related topics
  status: 'active' | 'failed' | 'disabled'
  lastChecked?: Timestamp
  lastSuccess?: Timestamp
  lastError?: {
    message: string
    timestamp: Timestamp
  }
  articlesLast24h: number
  config?: {                     // For API sources
    headers?: Record<string, string>
    auth?: 'api_key' | 'oauth'
    apiKey?: string
  }
  createdAt: Timestamp
  updatedAt: Timestamp
}
```

### Example

```json
{
  "id": "source_1",
  "name": "TechCrunch AI",
  "type": "rss",
  "url": "https://techcrunch.com/category/artificial-intelligence/feed/",
  "category": "tech",
  "topicTags": ["AI", "machine learning", "startups"],
  "status": "active",
  "lastChecked": "2025-11-14T14:00:00Z",
  "lastSuccess": "2025-11-14T14:00:00Z",
  "articlesLast24h": 15,
  "createdAt": "2025-11-14T10:00:00Z",
  "updatedAt": "2025-11-14T14:00:00Z"
}
```

---

## 5. articles Collection

**Path:** `/articles/{articleId}`
**Purpose:** All ingested and analyzed articles
**Security:** Read: all authenticated users

### Schema

```typescript
interface Article {
  id: string                     // Hash of URL or UUID
  title: string
  url: string                    // Original article URL
  source: string                 // Source name
  sourceId: string               // Reference to sources/{sourceId}
  publishedAt: Timestamp
  ingestedAt: Timestamp
  content?: string               // Full article text (optional)
  summary: string                // AI-generated 3-5 sentence summary
  aiTags: string[]               // Exactly 4 AI-generated tags
  relevanceScore: number         // 1-10 score
  importanceScore: number        // 1-10 score
  matchedTopics: string[]        // Topic IDs this matches
  matchedKeywords: string[]      // Keywords that matched
  sentiment?: 'positive' | 'neutral' | 'negative'
  imageUrl?: string
  author?: string
}
```

### Example

```json
{
  "id": "article_abc123",
  "title": "Google Launches Gemini 2.0 Flash",
  "url": "https://techcrunch.com/2025/11/14/google-gemini-2-flash",
  "source": "TechCrunch AI",
  "sourceId": "source_1",
  "publishedAt": "2025-11-14T12:00:00Z",
  "ingestedAt": "2025-11-14T14:00:00Z",
  "summary": "Google announced Gemini 2.0 Flash, a faster and more efficient AI model. The model offers 60% cost reduction compared to previous versions. It's now available via Vertex AI.",
  "aiTags": ["AI models", "Google", "Gemini", "performance"],
  "relevanceScore": 9,
  "importanceScore": 8,
  "matchedTopics": ["topic_1"],
  "matchedKeywords": ["Gemini", "AI model"],
  "sentiment": "positive"
}
```

---

## 6. briefs Collection

**Path:** `/briefs/{briefId}`
**Purpose:** Daily executive briefs and topic summaries
**Security:** Read: all authenticated users

### Schema

```typescript
interface Brief {
  id: string                     // Format: YYYY-MM-DD or topic_YYYY-MM-DD
  type: 'daily' | 'topic'
  date: string                   // YYYY-MM-DD
  topicId?: string               // If type=topic
  topicName?: string             // Topic display name
  executiveSummary: string       // 2-3 paragraph overview
  highlights: string[]           // 5-7 bullet points
  metrics: {
    articleCount: number
    topSources: Record<string, number>  // source name -> count
    mainTopics: string[]
  }
  articles: string[]             // Article IDs included in this brief
  generatedAt: Timestamp
  generatedBy: 'agent_5'         // Agent that created it
}
```

### Example

```json
{
  "id": "2025-11-14",
  "type": "daily",
  "date": "2025-11-14",
  "executiveSummary": "Today's major developments focused on AI model releases and regulatory updates. Google's Gemini 2.0 Flash represents a significant cost reduction...",
  "highlights": [
    "Google launches Gemini 2.0 Flash with 60% cost savings",
    "EU AI Act enforcement begins next quarter",
    "OpenAI announces GPT-5 preview timeline"
  ],
  "metrics": {
    "articleCount": 47,
    "topSources": {
      "TechCrunch": 15,
      "The Verge": 12,
      "BBC Tech": 10
    },
    "mainTopics": ["AI regulation", "Model releases", "Enterprise adoption"]
  },
  "articles": ["article_abc123", "article_def456"],
  "generatedAt": "2025-11-14T15:00:00Z",
  "generatedBy": "agent_5"
}
```

---

## 7. ingestion_runs Collection

**Path:** `/ingestion_runs/{runId}`
**Purpose:** Log of ingestion runs for monitoring
**Security:** Read: all authenticated users

### Schema

```typescript
interface IngestionRun {
  id: string                     // UUID
  startedAt: Timestamp
  completedAt?: Timestamp
  status: 'running' | 'completed' | 'failed'
  trigger: 'scheduled' | 'manual' | 'api'
  triggeredBy?: string           // User ID if manual
  stats: {
    sourcesChecked: number
    sourcesFailed: number
    articlesIngested: number
    articlesDeduplicated: number
    briefsGenerated: number
    alertsTriggered: number
  }
  errors?: Array<{
    sourceId: string
    message: string
    timestamp: Timestamp
  }>
  duration?: number              // Seconds
}
```

### Example

```json
{
  "id": "run_xyz789",
  "startedAt": "2025-11-14T14:00:00Z",
  "completedAt": "2025-11-14T14:03:45Z",
  "status": "completed",
  "trigger": "scheduled",
  "stats": {
    "sourcesChecked": 15,
    "sourcesFailed": 1,
    "articlesIngested": 247,
    "articlesDeduplicated": 15,
    "briefsGenerated": 1,
    "alertsTriggered": 2
  },
  "errors": [
    {
      "sourceId": "source_5",
      "message": "Connection timeout",
      "timestamp": "2025-11-14T14:02:00Z"
    }
  ],
  "duration": 225
}
```

---

## Indexes Required

### Firestore Composite Indexes

```javascript
// articles - by topic and date
{
  collection: 'articles',
  fields: [
    { field: 'matchedTopics', mode: 'ARRAY_CONTAINS' },
    { field: 'publishedAt', mode: 'DESCENDING' }
  ]
}

// articles - by relevance
{
  collection: 'articles',
  fields: [
    { field: 'relevanceScore', mode: 'DESCENDING' },
    { field: 'publishedAt', mode: 'DESCENDING' }
  ]
}

// briefs - by date
{
  collection: 'briefs',
  fields: [
    { field: 'date', mode: 'DESCENDING' }
  ]
}

// ingestion_runs - by date
{
  collection: 'ingestion_runs',
  fields: [
    { field: 'startedAt', mode: 'DESCENDING' }
  ]
}
```

---

## Security Rules

See `firestore.rules` for complete implementation. Key rules:

1. **Users can only read/write their own user document**
2. **Users can only access their own topics and alerts**
3. **Sources are read-only for users, write for admins**
4. **Articles and briefs are read-only**
5. **Ingestion runs are read-only**

---

## Seed Data Strategy

Initial seed data will include:

1. **Demo topics** (5-10 common categories)
2. **Active sources** (15-20 RSS feeds across categories)
3. **Sample articles** (50+ for testing dashboard)
4. **Sample brief** (today's date)
5. **Sample ingestion run** (recent completion)

This allows dashboard to display meaningful data immediately after user login.

---

**Last Updated:** 2025-11-14
**Standard:** Document Filing System v2.0
**Category:** AT-ARCH (Architecture & Technical)
