# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fvg_trading_bot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'yfinance>=0.2.36',
        'pandas>=2.0.0',
        'numpy>=1.24.0',
        'python-dateutil>=2.8.2',
        'requests>=2.31.0',
        'aiohttp>=3.9.0',
        'asyncio>=3.4.3',
        'typing-extensions>=4.7.0',
        'matplotlib>=3.8.0',
        'seaborn>=0.13.0',
        'cycler>=0.12.0',
        'kiwisolver>=1.4.0',
        'pyparsing>=3.1.0',
        'scipy>=1.11.0',
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A trading bot that implements fair value gap strategy with break of structure confirmation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/fvg_trading_bot",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'fvg_trading_bot=fvg_trading_bot.examples.main:main',
        ],
    },
    package_data={
        'fvg_trading_bot': ['README.md', 'LICENSE'],
    },
)