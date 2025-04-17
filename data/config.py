from dotenv import load_dotenv
from os import environ

load_dotenv()

BOT_TOKEN = environ.get("BOT_TOKEN")  # Bot toekn
ADMINS = environ.get("ADMIN")  # adminlar ro'yxati
ADMIN_M1 = environ.get("ADMIN1")
ADMIN_M2 = environ.get("ADMIN2")
IP = environ.get("IP")  # Xosting ip manzili
