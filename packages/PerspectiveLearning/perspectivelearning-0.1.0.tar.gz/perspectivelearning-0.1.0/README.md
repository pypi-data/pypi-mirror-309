# PerspectiveLearning

**PerspectiveLearning** is a Python library for hypothesis-driven iterative machine learning.

## Features
- Define multiple perspectives for hypothesis evaluation.
- Iteratively train and refine the best perspective.
- Predict outcomes using the refined model.

## Installation
Install via pip:
```
pip install PerspectiveLearning
```


## Usage
```python
from PerspectiveLearning import PerspectiveLearning

# Example usage with dataset
pl = PerspectiveLearning(dataset, features, target, perspectives)
pl.train()
predictions = pl.predict(new_data)
```