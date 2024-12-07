from setuptools import setup, find_packages

setup(
    name="py_own_lang_dect_pkg",  # Replace with your package name
    version="0.1.1",
    description="Fine-tuned BERT model for language detection.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",  # Specify the format of README
    author="aurionpro",
    license="MIT",  # Replace with your license
    packages=find_packages(),  # Automatically find all Python packages
    include_package_data=True,  # Include non-Python files if specified in MANIFEST.in
    package_data={
        "py_own_lang_dect_pkg": ["model/*"],  # Include your model files
    },
    install_requires=[
        "transformers>=4.0.0",  # Add necessary dependencies
        "python-dotenv==1.0.1",
        "torch==2.2.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",  # Specify compatible Python versions
)
