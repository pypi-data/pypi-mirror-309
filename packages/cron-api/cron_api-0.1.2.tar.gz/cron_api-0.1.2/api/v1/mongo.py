from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from models.log import Log
from services.mongodb import MongoDB

router = APIRouter()


class PaginatedLogs(BaseModel):
    """分页响应模型"""

    total: int = Field(..., description="总记录数")
    items: List[Log] = Field(..., description="日志列表")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页大小")
    pages: int = Field(..., description="总页数")


@router.get("/logs", response_model=PaginatedLogs)
async def get_logs(
    page: int = Query(1, description="页码", ge=1),
    page_size: int = Query(1000, description="每页记录数", ge=1, le=10000),
    job_name: Optional[str] = Query(None, description="任务名称"),
    command: Optional[str] = Query(None, description="命令"),
    start_time: Optional[int] = Query(
        None,
        description="开始时间戳(毫秒)",
        example=int((datetime.now() - timedelta(hours=1)).timestamp() * 1000),
    ),
    end_time: Optional[int] = Query(
        None,
        description="结束时间戳(毫秒)",
        example=int(datetime.now().timestamp() * 1000),
    ),
    has_error: Optional[bool] = Query(None, description="是否有错误"),
    sort_field: str = Query(
        "startTime",
        description="排序字段",
        enum=["planTime", "scheduleTime", "startTime", "endTime"],
    ),
    sort_order: str = Query(
        "desc",
        description="排序方向",
        enum=["asc", "desc"],
    ),
):
    """
     获取任务执行日志

    - 支持分页查询
    - 支持按任务名称过滤
    - 支持按命令过滤
    - 支持时间范围过滤
    - 支持筛选有错误的记录
    - 支持自定义排序字段和方向
    """
    async with MongoDB() as mongo:
        # 构建查询条件
        query = {}

        if job_name:
            query["jobName"] = {
                "$regex": job_name,
                "$options": "i",
            }  # i表示不区分大小写

        if command:
            query["command"] = {"$regex": command, "$options": "i"}  # i表示不区分大小写

        if start_time or end_time:
            query["startTime"] = {}
            if start_time:
                query["startTime"]["$gte"] = start_time
            if end_time:
                query["startTime"]["$lte"] = end_time

        if has_error is not None:
            if has_error:
                query["err"] = {"$ne": ""}
            else:
                query["err"] = ""

        # 计算总记录数
        total = await mongo.db["log"].count_documents(query)
        pages = (total + page_size - 1) // page_size
        skip = (page - 1) * page_size

        cursor = mongo.db["log"].find(
            query,
            sort=[(sort_field, -1 if sort_order == "desc" else 1)],
            skip=skip,
            limit=page_size,
        )

        # 转换为列表
        logs = await cursor.to_list(length=page_size)

        return {
            "total": total,
            "items": logs,
            "page": page,
            "page_size": page_size,
            "pages": pages,
        }
