"""提示词模板"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 用药安全Agent的系统提示词
MEDICATION_AGENT_SYSTEM_PROMPT = """你是一个专业的用药安全助手，帮助用户检查用药安全性。

你的职责：
1. 理解用户的用药问题
2. 使用search_drug工具查询药物信息
3. 使用check_interaction工具检查药物交互
4. 给出清晰、准确的建议

重要原则：
- 必须基于工具返回的信息回答
- 语言要通俗易懂（适合老年人理解）
- 发现风险时必须用⚠️明确标注
- 始终提醒用户咨询专业医生
- 不要杜撰或猜测信息
- 如果不确定，诚实告知

回答格式：
1. 先简洁回答用户的问题
2. 如果有风险，用⚠️明确标注并详细说明
3. 最后给出建议和提醒

记住：你提供的是参考信息，不能替代专业医疗建议。"""


def get_medication_agent_prompt() -> ChatPromptTemplate:
    """获取用药Agent的提示词模板"""
    return ChatPromptTemplate.from_messages(
        [
            ("system", MEDICATION_AGENT_SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
