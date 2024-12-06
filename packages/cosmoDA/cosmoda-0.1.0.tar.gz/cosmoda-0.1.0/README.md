# cosmoDA - Compositional Score Matching Optimization for Differential Abundance Testing

![cosmoDA](misc/concept_figure.png)
 
This repository contains the cosmoDA model (Ostner et al., 2024), as well as a Python interface 
to the score matching estimator for power interaction models in the genscore R package (Yu et al., 2024). 
It also contains all code needed to reproduce the analyses in the publication (TODO).

For usage info, please refer to the tutorial.

Raw and intermediate data objects can be downloaded on [zenodo](TODO). 
Simply download the `data` directory from there and unpack it in the cosmoDA directory.

## Installation

TODO

## Usage

TODO

## Repository structure

This repository is structured as follows:

- The `cosmoDA` directory contains the python code to run the cosmoDA or genscore models.
- The `src` directory contains the C code from genscore, as well as its extension from the cosmoDA model.
- The `simulation` and `applications` directories contain the simulated and real data applications from the paper, respectively.
- The `misc` directory contains code for supplementary and concept figures.
- The `figures` directory contains all generated figures.


