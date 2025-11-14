"""
API Feed Tool Router

Fetches articles from custom API endpoints (NewsAPI, etc.).

Phase 4: Returns fake but structurally correct responses.
Phase 5: Wire up real HTTP client + API integrations.
"""

import logging
import json
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
router = APIRouter()


# Pydantic Models
class FetchAPIFeedRequest(BaseModel):
    """Request schema for fetch_api_feed tool."""
    feed_id: str = Field(..., description="Firestore document ID from /sources collection")
    api_params: Optional[Dict[str, Any]] = Field(None, description="Source-specific API parameters")


class APIArticle(BaseModel):
    """Individual article from API feed."""
    title: str
    url: str
    published_at: str
    summary: Optional[str] = None
    author: Optional[str] = None
    content_snippet: Optional[str] = None
    source: Optional[str] = None
    categories: List[str] = Field(default_factory=list)


class FetchAPIFeedResponse(BaseModel):
    """Response schema for fetch_api_feed tool."""
    feed_id: str
    api_url: str
    fetched_at: str
    article_count: int
    articles: List[APIArticle]


# Tool Endpoint
@router.post("/fetch_api_feed", response_model=FetchAPIFeedResponse)
async def fetch_api_feed(request: FetchAPIFeedRequest):
    """
    Fetch articles from a custom API endpoint.

    Phase 4: Returns fake data.
    Phase 5 TODO:
    - Query Firestore /sources/{feed_id} for API config
    - Make HTTP request with proper headers/auth
    - Parse response based on source type
    - Handle pagination if needed
    """
    logger.info(json.dumps({
        "severity": "INFO",
        "message": "Fetching API feed",
        "mcp_tool": "fetch_api_feed",
        "feed_id": request.feed_id
    }))

    # PHASE 4: Fake response
    fake_articles = [
        APIArticle(
            title="Microsoft Launches New AI Tool",
            url="https://example.com/microsoft-ai",
            published_at=datetime.now(tz=timezone.utc).isoformat(),
            summary="Microsoft today unveiled a new AI-powered tool.",
            author="John Doe",
            content_snippet="Microsoft today unveiled...",
            source="TechCrunch",
            categories=["AI", "Microsoft"]
        )
    ]

    response = FetchAPIFeedResponse(
        feed_id=request.feed_id,
        api_url=f"https://api.example.com/{request.feed_id}",
        fetched_at=datetime.now(tz=timezone.utc).isoformat(),
        article_count=len(fake_articles),
        articles=fake_articles
    )

    logger.info(json.dumps({
        "severity": "INFO",
        "message": "API feed fetched successfully",
        "mcp_tool": "fetch_api_feed",
        "feed_id": request.feed_id,
        "article_count": response.article_count
    }))

    return response
