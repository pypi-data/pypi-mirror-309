from portkey_ai import Portkey
from typing import Dict, List, Optional
import random
import asyncio
import time
import sys
import tiktoken
import json

from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

def get_token_count(text: str) -> int:
    """
    Get the number of tokens in a text string using tiktoken.
    
    Args:
        text (str): The input text to count tokens for
        
    Returns:
        int: Number of tokens in the text
    """
    try:
        encoding = tiktoken.encoding_for_model("gpt-4o")
        tokens = encoding.encode(text)
        return len(tokens)
    except Exception as e:
        logger.debug(f"Error counting tokens: {str(e)}")
        return 0

def truncate_messages(messages: List[Dict[str, str]], max_tokens: int) -> List[Dict[str, str]]:
    """
    Truncate conversation history to fit within token limit while preserving system prompts.
    Preserves system messages and most recent messages.
    
    Args:
        messages: List of message dictionaries
        max_tokens: Maximum allowed tokens
        
    Returns:
        Truncated message list
    """
    # Separate system messages and other messages
    system_messages = [msg for msg in messages if msg['role'] == 'system']
    other_messages = [msg for msg in messages if msg['role'] != 'system']
    
    system_tokens = sum(get_token_count(json.dumps(msg)) for msg in system_messages)
    remaining_tokens = max_tokens - system_tokens
    
    truncated_messages = system_messages.copy()
    total_tokens = system_tokens
    
    # Add most recent non-system messages that fit
    for msg in reversed(other_messages):
        msg_text = json.dumps(msg)
        tokens = get_token_count(msg_text)
        
        if total_tokens + tokens <= max_tokens:
            truncated_messages.append(msg)
            total_tokens += tokens
            
    # Sort messages back to original order
    truncated_messages.sort(key=lambda x: messages.index(x))
    return truncated_messages

def split_message(message: Dict[str, str], max_tokens: int) -> List[Dict[str, str]]:
    """
    Split a large message into smaller chunks within token limit.
    Preserves message role and splits on sentence boundaries when possible.
    
    Args:
        message: Message dictionary to split
        max_tokens: Maximum tokens per chunk
        
    Returns:
        List of message chunks
    """
    content = message['content']
    role = message['role']
    
    # Don't split system messages
    if role == 'system':
        return [message]
        
    chunks = []
    current_chunk = ''
    current_tokens = 0
    
    # Split on sentences when possible
    sentences = content.replace('\n', '. ').split('. ')
    
    for sentence in sentences:
        sentence = sentence.strip() + '. '
        sentence_tokens = get_token_count(sentence)
        
        if current_tokens + sentence_tokens > max_tokens:
            if current_chunk:
                chunks.append({
                    'role': role,
                    'content': current_chunk.strip()
                })
            current_chunk = sentence
            current_tokens = sentence_tokens
        else:
            current_chunk += sentence
            current_tokens += sentence_tokens
            
    if current_chunk:
        chunks.append({
            'role': role,
            'content': current_chunk.strip()
        })
        
    return chunks

class TokenController:
    """Manages token counts and message processing while preserving message quality"""
    
    MAX_CONTEXT_TOKENS = 200000
    MAX_COMPLETION_TOKENS = 4096
    
    @classmethod
    async def process_messages(cls, messages: List[Dict[str, str]], max_completion_tokens: int) -> List[Dict[str, str]]:
        """
        Process messages to fit within token limits while maintaining quality.
        Preserves system messages and recent context.
        
        Args:
            messages: Input messages
            max_completion_tokens: Maximum completion tokens
            
        Returns:
            Processed messages list
        """
        # Reserve tokens for completion
        max_context_tokens = cls.MAX_CONTEXT_TOKENS - max_completion_tokens
        
        # Count total tokens
        total_tokens = sum(get_token_count(json.dumps(msg)) for msg in messages)
        
        if total_tokens <= max_context_tokens:
            return messages
            
        # First try truncating while preserving system messages
        truncated = truncate_messages(messages, max_context_tokens)
        if truncated:
            return truncated
            
        # If still too large, split non-system messages only
        last_msg = messages[-1]
        if last_msg['role'] != 'system':
            history = messages[:-1]
            history_tokens = sum(get_token_count(json.dumps(msg)) for msg in history)
            remaining_tokens = max_context_tokens - history_tokens
            
            chunks = split_message(last_msg, remaining_tokens)
            return history + chunks
            
        return messages

