import os


class Config:
    db_user = os.getenv("DB_USER", "default_user")
    db_pass = os.getenv("DB_PASSWORD", "default_pass")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "default_db")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///test_database.db"
    TESTING = True
