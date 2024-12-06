from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API配置
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Cron API"

    ETCD_HOSTS: str = "192.168.123.7:2379"
    MONGO_URL: str = "mongodb://192.168.123.7:27017"
    MONGO_DB_NAME: str = "cron"

    class Config:
        env_prefix = "CRON_API_"  # 添加环境变量前缀
        case_sensitive = True

    def reload(self):
        new_settings = Settings()
        for field in self.model_fields:
            setattr(self, field, getattr(new_settings, field))


settings = Settings()
