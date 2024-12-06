from openai import OpenAI
from openai.types.chat import ChatCompletion
from llm_store.store.basestore import BaseStore, PromptRecord, ModelRecord
from llm_store.store.baserowstore import BaseRowStore
import time
from jinja2 import Environment


class LLMGateway:
    store: BaseStore

    def __init__(self, store: BaseStore):
        self.store = store

    def _get_llm_client(self, model: ModelRecord):
        """获取LLM客户端
        """
        if model.api_style == "openai":
            return OpenAI(
                base_url=model.api_base,
                api_key=model.api_key
            )
        else:
            raise ValueError(f"Unsupported API style: {model}")

    def get_model(self, model_code: str) -> ModelRecord:
        return self.store.get_model(model_code)

    def get_client(self, model: ModelRecord) -> OpenAI:
        return self._get_llm_client(model)

    def completions(self, model: ModelRecord, messages, is_save_log=True, trace_id=None, prompt_record_id=None, **kwargs):
        llm_client = self._get_llm_client(model)
        start_time = time.time()
        chatCompletion = llm_client.chat.completions.create(messages=messages, model=model.model_name,
                                                            **kwargs)
        end_time = time.time()
        response_cost = round(end_time - start_time, 2)

        if is_save_log:
            log_record =self.save_log(
                messages= messages,
                model =model,
                chatCompletion= chatCompletion,
                time_cost = response_cost,
                traceid = trace_id,
                prompt_record_id = prompt_record_id
            )
            print("save baserow chat log:"+  str(log_record.id))

        return chatCompletion

    def render_prompt(self, prompt_code: str, params={}) -> tuple[ModelRecord, PromptRecord, list[dict]]:
        # 获取 Prompt 记录
        prompt = self.store.get_prompt(prompt_code)

        # 渲染参数
        env = Environment(
            trim_blocks=True,  # 去掉行尾的空白字符
            lstrip_blocks=False  # 去掉行首的空白字符
        )

        system_template = env.from_string(prompt.system_prompt)
        render_system_prompt = system_template.render(params)

        messages = [{"role": "system", "content": render_system_prompt}]
        if prompt.user_prompt:
            user_template = env.from_string(prompt.user_prompt)
            render_user_prompt = user_template.render(params)

            messages.append({"role": "user", "content": render_user_prompt})

        return messages

    def save_log(self, messages, model: ModelRecord,chatCompletion: ChatCompletion,time_cost:float, traceid: str, prompt_record_id: int = None):
        content_str = "----".join(message['content'] for message in messages)

        cached_token = None
        if 'prompt_tokens_details' in chatCompletion.usage:
            cached_token = chatCompletion.usage.prompt_tokens_details.cached_tokens

        fields = {
            "prompt": content_str,
            "completion": chatCompletion.choices[0].message.content,
            "model": model.model_name,
            "prompt_tokens": chatCompletion.usage.prompt_tokens,
            "completion_tokens": chatCompletion.usage.completion_tokens,
            "response_s": time_cost,
            "cached_tokens": cached_token,
            "trace_id": traceid
        }

        if prompt_record_id:
            fields['prompt_record'] = [prompt_record_id]

        return self.store.save_chatlog(fields)


if __name__ == "__main__":
    store = BaseRowStore(
        api_host="https://aiadmin.yucekj.com",
        api_key="Zfsk1r7M7FyMw9qRjAZcPxkTLVy3x8U7",
        db_code="3",
        model_table_code="614",
        prompt_table_code="308",
        chat_log_table_code="309")
    llm_gateway = LLMGateway(store)

    # 标准使用模式
    # -- 渲染 Prompt
    # prompt_code = "test_template"
    # model_record, prompt_record, messages = llm_gateway.render_prompt(prompt_code, {"topic": "科幻"})
    #
    # # -- 对话
    # chatCompletion, time_cost = llm_gateway.completions(model_record, messages)
    # print(chatCompletion, time_cost)
    #
    # # -- 保存对话记录
    # trace_id = "1234567890"
    # log = llm_gateway.save_log(trace_id, model_record, prompt_record.id)
    # print(log)

    # 不使用远程 Prompt 模式
    messages = [{"role": "system", "content": "今天星期几"}]

    # -- 获取 模型信息
    model_code = "litellm-us"
    model_record = llm_gateway.get_model(model_code)

    # -- 执行对话
    chatCompletion, time_cost = llm_gateway.completions(model_record,messages)

    # -- 保存日志
    trace_id = "1234567890"
    log = llm_gateway.save_log(messages, model_record, traceid=trace_id)
    print(log)


