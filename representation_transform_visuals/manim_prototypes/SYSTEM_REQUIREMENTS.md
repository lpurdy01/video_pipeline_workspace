# Manim System Requirements

Manim needs Python packages plus native Cairo/Pango build/runtime dependencies.

On this WSL Ubuntu machine, `pip install manim` failed because `pkg-config` and Cairo headers were missing.

Suggested system setup:

```bash
sudo apt-get update
sudo apt-get install -y pkg-config libcairo2-dev libpango1.0-dev
pip3 install --user --break-system-packages manim
```

Optional, only if later scenes use LaTeX-backed `MathTex`:

```bash
sudo apt-get install -y texlive-latex-base texlive-latex-extra texlive-fonts-recommended
```

Current prototype scenes avoid `MathTex` so LaTeX should not be required.

