#!/bin/bash

TYPE="$1"

PYTHON="/usr/bin/python3"
DIR_MAIN="/var/bertain-cdn/airpuff"
DIR_BIN="${DIR_MAIN}/bin"
DIR_DATA="${DIR_MAIN}/data"
SCRIPT="get-avwx-data.py"
AVWX_TYPE=`echo ${1} | tr '[:upper:]' '[:lower:]'`

AVWX_DIR="${AVWX_TYPE}s"
OUTPUT_DIR="${DIR_DATA}/${AVWX_DIR}"

${PYTHON} ${DIR_BIN}/${SCRIPT} --${AVWX_TYPE} --output_dir ${OUTPUT_DIR}
