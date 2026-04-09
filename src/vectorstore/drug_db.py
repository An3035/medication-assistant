# src/vectorstore/drug_db.py
"""药物向量数据库（使用最新 API）"""
import os
from pathlib import Path
from typing import List, Optional

from langchain_community.document_loaders import CSVLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

from src.config.settings import settings
from src.utils.logger import log


class DrugVectorDB:
    """药物向量数据库管理"""

    def __init__(self, persist_dir: Optional[Path] = None):
        """初始化向量数据库

        Args:
            persist_dir: 持久化目录路径，默认从配置读取
        """
        self.persist_dir = persist_dir or settings.chroma_persist_dir
        self.persist_dir.mkdir(parents=True, exist_ok=True)

        # 使用阿里云 DashScope Embeddings
        # 设置环境变量以处理SSL问题
        os.environ['REQUESTS_CA_BUNDLE'] = ''
        os.environ['CURL_CA_BUNDLE'] = ''
        
        self.embeddings = DashScopeEmbeddings(
            dashscope_api_key=settings.dashscope_api_key,
            model="text-embedding-v1"
        )

        self.vectorstore: Optional[Chroma] = None
        log.info(f"向量数据库初始化，持久化目录：{self.persist_dir}")

    def create_from_csv(self, csv_path: str) -> None:
        """从CSV创建向量数据库

        Args:
            csv_path: CSV文件路径
        """
        log.info(f"开始加载数据: {csv_path}")

        # 加载CSV
        loader = CSVLoader(file_path=csv_path, encoding="utf-8-sig")
        documents = loader.load()

        log.info(f"已加载 {len(documents)} 条数据")

        # 创建向量数据库（最新API）
        log.info("正在创建向量索引...")
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=str(self.persist_dir),
            collection_name="drugs",  # 指定集合名称
        )

        log.info(f"✅ 向量数据库创建成功: {self.persist_dir}")

    def load(self) -> None:
        """加载已有的向量数据库"""
        if not self.persist_dir.exists():
            raise FileNotFoundError(
                f"向量数据库不存在: {self.persist_dir}\n"
                f"请先运行数据准备脚本创建数据库"
            )

        log.info(f"正在加载向量数据库: {self.persist_dir}")

        self.vectorstore = Chroma(
            persist_directory=str(self.persist_dir),
            embedding_function=self.embeddings,
            collection_name="drugs",
        )

        log.info("✅ 向量数据库加载成功")

    def search(
        self, query: str, k: int = 3, filter_dict: Optional[dict] = None
    ) -> List[Document]:
        """搜索相关文档

        Args:
            query: 查询文本
            k: 返回结果数量
            filter_dict: 过滤条件（可选）

        Returns:
            相关文档列表
        """
        if self.vectorstore is None:
            raise ValueError("向量数据库未初始化，请先调用load()或create_from_csv()")

        log.debug(f"搜索查询: {query}, top_k={k}")

        # 使用最新的similarity_search API
        results = self.vectorstore.similarity_search(
            query=query, k=k, filter=filter_dict  # 支持元数据过滤
        )

        log.info(f"找到 {len(results)} 个相关文档")
        return results

    def search_with_score(self, query: str, k: int = 3) -> List[tuple[Document, float]]:
        """搜索并返回相似度分数

        Args:
            query: 查询文本
            k: 返回结果数量

        Returns:
            (文档, 分数)元组列表
        """
        if self.vectorstore is None:
            raise ValueError("向量数据库未初始化")

        results = self.vectorstore.similarity_search_with_score(query=query, k=k)

        return results


# 测试代码
if __name__ == "__main__":
    # 示例：创建数据库
    db = DrugVectorDB()

    # 如果数据文件存在，创建数据库
    csv_path = "data/raw/drugs.csv"
    if Path(csv_path).exists():
        db.create_from_csv(csv_path)

        # 测试搜索
        results = db.search("阿司匹林的副作用", k=2)
        for i, doc in enumerate(results):
            print(f"\n结果 {i+1}:")
            print(doc.page_content[:200])
    else:
        print(f"数据文件不存在: {csv_path}")
        print("请先创建数据文件")
