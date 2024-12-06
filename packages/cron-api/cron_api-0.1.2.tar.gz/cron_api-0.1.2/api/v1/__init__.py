from fastapi import APIRouter

from api.v1.etcd import router as etcd_router
from api.v1.mongo import router as mongo_router

# 后续其他路由模块导入到这里
# from api.v1.jobs import router as jobs_router
# from api.v1.workers import router as workers_router

api_router = APIRouter()

api_router.include_router(mongo_router, prefix="/mongo")
api_router.include_router(etcd_router, prefix="/etcd")
# api_router.include_router(jobs_router, prefix="/jobs")
# api_router.include_router(workers_router, prefix="/workers")
