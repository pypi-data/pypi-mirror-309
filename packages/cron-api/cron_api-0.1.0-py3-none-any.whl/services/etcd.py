import functools

import etcd3

from core.config import settings


def require_connection(func):
    """确保client已初始化的装饰器"""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.client is None:
            raise RuntimeError("Etcd client not initialized. Call connect() first.")
        return func(self, *args, **kwargs)

    return wrapper


class EtcdClient:
    def __init__(self):
        self.client = None

    def connect(self):
        """初始化etcd连接"""
        if self.client is None:
            host, port = settings.ETCD_HOSTS.split(":")
            self.client = etcd3.client(
                host=host,
                port=int(port),
                timeout=5,
            )
        return self.client

    @require_connection
    def test_connection(self):
        """测试连接是否成功"""
        status = self.client.status()
        print(f"✅ 成功连接到etcd服务器: {status}")

    @require_connection
    def get_client(self):
        """获取etcd客户端实例"""
        return self.client

    @require_connection
    def get_prefix(self, key_prefix: str):
        """
        获取指定前缀的所有键值对

        返回: 包含(value, metadata)元组的列表，如果没有匹配项返回空列表
        """
        results = list(self.client.get_prefix(key_prefix))
        return results if results else []

    @require_connection
    def lease(self, ttl: int):
        """
        创建一个具有指定TTL(秒)的lease

        参数:
            ttl: lease的存活时间(秒)

        返回:
            lease对象
        """
        return self.client.lease(ttl)

    @require_connection
    def put(self, key: str, value: str, lease=None):
        """
        设置键值对

        参数:
            key: 键
            value: 值
            lease: 可选的lease ID
        """
        return self.client.put(key, value, lease=lease)

    @require_connection
    def get(self, key: str):
        """获取指定键的值"""
        return self.client.get(key)

    @require_connection
    def delete(self, key: str) -> bool:
        """删除指定的键值对,成功返回True,键不存在返回False"""
        return self.client.delete(key)

    @require_connection
    def delete_prefix(self, prefix: str) -> int:
        """删除所有指定前缀的键值对，返回删除的数量"""
        return self.client.delete_prefix(prefix)

    def close(self):
        """关闭etcd连接"""
        if self.client:
            self.client.close()
            self.client = None

    def __enter__(self):
        """支持上下文管理器"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出时自动关闭连接"""
        self.close()
