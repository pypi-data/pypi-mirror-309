from typing import Optional

from pydantic import BaseModel, Field


class Log(BaseModel):
    jobName: str = Field(..., description="任务名称")
    command: str = Field(..., description="执行的命令")
    err: Optional[str] = Field(None, description="错误信息")
    output: Optional[str] = Field(None, description="输出结果")
    planTime: int = Field(..., description="计划执行时间")
    scheduleTime: int = Field(..., description="实际调度时间")
    startTime: int = Field(..., description="开始执行时间")
    endTime: int = Field(..., description="执行结束时间")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "job123456",
                "jobName": "backup-task",
                "command": "tar -czf backup.tar.gz /data",
                "err": None,
                "output": "backup completed successfully",
                "planTime": 1711006245000,
                "scheduleTime": 1711006245100,
                "startTime": 1711006245200,
                "endTime": 1711006248300,
            }
        }
