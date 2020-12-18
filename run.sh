#!/bin/bash

if [ ! -d "discord_bot_env/" ]; then
    echo "Created environment"
    python3 -m venv discord_bot_env
    source discord_bot_env/bin/activate
    pip install -r requirements.txt
fi

[ ! -f "src/auth.py" ] && echo -e "# Discord Authentication TOKEN\nTOKEN=None" > src/auth.py

source discord_bot_env/bin/activate

python3 src/bot.py