from typing import Dict, Any, List, Union, Optional, Tuple

import requests
import logging
import uuid
import json
from datetime import datetime
from .base import Base
from .cache import CacheManager, InteractionCacheManager
import os
import hashlib
import tempfile
from pathlib import Path
import mimetypes
from bson import ObjectId

from openai import OpenAI
import openai

import anthropic
import google.generativeai as genai
from google.ai import generativelanguage as glm
from google.generativeai import types as generation_types

from google.ai.generativelanguage_v1beta.types import content
import httpx
import base64

import pickle

PROMPT_TO_GENERATE_SUMMARIZED_CONTENT = "Summarize the above conversation in a detailed, concise, and well-structured manner. ensuring the summary does not exceed 250 words. Capture the key points and context, including important questions, answers, and relevant follow-up, while avoiding unnecessary repetition. Present the summary in a well-structured paragraph, focusing on the most important content exchanged"

# import openai

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="\n%(asctime)s - %(name)s - %(levelname)s - %(message)s\n",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True,  # This ensures our configuration takes precedence
    handlers=[logging.StreamHandler()],  # This ensures output goes to console
)
logger = logging.getLogger(__name__)


class PromptManager(Base):
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        # Set up persistent cache directory
        self.cache_dir = Path("./persistent_cache")
        self.cache_dir.mkdir(exist_ok=True)
        # logger.info(f"Using persistent cache directory: {self.cache_dir}")

    def _get_cache_path(self, cache_key: str) -> Path:
        """Get path for cache file"""
        return self.cache_dir / f"{cache_key}.pkl"

    def _save_to_persistent_cache(self, cache_key: str, data: Dict):
        """Save data to persistent cache"""
        try:
            cache_path = self._get_cache_path(cache_key)
            with open(cache_path, "wb") as f:
                pickle.dump(data, f)
            # logger.info(f"Saved to persistent cache: {cache_key}")
        except Exception as e:
            logger.error(f"Error saving to persistent cache: {str(e)}")

    def _load_from_persistent_cache(self, cache_key: str) -> Optional[Dict]:
        """Load data from persistent cache"""
        try:
            cache_path = self._get_cache_path(cache_key)
            if cache_path.exists():
                with open(cache_path, "rb") as f:
                    data = pickle.load(f)
                # logger.info(f"Loaded from persistent cache: {cache_key}")
                return data
        except Exception as e:
            logger.error(f"Error loading from persistent cache: {str(e)}")
        return None

    def _print_persistent_cache_contents(self):
        """Print contents of persistent cache"""
        # logger.info("\n=== Persistent Cache Contents ===")
        cache_files = list(self.cache_dir.glob("*.pkl"))
        if not cache_files:
            logger.info("Persistent cache is empty")
        for cache_file in cache_files:
            try:
                with open(cache_file, "rb") as f:
                    data = pickle.load(f)
                logger.info(f"Cache key: {cache_file.stem}")
                logger.info(f"Cache data: {data}")
            except Exception as e:
                logger.error(f"Error reading cache file {cache_file}: {str(e)}")

    async def get_all_prompts(self, folder_id: str) -> Dict:
        """
        Get all prompts for a given folder

        Args:
            folder_id: ID of the folder

        Returns:
            Dictionary containing prompt versions
        """
        response = await self._request(f"/{folder_id}")
        return response

    async def windowmemory_save_log_ai_interaction_prompt(
        self,
        user_prompt_id: str,
        interaction_request: Dict,
    ) -> Dict:
        """Process and save AI interaction using window memory cache"""
        try:

            # Generate session_id if not present
            session_id = interaction_request.get("session_id") or str(uuid.uuid4())

            # Print initial cache state
            # logger.info("Initial cache state:")
            CacheManager.print_cache_contents()
            InteractionCacheManager.print_cache_contents()

            # Get version (either from request or fetch latest)
            version = interaction_request.get("version")
            cache_key = f"{user_prompt_id}_{session_id}"
            prompt_details = CacheManager.get_prompt_details(cache_key)

            if not prompt_details:
                # Fetch and cache if not found
                prompt_details = await self._fetch_and_cache_prompt_details(
                    user_prompt_id, session_id, version
                )
                # logger.info(f"Cached new prompt details for {cache_key}")
            logger.info(
                f"windowmemory_save_log_ai_interaction_prompt  prompt_details ssssssss: {prompt_details}"
            )

            # First fetch and cache prompt details
            cache_key = f"{user_prompt_id}_{session_id}"
            prompt_details = CacheManager.get_prompt_details(cache_key)

            if not prompt_details:
                # Fetch and cache if not found
                prompt_details = await self._fetch_and_cache_prompt_details(
                    user_prompt_id, version
                )
            # logger.info(f"Cached new prompt details for {cache_key}")

            # Get interaction history
            interaction_history = InteractionCacheManager.get_interaction_history(
                user_prompt_id, session_id, version
            )

            prompt_collection_msg = []
            messages = []
            window_size = interaction_request.get("window_size", 10)

            # Add system message if platform is OpenAI
            if prompt_details["ai_platform"] == "openai":
                prompt_collection_msg.append(
                    {
                        "role": "system",
                        "content": [
                            {"type": "text", "text": prompt_details["system_prompt"]}
                        ],
                    }
                )

                # Add previous messages from history
            if prompt_details and "messages" in prompt_details:

                published_messages = prompt_details["messages"]
                if published_messages:
                    messages.extend(published_messages)

            # Add previous messages within window size
            if interaction_history and interaction_history.get("messages"):
                # Get last N messages based on window size
                messages.extend(interaction_history["messages"])
                start_idx = max(
                    0, len(messages) - (window_size * 2)
                )  # *2 for pairs of messages
                window_messages = messages[start_idx:]
                prompt_collection_msg.extend(window_messages)

            # Add new user message
            prompt_collection_msg.append(
                {
                    "role": "user",
                    "content": interaction_request["user_message"],
                }
            )

            def_variables = prompt_details["variables"] if prompt_details else []
            default_variables = {}
            if (
                def_variables
                and (isinstance(def_variables, list) and len(def_variables) > 0)
                or (isinstance(def_variables, dict) and def_variables)
            ):

                default_variables = self.convert_data(def_variables)

            platform_key = prompt_details["platform_config"]["platformKey"]

            # Determine which variables to use based on the conditions
            if not interaction_request.get("variables"):
                # Condition 1: No variables given in interaction_request
                variables = default_variables
            else:
                # Condition 2 and 3: Check how many variables are provided
                provided_variables = interaction_request.get("variables")
                variables = {**default_variables}  # Start with default variables
                # Count how many variables are in default_variables
                default_keys = set(default_variables.keys())
                provided_keys = set(provided_variables.keys())
                if provided_keys.issubset(default_keys):
                    # Condition 3: All provided variables are in default_variables
                    variables = provided_variables
                else:
                    # Condition 2: Some variables are provided
                    for key in provided_keys:
                        if key in default_keys:
                            variables[key] = provided_variables[key]
                    # Add remaining default variables
                    for key in default_keys:
                        if key not in provided_keys:
                            variables[key] = default_variables[key]

            # Make AI platform request
            platform_name = prompt_details["ai_platform"]
            platform_key = prompt_details["platform_config"]["platformKey"]
            response = await self._make_ai_platform_request(
                platform_name=platform_name,
                prompt_details=prompt_details,
                messages=prompt_collection_msg,
                system_message=prompt_details["system_prompt"],
                platform_key=platform_key,
            )

            assistant_reply = response["response"]

            # Create new messages to save
            current_time = datetime.now().isoformat()
            new_messages = [
                {
                    "id": str(uuid.uuid4()),
                    "role": "user",
                    "content": interaction_request["user_message"],
                    "env": interaction_request.get("env", "test"),
                    "requestFrom": interaction_request.get("request_from", "sdk"),
                    "initiatedAt": current_time,
                },
                {
                    "id": str(uuid.uuid4()),
                    "role": "assistant",
                    "content": [{"type": "text", "text": f"{assistant_reply}"}],
                    "env": interaction_request.get("env", "test"),
                    "requestFrom": interaction_request.get("request_from", "sdk"),
                    "initiatedAt": current_time,
                },
            ]

            # Save to cache with window memory configuration
            InteractionCacheManager.save_interaction(
                session_id=session_id,
                interaction_data={
                    "messages": new_messages,
                    "lastResponseAt": current_time,
                    "memory_type": "windowMemory",
                    "window_size": window_size,
                },
                prompt_id=user_prompt_id,
                version=version,
            )

            # Print final cache state
            CacheManager.print_cache_contents()
            InteractionCacheManager.print_cache_contents()

            return {
                "message": "AI interaction saved successfully for memory type: window memory",
                "user_prompt_id": user_prompt_id,
                "response": assistant_reply,
                "session_id": session_id,
            }

        except Exception as e:
            error_message = (
                f"An error occurred while processing AI interaction: {str(e)}"
            )
            logger.error(error_message)
            raise ValueError(error_message)

    def modify_new_user_message_for_claude(self, messages):
        """
        Process direct messages for Claude API format by converting file_url to base64 encoded images.
        Args:
            messages (list): List of direct messages containing potential image content
        Returns:
            list: Processed messages with images converted to Claude's format
        """
        # Define supported image types and their corresponding media types
        supported_media_types = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".jfif": "image/jpeg",
            # '.webp': 'image/webp',
            # '.heic': 'image/heic',
            # '.heif': 'image/heif',
            # '.gif': 'image/gif'
        }
        for message in messages:
            if "type" in message and message["type"] == "file":
                # Fetch the image URL dynamically
                file_url = message["file_url"]["url"]
                # Extract file extension from URL
                _, file_extension = os.path.splitext(file_url.lower())
                # Check if file extension is supported
                if file_extension not in supported_media_types:
                    raise ValueError(
                        f"Unsupported image format: {file_extension}. "
                        f"Supported formats are: {', '.join(supported_media_types.keys())}"
                    )
                # Get the corresponding media type
                image_media_type = supported_media_types[file_extension]
                # Fetch the image data and encode it in base64
                image_data = base64.b64encode(httpx.get(file_url).content).decode(
                    "utf-8"
                )
                # Update the message structure to Claude format
                message["type"] = "image"
                message["source"] = {
                    "type": "base64",
                    "media_type": image_media_type,
                    "data": image_data,
                }
                # Remove the old 'file_url' key
                message.pop("file_url", None)
        return messages

    async def fullmemory_save_log_ai_interaction_prompt(
        self,
        user_prompt_id: str,
        interaction_request: Dict,
    ) -> Dict:
        """Process and save AI interaction using cache memory"""
        try:

            # Generate session_id if not present
            session_id = interaction_request.get("session_id") or str(uuid.uuid4())

            # Print initial cache state
            CacheManager.print_cache_contents()
            InteractionCacheManager.print_cache_contents()

            # Get version (either from request or fetch latest)
            version = interaction_request.get("version")

            # First fetch and cache prompt details
            cache_key = f"{user_prompt_id}_{session_id}"
            prompt_details = CacheManager.get_prompt_details(cache_key)

            if not prompt_details:
                # Fetch and cache if not found
                prompt_details = await self._fetch_and_cache_prompt_details(
                    user_prompt_id, session_id, version
                )

            # Get interaction history
            interaction_history = InteractionCacheManager.get_interaction_history(
                user_prompt_id, session_id, version
            )

            if prompt_details["ai_platform"] == "claude":
                prompt_details["messages"][0]["content"] = (
                    self.modify_messages_for_claude(
                        prompt_details["messages"][0]["content"]
                    )
                )

            def_variables = prompt_details["variables"] if prompt_details else []
            default_variables = {}
            if (
                def_variables
                and (isinstance(def_variables, list) and len(def_variables) > 0)
                or (isinstance(def_variables, dict) and def_variables)
            ):

                default_variables = self.convert_data(def_variables)

            platform_key = prompt_details["platform_config"]["platformKey"]

            # Determine which variables to use based on the conditions
            if not interaction_request.get("variables"):
                # Condition 1: No variables given in interaction_request
                variables = default_variables
            else:
                # Condition 2 and 3: Check how many variables are provided
                provided_variables = interaction_request.get("variables")
                variables = {**default_variables}  # Start with default variables
                # Count how many variables are in default_variables
                default_keys = set(default_variables.keys())
                provided_keys = set(provided_variables.keys())
                if provided_keys.issubset(default_keys):
                    # Condition 3: All provided variables are in default_variables
                    variables = provided_variables
                else:
                    # Condition 2: Some variables are provided
                    for key in provided_keys:
                        if key in default_keys:
                            variables[key] = provided_variables[key]
                    # Add remaining default variables
                    for key in default_keys:
                        if key not in provided_keys:
                            variables[key] = default_variables[key]

            # Build message collection
            prompt_collection_msg = []

            # Add system message if platform is OpenAI
            if prompt_details["ai_platform"] == "openai":
                prompt_collection_msg.append(
                    {
                        "role": "system",
                        "content": [
                            {"type": "text", "text": prompt_details["system_prompt"]}
                        ],
                    }
                )

                # Add previous messages
            if interaction_history and interaction_history.get("messages"):
                prompt_collection_msg.extend(interaction_history["messages"])

            # prompt_collection_msg.extend(interaction_history["messages"])

            # Add previous messages from history
            if prompt_details and "messages" in prompt_details:

                published_messages = prompt_details["messages"]
                if published_messages:
                    prompt_collection_msg.extend(published_messages)

            # Add previous messages from history
            if interaction_history and interaction_history.get("messages"):
                prompt_collection_msg.extend(interaction_history["messages"])

            if prompt_details["platform"] == "claude":
                prompt_collection_msg = self.modify_messages_for_claude(
                    prompt_collection_msg
                )
                interaction_request.user_message = (
                    self.modify_new_user_message_for_claude(
                        interaction_request.user_message
                    )
                )

            # Add new user message
            prompt_collection_msg.append(
                {
                    "role": "user",
                    "content": interaction_request["user_message"],
                }
            )
            # Replace placeholders in prompt_collection_msg
            prompt_collection_msg = self.replace_placeholders(
                prompt_collection_msg, variables
            )

            # Make AI platform request
            platform_name = prompt_details["ai_platform"]
            response = await self._make_ai_platform_request(
                platform_name=platform_name,
                prompt_details=prompt_details,
                messages=prompt_collection_msg,
                system_message=prompt_details["system_prompt"],
                platform_key=platform_key,
            )

            assistant_reply = response["response"]

            # Create new messages to save
            current_time = datetime.now().isoformat()
            new_messages = [
                {
                    "id": str(uuid.uuid4()),
                    "role": "user",
                    "content": interaction_request["user_message"],
                    "env": interaction_request.get("env", "test"),
                    "requestFrom": interaction_request.get("request_from", "sdk"),
                    "initiatedAt": current_time,
                },
                {
                    "id": str(uuid.uuid4()),
                    "role": "assistant",
                    "content": [{"type": "text", "text": f"{assistant_reply}"}],
                    "env": interaction_request.get("env", "test"),
                    "requestFrom": interaction_request.get("request_from", "sdk"),
                    "initiatedAt": current_time,
                },
            ]

            # Save to cache with all required information
            InteractionCacheManager.save_interaction(
                session_id=session_id,
                interaction_data={
                    "messages": new_messages,
                    "lastResponseAt": current_time,
                    "memory_type": interaction_request.get("memory_type", "fullMemory"),
                    "window_size": interaction_request.get("window_size", 10),
                },
                prompt_id=user_prompt_id,
                version=version,
            )

            # Print final cache state
            CacheManager.print_cache_contents()
            InteractionCacheManager.print_cache_contents()

            return {
                "message": "AI interaction saved successfully for memory type: full memory",
                "user_prompt_id": user_prompt_id,
                "response": assistant_reply,
                "session_id": session_id,
            }

        except Exception as e:
            error_message = (
                f"An error occurred while processing AI interaction: {str(e)}"
            )
            logger.error(error_message)
            raise ValueError(error_message)

    def replace_placeholders(self, msg_list, variables):
        # Check if variables is empty
        if not variables:
            return msg_list  # Return original list if variables is empty
        # Handle different types of input
        if isinstance(msg_list, dict):
            # If input is a dictionary, recursively process each value
            return {
                k: self.replace_placeholders(v, variables) for k, v in msg_list.items()
            }
        elif isinstance(msg_list, list):
            # If input is a list, recursively process each item
            return [self.replace_placeholders(msg, variables) for msg in msg_list]
        elif isinstance(msg_list, str):
            # If input is a string, replace placeholders
            for key, value in variables.items():
                msg_list = msg_list.replace(f"{{{{{key}}}}}", str(value))
            return msg_list
        else:
            # For any other type, return unchanged
            return msg_list
        # The following code is for handling specific message structures
        # Create a new list to store the modified messages
        modified_msg_list = []
        for msg in msg_list:
            new_msg = msg.copy()  # Create a copy of the message to modify
            if isinstance(new_msg, dict) and "content" in new_msg:
                if isinstance(new_msg["content"], str):
                    # Handle string content
                    for key, value in variables.items():
                        new_msg["content"] = new_msg["content"].replace(
                            f"{{{{{key}}}}}", str(value)
                        )
                elif isinstance(new_msg["content"], list):
                    # Handle list of content
                    new_content = []
                    for content in new_msg["content"]:
                        new_content_item = content.copy()
                        if (
                            isinstance(new_content_item, dict)
                            and "text" in new_content_item
                        ):
                            for key, value in variables.items():
                                new_content_item["text"] = new_content_item[
                                    "text"
                                ].replace(f"{{{{{key}}}}}", str(value))
                        new_content.append(new_content_item)
                    new_msg["content"] = new_content
            modified_msg_list.append(new_msg)
        return modified_msg_list  # Return the new list with modified messages

    def convert_data(self, data):
        # Create an empty dictionary to hold the converted data
        result = {}
        # Iterate through each item in the input data
        for item in data:
            # Extract 'name' and 'value' and add them to the result dictionary
            if "name" in item and "value" in item:
                result[item["name"]] = item["value"]
        return result

    def modify_messages_for_claude(self, messages):
        """
        Process images in messages for Claude API format by converting file_url to base64 encoded images.
        Args:
            messages (list): List of messages containing potential image content
            Returns:
            list: Processed messages with images converted to Claude's format
        """
        # Define supported image types and their corresponding media types
        supported_media_types = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".jfif": "image/jpeg",
            # '.webp': 'image/webp',
            # '.heic': 'image/heic',
            # '.heif': 'image/heif',
            # '.gif': 'image/gif'
        }
        for message in messages:
            if "content" in message:
                for content in message["content"]:
                    if content.get("type") == "file":
                        # Fetch the image URL dynamically
                        file_url = content["file_url"]["url"]
                        # Extract file extension from URL
                        _, file_extension = os.path.splitext(file_url.lower())
                        # Check if file extension is supported
                        if file_extension not in supported_media_types:
                            raise ValueError(
                                f"Unsupported image format: {file_extension}. "
                                f"Supported formats are: {', '.join(supported_media_types.keys())}"
                            )
                        # Get the corresponding media type
                        image_media_type = supported_media_types[file_extension]
                        # Fetch the image data and encode it in base64
                        image_data = base64.b64encode(
                            httpx.get(file_url).content
                        ).decode("utf-8")
                        # Update the content structure
                        content["type"] = "image"
                        content["source"] = {
                            "type": "base64",
                            "media_type": image_media_type,
                            "data": image_data,
                        }
                        # Remove the old 'file_url' key
                        content.pop("file_url", None)
        return messages

    async def summarymemory_save_log_ai_interaction_prompt(
        self,
        user_id: str,
        user_prompt_id: str,
        user_prompt: dict,
        interaction_request: Dict,
    ) -> Dict:
        """Process and save AI interaction using summary memory cache"""
        try:
            # logger.info("\n" + "=" * 50)
            # logger.info("Starting summarymemory_save_log_ai_interaction_prompt")
            # logger.info("=" * 50)

            # Cache status before processing
            self._print_persistent_cache_contents()

            session_type, session_id = self._fetch_session_id(interaction_request)
            cache_key = f"{user_prompt_id}_{session_id}"

            # Load existing interaction history from persistent cache
            interaction_history = self._load_from_persistent_cache(cache_key)

            # Get version (either from request or fetch latest)
            version = interaction_request.get("version")

            # First fetch and cache prompt details
            prompt_details = CacheManager.get_prompt_details(cache_key)

            if not prompt_details:
                # Fetch and cache if not found
                prompt_details = await self._fetch_and_cache_prompt_details(
                    user_prompt_id, session_id, version
                )

            system_message = (
                prompt_details["system_prompt"]
                if prompt_details.get("system_prompt")
                else ""
            )
            variables = (
                prompt_details["variables"] if prompt_details.get("variables") else {}
            )

            default_variables = convert_variables_data(variables)

            variables = merge_default_and_provided_variables(
                interaction_request, default_variables
            )

            # Get interaction history
            # interaction_history = InteractionCacheManager.get_interaction_history(
            #     user_prompt_id, session_id, version
            # )

            # Initialize message collection
            prompt_collection_msg = []
            if user_prompt["platform"] == "openai":
                prompt_collection_msg.append(
                    {
                        "role": "system",
                        "content": [
                            {"type": "text", "text": prompt_details["system_prompt"]}
                        ],
                    }
                )

            # Get existing summarized content
            # summarized_content = self._get_existing_summarized_content(
            #     interaction_history, session_id, version
            # )

            result = await self.get_summarized_content(
                prompt_id=user_prompt_id,
                session_id=session_id,
            )

            # Initialize summarized_content
            summarized_content = ""
            if result["status"] == "success":
                summarized_content = result["summarized_content"]
            # else:

            if session_type == "new_session":
                prompt_collection_msg.extend(interaction_request["user_message"])

            elif session_type == "existing_session":
                content_msg = [
                    {
                        "role": "assistant",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Summary of previous AI Interaction: {summarized_content}\n\nNew user message that needs to be responded is in next message:",
                                # replaced with prompt colllection message
                            },
                        ],
                    }
                ]

                for message in interaction_request["user_message"]:
                    if isinstance(message, dict) and message.get("type") == "file":
                        content_msg.append(message)
                    else:
                        content_msg.append(message)

                prompt_collection_msg.extend(content_msg)
            print(f"prompt_collection_msg  ssssssss: {prompt_collection_msg}")

            print(f"prompt_details  ssssssss: {prompt_details}")

            platform_key = prompt_details["platform_config"]["platformKey"]
            response = await self._make_ai_platform_request(
                platform_name=prompt_details["ai_platform"],
                prompt_details=prompt_details,
                messages=prompt_collection_msg,
                system_message=prompt_details["system_prompt"],
                platform_key=platform_key,
            )

            # get_ai_response = {
            #     "role": "assistant",
            #     "content": [{"type": "text", "text": response["response"]}],
            # }

            get_ai_response = response["response"]

            processed_ai_response = process_ai_response_by_format(
                get_ai_response, prompt_details["response_format"]
            )

            # if not summarized_content:
            # If no summary exists, generate one from all messages
            prompt_collection_msg.extend(
                interaction_history.get("messages", []) if interaction_history else []
            )
            summary_message_collection = prompt_collection_msg
            logger.info(
                f"summary_message_collection   [processed_ai_response['content'][0]] ssssssss: { [processed_ai_response['content'][0]]}"
            )

            if session_type == "new_session":
                logger.info(
                    f" new_session summary_message_collection   [interaction_request['user_message']] ssssssss: {interaction_request['user_message']}"
                )
                summary_message_collection.extend(
                    [
                        {
                            "role": "user",
                            "content": interaction_request["user_message"],
                        },
                        {
                            "role": "assistant",
                            "content": [processed_ai_response["content"][0]],
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": PROMPT_TO_GENERATE_SUMMARIZED_CONTENT,
                                }
                            ],
                        },
                    ]
                )
            else:  # existing_session
                logger.info(
                    f" existing_session summary_message_collection   [interaction_request['user_message']] ssssssss: {interaction_request['user_message']}"
                )
                summary_message_collection.extend(
                    [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"Summary of previous AI Interaction: {summarized_content}\n\nNew user message that needs to be responded: {interaction_request['user_message']}",
                                }
                            ],
                        },
                        {
                            "role": "assistant",
                            "content": [processed_ai_response["content"][0]],
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": PROMPT_TO_GENERATE_SUMMARIZED_CONTENT,
                                }
                            ],
                        },
                    ]
                )

            platform_key = prompt_details["platform_config"]["platformKey"]
            logger.info(
                f"summary_message_collection   [summary_message_collection] ssssssss: {summary_message_collection}"
            )

            create_summary = await self._make_ai_platform_request(
                platform_name=prompt_details["ai_platform"],
                prompt_details=prompt_details,
                messages=summary_message_collection,
                system_message=system_message,
                platform_key=platform_key,
            )

            if prompt_details["ai_platform"] == "gemini":
                new_summarized_content = create_summary["response"]
                ai_response = {"type": "text", "text": response["response"]}

            else:
                new_summarized_content = create_summary["response"]
                ai_response = {"type": "text", "text": response["response"]}

            current_time = datetime.now().isoformat()
            new_messages = [
                {
                    "id": str(uuid.uuid4()),
                    "role": "user",
                    "content": interaction_request["user_message"],
                    "env": interaction_request.get("env", "test"),
                    "requestFrom": interaction_request.get("request_from", "sdk"),
                    "initiatedAt": current_time,
                },
                {
                    "id": str(uuid.uuid4()),
                    "role": "assistant",
                    "content": ai_response,
                    "env": interaction_request.get("env", "test"),
                    "requestFrom": interaction_request.get("request_from", "sdk"),
                    "initiatedAt": current_time,
                },
            ]

            # Before saving to cache, log the new summary

            # Save to persistent cache with new summary
            interaction_data = {
                "messages": new_messages,
                "lastResponseAt": current_time,
                "memory_type": "summarizedMemory",
                "summarized_content": new_summarized_content,  # Save the new summary
            }
            self._save_to_persistent_cache(cache_key, interaction_data)

            # Verify cache update
            self._print_persistent_cache_contents()

            # Verify the summary was saved
            updated_history = self._load_from_persistent_cache(cache_key)

            if prompt_details["ai_platform"] == "gemini":
                final_response = response["response"]
            else:
                final_response = response["response"]

            result = {
                "message": "AI interaction saved successfully for memory type: summarized memory",
                "user_prompt_id": str(user_prompt_id),
                "response": final_response,
                "session_id": session_id,
            }

            return result

        except Exception as e:
            error_message = (
                f"An error occurred while processing AI interaction: {str(e)}"
            )
            logger.error("\nERROR OCCURRED:")
            logger.error(error_message)
            logger.error("Cache state at error:")
            self._print_persistent_cache_contents()
            raise ValueError(error_message)

    async def _fetch_and_cache_prompt_details(
        self, prompt_id: str, session_id: str, version: Optional[str] = None
    ) -> Dict:
        """
        Fetch prompt details from PromptStudio

        Args:
            prompt_id: ID of the prompt
            session_id: Session ID
            version: Optional version number (if None, will use null in request)

        Returns:
            Dictionary containing prompt details
        """
        try:
            # Clean the prompt_id
            prompt_id = prompt_id.strip()

            # Prepare request body with proper version format and stringify
            request_body = json.dumps({"version": float(version) if version else None})

            # Make request to version_data endpoint with proper headers
            response = await self._request(
                f"/fetch/prompt/version_data/{prompt_id}",
                method="POST",
                data=request_body,  # Use data instead of json for stringified content
            )

            if not response.get("data") or not response["data"].get("result"):
                logger.error(f"Invalid response format for prompt_id: {prompt_id}")
                raise ValueError("Invalid response format from API")

            # Extract data from response
            result = response["data"]["result"]
            prompt = result["prompt"]
            ai_platform = prompt["aiPlatform"]
            messages = result["messages"]
            platform_config = result.get("platformConfig", {})
            variables = messages.get("variable", {})

            # Extract and format the prompt details
            prompt_details = {
                "ai_platform": ai_platform["platform"],
                "model": ai_platform["model"],
                "system_prompt": messages.get("systemMessage", ""),
                "temperature": ai_platform["temp"],
                "max_tokens": ai_platform["max_tokens"],
                "messages": messages.get("messages", []),
                "top_p": ai_platform["top_p"],
                "frequency_penalty": ai_platform["frequency_penalty"],
                "presence_penalty": ai_platform["presence_penalty"],
                "response_format": ai_platform["response_format"],
                "version": prompt["version"],
                "platform_config": platform_config,  # Include platform config if needed
                "variables": variables,
            }

            # Cache the prompt details
            cache_key = f"{prompt_id}_{session_id}"
            CacheManager.set_prompt_details(cache_key, prompt_details)

            return prompt_details

        except Exception as e:
            logger.error(f"Error in _fetch_and_cache_prompt_details: {str(e)}")
            raise

    def modify_messages_for_openai(self, messages):
        """Convert file types to image_url format for OpenAI"""
        modified_messages = []
        supported_extensions = [".png", ".jpeg", ".jpg", ".webp", ".jfif"]

        for message in messages:
            modified_content = []
            for content in message.get("content", []):
                if content.get("type") == "file" and content.get("file_url", {}).get(
                    "url"
                ):
                    image_url = content["file_url"]["url"]
                    _, extension = os.path.splitext(image_url)
                    if extension.lower() not in supported_extensions:
                        raise ValueError(
                            f"Unsupported image extension: {extension}. "
                            "We currently support PNG (.png), JPEG (.jpeg and .jpg), "
                            "WEBP (.webp), and JFIF (.jfif)"
                        )
                    modified_content.append(
                        {"type": "image_url", "image_url": {"url": image_url}}
                    )
                else:
                    modified_content.append(content)

            modified_messages.append(
                {"role": message["role"], "content": modified_content}
            )
        return modified_messages

    async def _make_openai_request(
        self, prompt_details: Dict, payload: Dict, platform_key
    ) -> Dict:
        """Make a direct request to OpenAI"""

        # Get OpenAI API key from environment when in bypass mode
        # openai_api_key = os.getenv("OPENAI_API_KEY")
        openai_api_key = platform_key
        if not openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY  variable is required , bypass mode is true. which is set while publishing the prompt"
            )

        # Extract messages from payload
        messages = payload.get("user_message", [])
        print(f"messages  ssssssss: {messages}")

        # Format messages for OpenAI while preserving structure
        formatted_messages = []

        # Add system message if present
        # if prompt_details.get("system_prompt"):
        #     formatted_messages.append(
        #         {"role": "system", "content": prompt_details["system_prompt"]}
        #     )

        # Process each message and handle file types
        messages = self.modify_messages_for_openai(messages)

        # Remove the first object (system message) and extend the formatted messages
        if len(messages) > 0:
            formatted_messages.extend(messages[1:])  # Skip the first message

        # Add system message at the start if present
        if prompt_details.get("system_prompt"):
            formatted_messages.insert(
                0,
                {
                    "role": "system",
                    "content": [
                        {"type": "text", "text": prompt_details["system_prompt"]}
                    ],
                },
            )
        print(f"formatted_messages  ssssssss: {formatted_messages}")

        try:
            response = openai_interaction(
                secret_key=openai_api_key,  # Use OpenAI key from environment
                model=prompt_details["model"],
                messages=formatted_messages,
                temperature=prompt_details.get("temp", 0.7),
                max_tokens=prompt_details["max_tokens"],
                top_p=prompt_details.get("top_p", 0.5),
                frequency_penalty=prompt_details.get("frequency_penalty", 0.7),
                presence_penalty=prompt_details.get("presence_penalty", 0.3),
                response_format=prompt_details.get("response_format"),
            )
            return response
        except Exception as e:
            logger.error(f"Error making OpenAI request: {str(e)}")
            raise

    async def _make_anthropic_request(
        self, prompt_details: Dict, payload: Dict, platform_key
    ) -> Dict:
        """Make a direct request to Anthropic"""
        user_message = next(
            (msg for msg in payload["user_message"] if msg["type"] == "text"), None
        )
        if not user_message:
            logger.error("No text message found in payload")
            raise ValueError("Text message is required for Anthropic requests")

        try:
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": platform_key,
                    "Content-Type": "application/json",
                },
                json={
                    "model": prompt_details["model"],
                    "messages": [
                        {
                            "role": "system",
                            "content": prompt_details["system_prompt"],
                        },
                        {"role": "user", "content": user_message["text"]},
                    ],
                    "max_tokens": prompt_details["max_tokens"],
                },
            )
            response.raise_for_status()
            data = response.json()
            return {"response": data["content"][0]["text"]}
        except Exception as e:
            logger.error(f"Error making Anthropic request: {str(e)}")
            raise

    async def _direct_ai_request(
        self, prompt_id: str, session_id: str, payload: Dict
    ) -> Dict:
        """Handle direct AI platform requests"""

        # Get version from payload
        version = (
            str(payload.get("version")) if payload.get("version") is not None else None
        )

        if version:
            cache_key = f"{prompt_id}_{session_id}_v{version}"
            prompt_details = CacheManager.get_prompt_details(cache_key)
        else:
            # Try to find latest version in cache
            prompt_details = None

        if not prompt_details:
            prompt_details = await self._fetch_and_cache_prompt_details(
                prompt_id, version
            )
            version = prompt_details[
                "version"
            ]  # Get the version (might be latest if none was specified)

        platform_key = prompt_details["platform_config"]["platformKey"]

        try:
            if prompt_details["ai_platform"] == "openai":
                return await self._make_openai_request(
                    prompt_details, payload, platform_key
                )
            elif prompt_details["ai_platform"] == "anthropic":
                return await self._make_anthropic_request(
                    prompt_details, payload, platform_key
                )
            else:
                logger.error(
                    f"Unsupported AI platform: {prompt_details['ai_platform']}"
                )
                raise ValueError(
                    f"Unsupported AI platform: {prompt_details['ai_platform']}"
                )
        except Exception as e:
            logger.error(f"Error in direct AI request: {str(e)}")
            raise

    def _get_existing_summarized_content(
        self, interaction_history: Dict, session_id: str, version: str
    ) -> str:
        """Get existing summarized content from interaction history"""
        if (
            interaction_history
            and interaction_history.get("memory_type") == "summarizedMemory"
            and "summarized_content" in interaction_history
        ):
            return interaction_history["summarized_content"]
        return ""

    async def chat_with_prompt(
        self,
        prompt_id: str,
        user_message: List[Dict[str, Union[str, Dict[str, str]]]],
        memory_type: str,
        window_size: int,
        session_id: str,
        variables: Dict[str, str],
        version: Optional[int] = None,
    ) -> Dict[str, str]:
        """
        Chat with a specific prompt

        Args:
            prompt_id: ID of the prompt
            user_message: List of message dictionaries
            memory_type: Type of memory ('fullMemory', 'windowMemory', or 'summarizedMemory')
            window_size: Size of the memory window
            session_id: Session identifier
            variables: Dictionary of variables
            version: Optional version number

        Returns:
            Dictionary containing the response
        """

        payload = {
            "user_message": user_message,
            "memory_type": memory_type,
            "window_size": window_size,
            "session_id": session_id,
            "variables": variables,
            "request_from": "python_sdk",
            "env": self.env,
            "version": version,
        }

        if version is not None:
            payload["version"] = version

        try:
            if self.bypass:
                # if memory_type == "summarizedMemory":
                #     return await self.summarizedmemory_save_log_ai_interaction_prompt(
                #         prompt_id, session_id, payload
                #     )
                if memory_type == "windowMemory":
                    return await self.windowmemory_save_log_ai_interaction_prompt(
                        prompt_id, payload
                    )
                elif memory_type == "fullMemory":
                    return await self.fullmemory_save_log_ai_interaction_prompt(
                        prompt_id, payload
                    )
                else:
                    return await self._direct_ai_request(prompt_id, session_id, payload)

            else:
                response = await self._request(
                    f"/chat_with_prompt_version/{prompt_id}",
                    method="POST",
                    json=payload,
                )
                return response
        except Exception as e:
            logger.error(f"Error in chat_with_prompt: {str(e)}")
            raise

    async def _make_ai_platform_request(
        self,
        platform_name: str,
        prompt_details: Dict,
        messages: List[Dict],
        system_message: str,
        platform_key: str,
    ) -> Dict:
        """
        Make request to the appropriate AI platform

        Args:
            platform_name: Name of the AI platform (openai, anthropic, etc.)
            prompt_details: Dictionary containing prompt configuration
            messages: List of messages to send
            system_message: System message to use

        Returns:
            Dictionary containing the response
        """

        try:
            print(f" _make_ai_platform_request  ssssssss: {messages}")
            if platform_name.lower() == "openai":
                return await self._make_openai_request(
                    prompt_details, {"user_message": messages}, platform_key
                )
            elif platform_name.lower() == "anthropic":
                return await self._make_anthropic_request(
                    prompt_details, {"user_message": messages}, platform_key
                )
            elif platform_name.lower() == "gemini":
                # Get Gemini API key from environment
                # gemini_api_key = os.getenv("GEMINI_API_KEY")
                gemini_api_key = platform_key
                if not gemini_api_key:
                    raise ValueError(
                        "GEMINI_API_KEY  is required when using Gemini, which is set while publishing the prompt. bypass mode is true"
                    )

                return gemini_interaction_chat_with_prompt(
                    secret_key=gemini_api_key,  # Use Gemini key from environment
                    model=prompt_details["model"],
                    messages=messages,
                    system_message=system_message,
                    temperature=prompt_details.get("temp", 0.7),
                    max_output_tokens=prompt_details.get("max_tokens", 1000),
                    top_p=prompt_details.get("top_p", 0.8),
                    top_k=prompt_details.get("top_k", 40),
                    response_format=prompt_details.get("response_format"),
                )
            else:
                error_msg = f"Unsupported AI platform: {platform_name}"
                logger.error(error_msg)
                raise ValueError(error_msg)

        except Exception as e:
            logger.error(f"Error in _make_ai_platform_request: {str(e)}")
            raise

    def _fetch_session_id(self, interaction_request: Dict) -> Tuple[str, str]:
        """
        Determine session type and get session ID from interaction request

        Args:
            interaction_request: Dictionary containing the interaction request

        Returns:
            Tuple containing (session_type, session_id)
        """
        session_id = interaction_request.get("session_id", "")
        if not session_id:
            new_session = str(ObjectId())
            return "new_session", new_session
        else:
            return "existing_session", session_id

    async def get_summarized_content(
        self, prompt_id: str, session_id: str
    ) -> Dict[str, Any]:
        """
        Fetch summarized content for a specific prompt session.

        Args:
            prompt_id: ID of the prompt
            session_id: Session identifier

        Returns:
            Dictionary containing the summarized content and status
        """
        try:

            # Generate cache key
            cache_key = f"{prompt_id}_{session_id}"

            # Try to load from persistent cache
            cached_data = self._load_from_persistent_cache(cache_key)

            if cached_data and "summarized_content" in cached_data:
                return {
                    "status": "success",
                    "summarized_content": cached_data["summarized_content"],
                    "memory_type": cached_data.get("memory_type", "summarizedMemory"),
                    "session_id": session_id,
                }

            return {
                "status": "not_found",
                "message": "No summarized content found for this session",
                "session_id": session_id,
            }

        except Exception as e:
            error_message = f"Error fetching summarized content: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "message": error_message,
                "session_id": session_id,
            }


