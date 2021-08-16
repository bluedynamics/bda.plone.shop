#!/bin/bash
set -e

REQUIREMENTS="https://raw.githubusercontent.com/plone/buildout.coredev/6.0/requirements.txt"

for dir in lib include local bin share pyvenv.cfg lib64; do
    if [ -d "$dir" ]; then
        echo "Removing $dir..."
        rm -r "$dir"
    fi
done

if [ "$1" == "venv" ]; then
    ln -fs plone-6.x.cfg buildout.cfg
    python3 -m venv .
    ./bin/pip install -r $REQUIREMENTS
    ./bin/buildout
else
    pyenv virtualenv 3.9.6 bda.plone6.shop
    pyenv local bda.plone6.shop
    pip install -r $REQUIREMENTS
    buildout
fi
