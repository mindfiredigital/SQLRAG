from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="sqlrag",  # Your package name
    # version="0.1.1",
    use_scm_version={"local_scheme": "no-local-version"},
    # Avoid using local versions
    setup_requires=[
        "setuptools>=42",
        "setuptools-scm",
    ],  # Use attr to get the version from your package
    description="""An open-source Generative AI (GenAI) application designed to provide users
                  with the flexibility and power to work with various open-source large
                  language models (LLMs). This application serves as a versatile tool,
                  enabling users to interact with and query their data using different
                  AI models and vector databases.""",
    author="Mindfire Digital LLP",
    author_email="abdulla.ansari@mindfiresolutions.com",
    packages=find_packages(
        where="."
    ),  # Specifies that packages are in the root directory
    package_dir={"": "."},  # Root directory is the package directory
    long_description=long_description,
    long_description_content_type="text/markdown",  # or "text/x-rst" if using reStructuredText
    install_requires=[
        "langchain",
        "langchain_experimental",
        "langchain_openai",
        "langchain_community",
        "redis",
        "gpt4all",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