def openai_interaction(
    secret_key,
    model,
    messages,
    temperature,
    max_tokens,
    top_p,
    frequency_penalty,
    presence_penalty,
    response_format,
):
    """Make a request to OpenAI API"""
    # Set the OpenAI API key
    client = OpenAI(api_key=secret_key)

    try:
        # Call the OpenAI API
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            response_format=response_format,
            timeout=50000,
        )

        # Get the response content using the new API format
        assistant_reply = response.choices[0].message.content.strip()

        return {
            "response": assistant_reply,
        }
    except Exception as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise


def format_messages_for_gemini(messages, system_message=None):
    formatted_messages = []

    for i, msg in enumerate(messages):
        role = msg.get("role")
        content = msg.get("content")

        if isinstance(content, list):
            text_content = " ".join(
                [
                    (
                        part.get("text", "")
                        if isinstance(part.get("text"), str)
                        else json.dumps(part.get("text", ""))
                    )
                    for part in content
                    if part.get("type") == "text"
                ]
            )
        elif isinstance(content, str):
            text_content = content
        else:
            text_content = json.dumps(content)

        if i == 0 and system_message:
            text_content = f"{system_message}\n\n{text_content}"

        formatted_messages.append(
            {
                "role": "user" if role in ["user", "system"] else "model",
                "parts": [{"text": text_content}],
            }
        )

    return formatted_messages