class BaseModel:
    def __init__(self, api_key: str, virtual_key: str, config_id: str):
        try:
            self.portkey = Portkey(api_key=api_key, virtual_key=virtual_key, config=config_id)
        except Exception as e:
            logger.debug(f"Failed to initialize Portkey: {str(e)}")
            raise

    async def prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        raise NotImplementedError

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        raise NotImplementedError

class AzureModel(BaseModel):

    async def coding_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using AzureModel for prompt")
            processed_messages = await TokenController.process_messages(messages, max_tokens)
            common_params = {
                "messages": processed_messages,
                "temperature": 0.2,
                "top_p": 0.1,
                "max_tokens": max_tokens
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"AzureModel coding_prompt failed: {str(e)}")
            raise

    async def prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using AzureModel for prompt")
            processed_messages = await TokenController.process_messages(messages, max_tokens)
            common_params = {
                "messages": processed_messages,
                "temperature": 0.2,
                "top_p": 0.1,
                "max_tokens": max_tokens
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"AzureModel prompt failed: {str(e)}")
            raise

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        try:
            logger.debug("Using AzureModel for stream_prompt")
            processed_messages = await TokenController.process_messages(messages, max_tokens)
            common_params = {
                "messages": processed_messages,
                "max_tokens": max_tokens,
                "temperature": 0.2,
                "top_p": 0.1,
                "stream": True
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"AzureModel stream_prompt failed: {str(e)}")
            raise

class BedrockModel3(BaseModel):

    async def coding_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using BedrockModel for prompt")
            processed_messages = await TokenController.process_messages(messages, max_tokens)
            common_params = {
                "messages": processed_messages,
                "temperature": 0.2,
                "top_p": 0.1,
                "max_tokens": max_tokens,
                "model": "anthropic.claude-3-5-sonnet-20240620-v1:0"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"BedrockModel coding_prompt failed: {str(e)}")
            raise

    async def prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using BedrockModel for prompt")
            processed_messages = await TokenController.process_messages(messages, max_tokens)
            common_params = {
                "messages": processed_messages,
                "temperature": 0.2,
                "top_p": 0.1,
                "max_tokens": max_tokens,
                "model": "anthropic.claude-3-5-sonnet-20240620-v1:0"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"BedrockModel prompt failed: {str(e)}")
            raise

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        try:
            logger.debug("Using BedrockModel for stream_prompt")
            processed_messages = await TokenController.process_messages(messages, max_tokens)
            common_params = {
                "messages": processed_messages,
                "max_tokens": max_tokens,
                "temperature": 0.2,
                "top_p": 0.1,
                "stream": True,
                "model": "anthropic.claude-3-5-sonnet-20240620-v1:0"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"BedrockModel stream_prompt failed: {str(e)}")
            raise
    
    def generate_image(self, prompt: str, model: str):
        try:
            return self.portkey.images.generate(
                prompt=prompt,
                model=model
            )
        except Exception as e:
            logger.debug(f"BedrockModel generate_image failed: {str(e)}")
            raise

