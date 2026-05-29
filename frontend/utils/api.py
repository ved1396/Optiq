import os

import requests
import streamlit as st

BASE_URL = os.getenv("OPTIQ_BACKEND_URL", "http://localhost:8000")
TIMEOUT = 10


def _request(method: str, path: str, **kwargs):
    try:
        response = requests.request(method, f"{BASE_URL}{path}", timeout=TIMEOUT, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        st.error(f"Backend request failed: {exc}")
        return None


def route_query(query: str):
    return _request("POST", "/route", json={"query": query})


def submit_feedback(query_id: int, rating: int, comments: str | None = None, correct_route: str | None = None):
    return _request(
        "POST",
        "/feedback",
        json={
            "query_id": query_id,
            "rating": rating,
            "comments": comments,
            "correct_route": correct_route,
        },
    )


def get_analytics(limit: int = 500):
    return _request("GET", "/analytics", params={"limit": limit}) or {}


def get_cost_summary():
    return _request("GET", "/cost-summary") or {}


def get_energy_summary():
    return _request("GET", "/energy-summary") or {}


def get_health():
    return _request("GET", "/health") or {}
