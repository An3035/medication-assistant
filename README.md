<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11"/>
  <img src="https://img.shields.io/badge/LangChain-1.0+-339933?style=for-the-badge&logo=chainlink&logoColor=white" alt="LangChain"/>
  <img src="https://img.shields.io/badge/Streamlit-1.40-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Chroma-0.5-FB542B?style=for-the-badge&logo=chromadb&logoColor=white" alt="Chroma"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="MIT"/>
</p>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=200&color=0:339933,50:4CAF50,100:2E7D32&text=💊%20Medication%20Assistant&fontSize=44&fontAlignY=35&fontColor=FFFFFF&section=header" width="100%"/>
</p>

<h2 align="center">智能用药安全助手 — RAG + LLM</h2>
<p align="center"><b>Intelligent Medication Safety Assistant</b></p>

<p align="center">
  基于 <b>RAG（检索增强生成）</b> 技术栈构建的智能用药助手。<br/>
  通过 <b>LangChain + Chroma + LLM</b> 实现药品信息查询、药物相互作用检测与个性化用药指导。
</p>

<p align="center">
  <a href="https://medication-assistant-6akrfyhd95rgxducxjpjsn.streamlit.app" target="_blank">
    <img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Streamlit App" width="180"/>
  </a>
</p>

<p align="center">
  <a href="#-功能特性">✨ 特性</a> &nbsp;|&nbsp;
  <a href="#-技术架构">🏗️ 架构</a> &nbsp;|&nbsp;
  <a href="#-快速开始">🚀 开始</a> &nbsp;|&nbsp;
  <a href="#-项目结构">📁 结构</a> &nbsp;|&nbsp;
  <a href="#-性能指标">📊 指标</a> &nbsp;|&nbsp;
  <a href="#-免责声明">⚖️ 声明</a>
</p>

<br/>

---

## 💡 项目背景

> 用药安全是关系到每个人健康的重要问题。特别是老年群体，常常同时服用多种药物，对药物相互作用的认知不足可能带来健康风险。

**Medication Assistant** 是一个个人学习项目，通过将 **大语言模型 (LLM)** 与 **私有知识库** 相结合，探索如何在医疗领域构建安全、可靠、智能的问答系统。

---

## ✨ 功能特性

| 功能 | 说明 |
|:----:|------|
| 💊 **药品信息查询** | 覆盖 <b>50+</b> 种常见药品，包含用法用量、副作用、禁忌症等 |
| ⚠️ **药物相互作用检测** | 智能识别多重用药风险，提前预警潜在药物冲突 |
| 🎯 **个性化用药指导** | 通俗易懂的用药建议，特别针对老年人友好的交互设计 |
| 💬 **自然对话交互** | 基于 Streamlit 构建的友好对话界面，像聊天一样获取信息 |

---

## 🏗️ 技术架构

```
用户提问: "阿莫西林和布洛芬能一起吃吗？"
        │
        ▼
┌─────────────────────────────┐
│  1. 向量检索 (Chroma)        │  ← 从知识库检索相关信息
│     语义相似度匹配药品文档    │
└────────────┬────────────────┘
             ▼
┌─────────────────────────────┐
│  2. 上下文构建               │  ← 拼接检索结果 + 用户问题
│     组成完整 Prompt          │
└────────────┬────────────────┘
             ▼
┌─────────────────────────────┐
│  3. LLM 生成回答             │  ← GPT-3.5 基于上下文回答
│     生成安全易读的答案        │
└────────────┬────────────────┘
             ▼
┌─────────────────────────────┐
│  4. 结果返回 → Streamlit UI  │  ← 展示给用户
└─────────────────────────────┘
```

### 🧩 技术栈

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,redis,fastapi,docker,git" />
</p>

