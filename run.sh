#!/bin/bash

# Путь до интерпретатора и скрипта
VENV_PATH="/home/blxnk/PycharmProjects/click_key_capture/.venv"

SCRIPT_DIR="/home/blxnk/PycharmProjects/click_key_capture"
PY_SCRIPT_PATH="$SCRIPT_DIR/main.py"
cd "$SCRIPT_DIR" || exit

source $VENV_PATH/bin/activate
python3 "$PY_SCRIPT_PATH" "$@"

deactivate