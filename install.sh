#!/bin/bash

# https://chat.openai.com/c/143bf330-901c-46ea-9115-03b450fdd07d
# Also install Python3 if needed

unzip -o MosamaticDesktop.zip

VENV_DIR="$HOME/.mosamatic/MosamaticDesktop"
mkdir -p $HOME/.mosamatic

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv $VENV_DIR
fi

source $VENV_DIR/bin/activate

pip install -r requirements.txt

deactivate