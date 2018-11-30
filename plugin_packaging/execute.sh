#!/bin/sh
PLUGIN_PATH=$1

COMMAND="python3.5 $1/main.py --project_name ${2} --db-database $5 --db-hostname $6 --db-port $7"

if [ ! -z ${3} ] && [ ${3} != "None" ]; then
	COMMAND="$COMMAND --db-user ${3}"
fi

if [ ! -z ${4} ] && [ ${4} != "None" ]; then
	COMMAND="$COMMAND --db-password ${4}"
fi

if [ ! -z ${8} ] && [ ${8} != "None" ]; then
	COMMAND="$COMMAND --db-authentication ${8}"
fi

if [ ! -z ${9} ] && [ ${9} != "None" ]; then
    COMMAND="$COMMAND --debug ${9}"
fi

if [ ! -z ${10} ] && [ ${10} != "None" ]; then
    COMMAND="$COMMAND --ssl"
fi

if [ ! -z ${11} ] && [ ${11} != "None" ]; then
    COMMAND="$COMMAND --cores ${11}"
fi

if [ ! -z ${12} ] && [ ${12} != "None" ]; then
    COMMAND="$COMMAND --start-index ${12}"
fi

if [ ! -z ${13} ] && [ ${13} != "None" ]; then
    COMMAND="$COMMAND --end-index ${13}"
fi

$COMMAND
