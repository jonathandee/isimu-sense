class Config:
    SECRET_KEY = "isimu-sense-secret-key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://jonathandangeni@localhost/isimu_sense_prod"


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://jonathandangeni@localhost/isimu_sense_dev"
    
    
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://jonathandangeni@localhost/isimu_sense_prod"
    WEATHER_API_KEY = "37540fd148bfac4c6d3f143778ab0715"