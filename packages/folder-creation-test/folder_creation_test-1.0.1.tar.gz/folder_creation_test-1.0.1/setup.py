from setuptools import setup, find_packages

setup(
    name='folder-creation-test',
    version='1.0.1',  # Increment the version
    description='CLI tool to generate folder structures for services',
    author='AABK',
    author_email='akhilesh.b@7edge.com',
    url='https://github.com/yourusername/folder-structure-generator-7edge',
    packages=find_packages(),
    package_data={
        "folder_structure_generator_7edge": ["*.yml", "*.py", "*.json"],
    },
    install_requires=[
        'InquirerPy'
    ],
    entry_points={
        'console_scripts': [
            'create=folder_structure_generator_7edge.generator:main',
        ],
    },
)
