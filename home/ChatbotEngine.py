import json
import logging
from datetime import datetime

import requests as http_requests
from django.conf import settings

from .models import PlanModel

logger = logging.getLogger(__name__)

OUT_OF_SCOPE_MESSAGE = (
    "I'm StyleBot, your fashion assistant! I can only help with fashion, "
    "outfits, and event planning. Try asking me: What should I wear to a wedding?"
)


# Status codes that should trigger failover to the next key.
_FAILOVER_STATUS_CODES = {401, 402, 403, 404, 429, 500, 503}


class FashionChatbotEngine:
    def __init__(self):
        self.model = getattr(settings, "STYLEBOT_MODEL", "openai/gpt-4o-mini")
        # Build ordered list of keys, skipping blanks.
        key1 = getattr(settings, "OPENROUTER_API_KEY", "")
        key2 = getattr(settings, "OPENROUTER_API_KEY_2", "")
        self.api_keys = [k for k in [key1, key2] if k]
        # active_key used during a single request; reset each call.
        self.api_key = self.api_keys[0] if self.api_keys else ""

    def _system_prompt(self):
        return (
            "You are StyleBot, a fashion and event-styling assistant. "
            "You must be concise, practical, and specific. "
            "\n\n"
            "SCOPE (in-scope): fashion, clothing, outfits, styling, colors, accessories, "
            "dress codes, event outfit planning, weather-based outfit advice, budget outfit advice, "
            "and event plan creation. "
            "Treat short commands as in-scope, for example: 'casual outfit', 'budget outfit', "
            "'office outfit', 'wedding look', 'what should I wear'. "
            "\n\n"
            "OUT OF SCOPE: coding, math, politics, news, unrelated general knowledge, and non-fashion tasks. "
            "If out-of-scope, respond with EXACTLY this sentence and nothing else: "
            f"{OUT_OF_SCOPE_MESSAGE}"
            "\n\n"
            "RESPONSE STYLE FOR IN-SCOPE: always use these 4 headers exactly and keep each section short: "
            "\nEvent Suggestion:\n"
            "Outfit Recommendation:\n"
            "Why:\n"
            "Next Step:\n"
            "\n"
            "QUALITY RULES:\n"
            "1) Give actionable suggestions (items, colors, and context).\n"
            "2) If user asks budget outfit, include budget-conscious alternatives.\n"
            "3) If user asks casual/formal, reflect that explicitly in recommendation.\n"
            "4) If key details are missing (gender preference, weather, budget, event type), ask only 1-2 focused follow-up questions in Next Step.\n"
            "5) Do not be verbose. Avoid long paragraphs.\n"
            "\n"
            "PLAN SAVE RULE:\n"
            "If user asks to save a plan, collect missing fields naturally and call save_event_plan only when all required fields are available: title, event, due_date, time, priority."
        )

    def _base_url(self):
        return getattr(
            settings,
            "OPENROUTER_BASE_URL",
            "https://openrouter.ai/api/v1",
        ).rstrip("/")

    def _headers(self, key):
        return {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "HTTP-Referer": getattr(settings, "OPENROUTER_SITE_URL", "http://localhost:8000"),
            "X-Title": getattr(settings, "OPENROUTER_APP_NAME", "StylePredictor"),
        }

    def _chat(self, payload):
        """Try each key in order; fall over on quota/auth/404 errors."""
        url = f"{self._base_url()}/chat/completions"
        last_exc = None
        for idx, key in enumerate(self.api_keys):
            try:
                resp = http_requests.post(url, headers=self._headers(key), json=payload, timeout=60)
                if resp.status_code in _FAILOVER_STATUS_CODES and idx < len(self.api_keys) - 1:
                    logger.warning(
                        "stylebot_key_failover key_index=%d status=%d", idx, resp.status_code
                    )
                    continue
                resp.raise_for_status()
                return resp.json()
            except http_requests.exceptions.HTTPError as exc:
                last_exc = exc
                if idx < len(self.api_keys) - 1:
                    logger.warning(
                        "stylebot_key_failover key_index=%d error=%s", idx, exc
                    )
                    continue
                raise
        if last_exc:
            raise last_exc
        raise RuntimeError("No OpenRouter keys configured.")

    def _normalize_priority(self, value):
        p = (value or "").strip().lower()
        if p in ("high", "h"):
            return "H"
        if p in ("medium", "mid", "average", "m"):
            return "M"
        if p in ("low", "l"):
            return "L"
        return "M"

    def _normalize_event(self, value):
        e = (value or "").strip().lower()
        if "islam" in e or "eid" in e or "ramadan" in e:
            return "I"
        if "relig" in e:
            return "R"
        return "S"

    def _parse_date(self, value):
        for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
            try:
                return datetime.strptime(value, fmt).date()
            except Exception:
                continue
        return None

    def _parse_time(self, value):
        candidate = (value or "").strip()
        for fmt in ("%H:%M", "%I:%M %p", "%I %p"):
            try:
                return datetime.strptime(candidate, fmt).time()
            except Exception:
                continue
        return None

    def _save_event_plan(self, args, user):
        if not user or not user.is_authenticated:
            return {
                "ok": False,
                "error": "login_required",
                "message": "Login is required to save event plans.",
            }

        required = ["title", "event", "due_date", "time", "priority"]
        missing = [f for f in required if not args.get(f)]
        if missing:
            return {
                "ok": False,
                "error": "missing_fields",
                "missing": missing,
                "message": "Missing required fields: " + ", ".join(missing),
            }

        date_obj = self._parse_date(str(args.get("due_date", "")))
        if not date_obj:
            return {
                "ok": False,
                "error": "invalid_date",
                "message": "Invalid due_date format. Use YYYY-MM-DD.",
            }

        time_obj = self._parse_time(str(args.get("time", "")))
        if not time_obj:
            return {
                "ok": False,
                "error": "invalid_time",
                "message": "Invalid time format. Use HH:MM or 7:30 PM.",
            }

        title = str(args.get("title", "")).strip()[:30]
        event_text = str(args.get("event", "")).strip()
        priority_text = str(args.get("priority", "")).strip()

        event_code = self._normalize_event(event_text)
        priority_code = self._normalize_priority(priority_text)

        content = f"{title} -- {time_obj.strftime('%H:%M')} {event_text}"

        plan = PlanModel.objects.create(
            user=user,
            title=title,
            content=content,
            event=event_code,
            due_date=date_obj,
            time=time_obj,
            priority=priority_code,
        )

        logger.info("plan_saved user_id=%s plan_id=%s", user.id, plan.id)

        return {
            "ok": True,
            "plan_id": plan.id,
            "title": title,
            "event": event_text,
            "due_date": str(date_obj),
            "time": time_obj.strftime("%H:%M"),
            "priority": priority_text or "Medium",
            "message": "Plan saved successfully.",
        }

    def process_message(self, history, user_message, user):
        if not self.api_keys:
            return (
                "StyleBot is temporarily unavailable right now. Please try again in a bit. "
                "You can ask me: What should I wear to a wedding?",
                history,
                None,
            )

        clean_history = history[:] if isinstance(history, list) else []
        clean_history.append({"role": "user", "content": user_message})

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "save_event_plan",
                    "description": "Save an event plan for the authenticated user.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "event": {"type": "string"},
                            "due_date": {
                                "type": "string",
                                "description": "Date in YYYY-MM-DD format",
                            },
                            "time": {
                                "type": "string",
                                "description": "Time in HH:MM or 7:30 PM format",
                            },
                            "priority": {
                                "type": "string",
                                "description": "Low, Medium, or High",
                            },
                        },
                        "required": ["title", "event", "due_date", "time", "priority"],
                    },
                },
            }
        ]

        api_messages = [{"role": "system", "content": self._system_prompt()}] + clean_history

        plan_save_result = None
        try:
            first = self._chat({
                "model": self.model,
                "messages": api_messages,
                "tools": tools,
                "tool_choice": "auto",
                "temperature": 0.3,
            })
            first_msg = first["choices"][0]["message"]
            tool_calls = first_msg.get("tool_calls") or []

            if tool_calls:
                api_messages.append(
                    {
                        "role": "assistant",
                        "content": first_msg.get("content") or "",
                        "tool_calls": tool_calls,
                    }
                )

                first_call = tool_calls[0]
                function_obj = first_call.get("function", {})
                name = function_obj.get("name")
                args = json.loads(function_obj.get("arguments") or "{}")
                if name == "save_event_plan":
                    tool_result = self._save_event_plan(args, user)
                    plan_save_result = tool_result if tool_result.get("ok") else None
                else:
                    tool_result = {"ok": False, "error": "unsupported_tool"}

                api_messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": first_call.get("id"),
                        "content": json.dumps(tool_result),
                    }
                )

                second = self._chat({
                    "model": self.model,
                    "messages": api_messages,
                    "temperature": 0.3,
                })
                reply = (second["choices"][0]["message"].get("content") or "").strip()
            else:
                reply = (first_msg.get("content") or "").strip()

            if reply == OUT_OF_SCOPE_MESSAGE:
                logger.info("out_of_scope_refusal user_id=%s", getattr(user, "id", None))

            clean_history.append({"role": "assistant", "content": reply})
            clean_history = clean_history[-30:]
            return reply, clean_history, plan_save_result

        except Exception as ex:
            logger.exception("stylebot_api_error: %s", ex)
            fallback = (
                "StyleBot is temporarily unavailable right now. Please try again shortly. "
                "You can ask me fashion questions like: What should I wear to an office event?"
            )
            return fallback, clean_history[-30:], None
