from celery import Celery
from decouple import config as env_config

# Variáveis de ambiente
env_config.encoding = "utf-8"
BROKER_URL = env_config("CELERY_BROKER_URL")
RESULT_BACKEND = env_config("CELERY_RESULT_BACKEND")

# Iniciando o Celery
app = Celery(
    __name__,
    broker=BROKER_URL,
    backend=str(RESULT_BACKEND),
)

# Configurações do Celery
app.conf.broker_connection_retry_on_startup = True
app.conf.accept_content = ["json"]
