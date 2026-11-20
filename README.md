# pairwise-tsr-history

时序超分在相机穿过栅栏时出现整片拖影，jitter 序列每帧重置导致亚像素偏移没累积，历史重投影只用了当前运动矢量，没区分相机与物体运动；disocclusion 掩码用深度差单阈值，薄栏杆后的背景被误判为可见；reactive mask 把半透明 UI 也算进几何，超分后文字边缘发虚；运动矢量在蒙皮顶点上按上一帧骨骼算，快速挥砍时边缘撕裂；分辨率从 1440p 切到 4K 后历史纹理没重建，采样坐标越界回绕；HDR 亮度在超分前被 clamp，夜空星点被抹掉；锐化在 RGB 三通道独立做，彩色边缘出现色散；多相机分屏共享历史，瞄准镜画面污染主视图；GPU 时间片不足时降级到双线性，没做边缘保护。render/temporal_super_resolution.py 是核心，tests/test_temporal_super_resolution.py 15个红。要修的是：jitter 跨帧累积并在切镜重置；重投影拆分相机/物体矢量；disocclusion 用深度+法线+色彩三联判；reactive mask 排除 UI；蒙皮矢量用当前骨骼重算；分辨率切换重建历史；HDR 线性域超分；锐化带亮度限幅；多相机隔离历史；降级路径保边缘。

## 运行

```bash
python -m pytest tests -q
```

初始状态：15 个用例失败。修复实现使全部用例通过，不要修改 `tests/` 下的测试。

子方向：见平台；任务类型：Bugfix；语言/框架：Python 3, pytest；环境可复现等级：无外部依赖。
