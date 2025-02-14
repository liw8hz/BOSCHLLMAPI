# Bosch AI Chat LLM

该项目主要帮助用户快速上手Bosch BD提供的LLM API，写一个封装好的demo接口代码。

- **API 调用逻辑 (`Bosch_llm_api_call.py`)**  
  负责处理获取 Token、发送 Chat 请求等底层交互。  
- **LangChain 自定义模型 (`Bosch_langchain_llm.py`)**  
  继承自 `BaseChatModel`，通过 `PrivateAttr` 引入 API 客户端对象，封装成可在 LangChain 中使用的 LLM。

## 目录结构

```plaintext
main/
├── Bosch_llm_api_call.py        # 封装了实际的 API 调用和 Token 获取
├── Bosch_langchain_llm.py       # 继承 LangChain BaseChatModel 的自定义 LLM
├── Demo.py                    # 演示如何使用自定义 LLM
└── README.md                  # 项目说明文档
```
# 依赖
- Python 3.8+
- requests
- pydantic
- langchain

示例安装命令

pip install requests pydantic langchain

# Quick Start

配置你的 Azure AD / API 信息
在 Demo.py（或类似脚本）里，填写正确的 oauth2_client_id, oauth2_client_secret, tenant_or_directory_id（通常是租户 ID 或 GUID），以及调用的 api_url（通常为聊天接口地址）。

# 许可证
示例代码可参考 MIT 开源协议使用和修改。

# History
2025.02.14: Updated code for deepseek-v3 and deepseek-R1, add reasoning thinking content if module is deepseek-R1

