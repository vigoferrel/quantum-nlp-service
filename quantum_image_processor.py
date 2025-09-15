#!/usr/bin/env python3
"""
⚛️ Quantum Image Processor (26D)
Enhanced 26-dimensional analysis using Pillow + NumPy only (no OpenCV).
Integrates QBTC dimensional model: 7 principal dimensions (3D-9D),
7 sacred geometries, 7 consciousness levels, and 5 Merkaba phases.
"""

import io
import math
import os
import time
import json
import logging
from dataclasses import dataclass
from typing import Dict, Any, List, Tuple

import numpy as np
from PIL import Image, ImageStat, ImageFilter

try:
    import cv2
except Exception:
    cv2 = None

# Prometheus-safe counters (no-op if prometheus_client not available)
try:
    from prometheus_client import Counter
    _METRICS_ENABLED = True
except Exception:
    Counter = None
    _METRICS_ENABLED = False

class _NoopCtr:
    def inc(self, *a, **k): pass

logger = logging.getLogger(__name__)

# Metrics counters
_small_image_skipped = Counter("qnlp_small_image_skipped_total","Small images skipped") if _METRICS_ENABLED else _NoopCtr()
_kernel_bad_size_events = Counter("qnlp_kernel_bad_size_events_total","Bad kernel size exceptions") if _METRICS_ENABLED else _NoopCtr()
_empty_slice_events = Counter("qnlp_empty_slice_events_total","Empty slice mean attempted") if _METRICS_ENABLED else _NoopCtr()

# Configuration from environment
MIN_IMAGE_SIDE_FOR_KERNEL = int(os.getenv("QIS_MIN_IMAGE_SIDE_FOR_KERNEL", "3"))
SMALL_IMAGE_FALLBACK = os.getenv("QIS_SMALL_IMAGE_FALLBACK", "identity")  # identity|upsample

def safe_mean(arr, default=np.nan):
    """Safe mean calculation that handles empty arrays"""
    if arr is None or getattr(arr, "size", 0) == 0:
        _empty_slice_events.inc()
        return default
    with np.errstate(all="ignore"):
        val = np.nanmean(arr)
    if np.isnan(val):
        return default
    return float(val)

PHI = 1.61803398875

@dataclass
class QuantumImageResult:
    analysis: str
    confidence: float
    processing_type: str
    metadata: Dict[str, Any]


def _to_grayscale(img: Image.Image) -> Image.Image:
    if img.mode != 'L':
        return img.convert('L')
    return img


def _resize_safely(img: Image.Image, max_side: int = 640) -> Image.Image:
    w, h = img.size
    scale = min(1.0, max_side / max(w, h))
    if scale < 1.0:
        return img.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.Resampling.LANCZOS)
    return img


def _image_stats(img: Image.Image) -> Dict[str, Any]:
    stat = ImageStat.Stat(img)
    mean = stat.mean[0] if len(stat.mean) == 1 else sum(stat.mean) / len(stat.mean)
    std = stat.stddev[0] if len(stat.stddev) == 1 else sum(stat.stddev) / len(stat.stddev)
    return {
        'mean': float(mean),
        'std': float(std),
        'entropy_estimate': float(np.clip(_entropy_estimate(np.array(_to_grayscale(img))), 0.0, 8.0))
    }


def _entropy_estimate(gray_np: np.ndarray) -> float:
    hist, _ = np.histogram(gray_np.flatten(), bins=256, range=(0, 255), density=True)
    hist = hist[hist > 1e-12]
    return -float(np.sum(hist * np.log2(hist)))


def _edge_map(gray: Image.Image) -> np.ndarray:
    edges = gray.filter(ImageFilter.FIND_EDGES)
    arr = np.asarray(edges, dtype=np.float32)
    arr = arr / (arr.max() + 1e-6)
    return arr


