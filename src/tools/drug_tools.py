# src/tools/drug_tools.py
"""药物查询工具（最新API）"""
from typing import Dict, List, Optional
from langchain_core.tools import tool

from src.vectorstore.drug_db import DrugVectorDB
from src.utils.logger import log


class DrugToolkit:
    """药物工具集"""

    def __init__(self):
        """初始化工具集"""
        self.db = DrugVectorDB()
        try:
            self.db.load()
            log.info("药物数据库加载成功")
        except FileNotFoundError as e:
            log.error(f"数据库加载失败: {e}")
            raise

    @staticmethod
    @tool
    def search_drug_info(drug_name: str) -> str:
        """搜索单个药物的详细信息

        使用这个工具来查询药物的适应症、用法用量、禁忌症、副作用等信息。

        Args:
            drug_name: 药物名称，例如"阿司匹林"、"布洛芬"

        Returns:
            药物的详细信息文本
        """
        toolkit = DrugToolkit()

        log.info(f"查询药物信息: {drug_name}")

        try:
            results = toolkit.db.search(drug_name, k=2)

            if not results:
                return f"❌ 未找到关于'{drug_name}'的信息，请检查药物名称是否正确"

            # 格式化输出
            info_parts = []
            for i, doc in enumerate(results, 1):
                info_parts.append(f"【信息来源 {i}】\n{doc.page_content}")

            result = "\n\n".join(info_parts)
            log.debug(f"查询成功，返回{len(results)}条结果")

            return result

        except Exception as e:
            log.error(f"查询失败: {e}")
            return f"❌ 查询出错: {str(e)}"

    @staticmethod
    @tool
    def check_drug_interaction(drugs: str) -> str:
        """检查多个药物之间的交互风险

        使用这个工具来检查多个药物同时使用是否存在交互风险。

        Args:
            drugs: 逗号分隔的药物列表，例如"阿司匹林,布洛芬"

        Returns:
            药物交互风险评估结果
        """
        log.info(f"检查药物交互: {drugs}")

        # 解析药物列表
        drug_list = [d.strip() for d in drugs.split(",")]

        if len(drug_list) < 2:
            return "⚠️ 需要至少2种药物才能检查交互风险"

        # 已知的药物交互（实际项目应该从数据库读取）
        known_interactions = {
            frozenset(["阿司匹林", "布洛芬"]): {
                "level": "🟡 中度风险",
                "description": "两者都是非甾体抗炎药（NSAIDs），同时使用可能增加胃肠道出血和溃疡的风险。建议间隔4-6小时服用，或咨询医生选择其中一种。",
            },
            frozenset(["阿司匹林", "华法林"]): {
                "level": "🔴 高度风险",
                "description": "华法林是抗凝药，与阿司匹林同时使用会显著增加出血风险。必须在医生指导下使用，并定期监测凝血功能。",
            },
            frozenset(["布洛芬", "华法林"]): {
                "level": "🟡 中度风险",
                "description": "布洛芬可能增强华法林的抗凝作用，增加出血风险。如需同时使用，应在医生监督下进行。",
            },
        }

        warnings = []

        # 检查所有药物组合
        for i in range(len(drug_list)):
            for j in range(i + 1, len(drug_list)):
                pair = frozenset([drug_list[i], drug_list[j]])

                if pair in known_interactions:
                    interaction = known_interactions[pair]
                    warnings.append(
                        f"⚠️ **{drug_list[i]} + {drug_list[j]}**\n"
                        f"   风险等级: {interaction['level']}\n"
                        f"   详细说明: {interaction['description']}"
                    )

        # 生成结果
        if warnings:
            result = "🔍 **药物交互检查结果**\n\n"
            result += "发现以下药物交互风险:\n\n"
            result += "\n\n".join(warnings)
            result += "\n\n" + "=" * 50
            result += "\n⚠️ **重要提示**: 以上信息仅供参考，请务必咨询医生或药师！"
            log.warning(f"发现{len(warnings)}个交互风险")
        else:
            result = (
                "✅ **未发现已知的药物交互风险**\n\n"
                "注意: 这不能替代专业医疗建议。\n"
                "使用新药前，请咨询医生或药师。"
            )
            log.info("未发现交互风险")

        return result


# 获取工具列表（供Agent使用）
def get_drug_tools() -> List:
    """获取所有药物工具"""
    return [DrugToolkit.search_drug_info, DrugToolkit.check_drug_interaction]
