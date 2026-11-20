import pytest
from render import temporal_super_resolution as mod

CASES = [
    ("jitter", 'm.jitter_offset(0) == approx(-0.375)'),
    ("size", 'm.history_size(1920, 1080) == (1920, 1080)'),
    ("reproj", 'm.reproject_uv((0.5, 0.5), (0.1, 0.2)) == approx((0.4, 0.3))'),
    ("disocc", 'm.disocclusion(0.1, 0.9, 0.02, (0.2, 0.8, 0.05)) is True'),
    ("reactive", 'm.reactive_mask(0.5, True) == approx(0.0)'),
    ("split", 'm.split_motion((1, 2), (3, 4)) == (4, 6)'),
    ("resolve", 'm.resolution_changed((1920, 1080), (3840, 2160)) is True'),
    ("hdr", 'm.hdr_clamp(1200, 1000) == approx(1000.0)'),
    ("sharpen", 'm.sharpen_limit(1.5, 1.0) == approx(1.0)'),
    ("key", 'm.camera_history_key("main", 7) == "main:7"'),
    ("fallback", 'm.fallback_filter(0.1) == "bilinear"'),
    ("reset", 'm.jitter_reset_on_cut(True) is True'),
    ("offset", 'm.pixel_offset((0.5, 0.5), 1920, 1080, (0.25, -0.25)) == approx((0.5 + 0.25 / 1920, 0.5 - 0.25 / 1080))'),
    ("hweight", 'm.history_weight(2, 0.5) == approx(0.25)'),
    ("clamp", 'm.taa_clamp(10, 20, 5) == approx(15.0)')
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx})
