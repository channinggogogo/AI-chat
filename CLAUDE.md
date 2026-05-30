# 我的 AI 助手 — AI Chat App

## 项目概述

基于 Streamlit 的 AI 聊天应用，支持多模型对话、参数调节、Token 用量统计。

## 技术栈

- **框架**: Streamlit 1.57
- **API 客户端**: openai (OpenAI SDK) — 通过兼容接口连接 DeepSeek
- **认证**: DeepSeek API Key（存储在 Streamlit Cloud Secrets / .env）
- **Python**: 3.12

## 文件结构

```
app.py              # 主程序 — Streamlit 聊天应用（唯一入口）
test_api_openai.py   # CLI 测试脚本（非部署文件）
requirements.txt     # 依赖: streamlit, openai, anthropic, python-dotenv
AI温度调节滑块电影写真.png  # 侧边栏配图 (4.5MB)
```

## 部署

- **平台**: Streamlit Community Cloud
- **GitHub**: `channinggogogo/AI-chat` (main 分支)
- **原始仓库**: `a328605822-max/AI-chat`
- **入口文件**: `app.py`
- **Secrets**: `DEEPSEEK_API_KEY`（在 Streamlit Cloud Dashboard → Settings → Secrets 中配置）
- **自动部署**: 推送 `main` 分支到 `channinggogogo/AI-chat`，Streamlit Cloud 自动重新部署

## 关键实现细节

### API 客户端（写死 DeepSeek）

```python
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com/v1")
```

客户端只连 DeepSeek，UI 中的 OpenAI/Claude/GLM 选项只是按静态价格表计价显示，**不会切换实际的 API 端点**。

### DeepSeek 模型

| 实际 API 中使用的名称 | 底层映射 | 说明 |
|---|---|---|
| `deepseek-chat` | → `deepseek-v4-flash` (non-thinking) | 旧名称，2026-07-24 下线 |
| `deepseek-reasoner` | → `deepseek-v4-flash` (thinking) | 旧名称，2026-07-24 下线 |

可用新模型: `deepseek-v4-flash` (快速，$0.14/M in)、`deepseek-v4-pro` (高性能，$0.435/M in)。所有 DeepSeek 模型都是纯语言模型，**无内置联网搜索**。V4 系列支持 Tool Calling，需要应用层实现搜索工具。

### 对话历史管理

- `st.session_state.messages` 存完整对话（含 system prompt）
- 显示时跳过 `role == "system"` 的消息（修复了移动端布局异常 Bug）
- system prompt 仍然发送给 API，只是不在 UI 中渲染

### 已知修复

1. **图片路径**: 从 Windows 绝对路径 `r"E:\...\AI温度调节滑块电影写真.png"` 改为相对路径 `"AI温度调节滑块电影写真.png"`（云端 Linux 兼容）
2. **移动端 AI 回复不可见**: 修复了 system 角色消息被当作聊天消息显示，导致 iPhone Safari 渲染布局异常

### 联网搜索

DeepSeek V4 模型支持 Tool Calling，可以通过实现搜索工具（如 DuckDuckGo）间接联网。目前未实现，AI 只能用训练截止日期之前的知识。

## 依赖

```
streamlit
openai
anthropic
python-dotenv
```
