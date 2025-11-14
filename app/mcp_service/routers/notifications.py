"""
Notification Tool Router

Sends notifications via Slack, email, or webhooks.

Phase 4: Returns fake but structurally correct responses.
Phase 6: Wire up real Slack API / email / webhook delivery.
"""

import logging
import json
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from fastapi import APIRouter
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
router = APIRouter()


# Pydantic Models
class NotificationMessage(BaseModel):
    """Notification message content."""
    title: str
    body: str
    url: Optional[str] = None


class SendNotificationRequest(BaseModel):
    """Request schema for send_notification tool."""
    channel: str = Field(..., description="Notification channel: slack | email | webhook")
    recipient: str = Field(..., description="Slack channel ID, email address, or webhook URL")
    message: NotificationMessage
    priority: str = Field("normal", description="Priority: low | normal | high")


class SendNotificationResponse(BaseModel):
    """Response schema for send_notification tool."""
    notification_id: str
    channel: str
    sent_at: str
    status: str


# Tool Endpoint
@router.post("/send_notification", response_model=SendNotificationResponse)
async def send_notification(request: SendNotificationRequest):
    """
    Send notification via Slack, email, or webhook.

    Phase 4: Returns fake data (STUB for future implementation).
    Phase 6 TODO:
    - Slack: Use Slack SDK to post messages
    - Email: Use SendGrid or GCP Email API
    - Webhook: POST JSON payload to provided URL
    - Handle delivery failures and retries
    """
    logger.info(json.dumps({
        "severity": "INFO",
        "message": "Sending notification",
        "mcp_tool": "send_notification",
        "channel": request.channel,
        "recipient": request.recipient,
        "priority": request.priority
    }))

    # PHASE 4: Fake response
    response = SendNotificationResponse(
        notification_id=f"notif_{int(datetime.now(tz=timezone.utc).timestamp())}",
        channel=request.channel,
        sent_at=datetime.now(tz=timezone.utc).isoformat(),
        status="delivered"
    )

    logger.info(json.dumps({
        "severity": "INFO",
        "message": "Notification sent successfully",
        "mcp_tool": "send_notification",
        "channel": request.channel,
        "notification_id": response.notification_id
    }))

    return response
