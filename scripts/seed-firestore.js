#!/usr/bin/env node

/**
 * Firestore Seed Data Script
 * Populates Firestore with initial demo data for Perception platform
 * Sources are loaded from data/initial_feeds.csv
 */

const admin = require('firebase-admin');
const fs = require('fs');
const path = require('path');
const { parse } = require('csv-parse/sync');

// Initialize Firebase Admin
admin.initializeApp({
  projectId: process.env.GOOGLE_CLOUD_PROJECT || 'perception-with-intent'
});

const db = admin.firestore();

// Load sources from CSV
function loadSourcesFromCSV() {
  const csvPath = path.join(__dirname, '../data/initial_feeds.csv');
  const csvContent = fs.readFileSync(csvPath, 'utf-8');
  const records = parse(csvContent, {
    columns: true,
    skip_empty_lines: true
  });

  return records.map(row => ({
    id: row.source_id,
    name: row.name,
    type: row.type,
    url: row.url,
    category: row.category,
    topicTags: [],
    status: row.enabled === 'true' ? 'active' : 'disabled',
    lastChecked: admin.firestore.Timestamp.now(),
    lastSuccess: admin.firestore.Timestamp.now(),
    articlesLast24h: 0,
    createdAt: admin.firestore.Timestamp.now(),
    updatedAt: admin.firestore.Timestamp.now()
  }));
}

// Seed data
const seedData = {
  sources: loadSourcesFromCSV(),

  articlesOLD: [
    {
      id: 'techcrunch-ai',
      name: 'TechCrunch AI',
      type: 'rss',
      url: 'https://techcrunch.com/category/artificial-intelligence/feed/',
      category: 'tech',
      topicTags: ['AI', 'machine learning', 'startups'],
      status: 'active',
      lastChecked: admin.firestore.Timestamp.now(),
      lastSuccess: admin.firestore.Timestamp.now(),
      articlesLast24h: 15,
      createdAt: admin.firestore.Timestamp.now(),
      updatedAt: admin.firestore.Timestamp.now()
    },
    {
      id: 'the-verge-ai',
      name: 'The Verge AI',
      type: 'rss',
      url: 'https://www.theverge.com/rss/ai-artificial-intelligence/index.xml',
      category: 'tech',
      topicTags: ['AI', 'technology', 'consumer tech'],
      status: 'active',
      lastChecked: admin.firestore.Timestamp.now(),
      lastSuccess: admin.firestore.Timestamp.now(),
      articlesLast24h: 12,
      createdAt: admin.firestore.Timestamp.now(),
      updatedAt: admin.firestore.Timestamp.now()
    },
    {
      id: 'bbc-technology',
      name: 'BBC Technology',
      type: 'rss',
      url: 'http://feeds.bbci.co.uk/news/technology/rss.xml',
      category: 'tech',
      topicTags: ['technology', 'news', 'global'],
      status: 'active',
      lastChecked: admin.firestore.Timestamp.now(),
      lastSuccess: admin.firestore.Timestamp.now(),
      articlesLast24h: 8,
      createdAt: admin.firestore.Timestamp.now(),
      updatedAt: admin.firestore.Timestamp.now()
    },
    {
      id: 'reuters-tech',
      name: 'Reuters Technology',
      type: 'rss',
      url: 'https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best',
      category: 'tech',
      topicTags: ['technology', 'business', 'enterprise'],
      status: 'active',
      lastChecked: admin.firestore.Timestamp.now(),
      lastSuccess: admin.firestore.Timestamp.now(),
      articlesLast24h: 10,
      createdAt: admin.firestore.Timestamp.now(),
      updatedAt: admin.firestore.Timestamp.now()
    },
    {
      id: 'mit-ai',
      name: 'MIT Technology Review AI',
      type: 'rss',
      url: 'https://www.technologyreview.com/topic/artificial-intelligence/feed',
      category: 'research',
      topicTags: ['AI', 'research', 'deep tech'],
      status: 'active',
      lastChecked: admin.firestore.Timestamp.now(),
      lastSuccess: admin.firestore.Timestamp.now(),
      articlesLast24h: 5,
      createdAt: admin.firestore.Timestamp.now(),
      updatedAt: admin.firestore.Timestamp.now()
    }
  ],

  articles: [
    {
      id: 'article_001',
      title: 'Google Announces Gemini 2.0 Flash with 60% Cost Reduction',
      url: 'https://techcrunch.com/2025/11/14/google-gemini-2-flash',
      source: 'TechCrunch AI',
      sourceId: 'techcrunch-ai',
      publishedAt: admin.firestore.Timestamp.fromDate(new Date('2025-11-14T12:00:00Z')),
      ingestedAt: admin.firestore.Timestamp.now(),
      summary: 'Google unveiled Gemini 2.0 Flash, a significant upgrade to their AI model lineup. The new model offers 60% lower operational costs while maintaining performance. Available now through Vertex AI.',
      aiTags: ['AI models', 'Google', 'cost reduction', 'Gemini'],
      relevanceScore: 9,
      importanceScore: 8,
      matchedTopics: [],
      matchedKeywords: ['Gemini', 'Google', 'AI model'],
      sentiment: 'positive'
    },
    {
      id: 'article_002',
      title: 'EU AI Act Enforcement Begins Next Quarter',
      url: 'https://www.theverge.com/2025/11/14/eu-ai-act-enforcement',
      source: 'The Verge AI',
      sourceId: 'the-verge-ai',
      publishedAt: admin.firestore.Timestamp.fromDate(new Date('2025-11-14T10:30:00Z')),
      ingestedAt: admin.firestore.Timestamp.now(),
      summary: 'The European Union will begin enforcing the AI Act in Q1 2026. Companies must ensure compliance with transparency and safety requirements. Non-compliance could result in significant fines.',
      aiTags: ['regulation', 'EU', 'compliance', 'AI Act'],
      relevanceScore: 8,
      importanceScore: 9,
      matchedTopics: [],
      matchedKeywords: ['AI regulation', 'EU', 'compliance'],
      sentiment: 'neutral'
    },
    {
      id: 'article_003',
      title: 'OpenAI Hints at GPT-5 Timeline',
      url: 'https://www.bbc.com/news/technology/openai-gpt5-preview',
      source: 'BBC Technology',
      sourceId: 'bbc-technology',
      publishedAt: admin.firestore.Timestamp.fromDate(new Date('2025-11-14T09:00:00Z')),
      ingestedAt: admin.firestore.Timestamp.now(),
      summary: 'OpenAI executives suggested GPT-5 may arrive in 2026. The model promises significant improvements in reasoning and multimodal capabilities. Beta access expected for select partners in early 2026.',
      aiTags: ['OpenAI', 'GPT-5', 'model release', 'preview'],
      relevanceScore: 9,
      importanceScore: 8,
      matchedTopics: [],
      matchedKeywords: ['OpenAI', 'GPT-5', 'model'],
      sentiment: 'positive'
    }
  ],

  briefs: [
    {
      id: '2025-11-14',
      type: 'daily',
      date: '2025-11-14',
      executiveSummary: `Today's major developments focused on AI model releases and regulatory updates. Google's Gemini 2.0 Flash represents a significant cost reduction for enterprises, while the EU prepares for AI Act enforcement. OpenAI continues to build anticipation for GPT-5 with a 2026 timeline hint. The convergence of improved models and stricter regulation signals a maturing AI industry where compliance and efficiency become competitive advantages.`,
      highlights: [
        'Google launches Gemini 2.0 Flash with 60% cost savings - major impact for enterprise adoption',
        'EU AI Act enforcement begins Q1 2026 - companies must ensure compliance or face fines',
        'OpenAI hints at GPT-5 timeline for 2026 - beta access for select partners early year',
        'Cost efficiency becomes key competitive factor as models mature',
        'Regulatory compliance increasingly important for enterprise AI deployments'
      ],
      metrics: {
        articleCount: 47,
        topSources: {
          'TechCrunch AI': 15,
          'The Verge AI': 12,
          'BBC Technology': 10,
          'Reuters Technology': 7,
          'MIT Technology Review AI': 3
        },
        mainTopics: ['AI model releases', 'Regulation', 'Enterprise adoption']
      },
      articles: ['article_001', 'article_002', 'article_003'],
      generatedAt: admin.firestore.Timestamp.now(),
      generatedBy: 'agent_5'
    }
  ],

  ingestionRuns: [
    {
      id: 'run_001',
      startedAt: admin.firestore.Timestamp.fromDate(new Date(Date.now() - 3600000)), // 1 hour ago
      completedAt: admin.firestore.Timestamp.fromDate(new Date(Date.now() - 3360000)), // 56 min ago
      status: 'completed',
      trigger: 'scheduled',
      stats: {
        sourcesChecked: 5,
        sourcesFailed: 0,
        articlesIngested: 47,
        articlesDeduplicated: 8,
        briefsGenerated: 1,
        alertsTriggered: 0
      },
      duration: 240
    }
  ]
};

