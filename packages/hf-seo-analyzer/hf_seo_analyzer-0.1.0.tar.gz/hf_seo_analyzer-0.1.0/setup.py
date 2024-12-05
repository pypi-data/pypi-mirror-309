from setuptools import setup, find_packages

setup(
    name="hf_seo_analyzer",
    version="0.1.0",
    description="A CLI and programmatic tool to analyze Markdown files for SEO using Huggingface API",
    author="Thinh Vu",
    author_email="mrthinh@live.com",
    url="https://github.com/thinh-vu/hf_seo_analyzer",
    packages=find_packages(),
    install_requires=[
        "requests>=2.0.0",
        "PyYAML>=5.4",
        "argparse>=1.4.0",
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
