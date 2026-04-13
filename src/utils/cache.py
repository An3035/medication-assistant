"""双层缓存工具：本地 LRU + Redis 持久化"""

import json
import hashlib
from typing import Any, Callable, Optional
from functools import wraps, lru_cache
from redis import Redis, ConnectionError
from src.utils.logger import log

# -------------------------- 配置 --------------------------
# 本地缓存：最多存 1000 条，防止内存溢出
# 使用 functools.lru_cache 替代 cachetools
LOCAL_CACHE_MAXSIZE = 1000

# 使用一个字典作为底层缓存存储
_local_cache = {}


def _check_local_cache(key):
    return key in _local_cache


def _get_from_local_cache(key):
    return _local_cache.get(key)


def _set_local_cache(key, value):
    if len(_local_cache) >= LOCAL_CACHE_MAXSIZE:
        # 简单地删除第一个项目（非真正的LRU，但在这种简单实现中足够了）
        first_key = next(iter(_local_cache))
        del _local_cache[first_key]
    _local_cache[key] = value


def _clear_local_cache(prefix=None):
    if prefix:
        keys_to_delete = [k for k in _local_cache if k.startswith(prefix)]
        for k in keys_to_delete:
            del _local_cache[k]
    else:
        _local_cache.clear()


# Redis 连接（单例模式）
_redis_client: Optional[Redis] = None


def get_redis() -> Redis:
    """获取 Redis 单例客户端"""
    global _redis_client
    if _redis_client is None:
        try:
            _redis_client = Redis(
                host="localhost",
                port=6379,
                db=0,
                decode_responses=True,  # 自动解码为字符串
                socket_connect_timeout=2,
                socket_timeout=2,
            )
            _redis_client.ping()  # 测试连接
            log.info("✅ Redis 连接成功")
        except ConnectionError:
            log.warning("⚠️ Redis 连接失败，降级为仅本地缓存")
            _redis_client = None
    return _redis_client


# 创建全局缓存实例
class GlobalCache:
    """全局缓存实例，提供直接的缓存操作方法"""

    def __init__(self):
        self.local_maxsize = LOCAL_CACHE_MAXSIZE

    def get(self, key: str, default=None):
        """获取缓存值"""
        # 先查本地缓存
        if _check_local_cache(key):
            log.debug(f"🎯 命中本地缓存: {key}")
            return _get_from_local_cache(key)

        # 再查 Redis
        redis_client = get_redis()
        if redis_client:
            cached_value = redis_client.get(key)
            if cached_value:
                log.debug(f"🎯 命中 Redis 缓存: {key}")
                result = json.loads(cached_value)
                # 同步到本地缓存
                _set_local_cache(key, result)
                return result

        return default

    def set(self, key: str, value: Any, ttl: int = 86400 * 365):  # 默认一年过期
        """设置缓存值"""
        # 先写本地
        _set_local_cache(key, value)
        # 再写 Redis
        redis_client = get_redis()
        if redis_client:
            try:
                redis_client.setex(key, ttl, json.dumps(value, ensure_ascii=False))
            except Exception as e:
                log.warning(f"⚠️ 写入 Redis 缓存失败: {e}")

    def exists(self, key: str) -> bool:
        """检查缓存是否存在"""
        return _check_local_cache(key) or (get_redis() and get_redis().exists(key))

    def delete(self, key: str):
        """删除缓存项"""
        # 删除本地缓存
        if key in _local_cache:
            del _local_cache[key]
        # 删除 Redis 缓存
        redis_client = get_redis()
        if redis_client:
            redis_client.delete(key)

    def clear(self, prefix: Optional[str] = None):
        """清空缓存（可选，用于数据更新时）"""
        # 清空本地
        _clear_local_cache(prefix)

        # 清空 Redis
        redis_client = get_redis()
        if redis_client:
            if prefix:
                pattern = f"{prefix}*"
                keys = redis_client.keys(pattern)
                if keys:
                    redis_client.delete(*keys)
            else:
                redis_client.flushdb()

        log.info(f"🧹 缓存已清空: {prefix or '全部'}")


# 创建全局缓存实例
cache_instance = GlobalCache()


# -------------------------- 缓存 Key 生成 --------------------------
def _generate_cache_key(prefix: str, *args, **kwargs) -> str:
    """生成唯一的缓存 Key"""
    key_data = f"{prefix}:{str(args)}:{str(sorted(kwargs.items()))}"
    return hashlib.md5(key_data.encode()).hexdigest()


# -------------------------- 双层缓存装饰器（核心） --------------------------
def dual_cache(prefix: str, ttl: int = 86400 * 365):  # 默认缓存 1 年
    """
    双层缓存装饰器：先查本地，再查 Redis，都没有则执行函数并缓存
    :param prefix: 缓存 Key 前缀（建议用 "工具名:函数名"）
    :param ttl: Redis 过期时间（秒），默认 1 年
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # 1. 生成缓存 Key
            cache_key = _generate_cache_key(prefix, *args, **kwargs)
            full_key = f"medication:{prefix}:{cache_key}"

            # 2. 使用统一的缓存实例进行查询（改进版）
            cached_result = cache_instance.get(full_key)
            if cached_result is not None:
                return cached_result

            # 3. 都没有，执行原函数
            log.info(f"⚡ 未命中缓存，执行函数: {func.__name__}")
            result = func(*args, **kwargs)

            # 4. 使用统一的缓存实例进行存储
            cache_instance.set(full_key, result, ttl)

            return result

        return wrapper

    return decorator


# -------------------------- 手动缓存操作（可选） --------------------------
def clear_cache(prefix: Optional[str] = None):
    """清空缓存（可选，用于数据更新时）"""
    cache_instance.clear(prefix)
