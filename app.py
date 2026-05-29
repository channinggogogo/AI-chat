import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

#页面配置
st.set_page_config(page_title="我的 AI 助手", page_icon="🤖")
st.title("🤖 我的 AI 助手")


# ✅ 必须在使用之前定义 model_map
model_map = {
    "DeepSeek（国内推荐）": ["deepseek-chat", "deepseek-reasoner"],
    "智谱 GLM（免费额度）": ["glm-4-flash", "glm-4-plus"],
    "OpenAI": ["gpt-4o-mini", "gpt-4o"],
    "Claude": ["claude-haiku-4-5-20251001", "claude-sonnet-4-6-20250514"]
}

# ✅ 必须在使用之前定义 prices
prices = {
    "deepseek-chat": {"input": 0.14, "output": 0.28},
    "deepseek-reasoner": {"input": 0.55, "output": 2.19},
    "glm-4-flash": {"input": 0, "output": 0},
    "glm-4-plus": {"input": 0.7, "output": 0.7},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o": {"input": 2.50, "output": 10.0},
    "claude-haiku-4-5-20251001": {"input": 0.25, "output": 1.25},
    "claude-sonnet-4-6-20250514": {"input": 3.0, "output": 15.0},
}



#API客户端#
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),base_url="https://api.deepseek.com/v1")

# 侧边栏：参数设置
with st.sidebar:
    st.header("⚙️ 参数设置")
    
    # System Prompt
    system_prompt = st.text_area(
        "System Prompt（AI 的人设）",
        value="你是一个友好的 AI 助手，乐于帮助用户解决问题。",
        height=100
    )

    # AI 服务商选择
    provider = st.selectbox(
        "AI 服务商",
        options=["DeepSeek（国内推荐）", "智谱 GLM（免费额度）", "OpenAI", "Claude"],
        index=0,
        help="国内用户推荐 DeepSeek 或智谱 GLM，无需代理"
    )
    model = st.selectbox("模型", options=model_map[provider])


    # Temperature 滑块
    temperature = st.slider(
        "Temperature（创造性）",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="0 = 确定保守，1 = 创意随机"
    )

    st.image(
        r"E:\360MoveData\Users\liuch\Desktop\Claude\AI\my-first-ai-app\AI温度调节滑块电影写真.png",  # 你的图片地址
        caption="调这个滑块就像调收音机——往左拧，AI 像个老学究，每句话都一丝不苟（temperature=0）；往右拧，AI 开始放飞自我，天马行空什么话都敢说（temperature=1）。日常使用推荐 0.3-0.7 之间，既有料又不离谱。",
    )

    # Max tokens
    max_tokens = st.slider("最大回复长度（tokens）",min_value=50,max_value=2000,value=500,step=50)
    
    # 显示当前设置
    st.divider()
    st.caption(f"当前温度：{temperature}")
    st.caption(f"最大长度：{max_tokens} tokens")
    st.caption("💰 费用估算（非常粗略）")

    model_price = prices.get(model, {"input": 0, "output": 0})


# 对话历史管理
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# 显示历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 用户输入
if prompt := st.chat_input("输入你的问题..."):
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 构建 API 请求的 messages
    # System prompt 作为第一条 system 消息
    api_messages = []
    for msg in st.session_state.messages:
        api_messages.append({"role": msg["role"], "content": msg["content"]})
    
    # 调用 API
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                response = client.chat.completions.create(model=model,max_tokens=max_tokens,temperature=temperature,messages=api_messages)
                ai_reply = response.choices[0].message.content
                st.markdown(ai_reply)
                
                # 显示 token 用量
                usage = response.usage
                input_tokens = usage.prompt_tokens
                output_tokens = usage.completion_tokens
                
                price = prices[model]
                cost = (input_tokens * price["input"] + output_tokens * price["output"]) / 1_000_000
                
                st.caption(f"📊 输入：{input_tokens} tokens · "f"输出：{output_tokens} tokens · "f"本次费用：${cost:.6f}")
                
                # 保存 AI 回复
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                
            except Exception as e:
                st.error(f"出错了：{e}")
                st.caption("检查 API Key 是否正确、账户余额是否充足")