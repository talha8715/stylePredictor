import json
import logging
from datetime import datetime

from django.conf import settings

import openai

from .models import PlanModel

logger = logging.getLogger(__name__)

OUT_OF_SCOPE_MESSAGE = (
    "I'm StyleBot, your fashion assistant! I can only help with fashion, "
    "outfits, and event planning. Try asking me: What should I wear to a wedding?"
)


class FashionChatbotEngine:
    def __init__(self):
        self.model = getattr(settings, "STYLEBOT_MODEL", "openai/gpt-4o-mini")
        self.api_key = getattr(settings, "OPENROUTER_API_KEY", "")

    def _system_prompt(self):
        return (
            "You are StyleBot, a smart AI fashion assistant. "
            "You ONLY help users with fashion and event-related topics, including: "
            "event suggestions, dress category recommendations, outfit ideas, colors, "
            "weather-based styling, budget outfit guidance, and event planning. "
            "\n\n"
            "If a user asks ANYTHING outside fashion, clothing, events, or style, "
            "respond ONLY with this exact sentence and nothing else: "
            f"{OUT_OF_SCOPE_MESSAGE}"
            "\n\n"
            "For in-scope responses, always use this exact structure with these headers:"
            "\nEvent Suggestion:\n"
            "Outfit Recommendation:\n"
            "Why:\n"
            "Next Step:\n"
            "\n"
            "When the user asks to save an event plan, collect missing fields naturally and "
            "call the save_event_plan tool only when all required fields are available."
        )

    def _get_client(self):
        if not self.api_key:
            return None
        try:
            openai.api_key = self.api_key
            openai.api_base = getattr(
                settings,
                "OPENROUTER_BASE_URL",
                "https://openrouter.ai/api/v1",
            )
            return openai
        except Exception as ex:
            logger.exception("stylebot_openai_import_error: %s", ex)
            return None

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
        client = self._get_client()
        if client is None:
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
            first = client.ChatCompletion.create(
                model=self.model,
                messages=api_messages,
                tools=tools,
                tool_choice="auto",
                temperature=0.3,
            )
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

                second = client.ChatCompletion.create(
                    model=self.model,
                    messages=api_messages,
                    temperature=0.3,
                )
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