def create_response_schema(payload: dict) -> content.Schema:
    def create_property_schema(prop):
        if isinstance(prop["type"], list):
            # Handle multiple types
            #  return content.Schema(
            #     type=content.Type.UNION,
            return glm.Content.Schema(
                type=glm.Content.Type.STRING,
                items=[
                    create_property_schema({"type": t})
                    for t in prop["type"]
                    if t != "null"
                ],
            )
        elif prop["type"] == "string":
            return content.Schema(type=content.Type.STRING)
        elif prop["type"] == "integer":
            return content.Schema(type=content.Type.INTEGER)
        elif prop["type"] == "number":
            return content.Schema(type=content.Type.NUMBER)
        elif prop["type"] == "boolean":
            return content.Schema(type=content.Type.BOOLEAN)
        elif prop["type"] == "array":
            if "items" in prop:
                return content.Schema(
                    type=content.Type.ARRAY, items=create_property_schema(prop["items"])
                )
            return content.Schema(type=content.Type.ARRAY)
        elif prop["type"] == "object":
            return create_response_schema(prop)
        else:
            return content.Schema(
                type=content.Type.STRING
            )  # Default to string for unknown types

    properties = {}
    for key, value in payload["properties"].items():
        properties[key] = create_property_schema(value)

    required = payload.get("required", [])
    return content.Schema(
        type=content.Type.OBJECT, properties=properties, required=required
    )


