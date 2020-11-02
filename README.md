# Discord Bot

Discord bot made with discord.py API wrapper

## Installing

To instanciate this bot is recomended to install his dependencies isolated in a virtual environment

### **Create virtual environment**

```shell
python3 -m venv discord_bot_env

source discord_bot_env/bin/activate

pip install -r requirements.txt
```

### **Set authentication token**

The discord bot instance will run as an application user over the given `TOKEN`

This token will be read from the file `src/auth.py`

```python
# src/auth.py
TOKEN='token_string'
```

### **Running** 

```shell
python3 src/bot.py
# or
./run.sh
```