#!/bin/sh
PLUGIN_PATH=$1

COMMAND="python3.5 $1/main.py --db-database $4 --db-hostname $5 --db-port $6 --project-name $8 --issueurl $9 --backend ${10}"

if [ ! -z ${11} ] && [ ${11} != "None" ]; then
	COMMAND="$COMMAND --token ${11}"
fi

if [ ! -z ${2} ] && [ ${2} != "None" ]; then
	COMMAND="$COMMAND --db-user ${2}"
fi

if [ ! -z ${3} ] && [ ${3} != "None" ]; then
	COMMAND="$COMMAND --db-password ${3}"
fi

if [ ! -z ${7} ] && [ ${7} != "None" ]; then
	COMMAND="$COMMAND --db-authentication ${7}"
fi

if [ ! -z ${12} ] && [ ${12} != "None" ]; then
    COMMAND="$COMMAND --proxy-host ${12}"
fi

if [ ! -z ${13} ] && [ ${13} != "None" ]; then
	COMMAND="$COMMAND --proxy-port ${13}"
fi

if [ ! -z ${14} ] && [ ${14} != "None" ]; then
    COMMAND="$COMMAND --proxy-user ${14}"
fi

if [ ! -z ${15} ] && [ ${15} != "None" ]; then
	COMMAND="$COMMAND --proxy-password ${15}"
fi

if [ ! -z ${16} ] && [ ${16} != "None" ]; then
    COMMAND="$COMMAND --debug ${16}"
fi

if [ ! -z ${17} ] && [ ${17} != "None" ]; then
    COMMAND="$COMMAND --issue-user ${17}"
fi

if [ ! -z ${18} ] && [ ${18} != "None" ]; then
    COMMAND="$COMMAND --issue-password ${18}"
fi

if [ ! -z ${19} ] && [ ${19} != "None" ]; then
    COMMAND="$COMMAND --ssl"
fi

$COMMAND
