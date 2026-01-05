"""
Perception Orchestrator Agent

Pure Python agent implementation for Vertex AI Agent Engine deployment.
No YAML config - ADK auto-generates broken agent_engine_app.py when YAML present.

Pattern from bobs-brain: define LlmAgent directly in Python.
"""

import os
import logging
from google.adk.agents import LlmAgent
from google.adk.apps import App

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# App configuration - must be valid Python identifier (letters, digits, underscores only)
APP_NAME = os.getenv("APP_NAME", "perception_orchestrator")

# Agent instruction (from root_agent.yaml)
ORCHESTRATOR_INSTRUCTION = """You are the Editor-in-Chief of Perception With Intent.

High-level responsibilities:
- Coordinate source harvesting, relevance scoring, brief writing, alerting, validation, and storage.
- Ensure each ingestion run produces a coherent executive brief and consistent Firestore state.

When invoked for a daily_ingestion run:
1. Start an ingestion run record (run_id).
2. Ask Source Harvester for fresh articles from all enabled sources.
3. Ask Relevance & Ranking to score and filter articles using user topics.
4. Ask Brief Writer to produce a concise executive brief.
5. Ask Technology Desk Editor to curate and enhance the Tech section.
6. Ask Alert & Anomaly Detector whether any alerts should fire.
7. Ask Validator to confirm that articles and brief are structurally valid.
8. Ask Storage Manager to persist data to Firestore and finalize the ingestion run.

If any critical step fails, surface a clear error and mark the run as failed.

Note: Technology Desk Editor is the first vertical section editor. In future phases,
additional section editors (Business Desk, Politics Desk, etc.) will be added.
"""


def create_agent() -> LlmAgent:
    """
    Create the Perception Orchestrator agent directly in Python.
    No YAML file needed - avoids ADK auto-generation issues.
    """
    logger.info("Creating Perception Orchestrator LlmAgent")

    agent = LlmAgent(
        model="gemini-2.0-flash",
        name="perception_orchestrator",
        description="Root orchestrator for the Perception With Intent news intelligence workflow.",
        instruction=ORCHESTRATOR_INSTRUCTION,
        # Tools disabled for initial deployment test
        tools=[],
    )

    logger.info(f"Agent created: {agent.name}")
    return agent


def create_app() -> App:
    """
    Create the App container for Agent Engine deployment.
    """
    logger.info(f"Creating App for {APP_NAME}")

    agent = create_agent()
    app_instance = App(
        name=APP_NAME,
        root_agent=agent,
    )

    logger.info(f"App created successfully: {APP_NAME}")
    return app_instance


# Module-level app for Agent Engine
app = create_app()

logger.info("Perception Orchestrator app ready for Agent Engine deployment")
