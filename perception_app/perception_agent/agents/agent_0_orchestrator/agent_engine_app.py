"""
Perception Orchestrator - Agent Engine Entrypoint for ADK Deployment

Required by 'adk deploy agent_engine' command.
Imports the app from agent.py for deployment.
"""

from .agent import app

# ADK CLI expects 'app' at module level - it's already imported above
