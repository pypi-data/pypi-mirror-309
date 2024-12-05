from setuptools import setup, find_packages

setup(
    name="causal-factory",
    version="0.1",
    description="A placeholder for the causal-factory package",
    long_description="This is a placeholder package to reserve the name causal-factory package. The full functionality will be added in future versions.",
    long_description_content_type="text/markdown",
    author="Awadelrahman M. A. Ahmed",
    author_email="awadrahman@gmail.com",
    url="https://github.com/Awadelrahman/causal-factory",  # Link to the GitHub repo (optional)
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "mlflow>=2.0.0",  
        "pandas>=1.0.0",
        "gastle",
        "torch"
    ],
)