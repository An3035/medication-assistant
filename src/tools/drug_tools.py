"""药物工具（优化版：从 data/raw/drugs.csv 预加载 + 双层缓存）"""

import csv
from pathlib import Path
from typing import Dict, List
from langchain_core.tools import tool
from src.utils.logger import log

# ===================== 1. 预加载药物数据到内存（启动时执行一次） =====================
PROJECT_ROOT = Path(__file__).parent.parent.parent
DRUGS_CSV_PATH = PROJECT_ROOT / "data" / "raw" / "drugs.csv"

_DRUG_DATA: Dict[str, Dict] = {}
_DRUG_INTERACTIONS: Dict[str, List[str]] = {}


def _load_drug_data():
    global _DRUG_DATA, _DRUG_INTERACTIONS
    log.info(f"📚 正在从 {DRUGS_CSV_PATH} 加载药物数据...")

    if not DRUGS_CSV_PATH.exists():
        log.error(f"❌ 药物数据文件不存在：{DRUGS_CSV_PATH}")
        return

    try:
        with open(DRUGS_CSV_PATH, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            log.info(f"✅ CSV 表头：{reader.fieldnames}")

            for row in reader:
                drug_name = row.get("drug_name", "").strip()
                if not drug_name:
                    continue

                # 👇 完全按照你的 CSV 表头读取！！！
                _DRUG_DATA[drug_name] = {
                    "generic_name": row.get("generic_name", ""),
                    "category": row.get("category", ""),
                    "indication": row.get("indication", ""),
                    "dosage": row.get("dosage", ""),
                    "contraindication": row.get("contraindication", ""),
                    "side_effects": row.get("side_effects", ""),
                    "interaction_drugs": row.get("interaction_drugs", ""),
                }

        log.info(f"✅ 药物数据预加载完成：共 {len(_DRUG_DATA)} 种药物")

    except Exception as e:
        log.error(f"❌ 加载失败：{str(e)}")


_load_drug_data()


# ===================== 工具函数 =====================
@tool
def get_side_effects(drug_name: str) -> str:
    """获取药物副作用"""
    info = _DRUG_DATA.get(drug_name)
    if not info:
        return f"未找到药物：{drug_name}"
    return info["side_effects"]


@tool
def get_dosage(drug_name: str) -> str:
    """获取药物用法用量"""
    info = _DRUG_DATA.get(drug_name)
    if not info:
        return f"未找到药物：{drug_name}"
    return info["dosage"]


@tool
def check_drug_interaction(drug_a: str, drug_b: str) -> str:
    """检查药物相互作用"""
    info_a = _DRUG_DATA.get(drug_a)
    if not info_a:
        return f"未找到药物：{drug_a}"

    interactions = info_a.get("interaction_drugs", "")
    if drug_b in interactions:
        return f"⚠️ {drug_a} 与 {drug_b} 存在相互作用风险：\n{interactions}"

    return f"✅ {drug_a} 与 {drug_b} 未发现明显相互作用"


def get_drug_tools():
    return [get_side_effects, get_dosage, check_drug_interaction]
