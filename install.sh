#!/bin/bash

unzip -o MosamaticDesktop.zip

VENV_DIR="$HOME/.mosamatic/MosamaticDesktop"
mkdir -p $HOME/.mosamatic

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv $VENV_DIR
fi

source $VENV_DIR/bin/activate

pip install -r requirements.txt

deactivate