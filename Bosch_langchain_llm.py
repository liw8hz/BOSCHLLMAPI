from typing import List, Optional, Any, Dict
import logging

import requests
from pydantic import PrivateAttr
from langchain.chat_models.base import BaseChatModel
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    ChatGeneration,
    ChatResult,
    BaseMessage
)

from Bosch_llm_api_call import BoschApiClient

logger = logging.getLogger(__name__)

class BoschChatLLM(BaseChatModel):
    """
    Custom Chat LLM Compatible with LangChain
    
    How to use：
    
    >>> from Bosch_langchain_llm import BoschChatLLM
    >>> llm = BoschChatLLM(
    ...     oauth2_client_id="xxx",
    ...     oauth2_client_secret="yyy",
    ...     tenant_or_directory_id="zzz",
    ...     api_url="https://aigc.bosch.com.cn/llmservice/api/v1/chat/messages",
    ...     model_name="gpt4o-mini",
    ...     temperature=0.1
    ... )
    >>> messages = [HumanMessage(content="Who are you?")]
    >>> result = llm.invoke(messages)
    >>> print(result.content)
    """
    # Use Pydantic's PrivateAttr to store internal fields that do not require model validation/serialization.
    _client: BoschApiClient = PrivateAttr()

    def __init__(
        self,
        oauth2_client_id: str,
        oauth2_client_secret: str,
        tenant_or_directory_id: str,
        api_url: str,
        model_name: str = "gpt4o-mini",
        temperature: float = 0.1,
        **kwargs: Any
    ):
        
        # Allow Pydantic (LangChain's BaseChatModel) to perform standard initialization first.
        super().__init__(**kwargs)

        # Use `object.__setattr__` to assign values to private attributes, avoiding conflicts with Pydantic fields.
        object.__setattr__(
            self,
            "_client",
            BoschApiClient(
                oauth2_client_id=oauth2_client_id,
                oauth2_client_secret=oauth2_client_secret,
                tenant_or_directory_id=tenant_or_directory_id,
                api_url=api_url,
                model_name=model_name,
                temperature=temperature
            )
        )

    @property
    def _llm_type(self) -> str:
        """
        Returns an identifier to distinguish between different types of LLMs.
        """
        return "Bosch_ai_llm"

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any
    ) -> ChatResult:
        """
        Core message generation logic: pass in a list of ChatMessage objects, call the custom API to get a response.
        Returns a ChatResult as defined in LangChain.
        """

        # 1. Convert LangChain's message format to the API's required format:
        #    LangChain: SystemMessage/HumanMessage/AIMessage ...
        #    API requires: {"role": "user", "content": "..."} or {"role": "assistant", "content": "..."} etc.
        transformed_messages = []
        for m in messages:
            if isinstance(m, HumanMessage):
                role = "user"
            elif isinstance(m, AIMessage):
                role = "assistant"
            elif isinstance(m, SystemMessage):
                role = "system"
            else:
                role = "user"  # fallback
            transformed_messages.append({"role": role, "content": m.content})

        try:
            # 2. call actual API
            response_json = self._client.chat(transformed_messages)
            # The successful response format from the API is:
            # {
            #   "msg": "Operation Success",
            #   "code": 200,
            #   "data": {
            #       "messages": [
            #           {"role": "assistant", "content": "..."}
            #       ]
            #   }
            # }
            assistant_content = ""
            if (
                response_json
                and "data" in response_json
                and isinstance(response_json["data"], dict)
                and "messages" in response_json["data"]
                and len(response_json["data"]["messages"]) > 0
            ):
                # Get the first assistant message is OK
                for item in response_json["data"]["messages"]:
                    if item.get("role") == "assistant":
                        assistant_content = item.get("content", "")
                        break

            # 3. Wrap the results into LangChain's ChatResult:
            #    ChatGeneration can be understood as an object representing "a single chat generation."
            #    ChatResult.generations is a list containing ChatGeneration objects.
            #    ChatGeneration includes an AIMessage.
            ai_message = AIMessage(content=assistant_content)
            generation = ChatGeneration(message=ai_message)
            print(f"[DEBUG msg] : msg: {response_json['msg']} || code:{response_json['code']}")
            return ChatResult(generations=[generation])

        except requests.exceptions.RequestException as e:
            logger.exception("Error calling BoschAI Chat API: %s", e)
            # Custom error handling can be implemented as needed.
            ai_message = AIMessage(content="(Error: Unable to get response from BoschAI.)")
            generation = ChatGeneration(message=ai_message)
            return ChatResult(generations=[generation])