def gemini_interaction_chat_with_prompt(
    secret_key,
    model,
    messages,
    system_message,
    temperature,
    max_output_tokens,
    top_p,
    top_k,
    response_format,
):
    genai.configure(api_key=secret_key)
    messages = [
        {
            "role": "system",
            "content": [{"type": "text", "text": "respond in only {{number}} words"}],
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "Summary of previous AI Interaction: This conversation thread explored the AI's response capabilities and summarization skills. Initially, the user requested the AI to respond with a specific number of words, indicated by a placeholder.  The AI acknowledged this request by echoing it back.  Subsequently, the user provided context for a new interaction, presenting a user message expressing gratitude for assistance. The AI simply replied with \"You're welcome.\"  Finally, the user twice requested a detailed, concise summary of the entire conversation, specifying a maximum length of \n\nNew user message that needs to be responded is in next message:",
                }
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Hello! How can you help me with Python programming?",
                }
            ],
        },
        {
            "id": "7152f5fd-4a8b-410e-af46-b24d5d1010fa",
            "role": "user",
            "content": [{"type": "text", "text": "Thank you for your help!"}],
            "env": "test",
            "requestFrom": "sdk",
            "initiatedAt": "2024-11-16T16:27:34.340258",
        },
        {
            "id": "2304ba60-131a-4809-82c3-d01c873f8a75",
            "role": "assistant",
            "content": [{"type": "text", "text": "You're welcome.\n"}],
            "env": "test",
            "requestFrom": "sdk",
            "initiatedAt": "2024-11-16T16:27:34.340258",
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Summary of previous AI Interaction: This conversation thread explored the AI's response capabilities and summarization skills. Initially, the user requested the AI to respond with a specific number of words, indicated by a placeholder.  The AI acknowledged this request by echoing it back.  Subsequently, the user provided context for a new interaction, presenting a user message expressing gratitude for assistance. The AI simply replied with \"You're welcome.\"  Finally, the user twice requested a detailed, concise summary of the entire conversation, specifying a maximum length of \n\nNew user message that needs to be responded: [{'role': 'user', 'content': [{'type': 'text', 'text': 'Hello! How can you help me with Python programming?'}]}]",
                }
            ],
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "Code explanation, debugging, generation, and tutorials.\n",
                }
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Summarize the above conversation in a detailed, concise, and well-structured manner. ensuring the summary does not exceed 250 words. Capture the key points and context, including important questions, answers, and relevant follow-up, while avoiding unnecessary repetition. Present the summary in a well-structured paragraph, focusing on the most important content exchanged",
                }
            ],
        },
    ]

    if system_message and system_message.strip():
        gemini_model = genai.GenerativeModel(
            model_name=model, system_instruction=system_message
        )
    else:
        gemini_model = genai.GenerativeModel(model_name=model)

    if response_format["type"] == "text":
        logger.info("Response format is text")
        response_schema = None
        response_mime_type = "text/plain"
    else:
        logger.info("Response format is not text")
        try:
            response_schema = create_gemini_schema(response_format)
            response_mime_type = "application/json"
        except Exception as e:
            raise ValueError(f"Invalid JSON schema")

    generated_history = convert_messages_to_gemini_format(messages)
    # Prepare the message to send
    last_message_parts = generated_history[-1]["parts"]

    # Check if there is any text in the last message parts
    if not any(isinstance(part, str) and part.strip() for part in last_message_parts):
        # If no text is found, add a default text message
        last_message_parts = [""] + last_message_parts

    chat = gemini_model.start_chat(history=generated_history)

    try:

        response = chat.send_message(
            last_message_parts,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_output_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                response_schema=response_schema,
                response_mime_type=response_mime_type,
            ),
        )

        # Check if we have a valid response
        if response is None:
            raise ValueError("No valid response received from Gemini API")

        # The last response will be the model's reply to the most recent user message
        if response_mime_type == "text/plain":
            assistant_reply = response.text

        else:

            assistant_reply = response.candidates[0].content.parts[0].text
            assistant_reply = json.loads(assistant_reply)

        return {"response": assistant_reply}

    except genai.types.generation_types.BlockedPromptException as e:
        raise ValueError(f"Gemini API error: The prompt was blocked. Reason: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in Gemini interaction: {str(e)}")
        raise ValueError(f"Unexpected error occurred: {str(e)}")


