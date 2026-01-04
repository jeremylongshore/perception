# Agent 0: Root Orchestrator
# This directory contains the ADK agent configuration for Vertex AI Agent Engine deployment

from .agent import app, create_agent, create_app

__all__ = ["app", "create_agent", "create_app"]
