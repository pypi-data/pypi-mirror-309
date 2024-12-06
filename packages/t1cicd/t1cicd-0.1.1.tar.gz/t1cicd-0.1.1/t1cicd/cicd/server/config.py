class Config:
    """Base config class."""

    DEBUG = False
    TESTING = False
    DATABASE_URI = "postgresql://user@localhost/dbname"
    SECRET_KEY = "your_secret_key"


class DevelopmentConfig(Config):
    """Development configuration."""

    TESTING = False
    DEBUG = False
    DATABASE_URI = "postgresql://dev_user@localhost/dev_dbname"


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    DATABASE_URI = "postgresql://test_user@localhost/test_dbname"
    DEBUG = True
    SECRET_KEY = "test_secret"


class ProductionConfig(Config):
    """Production configuration."""

    DATABASE_URI = "postgresql://prod_user@localhost/prod_dbname"
    SECRET_KEY = "prod_secret"
