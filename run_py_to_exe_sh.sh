#!/bin/bash
cd "$(dirname "$0")"
echo "Running run_py_to_exe_sh..."
wine "run_py_to_exe_sh" || ./"run_py_to_exe_sh" "$@"
