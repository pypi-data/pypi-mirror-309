<div align="center">

<img src="docs/assets/swe-rex-logo.png" alt="SWE-ReX" style="height: 12em"/>

# SWE-agent Remote Execution Framework

[![Pytest](https://github.com/SWE-agent/swe-rex/actions/workflows/pytest.yaml/badge.svg)](https://github.com/SWE-agent/swe-rex/actions/workflows/pytest.yaml)
[![Check Markdown links](https://github.com/SWE-agent/swe-rex/actions/workflows/check-links.yaml/badge.svg)](https://github.com/SWE-agent/swe-rex/actions/workflows/check-links.yaml)
[![build-docs](https://github.com/SWE-agent/swe-rex/actions/workflows/build-docs.yaml/badge.svg)](https://github.com/SWE-agent/swe-rex/actions/workflows/build-docs.yaml)
</div>

## Install

```bash
pip install -e .
# With modal support
pip install -e '.[modal]'
# With fargate support
pip install -e '.[fargate]'
# Development setup (all optional dependencies)
pip install -e '.[dev]'
```