def _box_counting_fractal_dimension(edge_arr: np.ndarray) -> float:
    # Binarize
    thr = np.clip(edge_arr.mean() + edge_arr.std(), 0.1, 0.9)
    bw = (edge_arr > thr).astype(np.uint8)
    # ensure min size
    h, w = bw.shape
    max_box = min(h, w)
    sizes = []
    box_counts = []
    s = max_box
    # Use powers of 2 down to 4
    while s >= 4:
        sizes.append(s)
        # Count boxes that contain at least one pixel
        count = 0
        for y in range(0, h, s):
            for x in range(0, w, s):
                if np.any(bw[y:y+s, x:x+s]):
                    count += 1
        box_counts.append(count)
        s //= 2
    if len(sizes) < 2:
        return 1.0
    sizes = np.array(sizes, dtype=np.float64)
    box_counts = np.array(box_counts, dtype=np.float64) + 1e-9
    # Fractal dim = -slope of log(box_counts) vs log(size)
    slope, _ = np.polyfit(np.log(sizes), np.log(box_counts), 1)
    return float(-slope)


def _fft_features(gray_np: np.ndarray) -> Dict[str, float]:
    # 2D FFT magnitude
    F = np.fft.fft2(gray_np)
    Fshift = np.fft.fftshift(F)
    mag = np.abs(Fshift)
    mag = mag / (mag.max() + 1e-6)
    h, w = mag.shape
    cy, cx = h // 2, w // 2
    r = min(h, w) // 6
    # low freq energy (center circle)
    Y, X = np.ogrid[:h, :w]
    mask_center = (X - cx) ** 2 + (Y - cy) ** 2 <= r ** 2
    low_e = float(mag[mask_center].mean())
    # high freq energy (outer ring)
    mask_outer = (X - cx) ** 2 + (Y - cy) ** 2 >= (r * 2) ** 2
    high_e = float(mag[mask_outer].mean()) if np.any(mask_outer) else 0.0
    low_high_ratio = float(low_e / (high_e + 1e-6))
    # directional anisotropy (horizontal vs vertical bands)
    vert_band = safe_mean(mag[:, max(0, cx - r // 4):min(w, cx + r // 4)], default=0.0)
    horiz_band = safe_mean(mag[max(0, cy - r // 4):min(h, cy + r // 4), :], default=0.0)
    anisotropy = float(abs(vert_band - horiz_band))
    return {
        'low_freq_energy': low_e,
        'high_freq_energy': high_e,
        'low_high_ratio': low_high_ratio,
        'directional_anisotropy': anisotropy
    }


def _symmetry_metrics(gray_np: np.ndarray) -> Dict[str, float]:
    # Normalize
    g = gray_np.astype(np.float32)
    g = (g - g.min()) / (g.max() - g.min() + 1e-6)
    # Mirror diffs
    lr = np.fliplr(g)
    tb = np.flipud(g)
    lr_sim = 1.0 - float(np.mean(np.abs(g - lr)))
    tb_sim = 1.0 - float(np.mean(np.abs(g - tb)))
    center = g[g.shape[0]//4: 3*g.shape[0]//4, g.shape[1]//4: 3*g.shape[1]//4]
    c_lr = 1.0 - float(np.mean(np.abs(center - np.fliplr(center))))
    c_tb = 1.0 - float(np.mean(np.abs(center - np.flipud(center))))
    return {
        'lr_symmetry': lr_sim,
        'tb_symmetry': tb_sim,
        'center_lr_sym': c_lr,
        'center_tb_sym': c_tb
    }


def _golden_ratio_features(w: int, h: int, gray_np: np.ndarray) -> Dict[str, Any]:
    ratio = w / (h + 1e-6)
    phi_closeness = 1.0 - float(min(abs(ratio - PHI), abs((1/ratio) - PHI))) / PHI
    # Rule-of-thirds/phi lines brightness sampling
    thirds_x = [int(w/PHI), int(w - w/PHI)]
    thirds_y = [int(h/PHI), int(h - h/PHI)]
    samples = []
    for x in thirds_x:
        if 0 <= x < w:
            samples.append(safe_mean(gray_np[:, x], default=0.0))
    for y in thirds_y:
        if 0 <= y < h:
            samples.append(safe_mean(gray_np[y, :], default=0.0))
    if samples:
        norm_samples = (np.array(samples) - gray_np.mean()) / (gray_np.std() + 1e-6)
        alignment_strength = float(np.clip(np.mean(np.abs(norm_samples)), 0.0, 3.0) / 3.0)
    else:
        alignment_strength = 0.0
    return {
        'aspect_ratio': float(ratio),
        'phi_closeness': float(np.clip(phi_closeness, 0.0, 1.0)),
        'phi_alignment_strength': alignment_strength
    }


def _ui_pattern_signals(gray: Image.Image) -> Dict[str, float]:
    # Safety check for kernel size
    if gray.size[0] < MIN_IMAGE_SIDE_FOR_KERNEL or gray.size[1] < MIN_IMAGE_SIDE_FOR_KERNEL:
        logger.info(f"Small image ({gray.size[0]}x{gray.size[1]}) detected in _ui_pattern_signals; returning zeros")
        _small_image_skipped.inc()
        return {
            'horizontal_edge_ratio': 0.0,
            'vertical_edge_ratio': 0.0,
            'gridness': 0.0
        }
    # Simple directional edge detectors as UI proxies with error handling
    try:
        horiz = gray.filter(ImageFilter.Kernel((1, 3), [-1, 2, -1], 1, 0))
        vert = gray.filter(ImageFilter.Kernel((3, 1), [-1, 2, -1], 1, 0))
    except Exception as e:
        logger.warning(f"Kernel filter failed in _ui_pattern_signals: {e}")
        _kernel_bad_size_events.inc()
        return {
            'horizontal_edge_ratio': 0.0,
            'vertical_edge_ratio': 0.0,
            'gridness': 0.0
        }
    ha = np.asarray(horiz, dtype=np.float32)
    va = np.asarray(vert, dtype=np.float32)
    ha = ha / (ha.max() + 1e-6)
    va = va / (va.max() + 1e-6)
    total = gray.size[0] * gray.size[1]
    h_edges = float(np.sum(ha > 0.6)) / total
    v_edges = float(np.sum(va > 0.6)) / total
    gridness = float(min(1.0, (h_edges + v_edges) * 2.0))
    return {
        'horizontal_edge_ratio': h_edges,
        'vertical_edge_ratio': v_edges,
        'gridness': gridness
    }


def _skin_nature_monochrome_flags(img: Image.Image) -> Dict[str, bool]:
    small = img.resize((64, 64), Image.Resampling.LANCZOS)
    arr = np.asarray(small, dtype=np.float32)
    R, G, B = arr[..., 0], arr[..., 1], arr[..., 2]
    skin_mask = (R > 95) & (G > 40) & (B > 20) & ((np.maximum(np.maximum(R, G), B) - np.minimum(np.minimum(R, G), B)) > 15) & (np.abs(R - G) > 15) & (R > G) & (R > B)
    has_skin = float(np.mean(skin_mask)) > 0.08
    nature_mask = (G > R) | (B > R)
    has_nature = float(np.mean(nature_mask)) > 0.35
    # monochrome test via std across channels
    std_channels = np.std(arr, axis=(0, 1))
    is_mono = bool(np.all(std_channels < 20))
    return {
        'has_skin_tones': bool(has_skin),
        'has_nature_colors': bool(has_nature),
        'is_monochrome': is_mono
    }


def _sacred_geometry_scores(phi: Dict[str, float], sym: Dict[str, float], fft: Dict[str, float], edge_arr: np.ndarray, ui: Dict[str, float]) -> Dict[str, float]:
    scores = {}
    # Heuristics for sacred geometry detection scores (0-1)
    scores['golden_spiral'] = float(np.clip(0.6 * phi['phi_closeness'] + 0.4 * phi['phi_alignment_strength'], 0.0, 1.0))
    # Flower of life ~ hex grid signature => high gridness + balanced anisotropy
    scores['flower_of_life'] = float(np.clip(0.7 * ui['gridness'] + 0.3 * (1.0 - abs(fft['directional_anisotropy'] - 0.05) / 0.5), 0.0, 1.0))
    # Sri Yantra ~ triangular symmetry => strong central symmetry
    scores['sri_yantra'] = float(np.clip(0.5 * sym['center_lr_sym'] + 0.5 * sym['center_tb_sym'], 0.0, 1.0))
    # Metatron's cube ~ complex structured edges + gridness
    scores['metatrons_cube'] = float(np.clip(0.5 * ui['gridness'] + 0.5 * float(edge_arr.mean()), 0.0, 1.0))
    # Platonic solids ~ strong symmetry overall
    scores['platonic_solids'] = float(np.clip((sym['lr_symmetry'] + sym['tb_symmetry']) / 2.0, 0.0, 1.0))
    # Torus field ~ balanced low/high frequency energy
    low_high_bal = 1.0 - abs(fft['low_high_ratio'] - 1.0) / (fft['low_high_ratio'] + 1.0)
    scores['torus_field'] = float(np.clip(low_high_bal, 0.0, 1.0))
    # Vesica Piscis ~ overlapping ovals signaled by moderate grid + symmetry
    scores['vesica_piscis'] = float(np.clip(0.4 * ui['gridness'] + 0.6 * ((sym['lr_symmetry'] + sym['tb_symmetry']) / 2.0), 0.0, 1.0))
    return scores


def _quantum_coherence(sym: Dict[str, float], fft: Dict[str, float], fractal_dim: float) -> float:
    # Coherence favors symmetry, balanced spectrum, and natural fractal dimension (~1.6-1.8)
    sym_score = (sym['lr_symmetry'] + sym['tb_symmetry'] + sym['center_lr_sym'] + sym['center_tb_sym']) / 4.0
    fractal_pref = 1.0 - min(abs(fractal_dim - 1.7) / 0.7, 1.0)
    spec_balance = 1.0 - min(abs(fft['low_high_ratio'] - 1.0) / (fft['low_high_ratio'] + 1e-6), 1.0)
    coh = 0.45 * sym_score + 0.35 * spec_balance + 0.20 * fractal_pref
    return float(np.clip(coh, 0.0, 1.0))


def _entanglement_summary(gray_np: np.ndarray) -> Dict[str, Any]:
    h, w = gray_np.shape
    H = h // 3
    W = w // 3
    cells = []
    for i in range(3):
        for j in range(3):
            region = gray_np[i*H:(i+1)*H, j*W:(j+1)*W]
            cells.append(safe_mean(region, default=0.0))
    cells = np.array(cells, dtype=np.float32)
    cells = (cells - cells.mean()) / (cells.std() + 1e-6)
    # Correlation with center cell (index 4)
    center = cells[4]
    corr = float(np.mean(cells * center))  # simplified correlation summary
    # Pair symmetry correlations
    lr_corr = float(np.mean((cells[1] + cells[7]) / 2.0 - (cells[3] + cells[5]) / 2.0))
    tb_corr = float(np.mean((cells[3] + cells[5]) / 2.0 - (cells[1] + cells[7]) / 2.0))
    return {
        'center_correlation': corr,
        'lr_axis_balance': lr_corr,
        'tb_axis_balance': tb_corr,
        'grid_means': cells.tolist()
    }


def _dimension_scores(features: Dict[str, Any]) -> Dict[str, float]:
    # Unpack
    stat = features['stats']
    fft = features['fft']
    sym = features['sym']
    phi = features['phi']
    flags = features['flags']
    fractal_dim = features['fractal_dim']
    ui = features['ui']

    # Principal dimensions (3D-9D)
    scores = {}
    scores['3D_physical'] = float(np.clip(0.5 * (stat['mean'] / 255.0) + 0.5 * (stat['std'] / 64.0), 0.0, 1.0))
    scores['4D_temporal'] = float(np.clip(1.0 - min(abs(fft['directional_anisotropy'] - 0.1) / 0.8, 1.0), 0.0, 1.0))
    scores['5D_probability'] = float(np.clip(stat['entropy_estimate'] / 8.0, 0.0, 1.0))
    scores['6D_consciousness'] = float(np.clip((0.6 * (1.0 if flags['has_skin_tones'] else 0.3) + 0.4 * ((sym['center_lr_sym'] + sym['center_tb_sym']) / 2.0)), 0.0, 1.0))
    scores['7D_divine'] = float(np.clip(0.6 * phi['phi_closeness'] + 0.4 * ((sym['lr_symmetry'] + sym['tb_symmetry']) / 2.0), 0.0, 1.0))
    scores['8D_infinite'] = float(np.clip(0.5 * (1.0 - abs(fft['low_high_ratio'] - 1.0) / (fft['low_high_ratio'] + 1e-6)) + 0.5 * (1.0 - abs(fractal_dim - 1.9) / 1.1), 0.0, 1.0))
    scores['9D_universal'] = float(np.clip(0.5 * ((sym['lr_symmetry'] + sym['tb_symmetry']) / 2.0) + 0.5 * (1.0 - abs(fractal_dim - 1.7) / 0.9), 0.0, 1.0))

    # Sacred geometries
    sg = features['sacred']
    scores['flower_of_life'] = sg['flower_of_life']
    scores['sri_yantra'] = sg['sri_yantra']
    scores['metatrons_cube'] = sg['metatrons_cube']
    scores['golden_spiral'] = sg['golden_spiral']
    scores['platonic_solids'] = sg['platonic_solids']
    scores['torus_field'] = sg['torus_field']
    scores['vesica_piscis'] = sg['vesica_piscis']

    # Consciousness levels (soft memberships)
    consciousness = float(np.clip((scores['6D_consciousness'] + scores['7D_divine'] + scores['9D_universal']) / 3.0, 0.0, 1.0))
    scores['sleeping'] = float(np.clip(1.0 - (consciousness * 1.5), 0.0, 1.0))
    scores['awakening'] = float(np.clip(consciousness * 0.6, 0.0, 1.0))
    scores['expanding'] = float(np.clip(consciousness * 0.75, 0.0, 1.0))
    scores['illuminated'] = float(np.clip(consciousness * 0.85, 0.0, 1.0))
    scores['transcendent'] = float(np.clip(consciousness * 0.95, 0.0, 1.0))
    scores['master'] = float(np.clip(consciousness * 1.05, 0.0, 1.0))
    scores['avatar'] = float(np.clip(consciousness * 1.15, 0.0, 1.0))

    # Merkaba phases: map energy_flow from edges+fft
    energy_flow = float(np.clip(0.5 * features['edge_mean'] + 0.5 * (1.0 - abs(fft['low_high_ratio'] - 1.0) / (fft['low_high_ratio'] + 1e-6)), 0.0, 1.0))
    scores['dormant'] = float(np.clip(1.0 - energy_flow * 1.2, 0.0, 1.0))
    scores['awakening_phase'] = float(np.clip(energy_flow * 0.6, 0.0, 1.0))
    scores['activation'] = float(np.clip(energy_flow * 0.85, 0.0, 1.0))
    scores['harmonization'] = float(np.clip(energy_flow * 0.95, 0.0, 1.0))
    scores['unity'] = float(np.clip(energy_flow * 1.05, 0.0, 1.0))

    return scores, consciousness, energy_flow


def _quantum_description(filename: str, width: int, height: int, coherence: float, consciousness: float, sacred_detected: List[str], fractal_dim: float, phi_close: float, merkaba_rps: float) -> str:
    geom_txt = ", ".join(sacred_detected[:3]) if sacred_detected else "sin geometrías sagradas dominantes"
    return (
        f"Manifestación cuántica {width}x{height} de coherencia {coherence:.2f}, "
        f"consciencia {consciousness:.2f}. Geometrías: {geom_txt}. "
        f"Proporción áurea {phi_close:.2f}, dimensión fractal {fractal_dim:.2f}. "
        f"Rotación Merkaba ~{merkaba_rps:.2f} RPS."
    )


def analyze_image_quantum(image_data: bytes, filename: str) -> Dict[str, Any]:
    """Main entry: 26D QBTC quantum analysis using Pillow + NumPy only."""
    t0 = time.time()
    try:
        img = Image.open(io.BytesIO(image_data))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        width, height = img.size

        # Prepare working images
        img_small = _resize_safely(img, 640)
        gray = _to_grayscale(img_small)
        gray_np = np.asarray(gray, dtype=np.float32)

        # Core features
        stats = _image_stats(gray)
        edge_arr = _edge_map(gray)
        fractal_dim = _box_counting_fractal_dimension(edge_arr)
        fft = _fft_features(gray_np)
        sym = _symmetry_metrics(gray_np)
        phi = _golden_ratio_features(img_small.size[0], img_small.size[1], gray_np)
        ui = _ui_pattern_signals(gray)
        flags = _skin_nature_monochrome_flags(img_small)

        sacred = _sacred_geometry_scores(phi, sym, fft, edge_arr, ui)
        coherence = _quantum_coherence(sym, fft, fractal_dim)
        ent = _entanglement_summary(gray_np)

        features = {
            'stats': stats,
            'fft': fft,
            'sym': sym,
            'phi': phi,
            'flags': flags,
            'fractal_dim': fractal_dim,
            'ui': ui,
            'sacred': sacred,
            'edge_mean': float(edge_arr.mean())
        }

        dim_scores, consciousness, energy_flow = _dimension_scores(features)
        sacred_detected = [k for k, v in sacred.items() if v >= 0.6]

        # Merkaba rotation speed heuristic (3.33 to 108 RPS)
        merkaba_rps = 3.33 + energy_flow * (108.0 - 3.33)

        analysis_text = _quantum_description(
            filename, width, height, coherence, consciousness, sacred_detected, fractal_dim, phi['phi_closeness'], merkaba_rps
        )

        result = QuantumImageResult(
            analysis=analysis_text,
            confidence=float(np.clip(0.80 + 0.15 * coherence, 0.0, 0.98)),
            processing_type='quantum_image_analysis_26D',
            metadata={
                'filename': filename,
                'width': width,
                'height': height,
                'format': getattr(img, 'format', 'UNKNOWN'),
                'quantum': {
                    'quantum_coherence': coherence,
                    'consciousness_level': consciousness,
                    'dimension_scores': dim_scores,
                    'sacred_geometry_detected': sacred_detected,
                    'phi': phi,
                    'fractal_dimension': fractal_dim,
                    'merkaba': {
                        'rotation_speed_rps': merkaba_rps,
                        'energy_flow': energy_flow
                    },
                    'ui_signals': ui,
                    'symmetry': sym,
                    'fft': fft,
                    'entanglement': ent
                },
                'stats': stats,
                'processing_time_ms': int((time.time() - t0) * 1000)
            }
        )

        return {
            'analysis': result.analysis,
            'confidence': result.confidence,
            'processing_type': result.processing_type,
            'metadata': result.metadata
        }

    except Exception as e:
        logger.error(f"Quantum image analysis failed: {e}")
        return {
            'analysis': f"Error en análisis cuántico: {str(e)}",
            'confidence': 0.0,
            'processing_type': 'error',
            'metadata': {'error': str(e)}
        }