def create_gemini_schema(response_dict: Dict[str, Any]) -> genai.protos.Schema:
    """
    Convert any dictionary into a Gemini response schema format.

    Args:
        response_dict (dict): Input dictionary to convert

    Returns:
        genai.protos.Schema: Gemini schema format
    """

    def _process_value(value: Any) -> genai.protos.Schema:
        if isinstance(value, dict):
            if "type" in value:
                # Handle OpenAPI/JSON schema style definitions
                schema_type = value["type"].upper()
                properties = {}
                required = []

                if schema_type == "OBJECT" and "properties" in value:
                    properties = {
                        k: _process_value(v) for k, v in value["properties"].items()
                    }
                    required = value.get("required", [])
                elif schema_type == "ARRAY" and "items" in value:
                    return genai.protos.Schema(
                        type=genai.protos.Type.ARRAY,
                        items=_process_value(value["items"]),
                    )

                schema = genai.protos.Schema(
                    type=getattr(genai.protos.Type, schema_type),
                    properties=properties,
                    required=required,
                )

                # Handle enums if present
                if "enum" in value:
                    schema = genai.protos.Schema(
                        type=genai.protos.Type.STRING, enum=value["enum"]
                    )

                # Handle description if present
                if "description" in value:
                    schema.description = value["description"]

                return schema
            else:
                # Handle nested dictionary without type specification
                return genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={k: _process_value(v) for k, v in value.items()},
                )
        elif isinstance(value, list):
            if value:
                return genai.protos.Schema(
                    type=genai.protos.Type.ARRAY, items=_process_value(value[0])
                )
            return genai.protos.Schema(
                type=genai.protos.Type.ARRAY,
                items=genai.protos.Schema(type=genai.protos.Type.STRING),
            )
        elif isinstance(value, bool):
            return genai.protos.Schema(type=genai.protos.Type.BOOLEAN)
        elif isinstance(value, int):
            return genai.protos.Schema(type=genai.protos.Type.INTEGER)
        elif isinstance(value, float):
            return genai.protos.Schema(type=genai.protos.Type.NUMBER)
        else:
            return genai.protos.Schema(type=genai.protos.Type.STRING)

    # Process the root schema
    return _process_value(response_dict)


