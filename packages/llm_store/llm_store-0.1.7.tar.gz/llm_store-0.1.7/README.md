# Feature

- LLM 配置读取远程存储
- Prompt 配置读取远程存储
- LLM 对话记录 存储到远程
- 远程存储: 支持 Baserow
- 支持使用 Jinja2 模板渲染 Prompt

# 使用示例
```python
from llm_store.gateway import LLMGateway
from llm_store.store.baserowstore import BaseRowStore
import os

store = BaseRowStore(
    api_host=os.environ.get("BASEROW_API_HOST", "localhost"),
    api_key=os.environ.get("BASEROW_API_KEY", ""),
    db_code="3",
    model_table_code="614",
    prompt_table_code="308",
    chat_log_table_code="309")

llm_gateway = LLMGateway(store)
prompt_code = "system_blank"

# -- 获取 AI 模型
llm_model = llm_gateway.get_model(prompt_code)

# -- 渲染 Prompt
messages = llm_gateway.render_prompt(prompt_code, {"content": "你是谁"})

# -- 执行对话
chatCompletion = llm_gateway.completions(llm_model, messages, trace_id="1234567890")
print(chatCompletion)
``````

# 约定
## 内置Prompt_code
- system_blank: 格式为 {{content}} , 模型为小参数模型, 一般为 4o-mini
- system_blank_advanced: 格式为: {{content}},  模型为大参数模型, 一般为 4o