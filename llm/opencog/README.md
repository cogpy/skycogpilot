# OpenCog AGI Framework on SkyPilot

<p align="center">
    <img src="https://opencog.org/images/opencog-logo.png" alt="OpenCog Logo" width="200"/>
</p>

This directory contains configurations to run OpenCog, an open-source Artificial General Intelligence (AGI) framework, on any cloud infrastructure using SkyPilot.

OpenCog is designed for developing human-level or superhuman cognitive abilities through multiple interacting AI components using a graph database called AtomSpace for knowledge representation and reasoning.

* [OpenCog Website](https://opencog.org/)
* [OpenCog GitHub](https://github.com/opencog/opencog)
* [OpenCog Hyperon](https://hyperon.opencog.org/)
* [Documentation](https://wiki.opencog.org/)

## Prerequisites

Install SkyPilot and check your cloud setup:
```bash
pip install skypilot
sky check
```

## Quick Start

### Basic OpenCog Setup

Launch a basic OpenCog environment with AtomSpace:
```bash
sky launch -c opencog-basic basic.yaml
```

### OpenCog Development Environment

Launch a full development environment with all OpenCog components:
```bash
sky launch -c opencog-dev dev.yaml
```

### OpenCog with Jupyter Notebook

Launch OpenCog with Jupyter for interactive development:
```bash
sky launch -c opencog-jupyter jupyter.yaml
```

## Available Configurations

| Configuration | Description | Resources |
|--------------|-------------|-----------|
| `basic.yaml` | Basic OpenCog installation with core components | 1x CPU, 4 cores, 8GB RAM |
| `dev.yaml` | Full development environment with all modules | 1x CPU, 8 cores, 16GB RAM |
| `jupyter.yaml` | OpenCog with Jupyter notebook interface | 1x CPU, 4 cores, 8GB RAM |
| `gpu.yaml` | OpenCog with GPU acceleration for ML components | 1x GPU, 8 cores, 16GB RAM |

## Custom Data and Experiments

To run your own OpenCog experiments:

1. Replace the example files in the workdir with your own OpenCog schemes/programs
2. Modify the `run` section in the YAML to execute your specific OpenCog tasks
3. Add any additional dependencies in the `setup` section

## Cost Optimization

Use spot instances to reduce costs:
```bash
sky launch -c opencog-basic basic.yaml --use-spot
```

## Multi-Node OpenCog (Experimental)

For distributed OpenCog reasoning:
```bash
sky launch -c opencog-cluster cluster.yaml
```

## Examples

The configurations include example OpenCog programs:
- Basic AtomSpace operations
- Reasoning with Pattern Matcher
- Cognitive architectures
- Simple AGI experiments

## Support

For OpenCog-specific questions, visit the [OpenCog community](https://github.com/opencog/opencog/discussions).
For SkyPilot deployment issues, see [SkyPilot documentation](https://docs.skypilot.co/).