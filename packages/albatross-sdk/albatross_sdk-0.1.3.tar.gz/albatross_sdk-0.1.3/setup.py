from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="albatross-sdk",
    version="0.1.3",
    author="Albatross",
    author_email="developers@usealbatross.ai",
    description="Python SDK for interacting with the Albatross API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/albatross-core/py-sdk",
    project_urls={
        "Bug Tracker": "https://github.com/albatross-core/py-sdk/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src", include=["albatross_sdk*"]),
    python_requires=">=3.12",
    install_requires=[
        "requests>=2.31.0",
        "cryptography>=42.0.0",
        "python-jose>=3.3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "responses>=0.24.0",
            "pyright>=1.1.0",
        ],
    },
)
