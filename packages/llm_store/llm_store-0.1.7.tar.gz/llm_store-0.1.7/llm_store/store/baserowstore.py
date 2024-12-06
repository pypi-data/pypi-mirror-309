from llm_store.store.basestore import BaseStore, ModelRecord,PromptRecord
from baserowsdk.client import Client
class BaseRowStore(BaseStore):
    client: Client

    def __init__(self, api_host, api_key,db_code, model_table_code, prompt_table_code, chat_log_table_code):
        self.api_host = api_host
        self.api_key = api_key
        self.model_table_code = model_table_code
        self.prompt_table_code = prompt_table_code
        self.chat_log_table_code = chat_log_table_code
        self.db_code = db_code

        self.client = Client(api_key=api_key, base_url=api_host)

    def get_model(self, prompt_code: str) -> ModelRecord:
        filters = {"filter_type":"AND","filters":[{"type":"equal","field":"code","value":prompt_code}],"groups":[]}
        prompt_datas = self.client.base(int(self.db_code)).table(self.prompt_table_code).rows(filters=filters)
        assert len(prompt_datas) == 1
        prompt_data = prompt_datas[0]

        api_style = prompt_data.api_style[0]['value']['value']
        api_base = prompt_data.api_base[0]['value']
        api_key = prompt_data.api_key[0]['value']
        model_name = prompt_data.model_name[0]['value']
        model_config = prompt_data.model_config[0]['value']

        rtn = ModelRecord(
                api_base=api_base,
                api_key=api_key,
                code=prompt_data.code,
                model_name=model_name,
                api_style=api_style,
                config=model_config)

        return rtn
   
   
    def get_prompt(self, code: str) -> PromptRecord:
        filters = {"filter_type":"AND","filters":[{"type":"equal","field":"code","value":code}],"groups":[]}
        model_data = self.client.base(self.db_code).table(self.prompt_table_code).rows(filters=filters)
        assert len(model_data) == 1 
        row = model_data[0]
        
        model = ModelRecord(
                api_base=row.api_base[0]['value'],
                api_key=row.api_key[0]['value'],
                code=row.code,
                model_name=row.model_name[0]['value'],
                api_style=row.api_style[0]['value']['value'],
                config=row.config[0]['value'] if row.config else None)
        

        rtn = PromptRecord(
            code =row.code,
            system_prompt=row.system_prompt,
            user_prompt=row.user_prompt,
            temperature=row.temperature,
            model = model,
            id = row.id
        )
        rtn.api_style = model.api_style
        return rtn
     
    
    def save_chatlog(self, fields:dict):
        return self.client.base(int(self.db_code)).table(self.chat_log_table_code).create(fields)
