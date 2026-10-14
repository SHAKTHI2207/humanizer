"""Request validation, rate limiting and error mapping. No web framework in here, so it is testable alone."""
import importlib.util, logging, os, threading, time
from collections import defaultdict, deque

import anthropic
from pydantic import BaseModel, Field, field_validator

import core

log = logging.getLogger("rewriter")
MAX_CHARS, MAX_SAMPLE = 20000, 5000
RATE, WINDOW = int(os.getenv("RATE_LIMIT", "20")), 60  # requests per client per minute
_hits, _lock = defaultdict(deque), threading.Lock()


class ApiError(Exception):
    def __init__(self, status, msg):
        super().__init__(msg)
        self.status, self.msg = status, msg


class Req(BaseModel):
    text: str = Field(max_length=MAX_CHARS)
    context: str = "general"
    options: dict[str, bool] = {}
    sample: str = Field("", max_length=MAX_SAMPLE)

    @field_validator("text")
    @classmethod
    def _text(cls, v):
        if not v.strip():
            raise ValueError("text is empty")
        return v

    @field_validator("context")
    @classmethod
    def _context(cls, v):
        if v not in core.CONTEXTS:
            raise ValueError("unknown context")
        return v

    @field_validator("options")
    @classmethod
    def _options(cls, v):
        if set(v) - set(core.OPTIONS):
            raise ValueError("unknown option")
        return v


def limited(ip, now=None):
    # ponytail: in-memory, single process; use a shared store (Redis) when running several workers
    now = time.monotonic() if now is None else now
    with _lock:
        q = _hits[ip]
        while q and now - q[0] > WINDOW:
            q.popleft()
        if len(q) >= RATE:
            return True
        q.append(now)
        return False


def run(req, ip):
    if limited(ip):
        raise ApiError(429, "Too many requests. Wait a minute and try again.")
    t = time.monotonic()
    try:
        segs = core.rewrite(req.text, req.context, req.options, req.sample)
    except anthropic.APITimeoutError:
        raise ApiError(504, "The model took too long to respond. Your text is unchanged. Try again.")
    except anthropic.APIError:
        raise ApiError(502, "The model provider returned an error. Your text is unchanged. Try again.")
    except anthropic.AnthropicError:
        raise ApiError(503, "Model credentials are not configured on the server.")
    # operational metadata only: sizes and timing, never the text
    log.info("rewrite ok context=%s segments=%d chars=%d secs=%.1f", req.context, len(segs), len(req.text),
             time.monotonic() - t)
    return segs


def config():
    return {"max_chars": MAX_CHARS, "max_sample": MAX_SAMPLE,
            "contexts": [{"key": k, "label": v[0]} for k, v in core.CONTEXTS.items()],
            "options": [{"key": k, "label": v[0], "default": v[1]} for k, v in core.OPTIONS.items()],
            "configured": bool(os.getenv("ANTHROPIC_API_KEY")) or core.DEMO, "demo": core.DEMO,
            "semantic": all(importlib.util.find_spec(m) for m in ("sentence_transformers", "transformers"))}
