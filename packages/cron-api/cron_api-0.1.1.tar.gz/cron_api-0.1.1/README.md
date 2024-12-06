# Cron API

自用 fastapi 项目,提供对应接口,通过命令行启动

-   etcd 配置定时任务
-   mongodb 查看任务执行日志

#### 安装

`pipx install cron-api` 或 `uv tool install cron-api`

#### 运行

`cron-api --help`

```shell
# CRON_API_ETCD_HOSTS="192.168.123.7:2379"
# CRON_API_MONGO_URL="mongodb://192.168.123.7:27017"
# CRON_API_MONGO_DB_NAME="cron"
# 指定环境变量文件,环境变量文件需提供以上参数
cron-api --dotenv-path .env
# 还可以通过 --host, --port 指定fastapi启动地址和端口
cron-api --host 0.0.0.0 --port 8000
```
