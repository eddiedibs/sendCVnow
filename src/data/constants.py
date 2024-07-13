from dotenv import load_dotenv
load_dotenv()

import os
from pathlib import Path

DATABASE_URL=os.getenv("DATABASE_URL")
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
OLLAMA_HOST = os.getenv('OLLAMA_HOST')
OLLAMA_PORT = os.getenv('OLLAMA_PORT')
OLLAMA_INIT_INSTRUCT = os.getenv('OLLAMA_INIT_INSTRUCT')
BASE_DIR = Path(__file__).resolve().parent.parent


# conf = ConnectionConfig(
#     MAIL_USERNAME = "Your SMTP username",
#     MAIL_PASSWORD = "Your SMTP password",
#     MAIL_FROM = "Your email",
#     MAIL_PORT = 587,
#     MAIL_SERVER = "your SMTP server",
#     MAIL_TLS = True,
#     MAIL_SSL = False,
#     USE_CREDENTIALS = True
# )