async function seedFirestore() {
  console.log('🌱 Starting Firestore seed...\n');

  try {
    // Seed sources
    console.log('📰 Seeding sources...');
    for (const source of seedData.sources) {
      await db.collection('sources').doc(source.id).set(source);
      console.log(`  ✓ ${source.name}`);
    }

    // Seed articles
    console.log('\n📄 Seeding articles...');
    for (const article of seedData.articles) {
      await db.collection('articles').doc(article.id).set(article);
      console.log(`  ✓ ${article.title.substring(0, 50)}...`);
    }

    // Seed briefs
    console.log('\n📋 Seeding briefs...');
    for (const brief of seedData.briefs) {
      await db.collection('briefs').doc(brief.id).set(brief);
      console.log(`  ✓ Daily brief: ${brief.date}`);
    }

    // Seed ingestion runs
    console.log('\n⚙️  Seeding ingestion runs...');
    for (const run of seedData.ingestionRuns) {
      await db.collection('ingestion_runs').doc(run.id).set(run);
      console.log(`  ✓ Run: ${run.id}`);
    }

    console.log('\n✅ Firestore seeding complete!');
    console.log('\nSeeded:');
    console.log(`  - ${seedData.sources.length} sources`);
    console.log(`  - ${seedData.articles.length} articles`);
    console.log(`  - ${seedData.briefs.length} briefs`);
    console.log(`  - ${seedData.ingestionRuns.length} ingestion runs`);

    process.exit(0);
  } catch (error) {
    console.error('\n❌ Error seeding Firestore:', error);
    process.exit(1);
  }
}

// Run the seed
seedFirestore();
