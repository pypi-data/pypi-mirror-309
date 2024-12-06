from typing import Dict, TypedDict, Optional
from .prompt import PromptManager


class ConfigDict(TypedDict):
    api_key: str
    env: str
    bypass: Optional[bool]


class PromptStudio(PromptManager):
    """
    Main client class for PromptStudio SDK
    Inherits all functionality from PromptManager
    """

    def __init__(self, config: ConfigDict):
        """
        Initialize the PromptStudio client

        Args:
            config: Dictionary containing:
                - 'api_key': API key
                - 'env': Environment ('test' or 'prod')
                - 'bypass': Optional boolean to bypass PromptStudio server
        """
        super().__init__(config)

    async def chat_with_prompt(self, *args, **kwargs):
        """
        Async wrapper for chat_with_prompt
        """
        return await super().chat_with_prompt(*args, **kwargs)

    async def get_folder_prompts(self, *args, **kwargs):
        """
        Async wrapper for get_folder_prompts
        """
        return await super().get_folder_prompts(*args, **kwargs)

    async def get_all_prompts(self, *args, **kwargs):
        """
        Async wrapper for get_all_prompts
        """
        return await super().get_all_prompts(*args, **kwargs)
