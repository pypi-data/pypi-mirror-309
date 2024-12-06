from setuptools import setup, find_packages

setup(
    name="claims-lib",  
    version="0.1.0",  
    author="Ritika Chatterjee",  
    author_email="ritikachat19@gmail.com",  
    description="A collection of utility functions for claim submission app",  # Short description
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown", 
    packages=find_packages(where="src"),  
    package_dir={"": "src"},  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  
)
