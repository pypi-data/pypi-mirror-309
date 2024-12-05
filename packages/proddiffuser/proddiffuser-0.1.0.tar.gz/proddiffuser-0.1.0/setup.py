from pathlib import Path

from setuptools import find_packages, setup

# README.mdを適切なエンコーディングで読み込む
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="proddiffuser",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "torch>=2.1.2",
        "diffusers>=0.31.0",
        "pillow>=9.5.0",
        "transparent-background>=1.3.3",
        "tqdm>=4.65.0",
        "click>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "flake8>=4.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "proddiffuser=proddiffuser.cli:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="Product image background generation and composition tool",  # 英語に変更
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ProdDiffuser",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
