"""ResearchBuoy11 — honest software prototype for a future research buoy."""

import os

import streamlit as st

from nemotron import ask_nemotron, fetch_regional_context
from seafloor import SCENARIOS, analyze_frames, generate_frames

st.set_page_config(page_title="ResearchBuoy11 | Seafloor Monitoring", page_icon="🌊", layout="wide")


def secret(name: str) -> str:
    try:
        return str(st.secrets.get(name, os.environ.get(name, "")))
    except (FileNotFoundError, KeyError):
        return os.environ.get(name, "")


st.title("🌊 ResearchBuoy11")
st.caption("AI Seafloor Stability Monitoring for Critical Infrastructure")
st.warning("SOFTWARE-ONLY RESEARCH DEMONSTRATION — Illustrative frames, not a real buoy or underwater camera. No Cosmos/Serverless Jobs deployment is claimed.")
st.write(
    "A prototype workflow for a future solar-powered buoy and seafloor camera pod. "
    "First compare two simulated camera frames, then request a real, evidence-aware "
    "interpretation from NVIDIA Nemotron on Nebius Token Factory."
)

with st.sidebar:
    st.header("Observation setup")
    scenario = st.selectbox("Synthetic observation", list(SCENARIOS))
    st.caption(SCENARIOS[scenario])
    sensitivity = st.slider("Pixel change threshold", min_value=5, max_value=80, value=25, step=5)
    st.divider()
    st.subheader("Optional live inference")
    nebius_key = st.text_input("Nebius Token Factory API key", value=secret("NEBIUS_API_KEY"), type="password", help="Kept in this browser session / app process. Never commit a key to GitHub.")
    st.caption("The model is invoked only when you click the button; it may incur inference charges.")
    st.divider()
    st.subheader("Optional outside context")
    region = st.text_input("Region to research", placeholder="e.g. Gulf of Mexico (optional)")
    tavily_key = st.text_input("Tavily API key", value=secret("TAVILY_API_KEY"), type="password")
    st.caption("News search is supplementary context, NOT proof about this simulated scene.")

before, after = generate_frames(scenario)
left, right = st.columns(2)
with left:
    st.image(before, caption="Simulated capture A — baseline", use_container_width=True)
with right:
    st.image(after, caption="Simulated capture B — follow-up", use_container_width=True)

st.subheader("Module 1 · Visual change detection")
if st.button("Run image comparison", type="primary", use_container_width=True):
    finding, overlay = analyze_frames(before, after, sensitivity)
    st.session_state["finding"] = finding
    st.session_state["overlay"] = overlay
    st.session_state["setting"] = (scenario, sensitivity)
    st.session_state.pop("nemotron_report", None)
    st.session_state.pop("supporting_sources", None)

valid = st.session_state.get("setting") == (scenario, sensitivity)
if valid:
    finding = st.session_state["finding"]
    st.image(st.session_state["overlay"], caption="Highlighted region — programmatic pixel comparison, not an AI vision diagnosis", width=640)
    m1, m2, m3 = st.columns(3)
    m1.metric("Image pixels changed", f"{finding.changed_percent:.2f}%")
    m2.metric("Changed pixels", f"{finding.changed_pixels:,}")
    m3.metric("Detection threshold", str(finding.threshold))
    st.info(finding.interpretation_hint)
else:
    st.info("Choose a scenario and run image comparison to produce a measured finding.")

st.subheader("Module 2 · NVIDIA Nemotron reasoning via Nebius Token Factory")
st.caption("Nebius receives computed observations and optional public-search context. This prototype does not send images to a vision model.")
if st.button("Generate a real Nemotron report", disabled=not valid or not nebius_key, use_container_width=True):
    with st.spinner("Running optional context retrieval and live Nemotron inference…"):
        try:
            context = fetch_regional_context(tavily_key, region) if (tavily_key and region.strip()) else []
            report = ask_nemotron(nebius_key, scenario, st.session_state["finding"], context=context)
            st.session_state["nemotron_report"] = report
            st.session_state["supporting_sources"] = context
            st.session_state["report_setting"] = (scenario, sensitivity)
        except Exception as exc:
            st.error(f"Live API call failed: {exc}")
if not nebius_key:
    st.info("To demonstrate actual Nemotron inference, add your Nebius Token Factory key in the sidebar.")
if st.session_state.get("report_setting") == (scenario, sensitivity) and st.session_state.get("nemotron_report"):
    st.success("Live Nemotron response received")
    st.markdown(st.session_state["nemotron_report"])
    context = st.session_state.get("supporting_sources", [])
    if context:
        st.markdown("**Supplementary regional public-search results — not evidence of simulated seafloor activity:**")
        for source in context:
            st.markdown(f"- [{source['title']}]({source['url']})")

st.subheader("Module 3 · Prototype architecture")
st.code("Synthetic illustrated frames → Pixel-difference detector → Measured change → Nebius Token Factory / Nemotron → Cautious operator report", language="text")
st.caption("Future work (NOT implemented): NVIDIA Cosmos synthetic video, Nebius Serverless Jobs, genuine ocean sensors, field validation, automated time-series monitoring, and operator alerts.")
