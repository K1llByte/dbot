from datetime import datetime

def __date_log_format():
    return datetime.now().strftime("%H:%M")


def info_log(message):
    date = __date_log_format()
    colored = '\033[1m\033[38;5;7mINFO\033[0m'
    return f"({date}) [{colored}] > {message}"


def command_log(username, command):
    date = __date_log_format()
    colored = "\033[1m\033[38;5;36mCOMMAND\033[0m"
    return f"({date}) [{colored}] {username} > {command}"


def error_log(message):
    date = __date_log_format()
    colored = "\033[1m\033[0;31mERROR\033[0m"
    return f"({date}) [{colored}] > {message}"