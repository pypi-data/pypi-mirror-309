from setuptools import setup, find_packages

setup(
    name="technical_analysis_sagar",  # Library name for PyPI
    version="0.1.0",  # Initial version
    description="A comprehensive Python library for technical analysis of financial markets",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sagar Jadhav",  # Replace with your name
    author_email="jadhavsagar750@gmail.com",  # Replace with your email
    url="https://github.com/sagar9187/technical_analysis",  # Replace with your repo URL
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[
        "numpy>=1.21.0",  # For numerical computations
        "pandas>=1.3.0",  # For data manipulation
        "yfinance>=0.2.0",  # For fetching financial data
        "ta>=0.10.1",  # For built-in technical analysis indicators
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Choose your license
        "Operating System :: OS Independent",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Software Development :: Libraries",
        "Topic :: Office/Business :: Financial",
    ],
    keywords="technical-analysis finance trading stock-market crypto forex patterns indicators",  # Relevant keywords
    python_requires=">=3.7",  # Minimum Python version
)
