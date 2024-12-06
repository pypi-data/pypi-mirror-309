# constants.py

# Copyright (c) 2024 Biprajeet Kar

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# constants.py

# Environment variable defaults
ENV_DEFAULTS = {
    "GENAI_SERVER_HOST": "localhost",
    "GENAI_SERVER_PORT": "8080"
}

UTILS_TEMPLATE = """# utils.py
import yaml
from pathlib import Path

def get_service_config(service_name):
    yaml_path = Path(__file__).parent.parent / "prompt_service.yaml"
    with open(yaml_path, 'r') as file:
        config = yaml.safe_load(file)

    for service in config['PromptServices']:
        if service_name in service:
            return service[service_name]
    raise ValueError(f"Service {service_name} not found in configuration")
"""

# Common imports template
IMPORTS_TEMPLATE = """from {llm_import}
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .utils import get_service_config

# Add required api keys or endpoint if required
"""

# Common chain template
CHAIN_TEMPLATE = """
# Get service configuration
service_config = get_service_config("{service_name}")

# Initialize the LLM
llm = {llm_class}(
    {llm_params}
)

# Create the prompt template
prompt_template = service_config['prompt']

# Create and export the chain
chain = ChatPromptTemplate.from_template(prompt_template) | llm | StrOutputParser()
"""

# Provider-specific configurations
PROVIDER_CONFIGS = {
    "aws": {
        "llm_import": "langchain_aws import ChatBedrockConverse",
        "llm_class": "ChatBedrockConverse",
        "llm_params_template": """model=service_config['model']['modelId'],
    temperature=service_config['model']['temperature'],
    max_tokens=service_config['model']['maxTokens']""",
        "extra_imports": []
    },
    "azure": {
        "llm_import": "langchain_openai import AzureChatOpenAI",
        "llm_class": "AzureChatOpenAI",
        "llm_params_template": """azure_deployment=service_config['model']['modelId'],
    temperature=service_config['model']['temperature'],
    max_tokens=service_config['model']['maxTokens'],
    api_version=service_config['model']['apiVersion']""",
        "extra_imports": ["import os"]
    }
}

# Add this at the end of constants.py

# Base requirements that are always needed
BASE_REQUIREMENTS = [
    "langchain",
    "fastapi",
    "uvicorn",
    "langserve",
    "sse_starlette",
    "python-dotenv",
    "pyyaml"
]

# Provider-specific requirements
PROVIDER_REQUIREMENTS = {
    "aws": ["langchain-aws"],
    "azure": ["langchain-openai"]
}

SERVE_APP_TEMPLATE = """from fastapi import FastAPI
from langserve import add_routes

{imports}

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="App Server", version="1.0", description="GenAI app")

{routes}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app=app, 
        host=os.getenv("GENAI_SERVER_HOST", "localhost"),
        port=int(os.getenv("GENAI_SERVER_PORT", 8080))
    )
"""

IMPORT_CHAIN_TEMPLATE = "from {chain_file} import chain as {chain_var}"
ADD_ROUTE_TEMPLATE = '''add_routes(
    app,
    {chain_var},
    path="/{path}"
)'''

BASE_CHAIN_TEMPLATE = """# base_chain.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from abc import ABC, abstractmethod
from service_chains.utils import get_service_config
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BaseChain(ABC):
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.service_config = get_service_config(service_name)
        self.chain = self._create_chain()

    @abstractmethod
    def _initialize_llm(self):
        \"\"\"Initialize the LLM based on provider configuration\"\"\"
        pass

    def _create_chain(self):
        llm = self._initialize_llm()
        prompt_template = self.service_config['prompt']
        return ChatPromptTemplate.from_template(prompt_template) | llm | StrOutputParser()

    def __call__(self, *args, **kwargs):
        return self.chain(*args, **kwargs)
"""

# Add templates for provider-specific base classes
PROVIDER_BASE_TEMPLATES = {
    "aws": """# aws_chain.py
from .base_chain import BaseChain
from langchain_aws import ChatBedrockConverse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AWSChain(BaseChain):
    def _initialize_llm(self):
        return ChatBedrockConverse(
            model=self.service_config['model']['modelId'],
            temperature=self.service_config['model']['temperature'],
            max_tokens=self.service_config['model']['maxTokens']
        )
""",
    "azure": """# azure_chain.py
from .base_chain import BaseChain
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AzureChain(BaseChain):
    def _initialize_llm(self):
        return AzureChatOpenAI(
            azure_deployment=self.service_config['model']['modelId'],
            temperature=self.service_config['model']['temperature'],
            max_tokens=self.service_config['model']['maxTokens'],
            api_version=self.service_config['model']['apiVersion']
        )
"""
}

SERVICE_CHAIN_TEMPLATE = """# {service_name}_chain.py
from service_chains.base_chains.{provider}_chain import {provider_class}

class {pascal_service_name}Chain({provider_class}):
    def __init__(self):
        super().__init__("{service_name}")

# Initialize chain instance
chain = {pascal_service_name}Chain().chain
"""

FOLDER_STRUCTURE = {
    "base_chains": "service_chains/base_chains",  # For base chain classes
    "service_chains": "service_chains",  # For service-specific chains
}

# Add template for base chains __init__.py
BASE_CHAINS_INIT_TEMPLATE = """from .base_chain import BaseChain
from .aws_chain import AWSChain
from .azure_chain import AzureChain

__all__ = ['BaseChain', 'AWSChain', 'AzureChain']
"""