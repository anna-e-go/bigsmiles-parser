#!/bin/bash


ABSOLUTE_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}")"

BIN_PATH=${ABSOLUTE_PATH/activate_venv.sh/}

ENV_PATH="${BIN_PATH}env/bin/activate"

echo $ENV_PATH

source $ENV_PATH