class BedrockModel2(BaseModel):

    async def coding_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using BedrockModel2 for prompt")
            processed_messages = await TokenController.process_messages(messages, max_tokens)
            common_params = {
                "messages": processed_messages,
                "temperature": 0.2,
                "top_p": 0.1,
                "max_tokens": max_tokens,
                "model": "anthropic.claude-3-5-sonnet-20241022-v2:0"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"BedrockModel2 coding_prompt failed: {str(e)}")
            raise

    async def prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using BedrockModel2 for prompt")
            processed_messages = await TokenController.process_messages(messages, max_tokens)
            common_params = {
                "messages": processed_messages,
                "temperature": 0.2,
                "top_p": 0.1,
                "max_tokens": max_tokens,
                "model": "anthropic.claude-3-5-sonnet-20241022-v2:0"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"BedrockModel2 prompt failed: {str(e)}")
            raise

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        try:
            logger.debug("Using BedrockModel2 for stream_prompt")
            processed_messages = await TokenController.process_messages(messages, max_tokens)
            common_params = {
                "messages": processed_messages,
                "max_tokens": max_tokens,
                "temperature": 0.2,
                "top_p": 0.1,
                "stream": True,
                "model": "anthropic.claude-3-5-sonnet-20241022-v2:0"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"BedrockModel2 stream_prompt failed: {str(e)}")
            raise
    
    def generate_image(self, prompt: str, model: str):
        try:
            return self.portkey.images.generate(
                prompt=prompt,
                model=model
            )
        except Exception as e:
            logger.debug(f"BedrockModel2 generate_image failed: {str(e)}")
            raise

class BedrockModel(BaseModel):

    async def coding_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using BedrockModel for prompt")
            processed_messages = await TokenController.process_messages(messages, max_tokens)
            common_params = {
                "messages": processed_messages,
                "temperature": 0.2,
                "top_p": 0.1,
                "max_tokens": max_tokens,
                "model": "anthropic.claude-3-5-sonnet-20240620-v1:0"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"BedrockModel coding_prompt failed: {str(e)}")
            raise

    async def prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using BedrockModel for prompt")
            processed_messages = await TokenController.process_messages(messages, max_tokens)
            common_params = {
                "messages": processed_messages,
                "temperature": 0.2,
                "top_p": 0.1,
                "max_tokens": max_tokens,
                "model": "anthropic.claude-3-5-sonnet-20240620-v1:0"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"BedrockModel prompt failed: {str(e)}")
            raise

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        try:
            logger.debug("Using BedrockModel for stream_prompt")
            processed_messages = await TokenController.process_messages(messages, max_tokens)
            common_params = {
                "messages": processed_messages,
                "max_tokens": max_tokens,
                "temperature": 0.2,
                "top_p": 0.1,
                "stream": True,
                "model": "anthropic.claude-3-5-sonnet-20240620-v1:0"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"BedrockModel stream_prompt failed: {str(e)}")
            raise
    
    def generate_image(self, prompt: str, model: str):
        try:
            return self.portkey.images.generate(
                prompt=prompt,
                model=model
            )
        except Exception as e:
            logger.debug(f"BedrockModel generate_image failed: {str(e)}")
            raise

