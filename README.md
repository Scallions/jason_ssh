
# 环境准备

pygmt 安装
https://www.pygmt.org/dev/install.html

```bash
conda create --name pygmt --channel conda-forge pygmt
```

```bash
uv python pin path/to/conda/pygmt/bin/python
```

```bash
uv sync
```

```bash
python src/jason_ssh/ui.py
```