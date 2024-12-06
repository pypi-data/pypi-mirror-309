import os
import yaml
from InquirerPy import inquirer
import shutil
import importlib.resources  # For locating resources in the installed package


def create_folder_structure_with_files():
    """
    Creates a folder structure in the current working directory and copies all files 
    from the source folder into the newly created structure.

    :param source_folder: The path to the folder containing the files to copy.
    """
    try:
        base_package_path = importlib.resources.files('folder_structure_generator_7edge')

        source_folder = f"{base_package_path}/backend_folder"  # Replace with the actual path

        # Define the root directory (current working directory)
        target_folder = os.getcwd()
        
        os.makedirs(f"{target_folder}/services", exist_ok=True)
        os.makedirs(f"{target_folder}/runbooks", exist_ok=True)



        # Copy all files from the source folder into the target folder
        if os.path.exists(source_folder):
            shutil.copytree(source_folder, target_folder, dirs_exist_ok=True)
            print("Folders created. Please navigate to the service folder and run the 'create' command to set up a new service.")
        else:
            print(f"Source folder '{source_folder}' does not exist.")
    
    except Exception as e:
        print(f"An error occurred while creating the folder structure: {e}")



# Function to create necessary directories
def create_directories(base_dir, folders):
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"Created folder: {folder}")

# Function to create handler files with boilerplate content
def create_handler_files(base_dir, handler_files, language_choice, file_extension):
    for file_name in handler_files:
        file_path = os.path.join(base_dir, "handlers", f"{file_name}.{file_extension}")
        content = ""

        if language_choice == "Python":
            content = """import json
import boto3

def handler(event, context):
    try:
        # Log the event
        print('Event:', json.dumps(event))

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Success'})
        }

    except Exception as error:
        print('Error:', error)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'There was an error while creating the template'})
        }
"""
        else:
            content = """const AWS = require('aws-sdk')

/**
 * AWS Lambda handler function
 * @param {Object} event - Lambda event object
 * @param {Object} context - Lambda context object
 * @returns {Object} Lambda response
 */
module.exports.handler = async (event, context) => {
    try {
        console.log('Event:', JSON.stringify(event))

        return {
            statusCode: 200,
            body: JSON.stringify({ message: 'Success' })
        }

    } catch (error) {
        console.error('Error:', error)
        return {
            statusCode: 500,
            body: JSON.stringify({ message: 'There was an error while creating the template' })
        }
    }
}
"""
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"Created file: {file_path}")

# Function to process template files and replace placeholders
def process_templates(template_files, base_dir, service_name, runtime):
    for template_name, template_path in template_files.items():
        output_file = template_name.replace('-template', '').replace('swagger', f"{service_name.strip()}-management-swagger")
        subfolder = "docs" if any(x in template_name for x in ["swagger", "hooks", "dredd"]) else ""
        output_path = os.path.join(base_dir, subfolder, output_file)

        try:
            with open(template_path, 'r') as template_file:
                content = template_file.read()
                content = content.replace("{{service_name}}", service_name.strip())
                if "serverless" in template_name:
                    content = content.replace("{{runtime}}", runtime)

                with open(output_path, 'w') as file:
                    file.write(content)

            print(f"Created file: {output_path}")
        except FileNotFoundError:
            print(f"Template file not found: {template_path}")

# Function to create the .env file
def create_env_file(base_dir):
    env_file_path = f"{base_dir}/.env"
    with open(env_file_path, 'w') as file:
        file.write("""STAGE=dev
DEBUG=true""")
    print(f"Created file: {env_file_path}")

# Function to check and update serverless-compose.yml
def update_serverless_compose(service_name):
    compose_file = 'serverless-compose.yml'
    
    # Check if the serverless-compose.yml file exists
    if os.path.exists(compose_file):
        print(f"Updating existing {compose_file}...")
        with open(compose_file, 'r') as file:
            compose_data = yaml.safe_load(file) or {}
        
        # Ensure the 'services' section exists
        if 'services' not in compose_data:
            compose_data['services'] = {}

        # Add new service to the services section
        service_path = f"services/{service_name.strip()}"
        compose_data['services'][service_name.strip()] = {
            'path': service_path,
            'config': "serverless.yml"
        }
        
        # Write updated data back to the file
        with open(compose_file, 'w') as file:
            yaml.dump(compose_data, file, default_flow_style=False)
        
        print(f"Service {service_name} added to {compose_file}")

    else:
        print(f"{compose_file} not found, creating a new one...")
        
        # Create initial structure if file doesn't exist
        compose_data = {
            'services': {
                service_name.strip(): {
                    'path': f"services/{service_name.strip()}",
                    'config': "serverless.yml"
                }
            }
        }

        # Write to new file
        with open(compose_file, 'w') as file:
            yaml.dump(compose_data, file, default_flow_style=False)
        
        print(f"Created new {compose_file} with {service_name} service.")

def create_service_structure():
    try:
        # Get the directory where the generator.py script is located
        base_package_path = importlib.resources.files('folder_structure_generator_7edge')

        # Paths to template files inside the package
        template_files = {
            "dredd-template.yml": base_package_path / "dredd-template.yml",
            "serverless-template.yml": base_package_path / "serverless-template.yml",
            "hooks-template.py": base_package_path / "hooks-template.py",
            "swagger-template.json": base_package_path / "swagger-template.json",
        }

        # Prompt user for the service name
        service_name = inquirer.text(message="Enter the service name:").execute()
        if not service_name.strip():
            print("Error: Service name cannot be empty.")
            return

        # Prompt user for the programming language
        language_choice = inquirer.select(
            message="Select the programming language:",
            choices=["Python", "Node.js"]
        ).execute()

        # Determine file extension and runtime based on language choice
        file_extension = "py" if language_choice == "Python" else "js"
        runtime = 'python3.11' if language_choice == 'Python' else 'nodejs14.x'

        # Define base directory for the service
        base_dir = f"services/{service_name.strip()}"

        # Define folder structure
        folders = [
            f"{base_dir}/handlers",
            f"{base_dir}/docs"
        ]
        
        # Create necessary directories
        create_directories(base_dir, folders)

        # Handler files
        handler_files = ["add", "list", "view", "update", "delete"]

        # Create handler files with boilerplate content
        create_handler_files(base_dir, handler_files, language_choice, file_extension)

        # Process template files and replace placeholders
        process_templates(template_files, base_dir, service_name, runtime)

        # Create .env file with environment variables
        create_env_file(base_dir)

        # Update serverless-compose.yml
        update_serverless_compose(service_name)

        print("\nService structure generated successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")




