import os
from InquirerPy import inquirer

def create_service_structure():
    try:
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

        # Determine file extension based on language choice
        file_extension = "py" if language_choice == "Python" else "js"
        runtime = 'python3.11' if language_choice == 'Python' else 'nodejs14.x'

        # Define base directory for the service
        base_dir = f"services/{service_name.strip()}"
        
        # Define folder structure
        folders = [
            f"{base_dir}/handlers",
            f"{base_dir}/docs"
        ]

        # Create directories
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
            print(f"Created folder: {folder}")

        # Define handler files
        handler_files = ["add", "list", "view", "update", "delete"]

        # Create handler files with boilerplate content
        for file_name in handler_files:
            file_path = os.path.join(base_dir, "handlers", f"{file_name}.{file_extension}")

            with open(file_path, 'w') as file:
                if language_choice == "Python":
                    file.write("""import json
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
""")
                else:
                    file.write("""const AWS = require('aws-sdk')

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
""")
            print(f"Created file: {file_path}")

        # Create .env file with variables
        env_file_path = f"{base_dir}/.env"
        with open(env_file_path, 'w') as file:
            file.write("""STAGE=dev
DEBUG=true""")
        print(f"Created file: {env_file_path}")

        # Create other additional files
        additional_files = [
            f"{base_dir}/docs/{service_name.strip()}-management-swagger.json",
            f"{base_dir}/docs/hooks.py",
            f"{base_dir}/serverless.yml"
        ]

        for file_path in additional_files:
            with open(file_path, 'w') as file:
                file.write(f"# {os.path.basename(file_path)} file\n")
            print(f"Created file: {file_path}")

        # Template processing code
        for template_info in [
            ("dredd-template.yml", "dredd.yml", "docs"),
            ("serverless-template.yml", "serverless.yml", ""),
            ("hooks-template.py", "hooks.py", "docs"),
            ("swagger-template.json", f"{service_name.strip()}-management-swagger.json", "docs"),

        ]:
            template_path, output_file, subfolder = template_info
            
            try:
                with open(template_path, 'r') as template_file:
                    template_content = template_file.read()
                    
                    # Replace placeholders
                    template_content = template_content.replace("{{service_name}}", service_name.strip())
                    if "serverless" in template_path:
                        template_content = template_content.replace("{{runtime}}", runtime)
                    
                    # Create output file
                    output_path = os.path.join(base_dir, subfolder, output_file) if subfolder else os.path.join(base_dir, output_file)
                    with open(output_path, 'w') as output_file:
                        output_file.write(template_content)
                    
                    print(f"Created file: {output_path}")
            except FileNotFoundError:
                print(f"Warning: Template file {template_path} not found. Skipping...")

        print("\nService structure generated successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

# Main entry point
def main():
    create_service_structure()

if __name__ == "__main__":
    main()