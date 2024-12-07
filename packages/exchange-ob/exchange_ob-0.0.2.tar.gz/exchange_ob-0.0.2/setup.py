from setuptools import setup, find_packages

setup(
    name="exchange-ob",  
    version="0.0.2",  
    packages=find_packages(),  
    install_requires=[
        "websockets>=13.1"
    ],
    author="Nischay Vaish",
    author_email="nischay.vaish@triremetrading.com",
    description="Its used to connect and trade with cryptocurrency exchanges.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Tower-Chain-Digital/exchange-ob", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Minimum Python version required
)