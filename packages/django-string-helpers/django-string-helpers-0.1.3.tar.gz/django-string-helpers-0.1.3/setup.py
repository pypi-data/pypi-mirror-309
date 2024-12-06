from setuptools import setup, find_packages

setup(
    name="django-string-helpers",
    version="0.1.3",
    author="Rohit Hazare",
    author_email="rohithazare20@gmail.com",
    description="A collection of string helper utilities for Django applications",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/rohit2096/sample-library.git",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=3.2",
    ],
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

