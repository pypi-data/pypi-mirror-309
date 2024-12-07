# Qianxing OpenAPI SDK for Python

A Python SDK for interacting with Qianxing's simulation platform. This package provides a simple and intuitive way to control and monitor simulations for autonomous driving scenarios.

## Installation

You can install the package directly from PyPI:

```bash
pip install qianxing-openapi
```

## Quick Start

Here's a simple example of how to use the SDK:

```python
from qianxing_openapi import Client, HttpConfig, SimulatorConfig

# Initialize the client
client = Client(
    HttpConfig(
        token="your_token_here",
        endpoint="your_endpoint_here"
    )
)

# Create a simulator instance
simulator = client.init_simulator_from_config(
    SimulatorConfig(
        scenario_id="your_scenario_id",
        scenario_version="your_version"
    )
)

# Run simulation steps
step_res = simulator.step()

# Get vehicle information
vehicle_ids = simulator.get_vehicle_id_list()
vehicle_positions = simulator.get_vehicle_position(vehicle_ids.vehicle_ids)

# Stop the simulation
simulator.stop()
```

## Features

- Easy-to-use client interface
- Comprehensive simulation control
- Vehicle state monitoring and control
- Traffic light and junction management
- Scenario configuration

## Requirements

- Python >= 3.7
- requests >= 2.25.0

## Development

To contribute to this project:

1. Clone the repository
```bash
git clone https://github.com/risenlighten-qianxing/openapi-sdk-python.git
cd openapi-sdk-python
```

2. Install development dependencies
```bash
pip install -r requirements.txt
```

## Publishing to PyPI

To publish a new version to PyPI:

1. Update version in setup.py
2. Install publishing tools:
```bash
pip install twine setuptools wheel
```

3. Build distribution packages:
```bash
python setup.py sdist bdist_wheel
```

4. Upload to PyPI:
```bash
twine upload dist/*
```

## License

This project is licensed under the MIT License.

## Support

For bug reports and feature requests, please use the [GitHub Issues](https://github.com/risenlighten-qianxing/openapi-sdk-python/issues) page.