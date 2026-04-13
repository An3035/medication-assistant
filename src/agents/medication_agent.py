from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_community.chat_models import ChatTongyi
from src.tools.drug_tools import get_drug_tools, _DRUG_DATA
from src.utils.prompts import get_medication_agent_prompt
from src.utils.logger import log
from src.utils.cache import cache_instance


class MedicationAgent:
    def __init__(self):
        self.tools = get_drug_tools()
        self.llm = ChatTongyi(
            model="qwen-turbo", temperature=0, max_tokens=2048, max_retries=3
        )
        self.prompt = get_medication_agent_prompt()
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.system_message = self.prompt.messages[0].prompt.template
        self.chat_history = []
        # 使用全局缓存实例替代原来的简单字典
        self.cache = cache_instance

    def chat(self, user_input: str, chat_history: list = None) -> str:
        history_to_use = chat_history if chat_history is not None else self.chat_history

        # 生成缓存键
        cache_key = f"medication_agent:response:{user_input}:{str(chat_history or [])}"

        # ===================== 前置拦截（第一轮就极速） =====================
        if not chat_history:
            # 1. 副作用
            if "副作用" in user_input:
                for drug in _DRUG_DATA:
                    if drug in user_input:
                        info = _DRUG_DATA[drug]
                        res = f"{drug}的常见副作用：\n{info['side_effects']}"
                        # 使用全局缓存实例保存结果
                        self.cache.set(cache_key, res)
                        return res

            # 2. 用法用量
            if any(
                k in user_input for k in ["用法", "用量", "怎么吃", "吃多少", "剂量"]
            ):
                for drug in _DRUG_DATA:
                    if drug in user_input:
                        info = _DRUG_DATA[drug]
                        res = f"{drug}的用法用量：\n{info['dosage']}"
                        # 使用全局缓存实例保存结果
                        self.cache.set(cache_key, res)
                        return res

            # 3. 药物相互作用 / 能不能一起吃
            if any(k in user_input for k in ["一起吃", "相互作用", "同服", "冲突"]):
                found_drugs = [d for d in _DRUG_DATA if d in user_input]
                if len(found_drugs) >= 2:
                    a, b = found_drugs[0], found_drugs[1]
                    info_a = _DRUG_DATA.get(a, {})
                    if b in info_a.get("interaction_drugs", ""):
                        res = f"⚠️ {a} 与 {b} 存在相互作用：\n{info_a['interaction_drugs']}"
                    else:
                        res = f"✅ {a} 与 {b} 未发现明显相互作用"
                    # 使用全局缓存实例保存结果
                    self.cache.set(cache_key, res)
                    return res

        # 先检查全局缓存（重复问题更快）
        cached_result = self.cache.get(cache_key)
        if cached_result is not None:
            log.debug(f"🎯 命中全局缓存: {cache_key}")
            return cached_result

        # ===================== 复杂问题才走 LLM（兜底） =====================
        try:
            messages = [("system", self.system_message)]
            messages.extend(history_to_use)
            messages.append(("human", user_input))

            response = self.llm_with_tools.invoke(messages)
            intermediate_messages = [response]

            if hasattr(response, "tool_calls") and response.tool_calls:
                for tool_call in response.tool_calls:
                    if hasattr(tool_call, "name"):
                        tool_name = tool_call.name
                        tool_args = tool_call.args
                        tool_call_id = tool_call.id
                    else:
                        tool_name = tool_call.get("name")
                        tool_args = tool_call.get("args")
                        tool_call_id = tool_call.get("id") or tool_call.get(
                            "tool_call_id"
                        )

                    if not all([tool_name, tool_args, tool_call_id]):
                        log.error(f"无效工具调用: {tool_call}")
                        continue

                    tool = next((t for t in self.tools if t.name == tool_name), None)
                    if tool:
                        try:
                            obs = tool.invoke(tool_args)
                            intermediate_messages.append(
                                ToolMessage(content=str(obs), tool_call_id=tool_call_id)
                            )
                        except Exception as e:
                            log.error(f"工具执行失败: {e}")
                            intermediate_messages.append(
                                ToolMessage(
                                    content=f"工具错误: {e}", tool_call_id=tool_call_id
                                )
                            )

                final_messages = messages + intermediate_messages
                # 使用stream而不是invoke来支持流式输出逻辑
                final_response_stream = self.llm.stream(final_messages)
                
                # 处理流式响应
                response_content = ""
                for chunk in final_response_stream:
                    if hasattr(chunk, 'content') and chunk.content:
                        response_content += chunk.content

                # 如果响应为空，说明大模型无法回答
                if not response_content.strip():
                    response_content = "抱歉，我不太清楚这个问题的答案。"
            else:
                # 如果没有工具调用，直接从response获取内容
                response_content = response.content if hasattr(response, 'content') and response.content else "抱歉，我不太清楚这个问题的答案。"

            # 确保响应内容不为空
            if not response_content.strip():
                response_content = "抱歉，我不太清楚这个问题的答案。"

            # 更新历史与全局缓存
            if not chat_history:
                self.chat_history.append(HumanMessage(content=user_input))
                self.chat_history.append(AIMessage(content=response_content))
                # 使用全局缓存实例保存结果
                self.cache.set(cache_key, response_content)

            return response_content

        except Exception as e:
            log.error(f"处理失败: {e}")
            return "抱歉，处理您的请求时遇到了问题，暂时无法回答。"

    def chat_stream(self, user_input: str, chat_history: list = None):
        """
        支持流式输出的聊天方法
        """
        history_to_use = chat_history if chat_history is not None else self.chat_history
        
        # 生成缓存键
        cache_key = f"medication_agent:response:{user_input}:{str(chat_history or [])}"
        
        # ===================== 前置拦截（第一轮就极速） =====================
        if not chat_history:
            # 1. 副作用
            if "副作用" in user_input:
                for drug in _DRUG_DATA:
                    if drug in user_input:
                        info = _DRUG_DATA[drug]
                        res = f"{drug}的常见副作用：\n{info['side_effects']}"
                        # 使用全局缓存实例保存结果
                        self.cache.set(cache_key, res)
                        yield res
                        return

            # 2. 用法用量
            if any(
                k in user_input for k in ["用法", "用量", "怎么吃", "吃多少", "剂量"]
            ):
                for drug in _DRUG_DATA:
                    if drug in user_input:
                        info = _DRUG_DATA[drug]
                        res = f"{drug}的用法用量：\n{info['dosage']}"
                        # 使用全局缓存实例保存结果
                        self.cache.set(cache_key, res)
                        yield res
                        return

            # 3. 药物相互作用 / 能不能一起吃
            if any(k in user_input for k in ["一起吃", "相互作用", "同服", "冲突"]):
                found_drugs = [d for d in _DRUG_DATA if d in user_input]
                if len(found_drugs) >= 2:
                    a, b = found_drugs[0], found_drugs[1]
                    info_a = _DRUG_DATA.get(a, {})
                    if b in info_a.get("interaction_drugs", ""):
                        res = f"⚠️ {a} 与 {b} 存在相互作用：\n{info_a['interaction_drugs']}"
                    else:
                        res = f"✅ {a} 与 {b} 未发现明显相互作用"
                    # 使用全局缓存实例保存结果
                    self.cache.set(cache_key, res)
                    yield res
                    return

        # 先检查全局缓存（重复问题更快）
        cached_result = self.cache.get(cache_key)
        if cached_result is not None:
            log.debug(f"🎯 命中全局缓存: {cache_key}")
            yield cached_result
            return

        # ===================== 复杂问题才走 LLM（兜底） =====================
        try:
            messages = [("system", self.system_message)]
            messages.extend(history_to_use)
            messages.append(("human", user_input))

            response = self.llm_with_tools.invoke(messages)
            intermediate_messages = [response]

            if hasattr(response, "tool_calls") and response.tool_calls:
                for tool_call in response.tool_calls:
                    if hasattr(tool_call, "name"):
                        tool_name = tool_call.name
                        tool_args = tool_call.args
                        tool_call_id = tool_call.id
                    else:
                        tool_name = tool_call.get("name")
                        tool_args = tool_call.get("args")
                        tool_call_id = tool_call.get("id") or tool_call.get(
                            "tool_call_id"
                        )

                    if not all([tool_name, tool_args, tool_call_id]):
                        log.error(f"无效工具调用: {tool_call}")
                        continue

                    tool = next((t for t in self.tools if t.name == tool_name), None)
                    if tool:
                        try:
                            obs = tool.invoke(tool_args)
                            intermediate_messages.append(
                                ToolMessage(content=str(obs), tool_call_id=tool_call_id)
                            )
                        except Exception as e:
                            log.error(f"工具执行失败: {e}")
                            intermediate_messages.append(
                                ToolMessage(
                                    content=f"工具错误: {e}", tool_call_id=tool_call_id
                                )
                            )

                final_messages = messages + intermediate_messages
                # 使用stream而不是invoke来支持流式输出逻辑
                final_response_stream = self.llm.stream(final_messages)
                
                # 处理流式响应
                response_content = ""
                for chunk in final_response_stream:
                    if hasattr(chunk, 'content') and chunk.content:
                        response_content += chunk.content
                        yield response_content

                # 如果响应为空，说明大模型无法回答
                if not response_content.strip():
                    response_content = "抱歉，我不太清楚这个问题的答案。"
                    yield response_content
            else:
                # 如果没有工具调用，直接从response获取内容
                response_content = response.content if hasattr(response, 'content') and response.content else "抱歉，我不太清楚这个问题的答案。"
                yield response_content

        except Exception as e:
            log.error(f"处理失败: {e}")
            yield "抱歉，处理您的请求时遇到了问题，暂时无法回答。"
