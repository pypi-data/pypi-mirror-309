from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lemenv",
    version="0.1.0",
    author="GenAIJake",
    author_email="contact@genaijake.com",
    description="A powerful and user-friendly virtual environment manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jakerains/lemenv",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "click>=8.0.0",
        "colorama>=0.4.4",
        "inquirer>=3.1.0",
    ],
    entry_points={
        "console_scripts": [
            "lemenv=lemenv.cli:cli",
        ],
    },
    include_package_data=True,
    keywords="virtual environment, venv, virtualenv, environment manager",
) 