def convert_messages_to_gemini_format(messages):
    gemini_messages = []
    for message in messages:
        role = "user" if message["role"] == "user" else "model"
        parts = []

        for content in message["content"]:
            if content["type"] == "text":
                parts.append(content["text"])
            elif content["type"] == "file":
                parts.append(upload_file_to_gemini(file_url=content["file_url"]["url"]))

        gemini_messages.append({"role": role, "parts": parts})

    return gemini_messages


def upload_file_to_gemini(file_url):

    with tempfile.TemporaryDirectory() as tempdir:
        tempfiles = Path(tempdir)
        response = requests.get(file_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.content

        # Generate file name and path
        name = file_url.split("/")[-1]
        hash = hashlib.sha256(data).hexdigest()
        path = tempfiles / hash

        # Write data to file
        path.write_bytes(data)

        print("Uploading:", file_url)
        mime_type = identify_mime_type(file_url)
        file_content = genai.upload_file(path, mime_type=mime_type)
        return file_content


def identify_mime_type(file_url):
    # Extract the file extension from the URL
    _, file_extension = os.path.splitext(file_url)
    file_extension = file_extension.lower()

    # Define custom mappings for specific file types
    custom_mime_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".jfif": "image/jpeg",
        ".webp": "image/webp",
        ".heic": "image/heic",
        ".heif": "image/heif",
        ".wav": "audio/wav",
        ".mp3": "audio/mp3",
        ".aiff": "audio/aiff",
        ".aac": "audio/aac",
        ".ogg": "audio/ogg",
        ".flac": "audio/flac",
    }

    # Check if the file extension is in our custom mappings
    if file_extension in custom_mime_types:
        return custom_mime_types[file_extension]

    # If not in custom mappings, use mimetypes library as a fallback
    mime_type, _ = mimetypes.guess_type(file_url)

    # If mimetypes library couldn't determine the type, return a default
    if mime_type is None:
        return "application/octet-stream"

    return mime_type


