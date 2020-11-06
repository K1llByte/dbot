from datetime import datetime
import sys

class Logger:
    is_stdout = True

    def __init__(self,logs_filename=""):
        if logs_filename != "":
            self.is_stdout = False
            sys.stdout = open(logs_filename, 'w')
    
    def __del__(self):
        if not self.is_stdout:
            sys.stdout.close()

    def __date_log_format():
        return datetime.now().strftime("%H:%M")


    def info(self, message):
        print("({date}) [INFO] > {message}".format(date=Logger.__date_log_format(), message=message))


    def command(self, username, command):
        print("({date}) [COMMAND] {user} > {cmd}".format(date=Logger.__date_log_format(), user=username, cmd=command))


    def error(self, message):
        print("({date}) [ERROR] > {message}".format(date=Logger.__date_log_format(), message=message))

logger = Logger("file.logs")
logger.info("You are gay :)")
logger.error("YOU CANNO'T NOT BE GAY!!!!!1!!1!")