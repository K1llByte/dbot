#!/bin/bash
[ ! -f "src/auth.py" ] && echo -e "# Discord Authentication TOKEN\nTOKEN=None" > src/auth.py
source discord_bot_env/bin/activate
python3 src/bot.py