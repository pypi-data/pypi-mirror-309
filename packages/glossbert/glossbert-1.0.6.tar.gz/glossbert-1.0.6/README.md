# GlossBERT Wrapper Class

![PyPI Version](https://img.shields.io/pypi/v/glossbert)
![Python Versions](https://img.shields.io/pypi/pyversions/glossbert)
![License](https://img.shields.io/pypi/l/glossbert)
[![Publish Python 🐍 distribution 📦 to PyPI](https://github.com/cruzlorite/glossbert/actions/workflows/publish-pypi.yaml/badge.svg)](https://github.com/cruzlorite/glossbert/actions/workflows/publish-pypi.yaml)

This Python package provides a convenient wrapper for using [GlossBERT](https://github.com/HSLCY/GlossBERT/tree/master), allowing you to easily perform word sense disambiguation (WSD) by searching WordNet through NLTK.

The source code in this repository is adapted from [this script](https://github.com/HSLCY/GlossBERT/blob/master/run_infer_demo_sent_cls_ws_with_nltk.py) from the original GlossBERT project.

## Features

- Simplifies the use of GlossBERT for WSD tasks.
- Provides integration with WordNet via NLTK.

## Installation

Install the package using pip:

```bash 
pip install glossbert
```

Alternatively, install directly from the GitHub repository:

```bash
pip install git+https://github.com/cruzlorite/glossbert.git
```

## Usage

Here is an example of how to use the GlossBERT class:

```python
>>> from glossbert import GlossBERT
>>> 
>>> # initialize the GlossBERT instance
>>> gloss = GlossBERT()
>>> 
>>> # define a sentence and specify the target word
>>> sent = "I love dogs!"
>>> start_idx, end_idx, target_word = 7, 11, "dog"
>>> 
>>> # perform word sense disambiguation
>>> gloss(sent, start_idx, end_idx, target_word)
[
    (0.9973864, Synset('dog.n.01')),
    (0.025929835, Synset('frank.n.02')),
    (0.0030947044, Synset('dog.n.03')),
    (0.0024504508, Synset('cad.n.01')),
    (0.001387376, Synset('andiron.n.01')),
    (0.00057538506, Synset('pawl.n.01')),
    (0.0005529578, Synset('chase.v.01')),
    (0.00046094437, Synset('frump.n.01'))
]
```

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit), consistent with the original [GlossBERT project](https://github.com/HSLCY/GlossBERT/tree/master).

## Acknowledgements

Special thanks to the authors of the original [GlossBERT](https://github.com/HSLCY/GlossBERT/tree/master) for their foundational work.