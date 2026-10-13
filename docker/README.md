# 🐳 Cyber Toolkit — Docker Guide

**Created by: Rebilraj**

Run the Cyber Toolkit in a safe, isolated container — no Python setup, no dependency hell.

## 🚀 Quick Start

```bash
# Build the image
docker build -t cyber-toolkit .

# Run --help
docker run --rm -it cyber-toolkit

# Open a shell
docker run --rm -it --entrypoint bash cyber-toolkit
