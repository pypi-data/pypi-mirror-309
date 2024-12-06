import os
from setuptools import setup, find_packages

# Read the README.md file for long description
current_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="inference-worker",                 # Package name
    version="0.12.0",                         # Initial version
    description="A package to handle ML model inference tasks.",  # Short description
    long_description=long_description,       # Detailed description from README.md
    long_description_content_type="text/markdown",  # README format (Markdown)
    author="Your Name",                      # Your name or the package author's name
    author_email="your.email@example.com",   # Your email
    url="https://github.com/yourusername/inference_worker",  # URL to the repository
    packages=find_packages(),                # Finds all packages in the directory
    install_requires=[                       # Dependencies
        "pika",                       # Pika for handling RabbitMQ
        "requests",                   # Requests for HTTP requests
        "click",
        "python-dotenv",
    ],
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        'inference_worker': ['boilerplate/*']
    },
    include_package_data=True,
    classifiers=[                            # Optional metadata for PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'inference-worker=inference_worker.cli:worker',
        ],
    },
)
