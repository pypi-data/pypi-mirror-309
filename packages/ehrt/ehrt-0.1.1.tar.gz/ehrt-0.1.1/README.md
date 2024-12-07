# ehrt

`ehrt` is a set of foundational tools and pipelines for processing EHR data to create research ready datasets. TETHER is a learning library designed to help analysts and healthcare professionals familiarize themselves with EHR processing.

## Installation

```bash

pip install ehrt
```

## Usage

```python
from ehrt import Text2Cui

# Initialize the Text2Cui processor and load dictionary
processor = Text2Cui("sample_dict.csv")

# Process a text
result = processor.traverse("example1 input")

print(result)  # Output: "CUI12345,CUI54321"
```