#!/bin/sh
PLUGIN_PATH=$1

COMMAND="python3.5 $1/main.py --db-database $4 --db-hostname $5 --db-port $6"

if [ ! -z ${2} ] && [ ${2} != "None" ]; then
	COMMAND="$COMMAND --db-user ${2}"
fi

if [ ! -z ${3} ] && [ ${3} != "None" ]; then
	COMMAND="$COMMAND --db-password ${3}"
fi

if [ ! -z ${7} ] && [ ${7} != "None" ]; then
	COMMAND="$COMMAND --db-authentication ${7}"
fi

if [ ! -z ${8} ] && [ ${8} != "None" ]; then
    COMMAND="$COMMAND --debug ${8}"
fi

if [ ! -z ${9} ] && [ ${9} != "None" ]; then
    COMMAND="$COMMAND --ssl"
fi

if [ ! -z ${10} ] && [ ${10} != "None" ]; then
    COMMAND="$COMMAND --cores ${10}"
fi

$COMMAND
