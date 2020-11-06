#!/bin/sh
rm -r ./lib ./include ./local ./bin
ln -fs plone-6.x.cfg buildout.cfg
pyenv virtualenv 3.8.6 bda.plone.shop
pyenv local bda.plone.shop
pip install -r https://raw.githubusercontent.com/plone/buildout.coredev/6.0/requirements.txt
buildout
