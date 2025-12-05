#!/usr/bin/env python3
"""
Setup script for plan-mcp-service
This is a fallback for older pip versions that don't support pyproject.toml fully.
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="plan-mcp-service",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Universal Plan Manager MCP Service for managing tasks, habits, and schedules via LLMs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/plan-mcp-service",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "mcp[cli]>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "plan-mcp-service=plan_mcp_service.server:main",
        ],
    },
    include_package_data=True,
    license="MIT",
)