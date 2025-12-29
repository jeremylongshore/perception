"""
Storage Tool Router

Handles Firestore writes for articles and data persistence.

Phase 4: Returns fake but structurally correct responses.
Phase 5: Wire up real Firestore batch writes.
"""

import logging
import json
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from fastapi import APIRouter
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
router = APIRouter()


# Pydantic Models
class Article(BaseModel):
    """Article to store in Firestore."""
    title: str
    url: str
    source_id: str
    published_at: str
    summary: Optional[str] = None
    content: Optional[str] = None
    ai_summary: Optional[str] = None
    ai_tags: List[str] = Field(default_factory=list)
    relevance_score: Optional[float] = None
    categories: List[str] = Field(default_factory=list)


class StoreArticlesRequest(BaseModel):
    """Request schema for store_articles tool."""
    run_id: str = Field(..., description="Ingestion run ID")
    articles: List[Article] = Field(..., description="Articles to store")


class StoreArticlesResponse(BaseModel):
    """Response schema for store_articles tool."""
    run_id: str
    stored_count: int
    failed_count: int
    failed_urls: List[str] = Field(default_factory=list)
    storage_stats: Dict[str, Any]


# Tool Endpoint
@router.post("/store_articles", response_model=StoreArticlesResponse)
async def store_articles(request: StoreArticlesRequest):
    """
    Batch write articles to Firestore /articles collection.

    Phase 4: Returns fake data.
    Phase 5 TODO:
    - Initialize Firestore client
    - Use batch writes (max 500 per batch)
    - Deduplicate by URL before storing
    - Handle partial failures gracefully
    - Return stats about writes
    """
    logger.info(json.dumps({
        "severity": "INFO",
        "message": "Storing articles",
        "mcp_tool": "store_articles",
        "run_id": request.run_id,
        "article_count": len(request.articles)
    }))

    # PHASE 4: Fake response
    response = StoreArticlesResponse(
        run_id=request.run_id,
        stored_count=len(request.articles),
        failed_count=0,
        failed_urls=[],
        storage_stats={
            "firestore_writes": len(request.articles),
            "duplicates_skipped": 0,
            "latency_ms": 250
        }
    )

    logger.info(json.dumps({
        "severity": "INFO",
        "message": "Articles stored successfully",
        "mcp_tool": "store_articles",
        "run_id": request.run_id,
        "stored_count": response.stored_count
    }))

    return response
