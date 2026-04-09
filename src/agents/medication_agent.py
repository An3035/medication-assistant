from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_community.chat_models import ChatTongyi
from src.tools.drug_tools import get_drug_tools
from src.utils.prompts import get_medication_agent_prompt
from src.utils.logger import log


class MedicationAgent:
    def __init__(self):
        self.tools = get_drug_tools()
        self.llm = ChatTongyi(model="qwen-turbo", temperature=0)

        self.prompt = get_medication_agent_prompt()
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.system_message = self.prompt.messages[0].prompt.template
        self.chat_history = []

    def chat(self, user_input: str, chat_history: list = None) -> str:
        history_to_use = chat_history if chat_history is not None else self.chat_history

        try:
            # 1. 构建初始消息
            messages = []
            messages.append(("system", self.system_message))
            messages.extend(history_to_use)
            messages.append(("human", user_input))

            # 2. 第一次调用 LLM（决定是否调用工具）
            response = self.llm_with_tools.invoke(messages)

            # 3. 处理工具调用
            if hasattr(response, "tool_calls") and response.tool_calls:
                intermediate_messages = [response]  # 包含 tool_calls 的 AI 消息

                for tool_call in response.tool_calls:
                    # --- 修复点 1：兼容处理 Pydantic 对象和字典 ---
                    if hasattr(tool_call, "name"):
                        # LangChain 新版本：ToolCall 是 Pydantic 对象
                        tool_name = tool_call.name
                        tool_args = tool_call.args
                        tool_call_id = tool_call.id
                    else:
                        # 旧版本/兼容模式：字典结构
                        tool_name = tool_call.get("name")
                        tool_args = tool_call.get("args")
                        tool_call_id = tool_call.get("id") or tool_call.get(
                            "tool_call_id"
                        )

                    if not tool_name or not tool_args or not tool_call_id:
                        log.error(f"无效的 tool_call: {tool_call}")
                        continue

                    # 执行工具
                    tool = next((t for t in self.tools if t.name == tool_name), None)
                    if tool:
                        try:
                            observation = tool.invoke(tool_args)
                            # --- 修复点 2：使用 ToolMessage 并传入 tool_call_id ---
                            intermediate_messages.append(
                                ToolMessage(
                                    content=str(observation), tool_call_id=tool_call_id
                                )
                            )
                        except Exception as e:
                            log.error(f"工具执行失败: {e}")
                            intermediate_messages.append(
                                ToolMessage(
                                    content=f"❌ 工具错误: {e}",
                                    tool_call_id=tool_call_id,
                                )
                            )

                # 4. 第二次调用 LLM（根据工具结果生成最终回复）
                final_messages = messages + intermediate_messages
                final_response = self.llm.invoke(final_messages)
                response_content = final_response.content
            else:
                response_content = response.content

            # 更新历史
            self.chat_history.append(HumanMessage(content=user_input))
            self.chat_history.append(AIMessage(content=response_content))

            return response_content

        except Exception as e:
            log.error(f"聊天处理失败: {e}")
            return f"❌ 处理出错: {str(e)}"
