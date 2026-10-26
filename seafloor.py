"""Deterministic simulated seafloor camera frames and simple change detection.

No photographs, physical sensor data, NVIDIA Cosmos, or Nebius Jobs are used in
this module. This simulation demonstrates a future camera-analysis workflow.
"""

from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np
from PIL import Image, ImageDraw

WIDTH = 640
HEIGHT = 360

SCENARIOS = {
    "Stable seabed": "The two simulated camera frames are identical.",
    "Sediment displacement": "A simulated patch of brighter sediment appears between captures.",
    "Sediment recedes near cable": "A simulated sediment covering shifts away from a cable segment.",
}


@dataclass(frozen=True)
class ChangeFinding:
    changed_percent: float
    changed_pixels: int
    total_pixels: int
    bounding_box: Optional[Tuple[int, int, int, int]]
    threshold: int
    interpretation_hint: str


def _base_frame() -> Image.Image:
    """Create a labeled, consistent underwater illustration with a subsea cable."""
    rng = np.random.default_rng(1103)
    y = np.linspace(0, 1, HEIGHT, dtype=np.float32)[:, None]
    x = np.linspace(0, 1, WIDTH, dtype=np.float32)[None, :]
    grain = rng.normal(0, 5.0, (HEIGHT, WIDTH))
    channels = [
        np.clip(13 + 27 * y + 2 * x + grain, 0, 255),
        np.clip(47 + 44 * y + 2 * x + grain, 0, 255),
        np.clip(72 + 34 * y + 2 * x + grain, 0, 255),
    ]
    image = Image.fromarray(np.stack(channels, axis=2).astype(np.uint8), "RGB")
    draw = ImageDraw.Draw(image)
    # The cable is a stylized shape: no real pipeline or geolocation is implied.
    draw.line([(0, 288), (130, 290), (260, 282), (390, 292), (520, 285), (639, 290)], fill=(15, 18, 27), width=22)
    draw.line([(0, 285), (130, 287), (260, 279), (390, 289), (520, 282), (639, 287)], fill=(109, 134, 140), width=9)
    for i in range(185):
        px = int(rng.integers(0, WIDTH))
        py = int(rng.integers(220, HEIGHT))
        w = int(rng.integers(1, 4))
        shade = int(rng.integers(58, 106))
        draw.ellipse((px, py, px+w, py+w), fill=(shade, shade+17, shade+10))
    return image


def generate_frames(scenario: str) -> tuple[Image.Image, Image.Image]:
    """Return before/after images generated wholly in code (not Cosmos)."""
    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {scenario}")
    before = _base_frame()
    after = before.copy()
    draw = ImageDraw.Draw(after)
    if scenario == "Sediment displacement":
        draw.polygon(
            [(206, 251), (241, 218), (297, 221), (344, 237), (399, 254), (411, 286), (285, 299), (215, 285)],
            fill=(139, 144, 120),
        )
        draw.line([(220, 267), (282, 248), (334, 264), (379, 266)], fill=(173, 177, 145), width=4)
    elif scenario == "Sediment recedes near cable":
        # Receding cover reveals the fixed cable. The detector identifies a
        # camera-frame difference, NOT real material movement or cable damage.
        draw.polygon(
            [(185, 268), (225, 253), (272, 260), (313, 270), (322, 294), (273, 301), (204, 296)],
            fill=(92, 110, 105),
        )
        draw.arc((175, 260, 325, 307), 180, 355, fill=(168, 173, 143), width=7)
    return before, after


def analyze_frames(before: Image.Image, after: Image.Image, threshold: int = 25) -> tuple[ChangeFinding, Image.Image]:
    """Pixel-difference comparison, bounding box, and a visibly labeled overlay."""
    a = np.asarray(before.convert("RGB"), dtype=np.int16)
    b = np.asarray(after.convert("RGB"), dtype=np.int16)
    if a.shape != b.shape:
        raise ValueError("Before and after image dimensions must match")
    if not 0 <= threshold <= 255:
        raise ValueError("threshold must be between 0 and 255")
    delta = np.mean(np.abs(a - b), axis=2)
    mask = delta >= threshold if threshold > 0 else delta > 0
    coords = np.argwhere(mask)
    changed_pixels = int(mask.sum())
    total = int(mask.size)
    box = None
    overlay = after.copy()
    d = ImageDraw.Draw(overlay)
    if len(coords):
        y0, x0 = coords.min(axis=0).tolist()
        y1, x1 = coords.max(axis=0).tolist()
        box = (x0, y0, x1, y1)
        d.rectangle(box, outline=(255, 185, 62), width=5)
        d.text((max(4, x0), max(4, y0 - 20)), "VISUAL CHANGE", fill=(255, 218, 130))
    pct = changed_pixels / total * 100
    hint = (
        "No visual change detected in this simulated image pair."
        if changed_pixels == 0 else
        "Visual change detected in a simulated image pair. This does not confirm an actual seafloor hazard."
    )
    return ChangeFinding(pct, changed_pixels, total, box, threshold, hint), overlay
