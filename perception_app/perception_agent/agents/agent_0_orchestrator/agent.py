"""
Perception Orchestrator Agent

Loads the root_agent.yaml configuration for Vertex AI Agent Engine deployment.
ADK's auto-generated paths are broken, so we provide explicit path resolution.

Pattern from bobs-brain: use os.path.dirname(__file__) for reliable paths.
"""

import os
import logging
from google.adk.agents import config_agent_utils
from google.adk.apps import App

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# App configuration - must be valid Python identifier (letters, digits, underscores only)
APP_NAME = os.getenv("APP_NAME", "perception_orchestrator")


def create_agent():
    """
    Create the agent from root_agent.yaml in the same directory.
    Uses os.path.dirname(__file__) for reliable path resolution.
    """
    config_path = os.path.join(os.path.dirname(__file__), "root_agent.yaml")
    logger.info(f"Loading agent config from: {config_path}")

    # Use config_agent_utils.from_config (the correct ADK API)
    agent = config_agent_utils.from_config(config_path)
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
