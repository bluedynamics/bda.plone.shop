#!/bin/sh
rm -r ./lib ./include ./local ./bin
ln -fs plone-5.2.x.cfg buildout.cfg
pyenv virtualenv 3.8.1 bda.plone.shop
pyenv local bda.plone.shop
pip install -r http://dist.plone.org/release/5.2-latest/requirements.txt
buildout
