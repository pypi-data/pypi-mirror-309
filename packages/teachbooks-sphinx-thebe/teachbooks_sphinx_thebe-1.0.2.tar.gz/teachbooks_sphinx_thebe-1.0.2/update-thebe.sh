#!/bin/bash

set -euo pipefail

CURRENT_DIR=$(pwd)
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

cleanup() {
    cd $CURRENT_DIR
}

trap cleanup EXIT

cd $SCRIPT_DIR
cd libs/thebe/

if ! command -v npm &>/dev/null; then
    echo "npm is not installed"
    exit 1
fi

npm ci
npm run build:thebe

rm -rf $SCRIPT_DIR/src/teachbooks_sphinx_thebe/_thebe_static/*
cp -r packages/thebe/lib/* $SCRIPT_DIR/src/teachbooks_sphinx_thebe/_thebe_static/
cp -r packages/lite/dist/lib/* $SCRIPT_DIR/src/teachbooks_sphinx_thebe/_thebe_static/
