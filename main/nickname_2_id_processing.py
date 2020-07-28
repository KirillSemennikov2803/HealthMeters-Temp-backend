import configparser

from general_module.models import Employee

config = configparser.ConfigParser()
config.read("config.ini")

bot_url = config["Hosts"]["tg_bot_url"]

def send_new_employees(employee:Employee)