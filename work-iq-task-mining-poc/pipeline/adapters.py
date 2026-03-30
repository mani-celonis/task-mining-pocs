"""
Source adapters that normalize raw events into the UnifiedActivityEvent schema.

Each adapter is source-specific but outputs a common format, making the
downstream clustering and analytics completely source-agnostic.
"""

from __future__ import annotations
import uuid
from abc import ABC, abstractmethod

from pipeline.models import UnifiedActivityEvent, ActorType, EventSource


class BaseAdapter(ABC):
    """Interface that every source adapter must implement."""

    @abstractmethod
    def normalize(self, raw_events: list[dict]) -> list[UnifiedActivityEvent]:
        ...


# ---------- Celonis Task Mining Adapter ----------

_TM_EVENT_TYPE_MAP = {
    "Left click": "Left click",
    "Left double click": "Left double click",
    "Right click": "Right click",
    "Copy to clipboard": "Copy to clipboard",
    "Paste from clipboard": "Paste from clipboard",
    "Cut to clipboard": "Cut to clipboard",
    "Element changed": "Element changed",
    "Text selected": "Text selected",
    "Activated tab": "Activated tab",
    "Closed tab": "Closed tab",
    "Page loaded": "Page loaded",
}


class TaskMiningAdapter(BaseAdapter):
    """
    Normalizes Celonis Task Mining UiEvents (from desktop client or
    Chrome/Edge extension) into the unified schema.

    Expected raw fields mirror the UiEvent class from task-mining-chrome-extension:
      timestamp, eventType, url, tabTitle, context, clipboardText,
      screenX, screenY, keyboardCommand, selectedText, domPath, extensionName
    """

    def normalize(self, raw_events: list[dict]) -> list[UnifiedActivityEvent]:
        return [self._convert(e) for e in raw_events]

    def _convert(self, raw: dict) -> UnifiedActivityEvent:
        source = EventSource.CELONIS_BROWSER
        if raw.get("extensionName") in (None, "", "desktop"):
            source = EventSource.CELONIS_DESKTOP

        app = raw.get("application") or self._infer_app(raw)

        return UnifiedActivityEvent(
            event_id=raw.get("event_id", str(uuid.uuid4())),
            timestamp=raw["timestamp"],
            event_type=_TM_EVENT_TYPE_MAP.get(raw["eventType"], raw["eventType"]),
            source=source.value,
            actor_type=ActorType.HUMAN.value,
            actor_id=raw.get("userId", raw.get("computerUserName", "unknown")),
            application=app,
            url=raw.get("url"),
            title=raw.get("tabTitle"),
            context={
                k: v
                for k, v in {
                    "clipboardText": raw.get("clipboardText"),
                    "selectedText": raw.get("selectedText"),
                    "keyboardCommand": raw.get("keyboardCommand"),
                    "elementType": (raw.get("context") or {}).get("elementType"),
                    "elementId": (raw.get("context") or {}).get("elementId"),
                }.items()
                if v
            },
            case_correlation_id=raw.get("caseId"),
            dom_path=raw.get("domPath"),
        )

    @staticmethod
    def _infer_app(raw: dict) -> str:
        url = raw.get("url", "")
        title = raw.get("tabTitle", "")
        if "sap" in title.lower() or "sap" in url.lower():
            return "SAP GUI"
        if "outlook" in url.lower() or "outlook" in title.lower():
            return "Outlook"
        if "sharepoint" in url.lower():
            return "SharePoint"
        if "excel" in title.lower():
            return "Excel"
        if raw.get("application"):
            return raw["application"]
        return raw.get("extensionName", "Browser")


# ---------- Microsoft Work IQ Adapter ----------

_WIQ_ACTION_MAP = {
    "copilot.invoke": "CopilotInvocation",
    "copilot.completion": "AgentCompletion",
    "copilot.toolCall": "AgentToolCall",
    "app.focus": "AppFocus",
    "app.switch": "AppSwitch",
    "meeting.join": "MeetingJoin",
    "meeting.leave": "MeetingLeave",
    "document.edit": "DocumentEdit",
    "document.open": "DocumentOpen",
    "email.send": "EmailSend",
    "email.read": "EmailRead",
    "click": "Left click",
}


class WorkIQAdapter(BaseAdapter):
    """
    Normalizes Microsoft Work IQ / Graph API signals into the unified schema.

    Work IQ provides app-usage telemetry plus Copilot interaction logs,
    surfaced via Microsoft Graph beta endpoints or the MCP context layer.
    """

    def normalize(self, raw_events: list[dict]) -> list[UnifiedActivityEvent]:
        return [self._convert(e) for e in raw_events]

    def _convert(self, raw: dict) -> UnifiedActivityEvent:
        action = raw.get("actionType", "")
        is_agent = raw.get("copilotUsed", False) or action.startswith("copilot.")

        actor_type = ActorType.AGENT.value if is_agent else ActorType.HUMAN.value
        if raw.get("actorType"):
            actor_type = raw["actorType"]

        event_type = _WIQ_ACTION_MAP.get(action, action)

        return UnifiedActivityEvent(
            event_id=raw.get("event_id", str(uuid.uuid4())),
            timestamp=raw["timestamp"],
            event_type=event_type,
            source=EventSource.WORK_IQ.value,
            actor_type=actor_type,
            actor_id=raw.get("userPrincipalName", raw.get("userId", "unknown")),
            application=raw.get("appHost", raw.get("application", "Unknown")),
            url=raw.get("resourceUrl"),
            title=raw.get("resourceTitle"),
            context={
                k: v
                for k, v in {
                    "prompt": raw.get("copilotPrompt"),
                    "output": raw.get("copilotResponse"),
                    "tool": raw.get("pluginName"),
                    "tool_calls": str(raw["pluginInvocations"]) if raw.get("pluginInvocations") else None,
                    "meeting_id": raw.get("meetingId"),
                    "duration_ms": raw.get("durationMs"),
                }.items()
                if v
            },
            case_correlation_id=raw.get("caseId"),
            dom_path=None,
        )
