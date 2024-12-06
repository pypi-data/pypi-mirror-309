# MTCLabPy

A comprehensive Python package for molecular biology and enzyme calculations.

## Features

- Solubility Analysis
- Molecular Pockets Analysis
- Mutations Analysis
- Affinity Calculations
- Kcat Prediction
- Enzyme Self Calculation
- Molecular Docking
- Developmental Tree Analysis

## Installation

```bash
pip install mtclabpy
```

## Usage

```python
# Example for kcat prediction
from mtclabpy.kcat_prediction import dlkat

# Example for solubility prediction
from mtclabpy.solubility import nessolp

# Predict solubility
result_url = nessolp(
    fasta_file_path="sequence.fasta",
    email="your_email@example.com",
    username="your_username",
    password="your_password"
)

# More examples in documentation
```

## Requirements

- Python >= 3.6
- NumPy
- Pandas
- SciPy
- BioPython
- Requests

## License

MIT License
