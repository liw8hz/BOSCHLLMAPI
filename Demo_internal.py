import warnings
from langchain.schema import HumanMessage, SystemMessage
from Bosch_langchain_llm import BoschChatLLM_internal
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

api_key = "sk-your api key here"
api_url = "https://blue-whale-msp.de.bosch.com/api/chat/completions"
model_name = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B"

prompt_template = "You are useful assistance."
my_contents = "请告诉我为什么地球在外太空看起来是蓝色的？"

def main():
    llm = BoschChatLLM_internal(
        api_key=api_key,
        api_url=api_url,
        model_name=model_name,
        temperature=0.1
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