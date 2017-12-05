#!/bin/sh
PLUGIN_PATH=$1
cd $PLUGIN_PATH

# if there are problems due to c libraries
# apt-get install python3-numpy
# apt-get install python3-scipy
# apt-get install python3-pandas
# then old version pip3 install numpy --user

# Install issueSHARK
python3.5 $PLUGIN_PATH/setup.py install --user