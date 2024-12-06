from motor.motor_asyncio import AsyncIOMotorClient

from core.config import settings


class MongoDB:
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.db = None

    async def connect(self):
        """初始化MongoDB连接"""
        if self.client is None:
            self.client = AsyncIOMotorClient(
                settings.MONGO_URL,
                serverSelectionTimeoutMS=5000,  # 服务器选择超时
                connectTimeoutMS=5000,  # 连接超时
                socketTimeoutMS=5000,  # socket超时
            )
            self.db = self.client[settings.MONGO_DB_NAME]
        return self.client

    async def test_connection(self):
        """测试连接是否成功"""

        server_info = await self.client.server_info()
        print(f"✅ 成功连接到MongoDB服务器: {server_info.get('version', 'unknown')}")

    def get_client(self):
        """获取MongoDB客户端实例"""
        if self.client is None:
            raise RuntimeError("MongoDB client not initialized. Call connect() first.")
        return self.client

    async def close(self):
        """关闭MongoDB连接"""
        if self.client:
            self.client.close()
            self.client = None

    async def __aenter__(self):
        """支持异步上下文管理器"""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """退出时自动关闭连接"""
        await self.close()
