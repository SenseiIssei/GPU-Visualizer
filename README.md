# GPU Visualizer

Modern GPU visualization app with real-time simulation and 2D/3D views (PySide6 + PyOpenGL).

Author: Jakob / Sensei Issei

## Features
- 2D layout view (GPC → SM → Core) with real-time coloring
- 3D GPU models with component highlighting and smart caching
- Controls panel for presets, colormaps, simulation speed/utilization/power
- JSON import/export for layouts
- Log window and component visibility panel

## Getting Started

### Requirements
- Python 3.10+
- Windows/macOS/Linux

Install dependencies:

```bash
pip install -r requirements.txt
```

### Run

```bash
python main.py
```

## Project Structure

```
.
├─ main.py                        # App entry (modern UI)
├─ gpuviz/
│  ├─ view2d.py                   # 2D layout view
│  ├─ view3d.py                   # 3D OpenGL view
│  ├─ sim.py                      # DVFS + activity simulation
│  ├─ controls.py                 # Controls panel
│  ├─ layouts.py                  # Presets + JSON IO
│  ├─ models.py                   # Data classes (Core/SM/GPC/GPULayout)
│  ├─ resources.py                # Colormaps
│  ├─ logWindow.py                # Log window
│  ├─ componentHighlighter.py     # Component info + highlight API
│  ├─ componentVisibilityPanel.py # Show/Hide + perf panel
│  └─ gpu_models/
│     ├─ __init__.py              # Model registry/factory
│     ├─ baseGpuModel.py          # Base model API
│     ├─ rtx4080Model.py          # RTX 4080 model
│     ├─ rtx4090Model.py          # RTX 4090 model
│     └─ rx7900XtxModel.py        # RX 7900 XTX model
└─ requirements.txt
```

## Notes
- Start the application via `main.py`.
- `gpuVisualizer.py` is legacy and not used by the modern app.

## Contributing
- Format: single file-level header per file, no inline comments
- Keep runtime strings (CSS/HTML) intact

## License
This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.