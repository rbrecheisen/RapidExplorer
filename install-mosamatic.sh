#!/bin/bash

# https://chat.openai.com/c/143bf330-901c-46ea-9115-03b450fdd07d
# Also install Python3 if needed

echo "Setting up virtual environment in $HOME/.mosamatic..."
VENV_DIR="$HOME/.mosamatic/MosamaticDesktop"
mkdir -p $HOME/.mosamatic
if [ -d "$VENV_DIR" ]; then
    rm -rf $HOME/.mosamatic    
fi
python3 -m venv $VENV_DIR

echo "Activating virtual environment and installing package requirements..."
source $VENV_DIR/bin/activate
$HOME/.mosamatic/MosamaticDesktop/bin/pip install --upgrade pip
$HOME/.mosamatic/MosamaticDesktop/bin/pip install mosamaticdesktop
deactivate

echo "Installing mosamatic.sh in /usr/local/bin..."
cp $HOME/.mosamatic/MosamaticDesktop/lib/python3.11/site-packages/mosamaticdesktop/scripts/mosamatic.sh /usr/local/bin

echo "Installation finished"
ehco "You can now run Mosamatic by typing 'mosamatic.sh' and pressing enter."