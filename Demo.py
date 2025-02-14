import warnings
from langchain.schema import HumanMessage, SystemMessage
from Bosch_langchain_llm import BoschChatLLM

# Suppress only the single InsecureRequestWarning from urllib3 needed
from urllib3.exceptions import InsecureRequestWarning
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

def main():
    tenant_id = "0ae51e19-aaaa-bbbb-cccc-648ee58410f4"
    oauth_data = {
        "client_id": "00eed4c4-xxxx-yyyy-b87e-8cea022e248c",
        "client_secret": "xxxxx"
    }

    # LLM API 配置
    api_url = "https://aigc.bosch.com.cn/llmservice/api/v1/chat/messages"

    llm = BoschChatLLM(
        oauth2_client_id=oauth_data["client_id"],
        oauth2_client_secret=oauth_data["client_secret"],
        tenant_or_directory_id=tenant_id,
        api_url=api_url, 
        model_name="deepseek-r1",        # 接口里使用的模型名称
        temperature=0.6,
        top_k=5,
        top_p=0.6
    )

    # 给模型发送一个 user 消息
    messages = [
        SystemMessage(content="请回答如实回答下面的问题，不能有臆造和不实的信息："),
        HumanMessage(content="假设有一个池塘，里面有无穷多的水。现有2个空水壶，容积分别为5升和6升。问题是如何只用这2个水壶从池塘里取得3升的水。")
        ]
    # 打印回复
    result = llm.invoke(messages)
    print(result.content)

if __name__ == "__main__":
    main()