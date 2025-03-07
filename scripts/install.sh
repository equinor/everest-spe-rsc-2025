#!/bin/bash

python -m venv .venv
pip install pip -U
pip install 'ert[everest]==14'
pip install everviz
pip install everest-models@git+https://github.com/equinor/everest-models
