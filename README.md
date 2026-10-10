# ResearchBuoy11

**AI Seafloor Stability Monitoring for Critical Infrastructure**

Track: **Physical AI** · Nebius Global AI Hackathon

🎥 **Demo video:** [YouTube link here]
📄 **License:** MIT (see [LICENSE](LICENSE))

> **Note on hardware:** This project has **no physical hardware component**. The buoy is a design concept. The demo video shows the **key application modules in action**, using synthetic seafloor footage in place of a real underwater camera.

---

## What it is

ResearchBuoy11 is a concept for a low-cost, solar-powered research buoy that monitors seafloor stability near subsea cables and pipelines. A surface buoy is tethered to a seafloor pod equipped with underwater cameras and LED lighting. On a set schedule, the pod lights the seafloor for a short period, captures images, and sends them up the tether for AI analysis.

Its mission is neutral, fact-finding research: detecting early signs of sediment shift, erosion, or slope movement before they become costly failures.

## Why we built it

Undersea cables and pipelines carry much of the world's data and energy, and damage to this infrastructure is increasingly in the news. Seafloor instability is one of the quieter causes of that damage, yet most stretches of seafloor are rarely observed. We wanted a simple, affordable way to watch them continuously and turn raw images into clear findings that operators, scientists, and governments can act on.

## How it works

The demo runs five application modules end to end:

```
Synthetic footage  →  Vision analysis  →  Reasoning agent  →  Real-world context  →  Dashboard
 (NVIDIA Cosmos)       (batch job)         (Nemotron)          (Tavily API)           (alerts)
```

1. **Synthetic sensor data** – NVIDIA Cosmos generates realistic underwater seafloor footage, including normal scenes and scenes showing instability, running on Nebius Serverless Jobs. This stands in for the buoy's camera.
2. **Vision analysis** – each simulated capture cycle is processed as a batch job that flags visual changes between images.
3. **Reasoning agent** – NVIDIA Nemotron, served through Nebius Token Factory, reviews the flagged changes, judges whether they matter, and writes a plain-language alert or report.
4. **Real-world context** – the agent uses the Tavily search API to check for recent earthquakes, storms, or reported incidents near the site and adds them to the alert.
5. **Dashboard** – alerts and images appear in a simple dashboard for operators and researchers.

## How we used NVIDIA and Nebius

| Tool | How it's used in ResearchBuoy11 |
|---|---|
| **NVIDIA Nemotron** | Reasoning agent that interprets flagged changes and writes alerts |
| **NVIDIA Cosmos** | Generates synthetic underwater seafloor footage for testing and the demo |
| **Nebius Token Factory** | Serves Nemotron for the agent. [Add 1–2 sentences on how Token Factory sped up your work, e.g. no model setup, fast API access.] |
| **Nebius Serverless Jobs** | Runs synthetic data generation and batch image analysis |
| **Tavily API** (third party) | Web search for real-world context such as earthquakes and storms |

## Setup and running

### Requirements

- Python 3.10 or newer
- A Nebius account with Token Factory access
- A Tavily API key

### 1. Clone the repository

```bash
git clone https://github.com/[your-username]/ResearchBuoy11.git
cd ResearchBuoy11
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add your API keys

Create a file named `.env` in the project folder:

```
NEBIUS_API_KEY=your_nebius_key_here
TAVILY_API_KEY=your_tavily_key_here
```

The `.env` file is listed in `.gitignore`, so your keys are never uploaded.

### 4. Run the demo

```bash
python [main_file_name].py
```

[Describe what happens when it runs, e.g. "This processes the sample footage in `data/`, prints alerts in the terminal, and opens the dashboard at http://localhost:8501."]

## Project structure

```
ResearchBuoy11/
├── [folder or file]     # [what it does]
├── [folder or file]     # [what it does]
├── requirements.txt     # Python dependencies
├── .gitignore
├── LICENSE
└── README.md
```

## What's next

Deploy a first prototype on the continental shelf (100–200 m), where many cables run and costs stay low, then scale the same design to deeper water.

## Hackathon note

ResearchBuoy11 was created during the Nebius Global AI Hackathon submission period.

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.
