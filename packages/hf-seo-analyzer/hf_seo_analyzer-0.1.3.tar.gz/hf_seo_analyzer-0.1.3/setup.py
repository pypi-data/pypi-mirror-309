from setuptools import setup, find_packages

setup(
    name="hf_seo_analyzer",
    version="0.1.3",
    description="A CLI and programmatic tool to analyze Markdown files for SEO using Huggingface API",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Thinh Vu",
    author_email="mrthinh@live.com",
    url="https://github.com/thinh-vu/hf_seo_analyzer",
    packages=find_packages(),
    install_requires=[
        "requests",
        "PyYAML",
        "argparse",
    ],
    entry_points={
        "console_scripts": [
            "hf-seo-analyzer=hf_seo_analyzer.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
