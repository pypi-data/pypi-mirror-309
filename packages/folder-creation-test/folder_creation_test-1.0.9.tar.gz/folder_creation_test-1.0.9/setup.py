from setuptools import setup, find_packages
setup(
    name='folder-creation-test',
    version='1.0.9',
    description='CLI tool to generate folder structures for services',
    author='AABK',
    author_email='akhilesh.b@7edge.com',
    url='https://github.com/yourusername/folder-structure-generator-7edge',
    packages=find_packages(),
    include_package_data=True,  # Include files specified in MANIFEST.in
    package_data={
        '': ['*.yml', '*.json'],  # Include specific file types
        'folder_structure_generator_7edge': [
            'backend_folder/*',  # Files directly in backend_folder
            'backend_folder/*/*'  # Files in subdirectories of backend_folder
        ]    
    },
    install_requires=[
        'InquirerPy',
        'pyyaml',  # Add pyyaml for YAML file handling
    ],
    entry_points={
        'console_scripts': [
            'start=folder_structure_generator_7edge.generator:create_folder_structure_with_files',  # Additional command
            'create=folder_structure_generator_7edge.generator:create_service',
            
        ],
    },
)
