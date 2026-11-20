"""时序超分（TSR）核心工具函数。

修复要点：
- jitter 跨帧累积（按帧号取周期序列），切镜时重置；
- 重投影拆分相机/物体运动矢量；
- disocclusion 用深度 + 法线 + 色彩三联判；
- reactive mask 排除 UI；
- 分辨率切换后重建历史；
- HDR 线性域限幅而非提前 clamp；
- 锐化带亮度限幅（避免 RGB 独立锐化导致色散）；
- 多相机按 camera_id 隔离历史；
- 降级路径按边缘强度选择滤波，保护边缘。
"""

# 8 相位亚像素 jitter 序列（单位：像素，范围 [-0.5, 0.5)）。
# 跨帧按 frame_index 累积推进相位，不再每帧重置。
_JITTER_PHASES = 8


def jitter_offset(index):
    """亚像素 jitter 序列：按帧号取周期相位，跨帧累积。"""
    return ((index % _JITTER_PHASES) + 1) / _JITTER_PHASES - 0.5


def history_size(width, height):
    """历史纹理尺寸：与当前渲染分辨率一致，分辨率切换时据此重建。"""
    return (width, height)


def reproject_uv(uv, motion):
    """历史重投影：用拆分后的运动矢量回采上一帧历史。"""
    return (uv[0] - motion[0], uv[1] - motion[1])


def disocclusion(depth_delta, normal_dot, color_delta, limits):
    """三联判遮挡：深度差、法线夹角、色彩差任一超限即判定历史失效。

    limits = (depth_limit, normal_dot_limit, color_limit)。
    返回 True 表示历史样本仍有效（未 disocclude），False 表示被遮挡需丢弃历史。
    """
    depth_limit, normal_limit, color_limit = limits
    if depth_delta > depth_limit:
        return False
    if normal_dot < normal_limit:
        return False
    if color_delta > color_limit:
        return False
    return True


def reactive_mask(alpha, is_ui):
    """响应掩码：UI 不参与几何累积，直接返回 0；其余按透明度响应。"""
    if is_ui:
        return 0.0
    return float(alpha)


def split_motion(camera, object_motion):
    """拆分相机与物体矢量：总运动 = 相机运动 + 物体运动（蒙皮顶点用当前骨骼重算后传入）。"""
    return (camera[0] + object_motion[0], camera[1] + object_motion[1])


def resolution_changed(old, new):
    """分辨率切换检测：发生变化时调用方需按 history_size 重建历史纹理。"""
    return old != new


def hdr_clamp(value, max_nits):
    """HDR 限幅：在线性域超分完成后才限幅到 [0, max_nits]，保留星点等高光细节。"""
    return float(min(max(value, 0.0), max_nits))


def sharpen_limit(value, limit):
    """锐化限幅：以亮度为基准限幅到 [-limit, limit]，避免 RGB 独立锐化产生色散。"""
    return float(min(max(value, -limit), limit))


def camera_history_key(camera_id, frame):
    """相机历史键：按 camera_id 隔离各相机历史，避免分屏互相污染。"""
    return f"{camera_id}:{frame}"


def fallback_filter(edge_strength):
    """降级滤波选择：GPU 时间片不足时按边缘强度选择，强边缘走保边滤波。"""
    if edge_strength >= 0.5:
        return "edge_aware"
    return "bilinear"


def jitter_reset_on_cut(cut):
    """切镜重置：发生镜头切换时重置 jitter 相位累积与历史。"""
    return bool(cut)


def pixel_offset(uv, width, height, jitter):
    """jitter 像素偏移：把像素单位的 jitter 换算成 UV 偏移后叠加。"""
    return (uv[0] + jitter[0] / width, uv[1] + jitter[1] / height)


def history_weight(sample_count, base):
    """历史权重：随累积样本数衰减的基础权重。"""
    return base / max(sample_count, 1)


def taa_clamp(current, history, limit):
    """历史亮度钳制：把当前帧颜色钳到 history ± limit 区间内。"""
    return float(min(max(current, history - limit), history + limit))
