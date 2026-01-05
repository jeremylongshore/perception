"""
Perception Orchestrator - Agent Engine Entrypoint for ADK Deployment

Required by 'adk deploy agent_engine' command.
Imports the app from agent.py for deployment.

NOTE: Use relative import for local dev, but ADK copies files flat so
we try both import patterns.
"""

try:
    # Try relative import first (local dev, proper package structure)
    from .agent import app
except ImportError:
    # Fall back to direct import (ADK flat copy)
    from agent import app

# ADK CLI expects 'app' at module level - it's already imported above
