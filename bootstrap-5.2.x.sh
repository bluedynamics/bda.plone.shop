#!/bin/bash
set -e

REQUIREMENTS="http://dist.plone.org/release/5.2-latest/requirements.txt"

for dir in lib include local bin share pyvenv.cfg lib64; do
    if [ -d "$dir" ]; then
        echo "Removing $dir..."
        rm -r "$dir"
    fi
done

ln -fs plone-5.2.x.cfg buildout.cfg

if [ "$1" == "venv" ]; then
    python3 -m venv .
    ./bin/pip install -r $REQUIREMENTS
    ./bin/buildout
else
    pyenv virtualenv 3.8.6 bda.plone.shop
    pyenv local bda.plone.shop
    pip install -r $REQUIREMENTS
    buildout
fi
