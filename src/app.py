import sys
import os

# 路径处理
file_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(file_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st
from src.agents.medication_agent import MedicationAgent

# --- 页面配置 ---
st.set_page_config(
    page_title="智能用药安全助手",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "智能用药安全助手 | 仅供参考，不替代专业医疗建议"},
)


# --- 自定义CSS (纯净专业版 | 提问后无任何多余方块) ---
def load_custom_css():
    st.markdown(
        """
    <style>
        /* 1. 全局背景 - 统一沉稳深色 */
        .main {
            background-color: #0a0f1d;
            min-height: 100vh;
            padding-bottom: 2rem;
        }

        /* 2. 侧边栏 - 专业深色统一 */
        [data-testid="stSidebar"] {
            background-color: #070c16 !important;
            color: #f8fafc !important;
            border-right: 1px solid #1e293b;
        }
        
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1.5rem;
        }
        
        /* 强制侧边栏文字清晰 */
        [data-testid="stSidebar"] * {
            color: #f8fafc !important;
        }
        [data-testid="stSidebar"] small {
            color: #94a3b8 !important;
        }
        [data-testid="stSidebar"] .stAlert {
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 8px;
        }
        [data-testid="stSidebar"] .stInfo {
            background-color: #1e3a5f;
            border: 1px solid #1e40af;
            border-radius: 8px;
        }

        /* 3. 标题样式 - 双状态适配 */
        .main-title {
            color: #ffffff;
            font-weight: 700;
            font-size: 2.2rem;
            margin-bottom: 0.5rem;
            text-align: center;
            letter-spacing: -0.02em;
        }
        .sub-title {
            color: #94a3b8;
            font-size: 1rem;
            text-align: center;
            margin-bottom: 2.5rem;
            font-weight: 400;
        }
        
        /* 有对话状态 - 极致压缩标题，节省空间 */
        .main-title.has-chat {
            font-size: 1.5rem;
            margin-bottom: 0.1rem;
        }
        .sub-title.has-chat {
            font-size: 0.85rem;
            margin-bottom: 1.5rem;
        }

        /* 4. 首页功能卡片 - 仅无对话时显示 */
        .function-card {
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 1.5rem;
            height: 100%;
            transition: all 0.2s ease;
            cursor: pointer;
        }
        
        .function-card:hover {
            background-color: #253347;
            border-color: #3b82f6;
        }
        
        .function-card .card-icon {
            font-size: 1.8rem;
            margin-bottom: 0.8rem;
            color: #3b82f6;
        }
        .function-card .card-title {
            color: #ffffff;
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 0.4rem;
        }
        .function-card .card-desc {
            color: #94a3b8;
            font-size: 0.85rem;
            line-height: 1.5;
        }

        /* 5. 首页安全警示卡片 - 仅无对话时显示 */
        .warning-card {
            background-color: #291515;
            border: 1px solid #7f1d1d;
            border-radius: 10px;
            padding: 1.2rem;
        }
        .warning-card .warning-title {
            color: #fca5a5;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.6rem;
            font-size: 0.95rem;
        }
        .warning-card .warning-text {
            color: #fecaca;
            font-size: 0.85rem;
            line-height: 1.6;
            margin: 0;
        }

        /* 6. 核心修改：彻底移除聊天容器方块！有对话时无任何中间色块 */
        .chat-container {
            max-width: 900px;
            margin: 0 auto;
            min-height: 65vh;
            display: flex;
            flex-direction: column;
            /* 无背景、无边框、无圆角，彻底去掉方块 */
            background: none !important;
            border: none !important;
            padding: 0 !important;
            box-shadow: none !important;
        }

        /* 7. 消息气泡 - 纯净适配无容器背景 */
        @keyframes slideInLeft {
            from { opacity: 0; transform: translateX(-30px); }
            to { opacity: 1; transform: translateX(0); }
        }
        @keyframes slideInRight {
            from { opacity: 0; transform: translateX(30px); }
            to { opacity: 1; transform: translateX(0); }
        }

        .message-bubble {
            padding: 1rem 1.3rem;
            border-radius: 12px;
            margin-bottom: 1.2rem;
            line-height: 1.6;
            position: relative;
            max-width: 80%;
            word-wrap: break-word;
        }

        /* 用户消息 - 医疗蓝，靠右 */
        .user-message {
            background-color: #1e40af;
            color: #ffffff !important;
            border-bottom-right-radius: 4px;
            margin-left: auto;
            animation: slideInRight 0.3s ease-out;
        }
        .user-message * {
            color: #ffffff !important;
        }

        /* 助手消息 - 深灰，靠左 */
        .assistant-message {
            background-color: #1e293b;
            color: #f8fafc !important;
            border-bottom-left-radius: 4px;
            margin-right: auto;
            border: 1px solid #334155;
            animation: slideInLeft 0.3s ease-out;
        }
        .assistant-message * {
            color: #f8fafc !important;
        }

        /* 消息发送者标签 */
        .msg-label {
            margin-bottom: 0.4rem;
            font-weight: 500;
            color: #64748b;
            font-size: 0.8rem;
        }

        /* 加载动画 - 极简 */
        .loading-bubble {
            background-color: #1e293b;
            border-radius: 12px;
            padding: 1rem 1.3rem;
            max-width: 100px;
            border: 1px solid #334155;
            animation: slideInLeft 0.3s ease-out;
        }
        .loading-dot {
            display: inline-block;
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #94a3b8;
            margin: 0 2px;
        }

        /* 8. 侧边栏按钮 - 极简专业 */
        .stButton > button {
            width: 100%;
            border-radius: 8px;
            background-color: #1e293b;
            color: #f8fafc !important;
            border: 1px solid #334155;
            transition: all 0.2s ease;
            font-weight: 500;
            margin-bottom: 0.6rem;
        }
        .stButton > button:hover {
            background-color: #253347;
            border-color: #3b82f6;
        }

        /* 9. 输入框美化 - 适配深色背景 */
        [data-testid="stChatInput"] {
            max-width: 900px;
            margin: 1rem auto 0;
        }
        [data-testid="stChatInput"] > div > div > input {
            border-radius: 12px;
            border: 1px solid #334155;
            background-color: #1e293b;
            color: #ffffff;
            padding: 0.9rem 1.2rem;
        }
        [data-testid="stChatInput"] > div > div > input::placeholder {
            color: #64748b;
        }
        [data-testid="stChatInput"] button {
            color: #3b82f6 !important;
        }

        /* 10. 通用样式优化 */
        hr {
            margin: 1.2rem 0;
            border-color: #1e293b;
        }
        /* 隐藏streamlit默认元素 */
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        /* 彻底隐藏无对话时的空白元素 */
        .stHidden {
            display: none !important;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )


load_custom_css()

# --- 初始化 ---
if "agent" not in st.session_state:
    st.session_state.agent = MedicationAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "is_loading" not in st.session_state:
    st.session_state.is_loading = False

# --- 侧边栏 (Sidebar) ---
with st.sidebar:
    # Logo区域
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("https://img.icons8.com/fluency/96/3b82f6/pill.png", width=45)
    with col2:
        st.markdown(
            "<h2 style='margin:0; color:#f8fafc; font-size:1.3rem; font-weight:600;'>智能用药助手</h2>",
            unsafe_allow_html=True,
        )
        st.caption("Medication Assistant")

    st.divider()

    st.markdown("### 快捷咨询")

    # 示例问题按钮
    example_1 = st.button("💊 布洛芬用法用量")
    example_2 = st.button("⚠️ 药物联用风险检查")
    example_3 = st.button("❓ 阿莫西林不良反应")

    st.divider()

    st.markdown("### 使用规范")
    st.info(
        """
    1. 输入药品名称查询完整说明书
    2. 输入多种药品检查联用风险
    3. 可咨询用药禁忌、不良反应等问题
    """
    )

    st.divider()

    st.markdown("### 免责声明")
    st.warning(
        "本助手仅为用药信息参考工具，**不能替代执业医师/药师的专业建议**。"
        "用药前请务必阅读药品说明书并遵医嘱，紧急情况请立即就医。"
    )

    st.divider()

    # 清空历史按钮
    if st.button("🔄 清空对话", type="secondary"):
        st.session_state.messages = []
        st.session_state.agent = MedicationAgent()
        st.session_state.is_loading = False
        st.rerun()

# --- 主界面 (Main Area) ---
# 标题双状态适配
has_chat = len(st.session_state.messages) > 0
title_class = "main-title has-chat" if has_chat else "main-title"
subtitle_class = "sub-title has-chat" if has_chat else "sub-title"

st.markdown(f'<h1 class="{title_class}">智能用药安全中心</h1>', unsafe_allow_html=True)
st.markdown(
    f'<p class="{subtitle_class}">专业药物信息查询 · 联用安全风险评估</p>',
    unsafe_allow_html=True,
)

# --- 核心逻辑：无对话显示功能首页，有对话彻底隐藏所有方块，只显示聊天 ---
if not has_chat:
    # ========== 空状态：仅无对话时显示功能首页 ==========
    st.markdown("<br>", unsafe_allow_html=True)
    func_cols = st.columns(4)

    # 功能1：药品信息查询
    with func_cols[0]:
        if st.container(border=False).button(
            "🔍 药品信息查询", use_container_width=True
        ):
            query_text = "请介绍布洛芬的完整药品信息，包括适应症、用法用量、禁忌"
        st.markdown(
            """
        <div class="function-card">
            <div class="card-icon">💊</div>
            <div class="card-title">药品全信息查询</div>
            <div class="card-desc">查询药品适应症、用法用量、禁忌、不良反应等完整说明书信息</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # 功能2：药物联用风险检查
    with func_cols[1]:
        if st.container(border=False).button(
            "⚠️ 联用风险检查", use_container_width=True
        ):
            query_text = "阿司匹林和华法林能不能一起吃，有什么风险"
        st.markdown(
            """
        <div class="function-card">
            <div class="card-icon">⚕️</div>
            <div class="card-title">联用风险评估</div>
            <div class="card-desc">检查多种药物同时使用的交互风险，规避严重不良反应</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # 功能3：用药禁忌查询
    with func_cols[2]:
        if st.container(border=False).button(
            "🚫 用药禁忌查询", use_container_width=True
        ):
            query_text = "头孢类药物的用药禁忌和注意事项有哪些"
        st.markdown(
            """
        <div class="function-card">
            <div class="card-icon">🚫</div>
            <div class="card-title">用药禁忌查询</div>
            <div class="card-desc">查询特殊人群、肝肾功能不全等场景的用药禁忌与注意事项</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # 功能4：不良反应解读
    with func_cols[3]:
        if st.container(border=False).button(
            "❓ 不良反应解读", use_container_width=True
        ):
            query_text = "服用他汀类药物可能出现哪些不良反应，如何应对"
        st.markdown(
            """
        <div class="function-card">
            <div class="card-icon">📊</div>
            <div class="card-title">不良反应解读</div>
            <div class="card-desc">解读药品不良反应，区分正常反应与危险信号，提供应对建议</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # 用药安全警示
    st.markdown("<br><br>", unsafe_allow_html=True)
    warn_cols = st.columns(3)

    with warn_cols[0]:
        st.markdown(
            """
        <div class="warning-card">
            <div class="warning-title">⚠️ 抗生素滥用风险</div>
            <p class="warning-text">抗生素仅对细菌感染有效，对病毒性感冒无效。滥用会导致耐药性、肠道菌群紊乱，需遵医嘱使用。</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with warn_cols[1]:
        st.markdown(
            """
        <div class="warning-card">
            <div class="warning-title">⚠️ 退烧药联用禁忌</div>
            <p class="warning-text">布洛芬与对乙酰氨基酚不可随意交替/联用，极易导致肝肾功能损伤，需严格按照剂量间隔使用。</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with warn_cols[2]:
        st.markdown(
            """
        <div class="warning-card">
            <div class="warning-title">⚠️ 处方药不可自行调整</div>
            <p class="warning-text">降压药、降糖药、抗凝药等处方药，不可自行增减剂量、停药或换药，否则会引发严重医疗风险。</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

else:
    # ========== 有对话状态：彻底移除所有方块，只显示纯净聊天 ==========
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)

        # 显示历史消息
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(
                    f"""
                <div style="display:flex; flex-direction:column; align-items:flex-end;">
                    <div class="msg-label">您</div>
                    <div class="message-bubble user-message">
                        {msg["content"]}
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                <div style="display:flex; flex-direction:column; align-items:flex-start;">
                    <div class="msg-label">AI 助手</div>
                    <div class="message-bubble assistant-message">
                        {msg["content"]}
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

        # 加载状态
        if st.session_state.is_loading:
            st.markdown(
                """
            <div style="display:flex; flex-direction:column; align-items:flex-start;">
                <div class="msg-label">AI 助手</div>
                <div class="loading-bubble">
                    <span class="loading-dot"></span>
                    <span class="loading-dot"></span>
                    <span class="loading-dot"></span>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

# --- 全局查询逻辑处理 ---
query_text = None

# 侧边栏示例按钮
if example_1:
    query_text = "布洛芬的用法用量、适应症和禁忌是什么？"
elif example_2:
    query_text = "检查阿司匹林和布洛芬能不能一起吃，有什么交互风险"
elif example_3:
    query_text = "阿莫西林的副作用和不良反应有哪些？"

# 底部输入框
if prompt := st.chat_input("请输入药品名称或用药问题..."):
    query_text = prompt

# 执行查询逻辑
if query_text and not st.session_state.is_loading:
    st.session_state.messages.append({"role": "user", "content": query_text})
    st.session_state.is_loading = True
    st.rerun()

# 处理AI回复生成
if st.session_state.is_loading and len(st.session_state.messages) > 0:
    last_user_msg = st.session_state.messages[-1]["content"]
    with st.spinner(""):
        # 使用真正的流式输出，而不是逐字符模拟
        response_placeholder = st.empty()
        full_response = ""
        
        # 从agent获取流式响应
        for chunk in st.session_state.agent.chat_stream(last_user_msg):
            full_response += chunk
            response_placeholder.markdown(full_response + "▌")
            
        # 最终移除光标标记
        response_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.session_state.is_loading = False
    st.rerun()

# src/app.py
"""智能用药助手 - Streamlit应用（最新版本）"""
import streamlit as st
from pathlib import Path

from src.agents.medication_agent import MedicationAgent
from src.config.settings import settings
from src.utils.logger import log

# 页面配置
st.set_page_config(
    page_title="智能用药安全助手",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="expanded",
)

# 自定义CSS
st.markdown(
    """
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
    }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource
def load_agent():
    """加载Agent（使用缓存避免重复加载）"""
    log.info("正在加载Agent...")
    try:
        agent = MedicationAgent()
        log.info("Agent加载成功")
        return agent
    except Exception as e:
        log.error(f"Agent加载失败: {e}")
        st.error(f"❌ 系统初始化失败: {str(e)}")
        st.stop()


def main():
    """主函数"""

    # 标题
    st.markdown(
        "<h1 class='main-header'>🏥 智能用药安全助手</h1>", unsafe_allow_html=True
    )
    st.markdown("---")

    # 使用说明（可折叠）
    with st.expander("📖 使用说明", expanded=False):
        st.markdown(
            """
        ### 功能介绍
        
        ✅ **药物信息查询**  
        查询药物的适应症、用法用量、禁忌症、副作用等详细信息
        
        ⚠️ **药物交互检查**  
        检查多种药物同时使用是否存在交互风险
        
        💡 **用药建议**  
        基于专业知识提供用药建议和注意事项
        
        ### 使用示例
        
        - "阿司匹林有什么副作用？"
        - "我在吃阿司匹林和布洛芬，有问题吗？"
        - "布洛芬的正确用法是什么？"
        - "高血压患者能吃布洛芬吗？"
        
        ### ⚠️ 重要提示
        
        本系统提供的信息**仅供参考**，不能替代专业医疗建议。  
        使用任何药物前，请咨询医生或药师。
        """
        )

    # 初始化会话状态
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "agent" not in st.session_state:
        with st.spinner("🔄 正在初始化AI助手..."):
            st.session_state.agent = load_agent()

    # 显示历史消息
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 用户输入
    if prompt := st.chat_input("请输入您的问题..."):
        # 显示用户消息
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 获取AI回复
        with st.chat_message("assistant"):
            with st.spinner("🤔 正在思考..."):
                # 准备对话历史（只保留最近5轮）
                chat_history = []
                for msg in st.session_state.messages[-10:]:  # 最近5轮=10条消息
                    if msg["role"] == "user":
                        chat_history.append(("user", msg["content"]))
                    else:
                        chat_history.append(("assistant", msg["content"]))

                # 创建响应占位符用于流式输出
                response_placeholder = st.empty()
                
                # 调用Agent，获取流式输出
                response = st.session_state.agent.chat(prompt, chat_history)
                
                # 流式显示响应
                full_response = ""
                # 将响应按字符逐个显示，模拟流式输出
                for char in response:
                    full_response += char
                    response_placeholder.markdown(full_response + "▌")
                    
                # 最终显示完整响应（移除光标标记）
                response_placeholder.markdown(full_response)

            # 将完整响应添加到消息历史
            st.session_state.messages.append({"role": "assistant", "content": full_response})

    # 侧边栏
    with st.sidebar:
        st.header("📊 会话信息")

        # 统计
        col1, col2 = st.columns(2)
        with col1:
            st.metric("对话轮次", len(st.session_state.messages) // 2)
        with col2:
            st.metric("消息数", len(st.session_state.messages))

        st.markdown("---")

        # 功能按钮
        st.header("🔧 功能")

        if st.button("🗑️ 清除对话历史", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        if st.button("💾 导出对话", use_container_width=True):
            # 导出为文本
            chat_text = "\n\n".join(
                [
                    f"{msg['role'].upper()}: {msg['content']}"
                    for msg in st.session_state.messages
                ]
            )
            st.download_button(
                label="📥 下载对话记录",
                data=chat_text,
                file_name="chat_history.txt",
                mime="text/plain",
                use_container_width=True,
            )

        st.markdown("---")

        # 关于信息
        st.header("ℹ️ 关于")
        st.markdown(
            """
        **开发者**: ZA
        
        **技术栈**:
        - LangChain 0.3+
        - OpenAI GPT-3.5
        - Chroma DB
        - Streamlit
        
        **版本**: v1.0.0
        
        **GitHub**: [查看源码](#)
        """
        )

        st.markdown("---")

        # 免责声明
        st.markdown(
            """
        <div class="warning-box">
        <strong>⚠️ 免责声明</strong><br>
        本系统提供的信息仅供参考，不能替代专业医疗建议、诊断或治疗。
        使用任何药物前，请咨询医生或药师。
        </div>
        """,
            unsafe_allow_html=True,
        )

        # 环境信息（开发模式显示）
        if settings.app_env == "development":
            with st.expander("🔧 调试信息"):
                st.json(
                    {
                        "环境": settings.app_env,
                        "模型": settings.openai_model,
                        "日志级别": settings.log_level,
                        "会话消息数": len(st.session_state.messages),
                    }
                )


if __name__ == "__main__":
    main()