# Helper methods for summary memory
SUMMARY_PROMPT = """Please provide a concise summary of the conversation so far, 
highlighting the key points and important context that would be relevant for continuing the discussion."""


def process_ai_response_by_format(get_ai_response, response_format):
    # Ensure get_ai_response is a string
    if not isinstance(get_ai_response, str):
        get_ai_response = json.dumps(get_ai_response)

    # Remove any surrounding quotes
    get_ai_response = get_ai_response.strip('"')

    # Process based on response_format type
    if response_format.get("type") == "text":
        # For text type, ensure it's a string
        try:
            # If it's valid JSON, convert it to a string
            parsed = json.loads(get_ai_response)
            if isinstance(parsed, (dict, list)):
                content = json.dumps(parsed)
            else:
                content = str(parsed)
        except json.JSONDecodeError:
            # If it's not valid JSON, use it as is
            content = get_ai_response
    elif response_format.get("type") == "object":
        # For object type, ensure it's a valid JSON object
        try:
            content = json.loads(get_ai_response)
            if not isinstance(content, dict):
                # If it's not a dict, wrap it in a dict
                content = {"content": content}
        except json.JSONDecodeError:
            # If it's not valid JSON, wrap it in a dict
            content = {"content": get_ai_response}
    else:
        # Default to treating it as text
        content = str(get_ai_response)

    # Return the processed response in the required format
    return {"role": "assistant", "content": [{"type": "text", "text": content}]}


