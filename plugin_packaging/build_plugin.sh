#!/bin/bash

current=`pwd`
mkdir -p /tmp/identitySHARK/
cp -R ../identityshark /tmp/identitySHARK/
cp ../setup.py /tmp/identitySHARK/
cp ../main.py /tmp/identitySHARK/
cp * /tmp/identitySHARK/
cd /tmp/identitySHARK/

tar -cvf "$current/identitySHARK_plugin.tar" --exclude=*.tar --exclude=build_plugin.sh --exclude=*/tests --exclude=*/__pycache__ --exclude=*.pyc *
