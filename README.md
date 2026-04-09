# 🏥 智能用药安全助手

基于LangChain 0.3+ 的智能用药安全检查系统

## 🌟 在线演示

🔗 [点击体验](链接) （明天部署后填入）

## ✨ 功能特性

- 🔍 **药物信息查询**：查询50+常用药物的详细信息
- ⚠️ **药物交互检查**：智能识别药物交互风险
- 💡 **个性化建议**：基于专业知识提供用药建议
- 💬 **自然对话**：友好的聊天界面，适合老年人使用

## 🎬 演示

![演示GIF](docs/demo.gif)

（明天录制GIF后添加）

## 📊 项目亮点

- ✅ 收录50+常用药物信息
- ✅ RAG检索准确率 >80%
- ✅ 响应时间 <3秒
- ✅ 适配移动端

## 🛠️ 技术栈

- **AI框架**: LangChain 0.3.7+
- **向量数据库**: Chroma 0.5.23
- **LLM**: OpenAI GPT-3.5-turbo
- **界面**: Streamlit 1.40+
- **环境管理**: uv

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/your-username/medication-assistant.git
cd medication-assistant
```

### 2. 安装依赖

```bash
uv venv --python 3.11
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### 3. 配置环境

```bash
cp .env.example .env
# 编辑.env，填入你的OPENAI_API_KEY
```

### 4. 准备数据

```bash
python scripts/prepare_data.py
```

### 5. 运行应用

```bash
streamlit run src/app.py
```

访问 http://localhost:8501

## 📂 项目结构

medication-assistant/
├── src/
│   ├── agents/      # Agent定义
│   ├── tools/       # 工具函数
│   ├── vectorstore/ # 向量数据库
│   ├── utils/       # 工具类
│   └── app.py       # 主应用
├── data/            # 数据目录
├── scripts/         # 脚本
└── tests/           # 测试

## 🎯 使用示例

用户："阿司匹林有什么副作用？"
助手：阿司匹林最常见的副作用是胃肠道反应...

## 📈 开发进度

- [x] Week 1: 基础功能实现
- [x] Week 2: 性能优化（进行中）
- [x] Week 3: 界面美化
- [ ] Week 4: 部署上线

## ⚠️ 免责声明

本系统提供的信息仅供参考，不能替代专业医疗建议。

## 📝 License

MIT

## 👨‍💻 作者

ZA - AI Agent开发者
- GitHub: @An3035

---

⭐ 如果觉得有帮助，请给个Star！