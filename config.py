class Config:
    SECRET_KEY = "isimu-sense-secret-key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/isimu_sense_prod"


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/isimu_sense_dev"