export default function About() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-zinc-50">
      {/* Hero Section */}
      <div className="max-w-6xl mx-auto px-4 py-16 sm:py-24">
        <div className="text-center space-y-6">
          <div className="inline-block">
            <span className="inline-flex items-center px-4 py-1.5 rounded-full text-sm font-medium bg-zinc-900 text-white">
              AI-Powered News Intelligence
            </span>
          </div>
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-zinc-900 leading-tight">
            Stop drowning in news.<br />
            <span className="text-zinc-600">Start seeing what matters.</span>
          </h1>
          <p className="text-xl text-zinc-600 max-w-3xl mx-auto leading-relaxed">
            Perception cuts through the noise with 8 specialized AI agents that monitor, analyze,
            and deliver strategic intelligence from any source—automatically.
          </p>
          <div className="flex gap-4 justify-center pt-4">
            <button className="bg-zinc-900 hover:bg-zinc-800 text-white px-8 py-3 rounded-lg font-semibold transition-all shadow-sm">
              Request Demo
            </button>
            <button className="bg-white hover:bg-zinc-50 text-zinc-900 border border-zinc-200 px-8 py-3 rounded-lg font-semibold transition-all">
              View Documentation
            </button>
          </div>
        </div>
      </div>

      {/* Stats Bar */}
      <div className="border-y border-zinc-200 bg-white">
        <div className="max-w-6xl mx-auto px-4 py-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-3xl font-bold text-zinc-900">8</div>
              <div className="text-sm text-zinc-600 mt-1">AI Agents</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-zinc-900">Any Source</div>
              <div className="text-sm text-zinc-600 mt-1">RSS, APIs, Custom</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-zinc-900">&lt; 30s</div>
              <div className="text-sm text-zinc-600 mt-1">Analysis Time</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-zinc-900">24/7</div>
              <div className="text-sm text-zinc-600 mt-1">Automated Monitoring</div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="max-w-6xl mx-auto px-4 py-16 sm:py-24">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-zinc-900 mb-4">
            Built for executives who need signal, not noise
          </h2>
          <p className="text-lg text-zinc-600 max-w-2xl mx-auto">
            Traditional news monitoring wastes your time. Perception delivers only what matters.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {/* Feature 1 */}
          <div className="group bg-white border border-zinc-200 rounded-xl p-8 hover:shadow-lg transition-all">
            <div className="w-12 h-12 bg-zinc-900 rounded-lg flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-zinc-900 mb-3">Source Agnostic</h3>
            <p className="text-zinc-600 leading-relaxed">
              Monitor any topic from any source. RSS feeds, proprietary APIs, custom connectors.
              We adapt to your intelligence needs.
            </p>
          </div>

          {/* Feature 2 */}
          <div className="group bg-white border border-zinc-200 rounded-xl p-8 hover:shadow-lg transition-all">
            <div className="w-12 h-12 bg-zinc-900 rounded-lg flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-zinc-900 mb-3">AI-Powered Analysis</h3>
            <p className="text-zinc-600 leading-relaxed">
              Gemini 2.0 Flash generates summaries, extracts key insights, and identifies strategic
              implications automatically—no manual review required.
            </p>
          </div>

          {/* Feature 3 */}
          <div className="group bg-white border border-zinc-200 rounded-xl p-8 hover:shadow-lg transition-all">
            <div className="w-12 h-12 bg-zinc-900 rounded-lg flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-zinc-900 mb-3">Executive Dashboard</h3>
            <p className="text-zinc-600 leading-relaxed">
              Real-time intelligence delivered through a clean, professional interface.
              Filter by relevance, topic, or strategic priority.
            </p>
          </div>

          {/* Feature 4 */}
          <div className="group bg-white border border-zinc-200 rounded-xl p-8 hover:shadow-lg transition-all">
            <div className="w-12 h-12 bg-zinc-900 rounded-lg flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-zinc-900 mb-3">Daily Executive Briefs</h3>
            <p className="text-zinc-600 leading-relaxed">
              Automated daily summaries highlight patterns, emerging trends, and strategic
              implications across all monitored topics.
            </p>
          </div>

          {/* Feature 5 */}
          <div className="group bg-white border border-zinc-200 rounded-xl p-8 hover:shadow-lg transition-all">
            <div className="w-12 h-12 bg-zinc-900 rounded-lg flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-zinc-900 mb-3">Smart Alerts</h3>
            <p className="text-zinc-600 leading-relaxed">
              Configurable alerts notify you when high-priority signals emerge. Slack, email,
              or webhook integration available.
            </p>
          </div>

          {/* Feature 6 */}
          <div className="group bg-white border border-zinc-200 rounded-xl p-8 hover:shadow-lg transition-all">
            <div className="w-12 h-12 bg-zinc-900 rounded-lg flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-zinc-900 mb-3">Enterprise Security</h3>
            <p className="text-zinc-600 leading-relaxed">
              Built on Google Cloud with Workload Identity Federation, encrypted storage,
              and comprehensive audit logging. Production-ready from day one.
            </p>
          </div>
        </div>
      </div>

      {/* How It Works */}
      <div className="bg-zinc-900 text-white py-16 sm:py-24">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">
              8 specialized agents working in perfect coordination
            </h2>
            <p className="text-lg text-zinc-400 max-w-2xl mx-auto">
              Powered by Google ADK and Vertex AI Agent Engine with A2A Protocol
            </p>
          </div>

          <div className="grid md:grid-cols-4 gap-6">
            <div className="bg-zinc-800 rounded-lg p-6 border border-zinc-700">
              <div className="text-2xl font-bold mb-2">Agent 1</div>
              <div className="text-sm text-zinc-400 mb-2">Topic Manager</div>
              <p className="text-sm text-zinc-300">Manages monitored topics and keywords dynamically</p>
            </div>
            <div className="bg-zinc-800 rounded-lg p-6 border border-zinc-700">
              <div className="text-2xl font-bold mb-2">Agent 2</div>
              <div className="text-sm text-zinc-400 mb-2">News Aggregator</div>
              <p className="text-sm text-zinc-300">Collects content from configured sources in parallel</p>
            </div>
            <div className="bg-zinc-800 rounded-lg p-6 border border-zinc-700">
              <div className="text-2xl font-bold mb-2">Agent 3</div>
              <div className="text-sm text-zinc-400 mb-2">Relevance Scorer</div>
              <p className="text-sm text-zinc-300">Filters noise, scores articles by strategic value</p>
            </div>
            <div className="bg-zinc-800 rounded-lg p-6 border border-zinc-700">
              <div className="text-2xl font-bold mb-2">Agent 4</div>
              <div className="text-sm text-zinc-400 mb-2">Article Analyst</div>
              <p className="text-sm text-zinc-300">Generates summaries and extracts key insights</p>
            </div>
            <div className="bg-zinc-800 rounded-lg p-6 border border-zinc-700">
              <div className="text-2xl font-bold mb-2">Agent 5</div>
              <div className="text-sm text-zinc-400 mb-2">Daily Synthesizer</div>
              <p className="text-sm text-zinc-300">Creates executive briefs highlighting patterns</p>
            </div>
            <div className="bg-zinc-800 rounded-lg p-6 border border-zinc-700">
              <div className="text-2xl font-bold mb-2">Agent 6</div>
              <div className="text-sm text-zinc-400 mb-2">Validator</div>
              <p className="text-sm text-zinc-300">Ensures data quality and source credibility</p>
            </div>
            <div className="bg-zinc-800 rounded-lg p-6 border border-zinc-700">
              <div className="text-2xl font-bold mb-2">Agent 7</div>
              <div className="text-sm text-zinc-400 mb-2">Storage Manager</div>
              <p className="text-sm text-zinc-300">Manages Firestore and BigQuery data layers</p>
            </div>
            <div className="bg-zinc-800 rounded-lg p-6 border border-zinc-700">
              <div className="text-2xl font-bold mb-2">Agent 0</div>
              <div className="text-sm text-zinc-400 mb-2">Root Orchestrator</div>
              <p className="text-sm text-zinc-300">Coordinates all agents via A2A Protocol</p>
            </div>
          </div>
        </div>
      </div>

      {/* Technology Stack */}
      <div className="max-w-6xl mx-auto px-4 py-16 sm:py-24">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-zinc-900 mb-4">
            Enterprise-grade infrastructure
          </h2>
          <p className="text-lg text-zinc-600 max-w-2xl mx-auto">
            Built on Google Cloud with production-ready architecture patterns
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          <div className="bg-white border border-zinc-200 rounded-xl p-8">
            <h3 className="text-xl font-semibold text-zinc-900 mb-6">AI & Agent Platform</h3>
            <ul className="space-y-3">
              <li className="flex items-start gap-3">
                <div className="w-5 h-5 rounded bg-zinc-900 flex-shrink-0 mt-0.5"></div>
                <div>
                  <div className="font-medium text-zinc-900">Google ADK</div>
                  <div className="text-sm text-zinc-600">Agent Development Kit for building production AI agents</div>
                </div>
              </li>
              <li className="flex items-start gap-3">
                <div className="w-5 h-5 rounded bg-zinc-900 flex-shrink-0 mt-0.5"></div>
                <div>
                  <div className="font-medium text-zinc-900">Vertex AI Agent Engine</div>
                  <div className="text-sm text-zinc-600">Managed platform for deploying and orchestrating agents</div>
                </div>
              </li>
              <li className="flex items-start gap-3">
                <div className="w-5 h-5 rounded bg-zinc-900 flex-shrink-0 mt-0.5"></div>
                <div>
                  <div className="font-medium text-zinc-900">A2A Protocol</div>
                  <div className="text-sm text-zinc-600">Agent-to-Agent communication for multi-agent coordination</div>
                </div>
              </li>
              <li className="flex items-start gap-3">
                <div className="w-5 h-5 rounded bg-zinc-900 flex-shrink-0 mt-0.5"></div>
                <div>
                  <div className="font-medium text-zinc-900">Gemini 2.0 Flash</div>
                  <div className="text-sm text-zinc-600">Latest Google AI model for fast, accurate analysis</div>
                </div>
              </li>
            </ul>
          </div>

          <div className="bg-white border border-zinc-200 rounded-xl p-8">
            <h3 className="text-xl font-semibold text-zinc-900 mb-6">Cloud Infrastructure</h3>
            <ul className="space-y-3">
              <li className="flex items-start gap-3">
                <div className="w-5 h-5 rounded bg-zinc-900 flex-shrink-0 mt-0.5"></div>
                <div>
                  <div className="font-medium text-zinc-900">Firebase Hosting + Firestore</div>
                  <div className="text-sm text-zinc-600">Real-time database and hosting for the dashboard</div>
                </div>
              </li>
              <li className="flex items-start gap-3">
                <div className="w-5 h-5 rounded bg-zinc-900 flex-shrink-0 mt-0.5"></div>
                <div>
                  <div className="font-medium text-zinc-900">Cloud Run</div>
                  <div className="text-sm text-zinc-600">Serverless containers that scale to zero</div>
                </div>
              </li>
              <li className="flex items-start gap-3">
                <div className="w-5 h-5 rounded bg-zinc-900 flex-shrink-0 mt-0.5"></div>
                <div>
                  <div className="font-medium text-zinc-900">Terraform</div>
                  <div className="text-sm text-zinc-600">Infrastructure as Code for reproducible deployments</div>
                </div>
              </li>
              <li className="flex items-start gap-3">
                <div className="w-5 h-5 rounded bg-zinc-900 flex-shrink-0 mt-0.5"></div>
                <div>
                  <div className="font-medium text-zinc-900">GitHub Actions + WIF</div>
                  <div className="text-sm text-zinc-600">CI/CD pipeline with keyless authentication</div>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-gradient-to-br from-zinc-900 to-zinc-800 text-white py-16 sm:py-24">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-3xl sm:text-4xl font-bold mb-6">
            Want this level of intelligence for your organization?
          </h2>
          <p className="text-lg text-zinc-300 mb-8 max-w-2xl mx-auto">
            Perception is in private beta. We're working with select organizations to deploy
            custom news intelligence systems tailored to their strategic needs.
          </p>
          <button className="bg-white text-zinc-900 px-10 py-4 rounded-lg font-semibold text-lg hover:bg-zinc-100 transition-all shadow-lg">
            Request Early Access
          </button>
        </div>
      </div>

      {/* Footer */}
      <div className="border-t border-zinc-200 bg-white py-12">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center gap-6">
            <div className="text-center md:text-left">
              <div className="text-lg font-semibold text-zinc-900 mb-1">
                Built by Intent Solutions IO
              </div>
              <p className="text-sm text-zinc-600">
                Custom AI agent systems for enterprise intelligence
              </p>
            </div>
            <div className="flex items-center gap-6">
              <a
                href="https://intentsolutions.io"
                target="_blank"
                rel="noopener noreferrer"
                className="text-zinc-600 hover:text-zinc-900 transition-colors text-sm font-medium"
              >
                Learn More →
              </a>
              <a
                href="https://github.com/jeremylongshore/perception-with-intent"
                target="_blank"
                rel="noopener noreferrer"
                className="text-zinc-600 hover:text-zinc-900 transition-colors"
              >
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
                </svg>
              </a>
            </div>
          </div>
          <div className="text-center text-zinc-500 text-sm mt-8 pt-8 border-t border-zinc-100">
            <p>Powered by Google Cloud Vertex AI • © 2025 Intent Solutions IO. All rights reserved.</p>
          </div>
        </div>
      </div>
    </div>
  )
}
