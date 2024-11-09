#!/bin/sh
MODE=${MODE:-'cli'}
if [ "$MODE" == "cli" ]
then
    . /tmp/pyenv/bin/activate
    python3 /opt/cli/main.py "$@"
else
    chmod +x /opt/apps/run.sh && /opt/apps/run.sh "$@"
fi
