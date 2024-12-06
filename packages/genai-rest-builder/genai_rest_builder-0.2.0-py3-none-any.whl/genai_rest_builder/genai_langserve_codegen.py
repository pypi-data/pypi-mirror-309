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

import yaml
import os
from typing import Dict, List, Set
from genai_rest_builder.constants import IMPORTS_TEMPLATE, CHAIN_TEMPLATE, PROVIDER_CONFIGS, BASE_REQUIREMENTS, PROVIDER_REQUIREMENTS, \
    SERVE_APP_TEMPLATE, IMPORT_CHAIN_TEMPLATE, ADD_ROUTE_TEMPLATE, ENV_DEFAULTS, UTILS_TEMPLATE, \
    BASE_CHAIN_TEMPLATE, PROVIDER_BASE_TEMPLATES, SERVICE_CHAIN_TEMPLATE, FOLDER_STRUCTURE, BASE_CHAINS_INIT_TEMPLATE


def get_unique_providers(prompt_services: List[Dict]) -> Set[str]:
    """Extract unique providers from prompt services configuration"""
    providers = set()
    for service in prompt_services:
        for service_config in service.values():
            provider = service_config['model']['provider']
            providers.add(provider)
    return providers


def create_folder_structure():
    """Create the required folder structure"""
    for folder in FOLDER_STRUCTURE.values():
        os.makedirs(folder, exist_ok=True)
        # Create __init__.py in each folder
        init_path = os.path.join(folder, "__init__.py")
        if not os.path.exists(init_path):
            with open(init_path, 'w') as f:
                f.write("")


def to_pascal_case(snake_str: str) -> str:
    """Convert snake_case or camelCase to PascalCase"""
    # First split by underscores
    components = snake_str.split('_')

    # Handle camelCase if present
    final_components = []
    for component in components:
        # Split by capital letters in camelCase
        final_components.extend(component)

    # Capitalize each component and join
    return ''.join(word.title() for word in final_components)


def create_base_classes(prompt_services: List[Dict]):
    """
    Create base chain classes in base_chains folder
    Only creates provider-specific base classes that are used in the configuration
    """
    base_chains_dir = FOLDER_STRUCTURE["base_chains"]

    # Create base_chain.py
    with open(f"{base_chains_dir}/base_chain.py", "w") as f:
        f.write(BASE_CHAIN_TEMPLATE)
        print(f"Created base chain class: {base_chains_dir}/base_chain.py")

    # Get unique providers from configuration
    used_providers = get_unique_providers(prompt_services)

    # Create only the necessary provider-specific base classes
    for provider in used_providers:
        if provider in PROVIDER_BASE_TEMPLATES:
            filename = f"{base_chains_dir}/{provider}_chain.py"
            if not os.path.exists(filename):
                with open(filename, "w") as f:
                    f.write(PROVIDER_BASE_TEMPLATES[provider])
                print(f"Created provider base class: {filename}")
            else:
                print(f"Provider base class already exists: {filename}")
        else:
            print(f"Warning: No template available for provider '{provider}'")

    # Create __init__.py with the standard template
    init_path = f"{base_chains_dir}/__init__.py"
    if not os.path.exists(init_path):
        with open(init_path, "w") as f:
            f.write(BASE_CHAINS_INIT_TEMPLATE)


def create_utils_file():
    """Create utils.py in service_chains folder"""
    utils_path = os.path.join(FOLDER_STRUCTURE["service_chains"], "utils.py")
    if not os.path.exists(utils_path):
        with open(utils_path, 'w') as f:
            f.write(UTILS_TEMPLATE)


def create_service_chains_folder(prompt_services: List[Dict]):
    """Create service_chains folder and initialize it"""
    # Create folder structure
    create_folder_structure()

    # Create base classes based on configuration
    create_base_classes(prompt_services)

    # Create utils.py in service_chains folder
    create_utils_file()


def read_yaml_file(file_path: str) -> Dict:
    """
    Read and parse the YAML file
    """
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return {}
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return {}


def generate_chain_code(service_name: str, details: Dict) -> str:
    """Generate service-specific chain class"""
    provider = details['model']['provider']
    provider_class = "AWSChain" if provider == "aws" else "AzureChain"
    pascal_service_name = to_pascal_case(service_name)

    return SERVICE_CHAIN_TEMPLATE.format(
        service_name=service_name,
        pascal_service_name=pascal_service_name,
        provider=provider,
        provider_class=provider_class
    )


