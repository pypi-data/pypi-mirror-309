import json
from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, Body, HTTPException, Query
from fastapi.responses import JSONResponse
from google.protobuf.json_format import MessageToDict
from pydantic import BaseModel, Field

from services.etcd import EtcdClient

router = APIRouter()


@router.get("/")
async def get_etcd_value(
    key: str = Query("", min_length=1, description="etcd key"),
    prefix: bool = Query(True, description="是否使用前缀匹配模式"),
):
    """
    通过key获取etcd中的值

    参数:
        key: etcd中的键名

    返回:
        包含键值对的JSON响应
    """
    with EtcdClient() as client:
        try:
            if prefix:
                results = [
                    {
                        "key": metadata.key.decode("utf-8"),
                        "value": value.decode("utf-8")
                        if isinstance(value, bytes)
                        else value,
                        "metadata": {
                            "version": metadata.version,
                            "create_revision": metadata.create_revision,
                            "mod_revision": metadata.mod_revision,
                        },
                    }
                    for value, metadata in client.get_prefix(key)
                ]
                if not results:
                    raise HTTPException(
                        status_code=404, detail=f"未找到前缀为 '{key}' 的键"
                    )
                return JSONResponse(results)
            else:
                # 获取单个key的值
                value, metadata = client.get(key)
                if value is None:
                    raise HTTPException(
                        status_code=404, detail=f"Key '{key}' not found"
                    )

                if isinstance(value, bytes):
                    value = value.decode("utf-8")

                return JSONResponse(
                    {
                        "key": key,
                        "value": value,
                        "metadata": {
                            "version": metadata.version,
                            "create_revision": metadata.create_revision,
                            "mod_revision": metadata.mod_revision,
                        },
                    }
                )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error getting value from etcd: {str(e)}"
            )


# 添加请求体模型
class EtcdValue(BaseModel):
    key: str = Field(..., description="etcd key")
    value: Union[str, Dict[str, Any], List[Any]] = Field(..., description="要设置的值")
    lease: Optional[int] = Field(None, ge=1, description="lease TTL in seconds")


@router.put("/")
async def put_etcd_value(
    data: EtcdValue = Body(..., description="要设置的键值对"),
):
    """
    设置etcd中的值

    参数:
        data: 包含key和value的请求体

    返回:
        设置成功的响应
    """
    with EtcdClient() as client:
        try:
            # 使用更简洁的序列化方式
            value_str = (
                json.dumps(data.value)
                if isinstance(data.value, (dict, list))
                else str(data.value)
            )

            lease_id = None
            if data.lease:
                try:
                    lease = client.lease(data.lease)
                    lease_id = lease.id
                except Exception as e:
                    raise HTTPException(
                        status_code=400, detail=f"创建lease失败: {str(e)}"
                    )

            try:
                metadata = client.put(data.key, value_str, lease=lease_id)
            except Exception:
                if lease_id:
                    # 如果put失败，尝试撤销lease
                    try:
                        lease.revoke()
                    except Exception:
                        pass
                raise

            return JSONResponse(
                {
                    "key": data.key,
                    "value": data.value,
                    "lease_id": lease_id,
                    "metadata": MessageToDict(metadata) if metadata else None,
                    "message": "设置成功",
                }
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"设置etcd值时发生错误: {str(e)}"
            )


@router.delete("/")
async def delete_etcd_value(
    key: str = Query(..., description="要删除的etcd key"),
    prefix: bool = Query(False, description="是否使用前缀删除模式"),
):
    """
    删除etcd中的键值

    参数:
        key: 要删除的键名
        prefix: 是否使用前缀删除模式,如果为True则删除所有匹配前缀的键

    返回:
        删除成功的响应
    """
    with EtcdClient() as client:
        try:
            if prefix:
                deleted = client.delete_prefix(key)
                return JSONResponse(
                    {
                        "message": f"已删除所有前缀为 '{key}' 的键值",
                        "deleted_count": deleted,
                    }
                )
            else:
                deleted = client.delete(key)
                if not deleted:
                    raise HTTPException(status_code=404, detail=f"未找到键 '{key}'")
                return JSONResponse(
                    {"message": f"成功删除键 '{key}'", "deleted_count": 1}
                )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"从etcd删除值时发生错误: {str(e)}"
            )
