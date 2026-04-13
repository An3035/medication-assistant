"""
测试环境配置是否正常
"""
import sys
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Python path: {sys.path[:3]}...")  # 只显示前3个项目

# 测试基本导入
try:
    import json
    import hashlib
    from typing import Any, Callable, Optional
    from functools import wraps
    print("✓ 基础库导入成功")
except ImportError as e:
    print(f"✗ 基础库导入失败: {e}")

# 测试项目相关导入
try:
    from src.utils.logger import log
    print("✓ logger 导入成功")
except ImportError as e:
    print(f"✗ logger 导入失败: {e}")

try:
    import redis
    print("✓ redis 导入成功")
except ImportError as e:
    print(f"✗ redis 导入失败: {e}")

# 最重要的测试：测试我们修改后的 cache 模块
try:
    from src.utils.cache import dual_cache
    print("✓ cache 模块导入成功")
except ImportError as e:
    print(f"✗ cache 模块导入失败: {e}")
    
print("\n环境测试完成")