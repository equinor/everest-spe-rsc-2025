#!/bin/bash

python -m venv everest
source everest/bin/activate

pip install pip -U
pip install 'ert[everest]==14'
pip install everviz
pip install everest-models@git+https://github.com/equinor/everest-models