async def _generate_summary(
    self, messages: list, prompt_details: Dict, interaction_request: Dict
) -> str:
    """Generate a summary of the conversation"""
    try:
        # Make request to AI platform for summary
        response = await self._make_ai_platform_request(
            platform_name=prompt_details["ai_platform"],
            prompt_details=prompt_details,
            messages=messages,
            system_message=self.SUMMARY_PROMPT,
        )

        return response["response"]
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise ValueError(f"Failed to generate summary: {str(e)}")


def convert_variables_data(data):
    # Create an empty dictionary to hold the converted data
    result = {}

    # Iterate through each item in the input data
    for item in data:
        # Extract 'name' and 'value' and add them to the result dictionary
        if "name" in item and "value" in item:
            result[item["name"]] = item["value"]

    return result


def merge_default_and_provided_variables(
    interaction_request: Dict, default_variables: Dict
) -> Dict:
    """
    Merge provided variables with default variables

    Args:
        interaction_request: Dictionary containing the interaction request
        default_variables: Dictionary containing default variables

    Returns:
        Dictionary containing merged variables
    """
    # Get variables from interaction request, defaulting to empty dict
    provided_variables = interaction_request.get("variables", {})

    if not provided_variables:
        return default_variables

    variables = {**default_variables}
    default_keys = set(default_variables.keys())
    provided_keys = set(provided_variables.keys())

    if provided_keys.issubset(default_keys):
        return provided_variables

    for key in provided_keys:
        if key in default_keys:
            variables[key] = provided_variables[key]
    for key in default_keys:
        if key not in provided_keys:
            variables[key] = default_variables[key]

    return variables


# def save_messages_and_summary(
#     user_prompt_id, session_id, interaction_request, ai_response, new_summarized_content
# ):
#     new_msgs_save = [
#         {
#             "_id": ObjectId(),
#             "role": "user",
#             "content": interaction_request.user_message,
#             "env": interaction_request.env,
#             "requestFrom": interaction_request.request_from,
#             "initiatedAt": datetime.now(),
#         },
#         {
#             "_id": ObjectId(),
#             "role": "assistant",
#             "content": ai_response,
#             "env": interaction_request.env,
#             "requestFrom": interaction_request.request_from,
#             "initiatedAt": datetime.now(),
#         },
#     ]

#     user_prompt_access = fetch_user_prompt_access(user_prompt_id, session_id)

#     if not user_prompt_access:

#         promptAccess_collection.update_one(
#             {"UserPromptsId": user_prompt_id},
#             {
#                 "$push": {
#                     "userPrompts": {
#                         "messages": new_msgs_save,
#                         "memory_type": interaction_request.memory_type,
#                         "window_size": interaction_request.window_size,
#                         "summarized_content": new_summarized_content,
#                         "sessionId": session_id,
#                     }
#                 },
#                 "$set": {"lastResponseAt": datetime.now()},
#             },
#             upsert=True,
#         )
#     else:
#         promptAccess_collection.update_one(
#             {
#                 "UserPromptsId": user_prompt_id,
#                 "userPrompts.sessionId": session_id,
#             },
#             {
#                 "$push": {"userPrompts.$.messages": {"$each": new_msgs_save}},
#                 "$set": {
#                     "userPrompts.$.summarized_content": new_summarized_content,  # Update summarized_content
#                     "lastResponseAt": datetime.now(),
#                 },
#             },
#         )
