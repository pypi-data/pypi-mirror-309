from setuptools import setup, find_packages

setup(
    name="PHASE-sc",  
    version="1.0.2",  
    author="Qinhua Wu", 
    author_email="wuqinhua21@mails.ucas.ac.cn",  
    description="PHASE:PHenotype prediction with Attention mechanisms for Single-cell Exploring", 
    long_description=open("README.md").read(), 
    long_description_content_type="text/markdown",  
    url="https://github.com/wuqinhua/PHASE.git",
    packages=find_packages(), 
    classifiers=[
        "Programming Language :: Python :: 3", 
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent", 
    ],
    python_requires=">=3.10", 
    install_requires=[
        "scanpy==1.10.2",  
        "anndata==0.10.8",  
        "tqdm==4.66.4",  
        "numpy>=1.23.5",  
        "pandas>=1.5.3",  
        "scipy>=1.11.4",  
        "seaborn>=0.13.2",  
        "matplotlib==3.6.3", 
        "captum==0.7.0", 
        "scikit-learn>=1.5.1", 
    ],
    entry_points={
        "console_scripts": [
            "PHASEtrain=PHASE.train:main",  
        ],
    },
)

## python setup.py sdist bdist_wheel
## twine upload dist/*

## rm -rf dist/ build/ *.egg-info
## python setup.py sdist bdist_wheel
