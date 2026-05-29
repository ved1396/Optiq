import requests
import streamlit as st

BASE_URL = "http://localhost:8000"

def route_query(query: str):
    try:
        response = requests.post(f"{BASE_URL}/route", json={"query": query})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend: {e}")
        return None

def get_analytics(limit: int = 100):
    try:
        response = requests.get(f"{BASE_URL}/analytics", params={"limit": limit})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend: {e}")
        return []

def get_cost_summary():
    try:
        response = requests.get(f"{BASE_URL}/cost-summary")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend: {e}")
        return []

def get_energy_summary():
    try:
        response = requests.get(f"{BASE_URL}/energy-summary")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend: {e}")
        return []

def check_health():
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=3)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
