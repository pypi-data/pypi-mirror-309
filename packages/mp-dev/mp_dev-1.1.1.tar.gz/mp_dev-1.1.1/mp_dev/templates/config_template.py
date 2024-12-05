import secrets


def get_content(project_name):
    return f"""from passlib.context import CryptContext
from datetime import datetime, timedelta


class Settings:
    # Obtenir la date et l'heure actuelles
    now = datetime.now()

    # Obtenir la date et l'heure du début de la journée
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # Calculer la différence entre la fin de la journée et l'heure actuelle
    time_left = start_of_day + timedelta(days=1) - now

    # Convertir le temps restant en minutes
    minutes_left = time_left.total_seconds() // 60

    PROJECT_NAME: str = "{project_name}"
    PROJECT_VERSION: str = "1.0.0"
    DATABASE_URL: str = "postgresql://root:root@db:5432/{project_name}_db"
    SECRET_KEY: str = "{secrets.token_hex(32)}"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = minutes_left
    PWD_CONTEXT = pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


settings = Settings()
"""