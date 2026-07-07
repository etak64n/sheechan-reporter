"""Seen-state persistence and URL normalization for dedupe keys.

state/seen.json:
  bootstrapped_sources  sources whose backlog has been marked seen (see check_feeds.py)
  seen_urls             normalized URLs of articles already published or skipped
"""

import json
import os

from paths import STATE_PATH


def normalize_url(url: str) -> str:
    """Normalize a URL into a stable seen-key: strip tracking params and fragments."""
    url = url.split("#", 1)[0]
    if "?" in url:
        base, query = url.split("?", 1)
        kept = [p for p in query.split("&") if not p.lower().startswith(("utm_", "ref=", "sc_"))]
        url = base + ("?" + "&".join(kept) if kept else "")
    return url.rstrip("/")


def load_state() -> dict:
    try:
        with open(STATE_PATH) as f:
            state = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        state = {}
    state.setdefault("bootstrapped_sources", [])
    state.setdefault("seen_urls", [])
    return state


def save_state(state: dict) -> None:
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    state["seen_urls"] = sorted(set(state["seen_urls"]))
    state["bootstrapped_sources"] = sorted(set(state["bootstrapped_sources"]))
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
        f.write("\n")