def create_service_file(service_name: str, details: Dict) -> None:
    """Create service-specific chain file if it doesn't exist"""
    file_name = f"{service_name}_chain.py"
    file_path = os.path.join(FOLDER_STRUCTURE["service_chains"], file_name)

    # Only create if file doesn't exist
    if not os.path.exists(file_path):
        try:
            content = generate_chain_code(service_name, details)
            with open(file_path, 'w') as file:
                file.write(content)
            print(f"Created file: {file_path}")
        except Exception as e:
            print(f"Error creating file {file_path}: {str(e)}")
    else:
        print(f"File already exists: {file_path}")


def process_services(services: List[Dict]) -> None:
    """
    Process each service and create corresponding Python files
    """
    for service in services:
        for service_name, details in service.items():
            print(f"\nProcessing service: {service_name}")
            create_service_file(service_name, details)


def get_required_packages(services: List[Dict]) -> Set[str]:
    """
    Determine required packages based on providers used in services
    """
    required_packages = set(BASE_REQUIREMENTS)

    # Check each service for its provider and add corresponding requirements
    for service in services:
        for service_details in service.values():
            provider = service_details.get('model', {}).get('provider')
            if provider in PROVIDER_REQUIREMENTS:
                required_packages.update(PROVIDER_REQUIREMENTS[provider])

    return required_packages


def create_requirements_file(packages: Set[str]) -> None:
    """
    Create requirements.txt file with the specified packages
    """
    try:
        with open('requirements.txt', 'w') as file:
            for package in sorted(packages):  # Sort for consistent ordering
                file.write(f"{package}\n")
        print("\nCreated requirements.txt file")
    except Exception as e:
        print(f"\nError creating requirements.txt: {str(e)}")


def create_serve_app(services: List[Dict]) -> None:
    """
    Create serve_app.py file that imports and sets up routes for all chains
    """
    try:
        # Generate imports for each chain
        imports = []
        routes = []

        for service in services:
            for service_name in service.keys():
                # Create chain variable name (avoid potential naming conflicts)
                chain_var = f"chain_{service_name.lower()}"

                # Create import statement
                chain_file = f"service_chains.{service_name}_chain"
                import_stmt = IMPORT_CHAIN_TEMPLATE.format(
                    chain_file=chain_file,
                    chain_var=chain_var
                )
                imports.append(import_stmt)

                # Create add_routes statement
                route_stmt = ADD_ROUTE_TEMPLATE.format(
                    chain_var=chain_var,
                    path=service_name
                )
                routes.append(route_stmt)

        # Combine all components
        content = SERVE_APP_TEMPLATE.format(
            imports="\n".join(imports),
            routes="\n\n".join(routes)
        )

        # Write to file
        with open('serve_app.py', 'w') as file:
            file.write(content)
        print("\nCreated serve_app.py file")

    except Exception as e:
        print(f"\nError creating serve_app.py: {str(e)}")


def create_env_file() -> None:
    """
    Create .env file with default server configuration
    """
    try:
        # Check if .env file exists
        if os.path.exists('.env'):
            print("\n.env file already exists, skipping creation")
            return

        with open('.env', 'w') as file:
            for key, value in ENV_DEFAULTS.items():
                file.write(f"{key}={value}\n")
        print("\nCreated .env file with default configuration")
    except Exception as e:
        print(f"\nError creating .env file: {str(e)}")


def main():
    """Main function to orchestrate the code generation"""
    # File path
    file_path = "prompt_service.yaml"

    # Read YAML file
    yaml_data = read_yaml_file(file_path)

    # Get services array
    prompt_services = yaml_data.get('PromptServices', [])

    if not prompt_services:
        print("No services found in the YAML file")
        return

    # Create necessary folders and base classes based on configuration
    create_service_chains_folder(prompt_services)

    # create env file
    create_env_file()

    # Process services and create files
    process_services(prompt_services)

    # Generate requirements.txt
    required_packages = get_required_packages(prompt_services)
    create_requirements_file(required_packages)

    # Generate serve_app.py
    create_serve_app(prompt_services)

    # Print summary
    print("\nGeneration Summary:")
    print(f"Base Chain Classes ({FOLDER_STRUCTURE['base_chains']}):")
    for provider in get_unique_providers(prompt_services):
        print(f"- {provider}_chain.py")
    print(f"\nService Chain Files ({FOLDER_STRUCTURE['service_chains']}):")
    for service in prompt_services:
        for service_name in service.keys():
            print(f"- {service_name}_chain.py")