#!/bin/bash
cd "$(dirname "$0")"
echo "Running run_script..."
wine "run_script" || ./"run_script" "$@"
