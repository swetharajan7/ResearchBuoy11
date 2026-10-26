"""Real Nebius Token Factory inference and optional Tavily public search."""

import os
import requests

DEFAULT_NEBIUS_BASE_URL = "https://api.tokenfactory.us-central1.nebius.com/v1"
DEFAULT_NEBIUS_MODEL = "nvidia/nemotron-3-super-120b-a12b"


def fetch_regional_context(api_key: str, region: str) -> list[dict]:
    """Retrieve optional regional news; never infer that it caused image changes."""
    if not api_key or not region.strip():
        return []
    response = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key": api_key,
            "query": f"recent earthquake seabed landslide major storm offshore {region}",
            "search_depth": "basic",
            "max_results": 3,
        },
        timeout=25,
    )
    response.raise_for_status()
    return [
        {"title": item.get("title", "Untitled"), "url": item.get("url", ""), "excerpt": item.get("content", "")[:650]}
        for item in response.json().get("results", [])[:3]
    ]


def ask_nemotron(api_key: str, scenario: str, finding, context: list[dict] | None = None,
                 base_url: str | None = None, model: str | None = None) -> str:
    """Ask Nemotron to explain measured numerical features, not unseen pixels."""
    if not api_key.strip():
        raise ValueError("A Nebius Token Factory API key is required for a live model response")
    context = context or []
    base_url = (base_url or os.getenv("NEBIUS_BASE_URL") or DEFAULT_NEBIUS_BASE_URL).rstrip("/")
    model = model or os.getenv("NEBIUS_MODEL") or DEFAULT_NEBIUS_MODEL
    user_message = f"""Interpret this observation from a SOFTWARE-ONLY SIMULATION.
Scenario: {scenario}
Two procedurally generated illustrative frames compared by pixel difference.
Changed pixels: {finding.changed_pixels} / {finding.total_pixels}
Changed area: {finding.changed_percent:.2f}%
Detection threshold: {finding.threshold} average RGB intensity units
Change bounding rectangle (pixels): {finding.bounding_box}
Regional public-search results, if supplied (do not infer causation): {context}

Output a short operator-facing report with: (1) observed change, (2) limitations and uncertainty,
(3) suggested next verification step. Be explicit that there is NO physical buoy, no real camera,
no actual site location, and no validated hazard detection. Distinguish image-difference
measurement from your interpretation. Do not fabricate events, sources, or hazard probabilities.
"""
    response = requests.post(
        f"{base_url}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a careful scientific research assistant. Never mistake simulated imagery for real-world sensor data. Be concise and uncertainty-aware."},
                {"role": "user", "content": user_message},
            ],
            "max_tokens": 900,
            "temperature": 0.2,
        },
        timeout=120,
    )
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        raise RuntimeError(f"Nebius API returned HTTP {response.status_code}. Check your key, model, account balance, and endpoint.") from exc
    payload = response.json()
    choices = payload.get("choices", [])
    answer = (choices[0].get("message", {}).get("content") if choices else None)
    if isinstance(answer, list):
        answer = "\n".join(str(item.get("text", "")) for item in answer if isinstance(item, dict))
    if not answer:
        raise RuntimeError("Nebius returned no visible model response. Check the model settings.")
    return str(answer)
