from langchain.schema import HumanMessage, SystemMessage
from Bosch_langchain_llm import BoschChatLLM

def main():
    tenant_id = "0ae51e19-ssss-bbbb-wwww-648ee58410f4"
    oauth_data = {
        "client_id": "00eed4c4-zzzz-xxxx-b87e-8cea022e248c",
        "client_secret": "4Bk8Q~qNMZvtoJXXb1v_XDp~xV_giKEzWmKQHcaK"
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
        top_k=40,
        top_p=0.9
    )

    # 给模型发送一个 user 消息
    messages = [
        SystemMessage(content="请将以下内容从英文翻译成中文:"),
        HumanMessage(content="What did you say?")
        ]
    # 打印回复
    result = llm.invoke(messages)
    print(result.content)

if __name__ == "__main__":
    main()