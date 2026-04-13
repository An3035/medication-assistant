"""性能测试（带缓存对比）"""

print("=" * 50)
print("【DEBUG】测试脚本开始运行！")
print("=" * 50)
import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.agents.medication_agent import MedicationAgent


def test_response_time():
    agent = MedicationAgent()

    test_queries = [
        "阿司匹林的副作用",
        "布洛芬的用法用量",
        "阿司匹林和布洛芬能一起吃吗",
        "感冒了吃什么药",
        "高血压用什么药",
    ]

    print("\n" + "=" * 60)
    print("🔴 第一轮测试（无缓存，第一次访问）")
    print("=" * 60)
    times_round1 = []
    for query in test_queries:
        print(f"\n测试: {query}")
        start = time.time()
        response = agent.chat(query)
        elapsed = time.time() - start
        times_round1.append(elapsed)
        print(f"耗时: {elapsed:.2f}秒")
        print(f"回答: {response[:100]}...")

    print("\n" + "=" * 60)
    print("🟢 第二轮测试（有缓存，第二次访问）")
    print("=" * 60)
    times_round2 = []
    for query in test_queries:
        print(f"\n测试: {query}")
        start = time.time()
        response = agent.chat(query)
        elapsed = time.time() - start
        times_round2.append(elapsed)
        print(f"耗时: {elapsed:.2f}秒")
        print(f"回答: {response[:100]}...")

    print("\n" + "=" * 60)
    print("📊 最终性能结果")
    print("=" * 60)
    print(f"第一轮平均（无缓存）: {sum(times_round1)/len(times_round1):.2f}秒")
    print(f"第二轮平均（有缓存）: {sum(times_round2)/len(times_round2):.2f}秒")
    print(
        f"🚀 缓存加速: {((sum(times_round1)-sum(times_round2))/sum(times_round1)*100):.1f}%"
    )


if __name__ == "__main__":
    test_response_time()
