import math

def jitter_offset(index):
    """亚像素 jitter 序列。"""
    raise NotImplementedError("TODO: jitter_offset")

def history_size(width, height):
    """历史纹理尺寸。"""
    raise NotImplementedError("TODO: history_size")

def reproject_uv(uv, motion):
    """历史重投影。"""
    raise NotImplementedError("TODO: reproject_uv")

def disocclusion(depth_delta, normal_dot, color_delta, limits):
    """三联判遮挡。"""
    raise NotImplementedError("TODO: disocclusion")

def reactive_mask(alpha, is_ui):
    """响应掩码。"""
    raise NotImplementedError("TODO: reactive_mask")

def split_motion(camera, object_motion):
    """拆分相机与物体矢量。"""
    raise NotImplementedError("TODO: split_motion")

def resolution_changed(old, new):
    """分辨率切换。"""
    raise NotImplementedError("TODO: resolution_changed")

def hdr_clamp(value, max_nits):
    """HDR 限幅。"""
    raise NotImplementedError("TODO: hdr_clamp")

def sharpen_limit(value, limit):
    """锐化限幅。"""
    raise NotImplementedError("TODO: sharpen_limit")

def camera_history_key(camera_id, frame):
    """相机历史键。"""
    raise NotImplementedError("TODO: camera_history_key")

def fallback_filter(edge_strength):
    """降级滤波选择。"""
    raise NotImplementedError("TODO: fallback_filter")

def jitter_reset_on_cut(cut):
    """切镜重置。"""
    raise NotImplementedError("TODO: jitter_reset_on_cut")

def pixel_offset(uv, width, height, jitter):
    """jitter 像素偏移。"""
    raise NotImplementedError("TODO: pixel_offset")

def history_weight(sample_count, base):
    """历史权重。"""
    raise NotImplementedError("TODO: history_weight")

def taa_clamp(current, history, limit):
    """历史亮度钳制。"""
    raise NotImplementedError("TODO: taa_clamp")
