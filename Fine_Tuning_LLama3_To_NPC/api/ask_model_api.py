import os
from dotenv import load_dotenv
from openai import OpenAI
from constants.available_models import AvailableModels
from constants.url import Open_Router_API_Url
from constants.sizes import Max_API_Context_Token_Per_Request

def ask_api_model(
    system_prompt: str = "",
    user_prompt: str = None, 
    n: int = 1, 
    model: AvailableModels = "meta-llama/llama-3.3-70b-instruct:free"
):
    if not user_prompt:
        raise Exception("Please provide a user prompt as the parameter of user_prompt")
    
    load_dotenv()
    __API_KEY = os.getenv("OPEN_ROUTER_API_KEY")
    if not __API_KEY:
        raise Exception("Missing environment variable of OPEN_ROUTER_API_KEY")
    
    client = OpenAI(
        base_url=Open_Router_API_Url,
        api_key=__API_KEY,
    )

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        n=n, 
        max_tokens=Max_API_Context_Token_Per_Request, 
        max_completion_tokens=Max_API_Context_Token_Per_Request, 
        # we skip the extra headers bcs we don't need it
    )
    
    return completion

def ask_api_model_with_key(
    api_key: str = None, 
    system_prompt: str = "",
    user_prompt: str = None, 
    n: int = 1, 
    model: AvailableModels = "meta-llama/llama-3.3-70b-instruct:free"
):
    if not api_key:
        raise Exception("Please provide a api key as the parameter of api_key")
    if not user_prompt:
        raise Exception("Please provide a user prompt as the parameter of user_prompt")
    
    client = OpenAI(
        base_url=Open_Router_API_Url,
        api_key=api_key,
    )

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        n=n, 
        max_tokens=Max_API_Context_Token_Per_Request, 
        max_completion_tokens=Max_API_Context_Token_Per_Request, 
        # we skip the extra headers bcs we don't need it
    )
    
    return completion