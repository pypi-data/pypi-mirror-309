from abc import ABC, abstractmethod

# LLM对象
class ModelRecord:
    code: str
    api_base: str
    api_key: str
    model_name: str
    api_style: str
    config:str

    def __init__(self, api_base, api_key, code, model_name, api_style, config):
        self.api_base = api_base
        self.api_key = api_key
        self.code = code
        self.model_name = model_name
        self.api_style = api_style
        self.config = config

    def __str__(self):
        return f'{self.api_base}:{self.api_key}:{self.model_name}:{self.api_style}'

# 提示词对象
class PromptRecord:
    code: str
    system_prompt: str
    user_prompt:str 
    temperature: float
    model: ModelRecord
    api_style: str
    id: int

    def __init__(self, code, system_prompt, user_prompt, temperature, model, id):
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.temperature = temperature
        self.model = model
        self.code = code
        self.id = id

# 聊天记录对象
class ChatRecord:
    trace_id: str
    prompt:str  
    completion:str 
    model:str 
    prompt_tokens:int
    completion_tokens:int
    response_s:float
    cached_tokens:int

    auto_id:int
    created_at:str

    def __init__(self, trace_id, prompt, completion, model, prompt_tokens, completion_tokens, response_s, cached_tokens):
        self.trace_id = trace_id
        self.prompt = prompt
        self.completion = completion
        self.model = model
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.response_s = response_s
        self.cached_tokens = cached_tokens

class BaseStore(ABC):
    api_host: str
    api_key: str
    db_code: str
    model_table_code: str
    prompt_table_code: str
    chat_log_table_code: str
    
    @abstractmethod
    def get_model(self, code: str) -> ModelRecord:
        """_summary_

        Args:
            code (str): _description_

        Returns:
            PromptRecord: _description_
        """
        pass

    @abstractmethod
    def get_prompt(self, code: str) -> PromptRecord:
        """获取提示词模板配置
        
        Args:
            code: 模板名称
            
        Returns:
            dict: 模板配置信息，包含 prompt 等
        """
        pass

    @abstractmethod
    def save_chatlog(self, fields:dict):
        """保存聊天记录
        
        Args:
            chat_data: 聊天记录数据
            
        Returns:
            bool: 保存是否成功
        """
        pass