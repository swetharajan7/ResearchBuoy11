# ResearchBuoy11

ResearchBuoy11: AI Seafloor Stability Monitoring for Critical Infrastructure

What it is
ResearchBuoy11 is a concept for a low-cost, solar-powered research buoy that monitors seafloor stability near subsea cables and pipelines. A surface buoy is tethered to a seafloor pod equipped with underwater cameras and LED lighting. On a set schedule, the pod lights the seafloor for a short period, captures images, and sends them up the tether for AI analysis. Its mission is neutral, fact-finding research: detecting early signs of sediment shift, erosion, or slope movement before they become costly failures.

Why we built it
Undersea cables and pipelines carry much of the world’s data and energy, and damage to this infrastructure is increasingly in the news. Seafloor instability is one of the quieter causes of that damage, yet most stretches of seafloor are rarely observed. We wanted a simple, affordable way to watch them continuously and turn raw images into clear findings that operators, scientists, and governments can act on.

How it works
This project has no physical hardware. Instead, the demo video shows the key application modules working end to end:

Synthetic sensor data: NVIDIA Cosmos generates realistic underwater seafloor footage, including normal scenes and scenes showing instability, running on Nebius Serverless Jobs. This stands in for the buoy’s camera.
Vision analysis: each simulated capture cycle is processed as a batch job that flags visual changes between images.
Reasoning agent: NVIDIA Nemotron, served through Nebius Token Factory, reviews the flagged changes, judges whether they matter, and writes a plain-language alert or report.
Real-world context: the agent uses the Tavily search API to check for recent earthquakes, storms, or reported incidents near the site and adds them to the alert.
Dashboard: alerts and images appear in a simple dashboard for operators and researchers.

Built with
NVIDIA Nemotron, NVIDIA Cosmos, Nebius Token Factory, Nebius Serverless Jobs, Tavily API.

What’s next
Deploy a first prototype on the continental shelf (100–200 m), where many cables run and costs stay low, then scale the same design to deeper water.