| 技术 | 用途 |
|------|------|
| 🐍 **Python 3.11** | 主开发语言 |
| 🔗 **LangChain 1.0+** | RAG框架 · LLM链式调用 |
| 🎨 **Streamlit 1.40+** | Web交互界面 |
| 🗄️ **Chroma 0.5** | 向量数据库 · 语义检索 |
| 🧠 **OpenAI GPT-3.5** | 基础LLM模型 |
| ⚡ **FastAPI + Uvicorn** | RESTful API服务 |
| 🚀 **Redis 5.0+** | 缓存加速 |

---

## 🚀 快速开始

### 前置条件

- Python ≥ 3.11, < 3.13
- [uv](https://github.com/astral-sh/uv) 包管理器
- OpenAI API Key

### 安装 & 运行

```bash
# 1. 克隆仓库
git clone https://github.com/An3035/medication-assistant.git
cd medication-assistant

# 2. 安装依赖（使用 uv 加速）
uv sync

# 3. 设置环境变量
cp .env.example .env
# 编辑 .env 填入你的 OPENAI_API_KEY

# 4. 准备药品知识数据
uv run python scripts/prepare_data.py

# 5. 启动 Streamlit 应用
uv run streamlit run src/app.py

# 6. 在浏览器中访问 http://localhost:8501
```

### 运行测试

```bash
# 性能测试
uv run python tests/test_performance.py

# 功能测试
uv run pytest tests/
```

---

## 📁 项目结构

```
medication-assistant/
├── src/
│   ├── agents/                # Agent 核心逻辑
│   │   └── medication_agent.py # 用药智能体
│   ├── tools/                 # 工具函数集
│   ├── vectorstore/           # 向量数据库层
│   ├── utils/                 # 工具类
│   └── app.py                 # Streamlit 入口
├── data/                      # 药品数据
├── scripts/
│   └── prepare_data.py        # 数据预处理脚本
├── tests/
│   ├── test_performance.py    # 性能测试
│   └── ...
├── docs/                      # 文档
├── .devcontainer/             # 开发容器配置
├── .streamlit/                # Streamlit 配置
├── pyproject.toml             # 项目配置
└── uv.lock                    # 依赖锁定
```

---

## 📊 性能指标

| 指标 | 数值 |
|------|:----:|
| 🎯 **RAG 准确率** | **>85%** |
| ⚡ **平均响应时间** | **<3s** |
| 👥 **并发支持** | **100+** |
| 💊 **药品覆盖** | **50+** |

---

## 🗺️ 开发路线图

- [x] ✅ **Week 1-2**: RAG框架搭建 + Streamlit 部署上线
- [ ] 🔄 **Week 3-4**: 语音交互功能 + 商业化探索

---

## ⚠️ 免责声明

> ⚕️ **本系统提供的信息仅供参考，不能替代专业医疗建议。**
>
> - 如有用药疑问，请咨询专业医生或药师
> - 本系统不提供诊断服务
> - 紧急情况请拨打 120

---

## 📄 License

MIT © あん ([@An3035](https://github.com/An3035))

---

## 📬 联系

<p align="center">
  <a href="mailto:An3035@163.com">
    <img src="https://img.shields.io/badge/Email-An3035@163.com-EA4335?style=flat-square&logo=gmail&logoColor=white" />
  </a>
  <a href="https://github.com/An3035">
    <img src="https://img.shields.io/badge/GitHub-@An3035-181717?style=flat-square&logo=github&logoColor=white" />
  </a>
  <a href="https://an3035-github-io.vercel.app">
    <img src="https://img.shields.io/badge/Blog-技术博客-0E83CD?style=flat-square&logo=vercel&logoColor=white" />
  </a>
  <a href="https://medication-assistant-6akrfyhd95rgxducxjpjsn.streamlit.app">
    <img src="https://img.shields.io/badge/Demo-Live-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" />
  </a>
</p>

---

<p align="center">
  <b>💙 如果这个项目对你有帮助，请给一个 ⭐️</b>
</p>

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=An3035-medication-assistant&color=4CAF50&style=flat-square" alt="访问计数"/>
</p>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:2E7D32,50:4CAF50,100:81C784&section=footer" width="100%"/>
</p>
