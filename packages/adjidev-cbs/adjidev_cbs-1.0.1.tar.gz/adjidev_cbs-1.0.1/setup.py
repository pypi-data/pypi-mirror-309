from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="adjidev-cbs", 
    version="1.0.1",  
    author="Adjidev",
    author_email="pixelpixx26@gmail.com", 
    description="Cyber brebes system advanced hacking tools",
    long_description=long_description,
    long_description_content_type="text/markdown",  
    url="https://github.com/adjidev/cbs",
    project_urls={
        "Bug Tracker": "https://github.com/adjidev/cbs/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},  
    packages=find_packages(include=["fitur", "fitur.*"]),  
    python_requires=">=3.11",  
    include_package_data=True,  
    install_requires=[
        "setuptools",
    ],
    entry_points={
        "console_scripts": [
            "cbs=cbs:main",
        ],
    },
)
