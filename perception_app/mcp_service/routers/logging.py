"""
Logging Tool Router

Handles ingestion run logging to Firestore.

Phase 4: Returns fake but structurally correct responses.
Phase 5: Wire up real Firestore /ingestion_runs writes.
"""

import logging as python_logging
import json
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from fastapi import APIRouter
from pydantic import BaseModel, Field

logger = python_logging.getLogger(__name__)
router = APIRouter()


# Pydantic Models
class IngestionStats(BaseModel):
    """Statistics for an ingestion run."""
    sources_checked: int
    articles_fetched: int
    articles_stored: int
    duplicates_skipped: int
    brief_generated: bool
    errors: List[str] = Field(default_factory=list)


class LogIngestionRunRequest(BaseModel):
    """Request schema for log_ingestion_run tool."""
    run_id: str = Field(..., description="Ingestion run ID")
    status: str = Field(..., description="Run status: running | completed | failed")
    stats: IngestionStats
    started_at: str = Field(..., description="Run start time (ISO 8601)")
    completed_at: Optional[str] = Field(None, description="Run completion time (ISO 8601)")


class LogIngestionRunResponse(BaseModel):
    """Response schema for log_ingestion_run tool."""
    run_id: str
    logged_at: str
    firestore_path: str


# Tool Endpoint
@router.post("/log_ingestion_run", response_model=LogIngestionRunResponse)
async def log_ingestion_run(request: LogIngestionRunRequest):
    """
    Create or update an ingestion run record in Firestore.

    Phase 4: Returns fake data.
    Phase 5 TODO:
    - Initialize Firestore client
    - Write/update to /ingestion_runs/{run_id}
    - Store all stats and timestamps
    - Handle status transitions (running → completed/failed)
    """
    logger.info(json.dumps({
        "severity": "INFO",
        "message": "Logging ingestion run",
        "mcp_tool": "log_ingestion_run",
        "run_id": request.run_id,
        "status": request.status
    }))

    # PHASE 4: Fake response
    response = LogIngestionRunResponse(
        run_id=request.run_id,
        logged_at=datetime.now(tz=timezone.utc).isoformat(),
        firestore_path=f"/ingestion_runs/{request.run_id}"
    )

    logger.info(json.dumps({
        "severity": "INFO",
        "message": "Ingestion run logged successfully",
        "mcp_tool": "log_ingestion_run",
        "run_id": request.run_id,
        "status": request.status
    }))

    return response
