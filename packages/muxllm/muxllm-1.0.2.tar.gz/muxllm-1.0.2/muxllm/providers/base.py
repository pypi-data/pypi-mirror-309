from pydantic import BaseModel
import json

class ModelNotAvailable(Exception):
    pass

class ToolCall(BaseModel):
    id: str
    name: str
    args: dict[str, str]

class ToolResponse(BaseModel):
    id: str
    name: str
    response: str

class LLMResponse(BaseModel):
    model: str
    raw_response: dict | object # raw response from the provider. Ideally dict, but google uses protobuf natively
    message: str | None
    tools: list[ToolCall] | None

class BaseProvider:
    def __init__(self):
        pass

    def parse_system_message(self, message : str) -> dict:
        pass

    def parse_user_message(self, message : str) -> dict:
        pass

    def parse_response(self, response: LLMResponse) -> dict:
        pass

    def parse_tool_response(self, tool_resp: ToolResponse) -> dict:
        pass

    def get_response(self, messages : list[dict[str, str | dict]], model : str, **kwargs) -> LLMResponse:
        pass

    async def get_response_async(self, messages : list[dict[str, str | dict]], model : str, **kwargs) -> LLMResponse:
        pass

    # def get_response_stream(self, messages : list[dict[str, str]], model : str, **kwargs):
    #     pass

class CloudProvider(BaseProvider):
    def __init__(self, model_alias : dict[str, str]):
        self.model_alias = model_alias
        self.client = None
        self.async_client = None

    def validate_model(self, model : str): 
        if model in self.model_alias:
            model = self.model_alias[model]
        return model
    
    def parse_system_message(self, message : str) -> dict:
        return {
            "role": "system",
            "content": message
        }
    
    def parse_user_message(self, message : str) -> dict:
        return {
            "role": "user",
            "content": message
        }
    
    def parse_response(self, response: LLMResponse) -> dict:
        msg = {
            "role": "assistant",
            "content": response.message if response.message else "",
        }
        if response.tools:
            msg["tool_calls"] = [
                {
                    "id": tool.id,
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "arguments": json.dumps(tool.args)
                    }
                } for tool in response.tools if response.tools is not None
            ]

        return msg
    
    def parse_tool_response(self, tool_resp: ToolResponse) -> dict:
        return {
            "role": "tool",
            "tool_call_id": tool_resp.id,
            "name": tool_resp.name,
            "content": tool_resp.response
        }

    def get_response(self, messages : list[dict[str, str | dict]], model : str, **kwargs) -> LLMResponse:
        model = self.validate_model(model)
        
        response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    **kwargs) 
        message = response.choices[0].message

        resp = LLMResponse(model=model, raw_response=dict(response), message=message.content, tools=[
                            ToolCall(id=message.tool_calls[i].id, name=message.tool_calls[i].function.name, args=json.loads(message.tool_calls[i].function.arguments))
                                for i in range(len(message.tool_calls))] if message.tool_calls else None)
        return resp
    
    async def get_response_async(self, messages : list[dict[str, str | dict]], model : str, **kwargs) -> LLMResponse:
        model = self.validate_model(model)

        response = await self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    **kwargs) 
        message = response.choices[0].message
        resp = LLMResponse(model=model, raw_response=dict(response), message=message.content, tools=[
                    ToolCall(id=message.tool_calls[i].id, name=message.tool_calls[i].function.name, args=json.loads(message.tool_calls[i].function.arguments))
                        for i in range(len(message.tool_calls))] if message.tool_calls else None)
        return resp
    
    # def get_response_stream(self, messages : list[dict[str, str]], model : str, **kwargs):
    #     model = self.validate_model(model)
        
    #     response = self.client.chat.completions.create(
    #                 model=model,
    #                 messages=messages,
    #                 **kwargs) 
        
    #     for chunk in response:
    #         yield LLMResponse(model=model, raw_response=chunk, message=chunk.choices[0].delta.content, tool=chunk.choices[0].delta.tools)


