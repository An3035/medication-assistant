"""配置管理（使用 Pydantic Settings）"""

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import Optional

# 加载.env 文件并覆盖已存在的环境变量
load_dotenv()


class Settings(BaseSettings):
    """应用配置"""

    # OpenAI 配置
    openai_api_key: str = ""
    openai_api_base: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-3.5-turbo"

    # DeepSeek 相关配置
    deepseek_api_key: Optional[str] = None
    deepseek_model: str = "deepseek-chat"

    # 智谱 AI 配置
    zhipuai_api_key: Optional[str] = None

    # 阿里云 DashScope 配置
    # 定义了一个叫 dashscope_api_key 的参数，它要么是一串字符（API Key），要么什么都没有（None）
    # 如果你不传值给我，我就默认它是 None
    dashscope_api_key: Optional[str] = None

    # 向量数据库
    chroma_persist_dir: Path = Path("./data/vectorstore")

    # 应用配置
    app_env: str = "development"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# 创建全局配置实例
settings = Settings()
