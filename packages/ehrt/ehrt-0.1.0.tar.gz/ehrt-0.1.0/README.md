# ehrt

`ehrt` is a set of foundational tools and pipelines for processing EHR data to create research ready datasets. TETHER is a learning library designed to help analysts and healthcare professionals familiarize themselves with EHR processing.

## Installation

Install via pip

## Usage

```python
from ehrt import nlp

# Example text and dictionary
text = "This is an example input to process."
dictionary_path = "sample_dict.txt"

# The dictionary should can be a csv file containg two columns: string,cui

# Traverse the text to find CUIs
result = nlp.text2cui.traverse(text, dictionary_path)

print(result)