class GeminiModel(BaseModel):

    async def coding_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using BedrockModel for prompt")
            processed_messages = await TokenController.process_messages(messages, max_tokens)
            common_params = {
                "messages": processed_messages,
                "temperature": 0.2,
                "top_p": 0.1,
                "max_tokens": max_tokens,
                "model": "gemini-1.5-pro"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"GeminiModel coding_prompt failed: {str(e)}")
            raise

    async def prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        try:
            logger.debug("Using GeminiModel for prompt")
            processed_messages = await TokenController.process_messages(messages, max_tokens)
            common_params = {
                "messages": processed_messages,
                "temperature": 0.2,
                "top_p": 0.1,
                "max_tokens": max_tokens,
                "model": "gemini-1.5-pro"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.debug(f"GeminiModel prompt failed: {str(e)}")
            raise

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        try:
            logger.debug("Using GeminiModel for stream_prompt")
            processed_messages = await TokenController.process_messages(messages, max_tokens)
            common_params = {
                "messages": processed_messages,
                "max_tokens": max_tokens,
                "temperature": 0.2,
                "top_p": 0.1,
                "stream": True,
                "model": "gemini-1.5-pro"
            }
            return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
        except Exception as e:
            logger.error(f"GeminiModel stream_prompt failed: {str(e)}")
            raise

class DalleModel(BaseModel):
    def generate_image(self, prompt: str, size: str = "1024x1024"):
        try:
            logger.debug("Using DALL-E 3 for image generation")
            return self.portkey.images.generate(prompt=prompt, size=size)
        except Exception as e:
            logger.debug(f"DalleModel generate_image failed: {str(e)}")
            raise

class AIGateway:
    _instance = None

    API_KEY = "Tf7rBh3ok+wNy+hzHum7dmizdBFh"
    CONFIG_ID = "pc-zinley-74e593"
    
    VIRTUAL_KEYS: Dict[str, str] = {
        "azure1": "azure-4667e4",
        "azure2": "azure-7e4746", 
        "bedrock": "bedrock-bfa916",
        "bedrock2": "bedrock-1c7d76",
        "bedrock3": "bedrock-1c7d76",
        "gemini": "gemini-b5d385",
        "dalle3_1": "dalle3-34c86a",
        "dalle3_2": "dalle3-ea9815"
    }
    ARCH_STEAM_WEIGHTS = {
        "azure1": 0.35,
        "azure2": 0.35,
        "bedrock": 0.1,
        "bedrock2": 0.1,
        "bedrock3": 0.1
    }

    MODEL_WEIGHTS = {
        "azure1": 0.35,
        "azure2": 0.35,
        "bedrock": 0.1,
        "bedrock2": 0.1,
        "bedrock3": 0.1
    }

    STREAM_MODEL_WEIGHTS = {
        "azure1": 0.35,
        "azure2": 0.35,
        "bedrock": 0.1,
        "bedrock2": 0.1,
        "bedrock3": 0.1
    }

    STREAM_EXPLAINER_MODEL_WEIGHTS = {
        "azure1": 0.35,
        "azure2": 0.35,
        "bedrock": 0.1,
        "bedrock2": 0.1,
        "bedrock3": 0.1
    }

    STREAM_Architect_MODEL_WEIGHTS = {
       "azure1": 0.3,
       "azure2": 0.3,
       "bedrock": 0.1,
       "bedrock2": 0.15,
       "bedrock3": 0.15
    }

    Architect_MODEL_WEIGHTS = {
       "azure1": 0.3,       "azure2": 0.3,
       "bedrock": 0.1,
       "bedrock2": 0.15,
       "bedrock3": 0.15
    }

    CODING_MODEL_WEIGHTS = {
       "bedrock2": 0.3,
       "bedrock3": 0.3,
       "bedrock": 0.2,
       "azure1": 0.1,
       "azure2": 0.1
    }

    FREE_IMAGE_MODEL_WEIGHTS = {
        "dalle3_1": 0.167,
        "dalle3_2": 0.167,
        "sdxl": 0.167,
        "sdxl2": 0.167,
        "stable_core": 0.166,
        "stable_core2": 0.166,
    }

    PRO_IMAGE_MODEL_WEIGHTS = {
        "sd": 0.25,
        "sd2": 0.25,
        "stable_ultra": 0.25,
        "stable_ultra2": 0.25,
        "dalle3_1": 0.05,
        "dalle3_2": 0.05,
    }

    def __new__(cls):
        if cls._instance is None:
            try:
                cls._instance = super(AIGateway, cls).__new__(cls)
                cls._instance.azure1_model = AzureModel(cls.API_KEY, cls.VIRTUAL_KEYS["azure1"], cls.CONFIG_ID)
                cls._instance.azure2_model = AzureModel(cls.API_KEY, cls.VIRTUAL_KEYS["azure2"], cls.CONFIG_ID)
                cls._instance.bedrock3_model = BedrockModel3(cls.API_KEY, cls.VIRTUAL_KEYS["bedrock3"], cls.CONFIG_ID)
                cls._instance.bedrock2_model = BedrockModel2(cls.API_KEY, cls.VIRTUAL_KEYS["bedrock2"], cls.CONFIG_ID)
                cls._instance.bedrock_model = BedrockModel(cls.API_KEY, cls.VIRTUAL_KEYS["bedrock"], cls.CONFIG_ID)
                cls._instance.gemini_model = GeminiModel(cls.API_KEY, cls.VIRTUAL_KEYS["gemini"], cls.CONFIG_ID)
                cls._instance.dalle3_1_model = DalleModel(cls.API_KEY, cls.VIRTUAL_KEYS["dalle3_1"], cls.CONFIG_ID)
                cls._instance.dalle3_2_model = DalleModel(cls.API_KEY, cls.VIRTUAL_KEYS["dalle3_2"], cls.CONFIG_ID)
                cls._instance.model_usage_count = {}
                logger.debug("AIGateway initialized with all models")
            except Exception as e:
                logger.error(f"Failed to initialize AI models")
                raise
        return cls._instance

    def _has_image_content(self, messages: List[Dict[str, str]]) -> bool:
        for message in messages:
            if isinstance(message.get('content'), list):
                for content in message['content']:
                    if isinstance(content, dict) and content.get('type') == 'image_url':
                        return True
        return False

    def _select_model(self, weights, exclude=None, messages=None):
        try:
            # If messages contain images, exclude gemini from available models
            if messages and self._has_image_content(messages):
                if exclude is None:
                    exclude = set()
                exclude.add('gemini')
                logger.debug("Image content detected - excluding Gemini model")

            for model in weights:
                if model not in self.model_usage_count:
                    self.model_usage_count[model] = 0

            total_usage = sum(self.model_usage_count[model] for model in weights)
            if total_usage == 0:
                available_models = [model for model in weights if model not in (exclude or set())]
                if not available_models:
                    logger.debug("No available models to choose from")
                    raise ValueError("No available models to choose from")
                
                weights_list = [(model, weights[model]) for model in available_models]
                selected_model = random.choices(
                    population=[m[0] for m in weights_list],
                    weights=[m[1] for m in weights_list],
                    k=1
                )[0]
            else:
                available_models = [model for model in weights if model not in (exclude or set())]
                if not available_models:
                    logger.debug("No available models to choose from")
                    raise ValueError("No available models to choose from")
                
                ratio_diffs = []
                for model in available_models:
                    current_ratio = self.model_usage_count[model] / total_usage
                    target_ratio = weights[model] / sum(weights[m] for m in available_models)
                    ratio_diffs.append((model, target_ratio - current_ratio))
                
                selected_model = max(ratio_diffs, key=lambda x: x[1])[0]

            self.model_usage_count[selected_model] += 1
            
            logger.debug(f"Selected model: {selected_model} (usage count: {self.model_usage_count[selected_model]})")
            return selected_model
            
        except Exception as e:
            logger.error(f"Error in model selection")
            raise

    async def prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0) -> Dict:
        logger.debug("Starting prompt method")
        tried_models = set()
        while len(tried_models) < len(self.MODEL_WEIGHTS):
            try:
                model_type = self._select_model(self.MODEL_WEIGHTS, exclude=tried_models, messages=messages)
                logger.debug(f"Attempting to use {model_type} model\n")
                model = getattr(self, f"{model_type}_model")
                completion = await model.prompt(messages, max_tokens, temperature, top_p)
                logger.debug(f"Successfully received response from {model_type} model")
                return completion
            except Exception as e:
                tried_models.add(model_type)
                if "429" in str(e):
                    logger.debug(f"Rate limit exceeded for {model_type} model: {str(e)}")
                else:
                    logger.debug(f"Error in prompting {model_type} model: {str(e)}")
                await asyncio.sleep(2)
        
        logger.error("All models failed to respond")
        raise Exception("All models failed to respond")
    
    async def arch_prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0) -> Dict:
        logger.debug("Starting arch_prompt method")
        tried_models = set()
        while len(tried_models) < len(self.Architect_MODEL_WEIGHTS):
            try:
                model_type = self._select_model(self.Architect_MODEL_WEIGHTS, exclude=tried_models, messages=messages)
                logger.debug(f"Attempting to use {model_type} model for architecture\n")
                model = getattr(self, f"{model_type}_model")
                completion = await model.prompt(messages, max_tokens, temperature, top_p)
                logger.debug(f"Successfully received response from {model_type} model for architecture")
                return completion
            except Exception as e:
                tried_models.add(model_type)
                if "429" in str(e):
                    logger.debug(f"Rate limit exceeded for {model_type} model in arch_prompt: {str(e)}")
                else:
                    logger.debug(f"Error in arch_prompt with {model_type} model: {str(e)}")
                await asyncio.sleep(2)
        
        logger.error("All models failed to respond for arch_prompt")
        raise Exception("All models failed to respond for arch_prompt")
    
    async def coding_prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0) -> Dict:
        logger.debug("Starting coding_prompt method")
        tried_models = set()
        while len(tried_models) < len(self.CODING_MODEL_WEIGHTS):
            try:
                model_type = self._select_model(self.CODING_MODEL_WEIGHTS, exclude=tried_models, messages=messages)
                logger.debug(f"Attempting to use {model_type} model\n")
                model = getattr(self, f"{model_type}_model")
                completion = await model.coding_prompt(messages, max_tokens, temperature, top_p)
                logger.debug(f"Successfully received response from {model_type} model")
                return completion
            except Exception as e:
                tried_models.add(model_type)
                if "429" in str(e):
                    logger.debug(f"Rate limit exceeded for {model_type} model in coding_prompt: {str(e)}")
                else:
                    logger.debug(f"Error in coding_prompt with {model_type} model: {str(e)}")
                await asyncio.sleep(2)
        
        logger.error("All models failed to respond in coding_prompt")
        raise Exception("All models failed to respond")

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        logger.debug("Starting stream_prompt method")
        tried_models = set()
        while len(tried_models) < len(self.STREAM_MODEL_WEIGHTS):
            try:
                model_type = self._select_model(self.STREAM_MODEL_WEIGHTS, exclude=tried_models, messages=messages)
                logger.debug(f"Attempting to use {model_type} model for streaming\n")
                model = getattr(self, f"{model_type}_model")
                chat_completion_stream = await model.stream_prompt(messages, max_tokens, temperature, top_p)
                logger.debug(f"Successfully received streaming response from {model_type} model")
                final_response = ""
                for chunk in chat_completion_stream:
                    if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        # Write content as UTF-8 encoded bytes to stdout
                        sys.stdout.buffer.write(content.encode('utf-8'))
                        sys.stdout.flush()
                        final_response += content
                # Ensure the cursor moves to the next line after streaming is complete
                print()
                return final_response
            except Exception as e:
                tried_models.add(model_type)
                if "429" in str(e):
                    logger.debug(f"Rate limit exceeded for {model_type} model in stream_prompt: {str(e)}")
                else:
                    logger.debug(f"Error in stream_prompt with {model_type} model: {str(e)}")
                await asyncio.sleep(2)

        logger.error("All models failed to respond for stream prompt")
        raise Exception("All models failed to respond")

    
    async def explainer_stream_prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0):
        logger.debug("Starting explainer_stream_prompt method")
        tried_models = set()
        while len(tried_models) < len(self.STREAM_EXPLAINER_MODEL_WEIGHTS):
            try:
                model_type = self._select_model(self.STREAM_EXPLAINER_MODEL_WEIGHTS, exclude=tried_models, messages=messages)
                logger.debug(f"Attempting to use {model_type} model for streaming\n")
                model = getattr(self, f"{model_type}_model")
                chat_completion_stream = await model.stream_prompt(messages, max_tokens, temperature, top_p)
                logger.debug(f"Successfully received streaming response from {model_type} model")
                final_response = ""
                for chunk in chat_completion_stream:
                    if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        # Write content as UTF-8 encoded bytes to stdout
                        sys.stdout.buffer.write(content.encode('utf-8'))
                        sys.stdout.flush()
                        final_response += content
                print()
                return final_response
            except Exception as e:
                tried_models.add(model_type)
                if "429" in str(e):
                    logger.debug(f"Rate limit exceeded for {model_type} model in explainer_stream_prompt: {str(e)}")
                else:
                    logger.debug(f"Error in explainer_stream_prompt with {model_type} model: {str(e)}")
                await asyncio.sleep(2)
        
        logger.error("All models failed to respond for explainer stream prompt")
        raise Exception("All models failed to respond")
    
    async def arch_stream_prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0):
        logger.debug("Starting arch_stream_prompt method")
        tried_models = set()
        while len(tried_models) < len(self.ARCH_STEAM_WEIGHTS):
            try:
                model_type = self._select_model(self.ARCH_STEAM_WEIGHTS, exclude=tried_models, messages=messages)
                logger.debug(f"Attempting to use {model_type} model for streaming\n")
                model = getattr(self, f"{model_type}_model")
                chat_completion_stream = await model.stream_prompt(messages, max_tokens, temperature, top_p)
                logger.debug(f"Successfully received streaming response from {model_type} model")
                final_response = ""
                for chunk in chat_completion_stream:
                    if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        # Write content as UTF-8 encoded bytes to stdout
                        sys.stdout.buffer.write(content.encode('utf-8'))
                        sys.stdout.flush()
                        final_response += content
                print()
                return final_response
            except Exception as e:
                tried_models.add(model_type)
                if "429" in str(e):
                    logger.debug(f"Rate limit exceeded for {model_type} model in arch_stream_prompt: {str(e)}")
                else:
                    logger.debug(f"Error in arch_stream_prompt with {model_type} model: {str(e)}")
                await asyncio.sleep(2)
        
        logger.error("All models failed to respond for arch stream prompt")
        raise Exception("All models failed to respond")


    def generate_image(self, prompt: str, size: str = "1024x1024", tier: str = "Free"):
        logger.debug("Starting image generation")
        tried_models = set()
        
        if tier == "Free":
            weights_to_try = [self.FREE_IMAGE_MODEL_WEIGHTS]
        else:
            # For Pro tier, combine PRO and FREE weights, excluding any duplicates
            pro_weights = self.PRO_IMAGE_MODEL_WEIGHTS.copy()
            free_weights = {k: v for k, v in self.FREE_IMAGE_MODEL_WEIGHTS.items() 
                          if k not in pro_weights}
            weights_to_try = [pro_weights, free_weights]
            
        for current_weights in weights_to_try:
            while len(tried_models) < len(current_weights):
                try:
                    model_type = self._select_model(current_weights, exclude=tried_models)
                    if model_type.startswith("dalle3"):
                        model = getattr(self, f"{model_type}_model")
                        return model.generate_image(prompt, size)
                    elif model_type == "sdxl":
                        return self.bedrock2_model.generate_image(prompt, model="stability.stable-diffusion-xl-v1")
                    elif model_type == "sdxl2":
                        return self.bedrock_model.generate_image(prompt, model="stability.stable-diffusion-xl-v1")
                    elif model_type == "sd":
                        return self.bedrock2_model.generate_image(prompt, model="stability.sd3-large-v1:0")
                    elif model_type == "sd2":
                        return self.bedrock_model.generate_image(prompt, model="stability.sd3-large-v1:0")
                    elif model_type == "stable_ultra":
                        return self.bedrock2_model.generate_image(prompt, model="stability.stable-image-ultra-v1:0")
                    elif model_type == "stable_ultra2":
                        return self.bedrock_model.generate_image(prompt, model="stability.stable-image-ultra-v1:0")
                    elif model_type == "stable_core":
                        return self.bedrock2_model.generate_image(prompt, model="stability.stable-image-core-v1:0")
                    else:  # stable_core2
                        return self.bedrock_model.generate_image(prompt, model="stability.stable-image-core-v1:0")
                except Exception as e:
                    logger.debug(f"Failed to generate image with {model_type}: {str(e)}")
                    tried_models.add(model_type)
                    time.sleep(1)  # Wait 1 second before trying next model
                    continue
        
        logger.error("All image generation models failed")
        raise Exception("All image generation models failed")
