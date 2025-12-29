# Agent Definition for ADK Deployment
# Perception - AI News Intelligence Platform
# Defines the root_agent for Vertex AI Agent Engine deployment

import os
import sys

# Add the current directory to the path for local imports
# This ensures our app/ directory is found before the Agent Engine's app/
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from google.adk.agents import Agent

# Import tools from the perception agent module using the adjusted path
from perception_app.perception_agent.tools.agent_0_tools import (
    start_ingestion_run,
    finalize_ingestion_run,
    build_daily_ingestion_plan,
    run_daily_ingestion,
)

# Define the root agent instruction
ORCHESTRATOR_INSTRUCTION = """
You are the Editor-in-Chief of Perception With Intent.

High-level responsibilities:
- Coordinate source harvesting, relevance scoring, brief writing, alerting, validation, and storage.
- Ensure each ingestion run produces a coherent executive brief and consistent Firestore state.

When invoked for a daily_ingestion run:
1. Start an ingestion run record (run_id).
2. Execute the full ingestion pipeline which:
   - Harvests fresh articles from all enabled sources
   - Scores and filters articles using user topics
   - Produces a concise executive brief
   - Curates and enhances the Tech section
   - Validates that articles and brief are structurally valid
   - Persists data to Firestore and finalizes the ingestion run

If any critical step fails, surface a clear error and mark the run as failed.

Note: Technology Desk Editor is the first vertical section editor. In future phases,
additional section editors (Business Desk, Politics Desk, etc.) will be added.
"""

# Create the root agent
root_agent = Agent(
    name="perception_orchestrator",
    model="gemini-2.0-flash",
    description="Root orchestrator for the Perception With Intent news intelligence workflow.",
    instruction=ORCHESTRATOR_INSTRUCTION,
    tools=[
        start_ingestion_run,
        finalize_ingestion_run,
        build_daily_ingestion_plan,
        run_daily_ingestion,
    ],
)
