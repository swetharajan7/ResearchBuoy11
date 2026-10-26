# ResearchBuoy11

**AI-assisted seafloor observation — software-only prototype**  
Physical AI track concept · Nebius × NVIDIA Global AI Hackathon

ResearchBuoy11 is a proposed low-cost, solar-powered ocean research buoy designed to monitor changes near subsea cables and pipelines. The **current prototype does not include a physical buoy, underwater camera, NVIDIA Cosmos-generated imagery, or Nebius Serverless Jobs**. It uses **deterministic, procedurally generated illustrative seafloor frames** to demonstrate change detection, followed by **real NVIDIA Nemotron 3 Super inference through Nebius Token Factory** if a user supplies an API key.

This distinction matters: a detected difference between two illustrations is **not** a validated geotechnical hazard, marine sensor reading, or physical AI field test.

## What's implemented

- Two synthetic camera-frame illustrations, including stable, sediment displacement, and cable-adjacent change examples.
- Programmatic change detection (mean per-pixel RGB difference), a visible bounding rectangle, and measurable changed area.
- Optional **live** `nvidia/nemotron-3-super-120b-a12b` text reasoning over the measured observation through Nebius Token Factory's OpenAI-compatible `/chat/completions` API.
- Optional Tavily regional public-search results used as **supplementary context**, never as proof that something happened in the simulated frame.
- Interactive Streamlit interface suitable for a screen-recorded software demonstration.

## Architecture

```text
Synthetic illustrated frames (NumPy / Pillow; NOT Cosmos)
     ↓
Pixel-difference analysis in Python
     ↓
Measured observations (changed area and bounding rectangle)
     ↓
NVIDIA Nemotron 3 Super via Nebius Token Factory (real API, with key)
     ↓
Operator-facing simulated-observation report
```

Tavily may supply additional regional context. No autonomous scheduling, physical sensors, hosted NVIDIA Cosmos execution, Nebius Serverless Jobs, or GPU instances are implemented in this MVP. These are possible **future development directions**, not shipped functionality.

## Quick start

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local address that Streamlit prints (usually http://localhost:8501).

1. Select `Sediment displacement` and click **Run image comparison**. See the bounding rectangle and measured change.
2. Enter a Nebius Token Factory API key into the sidebar and click **Generate a real Nemotron report**. This makes a paid/usage-metered API request, depending on your Nebius account.
3. Optionally enter a region and Tavily key to append public-search context to the real model request.
4. Try `Stable seabed` and compare how the reported measurement changes.

To use environment variables rather than entering keys in the UI:

```bash
export NEBIUS_API_KEY="your_key"
export NEBIUS_BASE_URL="https://api.tokenfactory.us-central1.nebius.com/v1"
export NEBIUS_MODEL="nvidia/nemotron-3-super-120b-a12b"
export TAVILY_API_KEY="optional_key"
```

For Streamlit Community Cloud, deploy the GitHub repository with `app.py` as the entrypoint, and add `NEBIUS_API_KEY` (and optional `TAVILY_API_KEY`) through **app Secrets**. Never put credentials into source code, the README, or a screen recording.

## Repeatable tests

```bash
python -m unittest discover -s tests -v
```

## Demonstration guidance (Physical AI track)

The hackathon requires a video under three minutes, with at least one minute of the **key application modules visibly operating** when there is no hardware. Screen-record the UI while changing scenarios, performing image comparison, and invoking a **real Nemotron API request**; never substitute a fabricated model response. Label the illustrations as simulations.

A live Nemotron call is required to demonstrate the model integration. The code and tests can run without credentials, but model inference cannot be tested without the user's API key.

For the Physical AI track, review the official rules carefully: the desired architecture also includes Nebius Serverless Jobs for simulations or scaled sensor processing. **Serverless Jobs and Cosmos are not implemented here**, so this MVP should not be described as satisfying all originally proposed track features.

## Future work

1. Generate more realistic synthetic seafloor imagery with NVIDIA Cosmos via supported Nebius infrastructure.
2. Run image-analysis batches or simulations on Nebius Serverless Jobs.
3. Introduce real camera captures from a tested tethered pod and validate image analysis against environmental data.
4. Add secure historical monitoring, operator review, and scientifically validated thresholds before issuing operational alerts.

## License

MIT — see [LICENSE](LICENSE).
