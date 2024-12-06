import os
from InquirerPy import inquirer
import importlib.resources  # For locating resources in the installed package

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

        print("\nService structure generated successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

# Main entry point
def main():
    create_service_structure()

if __name__ == "__main__":
    main()
