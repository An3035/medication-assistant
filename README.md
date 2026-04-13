# 🏥 智能用药安全助手

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://medication-assistant-6akrfyhd95rgxducxjpjsn.streamlit.app)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 基于 LangChain 0.3+ 和 RAG 架构的智能用药安全检查系统

## 🌟 在线演示

🔗 **[立即体验](https://medication-assistant-6akrfyhd95rgxducxjpjsn.streamlit.app)**

## ✨ 核心功能

- 🔍 **药物信息查询**：覆盖50+常用药物的详细信息
- ⚠️ **药物交互检查**：智能识别用药风险
- 💡 **个性化建议**：通俗易懂的用药指导
- 💬 **自然对话**：适合老年人的友好界面

## 📊 技术指标

| 指标 | 数值 |
|------|------|
| 药物数量 | 50+ |
| RAG准确率 | >85% |
| 平均响应时间 | <3秒 |
| 并发支持 | 100+ |

## 🛠️ 技术栈

- **AI框架**: LangChain 0.3.7+
- **向量数据库**: Chroma 0.5.23
- **LLM**: OpenAI GPT-3.5-turbo
- **界面**: Streamlit 1.40+
- **语言**: Python 3.11

## 🚀 本地运行

### 1. 克隆项目
```bash
git clone https://github.com/An3035/medication-assistant.git
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
# 编辑 .env，填入你的 API_KEY
```

### 4. 准备数据
```bash
python scripts/prepare_data.py
```

### 5. 运行
```bash
streamlit run src/app.py
```

## 📂 项目结构
medication-assistant/
├── src/
│   ├── agents/          # Agent核心逻辑
│   ├── tools/           # 工具函数
│   ├── vectorstore/     # 向量数据库
│   ├── utils/           # 工具类
│   └── app.py           # Streamlit应用
├── data/                # 数据文件
├── scripts/             # 脚本
├── tests/               # 测试
└── docs/                # 文档

## 🎯 项目亮点

### 技术亮点
- ✅ 基于RAG架构，准确率>85%
- ✅ 混合检索策略（规则引擎+LLM）
- ✅ 响应时间优化至<3秒
- ✅ 实现查询缓存机制
- ✅ 完整的日志系统

### 业务价值
- ✅ 解决老年人用药安全痛点
- ✅ 适配老年人使用习惯
- ✅ 可扩展至养老机构
- ✅ 支持移动端访问

## 📈 开发进度

- [x] Week 1: 基础RAG实现
- [x] Week 2: 性能优化 + 部署
- [ ] Week 3: 功能扩展（语音交互）
- [ ] Week 4: 商业化探索

## 🧪 测试

```bash
# 性能测试
python tests/test_performance.py

# 功能测试
pytest tests/
```

## 🤝 贡献

欢迎提Issue和PR！

## ⚠️ 免责声明

本系统提供的信息仅供参考，不能替代专业医疗建议、诊断或治疗。

## 📄 License

MIT © あん

## 👨‍💻 作者

**あん** - AI应用开发者

- GitHub: [@あん](https://github.com/An3035)
- Email: zhangan3035@163.com

---

⭐ 如果觉得有帮助，请给个Star！