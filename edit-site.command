#!/bin/sh
cd "$(dirname "$0")" || exit 1
python3 editor/server.py &
EDITOR_PID=$!
sleep 1
open "http://127.0.0.1:8765/"
wait "$EDITOR_PID"
