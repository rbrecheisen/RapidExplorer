#!/bin/bash

# https://chat.openai.com/c/143bf330-901c-46ea-9115-03b450fdd07d
# Also install Python3 if needed

VENV_DIR="$HOME/.mosamatic/MosamaticDesktop"

# echo "Setting up virtual environment in $HOME/.mosamatic..."
# mkdir -p $HOME/.mosamatic
# if [ -d "$VENV_DIR" ]; then
#     rm -rf $HOME/.mosamatic    
# fi
# python3 -m venv $VENV_DIR

echo "Activating virtual environment and installing package requirements..."
source $VENV_DIR/bin/activate
$HOME/.mosamatic/MosamaticDesktop/bin/pip install --upgrade pip
$HOME/.mosamatic/MosamaticDesktop/bin/pip install mosamaticdesktop
deactivate

# echo "Installing mosamatic.sh in /usr/local/bin..."
# cp $HOME/.mosamatic/MosamaticDesktop/lib/python3.11/site-packages/mosamaticdesktop/scripts/mosamatic /usr/local/bin

# echo "Creating desktop icon..."
# if [ -f "$HOME/Desktop/MosamaticDesktop" ]; then
#     rm $HOME/Desktop/MosamaticDesktop
# fi
# ln -s /usr/local/bin/mosamatic 

# echo "Installation finished"
# echo "You can now run Mosamatic by typing 'mosamatic' and pressing enter or by double-clicking the icon on your desktop"