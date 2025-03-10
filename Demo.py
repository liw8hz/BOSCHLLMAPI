import warnings
import time
from langchain.schema import HumanMessage, SystemMessage
from Bosch_langchain_llm import BoschChatLLM

# Suppress only the single InsecureRequestWarning from urllib3 needed
from urllib3.exceptions import InsecureRequestWarning
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time} seconds")
        return result
    return wrapper

prompt_template = "You are useful assistance. "

my_contents = "9.8和9.11哪个更大？"

@timeit
def main():
    tenant_id = "your tenant ID"
    oauth_data = {
        "client_id": "your oauth ID",
        "client_secret": "your secret here"
    }

    # LLM API 配置
    api_url = "https://aigc.bosch.com.cn/llmservice/api/v1/chat/messages"

    llm = BoschChatLLM(
        oauth2_client_id=oauth_data["client_id"],
        oauth2_client_secret=oauth_data["client_secret"],
        tenant_or_directory_id=tenant_id,
        api_url=api_url, 
        model_name="gpt4o-mini",        # 接口里使用的模型名称
        temperature=0.1,
        top_k=5,
        top_p=0.6
    )

    # 给模型发送一个 user 消息
    messages = [
        SystemMessage(content=prompt_template),
        HumanMessage(content=my_contents)
        ]
    
    # 打印回复
    result = llm.invoke(messages)
    print(result.content)

if __name__ == "__main__":
    main()