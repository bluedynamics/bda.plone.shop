#!/bin/sh

# see https://community.plone.org/t/not-using-bootstrap-py-as-default/620
rm -r ./lib ./include ./local ./bin
ln -fs plone-5.0.x.cfg buildout.cfg
virtualenv --clear .
./bin/pip install -r https://raw.githubusercontent.com/plone/buildout.coredev/5.0/requirements.txt./bin/buildout
